"""FLEXT Quality Models - Simple, pragmatic domain models.

Using Pydantic v2 BaseModel directly without over-engineering.
Follows SOLID principles and FLEXT DDD patterns minimally.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal, Self, TypedDict
from uuid import UUID, uuid4

from flext_core.utilities import u as flext_u
from pydantic import BaseModel, Field

from flext_quality.constants import c
from flext_quality.protocols import p
from flext_quality.typings import PositiveInt, ScoreRange, Timestamp

# Type alias for rule parameter values - no Any type
ParameterValue = str | int | float | bool


class FlextQualityModels:
    """FLEXT Quality Models - Unified namespace for models."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextQualityModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        flext_u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextQualityModels is deprecated. Use FlextModels directly with composition instead.",
        )

    class IssueDict(TypedDict, total=False):
        """Typed representation of a quality issue."""

        type: str
        message: str
        severity: str
        file_path: str
        line_number: int
        column_number: int

    class MetricsDict(TypedDict, total=False):
        """Typed representation of analysis metrics."""

        total_issues: int
        security_issues: int
        complexity_issues: int
        dead_code_issues: int
        duplication_issues: int
        critical_issues: int
        high_issues: int
        medium_issues: int
        low_issues: int
        info_issues: int
        files_analyzed: int

    class CheckDetailsDict(TypedDict, total=False):
        """Typed representation of check details."""

        violations: int
        warnings: int
        info: int
        last_checked: str

    # =====================================================================
    # STATUS & SEVERITY ENUMERATIONS - Aliases from constants.py
    # =====================================================================

    AnalysisStatus = c.Quality.AnalysisStatus
    IssueSeverity = c.Quality.IssueSeverity
    IssueType = c.Quality.IssueType
    QualityGrade = c.Quality.QualityGrade

    # =====================================================================
    # PROTOCOLS - Moved to protocols.py
    # =====================================================================
    # All protocol definitions are centralized in protocols.py
    # Use p.Quality.IssueProtocol for the issue protocol

    # Protocol reference from centralized protocols.py for backward compatibility
    IssueProtocol = p.Quality.IssueProtocol

    # =====================================================================
    # DOMAIN MODELS - Simple, pragmatic Pydantic models
    # =====================================================================

    class ProjectModel(BaseModel):
        """Project entity - root aggregate."""

        id: str = Field(description="Project ID")
        name: str = Field(min_length=1, max_length=255, description="Project name")
        path: str = Field(description="Project file path")
        description: str | None = None
        created_at: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    class AnalysisModel(BaseModel):
        """Quality analysis result entity."""

        id: UUID = Field(default_factory=uuid4)
        project_id: UUID = Field(description="Associated project")
        status: str = Field(default="queued", description="Analysis status")
        started_at: Timestamp = Field(default_factory=lambda: datetime.now(UTC))
        completed_at: datetime | None = None
        overall_score: ScoreRange = 0.0
        coverage_score: ScoreRange = 0.0
        security_score: ScoreRange = 0.0
        complexity_score: ScoreRange = 0.0
        error_message: str | None = None

    class IssueModel(BaseModel):
        """Quality issue entity."""

        id: UUID = Field(default_factory=uuid4)
        analysis_id: UUID = Field(description="Associated analysis")
        file_path: str = Field(description="File path")
        line_number: PositiveInt | None = None
        column_number: PositiveInt | None = None
        issue_type: FlextQualityModels.IssueType = Field(description="Type of issue")
        severity: str = Field(default="MEDIUM", description="Issue severity level")
        message: str = Field(description="Issue description")
        rule_id: str | None = None

    # Alias for backward compatibility (analyzer.py uses CodeIssue)
    CodeIssue = IssueModel

    class RuleModel(BaseModel):
        """Quality rule entity - represents a configurable quality check."""

        id: str = Field(description="Unique rule identifier")
        rule_id: str = Field(description="Rule code (e.g., E302, W605)")
        category: FlextQualityModels.IssueType = Field(
            description="Type of issue the rule checks",
        )
        severity: str = Field(default="MEDIUM", description="Issue severity level")
        enabled: bool = Field(default=True, description="Whether rule is active")
        parameters: dict[str, ParameterValue] = Field(
            default_factory=dict,
            description="Rule parameters",
        )
        description: str | None = Field(default=None, description="Rule description")

        def enable(self) -> Self:
            """Enable this rule."""
            return self.model_copy(update={"enabled": True})

        def disable(self) -> Self:
            """Disable this rule."""
            return self.model_copy(update={"enabled": False})

        def update_severity(self, severity: FlextQualityModels.IssueSeverity) -> Self:
            """Update rule severity."""
            return self.model_copy(update={"severity": severity})

        def set_parameter(self, key: str, value: ParameterValue) -> Self:
            """Set a rule parameter."""
            new_params = self.parameters.copy()
            new_params[key] = value
            return self.model_copy(update={"parameters": new_params})

    class ReportModel(BaseModel):
        """Quality report entity."""

        id: UUID = Field(default_factory=uuid4)
        analysis_id: UUID = Field(description="Associated analysis")
        format_type: Literal["HTML", "JSON", "CSV"] = "JSON"
        file_path: str | None = None
        generated_at: Timestamp = Field(default_factory=lambda: datetime.now(UTC))

    class ConfigModel(BaseModel):
        """Analysis configuration value object."""

        include_patterns: list[str] = Field(default_factory=list)
        exclude_patterns: list[str] = Field(default_factory=list)
        enable_security: bool = True
        enable_complexity: bool = True
        enable_coverage: bool = True
        max_complexity: int = 10
        min_coverage: ScoreRange = 80.0

    class AnalysisMetricsModel(BaseModel):
        """Validated metrics for analysis results - replacing MetricsDict fallbacks."""

        project_path: str = Field(default="", description="Project path analyzed")
        files_analyzed: int = Field(
            default=0, ge=0, description="Number of files analyzed",
        )
        total_lines: int = Field(default=0, ge=0, description="Total lines of code")
        code_lines: int = Field(default=0, ge=0, description="Lines of actual code")
        comment_lines: int | None = Field(
            default=None,
            ge=0,
            description="Lines with comments",
        )
        blank_lines: int | None = Field(default=None, ge=0, description="Blank lines")
        overall_score: ScoreRange = Field(
            default=0.0, description="Overall quality score",
        )
        coverage_score: ScoreRange = Field(
            default=0.0, description="Test coverage score",
        )
        complexity_score: ScoreRange = Field(
            default=0.0,
            description="Code complexity score",
        )
        security_score: ScoreRange = Field(default=0.0, description="Security score")
        maintainability_score: ScoreRange = Field(
            default=0.0,
            description="Maintainability score",
        )
        duplication_score: ScoreRange = Field(
            default=0.0, description="Duplication score",
        )

    class AnalysisResults(BaseModel):
        """Analysis results value object."""

        issues: list[FlextQualityModels.IssueDict] = Field(default_factory=list)
        metrics: FlextQualityModels.AnalysisMetricsModel | dict[str, object] = Field(
            default_factory=dict,
            description="Analysis metrics - use AnalysisMetricsModel for new code",
        )
        recommendations: list[str] = Field(default_factory=list)
        overall_score: ScoreRange = 0.0
        coverage_score: ScoreRange = 0.0
        security_score: ScoreRange = 0.0
        complexity_score: ScoreRange = 0.0
        quality_grade: str = Field(
            default="F",
            description="Quality grade letter (A+ to F)",
        )

        # Optional issue type lists for compatibility
        security_issues: list[FlextQualityModels.IssueModel] = Field(
            default_factory=list,
        )
        complexity_issues: list[FlextQualityModels.IssueModel] = Field(
            default_factory=list,
        )
        dead_code_issues: list[FlextQualityModels.IssueModel] = Field(
            default_factory=list,
        )
        duplication_issues: list[FlextQualityModels.IssueModel] = Field(
            default_factory=list,
        )

        # Metrics property for compatibility
        @property
        def overall_metrics(self) -> FlextQualityModels.OverallMetrics:
            """Get overall metrics object."""
            metrics = (
                self.metrics
                if isinstance(self.metrics, FlextQualityModels.AnalysisMetricsModel)
                else FlextQualityModels.AnalysisMetricsModel()
            )
            return FlextQualityModels.OverallMetrics(
                files_analyzed=metrics.files_analyzed,
                coverage_score=metrics.coverage_score,
                total_issues=len(
                    self.security_issues
                    + self.complexity_issues
                    + self.dead_code_issues
                    + self.duplication_issues,
                ),
                critical_issues=len([
                    i
                    for i in (self.security_issues + self.complexity_issues)
                    if i.severity == FlextQualityModels.IssueSeverity.CRITICAL
                ]),
                high_issues=len([
                    i
                    for i in (self.security_issues + self.complexity_issues)
                    if i.severity == FlextQualityModels.IssueSeverity.HIGH
                ]),
                overall_score=self.overall_score,
            )

        @property
        def total_issues(self) -> int:
            """Calculate total issue count."""
            return (
                len(self.security_issues)
                + len(self.complexity_issues)
                + len(self.dead_code_issues)
                + len(self.duplication_issues)
            )

    class TestResults(BaseModel):
        """Test execution results value object."""

        total_tests: int = 0
        passed_tests: int = 0
        failed_tests: int = 0
        skipped_tests: int = 0
        coverage_percent: ScoreRange = 0.0

    class CheckResult(BaseModel):
        """Quality check result value object."""

        check_name: str = Field(description="Name of the quality check")
        status: c.Quality.Literals.CheckStatusLiteral | str = Field(
            description="Check status: passed, failed, warning",
        )
        issues_found: int = 0
        score: ScoreRange = 0.0
        details: FlextQualityModels.CheckDetailsDict | None = None

    class AnalysisResult(BaseModel):
        """Simple analysis result for API responses."""

        analysis_id: str = Field(description="Analysis identifier")
        project_path: str = Field(description="Project path analyzed")
        status: c.Quality.Literals.AnalysisStatusLiteral | str = Field(
            description="Analysis status",
        )
        issues_found: int = 0
        overall_score: ScoreRange = 0.0
        quality_grade: str = "F"

    class Dependency(BaseModel):
        """Dependency information for projects."""

        name: str = Field(description="Package name")
        version: str | None = Field(default=None, description="Package version")
        requirement: str | None = Field(
            default=None, description="Requirement specifier",
        )

    class OverallMetrics(BaseModel):
        """Consolidated metrics for analysis results."""

        files_analyzed: int = 0
        total_issues: int = 0
        critical_issues: int = 0
        high_issues: int = 0
        medium_issues: int = 0
        low_issues: int = 0
        info_issues: int = 0
        coverage_score: ScoreRange = 0.0
        overall_score: ScoreRange = 0.0

    # =====================================================================
    # VALUE OBJECTS - Simple, immutable value objects for domain concepts
    # =====================================================================

    class ComplexityMetric(BaseModel):
        """Value object for complexity metrics."""

        cyclomatic: int = Field(default=0, ge=0, description="Cyclomatic complexity")
        cognitive: int = Field(default=0, ge=0, description="Cognitive complexity")
        max_depth: int = Field(default=0, ge=0, description="Maximum nesting depth")

        model_config = {"frozen": True}

    class CoverageMetric(BaseModel):
        """Value object for test coverage metrics."""

        line_coverage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Line coverage percentage",
        )
        branch_coverage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Branch coverage percentage",
        )
        function_coverage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Function coverage percentage",
        )

        model_config = {"frozen": True}

    class DuplicationMetric(BaseModel):
        """Value object for code duplication metrics."""

        percentage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Duplication percentage",
        )
        lines: int = Field(default=0, ge=0, description="Number of duplicate lines")

        model_config = {"frozen": True}

    class IssueLocation(BaseModel):
        """Value object for issue location information."""

        file_path: str = Field(description="File path containing the issue")
        line_number: PositiveInt = Field(description="Line number of the issue")
        column_number: PositiveInt = Field(description="Column number of the issue")

        model_config = {"frozen": True}

    class QualityScore(BaseModel):
        """Value object for quality scores with timestamp."""

        score: float = Field(ge=0.0, le=100.0, description="Quality score")
        grade: str = Field(description="Quality grade (A+, A, B, etc.)")
        timestamp: Timestamp = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Score timestamp",
        )

        model_config = {"frozen": True}

    class QualityValidationResult(BaseModel):
        """Quality validation result value object."""

        passed: bool = Field(description="Whether validation passed")
        checks_run: int = Field(ge=0, description="Number of checks run")
        checks_passed: int = Field(ge=0, description="Number of checks passed")
        failures: list[str] = Field(
            default_factory=list, description="List of failures",
        )
        message: str | None = Field(default=None, description="Optional message")

    class AppConfig(BaseModel):
        """Application configuration for web interface."""

        title: str = Field(default="flext-quality", description="Application title")
        version: str = Field(default="0.9.0", description="Application version")
        enable_cors: bool = Field(default=True, description="Enable CORS")
        enable_docs: bool = Field(default=True, description="Enable API documentation")
        debug: bool = Field(default=False, description="Debug mode")
        host: str = Field(default="127.0.0.1", description="Server host")
        port: int = Field(default=8000, ge=1, le=65535, description="Server port")

    class RewriteResult(BaseModel):
        """Git history rewrite operation result."""

        commits_processed: int = Field(
            default=0, description="Number of commits processed",
        )
        commits_changed: int = Field(default=0, description="Number of commits changed")
        errors: list[str] = Field(default_factory=list, description="List of errors")
        dry_run: bool = Field(default=True, description="Whether this was a dry run")

    class OptimizationTarget(BaseModel):
        """Optimization target specification."""

        project_path: str = Field(default=".", description="Path to project")
        module_name: str = Field(default="", description="Module name")
        file_path: str = Field(default="", description="Path to file")
        optimization_type: str = Field(default="", description="Type of optimization")

    class OptimizationResult(BaseModel):
        """Code optimization operation result."""

        target: FlextQualityModels.OptimizationTarget = Field(
            description="Optimization target",
        )
        changes_made: int = Field(default=0, description="Number of changes made")
        success: bool = Field(
            default=True, description="Whether optimization succeeded",
        )
        errors: list[str] = Field(default_factory=list, description="List of errors")
        warnings: list[str] = Field(
            default_factory=list, description="List of warnings",
        )

    class DependencyInfo(BaseModel):
        """Dependency information model."""

        name: str = Field(description="Dependency name")
        version: str = Field(default="", description="Version constraint")
        source: str = Field(default="", description="Source of dependency")
        is_direct: bool = Field(default=True, description="Whether direct dependency")

    class Analysis(BaseModel):
        """Analysis model for analysis operations."""

        analysis_id: str = Field(description="Unique analysis ID")
        project_path: str = Field(description="Path to analyzed project")
        status: str = Field(default="pending", description="Analysis status")
        results: dict[str, object] = Field(default_factory=dict, description="Results")

    class Report(BaseModel):
        """Report model for report operations."""

        report_id: str = Field(description="Unique report ID")
        analysis_id: str = Field(description="Related analysis ID")
        format: str = Field(default="json", description="Report format")
        content: dict[str, object] = Field(default_factory=dict, description="Content")


m = FlextQualityModels
m_quality = FlextQualityModels

__all__ = [
    "FlextQualityModels",
    "m",
    "m_quality",
]
