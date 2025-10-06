"""FLEXT Quality Value Objects - Domain value objects for quality analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import ClassVar, override

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextModels,
    FlextResult,
)
from pydantic import Field

from .constants import FlextQualityConstants


class FlextQualityValueObjects:
    """Unified quality value objects class following FLEXT pattern - ZERO DUPLICATION.

    Single responsibility: Quality value objects and validation
    Contains all enums, models, and utilities as nested classes.
    """

    @override
    def __init__(self, **data: object) -> None:
        """Initialize value objects service."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        # Store initialization data if provided
        self._init_data = data

    # =============================================================================
    # NESTED ENUMERATIONS - All quality-related enums
    # =============================================================================

    class IssueSeverity(StrEnum):
        """Issue severity levels using StrEnum."""

        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"
        INFO = "INFO"

    class IssueType(StrEnum):
        """Issue type enumeration using StrEnum."""

        # Code quality issues
        SYNTAX_ERROR = "syntax_error"
        STYLE_VIOLATION = "style_violation"
        NAMING_CONVENTION = "naming_convention"
        # Complexity issues
        HIGH_COMPLEXITY = "high_complexity"
        HIGH_COGNITIVE_COMPLEXITY = "high_cognitive_complexity"
        LONG_METHOD = "long_method"
        LONG_PARAMETER_LIST = "long_parameter_list"
        # Security issues
        SECURITY_VULNERABILITY = "security_vulnerability"
        HARDCODED_CREDENTIAL = "hardcoded_credential"
        SQL_INJECTION = "sql_injection"
        XSS_VULNERABILITY = "xss_vulnerability"
        # Dead code issues
        UNUSED_IMPORT = "unused_import"
        UNUSED_VARIABLE = "unused_variable"
        UNUSED_FUNCTION = "unused_function"
        UNREACHABLE_CODE = "unreachable_code"
        # Duplication issues
        DUPLICATE_CODE = "duplicate_code"
        SIMILAR_CODE = "similar_code"
        TYPE_ERROR = "type_error"
        MISSING_TYPE_ANNOTATION = "missing_type_annotation"
        # Documentation issues
        MISSING_DOCSTRING = "missing_docstring"
        INVALID_DOCSTRING = "invalid_docstring"

    class Grade(StrEnum):
        """Quality grade enumeration using StrEnum."""

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
        D_MINUS = "D-"
        F = "F"

    # =============================================================================
    # NESTED VALUE MODELS - All Pydantic models as nested classes
    # =============================================================================

    class Score(FlextModels):
        """Quality score value object with validation."""

        value: float = Field(
            ge=0.0,
            le=100.0,
            description="Quality score percentage",
        )
        grade: str = Field(description="Letter grade representation")
        category: str = Field(description="Score category")

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate business rules for quality score."""
            if (
                self.value < 0.0
                or self.value > FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE
            ):
                return FlextResult[None].fail("Quality score must be 0-100")

            # Validate grade matches score
            expected_grade = self._calculate_grade_from_score(self.value)
            if self.grade != expected_grade:
                return FlextResult[None].fail(
                    f"Grade {self.grade} does not match score {self.value}",
                )

            return FlextResult[None].ok(None)

        @staticmethod
        def _calculate_grade_from_score(score: float) -> str:
            """Calculate grade from score using GRADE_THRESHOLDS."""
            thresholds = FlextQualityValueObjects._GRADE_THRESHOLDS
            for threshold, grade in thresholds:
                if score >= threshold:
                    return grade.value
            return FlextQualityValueObjects.Grade.F.value

    class IssueLocation(FlextModels):
        """Issue location value object."""

        file_path: str = Field(description="File path where issue occurs")
        line_number: int = Field(ge=1, description="Line number (1-based)")
        column_number: int = Field(ge=0, description="Column number (0-based)")
        end_line: int | None = Field(
            default=None,
            ge=1,
            description="End line for multi-line issues",
        )
        end_column: int | None = Field(
            default=None,
            ge=0,
            description="End column for multi-line issues",
        )

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate business rules for issue location."""
            if self.end_line is not None and self.end_line < self.line_number:
                return FlextResult[None].fail("End line cannot be before start line")

            if (
                self.end_line == self.line_number
                and self.end_column is not None
                and self.end_column < self.column_number
            ):
                return FlextResult[None].fail(
                    "End column cannot be before start column on same line",
                )

            return FlextResult[None].ok(None)

    class ComplexityMetric(FlextModels):
        """Complexity metric value object."""

        cyclomatic: int = Field(ge=0, description="Cyclomatic complexity")
        cognitive: int = Field(ge=0, description="Cognitive complexity")
        nesting_depth: int = Field(ge=0, description="Maximum nesting depth")

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate complexity metric values."""
            if (
                self.cyclomatic
                > FlextQualityValueObjects.COMPLEXITY_CYCLOMATIC_HIGH * 5
            ):  # Reasonable upper bound
                return FlextResult[None].fail(
                    f"Cyclomatic complexity {self.cyclomatic} is extremely high",
                )

            if (
                self.cognitive > FlextQualityValueObjects.COMPLEXITY_COGNITIVE_HIGH * 5
            ):  # Reasonable upper bound
                return FlextResult[None].fail(
                    f"Cognitive complexity {self.cognitive} is extremely high",
                )

            return FlextResult[None].ok(None)

        def get_complexity_level(self) -> str:
            """Get complexity level based on thresholds."""
            if self.cyclomatic <= FlextQualityValueObjects.COMPLEXITY_SIMPLE_MAX:
                return "simple"
            if self.cyclomatic <= FlextQualityValueObjects.COMPLEXITY_MODERATE_MAX:
                return "moderate"
            return "complex"

    class CoverageMetric(FlextModels):
        """Coverage metric value object."""

        line_coverage: float = Field(
            ge=0.0,
            le=100.0,
            description="Line coverage percentage",
        )
        branch_coverage: float = Field(
            ge=0.0,
            le=100.0,
            description="Branch coverage percentage",
        )
        function_coverage: float = Field(
            ge=0.0,
            le=100.0,
            description="Function coverage percentage",
        )

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate coverage metrics."""
            # All validations handled by Field constraints
            return FlextResult[None].ok(None)

        def get_overall_coverage(self) -> float:
            """Calculate weighted overall coverage."""
            return (
                self.line_coverage * 0.5
                + self.branch_coverage * 0.3
                + self.function_coverage * 0.2
            )

    class DuplicationMetric(FlextModels):
        """Code duplication metric value object."""

        percentage: float = Field(
            ge=0.0,
            le=100.0,
            description="Duplication percentage",
        )
        lines_duplicated: int = Field(ge=0, description="Number of duplicated lines")
        files_with_duplicates: int = Field(
            ge=0,
            description="Number of files with duplicates",
        )

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate duplication metrics."""
            if self.lines_duplicated > 0 and self.files_with_duplicates == 0:
                return FlextResult[None].fail(
                    "Cannot have duplicated lines without files containing duplicates",
                )

            return FlextResult[None].ok(None)

    class FilePath(FlextModels):
        """File path value object with validation."""

        path: str = Field(description="File system path")

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate file path."""
            if len(self.path) > FlextQualityValueObjects.FILE_PATH_MAX_LENGTH:
                return FlextResult[None].fail(
                    f"Path exceeds maximum length {FlextQualityValueObjects.FILE_PATH_MAX_LENGTH}",
                )

            if not self.path.strip():
                return FlextResult[None].fail("Path cannot be empty")

            return FlextResult[None].ok(None)

        def as_path(self) -> Path:
            """Convert to pathlib.Path object."""
            return Path(self.path)

        @property
        def extension(self) -> str:
            """Get file extension."""
            path_obj = self.as_path()
            return path_obj.suffix

        @property
        def parent_dir(self) -> str:
            """Get parent directory."""
            path_obj = self.as_path()
            return str(path_obj.parent)

    # =============================================================================
    # CONSTANTS AND THRESHOLDS - Using FlextQualityConstants
    # =============================================================================

    # Quality score constants from FlextQualityConstants
    MIN_QUALITY_SCORE = FlextQualityConstants.Validation.MINIMUM_PERCENTAGE
    MAX_QUALITY_SCORE = FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE

    # Quality grade thresholds (score percentages)
    GRADE_A_PLUS = int(FlextQualityConstants.Thresholds.OUTSTANDING_THRESHOLD)
    GRADE_A = int(FlextQualityConstants.Thresholds.EXCELLENT_THRESHOLD)
    GRADE_A_MINUS = int(FlextQualityConstants.Thresholds.ENTERPRISE_READY_THRESHOLD)
    GRADE_B_PLUS = int(FlextQualityConstants.Thresholds.GOOD_THRESHOLD)
    GRADE_B = 75
    GRADE_B_MINUS = int(FlextQualityConstants.Thresholds.ACCEPTABLE_THRESHOLD)
    GRADE_C_PLUS = 65
    GRADE_C = int(FlextQualityConstants.Thresholds.BELOW_AVERAGE_THRESHOLD)
    GRADE_C_MINUS = 55
    GRADE_D_PLUS = 50
    GRADE_D = 45
    GRADE_D_MINUS = 40

    # Complexity thresholds from FlextQualityConstants
    COMPLEXITY_CYCLOMATIC_HIGH = FlextQualityConstants.Complexity.MAX_COMPLEXITY
    COMPLEXITY_COGNITIVE_HIGH = 15
    COMPLEXITY_DEPTH_HIGH = 4
    COMPLEXITY_SIMPLE_MAX = FlextQualityConstants.Complexity.IDEAL_COMPLEXITY
    COMPLEXITY_MODERATE_MAX = FlextQualityConstants.Complexity.WARNING_COMPLEXITY
    COMPLEXITY_COMPLEX_MAX = 20

    # Coverage and quality thresholds from FlextQualityConstants
    COVERAGE_EXCELLENT = FlextQualityConstants.Coverage.EXCELLENT_COVERAGE
    COVERAGE_PERCENTAGE_MAX = FlextQualityConstants.Coverage.MAXIMUM_COVERAGE
    DUPLICATION_LOW_MAX = FlextQualityConstants.Duplication.MAXIMUM_DUPLICATION

    # File system limits
    FILE_PATH_MAX_LENGTH = 4096

    # Grade mapping for efficient lookup
    _GRADE_THRESHOLDS: ClassVar[list[tuple[int, Grade]]] = [
        (GRADE_A_PLUS, Grade.A_PLUS),
        (GRADE_A, Grade.A),
        (GRADE_A_MINUS, Grade.A_MINUS),
        (GRADE_B_PLUS, Grade.B_PLUS),
        (GRADE_B, Grade.B),
        (GRADE_B_MINUS, Grade.B_MINUS),
        (GRADE_C_PLUS, Grade.C_PLUS),
        (GRADE_C, Grade.C),
        (GRADE_C_MINUS, Grade.C_MINUS),
        (GRADE_D_PLUS, Grade.D_PLUS),
        (GRADE_D, Grade.D),
        (GRADE_D_MINUS, Grade.D_MINUS),
    ]

    # =============================================================================
    # VALIDATION HELPER METHODS
    # =============================================================================

    class _ValidationHelper:
        """Nested validation helper class - no loose functions."""

        @staticmethod
        def validate_file_path(path: str | Path) -> FlextResult[Path]:
            """Validate and convert file path."""
            try:
                path_obj = Path(path)
                if len(str(path_obj)) > FlextQualityValueObjects.FILE_PATH_MAX_LENGTH:
                    return FlextResult[Path].fail("File path exceeds maximum length")
                return FlextResult[Path].ok(path_obj)
            except (ValueError, TypeError, OSError) as e:
                return FlextResult[Path].fail(f"Invalid file path: {e}")

        @staticmethod
        def validate_quality_score(score: float) -> FlextResult[float]:
            """Validate quality score is in valid range."""
            if (
                not FlextQualityValueObjects.MIN_QUALITY_SCORE
                <= score
                <= FlextQualityValueObjects.MAX_QUALITY_SCORE
            ):
                return FlextResult[float].fail(
                    f"Quality score must be between {FlextQualityValueObjects.MIN_QUALITY_SCORE} and {FlextQualityValueObjects.MAX_QUALITY_SCORE}",
                )
            return FlextResult[float].ok(score)

        @staticmethod
        def get_grade_from_score(score: float) -> FlextResult[str]:
            """Get quality grade from numeric score."""
            try:
                thresholds = FlextQualityValueObjects._GRADE_THRESHOLDS
                for threshold, grade in thresholds:
                    if score >= threshold:
                        return FlextResult[str].ok(grade.value)
                return FlextResult[str].ok(FlextQualityValueObjects.Grade.F.value)
            except Exception as e:
                return FlextResult[str].fail(f"Failed to calculate grade: {e}")

    # =============================================================================
    # PUBLIC API METHODS
    # =============================================================================

    def create_quality_score(
        self,
        percentage: float,
    ) -> FlextResult[FlextQualityValueObjects.Score]:
        """Create a validated quality score."""
        try:
            # Calculate grade using helper
            grade_result: FlextResult[str] = (
                self._ValidationHelper.get_grade_from_score(percentage)
            )
            if grade_result.is_failure:
                return FlextResult[FlextQualityValueObjects.Score].fail(
                    f"Failed to calculate grade: {grade_result.error}",
                )

            # Create instance using dict construction
            score_data = {
                "value": percentage,
                "grade": grade_result.value,
                "category": self._get_category_from_score(percentage),
            }
            instance = self.Score(**score_data)

            # Validate business rules
            validation_result: FlextResult[None] = instance.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextQualityValueObjects.Score].fail(
                    validation_result.error or "Validation failed",
                )

            return FlextResult[FlextQualityValueObjects.Score].ok(instance)
        except Exception as e:
            return FlextResult[FlextQualityValueObjects.Score].fail(
                f"Failed to create QualityScore: {e}",
            )

    def validate_file_path(self, path: str | Path) -> FlextResult[Path]:
        """Validate file path using helper."""
        return self._ValidationHelper.validate_file_path(path)

    def validate_quality_score(self, score: float) -> FlextResult[float]:
        """Validate quality score using helper."""
        return self._ValidationHelper.validate_quality_score(score)

    def get_grade_from_score(self, score: float) -> FlextResult[str]:
        """Get grade from score using helper."""
        return self._ValidationHelper.get_grade_from_score(score)

    def _get_category_from_score(self, score: float) -> str:
        """Get category from score."""
        if score >= self.COVERAGE_EXCELLENT:
            return "excellent"
        if score >= self.GRADE_B:
            return "good"
        if score >= self.GRADE_C:
            return "acceptable"
        return "poor"


# Backward compatibility aliases
FlextIssueSeverity = FlextQualityValueObjects.IssueSeverity
FlextIssueType = FlextQualityValueObjects.IssueType
FlextQualityGrade = FlextQualityValueObjects.Grade
IssueSeverity = FlextQualityValueObjects.IssueSeverity

# Export all classes
__all__ = [
    "FlextIssueSeverity",
    "FlextIssueType",
    "FlextQualityGrade",
    "FlextQualityValueObjects",
    "IssueSeverity",
]
