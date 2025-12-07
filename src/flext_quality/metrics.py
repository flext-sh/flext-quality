"""FLEXT Quality Metrics - Immutable quality measurements with utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult, t
from pydantic import BaseModel, ConfigDict, Field

from .constants import c
from .grade_calculator import QualityGradeCalculator
from .models import m

MAX_QUALITY_SCORE = c.Quality.Scoring.MAX_QUALITY_SCORE


# =====================================================================
# Legacy Data Models - Parse and validate external data structures
# =====================================================================


class LegacyIssueData(BaseModel):
    """Validated issue from external analysis results."""

    line_number: int = Field(default=1, ge=1)
    severity: str = Field(default="medium")
    message: str = Field(default="")
    rule_id: str = Field(default="")


class LegacyIssuesDict(BaseModel):
    """Validated issues dictionary from legacy results."""

    security: list[LegacyIssueData] = Field(default_factory=list)
    complexity: list[LegacyIssueData] = Field(default_factory=list)
    dead_code: list[LegacyIssueData] = Field(default_factory=list)
    duplicates: list[LegacyIssueData] = Field(default_factory=list)


class LegacyMetricsDict(BaseModel):
    """Validated metrics dictionary from legacy results."""

    total_files: int = Field(default=0, ge=0)
    total_lines_of_code: int = Field(default=0, ge=0)
    total_functions: int = Field(default=0, ge=0)
    total_classes: int = Field(default=0, ge=0)


class LegacyAnalysisResults(BaseModel):
    """Validated legacy analysis results structure."""

    metrics: LegacyMetricsDict = Field(default_factory=LegacyMetricsDict)
    issues: LegacyIssuesDict = Field(default_factory=LegacyIssuesDict)


class QualityMetrics(BaseModel):
    """Immutable quality metrics value object.

    Encapsulates complete code quality measurements including overall scoring,
    category-specific scores, and detailed metrics from code analysis results.

    Use MetricsFactory to create instances, MetricsCalculator for score calculations.
    """

    model_config = ConfigDict(frozen=True)

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

    @property
    def scores_summary(self) -> t.FloatDict:
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

    def to_dict(self) -> dict[str, float | int | str]:
        """Export metrics as dictionary for serialization."""
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

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate metrics against business rules."""
        # Validate score range
        if self.overall_score < 0 or self.overall_score > MAX_QUALITY_SCORE:
            return FlextResult[bool].fail("Overall score must be between 0 and 100")

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
            return FlextResult[bool].fail("All counts must be non-negative")

        # Validate complexity scores
        if (
            self.average_complexity < 0
            or self.max_complexity < 0
            or self.max_complexity < self.average_complexity
        ):
            return FlextResult[bool].fail("Complexity scores must be valid")

        # Validate all scores are in range
        for score_name, score_value in self.scores_summary.items():
            if score_value < 0 or score_value > MAX_QUALITY_SCORE:
                return FlextResult[bool].fail(
                    f"{score_name} score must be between 0 and 100",
                )

        return FlextResult[bool].ok(True)

    @staticmethod
    def from_analysis_results(
        results: m.AnalysisResults | dict[str, object],
    ) -> QualityMetrics:
        """Create QualityMetrics from analysis results."""
        if isinstance(results, dict):
            return MetricsCalculator.calculate_from_dict(results)
        return MetricsCalculator.calculate_from_object(results)


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
    def create_with_defaults(
        overrides: dict[str, float | int | str] | None = None,
    ) -> QualityMetrics:
        """Create QualityMetrics with optional field overrides using builder pattern.

        Uses Pydantic's model_validate to ensure type safety and validation.
        """
        if overrides is None:
            return MetricsFactory.create_default()

        # Create default dict and merge with overrides
        defaults: dict[str, float | int | str] = {
            "overall_score": 0.0,
            "quality_grade": "F",
            "total_files": 0,
            "total_lines_of_code": 0,
            "total_functions": 0,
            "total_classes": 0,
            "average_complexity": 0.0,
            "max_complexity": 0.0,
            "complex_files_count": 0,
            "security_issues_count": 0,
            "dead_code_items_count": 0,
            "duplicate_blocks_count": 0,
            "complexity_issues_count": 0,
            "complexity_score": 100.0,
            "security_score": 100.0,
            "maintainability_score": 100.0,
            "duplication_score": 100.0,
            "documentation_score": 100.0,
        }
        defaults.update(overrides)
        return QualityMetrics.model_validate(defaults)


# =====================================================================
# Calculator - Single Responsibility: Score Calculations
# =====================================================================


class MetricsCalculator:
    """Calculates quality metrics from analysis results."""

    @staticmethod
    def calculate_from_dict(results: dict[str, object]) -> QualityMetrics:
        """Calculate metrics from legacy dict format.

        Validates structure with Pydantic - fail-fast on invalid data.
        """
        # Parse and validate with Pydantic - no fallbacks, strict validation
        validated_results = LegacyAnalysisResults.model_validate(results)

        # Extract validated metrics - direct access, no .get()
        metrics = validated_results.metrics
        issues = validated_results.issues

        # Access validated fields directly
        files_analyzed = metrics.total_files
        total_lines = metrics.total_lines_of_code
        total_functions = metrics.total_functions
        total_classes = metrics.total_classes

        # Count issues from validated lists - no type checks needed
        security_count = len(issues.security)
        complexity_count = len(issues.complexity)
        dead_code_count = len(issues.dead_code)
        duplicate_count = len(issues.duplicates)

        # Calculate scores with proper weights
        total_issues = (
            security_count + complexity_count + dead_code_count + duplicate_count
        )
        overall_score = max(0.0, 100.0 - (total_issues * 5))
        complexity_score = max(0.0, 100.0 - (complexity_count * 10))
        security_score = max(0.0, 100.0 - (security_count * 15))
        duplication_score = max(0.0, 100.0 - (duplicate_count * 8))

        # Calculate maintainability from dead code issues
        maintainability_score = max(0.0, 100.0 - (dead_code_count * 5))

        # Calculate documentation score from actual data or calculation
        documentation_score = max(0.0, 100.0 - (total_functions - total_classes) * 0.5)

        return QualityMetrics(
            overall_score=overall_score,
            quality_grade=QualityGradeCalculator.calculate_grade(overall_score).value,
            total_files=files_analyzed,
            total_lines_of_code=total_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            average_complexity=0.0,
            max_complexity=0.0,
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

    @staticmethod
    def calculate_from_object(
        results: m.AnalysisResults,
    ) -> QualityMetrics:
        """Calculate metrics from typed analysis results object with no fallbacks."""
        # Handle both legacy dict metrics and typed AnalysisMetricsModel
        if isinstance(results.metrics, dict):
            # Legacy: metrics is a dict with average_complexity
            avg_complexity = float(results.metrics.get("average_complexity", 0.0))
            # Count issues from results.issues list (legacy format: [{"type": "...", ...}])
            security_count = sum(
                1
                for i in results.issues
                if isinstance(i, dict) and i.get("type") == "security"
            )
            complexity_count = sum(
                1
                for i in results.issues
                if isinstance(i, dict) and i.get("type") == "complexity"
            )
            dead_code_count = sum(
                1
                for i in results.issues
                if isinstance(i, dict) and i.get("type") == "dead_code"
            )
            duplicate_count = sum(
                1
                for i in results.issues
                if isinstance(i, dict) and i.get("type") == "duplication"
            )
            total_files = 0
            total_loc = 0
        else:
            # Typed model: metrics is AnalysisMetricsModel
            metrics = results.metrics
            avg_complexity = getattr(metrics, "average_complexity", 0.0)
            # Use typed issue lists
            security_count = len(getattr(results, "security_issues", []))
            dead_code_count = len(getattr(results, "dead_code_issues", []))
            duplicate_count = len(getattr(results, "duplication_issues", []))
            complexity_count = len(getattr(results, "complexity_issues", []))
            total_files = metrics.files_analyzed
            total_loc = metrics.total_lines

        max_complexity = 0.0

        # Calculate component scores based on actual metrics and issues
        complexity_score = max(0.0, 100.0 - (avg_complexity * 5))
        security_score = max(0.0, 100.0 - (security_count * 10))
        maintainability_score = max(0.0, 100.0 - (complexity_count * 5))
        duplication_score = max(0.0, 100.0 - (duplicate_count * 10))

        # Calculate documentation score from dead code percentage
        documentation_score = max(0.0, 100.0 - (dead_code_count * 8))

        # Calculate overall score (weighted average)
        overall_score = (
            complexity_score * 0.25
            + security_score * 0.25
            + maintainability_score * 0.2
            + duplication_score * 0.15
            + documentation_score * 0.15
        )

        # Calculate quality grade based on overall score
        quality_grade = QualityGradeCalculator.calculate_grade(overall_score).value

        return QualityMetrics(
            overall_score=overall_score,
            quality_grade=quality_grade,
            total_files=total_files,
            total_lines_of_code=total_loc,
            total_functions=0,
            total_classes=0,
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
