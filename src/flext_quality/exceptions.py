"""Quality service exception hierarchy using flext-core DRY patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions using factory pattern to eliminate 150+ lines of duplication.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


# Define base exception class explicitly for MyPy compatibility
class FlextQualityError(FlextError):
    """Base exception for all quality service errors."""


# Standard exception hierarchy using flext-core patterns
class FlextQualityValidationError(FlextValidationError):
    """Quality validation errors."""


class FlextQualityConfigurationError(FlextConfigurationError):
    """Quality configuration errors."""


class FlextQualityConnectionError(FlextConnectionError):
    """Quality connection errors."""


class FlextQualityProcessingError(FlextProcessingError):
    """Quality processing errors."""


class FlextQualityAuthenticationError(FlextAuthenticationError):
    """Quality authentication errors."""


class FlextQualityTimeoutError(FlextTimeoutError):
    """Quality timeout errors."""


class FlextQualityAnalysisError(FlextQualityError):
    """Quality service analysis errors."""

    def __init__(
        self,
        message: str = "Quality analysis error",
        analyzer_name: str | None = None,
        file_count: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality analysis error with context."""
        context = kwargs.copy()
        if analyzer_name is not None:
            context["analyzer_name"] = analyzer_name
        if file_count is not None:
            context["file_count"] = file_count

        super().__init__(f"Quality analysis: {message}", context=context)


class FlextQualityReportError(FlextQualityError):
    """Quality service report errors."""

    def __init__(
        self,
        message: str = "Quality report error",
        report_type: str | None = None,
        output_format: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality report error with context."""
        context = kwargs.copy()
        if report_type is not None:
            context["report_type"] = report_type
        if output_format is not None:
            context["output_format"] = output_format

        super().__init__(f"Quality report: {message}", context=context)


class FlextQualityMetricsError(FlextQualityError):
    """Quality service metrics errors."""

    def __init__(
        self,
        message: str = "Quality metrics error",
        metric_name: str | None = None,
        metric_value: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality metrics error with context."""
        context = kwargs.copy()
        if metric_name is not None:
            context["metric_name"] = metric_name
        if metric_value is not None:
            context["metric_value"] = metric_value

        super().__init__(f"Quality metrics: {message}", context=context)


class FlextQualityGradeError(FlextQualityError):
    """Quality service grade calculation errors."""

    def __init__(
        self,
        message: str = "Quality grade error",
        grade_type: str | None = None,
        calculated_grade: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality grade error with context."""
        context = kwargs.copy()
        if grade_type is not None:
            context["grade_type"] = grade_type
        if calculated_grade is not None:
            context["calculated_grade"] = calculated_grade

        super().__init__(f"Quality grade: {message}", context=context)


class FlextQualityRuleError(FlextQualityError):
    """Quality service rule errors."""

    def __init__(
        self,
        message: str = "Quality rule error",
        rule_name: str | None = None,
        rule_severity: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality rule error with context."""
        context = kwargs.copy()
        if rule_name is not None:
            context["rule_name"] = rule_name
        if rule_severity is not None:
            context["rule_severity"] = rule_severity

        super().__init__(f"Quality rule: {message}", context=context)


__all__ = [
    "FlextQualityAnalysisError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityError",
    "FlextQualityGradeError",
    "FlextQualityMetricsError",
    "FlextQualityProcessingError",
    "FlextQualityReportError",
    "FlextQualityRuleError",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
]
