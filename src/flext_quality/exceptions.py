"""Quality Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides quality-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextErrorMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in quality operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextError


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
class FlextQualityExceptionsError(FlextError):
    """Single consolidated class containing ALL quality exceptions.
    
    Consolidates ALL exception definitions into one class following FLEXT patterns.
    Individual exceptions available as nested classes for organization.
    """

    class QualityError(FlextError):
        """Base exception for all quality domain errors."""


    class ValidationError(FlextError):
        """Quality validation errors."""


    class ConfigurationError(FlextError):
        """Quality configuration errors."""


    class QualityConnectionError(FlextError):
        """Quality connection errors."""


    class ProcessingError(FlextError):
        """Quality processing errors."""


    class AuthenticationError(FlextError):
        """Quality authentication errors."""


    class QualityTimeoutError(FlextError):
        """Quality timeout errors."""


    class AnalysisError(FlextError):
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

    class ReportError(FlextError):
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

    class MetricsError(FlextError):
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

    class GradeError(FlextError):
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

    class RuleError(FlextError):
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

    class IssueError(FlextError):
        """Quality issue errors."""


    class ThresholdError(FlextError):
        """Quality threshold errors."""


    # Legacy compatibility properties (as per FLEXT_REFACTORING_PROMPT.md)
    @property
    def FlextQualityError(self):
        return self.QualityError

    @property
    def FlextQualityValidationError(self):
        return self.ValidationError

    @property
    def FlextQualityConfigurationError(self):
        return self.ConfigurationError

    @property
    def FlextQualityConnectionError(self):
        return self.QualityConnectionError

    @property
    def FlextQualityProcessingError(self):
        return self.ProcessingError

    @property
    def FlextQualityAuthenticationError(self):
        return self.AuthenticationError

    @property
    def FlextQualityTimeoutError(self):
        return self.QualityTimeoutError

    @property
    def FlextQualityAnalysisError(self):
        return self.AnalysisError

    @property
    def FlextQualityReportError(self):
        return self.ReportError

    @property
    def FlextQualityMetricsError(self):
        return self.MetricsError

    @property
    def FlextQualityGradeError(self):
        return self.GradeError

    @property
    def FlextQualityRuleError(self):
        return self.RuleError

    @property
    def FlextQualityIssueError(self):
        return self.IssueError

    @property
    def FlextQualityThresholdError(self):
        return self.ThresholdError


# Export consolidated class
__all__ = [
    "FlextQualityErrorCodes",
    "FlextQualityExceptionsError",
]
