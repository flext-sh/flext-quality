"""FLEXT Quality Entities - Domain entities for quality analysis operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import override

from pydantic import BaseModel, Field

from flext_core import FlextContainer, FlextLogger, FlextResult
from flext_quality.typings import FlextQualityTypes
from flext_quality.value_objects import FlextIssueSeverity, FlextIssueType


class FlextQualityEntities:
    """Unified quality entities class following FLEXT pattern - ZERO DUPLICATION.

    Single responsibility: Quality domain entities management
    Contains all domain entities as nested classes with shared functionality.
    """

    @override
    def __init__(self) -> None:
        """Initialize quality entities with dependency injection."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    # =============================================================================
    # NESTED ENUM CLASSES - All status enumerations
    # =============================================================================

    class AnalysisStatus(StrEnum):
        """Analysis status for quality analysis."""

        QUEUED = "queued"
        ANALYZING = "analyzing"
        COMPLETED = "completed"
        FAILED = "failed"

    # =============================================================================
    # NESTED BASE CLASSES - Foundation classes
    # =============================================================================

    class DomainEvent(BaseModel):
        """Base class for domain events."""

        event_type: str
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # =============================================================================
    # NESTED ENTITY CLASSES - Core domain entities
    # =============================================================================

    class QualityProject(BaseModel):
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
        analysis_schedule: str | None = None  # cron format

        # Quality thresholds
        min_coverage: float = Field(default=95.0, ge=0.0, le=100.0)
        max_complexity: int = Field(default=10, ge=1)
        max_duplication: float = Field(default=5.0, ge=0.0, le=100.0)

        # Statistics
        last_analysis_at: datetime | None = None
        total_analyses: int = Field(default=0)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for quality project."""
            if not self.project_path:
                return FlextResult[None].fail("Project path is required")
            return FlextResult[None].ok(None)

        def update_last_analysis(self) -> FlextQualityEntities.QualityProject:
            """Update last analysis timestamp and return new instance."""
            return self.model_copy(
                update={
                    "last_analysis_at": datetime.now(UTC),
                    "total_analyses": self.total_analyses + 1,
                },
            )

    class QualityAnalysis(BaseModel):
        """Quality analysis domain entity using enhanced mixins for code reduction."""

        id: str = Field(
            default_factory=lambda: str(__import__("uuid").uuid4()),
            description="Unique analysis ID",
        )
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
        total_files: int = 0
        total_lines: int = 0
        code_lines: int = 0
        comment_lines: int = 0
        blank_lines: int = 0

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
        status: str = Field(default="queued")

        # Analysis data
        analysis_config: FlextQualityTypes.Core.AnalysisDict = Field(
            default_factory=dict
        )

        def start_analysis(self) -> FlextQualityEntities.QualityAnalysis:
            """Start analysis and return new instance."""
            return self.model_copy(
                update={
                    "started_at": datetime.now(UTC),
                    "status": FlextQualityEntities.AnalysisStatus.ANALYZING,
                },
            )

        def complete_analysis(self) -> FlextQualityEntities.QualityAnalysis:
            """Complete analysis and return new instance."""
            completed_at = datetime.now(UTC)
            if self.started_at:
                duration = completed_at - self.started_at
                duration.total_seconds()

            return self.model_copy(
                update={
                    "completed_at": "completed_at",
                    "status": FlextQualityEntities.AnalysisStatus.COMPLETED,
                    "duration_seconds": "duration_seconds",
                },
            )

        def fail_analysis(self, _error: str) -> FlextQualityEntities.QualityAnalysis:
            """Fail analysis and return new instance."""
            completed_at = datetime.now(UTC)
            if self.started_at:
                duration = completed_at - self.started_at
                duration.total_seconds()

            return self.model_copy(
                update={
                    "completed_at": "completed_at",
                    "status": FlextQualityEntities.AnalysisStatus.FAILED,
                    "duration_seconds": "duration_seconds",
                    "overall_score": 0.0,  # Failed analysis gets 0 score
                    "analysis_config": {**self.analysis_config, "error": "error"},
                },
            )

        def calculate_overall_score(
            self,
        ) -> FlextQualityEntities.QualityAnalysis:
            """Calculate overall score and return new instance."""
            scores = [
                self.coverage_score,
                self.complexity_score,
                self.duplication_score,
                self.security_score,
                self.maintainability_score,
            ]
            sum(scores) / len(scores)
            return self.model_copy(update={"overall_score": "overall_score"})

        @property
        def is_completed(self) -> bool:
            """Check if analysis is completed (either succeeded or failed)."""
            return self.status in {
                FlextQualityEntities.AnalysisStatus.COMPLETED,
                FlextQualityEntities.AnalysisStatus.FAILED,
            }

        @property
        def successful(self) -> bool:
            """Check if analysis completed successfully."""
            return self.status == FlextQualityEntities.AnalysisStatus.COMPLETED

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for quality analysis."""
            if not self.project_id:
                return FlextResult[None].fail("Project ID is required")
            return FlextResult[None].ok(None)

    class QualityIssue(BaseModel):
        """Quality issue domain entity using enhanced mixins for code reduction."""

        analysis_id: str = Field(..., description="Associated analysis ID")

        # Issue identification
        issue_type: FlextIssueType = Field(...)
        severity: FlextIssueSeverity = Field(...)
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

        def mark_fixed(self) -> FlextQualityEntities.QualityIssue:
            """Mark issue as fixed and return new instance."""
            return self.model_copy(update={"is_fixed": "True"})

        def suppress(self, _reason: str) -> FlextQualityEntities.QualityIssue:
            """Suppress issue and return new instance."""
            return self.model_copy(
                update={
                    "is_suppressed": "True",
                    "suppression_reason": "reason",
                },
            )

        def unsuppress(self) -> FlextQualityEntities.QualityIssue:
            """Unsuppress issue and return new instance."""
            return self.model_copy(
                update={
                    "is_suppressed": "False",
                    "suppression_reason": "None",
                },
            )

        def increment_occurrence(self) -> FlextQualityEntities.QualityIssue:
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
                return FlextResult[None].fail("Analysis ID is required")
            return FlextResult[None].ok(None)

    class QualityRule(BaseModel):
        """Quality rule domain entity using enhanced mixins for code reduction."""

        # Rule identification
        rule_id: str = Field(..., min_length=1)
        category: FlextIssueType = Field(...)

        # Rule configuration
        enabled: bool = Field(default=True)
        severity: FlextIssueSeverity = Field(default=FlextIssueSeverity.MEDIUM)

        # Rule details
        pattern: str | None = None
        parameters: FlextQualityTypes.Core.DataDict = Field(default_factory=dict)

        # Documentation
        documentation_url: str | None = None
        examples: list[FlextQualityTypes.Core.DataDict] = Field(default_factory=list)

        def enable(self) -> FlextQualityEntities.QualityRule:
            """Enable rule and return new instance."""
            return self.model_copy(update={"enabled": "True"})

        def disable(self) -> FlextQualityEntities.QualityRule:
            """Disable rule and return new instance."""
            return self.model_copy(update={"enabled": "False"})

        def update_severity(
            self,
            _severity: FlextIssueSeverity,
        ) -> FlextQualityEntities.QualityRule:
            """Update severity and return new instance."""
            return self.model_copy(update={"severity": "severity"})

        def set_parameter(
            self,
            key: str,
            value: object,
        ) -> FlextQualityEntities.QualityRule:
            """Set parameter and return new instance."""
            new_parameters = self.parameters.copy()
            new_parameters[key] = value
            return self.model_copy(update={"parameters": "new_parameters"})

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for quality rule."""
            if not self.rule_id:
                return FlextResult[None].fail("Rule ID is required")
            return FlextResult[None].ok(None)

    class QualityReport(BaseModel):
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

        def increment_access(self) -> FlextQualityEntities.QualityReport:
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
                return FlextResult[None].fail("Analysis ID is required")
            return FlextResult[None].ok(None)

    # =============================================================================
    # NESTED EVENT CLASSES - Domain events
    # =============================================================================

    class ProjectCreatedEvent(DomainEvent):
        """Event raised when quality project is created."""

        project_id: str
        project_name: str | None = None

    class AnalysisStartedEvent(DomainEvent):
        """Event raised when quality analysis starts."""

        project_id: str
        analysis_id: str | None = None
        branch: str | None = None
        triggered_by: str | None = None

    class AnalysisCompletedEvent(DomainEvent):
        """Event raised when quality analysis completes."""

        project_id: str
        analysis_id: str
        overall_score: float
        total_issues: int
        critical_issues: int
        duration_seconds: float

    class IssueDetectedEvent(DomainEvent):
        """Event raised when quality issue is detected."""

        analysis_id: str
        issue_id: str
        issue_type: FlextIssueType
        severity: FlextIssueSeverity
        file_path: str
        rule_id: str

    class ReportGeneratedEvent(DomainEvent):
        """Event raised when quality report is generated."""

        analysis_id: str
        report_id: str
        report_type: str
        report_path: str
        report_size_bytes: int

    # =============================================================================
    # ENTITY FACTORY METHODS - Removed for 1.0 production readiness
    # =============================================================================
    # Factory methods removed to eliminate object type usage and ensure type safety
    # Users should instantiate entities directly: QualityProject(name="...", project_path="...")


# Rebuild models to resolve forward references and type annotations
try:
    _entities = FlextQualityEntities()

    # Rebuild nested models
    FlextQualityEntities.QualityProject.model_rebuild()
    FlextQualityEntities.QualityAnalysis.model_rebuild()
    FlextQualityEntities.QualityIssue.model_rebuild()
    FlextQualityEntities.QualityRule.model_rebuild()
    FlextQualityEntities.QualityReport.model_rebuild()

    # Also rebuild domain events
    FlextQualityEntities.DomainEvent.model_rebuild()
    FlextQualityEntities.ProjectCreatedEvent.model_rebuild()
    FlextQualityEntities.AnalysisStartedEvent.model_rebuild()
    FlextQualityEntities.AnalysisCompletedEvent.model_rebuild()
    FlextQualityEntities.IssueDetectedEvent.model_rebuild()
    FlextQualityEntities.ReportGeneratedEvent.model_rebuild()
except Exception as e:
    # Log rebuild errors in development - should not affect runtime
    from flext_core import FlextLogger, FlextResult

    FlextLogger(__name__).debug("Model rebuild error: %s", e)
