"""CONSOLIDATED Value Objects for FLEXT-QUALITY.

REFACTORED: Single CONSOLIDATED class following FLEXT_REFACTORING_PROMPT.md patterns.
Uses flext-core FlextValue - NO duplication, NO multiple separate classes.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from flext_core import FlextResult, FlextValue


class FlextQualityValueObjects:
    """CONSOLIDATED value objects class following FLEXT_REFACTORING_PROMPT.md pattern.

    Single class containing ALL value objects functionality to eliminate duplication
    and follow FLEXT ecosystem standards.
    """

    # CONSOLIDATED: Quality grade thresholds (score percentages)
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

    # CONSOLIDATED: Complexity thresholds
    COMPLEXITY_CYCLOMATIC_HIGH = 10
    COMPLEXITY_COGNITIVE_HIGH = 15
    COMPLEXITY_DEPTH_HIGH = 4
    COMPLEXITY_SIMPLE_MAX = 5
    COMPLEXITY_MODERATE_MAX = 10
    COMPLEXITY_COMPLEX_MAX = 20
    COMPLEXITY_CYCLOMATIC_MAX = 50

    # CONSOLIDATED: Coverage and quality thresholds
    COVERAGE_EXCELLENT = 95.0
    COVERAGE_PERCENTAGE_MAX = 100.0
    DUPLICATION_LOW_MAX = 5.0

    # CONSOLIDATED: File system limits
    FILE_PATH_MAX_LENGTH = 4096

    # CONSOLIDATED: Nested enum classes for related types
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

    # CONSOLIDATED: Value object methods for path validation
    @staticmethod
    def validate_file_path(path: str | Path) -> FlextResult[Path]:
        """Validate and convert file path."""
        try:
            path_obj = Path(path)
            if len(str(path_obj)) > FlextQualityValueObjects.FILE_PATH_MAX_LENGTH:
                return FlextResult[Path].fail("File path exceeds maximum length")
            return FlextResult[Path].ok(path_obj)
        except Exception as e:
            return FlextResult[Path].fail(f"Invalid file path: {e}")

    # CONSOLIDATED: Quality score validation
    @staticmethod
    def validate_quality_score(score: float) -> FlextResult[float]:
        """Validate quality score is in valid range."""
        if not 0.0 <= score <= FlextQualityValueObjects.COVERAGE_PERCENTAGE_MAX:
            return FlextResult[float].fail("Quality score must be between 0.0 and 100.0")
        return FlextResult[float].ok(score)

    # CONSOLIDATED: Grade calculation
    @classmethod
    def calculate_grade(cls, score: float) -> QualityGrade:  # noqa: PLR0911
        """Calculate quality grade from score."""
        if score >= cls.GRADE_A_PLUS:
            return cls.QualityGrade.A_PLUS
        if score >= cls.GRADE_A:
            return cls.QualityGrade.A
        if score >= cls.GRADE_A_MINUS:
            return cls.QualityGrade.A_MINUS
        if score >= cls.GRADE_B_PLUS:
            return cls.QualityGrade.B_PLUS
        if score >= cls.GRADE_B:
            return cls.QualityGrade.B
        if score >= cls.GRADE_B_MINUS:
            return cls.QualityGrade.B_MINUS
        if score >= cls.GRADE_C_PLUS:
            return cls.QualityGrade.C_PLUS
        if score >= cls.GRADE_C:
            return cls.QualityGrade.C
        if score >= cls.GRADE_C_MINUS:
            return cls.QualityGrade.C_MINUS
        if score >= cls.GRADE_D_PLUS:
            return cls.QualityGrade.D_PLUS
        if score >= cls.GRADE_D:
            return cls.QualityGrade.D
        if score >= cls.GRADE_D_MINUS:
            return cls.QualityGrade.D_MINUS
        return cls.QualityGrade.F


# Backward compatibility aliases - following flext-cli pattern
FlextQualityThresholds = FlextQualityValueObjects
FlextIssueSeverity = FlextQualityValueObjects.IssueSeverity
FlextIssueType = FlextQualityValueObjects.IssueType
FlextQualityGrade = FlextQualityValueObjects.QualityGrade

# Legacy compatibility
QualityGrade = FlextQualityValueObjects.QualityGrade

# For other complex value objects, use FlextValue as base but centralized methods
FlextFilePath = FlextValue
FlextIssueLocation = FlextValue
FlextQualityScore = FlextValue
FlextComplexityMetric = FlextValue
FlextCoverageMetric = FlextValue
FlextDuplicationMetric = FlextValue


# Export CONSOLIDATED class and aliases
__all__ = [
    "FlextComplexityMetric",
    "FlextCoverageMetric",
    "FlextDuplicationMetric",
    "FlextFilePath",
    "FlextIssueLocation",
    "FlextIssueSeverity",
    "FlextIssueType",
    "FlextQualityGrade",
    "FlextQualityScore",
    # Backward compatibility
    "FlextQualityThresholds",
    "FlextQualityValueObjects",
    # Legacy compatibility
    "QualityGrade",
]
