"""Modern Python 3.13 type aliases for comprehensive error handling in quality operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextContainer, FlextExceptions, FlextLogger, FlextTypes


class FlextQualityExceptions:
    """Unified quality exceptions class following FLEXT architecture patterns.

    Single responsibility: Quality error handling and exception management
    Contains all error codes and exceptions as nested classes with shared functionality.
    """

    def __init__(self: object) -> None:
        """Initialize exceptions with dependency injection."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    class ErrorCodes(Enum):
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

    class QualityError(FlextExceptions.BaseError):
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
            code: str = "QUALITY_ANALYSIS_ERROR",
            context: FlextTypes.Core.Dict | None = None,
        ) -> None:
            """Initialize quality analysis error with message and optional context."""
            super().__init__(message, code=code, context=context)

        @override
        def __str__(self: object) -> str:
            return f"Quality analysis: {self.message}"

    class ReportError(QualityError):
        """Quality report errors."""

        def __init__(
            self,
            message: str = "Quality report error",
            *,
            code: str = "QUALITY_REPORT_ERROR",
            context: FlextTypes.Core.Dict | None = None,
        ) -> None:
            """Initialize quality report error with message and optional context."""
            super().__init__(message, code=code, context=context)

        @override
        def __str__(self: object) -> str:
            return f"Quality report: {self.message}"

    class MetricsError(QualityError):
        """Quality metrics errors."""

        def __init__(
            self,
            message: str = "Quality metrics error",
            *,
            code: str = "QUALITY_METRICS_ERROR",
            context: FlextTypes.Core.Dict | None = None,
        ) -> None:
            """Initialize quality metrics error with message and optional context."""
            super().__init__(message, code=code, context=context)

        @override
        def __str__(self: object) -> str:
            return f"Quality metrics: {self.message}"

    class GradeError(QualityError):
        """Quality grade errors."""

        def __init__(
            self,
            message: str = "Quality grade error",
            *,
            code: str = "QUALITY_GRADE_ERROR",
            context: FlextTypes.Core.Dict | None = None,
        ) -> None:
            """Initialize quality grade error with message and optional context."""
            super().__init__(message, code=code, context=context)

        @override
        def __str__(self: object) -> str:
            return f"Quality grade: {self.message}"

    class RuleError(QualityError):
        """Quality rule errors."""

        def __init__(
            self,
            message: str = "Quality rule error",
            *,
            code: str = "QUALITY_RULE_ERROR",
            context: FlextTypes.Core.Dict | None = None,
        ) -> None:
            """Initialize quality rule error with message and optional context."""
            super().__init__(message, code=code, context=context)

        @override
        def __str__(self: object) -> str:
            return f"Quality rule: {self.message}"

    class IssueError(QualityError):
        """Quality issue errors."""

    class ThresholdError(QualityError):
        """Quality threshold errors."""


# Backward compatibility aliases for existing code
FlextQualityErrorCodes = FlextQualityExceptions.ErrorCodes
FlextQualityError = FlextQualityExceptions.QualityError
FlextQualityValidationError = FlextQualityExceptions.ValidationError
FlextQualityConfigurationError = FlextQualityExceptions.ConfigurationError
FlextQualityConnectionError = FlextQualityExceptions.QualityConnectionError
FlextQualityProcessingError = FlextQualityExceptions.ProcessingError
FlextQualityAuthenticationError = FlextQualityExceptions.AuthenticationError
FlextQualityTimeoutError = FlextQualityExceptions.QualityTimeoutError
FlextQualityAnalysisError = FlextQualityExceptions.AnalysisError
FlextQualityReportError = FlextQualityExceptions.ReportError
FlextQualityMetricsError = FlextQualityExceptions.MetricsError
FlextQualityGradeError = FlextQualityExceptions.GradeError
FlextQualityRuleError = FlextQualityExceptions.RuleError
FlextQualityIssueError = FlextQualityExceptions.IssueError
FlextQualityThresholdError = FlextQualityExceptions.ThresholdError

# Legacy compatibility facade
FlextQualityExceptionsError = FlextQualityExceptions

# Consolidated exceptions collection for legacy compatibility
exceptions_all = FlextQualityExceptions


# Export consolidated class and legacy aliases
__all__ = [
    "FlextQualityAnalysisError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    # Legacy compatibility aliases
    "FlextQualityError",
    "FlextQualityErrorCodes",
    "FlextQualityExceptions",
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
    "exceptions_all",
]
