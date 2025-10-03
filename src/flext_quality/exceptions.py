"""FLEXT Quality Exceptions - Complete Quality Analysis Error Handling.

This module implements comprehensive exception handling for the FLEXT code quality analysis,
quality assurance, metrics collection, and reporting operations. Extends flext-core exception
foundation with domain-specific error types for production quality needs.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextExceptions


class FlextQualityExceptions(FlextExceptions):
    """Single CONSOLIDATED class containing ALL quality exceptions."""

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

    # Base quality exception classes as nested classes
    class QualityError(FlextExceptions.BaseError):
        """Base exception for all quality domain errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            component: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize quality error with context using helpers.

            Args:
                message: Error message
                component: Quality component that caused the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store component before extracting common kwargs
            self.component = component

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with quality-specific fields
            context = self._build_context(
                base_context,
                component=component,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "QUALITY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ValidationError(QualityError):
        """Quality validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            field_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize validation error using helpers.

            Args:
                message: Error message
                field_name: Name of the field that failed validation
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store field_name before extracting common kwargs
            self.field_name = field_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with validation-specific fields
            context = self._build_context(
                base_context,
                field_name=field_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="validation",
                code=error_code or "QUALITY_VALIDATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ConfigurationError(QualityError):
        """Quality configuration errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            config_key: str | None = None,
            config_value: object = None,
            **kwargs: object,
        ) -> None:
            """Initialize configuration error using helpers.

            Args:
                message: Error message
                config_key: Configuration key that failed
                config_value: Invalid configuration value
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store config attributes before extracting common kwargs
            self.config_key = config_key
            self.config_value = config_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with configuration fields
            context = self._build_context(
                base_context,
                config_key=config_key,
                config_value=config_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="configuration",
                code=error_code or "QUALITY_CONFIGURATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class QualityConnectionError(QualityError):
        """Quality connection errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            connection_target: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize connection error using helpers.

            Args:
                message: Error message
                connection_target: Target of the failed connection
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store connection attributes before extracting common kwargs
            self.connection_target = connection_target

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with connection fields
            context = self._build_context(
                base_context,
                connection_target=connection_target,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="connection",
                code=error_code or "QUALITY_CONNECTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ProcessingError(QualityError):
        """Quality processing errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            processing_step: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize processing error using helpers.

            Args:
                message: Error message
                processing_step: Processing step that failed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store processing attributes before extracting common kwargs
            self.processing_step = processing_step

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with processing fields
            context = self._build_context(
                base_context,
                processing_step=processing_step,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="processing",
                code=error_code or "QUALITY_PROCESSING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AuthenticationError(QualityError):
        """Quality authentication errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            username: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize authentication error using helpers.

            Args:
                message: Error message
                username: Username that failed authentication
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store username before extracting common kwargs
            self.username = username

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with authentication fields
            context = self._build_context(
                base_context,
                username=username,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="authentication",
                code=error_code or "QUALITY_AUTHENTICATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class QualityTimeoutError(QualityError):
        """Quality timeout errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            timeout_duration: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize timeout error using helpers.

            Args:
                message: Error message
                timeout_duration: Duration of the timeout in seconds
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store timeout attributes before extracting common kwargs
            self.timeout_duration = timeout_duration

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with timeout fields
            context = self._build_context(
                base_context,
                timeout_duration=timeout_duration,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="timeout",
                code=error_code or "QUALITY_TIMEOUT_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class AnalysisError(QualityError):
        """Quality analysis errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            analysis_type: str | None = None,
            project_path: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize analysis error using helpers.

            Args:
                message: Error message
                analysis_type: Type of analysis that failed
                project_path: Path to the project being analyzed
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store analysis attributes before extracting common kwargs
            self.analysis_type = analysis_type
            self.project_path = project_path

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with analysis fields
            context = self._build_context(
                base_context,
                analysis_type=analysis_type,
                project_path=project_path,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="analysis",
                code=error_code or "QUALITY_ANALYSIS_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ReportError(QualityError):
        """Quality report errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            report_format: str | None = None,
            report_path: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize report error using helpers.

            Args:
                message: Error message
                report_format: Format of the report being generated
                report_path: Path where the report should be saved
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store report attributes before extracting common kwargs
            self.report_format = report_format
            self.report_path = report_path

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with report fields
            context = self._build_context(
                base_context,
                report_format=report_format,
                report_path=report_path,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="reporting",
                code=error_code or "QUALITY_REPORT_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MetricsError(QualityError):
        """Quality metrics errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            metric_name: str | None = None,
            metric_value: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metrics error using helpers.

            Args:
                message: Error message
                metric_name: Name of the metric
                metric_value: Value of the metric
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store metrics attributes before extracting common kwargs
            self.metric_name = metric_name
            self.metric_value = metric_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with metrics fields
            context = self._build_context(
                base_context,
                metric_name=metric_name,
                metric_value=metric_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="metrics",
                code=error_code or "QUALITY_METRICS_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class GradeError(QualityError):
        """Quality grade errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            grade_value: str | None = None,
            score: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize grade error using helpers.

            Args:
                message: Error message
                grade_value: Quality grade value
                score: Numerical quality score
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store grade attributes before extracting common kwargs
            self.grade_value = grade_value
            self.score = score

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with grade fields
            context = self._build_context(
                base_context,
                grade_value=grade_value,
                score=score,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="grading",
                code=error_code or "QUALITY_GRADE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class RuleError(QualityError):
        """Quality rule errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            rule_id: str | None = None,
            rule_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize rule error using helpers.

            Args:
                message: Error message
                rule_id: Quality rule identifier
                rule_name: Quality rule name
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store rule attributes before extracting common kwargs
            self.rule_id = rule_id
            self.rule_name = rule_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with rule fields
            context = self._build_context(
                base_context,
                rule_id=rule_id,
                rule_name=rule_name,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="rules",
                code=error_code or "QUALITY_RULE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class IssueError(QualityError):
        """Quality issue errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            issue_id: str | None = None,
            severity: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize issue error using helpers.

            Args:
                message: Error message
                issue_id: Quality issue identifier
                severity: Issue severity level
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store issue attributes before extracting common kwargs
            self.issue_id = issue_id
            self.severity = severity

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with issue fields
            context = self._build_context(
                base_context,
                issue_id=issue_id,
                severity=severity,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="issues",
                code=error_code or "QUALITY_ISSUE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ThresholdError(QualityError):
        """Quality threshold errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            threshold_name: str | None = None,
            threshold_value: float | None = None,
            actual_value: float | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize threshold error using helpers.

            Args:
                message: Error message
                threshold_name: Name of the threshold
                threshold_value: Expected threshold value
                actual_value: Actual value that violated the threshold
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store threshold attributes before extracting common kwargs
            self.threshold_name = threshold_name
            self.threshold_value = threshold_value
            self.actual_value = actual_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with threshold fields
            context = self._build_context(
                base_context,
                threshold_name=threshold_name,
                threshold_value=threshold_value,
                actual_value=actual_value,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                component="thresholds",
                code=error_code or "QUALITY_THRESHOLD_ERROR",
                context=context,
                correlation_id=correlation_id,
            )


# Backward compatibility aliases - property-based exports
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
