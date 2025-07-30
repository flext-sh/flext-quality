"""Quality service exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for quality service operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextQualityError(FlextError):
    """Base exception for quality service operations."""

    def __init__(
        self,
        message: str = "Quality service error",
        project_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality service error with context."""
        context = kwargs.copy()
        if project_name is not None:
            context["project_name"] = project_name

        super().__init__(message, error_code="QUALITY_SERVICE_ERROR", context=context)


class FlextQualityValidationError(FlextValidationError):
    """Quality service validation errors."""

    def __init__(
        self,
        message: str = "Quality validation failed",
        field: str | None = None,
        value: object = None,
        rule_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality validation error with context."""
        validation_details: dict[str, object] = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if rule_name is not None:
            context["rule_name"] = rule_name

        super().__init__(
            f"Quality validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextQualityConfigurationError(FlextConfigurationError):
    """Quality service configuration errors."""

    def __init__(
        self,
        message: str = "Quality configuration error",
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key

        super().__init__(f"Quality config: {message}", **context)


class FlextQualityConnectionError(FlextConnectionError):
    """Quality service connection errors."""

    def __init__(
        self,
        message: str = "Quality connection failed",
        service_name: str | None = None,
        endpoint: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality connection error with context."""
        context = kwargs.copy()
        if service_name is not None:
            context["service_name"] = service_name
        if endpoint is not None:
            context["endpoint"] = endpoint

        super().__init__(f"Quality connection: {message}", **context)


class FlextQualityProcessingError(FlextProcessingError):
    """Quality service processing errors."""

    def __init__(
        self,
        message: str = "Quality processing failed",
        analysis_type: str | None = None,
        file_path: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality processing error with context."""
        context = kwargs.copy()
        if analysis_type is not None:
            context["analysis_type"] = analysis_type
        if file_path is not None:
            context["file_path"] = file_path

        super().__init__(f"Quality processing: {message}", **context)


class FlextQualityTimeoutError(FlextTimeoutError):
    """Quality service timeout errors."""

    def __init__(
        self,
        message: str = "Quality operation timed out",
        operation: str | None = None,
        timeout_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize quality timeout error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if timeout_seconds is not None:
            context["timeout_seconds"] = timeout_seconds

        super().__init__(f"Quality timeout: {message}", **context)


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

        super().__init__(f"Quality analysis: {message}", project_name=None, **context)


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

        super().__init__(f"Quality report: {message}", project_name=None, **context)


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

        super().__init__(f"Quality metrics: {message}", project_name=None, **context)


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

        super().__init__(f"Quality grade: {message}", project_name=None, **context)


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

        super().__init__(f"Quality rule: {message}", project_name=None, **context)


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
