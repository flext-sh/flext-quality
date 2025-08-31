"""Analysis Types for FLEXT-QUALITY.

Following FLEXT patterns: Multiple independent classes per module like flext-core.
Each class is a separate domain model following SOLID principles.
Strongly-typed data structures that integrate with FLEXT ecosystem.
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextModels
from pydantic import Field

from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
)


class FileAnalysisResult(FlextModels):
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


class ComplexityIssue(FlextModels):
    """Represents a complexity issue in code."""

    file_path: str = Field(..., description="File where issue was found")
    function_name: str = Field(..., description="Function with complexity issue")
    line_number: int = Field(..., ge=1, description="Line number of function")
    complexity_value: int = Field(..., ge=1, description="Cyclomatic complexity value")
    message: str = Field(..., description="Human-readable issue message")
    issue_type: str = Field(
        default="high_complexity", description="Type of complexity issue"
    )
    severity: IssueSeverity = Field(
        default=IssueSeverity.MEDIUM, description="Issue severity level"
    )


class SecurityIssue(FlextModels):
    """Represents a security issue found in code."""

    file_path: str = Field(..., description="File where issue was found")
    line_number: int = Field(..., ge=1, description="Line number of issue")
    issue_type: str = Field(..., description="Type of security issue")
    description: str = Field(..., description="Detailed issue description")
    message: str = Field(..., description="Human-readable issue message")
    rule_id: str = Field(..., description="Security rule identifier")
    severity: IssueSeverity = Field(
        default=IssueSeverity.HIGH, description="Security issue severity"
    )
    confidence: str = Field(
        default="MEDIUM", description="Confidence level of detection"
    )


class DeadCodeIssue(FlextModels):
    """Represents dead/unused code found during analysis."""

    file_path: str = Field(..., description="File containing dead code")
    line_number: int = Field(..., ge=1, description="Line number of dead code")
    end_line_number: int = Field(..., ge=1, description="End line number of dead code")
    issue_type: str = Field(..., description="Type of dead code")
    code_type: str = Field(
        ..., description="Type of code element (function, class, etc)"
    )
    code_snippet: str = Field(..., description="The unused code snippet")
    message: str = Field(..., description="Human-readable issue message")
    severity: IssueSeverity = Field(
        default=IssueSeverity.LOW, description="Dead code severity"
    )


class DuplicationIssue(FlextModels):
    """Represents code duplication detected in analysis."""

    files: list[str] = Field(..., description="Files containing duplicated code")
    line_ranges: list[tuple[int, int]] = Field(
        ..., description="Line ranges of duplicate code"
    )
    duplicate_lines: int = Field(..., ge=1, description="Number of duplicate lines")
    similarity: float = Field(
        ..., ge=0.0, le=100.0, description="Similarity score (0.0 to 100.0)"
    )
    similarity_percent: float = Field(
        ..., ge=0.0, le=100.0, description="Percentage similarity"
    )
    message: str = Field(..., description="Human-readable duplication message")
    severity: IssueSeverity = Field(
        default=IssueSeverity.MEDIUM, description="Duplication severity"
    )


class OverallMetrics(FlextModels):
    """Overall metrics for the entire analysis."""

    files_analyzed: int = Field(default=0, ge=0, description="Total files analyzed")
    total_lines: int = Field(default=0, ge=0, description="Total lines of code")
    functions_count: int = Field(default=0, ge=0, description="Total functions")
    classes_count: int = Field(default=0, ge=0, description="Total classes")
    average_complexity: float = Field(
        default=0.0, ge=0.0, description="Average cyclomatic complexity"
    )
    max_complexity: float = Field(
        default=0.0, ge=0.0, description="Maximum complexity found"
    )
    # Quality scores
    quality_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Overall quality score"
    )
    coverage_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Code coverage score"
    )
    security_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Security quality score"
    )
    maintainability_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Maintainability score"
    )
    complexity_score: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Complexity score"
    )


class AnalysisResults(FlextModels):
    """Complete analysis results containing all metrics and issues."""

    overall_metrics: OverallMetrics = Field(
        default_factory=OverallMetrics, description="Overall analysis metrics"
    )
    file_metrics: list[FileAnalysisResult] = Field(
        default_factory=list, description="Per-file analysis results"
    )
    complexity_issues: list[ComplexityIssue] = Field(
        default_factory=list, description="Complexity issues found"
    )
    security_issues: list[SecurityIssue] = Field(
        default_factory=list, description="Security issues found"
    )
    dead_code_issues: list[DeadCodeIssue] = Field(
        default_factory=list, description="Dead code issues found"
    )
    duplication_issues: list[DuplicationIssue] = Field(
        default_factory=list, description="Code duplication issues found"
    )

    @property
    def total_issues(self) -> int:
        """Calculate total number of issues across all categories."""
        return (
            len(self.complexity_issues)
            + len(self.security_issues)
            + len(self.dead_code_issues)
            + len(self.duplication_issues)
        )

    @property
    def critical_issues(self) -> int:
        """Calculate number of critical issues."""
        critical_count = 0
        for sec_issue in self.security_issues:
            if sec_issue.severity == IssueSeverity.HIGH:
                critical_count += 1
        for comp_issue in self.complexity_issues:
            if comp_issue.severity == IssueSeverity.HIGH:
                critical_count += 1
        return critical_count


# Export all classes
__all__ = [
    "AnalysisResults",
    "ComplexityIssue",
    "DeadCodeIssue",
    "DuplicationIssue",
    "FileAnalysisResult",
    # Type aliases for backward compatibility
    "IssueSeverity",
    "IssueType",
    "OverallMetrics",
    "SecurityIssue",
]
