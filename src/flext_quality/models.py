"""FLEXT Quality Models - Simple, pragmatic domain models.

Using Pydantic v2 BaseModel directly without over-engineering.
Follows SOLID principles and FLEXT DDD patterns minimally.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# Type aliases (from typings.py)
from flext_quality.typings import PositiveInt, ScoreRange, Timestamp

# =====================================================================
# STATUS & SEVERITY ENUMERATIONS (Module-level)
# =====================================================================


class AnalysisStatus(StrEnum):
    """Analysis status values."""

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
    """Issue types for categorization."""

    SYNTAX_ERROR = "syntax_error"
    STYLE_VIOLATION = "style_violation"
    SECURITY_VULNERABILITY = "security_vulnerability"
    HIGH_COMPLEXITY = "high_complexity"
    DUPLICATE_CODE = "duplicate_code"
    MISSING_DOCSTRING = "missing_docstring"
    UNUSED_CODE = "unused_code"
    TYPE_ERROR = "type_error"


class QualityGrade(StrEnum):
    """Quality grades with comprehensive scale (A+ through F)."""

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
    F = "F"


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
    status: AnalysisStatus = Field(default=AnalysisStatus.QUEUED)
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
    issue_type: IssueType = Field(description="Type of issue")
    severity: IssueSeverity = Field(default=IssueSeverity.MEDIUM)
    message: str = Field(description="Issue description")
    rule_id: str | None = None


class RuleModel(BaseModel):
    """Quality rule entity - represents a configurable quality check."""

    id: str = Field(description="Unique rule identifier")
    rule_id: str = Field(description="Rule code (e.g., E302, W605)")
    category: IssueType = Field(description="Type of issue the rule checks")
    severity: IssueSeverity = Field(default=IssueSeverity.MEDIUM)
    enabled: bool = Field(default=True, description="Whether rule is active")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Rule parameters"
    )
    description: str | None = Field(default=None, description="Rule description")

    def enable(self) -> RuleModel:
        """Enable this rule."""
        return self.model_copy(update={"enabled": True})

    def disable(self) -> RuleModel:
        """Disable this rule."""
        return self.model_copy(update={"enabled": False})

    def update_severity(self, severity: IssueSeverity) -> RuleModel:
        """Update rule severity."""
        return self.model_copy(update={"severity": severity})

    def set_parameter(self, key: str, value: Any) -> RuleModel:
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


class AnalysisResults(BaseModel):
    """Analysis results value object."""

    issues: list[dict[str, Any]] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    overall_score: ScoreRange = 0.0
    coverage_score: ScoreRange = 0.0
    security_score: ScoreRange = 0.0
    complexity_score: ScoreRange = 0.0
    quality_grade: str = Field(
        default="F", description="Quality grade letter (A+ to F)"
    )


class TestResults(BaseModel):
    """Test execution results value object."""

    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    coverage_percent: ScoreRange = 0.0


class AnalysisResult(BaseModel):
    """Simple analysis result for API responses."""

    analysis_id: str = Field(description="Analysis identifier")
    project_path: str = Field(description="Project path analyzed")
    status: str = Field(description="Analysis status")
    issues_found: int = 0
    overall_score: ScoreRange = 0.0
    quality_grade: str = "F"


class Dependency(BaseModel):
    """Dependency information for projects."""

    name: str = Field(description="Package name")
    version: str | None = Field(default=None, description="Package version")
    requirement: str | None = Field(default=None, description="Requirement specifier")


class OverallMetrics(BaseModel):
    """Consolidated metrics for analysis results."""

    files_analyzed: int = 0
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    info_issues: int = 0
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
        default=0.0, ge=0.0, le=100.0, description="Line coverage percentage"
    )
    branch_coverage: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Branch coverage percentage"
    )
    function_coverage: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Function coverage percentage"
    )

    model_config = {"frozen": True}


class DuplicationMetric(BaseModel):
    """Value object for code duplication metrics."""

    percentage: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Duplication percentage"
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
        default_factory=lambda: datetime.now(UTC), description="Score timestamp"
    )

    model_config = {"frozen": True}


# =====================================================================
# NAMESPACE CLASS - Maintains backwards compatibility with test code
# =====================================================================


class FlextQualityModels:
    """FLEXT Quality Models - Unified namespace for models."""

    # Import module-level models into namespace
    ProjectModel = ProjectModel
    AnalysisModel = AnalysisModel
    IssueModel = IssueModel
    RuleModel = RuleModel
    ReportModel = ReportModel
    ConfigModel = ConfigModel
    AnalysisResults = AnalysisResults
    TestResults = TestResults
    AnalysisResult = AnalysisResult
    Dependency = Dependency
    OverallMetrics = OverallMetrics

    # Value objects
    ComplexityMetric = ComplexityMetric
    CoverageMetric = CoverageMetric
    DuplicationMetric = DuplicationMetric
    IssueLocation = IssueLocation
    QualityScore = QualityScore

    # Enums
    AnalysisStatus = AnalysisStatus
    IssueSeverity = IssueSeverity
    IssueType = IssueType
    QualityGrade = QualityGrade

    # Aliases for compatibility
    CodeIssue = IssueModel  # For analysis_types.py compatibility
    ComplexityIssue = IssueModel
    SecurityIssue = IssueModel
    DeadCodeIssue = IssueModel
    DuplicationIssue = IssueModel
    Issue = IssueModel
    Report = ReportModel
    Analysis = AnalysisModel
    Project = ProjectModel
    Config = ConfigModel
    Results = AnalysisResults
