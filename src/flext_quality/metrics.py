"""Quality Metrics - Comprehensive Code Quality Measurement and Scoring.

This module provides the QualityMetrics value object that encapsulates
comprehensive code quality measurements, scoring algorithms, and quality
grade calculations for the FLEXT Quality analysis system.

Key Features:
    - Multi-dimensional quality scoring (complexity, security, maintainability)
    - Standardized quality grading with letter grades (A+ to F)
    - Comprehensive metrics aggregation from analysis results
    - Domain rule validation for data integrity
    - Export capabilities for reporting and integration

Scoring Categories:
    - Complexity Score: Based on cyclomatic complexity measurements
    - Security Score: Derived from security vulnerability detection
    - Maintainability Score: Calculated from code structure metrics
    - Duplication Score: Based on duplicate code detection
    - Documentation Score: Assessment of code documentation quality

Architecture:
    Built as a FlextValueObject using flext-core patterns for immutability
    and validation. Integrates with QualityGradeCalculator for consistent
    grading across the FLEXT ecosystem.

Integration:
    - Uses flext-core.FlextValueObject for immutable data structures
    - Integrates with domain layer for grade calculation
    - Provides dict[str, object] compatibility for data exchange
    - Supports validation through FlextResult patterns

Example:
    Creating metrics from analysis results:

    >>> results = analyzer.analyze_project()
    >>> metrics = QualityMetrics.from_analysis_results(results)
    >>> print(f"Grade: {metrics.quality_grade} ({metrics.overall_score:.1f})")
    >>> print(metrics.get_summary())

Author: FLEXT Development Team
Version: 0.9.0

"""

from __future__ import annotations

from pydantic import Field, computed_field

from flext_core import FlextResult, FlextValueObject
from flext_quality.domain.quality_grade_calculator import QualityGradeCalculator


class QualityMetrics(FlextValueObject):
    """Comprehensive Quality Metrics Value Object.

    Immutable value object that encapsulates comprehensive code quality
    measurements including overall scoring, category-specific scores,
    and detailed metrics from code analysis results.

    This class serves as the central data structure for quality assessment,
    providing standardized quality scoring and grading across the FLEXT
    ecosystem. Built on flext-core patterns for consistency and reliability.

    Attributes:
        overall_score: Weighted overall quality score (0-100)
        quality_grade: Letter grade based on overall score (A+ to F)

        File Metrics:
            total_files: Number of files analyzed
            total_lines_of_code: Total non-comment, non-blank lines
            total_functions: Total function definitions
            total_classes: Total class definitions

        Complexity Metrics:
            average_complexity: Mean cyclomatic complexity
            max_complexity: Highest complexity value found
            complex_files_count: Files exceeding complexity threshold

        Issue Counts:
            security_issues_count: Security vulnerabilities detected
            dead_code_items_count: Unused code items found
            duplicate_blocks_count: Duplicate code blocks identified
            complexity_issues_count: High complexity violations

        Category Scores (0-100):
            complexity_score: Code complexity quality score
            security_score: Security vulnerability score
            maintainability_score: Code maintainability score
            duplication_score: Code duplication score
            documentation_score: Documentation quality score

    """

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
    def from_analysis_results(cls, results: dict[str, object]) -> QualityMetrics:
        """Create QualityMetrics from comprehensive analysis results.

        Factory method that processes raw analysis results and calculates
        comprehensive quality metrics including weighted scores, issue counts,
        and overall quality grading.

        Args:
            results: Analysis results dictionary containing:
                - metrics: Aggregated file-level metrics
                - issues: Categorized quality issues by type
                - project_path: Analyzed project location
                - files_analyzed: Number of files processed

        Returns:
            QualityMetrics instance with calculated scores and metrics

        Scoring Algorithm:
            - Overall score is weighted average of category scores:
              * Complexity: 25% weight
              * Security: 25% weight
              * Maintainability: 20% weight
              * Duplication: 15% weight
              * Documentation: 15% weight
            - Category scores penalize issues with configurable weights
            - Quality grade calculated using standardized grade scale

        Note:
            Uses type-safe extraction to handle mixed data types and
            missing values gracefully with appropriate defaults.

        """
        # Extract results data safely
        results_dict = results
        metrics_obj = results_dict.get("metrics", {})
        metrics_data = dict(metrics_obj) if isinstance(metrics_obj, dict) else {}
        issues_obj = results_dict.get("issues", {})
        issues = dict(issues_obj) if isinstance(issues_obj, dict) else {}

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

        # Quality grade - using centralized calculator for consistency
        quality_grade_enum = QualityGradeCalculator.calculate_grade(overall_score)
        quality_grade = quality_grade_enum.value

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
        """Get comprehensive summary of quality scores by category.

        Provides a structured view of all quality category scores for
        reporting, analysis, and integration with monitoring systems.

        Returns:
            Dictionary mapping category names to quality scores (0-100):
            - complexity: Code complexity quality score
            - security: Security vulnerability score
            - maintainability: Code maintainability score
            - duplication: Code duplication score
            - documentation: Documentation quality score

        Note:
            This computed field is automatically updated when the
            underlying score values change, ensuring consistency.

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
        """Calculate total count of all detected quality issues.

        Aggregates issue counts across all analysis categories to provide
        a single metric for overall code quality assessment.

        Returns:
            Sum of all issue counts including:
            - Security vulnerabilities
            - Dead code items
            - Duplicate code blocks
            - Complexity violations

        Note:
            This computed field automatically updates when individual
            issue counts change, providing real-time total calculation.

        """
        return (
            self.security_issues_count
            + self.dead_code_items_count
            + self.duplicate_blocks_count
            + self.complexity_issues_count
        )

    def to_dict(self) -> dict[str, object]:
        """Export metrics as dictionary for serialization and integration.

        Converts the immutable metrics object to a dictionary format suitable
        for JSON serialization, API responses, and integration with external
        systems and reporting tools.

        Returns:
            Dictionary containing all metrics, scores, and computed fields:
            - Basic metrics (files, lines, functions, classes)
            - Quality scores by category and overall
            - Issue counts and totals
            - Computed summary fields

        Note:
            The returned dictionary includes both stored attributes and
            computed fields for comprehensive data export.

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
        """Generate human-readable quality metrics summary.

        Creates a formatted text summary of key quality metrics suitable
        for console output, reports, and dashboard displays.

        Returns:
            Multi-line formatted string containing:
            - Quality grade and overall score
            - File and code statistics (files, lines, functions, classes)
            - Issue breakdown by category with counts

        Format:
            Quality Grade: A (85.2/100)
            Files: 45, Lines: 2,345
            Functions: 123, Classes: 15
            Issues: Security(0), Complexity(3), DeadCode(1), Duplicates(0)

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

    # Architecture Note: Grade calculation centralized in QualityGradeCalculator
    # for consistency across FLEXT ecosystem quality services

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate quality metrics against domain business rules.

        Performs comprehensive validation of all metric values against
        business rules and constraints to ensure data integrity and
        consistency within the quality analysis domain.

        Returns:
            FlextResult indicating validation success or failure with
            specific error messages for any rule violations

        Validation Rules:
            - Overall score must be between 0 and 100
            - All count fields must be non-negative integers
            - Complexity values must be valid (max >= average >= 0)
            - Category scores must be within valid ranges

        Note:
            This method is called automatically during object creation
            and update operations to maintain data integrity.

        """
        # Validate score consistency
        if self.overall_score < 0 or self.overall_score > 100:
            return FlextResult.fail("Overall score must be between 0 and 100")

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
            return FlextResult.fail("All counts must be non-negative")

        # Validate complexity scores
        if (
            self.average_complexity < 0
            or self.max_complexity < 0
            or self.max_complexity < self.average_complexity
        ):
            return FlextResult.fail("Complexity scores must be valid")

        return FlextResult.ok(None)
