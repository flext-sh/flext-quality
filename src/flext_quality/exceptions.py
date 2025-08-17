"""Quality Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides quality-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextErrorMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in quality operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

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


# Base quality exception hierarchy using FlextErrorMixin pattern
class FlextQualityError(FlextError):
    """Base exception for all quality domain errors."""


class FlextQualityValidationError(FlextQualityError):
    """Quality validation errors."""


class FlextQualityConfigurationError(FlextQualityError):
    """Quality configuration errors."""


class FlextQualityConnectionError(FlextQualityError):
    """Quality connection errors."""


class FlextQualityProcessingError(FlextQualityError):
    """Quality processing errors."""


class FlextQualityAuthenticationError(FlextQualityError):
    """Quality authentication errors."""


class FlextQualityTimeoutError(FlextQualityError):
    """Quality timeout errors."""


class FlextQualityAnalysisError(FlextQualityError):
    """Quality analysis errors."""


class FlextQualityReportError(FlextQualityError):
    """Quality report errors."""


class FlextQualityMetricsError(FlextQualityError):
    """Quality metrics errors."""


class FlextQualityGradeError(FlextQualityError):
    """Quality grade calculation errors."""


class FlextQualityRuleError(FlextQualityError):
    """Quality rule errors."""


class FlextQualityIssueError(FlextQualityError):
    """Quality issue management errors."""


class FlextQualityThresholdError(FlextQualityError):
    """Quality threshold validation errors."""


# Domain-specific exceptions for quality business logic
# Using modern FlextErrorMixin pattern with context support


class FlextQualityAnalysisOperationError(FlextQualityAnalysisError):
    """Quality analysis operation errors with analysis context."""

    def __init__(
        self,
        message: str,
        *,
        analyzer_name: str | None = None,
        file_count: int | None = None,
        analysis_type: str | None = None,
        execution_time: float | None = None,
        code: FlextQualityErrorCodes
        | None = FlextQualityErrorCodes.QUALITY_ANALYSIS_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality analysis context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if analyzer_name is not None:
            context_dict["analyzer_name"] = analyzer_name
        if file_count is not None:
            context_dict["file_count"] = file_count
        if analysis_type is not None:
            context_dict["analysis_type"] = analysis_type
        if execution_time is not None:
            context_dict["execution_time"] = execution_time

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextQualityReportOperationError(FlextQualityReportError):
    """Quality report operation errors with report context."""

    def __init__(
        self,
        message: str,
        *,
        report_type: str | None = None,
        output_format: str | None = None,
        project_name: str | None = None,
        report_size: int | None = None,
        code: FlextQualityErrorCodes
        | None = FlextQualityErrorCodes.QUALITY_REPORT_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality report context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if report_type is not None:
            context_dict["report_type"] = report_type
        if output_format is not None:
            context_dict["output_format"] = output_format
        if project_name is not None:
            context_dict["project_name"] = project_name
        if report_size is not None:
            context_dict["report_size"] = report_size

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextQualityMetricsOperationError(FlextQualityMetricsError):
    """Quality metrics operation errors with metrics context."""

    def __init__(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: float | None = None,
        metric_type: str | None = None,
        threshold_value: float | None = None,
        code: FlextQualityErrorCodes
        | None = FlextQualityErrorCodes.QUALITY_METRICS_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality metrics context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if metric_name is not None:
            context_dict["metric_name"] = metric_name
        if metric_value is not None:
            context_dict["metric_value"] = metric_value
        if metric_type is not None:
            context_dict["metric_type"] = metric_type
        if threshold_value is not None:
            context_dict["threshold_value"] = threshold_value

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextQualityGradeOperationError(FlextQualityGradeError):
    """Quality grade operation errors with grade context."""

    def __init__(
        self,
        message: str,
        *,
        grade_type: str | None = None,
        calculated_grade: str | None = None,
        grade_score: float | None = None,
        min_threshold: float | None = None,
        code: FlextQualityErrorCodes
        | None = FlextQualityErrorCodes.QUALITY_GRADE_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality grade context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if grade_type is not None:
            context_dict["grade_type"] = grade_type
        if calculated_grade is not None:
            context_dict["calculated_grade"] = calculated_grade
        if grade_score is not None:
            context_dict["grade_score"] = grade_score
        if min_threshold is not None:
            context_dict["min_threshold"] = min_threshold

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextQualityRuleOperationError(FlextQualityRuleError):
    """Quality rule operation errors with rule context."""

    def __init__(
        self,
        message: str,
        *,
        rule_name: str | None = None,
        rule_severity: str | None = None,
        rule_category: str | None = None,
        violation_count: int | None = None,
        code: FlextQualityErrorCodes | None = FlextQualityErrorCodes.QUALITY_RULE_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality rule context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if rule_name is not None:
            context_dict["rule_name"] = rule_name
        if rule_severity is not None:
            context_dict["rule_severity"] = rule_severity
        if rule_category is not None:
            context_dict["rule_category"] = rule_category
        if violation_count is not None:
            context_dict["violation_count"] = violation_count

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextQualityThresholdOperationError(FlextQualityThresholdError):
    """Quality threshold operation errors with threshold context."""

    def __init__(
        self,
        message: str,
        *,
        threshold_name: str | None = None,
        current_value: float | None = None,
        threshold_value: float | None = None,
        threshold_type: str | None = None,
        code: FlextQualityErrorCodes
        | None = FlextQualityErrorCodes.QUALITY_THRESHOLD_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with quality threshold context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if threshold_name is not None:
            context_dict["threshold_name"] = threshold_name
        if current_value is not None:
            context_dict["current_value"] = current_value
        if threshold_value is not None:
            context_dict["threshold_value"] = threshold_value
        if threshold_type is not None:
            context_dict["threshold_type"] = threshold_type

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


__all__: list[str] = [
    # Base exceptions (alphabetical)
    "FlextQualityAnalysisError",
    # Domain-specific operation exceptions
    "FlextQualityAnalysisOperationError",
    "FlextQualityAuthenticationError",
    "FlextQualityConfigurationError",
    "FlextQualityConnectionError",
    "FlextQualityError",
    # Error codes enum
    "FlextQualityErrorCodes",
    "FlextQualityGradeError",
    "FlextQualityGradeOperationError",
    "FlextQualityIssueError",
    "FlextQualityMetricsError",
    "FlextQualityMetricsOperationError",
    "FlextQualityProcessingError",
    "FlextQualityReportError",
    "FlextQualityReportOperationError",
    "FlextQualityRuleError",
    "FlextQualityRuleOperationError",
    "FlextQualityThresholdError",
    "FlextQualityThresholdOperationError",
    "FlextQualityTimeoutError",
    "FlextQualityValidationError",
]
