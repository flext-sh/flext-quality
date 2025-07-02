"""Quality metrics calculation and management."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class QualityMetrics:
    """Quality metrics for code analysis."""

    # Overall metrics
    overall_score: float = 0.0
    quality_grade: str = "F"

    # File metrics
    total_files: int = 0
    total_lines_of_code: int = 0
    total_functions: int = 0
    total_classes: int = 0

    # Complexity metrics
    average_complexity: float = 0.0
    max_complexity: float = 0.0
    complex_files_count: int = 0

    # Issue counts
    security_issues_count: int = 0
    dead_code_items_count: int = 0
    duplicate_blocks_count: int = 0
    complexity_issues_count: int = 0

    # Scores by category (0-100)
    complexity_score: float = 100.0
    security_score: float = 100.0
    maintainability_score: float = 100.0
    duplication_score: float = 100.0
    documentation_score: float = 100.0

    @classmethod
    def from_analysis_results(cls, results: dict[str, Any]) -> QualityMetrics:
        """Create metrics from analysis results.

        Args:
            results: Analysis results dictionary.

        Returns:
            QualityMetrics instance.
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

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary.

        Returns:
            Dictionary representation of metrics.
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
            "scores": {
                "complexity": self.complexity_score,
                "security": self.security_score,
                "maintainability": self.maintainability_score,
                "duplication": self.duplication_score,
                "documentation": self.documentation_score,
            },
        }

    def get_summary(self) -> str:
        """Get a human-readable summary.

        Returns:
            Summary string.
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

    @staticmethod
    def _calculate_grade(score: float) -> str:
        """Calculate letter grade from numeric score."""
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "A-"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "B-"
        elif score >= 65:
            return "C+"
        elif score >= 60:
            return "C"
        elif score >= 55:
            return "C-"
        elif score >= 50:
            return "D+"
        elif score >= 45:
            return "D"
        else:
            return "F"
