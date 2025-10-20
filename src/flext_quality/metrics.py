"""FLEXT Quality Metrics - Immutable quality measurements with utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import cast

from flext_core import FlextModels, FlextResult, FlextTypes
from pydantic import Field

from .grade_calculator import QualityGradeCalculator
from .models import FlextQualityModels

# Constants
MAX_QUALITY_SCORE = 100


class QualityMetrics(FlextModels.Value):
    """Immutable quality metrics value object.

    Encapsulates comprehensive code quality measurements including overall scoring,
    category-specific scores, and detailed metrics from code analysis results.

    Use MetricsFactory to create instances, MetricsCalculator for score calculations.
    """

    # Overall metrics
    overall_score: float = Field(
        0.0, description="Overall quality score (0-100)", ge=0, le=100
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
        0, description="Number of duplicate blocks", ge=0
    )
    complexity_issues_count: int = Field(
        0, description="Number of complexity issues", ge=0
    )

    # Scores by category (0-100)
    complexity_score: float = Field(
        100.0, description="Complexity score (0-100)", ge=0, le=100
    )
    security_score: float = Field(
        100.0, description="Security score (0-100)", ge=0, le=100
    )
    maintainability_score: float = Field(
        100.0, description="Maintainability score (0-100)", ge=0, le=100
    )
    duplication_score: float = Field(
        100.0, description="Duplication score (0-100)", ge=0, le=100
    )
    documentation_score: float = Field(
        100.0, description="Documentation score (0-100)", ge=0, le=100
    )

    @property
    def scores_summary(self) -> FlextTypes.FloatDict:
        """Get summary of all category scores."""
        return {
            "complexity": self.complexity_score,
            "security": self.security_score,
            "maintainability": self.maintainability_score,
            "duplication": self.duplication_score,
            "documentation": self.documentation_score,
        }

    @property
    def total_issues(self) -> int:
        """Calculate total count of all detected quality issues."""
        return (
            self.security_issues_count
            + self.dead_code_items_count
            + self.duplicate_blocks_count
            + self.complexity_issues_count
        )

    def to_dict(
        self,
        *,
        by_alias: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, object]:
        """Export metrics as dictionary for serialization."""
        base: dict[str, object] = {
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
        _ = (by_alias, exclude_none)
        return base

    def get_summary(self) -> str:
        """Generate human-readable quality metrics summary."""
        return (
            f"Quality Grade: {self.quality_grade} ({self.overall_score:.1f}/100)\n"
            f"Files: {self.total_files}, Lines: {self.total_lines_of_code:,}\n"
            f"Functions: {self.total_functions}, Classes: {self.total_classes}\n"
            f"Issues: Security({self.security_issues_count}), "
            f"Complexity({self.complexity_issues_count}), "
            f"DeadCode({self.dead_code_items_count}), "
            f"Duplicates({self.duplicate_blocks_count})"
        )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate metrics against business rules."""
        # Validate score range
        if self.overall_score < 0 or self.overall_score > MAX_QUALITY_SCORE:
            return FlextResult[None].fail("Overall score must be between 0 and 100")

        # Validate counts are non-negative
        if any(
            count < 0
            for count in [
                self.total_files,
                self.total_lines_of_code,
                self.total_functions,
                self.total_classes,
                self.security_issues_count,
                self.dead_code_items_count,
                self.duplicate_blocks_count,
                self.complexity_issues_count,
            ]
        ):
            return FlextResult[None].fail("All counts must be non-negative")

        # Validate complexity scores
        if (
            self.average_complexity < 0
            or self.max_complexity < 0
            or self.max_complexity < self.average_complexity
        ):
            return FlextResult[None].fail("Complexity scores must be valid")

        # Validate all scores are in range
        for score_name, score_value in self.scores_summary.items():
            if score_value < 0 or score_value > MAX_QUALITY_SCORE:
                return FlextResult[None].fail(
                    f"{score_name} score must be between 0 and 100"
                )

        return FlextResult[None].ok(None)


# =====================================================================
# Factory - Single Responsibility: Object Creation
# =====================================================================


class MetricsFactory:
    """Creates QualityMetrics instances from various sources."""

    @staticmethod
    def create_default() -> QualityMetrics:
        """Create QualityMetrics with all default values."""
        return QualityMetrics(
            overall_score=0.0,
            quality_grade="F",
            total_files=0,
            total_lines_of_code=0,
            total_functions=0,
            total_classes=0,
            average_complexity=0.0,
            max_complexity=0.0,
            complex_files_count=0,
            security_issues_count=0,
            dead_code_items_count=0,
            duplicate_blocks_count=0,
            complexity_issues_count=0,
            complexity_score=100.0,
            security_score=100.0,
            maintainability_score=100.0,
            duplication_score=100.0,
            documentation_score=100.0,
        )

    @staticmethod
    def create_with_defaults(**overrides: object) -> QualityMetrics:
        """Create QualityMetrics with optional field overrides."""

        def get_float(key: str, default: float) -> float:
            value = overrides.get(key, default)
            return float(value) if isinstance(value, (int, float)) else default

        def get_int(key: str, default: int) -> int:
            value = overrides.get(key, default)
            return int(value) if isinstance(value, (int, float)) else default

        def get_str(key: str, default: str) -> str:
            value = overrides.get(key, default)
            return str(value) if isinstance(value, str) else default

        return QualityMetrics(
            overall_score=get_float("overall_score", 0.0),
            quality_grade=get_str("quality_grade", "F"),
            total_files=get_int("total_files", 0),
            total_lines_of_code=get_int("total_lines_of_code", 0),
            total_functions=get_int("total_functions", 0),
            total_classes=get_int("total_classes", 0),
            average_complexity=get_float("average_complexity", 0.0),
            max_complexity=get_float("max_complexity", 0.0),
            complex_files_count=get_int("complex_files_count", 0),
            security_issues_count=get_int("security_issues_count", 0),
            dead_code_items_count=get_int("dead_code_items_count", 0),
            duplicate_blocks_count=get_int("duplicate_blocks_count", 0),
            complexity_issues_count=get_int("complexity_issues_count", 0),
            complexity_score=get_float("complexity_score", 100.0),
            security_score=get_float("security_score", 100.0),
            maintainability_score=get_float("maintainability_score", 100.0),
            duplication_score=get_float("duplication_score", 100.0),
            documentation_score=get_float("documentation_score", 100.0),
        )

    @staticmethod
    def from_analysis_results(
        results: FlextQualityModels.AnalysisResults | dict[str, object],
    ) -> QualityMetrics:
        """Create QualityMetrics from analysis results."""
        if isinstance(results, dict):
            return MetricsCalculator.calculate_from_dict(results)
        return MetricsCalculator.calculate_from_object(results)


# =====================================================================
# Calculator - Single Responsibility: Score Calculations
# =====================================================================


class MetricsCalculator:
    """Calculates quality metrics from analysis results."""

    @staticmethod
    def calculate_from_dict(results: dict[str, object]) -> QualityMetrics:
        """Calculate metrics from legacy dict format."""

        def get_int_from_dict(
            source: dict[str, object], key: str, default: int = 0
        ) -> int:
            """Extract integer value with type checking."""
            value = source.get(key, default)
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                return int(value)
            return default

        # Extract metrics
        metrics_raw = results.get("metrics", {})
        metrics: dict[str, object] = cast("dict[str, object]", metrics_raw)
        if isinstance(metrics, dict):
            files_analyzed = get_int_from_dict(metrics, "total_files", 0)
            total_lines = get_int_from_dict(metrics, "total_lines_of_code", 0)
            total_functions = get_int_from_dict(metrics, "total_functions", 0)
            total_classes = get_int_from_dict(metrics, "total_classes", 0)
        else:
            files_analyzed = get_int_from_dict(results, "files_analyzed", 0)
            total_lines = get_int_from_dict(results, "total_lines_of_code", 0)
            total_functions = get_int_from_dict(results, "total_functions", 0)
            total_classes = get_int_from_dict(results, "total_classes", 0)

        # Extract issues
        issues_raw = results.get("issues", {})
        issues: dict[str, object] = cast("dict[str, object]", issues_raw)
        if isinstance(issues, dict):
            security_count = len(cast("list[object]", issues.get("security", [])))
            complexity_count = len(cast("list[object]", issues.get("complexity", [])))
            dead_code_count = len(cast("list[object]", issues.get("dead_code", [])))
            duplicate_count = len(cast("list[object]", issues.get("duplicates", [])))
        else:
            security_count = complexity_count = dead_code_count = duplicate_count = 0

        # Calculate scores
        total_issues = (
            security_count + complexity_count + dead_code_count + duplicate_count
        )
        quality_score = max(0, 100 - (total_issues * 5))

        return QualityMetrics(
            overall_score=quality_score,
            quality_grade="B",
            total_files=files_analyzed,
            total_lines_of_code=total_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            average_complexity=0.0,
            max_complexity=0.0,
            complex_files_count=0,
            security_issues_count=security_count,
            dead_code_items_count=dead_code_count,
            duplicate_blocks_count=duplicate_count,
            complexity_issues_count=complexity_count,
            complexity_score=max(0, 100 - (complexity_count * 10)),
            security_score=max(0, 100 - (security_count * 15)),
            maintainability_score=80.0,
            duplication_score=max(0, 100 - (duplicate_count * 8)),
            documentation_score=75.0,
        )

    @staticmethod
    def calculate_from_object(
        results: FlextQualityModels.AnalysisResults,
    ) -> QualityMetrics:
        """Calculate metrics from typed analysis results object."""
        # Extract file metrics
        total_files = len(results.file_metrics)
        total_loc = sum(file.lines_of_code for file in results.file_metrics)

        # Extract complexity metrics
        complexity_values: FlextTypes.IntList = [
            int(getattr(issue, "complexity_value", 0))
            for issue in results.complexity_issues
        ]
        avg_complexity = (
            sum(complexity_values) / len(complexity_values)
            if complexity_values
            else 0.0
        )
        max_complexity = float(max(complexity_values)) if complexity_values else 0.0

        # Extract issue counts
        security_count = len(results.security_issues)
        dead_code_count = len(results.dead_code_issues)
        duplicate_count = len(results.duplication_issues)
        complexity_count = len(results.complexity_issues)

        # Calculate component scores
        complexity_score = max(0.0, 100.0 - (avg_complexity * 5))
        security_score = max(0.0, 100.0 - (security_count * 10))
        maintainability_score = max(0.0, 100.0 - (complexity_count * 5))
        duplication_score = max(0.0, 100.0 - (duplicate_count * 10))
        documentation_score = 75.0

        # Calculate overall score (weighted average)
        overall_score = (
            complexity_score * 0.25
            + security_score * 0.25
            + maintainability_score * 0.2
            + duplication_score * 0.15
            + documentation_score * 0.15
        )

        # Calculate quality grade
        quality_grade_enum = QualityGradeCalculator.calculate_grade(overall_score)
        quality_grade = quality_grade_enum.value

        return QualityMetrics(
            overall_score=overall_score,
            quality_grade=quality_grade,
            total_files=total_files,
            total_lines_of_code=total_loc,
            total_functions=0,  # Not available from results
            total_classes=0,  # Not available from results
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
