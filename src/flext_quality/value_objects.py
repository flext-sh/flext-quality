"""Value objects for FLEXT-QUALITY.

REFACTORED:
          Uses flext-core FlextValue - NO duplication.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import override

from flext_core import FlextResult, FlextValue
from pydantic import Field, field_validator

# Using flext-core patterns consistently


class FlextQualityThresholds:
    """Business rule constants for quality assessment - extracted magic numbers."""

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
    COMPLEXITY_CYCLOMATIC_MAX = 50

    # Coverage and quality thresholds
    COVERAGE_EXCELLENT = 95.0
    COVERAGE_PERCENTAGE_MAX = 100.0
    DUPLICATION_LOW_MAX = 5.0

    # File system limits
    FILE_PATH_MAX_LENGTH = 4096


class FlextIssueSeverity(StrEnum):
    """Issue severity levels using StrEnum."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FlextIssueType(StrEnum):
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

    # Type issues
    TYPE_ERROR = "type_error"
    MISSING_TYPE_ANNOTATION = "missing_type_annotation"

    # Documentation issues
    MISSING_DOCSTRING = "missing_docstring"
    INVALID_DOCSTRING = "invalid_docstring"


class FlextQualityGrade(StrEnum):
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


class FlextFilePath(FlextValue):
    """File path value object."""

    value: str = Field(..., description="File path")
    is_absolute: bool = Field(default=False, description="Whether path is absolute")

    @field_validator("value")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate file path.

        Args:
            v: Path string to validate.

        Returns:
            Normalized path string.

        Raises:
            ValueError: If path is empty.

        """
        if not v:
            msg = "File path cannot be empty"
            raise ValueError(msg)
        return str(Path(v).as_posix())  # Normalize path

    @property
    def path(self) -> Path:
        """Get Path object from string value.

        Returns:
            Path object.

        """
        return Path(self.value)

    @property
    def filename(self) -> str:
        """Get filename from path.

        Returns:
            Filename string.

        """
        return self.path.name

    @property
    def extension(self) -> str:
        """Get file extension from path.

        Returns:
            File extension string.

        """
        return self.path.suffix

    @property
    def parent_dir(self) -> str:
        """Get parent directory from path.

        Returns:
            Parent directory string.

        """
        return str(self.path.parent)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate file path business rules."""
        if not self.value:
            return FlextResult[None].fail("File path cannot be empty")
        if len(self.value) > FlextQualityThresholds.FILE_PATH_MAX_LENGTH:
            return FlextResult[None].fail(
                f"File path too long (>{FlextQualityThresholds.FILE_PATH_MAX_LENGTH} characters)"
            )

        return FlextResult[None].ok(None)


class FlextIssueLocation(FlextValue):
    """Location of an issue in a file."""

    line: int = Field(..., description="Line number", ge=1)
    column: int = Field(default=1, description="Column number", ge=1)
    end_line: int | None = Field(default=None, description="End line number", ge=1)
    end_column: int | None = Field(default=None, description="End column number", ge=1)

    @field_validator("end_line", mode="before")
    @classmethod
    def validate_end_line(cls, v: int | None) -> int | None:
        """Validate end line is valid.

        Args:
            v: End line number to validate.

        Returns:
            Validated end line number.

        """
        # Simple validation - must be positive if provided
        if v is not None and v < 1:
            msg = "End line number must be positive"
            raise ValueError(msg)
        return v

    @property
    def range_text(self) -> str:
        """Get human-readable text representation of location range.

        Returns:
            Formatted range text.

        """
        if self.end_line is None:
            return f"line {self.line}, column {self.column}"
        if self.line == self.end_line:
            return f"line {self.line}, columns {self.column}-{self.end_column or 'end'}"
        return f"lines {self.line}-{self.end_line}"

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate issue location business rules."""
        if self.line < 1:
            return FlextResult[None].fail("Line number must be positive")
        if self.column < 1:
            return FlextResult[None].fail("Column number must be positive")
        if self.end_line is not None and self.end_line < self.line:
            return FlextResult[None].fail("End line cannot be before start line")
        if self.end_column is not None and self.end_column < 1:
            return FlextResult[None].fail("End column must be positive")

        return FlextResult[None].ok(None)


class FlextQualityScore(FlextValue):
    """Quality score value object."""

    value: float = Field(..., description="Quality score", ge=0.0, le=100.0)

    @property
    def percentage(self) -> str:
        """Get quality score as percentage string.

        Returns:
            Formatted percentage string.

        """
        return f"{self.value:.1f}%"

    @property
    def grade(self) -> FlextQualityGrade:  # noqa: PLR0911  # Grade calculation legitimately needs many returns
        """Get quality grade based on score.

        Returns:
            Quality grade enum value.

        """
        if self.value >= FlextQualityThresholds.GRADE_A_PLUS:
            return FlextQualityGrade.A_PLUS
        if self.value >= FlextQualityThresholds.GRADE_A:
            return FlextQualityGrade.A
        if self.value >= FlextQualityThresholds.GRADE_A_MINUS:
            return FlextQualityGrade.A_MINUS
        if self.value >= FlextQualityThresholds.GRADE_B_PLUS:
            return FlextQualityGrade.B_PLUS
        if self.value >= FlextQualityThresholds.GRADE_B:
            return FlextQualityGrade.B
        if self.value >= FlextQualityThresholds.GRADE_B_MINUS:
            return FlextQualityGrade.B_MINUS
        if self.value >= FlextQualityThresholds.GRADE_C_PLUS:
            return FlextQualityGrade.C_PLUS
        if self.value >= FlextQualityThresholds.GRADE_C:
            return FlextQualityGrade.C
        if self.value >= FlextQualityThresholds.GRADE_C_MINUS:
            return FlextQualityGrade.C_MINUS
        if self.value >= FlextQualityThresholds.GRADE_D_PLUS:
            return FlextQualityGrade.D_PLUS
        if self.value >= FlextQualityThresholds.GRADE_D:
            return FlextQualityGrade.D
        if self.value >= FlextQualityThresholds.GRADE_D_MINUS:
            return FlextQualityGrade.D_MINUS
        return FlextQualityGrade.F

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate quality score business rules."""
        if self.value < 0.0 or self.value > FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX:
            return FlextResult[None].fail(
                f"Quality score must be between 0.0 and {FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX}"
            )

        return FlextResult[None].ok(None)


class FlextComplexityMetric(FlextValue):
    """Complexity metric value object."""

    cyclomatic: int = Field(default=1, description="Cyclomatic complexity", ge=1)
    cognitive: int = Field(default=0, description="Cognitive complexity", ge=0)
    max_depth: int = Field(default=0, description="Maximum nesting depth", ge=0)

    @property
    def is_complex(self) -> bool:
        """Check if complexity metrics indicate complex code.

        Returns:
            True if code is considered complex.

        """
        return (
            self.cyclomatic > FlextQualityThresholds.COMPLEXITY_CYCLOMATIC_HIGH
            or self.cognitive > FlextQualityThresholds.COMPLEXITY_COGNITIVE_HIGH
            or self.max_depth > FlextQualityThresholds.COMPLEXITY_DEPTH_HIGH
        )

    @property
    def complexity_level(self) -> str:
        """Get complexity level description.

        Returns:
            Complexity level as string.

        """
        if self.cyclomatic <= FlextQualityThresholds.COMPLEXITY_SIMPLE_MAX:
            return "simple"
        if self.cyclomatic <= FlextQualityThresholds.COMPLEXITY_MODERATE_MAX:
            return "moderate"
        if self.cyclomatic <= FlextQualityThresholds.COMPLEXITY_COMPLEX_MAX:
            return "complex"
        return "very complex"

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate complexity metric business rules."""
        if self.cyclomatic < 1:
            return FlextResult[None].fail("Cyclomatic complexity must be at least 1")
        if self.cognitive < 0:
            return FlextResult[None].fail("Cognitive complexity cannot be negative")
        if self.max_depth < 0:
            return FlextResult[None].fail("Max depth cannot be negative")
        if self.cyclomatic > FlextQualityThresholds.COMPLEXITY_CYCLOMATIC_MAX:
            return FlextResult[None].fail(
                f"Cyclomatic complexity too high (>{FlextQualityThresholds.COMPLEXITY_CYCLOMATIC_MAX})"
            )

        return FlextResult[None].ok(None)


class FlextCoverageMetric(FlextValue):
    """Test coverage metric value object."""

    line_coverage: float = Field(
        default=0.0,
        description="Line coverage percentage",
        ge=0.0,
        le=100.0,
    )
    branch_coverage: float = Field(
        default=0.0,
        description="Branch coverage percentage",
        ge=0.0,
        le=100.0,
    )
    function_coverage: float = Field(
        default=0.0,
        description="Function coverage percentage",
        ge=0.0,
        le=100.0,
    )

    @property
    def overall_coverage(self) -> float:
        """Calculate weighted overall coverage percentage.

        Returns:
            Overall coverage percentage.

        """
        # Weight: 50% line, 30% branch, 20% function
        return (
            self.line_coverage * 0.5
            + self.branch_coverage * 0.3
            + self.function_coverage * 0.2
        )

    @property
    def is_sufficient(self) -> bool:
        """Check if coverage meets minimum requirements.

        Returns:
            True if coverage is sufficient.

        """
        return self.overall_coverage >= FlextQualityThresholds.COVERAGE_EXCELLENT

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate coverage metric business rules."""
        # Pydantic validators handle range validation (0-100),
        # so we only need business logic validation here
        if (
            self.line_coverage > FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX
            or self.line_coverage < 0.0
        ):
            return FlextResult[None].fail(
                f"Line coverage must be between 0% and {FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX}%"
            )
        if (
            self.branch_coverage > FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX
            or self.branch_coverage < 0.0
        ):
            return FlextResult[None].fail(
                f"Branch coverage must be between 0% and {FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX}%"
            )
        if (
            self.function_coverage > FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX
            or self.function_coverage < 0.0
        ):
            return FlextResult[None].fail(
                f"Function coverage must be between 0% and {FlextQualityThresholds.COVERAGE_PERCENTAGE_MAX}%"
            )

        return FlextResult[None].ok(None)


class FlextDuplicationMetric(FlextValue):
    """Code duplication metric value object."""

    duplicate_lines: int = Field(
        default=0,
        description="Number of duplicate lines",
        ge=0,
    )
    total_lines: int = Field(
        default=0,
        description="Total lines of code",
        ge=0,
    )
    duplicate_blocks: int = Field(
        default=0,
        description="Number of duplicate blocks",
        ge=0,
    )

    @property
    def duplication_percentage(self) -> float:
        """Calculate duplication percentage.

        Returns:
            Duplication percentage.

        """
        if self.total_lines == 0:
            return 0.0
        return (self.duplicate_lines / self.total_lines) * 100

    @property
    def is_acceptable(self) -> bool:
        """Check if duplication level is acceptable.

        Returns:
            True if duplication is below threshold.

        """
        return self.duplication_percentage < FlextQualityThresholds.DUPLICATION_LOW_MAX

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate duplication metric business rules."""
        if self.duplicate_lines < 0:
            return FlextResult[None].fail("Duplicate lines cannot be negative")
        if self.total_lines < 0:
            return FlextResult[None].fail("Total lines cannot be negative")
        if self.duplicate_blocks < 0:
            return FlextResult[None].fail("Duplicate blocks cannot be negative")
        if self.duplicate_lines > self.total_lines:
            return FlextResult[None].fail("Duplicate lines cannot exceed total lines")

        return FlextResult[None].ok(None)
