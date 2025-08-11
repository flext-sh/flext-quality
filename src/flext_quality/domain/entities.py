"""Domain entities for FLEXT-QUALITY v0.7.0.

REFACTORED:
            Using flext-core modern patterns - NO duplication.
All entities use mixins from flext-core for maximum code reduction.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from flext_core import FlextEntity, FlextResult, FlextTypes
from pydantic import BaseModel, Field


class FlextDomainEvent(BaseModel):
    """Base class for domain events."""

    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class IssueSeverity(StrEnum):
    """Issue severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueType(StrEnum):
    """Issue types."""

    SYNTAX = "syntax"
    STYLE = "style"
    COMPLEXITY = "complexity"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    DUPLICATION = "duplication"
    DEAD_CODE = "dead_code"
    TYPING = "typing"
    DOCUMENTATION = "documentation"


class AnalysisStatus(StrEnum):
    """Analysis status for quality analysis."""

    QUEUED = "queued"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class QualityProject(FlextEntity):
    """Quality project domain entity using enhanced mixins for code reduction."""

    # Project identification
    name: str = Field(..., min_length=1)
    # Project paths
    project_path: str = Field(..., min_length=1)
    repository_url: str | None = None

    # Configuration
    config_path: str | None = None
    language: str = Field(default="python")

    # Analysis settings
    auto_analyze: bool = Field(default=True)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for quality project."""
        if not self.project_path:
            return FlextResult.fail("Project path is required")
        return FlextResult.ok(None)

    analysis_schedule: str | None = None  # cron format

    # Quality thresholds
    min_coverage: float = Field(default=95.0, ge=0.0, le=100.0)
    max_complexity: int = Field(default=10, ge=1)
    max_duplication: float = Field(default=5.0, ge=0.0, le=100.0)

    # Statistics
    last_analysis_at: datetime | None = None
    total_analyses: int = Field(default=0)

    def update_last_analysis(self) -> QualityProject:
        """Update last analysis timestamp and return new instance."""
        return self.model_copy(
            update={
                "last_analysis_at": datetime.now(UTC),
                "total_analyses": self.total_analyses + 1,
            },
        )


class QualityAnalysis(FlextEntity):
    """Quality analysis domain entity using enhanced mixins for code reduction."""

    project_id: str = Field(..., description="Associated project ID")

    # Analysis identification
    commit_hash: str | None = None
    branch: str | None = None
    pull_request_id: str | None = None

    # Timing
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    duration_seconds: float | None = None

    # Metrics
    total_files: int = Field(default=0)
    total_lines: int = Field(default=0)
    code_lines: int = Field(default=0)
    comment_lines: int = Field(default=0)
    blank_lines: int = Field(default=0)

    # Quality scores
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    coverage_score: float = Field(default=0.0, ge=0.0, le=100.0)
    complexity_score: float = Field(default=0.0, ge=0.0, le=100.0)
    duplication_score: float = Field(default=0.0, ge=0.0, le=100.0)
    security_score: float = Field(default=0.0, ge=0.0, le=100.0)
    maintainability_score: float = Field(default=0.0, ge=0.0, le=100.0)

    # Issue counts
    total_issues: int = Field(default=0)
    critical_issues: int = Field(default=0)
    high_issues: int = Field(default=0)
    medium_issues: int = Field(default=0)
    low_issues: int = Field(default=0)

    # Analysis status
    status: AnalysisStatus = Field(default=AnalysisStatus.QUEUED)

    # Analysis data
    analysis_config: FlextTypes.Core.JsonDict = Field(default_factory=dict)

    def start_analysis(self) -> QualityAnalysis:
        """Start analysis and return new instance."""
        return self.model_copy(
            update={
                "started_at": datetime.now(UTC),
                "status": AnalysisStatus.ANALYZING,
            },
        )

    def complete_analysis(self) -> QualityAnalysis:
        """Complete analysis and return new instance."""
        completed_at = datetime.now(UTC)
        duration_seconds = None
        if self.started_at:
            duration = completed_at - self.started_at
            duration_seconds = duration.total_seconds()

        return self.model_copy(
            update={
                "completed_at": completed_at,
                "status": AnalysisStatus.COMPLETED,
                "duration_seconds": duration_seconds,
            },
        )

    def fail_analysis(self, error: str) -> QualityAnalysis:
        """Fail analysis and return new instance."""
        completed_at = datetime.now(UTC)
        duration_seconds = None
        if self.started_at:
            duration = completed_at - self.started_at
            duration_seconds = duration.total_seconds()

        return self.model_copy(
            update={
                "completed_at": completed_at,
                "status": AnalysisStatus.FAILED,
                "duration_seconds": duration_seconds,
                # Store error message in overall_quality_score for debugging
                "overall_quality_score": 0.0,  # Failed analysis gets 0 score
                # Log error for debugging (used argument to satisfy linter)
                "analysis_config": {**self.analysis_config, "error": error},
            },
        )

    def calculate_overall_score(self) -> QualityAnalysis:
        """Calculate overall score and return new instance."""
        scores = [
            self.coverage_score,
            self.complexity_score,
            self.duplication_score,
            self.security_score,
            self.maintainability_score,
        ]
        overall_score = sum(scores) / len(scores)
        return self.model_copy(update={"overall_score": overall_score})

    @property
    def is_completed(self) -> bool:
        """Check if analysis is completed (either succeeded or failed)."""
        return self.status in {AnalysisStatus.COMPLETED, AnalysisStatus.FAILED}

    @property
    def successful(self) -> bool:
        """Check if analysis completed successfully."""
        return self.status == AnalysisStatus.COMPLETED

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for quality analysis."""
        if not self.project_id:
            return FlextResult.fail("Project ID is required")
        return FlextResult.ok(None)


class QualityIssue(FlextEntity):
    """Quality issue domain entity using enhanced mixins for code reduction."""

    analysis_id: str = Field(..., description="Associated analysis ID")

    # Issue identification
    issue_type: IssueType = Field(...)
    severity: IssueSeverity = Field(...)
    rule_id: str = Field(..., min_length=1)

    # Location
    file_path: str = Field(..., min_length=1)
    line_number: int | None = None
    column_number: int | None = None
    end_line_number: int | None = None
    end_column_number: int | None = None

    # Details
    message: str = Field(..., min_length=1)
    code_snippet: str | None = None
    suggestion: str | None = None

    # Status
    is_fixed: bool = Field(default=False)
    is_suppressed: bool = Field(default=False)
    suppression_reason: str | None = None

    # Tracking
    first_detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_seen_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    occurrence_count: int = Field(default=1)

    def mark_fixed(self) -> QualityIssue:
        """Mark issue as fixed and return new instance."""
        return self.model_copy(update={"is_fixed": True})

    def suppress(self, reason: str) -> QualityIssue:
        """Suppress issue and return new instance."""
        return self.model_copy(
            update={
                "is_suppressed": True,
                "suppression_reason": reason,
            },
        )

    def unsuppress(self) -> QualityIssue:
        """Unsuppress issue and return new instance."""
        return self.model_copy(
            update={
                "is_suppressed": False,
                "suppression_reason": None,
            },
        )

    def increment_occurrence(self) -> QualityIssue:
        """Increment occurrence count and return new instance."""
        return self.model_copy(
            update={
                "occurrence_count": self.occurrence_count + 1,
                "last_seen_at": datetime.now(UTC),
            },
        )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for quality issue."""
        if not self.analysis_id:
            return FlextResult.fail("Analysis ID is required")
        return FlextResult.ok(None)


class QualityRule(FlextEntity):
    """Quality rule domain entity using enhanced mixins for code reduction."""

    # Rule identification
    rule_id: str = Field(..., min_length=1)
    category: IssueType = Field(...)

    # Rule configuration
    enabled: bool = Field(default=True)
    severity: IssueSeverity = Field(default=IssueSeverity.MEDIUM)

    # Rule details
    pattern: str | None = None
    parameters: dict[str, object] = Field(default_factory=dict)

    # Documentation
    documentation_url: str | None = None
    examples: list[dict[str, str]] = Field(default_factory=list)

    def enable(self) -> QualityRule:
        """Enable rule and return new instance."""
        return self.model_copy(update={"enabled": True})

    def disable(self) -> QualityRule:
        """Disable rule and return new instance."""
        return self.model_copy(update={"enabled": False})

    def update_severity(self, severity: IssueSeverity) -> QualityRule:
        """Update severity and return new instance."""
        return self.model_copy(update={"severity": severity})

    def set_parameter(self, key: str, value: object) -> QualityRule:
        """Set parameter and return new instance."""
        new_parameters = self.parameters.copy()
        new_parameters[key] = value
        return self.model_copy(update={"parameters": new_parameters})

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for quality rule."""
        if not self.rule_id:
            return FlextResult.fail("Rule ID is required")
        return FlextResult.ok(None)


class QualityReport(FlextEntity):
    """Quality report domain entity using enhanced mixins for code reduction."""

    analysis_id: str = Field(..., description="Associated analysis ID")

    # Report type
    report_type: str = Field(..., min_length=1)  # html, json, markdown, pdf
    report_format: str = Field(default="summary")  # summary, detailed, full

    # Report data
    report_path: str | None = None
    report_size_bytes: int = Field(default=0)

    # Generation
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    generation_duration_ms: float | None = None

    # Access
    access_count: int = Field(default=0)
    last_accessed_at: datetime | None = None

    def increment_access(self) -> QualityReport:
        """Increment access count and return new instance."""
        return self.model_copy(
            update={
                "access_count": self.access_count + 1,
                "last_accessed_at": datetime.now(UTC),
            },
        )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for quality report."""
        if not self.analysis_id:
            return FlextResult.fail("Analysis ID is required")
        return FlextResult.ok(None)


# Domain Events
class ProjectCreatedEvent(FlextDomainEvent):
    """Event raised when quality project is created."""

    project_id: str
    project_name: str | None = None


class AnalysisStartedEvent(FlextDomainEvent):
    """Event raised when quality analysis starts."""

    project_id: str
    analysis_id: str | None = None
    branch: str | None = None
    triggered_by: str | None = None


class AnalysisCompletedEvent(FlextDomainEvent):
    """Event raised when quality analysis completes."""

    project_id: str
    analysis_id: str
    overall_score: float
    total_issues: int
    critical_issues: int
    duration_seconds: float


class IssueDetectedEvent(FlextDomainEvent):
    """Event raised when quality issue is detected."""

    analysis_id: str
    issue_id: str
    issue_type: IssueType
    severity: IssueSeverity
    file_path: str
    rule_id: str


class ReportGeneratedEvent(FlextDomainEvent):
    """Event raised when quality report is generated."""

    analysis_id: str
    report_id: str
    report_type: str
    report_path: str
    report_size_bytes: int


# Rebuild models to resolve forward references and type annotations
try:
    QualityProject.model_rebuild()
    QualityAnalysis.model_rebuild()
    QualityIssue.model_rebuild()
    QualityRule.model_rebuild()
    QualityReport.model_rebuild()

    # Also rebuild domain events
    FlextDomainEvent.model_rebuild()
    ProjectCreatedEvent.model_rebuild()
    AnalysisStartedEvent.model_rebuild()
    AnalysisCompletedEvent.model_rebuild()
    IssueDetectedEvent.model_rebuild()
    ReportGeneratedEvent.model_rebuild()
except Exception as e:
    # Log rebuild errors in development - should not affect runtime
    import logging

    logging.getLogger(__name__).debug("Model rebuild error: %s", e)
