"""Value objects for FLEXT-QUALITY.

REFACTORED:
            Uses flext-core FlextValueObject - NO duplication.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field, field_validator

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_quality.infrastructure.di_container import get_domain_entity

DomainEntity = get_domain_entity()
DomainEvent = get_domain_entity()  # Placeholder
FlextDomainBaseModel = get_domain_entity()  # Placeholder


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
    HARDCODED_SECRET = "hardcoded_secret"  # nosec: B105 # This is an issue type constant, not a password
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


class FilePath(FlextDomainBaseModel):
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


class IssueLocation(FlextDomainBaseModel):
    """Location of an issue in a file."""

    line: int = Field(..., description="Line number", ge=1)
    column: int = Field(default=1, description="Column number", ge=1)
    end_line: int | None = Field(None, description="End line number", ge=1)
    end_column: int | None = Field(None, description="End column number", ge=1)

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


class QualityScore(FlextDomainBaseModel):
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
    def grade(self) -> QualityGrade:
        """Get quality grade based on score.

        Returns:
            Quality grade enum value.

        """
        if self.value >= 95:
            return QualityGrade.A_PLUS
        if self.value >= 90:
            return QualityGrade.A
        if self.value >= 85:
            return QualityGrade.A_MINUS
        if self.value >= 80:
            return QualityGrade.B_PLUS
        if self.value >= 75:
            return QualityGrade.B
        if self.value >= 70:
            return QualityGrade.B_MINUS
        if self.value >= 65:
            return QualityGrade.C_PLUS
        if self.value >= 60:
            return QualityGrade.C
        if self.value >= 55:
            return QualityGrade.C_MINUS
        if self.value >= 50:
            return QualityGrade.D_PLUS
        if self.value >= 45:
            return QualityGrade.D
        if self.value >= 40:
            return QualityGrade.D_MINUS
        return QualityGrade.F


class ComplexityMetric(FlextDomainBaseModel):
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
        return self.cyclomatic > 10 or self.cognitive > 15 or self.max_depth > 4

    @property
    def complexity_level(self) -> str:
        """Get complexity level description.

        Returns:
            Complexity level as string.

        """
        if self.cyclomatic <= 5:
            return "simple"
        if self.cyclomatic <= 10:
            return "moderate"
        if self.cyclomatic <= 20:
            return "complex"
        return "very complex"


class CoverageMetric(FlextDomainBaseModel):
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
        return self.overall_coverage >= 95.0


class DuplicationMetric(FlextDomainBaseModel):
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
        return self.duplication_percentage < 5.0
