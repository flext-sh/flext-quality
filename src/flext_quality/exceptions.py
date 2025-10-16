"""Exception hierarchy for flext-quality.

The legacy ``flext_tools`` package exposed a rich set of exception classes that
callers still import.  This module provides lightweight replacements so the
public API remains stable after the migration.
"""

from __future__ import annotations


class FlextQualityError(Exception):
    """Base exception for flext-quality."""


class FlextQualityAnalysisError(FlextQualityError):
    """Raised when an analysis operation fails."""


class FlextQualityConfigurationError(FlextQualityError):
    """Raised when configuration is invalid or missing."""


class FlextQualityConnectionError(FlextQualityError):
    """Raised when an external dependency cannot be reached."""


class FlextQualityAuthenticationError(FlextQualityError):
    """Raised when authentication with an external system fails."""


class FlextQualityValidationError(FlextQualityError):
    """Raised when data validation fails."""


class FlextQualityProcessingError(FlextQualityError):
    """Raised when an internal processing step fails."""


class FlextQualityTimeoutError(FlextQualityError):
    """Raised when an operation times out."""


class FlextQualityGradeError(FlextQualityError):
    """Raised when quality grading fails."""


class FlextQualityMetricsError(FlextQualityError):
    """Raised when metric calculation fails."""


class FlextQualityReportError(FlextQualityError):
    """Raised when report generation fails."""


class FlextQualityRuleError(FlextQualityError):
    """Raised when a quality rule evaluation fails."""


class FlextQualityExceptions:
    """Namespace container replicating the legacy flext_tools API."""

    Analysis = FlextQualityAnalysisError
    Authentication = FlextQualityAuthenticationError
    Configuration = FlextQualityConfigurationError
    Connection = FlextQualityConnectionError
    Error = FlextQualityError
    Grade = FlextQualityGradeError
    Metrics = FlextQualityMetricsError
    Processing = FlextQualityProcessingError
    Report = FlextQualityReportError
    Rule = FlextQualityRuleError
    Timeout = FlextQualityTimeoutError
    Validation = FlextQualityValidationError


__all__ = [
    "FlextQualityAnalysisError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityError",
    "FlextQualityExceptions",
    "FlextQualityGradeError",
    "FlextQualityMetricsError",
    "FlextQualityProcessingError",
    "FlextQualityReportError",
    "FlextQualityRuleError",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
]
