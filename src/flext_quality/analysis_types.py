"""Specific types for analysis results, replacing dict[str, object] usage.

This module defines strongly-typed data structures for analysis results,
eliminating the use of weakly-typed dictionaries that cause type issues.

All types follow Pydantic patterns and integrate with the FLEXT ecosystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from flext_core.models import FlextModel
from pydantic import Field

from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
)


# Use enums from domain.value_objects (single source of truth)
# Define issue classes
class FileAnalysisResult(FlextModel):
    """Result of analyzing a single file."""

    file_path: Path = Field(..., description="Path to the analyzed file")
    lines_of_code: int = Field(default=0, ge=0, description="Total lines of code")
    complexity_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Complexity score"
    )
    security_issues: int = Field(
        default=0, ge=0, description="Number of security issues"
    )
    style_issues: int = Field(default=0, ge=0, description="Number of style issues")
    dead_code_lines: int = Field(default=0, ge=0, description="Lines of dead code")


class ComplexityIssue(FlextModel):
    """Represents a complexity issue in code."""

    file_path: str = Field(..., description="File where issue was found")
    function_name: str = Field(..., description="Function with complexity issue")
    line_number: int = Field(..., ge=1, description="Line number of function")
    complexity_value: int = Field(..., ge=1, description="Cyclomatic complexity value")
    issue_type: str = Field("high_complexity", description="Type of complexity issue")
    message: str = Field(..., description="Description of the complexity issue")


class SecurityIssue(FlextModel):
    """Represents a security issue in code."""

    file_path: str = Field(..., description="File where issue was found")
    line_number: int = Field(..., ge=0, description="Line number of issue")
    issue_type: IssueType = Field(..., description="Type of security issue")
    severity: IssueSeverity = Field(..., description="Severity level")
    message: str = Field(..., description="Description of the security issue")
    rule_id: str | None = Field(None, description="Security rule that triggered")


class DeadCodeIssue(FlextModel):
    """Represents dead code detected in analysis."""

    file_path: str = Field(..., description="File containing dead code")
    line_number: int = Field(..., ge=1, description="Starting line of dead code")
    end_line_number: int = Field(..., ge=1, description="Ending line of dead code")
    code_type: str = Field(
        ..., description="Type of dead code (function, class, variable)"
    )
    message: str = Field(..., description="Description of the dead code")


class DuplicationIssue(FlextModel):
    """Represents code duplication detected in analysis."""

    files: list[str] = Field(
        ..., min_length=2, description="Files containing duplicated code"
    )
    similarity: float = Field(..., ge=0.0, le=1.0, description="Similarity percentage")
    line_ranges: list[tuple[int, int]] = Field(
        ..., description="Line ranges of duplicated code"
    )
    message: str = Field(..., description="Description of the duplication")


# Define metrics classes
class OverallMetrics(FlextModel):
    """Overall quality metrics from analysis."""

    files_analyzed: int = Field(default=0, ge=0, description="Total files analyzed")
    total_lines: int = Field(default=0, ge=0, description="Total lines of code")
    quality_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Overall quality score"
    )
    coverage_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Test coverage score"
    )
    security_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Security score"
    )
    duplication_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Duplication score"
    )
    maintainability_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Maintainability score"
    )
    complexity_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Complexity score"
    )


# Define the main results class last
class AnalysisResults(FlextModel):
    """Complete results from code analysis."""

    overall_metrics: Annotated[OverallMetrics, Field(default_factory=OverallMetrics)]
    file_metrics: Annotated[list[FileAnalysisResult], Field(default_factory=list)]
    complexity_issues: Annotated[list[ComplexityIssue], Field(default_factory=list)]
    security_issues: Annotated[list[SecurityIssue], Field(default_factory=list)]
    dead_code_issues: Annotated[list[DeadCodeIssue], Field(default_factory=list)]
    duplication_issues: Annotated[list[DuplicationIssue], Field(default_factory=list)]

    @property
    def total_issues(self) -> int:
        """Calculate total number of issues found."""
        return (
            len(self.complexity_issues)
            + len(self.security_issues)
            + len(self.dead_code_issues)
            + len(self.duplication_issues)
        )

    @property
    def critical_issues(self) -> int:
        """Count critical severity issues."""
        return len(
            [
                issue
                for issue in self.security_issues
                if issue.severity == IssueSeverity.CRITICAL
            ]
        )


__all__ = [
    "AnalysisResults",
    "ComplexityIssue",
    "DeadCodeIssue",
    "DuplicationIssue",
    "FileAnalysisResult",
    "IssueSeverity",
    "IssueType",
    "OverallMetrics",
    "SecurityIssue",
]

# Rebuild all models to resolve forward references and ensure proper typing
try:
    FileAnalysisResult.model_rebuild()
    ComplexityIssue.model_rebuild()
    SecurityIssue.model_rebuild()
    DeadCodeIssue.model_rebuild()
    DuplicationIssue.model_rebuild()
    OverallMetrics.model_rebuild()
    AnalysisResults.model_rebuild()
except Exception as e:
    # Log rebuild errors but don't fail import
    import logging

    logging.getLogger(__name__).debug("Model rebuild warning: %s", e)
