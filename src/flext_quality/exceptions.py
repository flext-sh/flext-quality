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

from flext_core import FlextCore


class FlextQualityExceptions(FlextCore.Exceptions):
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
    class Error(FlextCore.Exceptions.BaseError):
        """Base exception for all quality domain errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            component: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize quality error with context.

            Args:
                message: Error message
                component: Quality component that caused the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store component
            self.component = component

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = (
                str(kwargs.get("correlation_id"))
                if kwargs.get("correlation_id")
                else None
            )
            error_code = str(kwargs.get("error_code", "QUALITY_ERROR"))

            # Add component to context if provided
            if component:
                context["component"] = component

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code,
                correlation_id=correlation_id,
                metadata=context,
            )

    class ValidationError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_VALIDATION_ERROR"))

            # Add field name to context if provided
            if field_name:
                context["field_name"] = field_name

            # Call parent with specific error code
            super().__init__(
                message,
                component="validation",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class ConfigurationError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_CONFIGURATION_ERROR"))

            # Add config fields to context if provided
            if config_key:
                context["config_key"] = config_key
            if config_value is not None:
                context["config_value"] = str(config_value)

            # Call parent with specific error code
            super().__init__(
                message,
                component="configuration",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class ConnectionError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_CONNECTION_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="connection",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class ProcessingError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_PROCESSING_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="processing",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class AuthenticationError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_AUTHENTICATION_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="authentication",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class TimeoutError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_TIMEOUT_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="timeout",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class AnalysisError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_ANALYSIS_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="analysis",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class ReportError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_REPORT_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="reporting",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class MetricsError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_METRICS_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="metrics",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class GradeError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_GRADE_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="grading",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class RuleError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_RULE_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="rules",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class IssueError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_ISSUE_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="issues",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    class ThresholdError(Error):
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

            # Extract common parameters
            context_raw = kwargs.get("context", {})
            context = dict(context_raw) if isinstance(context_raw, dict) else {}
            correlation_id = kwargs.get("correlation_id")
            error_code = str(kwargs.get("error_code", "QUALITY_THRESHOLD_ERROR"))

            # Add specific fields to context if provided
            # (Add specific field handling here)

            # Call parent with specific error code
            super().__init__(
                message,
                component="thresholds",
                error_code=error_code,
                correlation_id=correlation_id,
                context=context,
            )

    # ==== INTERNAL TOOLS EXCEPTIONS (from flext_tools migration) ====

    class GitOperationError(FlextCore.Exceptions.BaseError):
        """Git operation error for quality tools."""

        def __init__(
            self,
            message: str,
            repo_path: str | None = None,
        ) -> None:
            """Initialize git operation error."""
            super().__init__(message)
            self.repo_path = repo_path

    class OptimizationError(FlextCore.Exceptions.BaseError):
        """Module optimization error."""

        def __init__(
            self,
            message: str,
            module_path: str | None = None,
        ) -> None:
            """Initialize optimization error."""
            super().__init__(message)
            self.module_path = module_path

    class GateFailure(FlextCore.Exceptions.ValidationError):
        """Quality gate validation failure."""

        def __init__(
            self,
            message: str,
            violations: FlextCore.Types.StringList,
        ) -> None:
            """Initialize quality gate failure."""
            super().__init__(message)
            self.violations = violations

    class DomainLibraryViolation(FlextCore.Exceptions.ValidationError):
        """Domain library usage violation."""

        def __init__(
            self,
            message: str,
            forbidden_import: str,
            required_library: str,
        ) -> None:
            """Initialize domain library violation."""
            super().__init__(message)
            self.forbidden_import = forbidden_import
            self.required_library = required_library

    class ValidationFailure(FlextCore.Exceptions.ValidationError):
        """General validation failure."""

        def __init__(
            self,
            message: str,
            failures: FlextCore.Types.StringList,
        ) -> None:
            """Initialize validation failure."""
            super().__init__(message)
            self.failures = failures

    class ArchitectureViolation(FlextCore.Exceptions.ValidationError):
        """Architecture violation error."""

        def __init__(
            self,
            message: str,
            violation_type: str,
        ) -> None:
            """Initialize architecture violation."""
            super().__init__(message)
            self.violation_type = violation_type

    class DependencyError(FlextCore.Exceptions.BaseError):
        """Dependency management error."""

        def __init__(
            self,
            message: str,
            dependency_name: str | None = None,
        ) -> None:
            """Initialize dependency error."""
            super().__init__(message)
            self.dependency_name = dependency_name

    class DryRunViolation(FlextCore.Exceptions.ValidationError):
        """Dry-run mode violation."""

        def __init__(
            self,
            message: str,
            operation: str,
        ) -> None:
            """Initialize dry-run violation."""
            super().__init__(message)
            self.operation = operation


# Backward compatibility aliases - property-based exports
FlextQualityErrorCodes = FlextQualityExceptions.ErrorCodes
FlextQualityError = FlextQualityExceptions.Error
FlextQualityValidationError = FlextQualityExceptions.ValidationError
FlextQualityConfigurationError = FlextQualityExceptions.ConfigurationError
FlextQualityConnectionError = FlextQualityExceptions.ConnectionError
FlextQualityProcessingError = FlextQualityExceptions.ProcessingError
FlextQualityAuthenticationError = FlextQualityExceptions.AuthenticationError
FlextQualityTimeoutError = FlextQualityExceptions.TimeoutError
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
