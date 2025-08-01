"""Quality service exception hierarchy using flext-core DRY patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions using factory pattern to eliminate 150+ lines of duplication.
"""

from __future__ import annotations

from flext_core.exceptions import (
    create_module_exception_classes,
)

# Create all standard exception classes using factory pattern - eliminates duplication
quality_exceptions = create_module_exception_classes("flext_quality")

# Import generated classes for clean usage
FlextQualityError = quality_exceptions["FlextQualityError"]
FlextQualityValidationError = quality_exceptions["FlextQualityValidationError"]
FlextQualityConfigurationError = quality_exceptions["FlextQualityConfigurationError"]
FlextQualityConnectionError = quality_exceptions["FlextQualityConnectionError"]
FlextQualityProcessingError = quality_exceptions["FlextQualityProcessingError"]
FlextQualityAuthenticationError = quality_exceptions["FlextQualityAuthenticationError"]
FlextQualityTimeoutError = quality_exceptions["FlextQualityTimeoutError"]


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
