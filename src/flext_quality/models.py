"""FLEXT Quality Models - Direct FLEXT DDD patterns implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any, Literal, TypeVar
from uuid import UUID

from flext_core import FlextModels
from pydantic import Field, computed_field, field_validator

T = TypeVar("T")
ScoreT = TypeVar("ScoreT", bound=float)

# Advanced validation using Python 3.13+ syntax
type ScoreRange = Annotated[float, Field(ge=0.0, le=100.0)]
type PositiveInt = Annotated[int, Field(ge=1)]
type Timestamp = Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]


class FlextQualityModels(FlextModels):
    """Unified FLEXT Quality Models - Single class following SOLID principles.

    Single responsibility: Generic quality analysis models with proper DDD patterns.
    All models consolidated into focused, reusable components.
    """

    # Quality score thresholds - generic configuration
    GRADE_A_THRESHOLD = 90.0
    GRADE_B_THRESHOLD = 80.0
    GRADE_C_THRESHOLD = 70.0
    GRADE_D_THRESHOLD = 60.0

    class QualityMixin:
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

    class ScoreMixin:
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

    class TimestampMixin:
        """Mixin for models with timestamp tracking."""

        created_at: Timestamp
        updated_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

        @field_validator("updated_at", mode="before")
        @classmethod
        def validate_updated_at(cls, v: datetime | None) -> datetime:
            """Ensure updated_at is never None."""
            return v or datetime.now(UTC)

    class ProjectModel(FlextModels.Entity, TimestampMixin, QualityMixin):
        """Project entity with advanced validation."""

        id: str = Field(..., description="Unique project identifier")
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

        id: str = Field(..., description="Unique analysis identifier")
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

        id: str = Field(..., description="Unique issue identifier")
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

        id: str = Field(..., description="Unique report identifier")
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

    class DomainEvent(FlextModels.DomainEvent):
        """Base domain event for quality analysis."""

        event_type: str
        timestamp: Timestamp
        data: dict[str, Any] = Field(default_factory=dict)

    # Export all nested model classes for direct access
    ProjectModel = ProjectModel
    AnalysisModel = AnalysisModel
    IssueModel = IssueModel
    ReportModel = ReportModel
    ConfigModel = ConfigModel
    AnalysisResults = AnalysisResults
    Dependency = Dependency
    TestResults = TestResults
    OverallMetrics = OverallMetrics
    FunctionInfo = FunctionInfo
    ClassInfo = ClassInfo
    DomainEvent = DomainEvent

    # Direct aliases for compatibility (no wrappers)
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


# Rebuild models after all classes are defined to resolve forward references
FlextQualityModels.ProjectModel.model_rebuild()
FlextQualityModels.AnalysisModel.model_rebuild()
FlextQualityModels.IssueModel.model_rebuild()
FlextQualityModels.ReportModel.model_rebuild()
FlextQualityModels.ConfigModel.model_rebuild()
FlextQualityModels.AnalysisResults.model_rebuild()
FlextQualityModels.TestResults.model_rebuild()
FlextQualityModels.OverallMetrics.model_rebuild()
FlextQualityModels.FunctionInfo.model_rebuild()
FlextQualityModels.ClassInfo.model_rebuild()
FlextQualityModels.DomainEvent.model_rebuild()

# Export models for clean imports
__all__ = [
    "FlextQualityModels",
]
