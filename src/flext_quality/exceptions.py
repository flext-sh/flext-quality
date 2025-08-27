"""Quality Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides quality-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextExceptionsMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in quality operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextExceptions


class FlextQualityErrorCodes(Enum):
    """Error codes for quality domain operations."""

    QUALITY_ERROR = "QUALITY_ERROR"
    QUALITY_VALIDATION_ERROR = "QUALITY_VALIDATION_ERROR"
    QUALITY_CONFIGURATION_ERROR = "QUALITY_CONFIGURATION_ERROR"
    QUALITY_CONNECTION_ERROR = "QUALITY_CONNECTION_ERROR"
    QUALITY_PROCESSING_ERROR = "QUALITY_PROCESSING_ERROR"
    QUALITY_AUTHENTICATION_ERROR = "QUALITY_AUTHENTICATION_ERROR"
    QUALITY_TIMEOUT_ERROR = "QUALITY_TIMEOUT_ERROR"
    QUALITY_ANALYSIS_ERROR = "QUALITY_ANALYSIS_ERROR"
    QUALITY_REPORT_ERROR = "QUALITY_REPORT_ERROR"
    QUALITY_METRICS_ERROR = "QUALITY_METRICS_ERROR"
    QUALITY_GRADE_ERROR = "QUALITY_GRADE_ERROR"
    QUALITY_RULE_ERROR = "QUALITY_RULE_ERROR"
    QUALITY_ISSUE_ERROR = "QUALITY_ISSUE_ERROR"
    QUALITY_THRESHOLD_ERROR = "QUALITY_THRESHOLD_ERROR"


# CONSOLIDATED Exception Class following FLEXT_REFACTORING_PROMPT.md pattern
class FlextQualityExceptionsError(FlextExceptions):
    """Single consolidated class containing ALL quality exceptions.

    Consolidates ALL exception definitions into one class following FLEXT patterns.
    Individual exceptions available as nested classes for organization.
    """

    class QualityError(FlextExceptions):
        """Base exception for all quality domain errors."""

    class ValidationError(QualityError):
        """Quality validation errors."""

    class ConfigurationError(QualityError):
        """Quality configuration errors."""

    class QualityConnectionError(QualityError):
        """Quality connection errors."""

    class ProcessingError(QualityError):
        """Quality processing errors."""

    class AuthenticationError(QualityError):
        """Quality authentication errors."""

    class QualityTimeoutError(QualityError):
        """Quality timeout errors."""

    class AnalysisError(QualityError):
        """Quality analysis errors."""

        def __init__(
            self,
            message: str = "Quality analysis error",
            *,
            error_code: str = "QUALITY_ANALYSIS_ERROR",
            context: dict[str, object] | None = None,
        ) -> None:
            super().__init__(message, error_code=error_code, context=context)

        @override
        def __str__(self) -> str:
            return f"Quality analysis: {self.message}"

    class ReportError(QualityError):
        """Quality report errors."""

        def __init__(
            self,
            message: str = "Quality report error",
            *,
            error_code: str = "QUALITY_REPORT_ERROR",
            context: dict[str, object] | None = None,
        ) -> None:
            super().__init__(message, error_code=error_code, context=context)

        @override
        def __str__(self) -> str:
            return f"Quality report: {self.message}"

    class MetricsError(QualityError):
        """Quality metrics errors."""

        def __init__(
            self,
            message: str = "Quality metrics error",
            *,
            error_code: str = "QUALITY_METRICS_ERROR",
            context: dict[str, object] | None = None,
        ) -> None:
            super().__init__(message, error_code=error_code, context=context)

        @override
        def __str__(self) -> str:
            return f"Quality metrics: {self.message}"

    class GradeError(QualityError):
        """Quality grade errors."""

        def __init__(
            self,
            message: str = "Quality grade error",
            *,
            error_code: str = "QUALITY_GRADE_ERROR",
            context: dict[str, object] | None = None,
        ) -> None:
            super().__init__(message, error_code=error_code, context=context)

        @override
        def __str__(self) -> str:
            return f"Quality grade: {self.message}"

    class RuleError(QualityError):
        """Quality rule errors."""

        def __init__(
            self,
            message: str = "Quality rule error",
            *,
            error_code: str = "QUALITY_RULE_ERROR",
            context: dict[str, object] | None = None,
        ) -> None:
            super().__init__(message, error_code=error_code, context=context)

        @override
        def __str__(self) -> str:
            return f"Quality rule: {self.message}"

    class IssueError(QualityError):
        """Quality issue errors."""

    class ThresholdError(QualityError):
        """Quality threshold errors."""


# Legacy compatibility aliases - following flext-cli pattern
FlextQualityError = FlextQualityExceptionsError.QualityError
FlextQualityValidationError = FlextQualityExceptionsError.ValidationError
FlextQualityConfigurationError = FlextQualityExceptionsError.ConfigurationError
FlextQualityConnectionError = FlextQualityExceptionsError.QualityConnectionError
FlextQualityProcessingError = FlextQualityExceptionsError.ProcessingError
FlextQualityAuthenticationError = FlextQualityExceptionsError.AuthenticationError
FlextQualityTimeoutError = FlextQualityExceptionsError.QualityTimeoutError
FlextQualityAnalysisError = FlextQualityExceptionsError.AnalysisError
FlextQualityReportError = FlextQualityExceptionsError.ReportError
FlextQualityMetricsError = FlextQualityExceptionsError.MetricsError
FlextQualityGradeError = FlextQualityExceptionsError.GradeError
FlextQualityRuleError = FlextQualityExceptionsError.RuleError
FlextQualityIssueError = FlextQualityExceptionsError.IssueError
FlextQualityThresholdError = FlextQualityExceptionsError.ThresholdError


# Export consolidated class and legacy aliases
__all__ = [
    "FlextQualityAnalysisError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    # Legacy compatibility aliases
    "FlextQualityError",
    "FlextQualityErrorCodes",
    "FlextQualityExceptionsError",
    "FlextQualityGradeError",
    "FlextQualityIssueError",
    "FlextQualityMetricsError",
    "FlextQualityProcessingError",
    "FlextQualityReportError",
    "FlextQualityRuleError",
    "FlextQualityThresholdError",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
]
