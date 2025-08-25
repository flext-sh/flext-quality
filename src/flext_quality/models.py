"""Centralized Pydantic models for flext-quality.

This module provides centralized model definitions following FLEXT patterns,
extending FlextEntity from flext-core for consistency across the ecosystem.

Models are organized by domain responsibility:
- Quality: Core quality analysis models
- Analysis: Analysis execution and results
- Reporting: Report generation and metrics
- Configuration: Analysis configuration models
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from flext_core.models import FlextModel
from pydantic import Field, field_validator

from flext_quality.constants import FlextQualityConstants


class FlextQualityBaseModel(FlextModel):
    """Base model for all quality domain entities extending FlextEntity patterns."""


class FlextQualityProjectModel(FlextQualityBaseModel):
    """Pydantic model for quality project representation."""

    id: UUID = Field(..., description="Unique project identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    path: str = Field(..., description="Project path for analysis")
    description: str | None = Field(None, description="Project description")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate project name follows basic constraints."""
        if not v.strip():
            msg = "Project name cannot be empty"
            raise ValueError(msg)
        return v.strip()


class FlextQualityAnalysisModel(FlextQualityBaseModel):
    """Pydantic model for quality analysis representation."""

    id: UUID = Field(..., description="Unique analysis identifier")
    project_id: UUID = Field(..., description="Associated project identifier")
    status: str = Field(..., description="Analysis status")
    overall_score: float = Field(
        0.0, ge=0.0, le=100.0, description="Overall quality score"
    )
    coverage_score: float = Field(
        0.0, ge=0.0, le=100.0, description="Test coverage score"
    )
    security_score: float = Field(
        0.0, ge=0.0, le=100.0, description="Security analysis score"
    )
    maintainability_score: float = Field(
        0.0, ge=0.0, le=100.0, description="Maintainability score"
    )
    complexity_score: float = Field(
        0.0, ge=0.0, le=100.0, description="Complexity score"
    )
    started_at: datetime = Field(
        default_factory=datetime.now, description="Analysis start time"
    )
    completed_at: datetime | None = Field(None, description="Analysis completion time")
    error_message: str | None = Field(
        None, description="Error message if analysis failed"
    )

    @field_validator(
        "overall_score",
        "coverage_score",
        "security_score",
        "maintainability_score",
        "complexity_score",
    )
    @classmethod
    def validate_score_range(cls, v: float) -> float:
        """Ensure scores are within valid range."""
        return max(0.0, min(100.0, v))


class FlextQualityIssueModel(FlextQualityBaseModel):
    """Pydantic model for quality issue representation."""

    id: UUID = Field(..., description="Unique issue identifier")
    analysis_id: UUID = Field(..., description="Associated analysis identifier")
    file_path: str = Field(..., description="File path where issue was found")
    line_number: int = Field(..., ge=1, description="Line number of the issue")
    column_number: int | None = Field(
        None, ge=1, description="Column number of the issue"
    )
    severity: str = Field(..., description="Issue severity level")
    issue_type: str = Field(..., description="Type of quality issue")
    message: str = Field(..., description="Issue description message")
    rule: str | None = Field(None, description="Rule that triggered this issue")
    source: str = Field(..., description="Analysis backend that detected the issue")

    @field_validator("line_number", "column_number")
    @classmethod
    def validate_positive_numbers(cls, v: int | None) -> int | None:
        """Ensure line and column numbers are positive."""
        if v is not None and v < 1:
            msg = "Line and column numbers must be positive"
            raise ValueError(msg)
        return v


class FlextQualityReportModel(FlextQualityBaseModel):
    """Pydantic model for quality report representation."""

    id: UUID = Field(..., description="Unique report identifier")
    analysis_id: UUID = Field(..., description="Associated analysis identifier")
    format_type: str = Field(..., description="Report format (HTML, JSON, PDF)")
    content: str = Field(..., description="Report content")
    file_path: str | None = Field(None, description="Path to saved report file")
    generated_at: datetime = Field(
        default_factory=datetime.now, description="Report generation time"
    )
    metadata: dict[str, object] = Field(
        default_factory=dict, description="Additional report metadata"
    )


class FlextAnalysisConfigModel(FlextQualityBaseModel):
    """Pydantic model for analysis configuration."""

    include_patterns: list[str] = Field(
        default_factory=list, description="File patterns to include"
    )
    exclude_patterns: list[str] = Field(
        default_factory=list, description="File patterns to exclude"
    )
    enable_security: bool = Field(default=True, description="Enable security analysis")
    enable_complexity: bool = Field(
        default=True, description="Enable complexity analysis"
    )
    enable_coverage: bool = Field(default=True, description="Enable coverage analysis")
    max_complexity: int = Field(
        FlextQualityConstants.Complexity.MAX_COMPLEXITY,
        description="Maximum allowed complexity",
    )
    min_coverage: float = Field(
        FlextQualityConstants.Coverage.MINIMUM_COVERAGE,
        description="Minimum coverage threshold",
    )
    security_threshold: float = Field(
        FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE,
        description="Security score threshold",
    )

    @field_validator("max_complexity")
    @classmethod
    def validate_max_complexity(cls, v: int) -> int:
        """Ensure max complexity is reasonable."""
        return max(1, min(50, v))

    @field_validator("min_coverage", "security_threshold")
    @classmethod
    def validate_percentage(cls, v: float) -> float:
        """Ensure percentage values are within valid range."""
        return max(0.0, min(100.0, v))


# Export models for clean imports
__all__ = [
    "FlextAnalysisConfigModel",
    "FlextQualityAnalysisModel",
    "FlextQualityBaseModel",
    "FlextQualityIssueModel",
    "FlextQualityProjectModel",
    "FlextQualityReportModel",
]
