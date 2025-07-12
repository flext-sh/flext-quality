"""Domain entities for FLEXT-QUALITY v0.7.0.

REFACTORED:
            Using flext-core modern patterns - NO duplication.
All entities use mixins from flext-core for maximum code reduction.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from flext_core.domain.pydantic_base import DomainEntity, DomainEvent
from flext_core.domain.types import Status, StrEnum
from pydantic import Field

if TYPE_CHECKING:
    from uuid import UUID


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


class QualityProject(DomainEntity):
    """Quality project domain entity using enhanced mixins for code reduction."""

    # Project paths
    project_path: str = Field(..., min_length=1)
    repository_url: str | None = None

    # Configuration
    config_path: str | None = None
    language: str = Field(default="python")

    # Analysis settings
    auto_analyze: bool = Field(default=True)
    analysis_schedule: str | None = None  # cron format

    # Quality thresholds
    min_coverage: float = Field(default=95.0, ge=0.0, le=100.0)
    max_complexity: int = Field(default=10, ge=1)
    max_duplication: float = Field(default=5.0, ge=0.0, le=100.0)

    # Statistics
    last_analysis_at: datetime | None = None
    total_analyses: int = Field(default=0)

    def update_last_analysis(self) -> None:
        self.last_analysis_at = datetime.now()
        self.total_analyses += 1
        self.touch()


class QualityAnalysis(DomainEntity):
    """Quality analysis domain entity using enhanced mixins for code reduction."""

    project_id: UUID = Field(..., description="Associated project ID")

    # Analysis identification
    commit_hash: str | None = None
    branch: str | None = None
    pull_request_id: str | None = None

    # Timing
    started_at: datetime = Field(default_factory=datetime.now)
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

    # Analysis data
    analysis_config: dict[str, Any] = Field(default_factory=dict)

    def start_analysis(self) -> None:
        self.started_at = datetime.now()
        self.status = AnalysisStatus.ANALYZING
        self.touch()

    def complete_analysis(self) -> None:
        self.completed_at = datetime.now()
        self.status = Status.COMPLETED

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()

        self.touch()

    def fail_analysis(self, error: str) -> None:
        self.completed_at = datetime.now()
        self.status = Status.FAILED
        self.add_validation_error(error)

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()

        self.touch()

    def calculate_overall_score(self) -> None:
        scores = [
            self.coverage_score,
            self.complexity_score,
            self.duplication_score,
            self.security_score,
            self.maintainability_score,
        ]
        self.overall_score = sum(scores) / len(scores)

    @property
    def is_completed(self) -> bool:
        return self.status in {Status.COMPLETED, Status.FAILED}

    @property
    def is_successful(self) -> bool:
        return self.status == Status.COMPLETED


class QualityIssue(DomainEntity):
    """Quality issue domain entity using enhanced mixins for code reduction."""

    analysis_id: UUID = Field(..., description="Associated analysis ID")

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
    first_detected_at: datetime = Field(default_factory=datetime.now)
    last_seen_at: datetime = Field(default_factory=datetime.now)
    occurrence_count: int = Field(default=1)

    def mark_fixed(self) -> None:
        self.is_fixed = True
        self.status = Status.RESOLVED
        self.touch()

    def suppress(self, reason: str) -> None:
        self.is_suppressed = True
        self.suppression_reason = reason
        self.touch()

    def unsuppress(self) -> None:
        self.is_suppressed = False
        self.suppression_reason = None
        self.touch()

    def increment_occurrence(self) -> None:
        self.occurrence_count += 1
        self.last_seen_at = datetime.now()
        self.touch()


class QualityRule(DomainEntity):
    """Quality rule domain entity using enhanced mixins for code reduction."""

    # Rule identification
    rule_id: str = Field(..., min_length=1, unique=True)
    category: IssueType = Field(...)

    # Rule configuration
    enabled: bool = Field(default=True)
    severity: IssueSeverity = Field(default=IssueSeverity.MEDIUM)

    # Rule details
    pattern: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)

    # Documentation
    documentation_url: str | None = None
    examples: list[dict[str, str]] = Field(default_factory=list)

    def enable(self) -> None:
        self.enabled = True
        self.status = Status.ACTIVE
        self.touch()

    def disable(self) -> None:
        self.enabled = False
        self.status = Status.INACTIVE
        self.touch()

    def update_severity(self, severity: IssueSeverity) -> None:
        self.severity = severity
        self.touch()

    def set_parameter(self, key: str, value: Any) -> None:
        self.parameters[key] = value
        self.touch()


class QualityReport(DomainEntity):
    """Quality report domain entity using enhanced mixins for code reduction."""

    analysis_id: UUID = Field(..., description="Associated analysis ID")

    # Report type
    report_type: str = Field(..., min_length=1)  # html, json, markdown, pdf
    report_format: str = Field(default="summary")  # summary, detailed, full

    # Report data
    report_path: str | None = None
    report_size_bytes: int = Field(default=0)

    # Generation
    generated_at: datetime = Field(default_factory=datetime.now)
    generation_duration_ms: float | None = None

    # Access
    access_count: int = Field(default=0)
    last_accessed_at: datetime | None = None

    def increment_access(self) -> None:
        self.access_count += 1
        self.last_accessed_at = datetime.now()
        self.touch()


# Domain Events
class ProjectCreatedEvent(DomainEvent):
    """Event raised when quality project is created."""

    project_id: UUID
    project_name: str | None = None


class AnalysisStartedEvent(DomainEvent):
    """Event raised when quality analysis starts."""

    project_id: UUID
    analysis_id: UUID | None = None
    branch: str | None = None
    triggered_by: str | None = None


class AnalysisCompletedEvent(DomainEvent):
    """Event raised when quality analysis completes."""

    project_id: UUID
    analysis_id: UUID
    overall_score: float
    total_issues: int
    critical_issues: int
    duration_seconds: float


class IssueDetectedEvent(DomainEvent):
    """Event raised when quality issue is detected."""

    analysis_id: UUID
    issue_id: UUID
    issue_type: IssueType
    severity: IssueSeverity
    file_path: str
    rule_id: str


class ReportGeneratedEvent(DomainEvent):
    """Event raised when quality report is generated."""

    analysis_id: UUID
    report_id: UUID
    report_type: str
    report_path: str
    report_size_bytes: int
