"""FLEXT Quality Models - Direct FLEXT DDD patterns implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import UUID

from flext_core import FlextModels
from pydantic import BaseModel, Field, computed_field, field_validator

from flext_quality.typings import PositiveInt, ScoreRange, Timestamp


class FlextQualityModels(FlextModels):
    """Unified FLEXT Quality Models - Single class following SOLID principles.

    Single responsibility: Generic quality analysis models with proper DDD patterns.
    All models consolidated into focused, reusable components.

    Architecture: Layer 2 (Domain)
    Provides comprehensive domain models for quality analysis following FLEXT patterns:
    - Value Objects: Immutable domain values (FlextModels.Value)
    - Entities: Domain entities with identity (FlextModels.Entity)
    - Aggregate Roots: Consistency boundaries (FlextModels.AggregateRoot)
    - Commands: CQRS commands (FlextModels.Command)
    - Queries: CQRS queries (FlextModels.Query)
    - Domain Events: Event sourcing (FlextModels.DomainEvent)
    """

    # =========================================================================
    # ENUMERATIONS - Domain enums for quality analysis
    # =========================================================================

    class AnalysisStatus(StrEnum):
        """Analysis status enumeration."""

        QUEUED = "queued"
        ANALYZING = "analyzing"
        COMPLETED = "completed"
        FAILED = "failed"

    class IssueSeverity(StrEnum):
        """Issue severity levels."""

        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"
        INFO = "INFO"

    class IssueType(StrEnum):
        """Issue type enumeration."""

        # Code quality issues
        SYNTAX_ERROR = "syntax_error"
        STYLE_VIOLATION = "style_violation"
        NAMING_CONVENTION = "naming_convention"
        # Complexity issues
        HIGH_COMPLEXITY = "high_complexity"
        HIGH_COGNITIVE_COMPLEXITY = "high_cognitive_complexity"
        LONG_METHOD = "long_method"
        LONG_PARAMETER_LIST = "long_parameter_list"
        # Security issues
        SECURITY_VULNERABILITY = "security_vulnerability"
        HARDCODED_CREDENTIAL = "hardcoded_credential"
        SQL_INJECTION = "sql_injection"
        XSS_VULNERABILITY = "xss_vulnerability"
        # Dead code issues
        UNUSED_IMPORT = "unused_import"
        UNUSED_VARIABLE = "unused_variable"
        UNUSED_FUNCTION = "unused_function"
        UNREACHABLE_CODE = "unreachable_code"
        # Duplication issues
        DUPLICATE_CODE = "duplicate_code"
        SIMILAR_CODE = "similar_code"
        # Type issues
        TYPE_ERROR = "type_error"
        MISSING_TYPE_ANNOTATION = "missing_type_annotation"
        # Documentation issues
        MISSING_DOCSTRING = "missing_docstring"
        INVALID_DOCSTRING = "invalid_docstring"

    class QualityGrade(StrEnum):
        """Quality grade enumeration."""

        A_PLUS = "A+"
        A = "A"
        A_MINUS = "A-"
        B_PLUS = "B+"
        B = "B"
        B_MINUS = "B-"
        C_PLUS = "C+"
        C = "C"
        C_MINUS = "C-"
        D_PLUS = "D+"
        D = "D"
        D_MINUS = "D-"
        F = "F"

    # Quality score thresholds - generic configuration
    GRADE_A_THRESHOLD = 90.0
    GRADE_B_THRESHOLD = 80.0
    GRADE_C_THRESHOLD = 70.0
    GRADE_D_THRESHOLD = 60.0

    # =========================================================================
    # MIXINS - Reusable model behaviors (must extend BaseModel for Pydantic)
    # =========================================================================

    class QualityMixin(BaseModel):
        """Mixin providing common quality model functionality."""

        @computed_field
        @property
        def quality_metadata(self) -> dict[str, Any]:
            """Generic quality metadata for all models."""
            return {
                "model_type": self.__class__.__name__,
                "created_at": getattr(
                    self, "created_at", datetime.now(UTC)
                ).isoformat(),
                "validation_status": "passed",
            }

    class ScoreMixin(BaseModel):
        """Mixin for models with quality scores."""

        overall_score: ScoreRange = Field(0.0, description="Overall quality score")
        coverage_score: ScoreRange = Field(0.0, description="Test coverage score")
        security_score: ScoreRange = Field(0.0, description="Security analysis score")
        maintainability_score: ScoreRange = Field(
            0.0, description="Maintainability score"
        )
        complexity_score: ScoreRange = Field(0.0, description="Complexity score")

        @computed_field
        @property
        def average_score(self) -> float:
            """Computed average of all quality scores."""
            scores = [
                self.overall_score,
                self.coverage_score,
                self.security_score,
                self.maintainability_score,
                self.complexity_score,
            ]
            return sum(scores) / len(scores)

        @computed_field
        @property
        def quality_grade(self) -> Literal["A", "B", "C", "D", "F"]:
            """Computed quality grade based on average score."""
            score = self.average_score
            if score >= FlextQualityModels.GRADE_A_THRESHOLD:
                return "A"
            if score >= FlextQualityModels.GRADE_B_THRESHOLD:
                return "B"
            if score >= FlextQualityModels.GRADE_C_THRESHOLD:
                return "C"
            if score >= FlextQualityModels.GRADE_D_THRESHOLD:
                return "D"
            return "F"

    class TimestampMixin(BaseModel):
        """Mixin for models with timestamp tracking."""

        created_at: Timestamp = Field(default_factory=lambda: datetime.now(UTC))
        updated_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

        @field_validator("updated_at", mode="before")
        @classmethod
        def validate_updated_at(cls, v: datetime | None) -> datetime:
            """Ensure updated_at is never None."""
            return v or datetime.now(UTC)

    class ProjectModel(FlextModels.Entity, TimestampMixin, QualityMixin):
        """Project entity with advanced validation."""

        name: str = Field(min_length=1, max_length=255)
        path: str = Field(..., description="Project path for analysis")
        description: str | None = None

        @computed_field
        @property
        def project_info(self) -> dict[str, Any]:
            """Consolidated project information."""
            return {
                "id": self.id,
                "name": self.name,
                "path": self.path,
                "description": self.description,
                **self.quality_metadata,
            }

    class AnalysisModel(FlextModels.Entity, ScoreMixin, TimestampMixin, QualityMixin):
        """Analysis entity with score tracking."""

        project_id: UUID = Field(..., description="Associated project")
        status: str = Field(..., description="Analysis status")
        started_at: Timestamp
        completed_at: datetime | None = None
        error_message: str | None = None

        @computed_field
        @property
        def analysis_summary(self) -> dict[str, Any]:
            """Analysis execution summary."""
            return {
                "id": self.id,
                "status": self.status,
                "duration": (
                    (self.completed_at - self.started_at).total_seconds()
                    if self.completed_at
                    else None
                ),
                "scores": {
                    "overall": self.overall_score,
                    "coverage": self.coverage_score,
                    "security": self.security_score,
                    "maintainability": self.maintainability_score,
                    "complexity": self.complexity_score,
                    "average": self.average_score,
                    "grade": self.quality_grade,
                },
                **self.quality_metadata,
            }

    class IssueModel(FlextModels.Entity, TimestampMixin, QualityMixin):
        """Quality issue entity."""

        analysis_id: UUID = Field(..., description="Associated analysis")
        file_path: str = Field(..., description="File containing the issue")
        line_number: PositiveInt | None = None
        column_number: PositiveInt | None = None
        issue_type: str = Field(..., description="Type of quality issue")
        severity: Literal["low", "medium", "high", "critical"] = "medium"
        message: str = Field(..., description="Issue description")
        rule_id: str | None = None

        @computed_field
        @property
        def issue_location(self) -> dict[str, Any]:
            """Issue location information."""
            return {
                "file": self.file_path,
                "line": self.line_number,
                "column": self.column_number,
                "severity": self.severity,
                "type": self.issue_type,
            }

    class ReportModel(FlextModels.Entity, ScoreMixin, TimestampMixin, QualityMixin):
        """Quality report entity."""

        analysis_id: UUID = Field(..., description="Associated analysis")
        format_type: Literal["HTML", "JSON", "PDF", "CSV", "XML", "MARKDOWN"] = "HTML"
        file_path: str | None = None
        generated_at: Timestamp

        @computed_field
        @property
        def report_capabilities(self) -> list[str]:
            """Report format capabilities."""
            capabilities_map = {
                "HTML": ["interactive", "visual", "web-friendly"],
                "JSON": ["machine-readable", "api-friendly", "structured"],
                "CSV": ["spreadsheet-compatible", "data-analysis"],
                "XML": ["structured", "schema-validation", "interoperable"],
                "MARKDOWN": ["human-readable", "version-control-friendly"],
            }
            return capabilities_map.get(self.format_type, [])

    class ConfigModel(FlextModels.Value, QualityMixin):
        """Configuration value object."""

        include_patterns: list[str] = Field(default_factory=list)
        exclude_patterns: list[str] = Field(default_factory=list)
        enable_security: bool = True
        enable_complexity: bool = True
        enable_coverage: bool = True
        max_complexity: int = Field(default=10)
        min_coverage: ScoreRange = Field(default=80.0)
        security_threshold: ScoreRange = Field(default=90.0)

        @computed_field
        @property
        def config_summary(self) -> dict[str, Any]:
            """Configuration summary."""
            return {
                "patterns": {
                    "include": len(self.include_patterns),
                    "exclude": len(self.exclude_patterns),
                },
                "enabled_features": [
                    k.replace("enable_", "")
                    for k, v in self.__dict__.items()
                    if k.startswith("enable_") and v
                ],
                "thresholds": {
                    "complexity": self.max_complexity,
                    "coverage": self.min_coverage,
                    "security": self.security_threshold,
                },
            }

    class AnalysisResults(FlextModels.Value, ScoreMixin, QualityMixin):
        """Analysis results value object."""

        issues: list[dict[str, Any]] = Field(default_factory=list)
        metrics: dict[str, Any] = Field(default_factory=dict)
        recommendations: list[str] = Field(default_factory=list)

        @computed_field
        @property
        def results_summary(self) -> dict[str, Any]:
            """Results summary."""
            return {
                "issues_count": len(self.issues),
                "metrics_count": len(self.metrics),
                "recommendations_count": len(self.recommendations),
                "scores": {
                    "overall": self.overall_score,
                    "grade": self.quality_grade,
                },
                **self.quality_metadata,
            }

    class Dependency(FlextModels.Value):
        """Dependency information."""

        name: str
        version: str | None = None
        type: str = "runtime"

    class TestResults(FlextModels.Value, ScoreMixin):
        """Test execution results."""

        total_tests: int = 0
        passed_tests: int = 0
        failed_tests: int = 0
        skipped_tests: int = 0

        @computed_field
        @property
        def pass_rate(self) -> float:
            """Test pass rate percentage."""
            return (
                (self.passed_tests / self.total_tests * 100)
                if self.total_tests > 0
                else 0.0
            )

    class OverallMetrics(FlextModels.Value, ScoreMixin):
        """Consolidated metrics."""

        files_analyzed: int = 0
        total_lines: int = 0
        functions_count: int = 0
        classes_count: int = 0

    class AnalysisResult(FlextModels.Value, ScoreMixin, QualityMixin):
        """Analysis result value object."""

        analysis_id: str = Field(..., description="Analysis identifier")
        project_path: str = Field(..., description="Project path analyzed")
        status: str = Field(..., description="Analysis status")
        issues_found: list[dict[str, Any]] = Field(default_factory=list)
        metrics: dict[str, Any] = Field(default_factory=dict)

        @computed_field
        @property
        def analysis_summary(self) -> dict[str, Any]:
            """Analysis summary."""
            return {
                "analysis_id": self.analysis_id,
                "project_path": self.project_path,
                "status": self.status,
                "issues_count": len(self.issues_found),
                "metrics_count": len(self.metrics),
                "scores": {
                    "overall": self.overall_score,
                    "grade": self.quality_grade,
                },
                **self.quality_metadata,
            }

    class RewriteResult(FlextModels.Value):
        """Git rewrite operation result."""

        original_commit: str = Field(..., description="Original commit hash")
        new_commit: str = Field(..., description="New commit hash")
        files_changed: list[str] = Field(default_factory=list)
        operation_type: str = Field(..., description="Type of rewrite operation")

    class OptimizationTarget(FlextModels.Value):
        """Optimization target specification."""

        file_path: str = Field(..., description="Target file path")
        optimization_type: str = Field(..., description="Type of optimization")
        priority: Literal["low", "medium", "high", "critical"] = "medium"

    class OptimizationResult(FlextModels.Value, ScoreMixin):
        """Optimization operation result."""

        optimization_id: str = Field(..., description="Optimization identifier")
        target_files: list[str] = Field(default_factory=list)
        optimizations_applied: list[str] = Field(default_factory=list)
        performance_improvement: float = Field(default=0.0)
        target: str | None = Field(default=None, description="Optimization target")
        changes_made: int = Field(default=0, description="Number of changes made")
        success: bool = Field(
            default=True, description="Whether the operation was successful"
        )
        errors: list[str] = Field(
            default_factory=list, description="List of errors encountered"
        )
        warnings: list[str] = Field(
            default_factory=list, description="List of warnings encountered"
        )

        @computed_field
        @property
        def optimization_summary(self) -> dict[str, Any]:
            """Optimization summary."""
            return {
                "optimization_id": self.optimization_id,
                "target_files_count": len(self.target_files),
                "optimizations_count": len(self.optimizations_applied),
                "performance_improvement": self.performance_improvement,
                "scores": {
                    "overall": self.overall_score,
                    "grade": self.quality_grade,
                },
            }

    class FunctionInfo(FlextModels.Value):
        """Function information from AST."""

        name: str
        line_number: PositiveInt
        complexity: int = 1
        parameters_count: int = 0

    class ClassInfo(FlextModels.Value):
        """Class information from AST."""

        name: str
        line_number: PositiveInt
        methods_count: int = 0
        attributes_count: int = 0

    # =========================================================================
    # COMMANDS - CQRS commands (EXTEND FlextModels.Command)
    # =========================================================================

    class AnalyzeProjectCommand(FlextModels.Command):
        """Command to analyze a project."""

        project_path: str = Field(..., description="Path to project to analyze")
        include_security: bool = Field(True, description="Include security analysis")
        include_complexity: bool = Field(
            True, description="Include complexity analysis"
        )
        include_dead_code: bool = Field(True, description="Include dead code detection")
        include_duplicates: bool = Field(
            True, description="Include duplication detection"
        )

    class GenerateReportCommand(FlextModels.Command):
        """Command to generate quality report."""

        analysis_id: UUID = Field(..., description="Analysis ID")
        format_type: Literal["HTML", "JSON", "PDF", "CSV", "MARKDOWN"] = Field(
            "HTML", description="Report format"
        )

    # =========================================================================
    # QUERIES - CQRS queries (EXTEND FlextModels.Query)
    # =========================================================================

    class GetProjectQuery(FlextModels.Query):
        """Query to get project details."""

        project_id: str = Field(..., description="Project ID")

    class GetAnalysisResultsQuery(FlextModels.Query):
        """Query to get analysis results."""

        analysis_id: UUID = Field(..., description="Analysis ID")

    class GetQualityMetricsQuery(FlextModels.Query):
        """Query to get quality metrics."""

        project_id: str = Field(..., description="Project ID")

    # =========================================================================
    # DOMAIN EVENTS - Event sourcing (EXTEND FlextModels.DomainEvent)
    # =========================================================================

    class AnalysisStartedEvent(FlextModels.DomainEvent):
        """Event when analysis starts."""

        analysis_id: UUID = Field(..., description="Analysis ID")
        project_path: str = Field(..., description="Project path")
        timestamp: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    class AnalysisCompletedEvent(FlextModels.DomainEvent):
        """Event when analysis completes."""

        analysis_id: UUID = Field(..., description="Analysis ID")
        overall_score: float = Field(..., ge=0.0, le=100.0)
        timestamp: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    class IssueDetectedEvent(FlextModels.DomainEvent):
        """Event when quality issue detected."""

        issue_id: str = Field(..., description="Issue ID")
        severity: str = Field(..., description="Issue severity")
        file_path: str = Field(..., description="File path")
        timestamp: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    class ReportGeneratedEvent(FlextModels.DomainEvent):
        """Event when report is generated."""

        report_id: str = Field(..., description="Report ID")
        analysis_id: UUID = Field(..., description="Analysis ID")
        format_type: str = Field(..., description="Report format")
        timestamp: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    # =========================================================================
    # EXPORT & ALIASES - Direct access patterns
    # =========================================================================

    # Direct aliases for backward compatibility (no wrappers)
    Project = ProjectModel
    Analysis = AnalysisModel
    Issue = IssueModel
    Report = ReportModel
    FileAnalysisResult = AnalysisResults
    CodeIssue = IssueModel
    ComplexityIssue = IssueModel
    SecurityIssue = IssueModel
    DeadCodeIssue = IssueModel
    DuplicationIssue = IssueModel


# =========================================================================
# MODEL RECONSTRUCTION - Resolve forward references after all classes defined
# =========================================================================

FlextQualityModels.ProjectModel.model_rebuild()
FlextQualityModels.AnalysisModel.model_rebuild()
FlextQualityModels.IssueModel.model_rebuild()
FlextQualityModels.ReportModel.model_rebuild()
FlextQualityModels.ConfigModel.model_rebuild()
FlextQualityModels.AnalysisResults.model_rebuild()
FlextQualityModels.TestResults.model_rebuild()
FlextQualityModels.OverallMetrics.model_rebuild()
FlextQualityModels.AnalysisResult.model_rebuild()
FlextQualityModels.RewriteResult.model_rebuild()
FlextQualityModels.OptimizationResult.model_rebuild()
FlextQualityModels.OptimizationTarget.model_rebuild()
FlextQualityModels.FunctionInfo.model_rebuild()
FlextQualityModels.ClassInfo.model_rebuild()

# CQRS Commands
FlextQualityModels.AnalyzeProjectCommand.model_rebuild()
FlextQualityModels.GenerateReportCommand.model_rebuild()

# CQRS Queries
FlextQualityModels.GetProjectQuery.model_rebuild()
FlextQualityModels.GetAnalysisResultsQuery.model_rebuild()
FlextQualityModels.GetQualityMetricsQuery.model_rebuild()

# Domain Events
FlextQualityModels.AnalysisStartedEvent.model_rebuild()
FlextQualityModels.AnalysisCompletedEvent.model_rebuild()
FlextQualityModels.IssueDetectedEvent.model_rebuild()
FlextQualityModels.ReportGeneratedEvent.model_rebuild()

# =========================================================================
# PUBLIC API - Export models for clean imports
# =========================================================================

__all__ = [
    "FlextQualityModels",
]
