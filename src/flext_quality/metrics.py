"""Quality metrics calculation and management - Modern Python 3.13 + flext-core patterns."""

from __future__ import annotations

from typing import Any, ClassVar

from flext_core.domain.pydantic_base import DomainValueObject
from pydantic import Field, computed_field


class QualityMetrics(DomainValueObject):
    """Quality metrics for code analysis - REFACTORED to use flext-core patterns."""

    # Overall metrics
    overall_score: float = Field(
        0.0,
        description="Overall quality score (0-100)",
        ge=0,
        le=100,
    )
    quality_grade: str = Field("F", description="Quality grade letter (A+ to F)")

    # File metrics
    total_files: int = Field(0, description="Total number of files", ge=0)
    total_lines_of_code: int = Field(0, description="Total lines of code", ge=0)
    total_functions: int = Field(0, description="Total functions", ge=0)
    total_classes: int = Field(0, description="Total classes", ge=0)

    # Complexity metrics
    average_complexity: float = Field(0.0, description="Average complexity score", ge=0)
    max_complexity: float = Field(0.0, description="Maximum complexity score", ge=0)
    complex_files_count: int = Field(0, description="Number of complex files", ge=0)

    # Issue counts
    security_issues_count: int = Field(0, description="Number of security issues", ge=0)
    dead_code_items_count: int = Field(0, description="Number of dead code items", ge=0)
    duplicate_blocks_count: int = Field(
        0,
        description="Number of duplicate blocks",
        ge=0,
    )
    complexity_issues_count: int = Field(
        0,
        description="Number of complexity issues",
        ge=0,
    )

    # Scores by category (0-100)
    complexity_score: float = Field(
        100.0,
        description="Complexity score (0-100)",
        ge=0,
        le=100,
    )
    security_score: float = Field(
        100.0,
        description="Security score (0-100)",
        ge=0,
        le=100,
    )
    maintainability_score: float = Field(
        100.0,
        description="Maintainability score (0-100)",
        ge=0,
        le=100,
    )
    duplication_score: float = Field(
        100.0,
        description="Duplication score (0-100)",
        ge=0,
        le=100,
    )
    documentation_score: float = Field(
        100.0,
        description="Documentation score (0-100)",
        ge=0,
        le=100,
    )

    @classmethod
    def from_analysis_results(cls, results: dict[str, Any]) -> QualityMetrics:
        """Create QualityMetrics from analysis results dictionary.

        Args:
            results: Analysis results containing metrics and issues data.

        Returns:
            QualityMetrics instance with calculated scores and metrics.

        """
        metrics_data = results.get("metrics", {})
        issues = results.get("issues", {})

        # Basic counts
        total_files = metrics_data.get("total_files", 0)
        total_loc = metrics_data.get("total_lines_of_code", 0)
        total_functions = metrics_data.get("total_functions", 0)
        total_classes = metrics_data.get("total_classes", 0)

        # Complexity
        avg_complexity = metrics_data.get("average_complexity", 0.0)
        max_complexity = metrics_data.get("max_complexity", 0.0)

        # Issue counts
        security_count = len(issues.get("security", []))
        dead_code_count = len(issues.get("dead_code", []))
        duplicate_count = len(issues.get("duplicates", []))
        complexity_count = len(issues.get("complexity", []))

        # Calculate component scores
        complexity_score = max(0, 100 - (avg_complexity * 5))
        security_score = max(0, 100 - (security_count * 10))
        maintainability_score = max(0, 100 - (complexity_count * 5))
        duplication_score = max(0, 100 - (duplicate_count * 10))
        documentation_score = 75.0  # Placeholder

        # Overall score (weighted average)
        overall_score = (
            complexity_score * 0.25
            + security_score * 0.25
            + maintainability_score * 0.2
            + duplication_score * 0.15
            + documentation_score * 0.15
        )

        # Quality grade
        quality_grade = cls._calculate_grade(overall_score)

        return cls(
            overall_score=overall_score,
            quality_grade=quality_grade,
            total_files=total_files,
            total_lines_of_code=total_loc,
            total_functions=total_functions,
            total_classes=total_classes,
            average_complexity=avg_complexity,
            max_complexity=max_complexity,
            complex_files_count=complexity_count,
            security_issues_count=security_count,
            dead_code_items_count=dead_code_count,
            duplicate_blocks_count=duplicate_count,
            complexity_issues_count=complexity_count,
            complexity_score=complexity_score,
            security_score=security_score,
            maintainability_score=maintainability_score,
            duplication_score=duplication_score,
            documentation_score=documentation_score,
        )

    @computed_field
    def scores_summary(self) -> dict[str, float]:
        """Get summary of all quality scores by category.

        Returns:
            Dictionary mapping category names to their quality scores.

        """
        return {
            "complexity": self.complexity_score,
            "security": self.security_score,
            "maintainability": self.maintainability_score,
            "duplication": self.duplication_score,
            "documentation": self.documentation_score,
        }

    @computed_field
    def total_issues(self) -> int:
        """Get total count of all quality issues.

        Returns:
            Sum of all issue counts across all categories.

        """
        return (
            self.security_issues_count
            + self.dead_code_items_count
            + self.duplicate_blocks_count
            + self.complexity_issues_count
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary format.

        Returns:
            Dictionary representation of all metrics and scores.

        """
        return {
            "overall_score": self.overall_score,
            "quality_grade": self.quality_grade,
            "total_files": self.total_files,
            "total_lines_of_code": self.total_lines_of_code,
            "total_functions": self.total_functions,
            "total_classes": self.total_classes,
            "average_complexity": self.average_complexity,
            "max_complexity": self.max_complexity,
            "complex_files_count": self.complex_files_count,
            "security_issues_count": self.security_issues_count,
            "dead_code_items_count": self.dead_code_items_count,
            "duplicate_blocks_count": self.duplicate_blocks_count,
            "complexity_issues_count": self.complexity_issues_count,
            "total_issues": self.total_issues,
            "scores": self.scores_summary,
        }

    def get_summary(self) -> str:
        """Get human-readable summary of quality metrics.

        Returns:
            Formatted string summarizing key metrics and issue counts.

        """
        return (
            f"Quality Grade: {self.quality_grade} ({self.overall_score:.1f}/100)\n"
            f"Files: {self.total_files}, Lines: {self.total_lines_of_code:,}\n"
            f"Functions: {self.total_functions}, Classes: {self.total_classes}\n"
            f"Issues: Security({self.security_issues_count}), "
            f"Complexity({self.complexity_issues_count}), "
            f"DeadCode({self.dead_code_items_count}), "
            f"Duplicates({self.duplicate_blocks_count})"
        )

    # Grade thresholds - each tuple is (threshold, grade)
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, str]]] = [
        (95, "A+"),
        (90, "A"),
        (85, "A-"),
        (80, "B+"),
        (75, "B"),
        (70, "B-"),
        (65, "C+"),
        (60, "C"),
        (55, "C-"),
        (50, "D+"),
        (45, "D"),
    ]

    @classmethod
    def _calculate_grade(cls, score: float) -> str:
        """Calculate letter grade based on score using predefined thresholds."""
        for threshold, grade in cls._GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "F"
