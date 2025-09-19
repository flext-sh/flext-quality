"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field

from flext_core import FlextContainer, FlextLogger, FlextModels, FlextResult

# Quality Score Constants
MIN_QUALITY_SCORE = 0.0
MAX_QUALITY_SCORE = 100.0

# Quality Grade Thresholds
GRADE_A_PLUS_THRESHOLD = 95
GRADE_A_THRESHOLD = 90
GRADE_A_MINUS_THRESHOLD = 85
GRADE_B_PLUS_THRESHOLD = 80
GRADE_B_THRESHOLD = 75
GRADE_B_MINUS_THRESHOLD = 70
GRADE_C_PLUS_THRESHOLD = 65
GRADE_C_THRESHOLD = 60
GRADE_C_MINUS_THRESHOLD = 55
GRADE_D_PLUS_THRESHOLD = 50
GRADE_D_THRESHOLD = 45
GRADE_D_MINUS_THRESHOLD = 40


# Coverage Constants
MIN_COVERAGE_REQUIREMENT = 90.0

# Duplication Constants
MAX_DUPLICATION_THRESHOLD = 5.0

# File Path Constants
MAX_PATH_LENGTH = 4096

# Complexity Thresholds
CYCLOMATIC_HIGH_THRESHOLD = 10
COGNITIVE_HIGH_THRESHOLD = 15
MAX_DEPTH_THRESHOLD = 4
COMPLEXITY_SIMPLE_MAX = 5
COMPLEXITY_MODERATE_MAX = 10
COMPLEXITY_COMPLEX_MAX = 20

# Quality Category Thresholds
EXCELLENT_QUALITY_THRESHOLD = 90.0
GOOD_QUALITY_THRESHOLD = 70.0


class IssueSeverity(StrEnum):
    """Issue severity levels using StrEnum."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


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


class QualityGrade(StrEnum):
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


# Grade mapping for efficient lookup (defined after QualityGrade class)
GRADE_THRESHOLDS = [
    (GRADE_A_PLUS_THRESHOLD, QualityGrade.A_PLUS),
    (GRADE_A_THRESHOLD, QualityGrade.A),
    (GRADE_A_MINUS_THRESHOLD, QualityGrade.A_MINUS),
    (GRADE_B_PLUS_THRESHOLD, QualityGrade.B_PLUS),
    (GRADE_B_THRESHOLD, QualityGrade.B),
    (GRADE_B_MINUS_THRESHOLD, QualityGrade.B_MINUS),
    (GRADE_C_PLUS_THRESHOLD, QualityGrade.C_PLUS),
    (GRADE_C_THRESHOLD, QualityGrade.C),
    (GRADE_C_MINUS_THRESHOLD, QualityGrade.C_MINUS),
    (GRADE_D_PLUS_THRESHOLD, QualityGrade.D_PLUS),
    (GRADE_D_THRESHOLD, QualityGrade.D),
    (GRADE_D_MINUS_THRESHOLD, QualityGrade.D_MINUS),
]


class QualityScore(FlextModels):
    """Quality score value object with validation and grade calculation."""

    value: float = Field(
        ...,
        ge=MIN_QUALITY_SCORE,
        le=MAX_QUALITY_SCORE,
        description="Quality score percentage",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules for quality score."""
        if not MIN_QUALITY_SCORE <= self.value <= MAX_QUALITY_SCORE:
            return FlextResult[None].fail(
                f"Quality score must be between {MIN_QUALITY_SCORE} and {MAX_QUALITY_SCORE}",
            )
        return FlextResult[None].ok(None)

    @property
    def percentage(self) -> str:
        """Format score as percentage string."""
        return f"{self.value:.1f}%"

    @property
    def grade(self) -> QualityGrade:
        """Calculate quality grade from score using efficient lookup."""
        for threshold, grade in GRADE_THRESHOLDS:
            if self.value >= threshold:
                return grade
        return QualityGrade.F


class IssueLocation(FlextModels):
    """Represents location of an issue in source code."""

    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(default=1, ge=1, description="Column number")
    end_line: int | None = Field(default=None, ge=1, description="End line number")
    end_column: int | None = Field(default=None, ge=1, description="End column number")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate issue location business rules."""
        if self.end_line is not None and self.end_line < self.line:
            return FlextResult[None].fail("End line must be >= start line")
        return FlextResult[None].ok(None)

    @property
    def range_text(self) -> str:
        """Human-readable range description."""
        if self.end_line is None:
            return f"line {self.line}, column {self.column}"
        if self.end_line == self.line:
            if self.end_column is None:
                return f"line {self.line}, columns {self.column}-end"
            return f"line {self.line}, columns {self.column}-{self.end_column}"
        return f"lines {self.line}-{self.end_line}"


class ComplexityMetric(FlextModels):
    """Complexity metrics for code analysis."""

    cyclomatic: int = Field(default=1, ge=1, description="Cyclomatic complexity")
    cognitive: int = Field(default=0, ge=0, description="Cognitive complexity")
    max_depth: int = Field(default=0, ge=0, description="Maximum nesting depth")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate complexity metrics business rules."""
        if self.cyclomatic < 1:
            return FlextResult[None].fail("Cyclomatic complexity must be >= 1")
        return FlextResult[None].ok(None)

    @property
    def is_complex(self) -> bool:
        """Check if complexity is too high."""
        return (
            self.cyclomatic > CYCLOMATIC_HIGH_THRESHOLD
            or self.cognitive > COGNITIVE_HIGH_THRESHOLD
            or self.max_depth > MAX_DEPTH_THRESHOLD
        )

    @property
    def complexity_level(self) -> str:
        """Get complexity level description."""
        if self.cyclomatic <= COMPLEXITY_SIMPLE_MAX:
            return "simple"
        if self.cyclomatic <= COMPLEXITY_MODERATE_MAX:
            return "moderate"
        if self.cyclomatic <= COMPLEXITY_COMPLEX_MAX:
            return "complex"
        return "very complex"


class CoverageMetric(FlextModels):
    """Code coverage metrics with weighted calculations."""

    line_coverage: float = Field(
        default=MIN_QUALITY_SCORE,
        ge=MIN_QUALITY_SCORE,
        le=MAX_QUALITY_SCORE,
        description="Line coverage %",
    )
    branch_coverage: float = Field(
        default=MIN_QUALITY_SCORE,
        ge=MIN_QUALITY_SCORE,
        le=MAX_QUALITY_SCORE,
        description="Branch coverage %",
    )
    function_coverage: float = Field(
        default=MIN_QUALITY_SCORE,
        ge=MIN_QUALITY_SCORE,
        le=MAX_QUALITY_SCORE,
        description="Function coverage %",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate coverage metrics business rules."""
        for field_name in ["line_coverage", "branch_coverage", "function_coverage"]:
            value = getattr(self, field_name)
            if not MIN_QUALITY_SCORE <= value <= MAX_QUALITY_SCORE:
                return FlextResult[None].fail(
                    f"{field_name} must be between {MIN_QUALITY_SCORE} and {MAX_QUALITY_SCORE}",
                )
        return FlextResult[None].ok(None)

    @property
    def overall_coverage(self) -> float:
        """Calculate weighted overall coverage."""
        # Weighted average: line 50%, branch 30%, function 20%
        return (
            self.line_coverage * 0.5
            + self.branch_coverage * 0.3
            + self.function_coverage * 0.2
        )

    @property
    def is_sufficient(self) -> bool:
        """Check if coverage meets minimum requirements."""
        return self.overall_coverage >= MIN_COVERAGE_REQUIREMENT


class DuplicationMetric(FlextModels):
    """Code duplication metrics."""

    duplicate_lines: int = Field(
        default=0, ge=0, description="Number of duplicate lines",
    )
    total_lines: int = Field(default=0, ge=0, description="Total lines of code")
    duplicate_blocks: int = Field(
        default=0, ge=0, description="Number of duplicate blocks",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate duplication metrics business rules."""
        if (
            self.duplicate_lines < 0
            or self.total_lines < 0
            or self.duplicate_blocks < 0
        ):
            return FlextResult[None].fail("All metrics must be >= 0")
        return FlextResult[None].ok(None)

    @property
    def duplication_percentage(self) -> float:
        """Calculate duplication percentage."""
        if self.total_lines == 0:
            return 0.0
        return (self.duplicate_lines / self.total_lines) * MAX_QUALITY_SCORE

    @property
    def is_acceptable(self) -> bool:
        """Check if duplication is within acceptable limits."""
        return self.duplication_percentage < MAX_DUPLICATION_THRESHOLD


class FilePath(FlextModels):
    """File path value object with validation."""

    value: str = Field(
        ..., min_length=1, max_length=MAX_PATH_LENGTH, description="File path string",
    )
    is_absolute: bool = Field(default=False, description="Whether path is absolute")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate file path business rules."""
        try:
            path_obj = Path(self.value)
            if len(str(path_obj)) > MAX_PATH_LENGTH:
                return FlextResult[None].fail("File path exceeds maximum length")
            return FlextResult[None].ok(None)
        except (ValueError, TypeError, OSError) as e:
            return FlextResult[None].fail(f"Invalid file path: {e}")

    @property
    def path(self) -> Path:
        """Get Path object."""
        return Path(self.value)

    @property
    def filename(self) -> str:
        """Get filename."""
        return self.path.name

    @property
    def extension(self) -> str:
        """Get file extension."""
        return self.path.suffix

    @property
    def parent_dir(self) -> str:
        """Get parent directory."""
        return str(self.path.parent)


class FlextQualityValueObjects:
    """Unified value objects class following FLEXT pattern - ZERO DUPLICATION.

    Single responsibility: Quality value objects and validation
    Contains all enums, models, and utilities as nested classes.
    """

    def __init__(self, **data: object) -> None:
        """Initialize value objects service."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        # Store initialization data if provided
        self._init_data = data

    # =============================================================================
    # NESTED ENUMERATIONS - All quality-related enums
    # =============================================================================

    class IssueSeverity(StrEnum):
        """Issue severity levels using StrEnum."""

        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

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

    class QualityGrade(StrEnum):
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

    class QualityScore(FlextModels):
        """Quality score value object with validation."""

        value: float = Field(
            ge=MIN_QUALITY_SCORE,
            le=MAX_QUALITY_SCORE,
            description="Quality score percentage",
        )
        grade: str = Field(description="Letter grade representation")
        category: str = Field(description="Score category")

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate business rules for quality score."""
            if self.value < MIN_QUALITY_SCORE or self.value > MAX_QUALITY_SCORE:
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
            for threshold, grade in GRADE_THRESHOLDS:
                if score >= threshold:
                    return grade
            return FlextQualityValueObjects.QualityGrade.F

    class IssueLocation(FlextModels):
        """Issue location value object."""

        file_path: str = Field(description="File path where issue occurs")
        line_number: int = Field(ge=1, description="Line number (1-based)")
        column_number: int = Field(ge=0, description="Column number (0-based)")
        end_line: int | None = Field(
            default=None, ge=1, description="End line for multi-line issues",
        )
        end_column: int | None = Field(
            default=None, ge=0, description="End column for multi-line issues",
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
                self.cyclomatic > CYCLOMATIC_HIGH_THRESHOLD * 5
            ):  # Reasonable upper bound
                return FlextResult[None].fail(
                    f"Cyclomatic complexity {self.cyclomatic} is extremely high",
                )

            if self.cognitive > COGNITIVE_HIGH_THRESHOLD * 5:  # Reasonable upper bound
                return FlextResult[None].fail(
                    f"Cognitive complexity {self.cognitive} is extremely high",
                )

            return FlextResult[None].ok(None)

        def get_complexity_level(self) -> str:
            """Get complexity level based on thresholds."""
            if self.cyclomatic <= COMPLEXITY_SIMPLE_MAX:
                return "simple"
            if self.cyclomatic <= COMPLEXITY_MODERATE_MAX:
                return "moderate"
            return "complex"

    class CoverageMetric(FlextModels):
        """Coverage metric value object."""

        line_coverage: float = Field(
            ge=0.0, le=100.0, description="Line coverage percentage",
        )
        branch_coverage: float = Field(
            ge=0.0, le=100.0, description="Branch coverage percentage",
        )
        function_coverage: float = Field(
            ge=0.0, le=100.0, description="Function coverage percentage",
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
            ge=0.0, le=100.0, description="Duplication percentage",
        )
        lines_duplicated: int = Field(ge=0, description="Number of duplicated lines")
        files_with_duplicates: int = Field(
            ge=0, description="Number of files with duplicates",
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
            if len(self.path) > MAX_PATH_LENGTH:
                return FlextResult[None].fail(
                    f"Path exceeds maximum length {MAX_PATH_LENGTH}",
                )

            if not self.path.strip():
                return FlextResult[None].fail("Path cannot be empty")

            return FlextResult[None].ok(None)

        def as_path(self) -> Path:
            """Convert to pathlib.Path object."""
            return Path(self.path)

    # =============================================================================
    # CONSTANTS AND THRESHOLDS
    # =============================================================================

    # Quality grade thresholds (score percentages)
    GRADE_A_PLUS = 95
    GRADE_A = 90
    GRADE_A_MINUS = 85
    GRADE_B_PLUS = 80
    GRADE_B = 75
    GRADE_B_MINUS = 70
    GRADE_C_PLUS = 65
    GRADE_C = 60
    GRADE_C_MINUS = 55
    GRADE_D_PLUS = 50
    GRADE_D = 45
    GRADE_D_MINUS = 40

    # Complexity thresholds
    COMPLEXITY_CYCLOMATIC_HIGH = 10
    COMPLEXITY_COGNITIVE_HIGH = 15
    COMPLEXITY_DEPTH_HIGH = 4
    COMPLEXITY_SIMPLE_MAX = 5
    COMPLEXITY_MODERATE_MAX = 10
    COMPLEXITY_COMPLEX_MAX = 20

    # Coverage and quality thresholds
    COVERAGE_EXCELLENT = 95.0
    COVERAGE_PERCENTAGE_MAX = 100.0
    DUPLICATION_LOW_MAX = 5.0

    # File system limits
    FILE_PATH_MAX_LENGTH = 4096

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
            if not MIN_QUALITY_SCORE <= score <= MAX_QUALITY_SCORE:
                return FlextResult[float].fail(
                    f"Quality score must be between {MIN_QUALITY_SCORE} and {MAX_QUALITY_SCORE}",
                )
            return FlextResult[float].ok(score)

        @staticmethod
        def get_grade_from_score(score: float) -> FlextResult[str]:
            """Get quality grade from numeric score."""
            try:
                for threshold, grade in GRADE_THRESHOLDS:
                    if score >= threshold:
                        return FlextResult[str].ok(grade)
                return FlextResult[str].ok(FlextQualityValueObjects.QualityGrade.F)
            except Exception as e:
                return FlextResult[str].fail(f"Failed to calculate grade: {e}")

    # =============================================================================
    # PUBLIC API METHODS
    # =============================================================================

    def create_quality_score(
        self, percentage: float,
    ) -> FlextResult[FlextQualityValueObjects.QualityScore]:
        """Create a validated quality score."""
        try:
            # Calculate grade using helper
            grade_result = self._ValidationHelper.get_grade_from_score(percentage)
            if grade_result.is_failure:
                return FlextResult[FlextQualityValueObjects.QualityScore].fail(
                    f"Failed to calculate grade: {grade_result.error}",
                )

            grade = grade_result.value
            category = (
                "excellent"
                if percentage >= EXCELLENT_QUALITY_THRESHOLD
                else "good"
                if percentage >= GOOD_QUALITY_THRESHOLD
                else "needs_improvement"
            )

            # Create instance using dict construction
            score_data = {"value": percentage, "grade": grade, "category": category}
            instance = self.QualityScore(**score_data)

            # Validate business rules
            validation_result = instance.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextQualityValueObjects.QualityScore].fail(
                    validation_result.error or "Validation failed",
                )

            return FlextResult[FlextQualityValueObjects.QualityScore].ok(instance)
        except Exception as e:
            return FlextResult[FlextQualityValueObjects.QualityScore].fail(
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


# Backward compatibility aliases
FlextQualityThresholds = FlextQualityValueObjects
FlextIssueSeverity = IssueSeverity
FlextIssueType = IssueType
FlextQualityGrade = QualityGrade
FlextFilePath = FilePath
FlextIssueLocation = IssueLocation
FlextQualityScore = QualityScore
FlextComplexityMetric = ComplexityMetric
FlextCoverageMetric = CoverageMetric
FlextDuplicationMetric = DuplicationMetric


# Export all classes
__all__ = [
    # Independent classes (FLEXT pattern)
    "ComplexityMetric",
    "CoverageMetric",
    "DuplicationMetric",
    "FilePath",
    # Backward compatibility aliases
    "FlextComplexityMetric",
    "FlextCoverageMetric",
    "FlextDuplicationMetric",
    "FlextFilePath",
    "FlextIssueLocation",
    "FlextIssueSeverity",
    "FlextIssueType",
    "FlextQualityGrade",
    "FlextQualityScore",
    "FlextQualityThresholds",
    # Consolidated namespace
    "FlextQualityValueObjects",
    "IssueLocation",
    "IssueSeverity",
    "IssueType",
    "QualityGrade",
    "QualityScore",
]
