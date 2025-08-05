"""Test custom exceptions to achieve 100% coverage.

Tests all custom exceptions defined in exceptions.py to ensure they work correctly
and improve coverage from 0% to 100% for exceptions.py module.
"""

from __future__ import annotations

import pytest
from flext_quality.exceptions import (
    FlextQualityAnalysisError,
    FlextQualityAuthenticationError,
    FlextQualityConfigurationError,
    FlextQualityConnectionError,
    FlextQualityError,
    FlextQualityGradeError,
    FlextQualityMetricsError,
    FlextQualityProcessingError,
    FlextQualityReportError,
    FlextQualityRuleError,
    FlextQualityTimeoutError,
    FlextQualityValidationError,
)


class TestFlextQualityExceptions:
    """Test all custom exceptions defined in exceptions.py."""

    def test_base_exception_creation(self) -> None:
        """Test FlextQualityError base exception creation."""
        exception = FlextQualityError("Test error")
        assert "Test error" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, Exception)

    def test_validation_error_creation(self) -> None:
        """Test FlextQualityValidationError creation."""
        exception = FlextQualityValidationError("Validation failed")
        assert "Validation failed" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_configuration_error_creation(self) -> None:
        """Test FlextQualityConfigurationError creation."""
        exception = FlextQualityConfigurationError("Config error")
        assert "Config error" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_connection_error_creation(self) -> None:
        """Test FlextQualityConnectionError creation."""
        exception = FlextQualityConnectionError("Connection failed")
        assert "Connection failed" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_processing_error_creation(self) -> None:
        """Test FlextQualityProcessingError creation."""
        exception = FlextQualityProcessingError("Processing failed")
        assert "Processing failed" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_authentication_error_creation(self) -> None:
        """Test FlextQualityAuthenticationError creation."""
        exception = FlextQualityAuthenticationError("Auth failed")
        assert "Auth failed" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_timeout_error_creation(self) -> None:
        """Test FlextQualityTimeoutError creation."""
        exception = FlextQualityTimeoutError("Timeout occurred")
        assert "Timeout occurred" in str(exception)  # FlextError adds prefixes
        assert isinstance(exception, FlextQualityError)

    def test_analysis_error_basic(self) -> None:
        """Test FlextQualityAnalysisError with basic message."""
        exception = FlextQualityAnalysisError("Analysis failed")
        assert "Quality analysis: Analysis failed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_analysis_error_with_context(self) -> None:
        """Test FlextQualityAnalysisError with full context."""
        exception = FlextQualityAnalysisError(
            "Analyzer crashed",
            analyzer_name="pylint",
            file_count=42,
            custom_field="test_value",
        )
        assert "Quality analysis: Analyzer crashed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_analysis_error_default_message(self) -> None:
        """Test FlextQualityAnalysisError with default message."""
        exception = FlextQualityAnalysisError()
        assert "Quality analysis: Quality analysis error" in str(exception)

    def test_report_error_basic(self) -> None:
        """Test FlextQualityReportError with basic message."""
        exception = FlextQualityReportError("Report generation failed")
        assert "Quality report: Report generation failed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_report_error_with_context(self) -> None:
        """Test FlextQualityReportError with full context."""
        exception = FlextQualityReportError(
            "Invalid format", report_type="html", output_format="pdf", extra_info="test",
        )
        assert "Quality report: Invalid format" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_report_error_default_message(self) -> None:
        """Test FlextQualityReportError with default message."""
        exception = FlextQualityReportError()
        assert "Quality report: Quality report error" in str(exception)

    def test_metrics_error_basic(self) -> None:
        """Test FlextQualityMetricsError with basic message."""
        exception = FlextQualityMetricsError("Metrics calculation failed")
        assert "Quality metrics: Metrics calculation failed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_metrics_error_with_context(self) -> None:
        """Test FlextQualityMetricsError with full context."""
        exception = FlextQualityMetricsError(
            "Invalid value", metric_name="complexity", metric_value=42.5, threshold=10.0,
        )
        assert "Quality metrics: Invalid value" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_metrics_error_default_message(self) -> None:
        """Test FlextQualityMetricsError with default message."""
        exception = FlextQualityMetricsError()
        assert "Quality metrics: Quality metrics error" in str(exception)

    def test_grade_error_basic(self) -> None:
        """Test FlextQualityGradeError with basic message."""
        exception = FlextQualityGradeError("Grade calculation failed")
        assert "Quality grade: Grade calculation failed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_grade_error_with_context(self) -> None:
        """Test FlextQualityGradeError with full context."""
        exception = FlextQualityGradeError(
            "Invalid grade", grade_type="overall", calculated_grade="A++", score=95.5,
        )
        assert "Quality grade: Invalid grade" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_grade_error_default_message(self) -> None:
        """Test FlextQualityGradeError with default message."""
        exception = FlextQualityGradeError()
        assert "Quality grade: Quality grade error" in str(exception)

    def test_rule_error_basic(self) -> None:
        """Test FlextQualityRuleError with basic message."""
        exception = FlextQualityRuleError("Rule validation failed")
        assert "Quality rule: Rule validation failed" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_rule_error_with_context(self) -> None:
        """Test FlextQualityRuleError with full context."""
        exception = FlextQualityRuleError(
            "Rule not found", rule_name="E302", rule_severity="high", category="style",
        )
        assert "Quality rule: Rule not found" in str(exception)
        assert isinstance(exception, FlextQualityError)

    def test_rule_error_default_message(self) -> None:
        """Test FlextQualityRuleError with default message."""
        exception = FlextQualityRuleError()
        assert "Quality rule: Quality rule error" in str(exception)


class TestExceptionInheritance:
    """Test exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test that all custom exceptions inherit from FlextQualityError."""
        exceptions = [
            FlextQualityValidationError("test"),
            FlextQualityConfigurationError("test"),
            FlextQualityConnectionError("test"),
            FlextQualityProcessingError("test"),
            FlextQualityAuthenticationError("test"),
            FlextQualityTimeoutError("test"),
            FlextQualityAnalysisError("test"),
            FlextQualityReportError("test"),
            FlextQualityMetricsError("test"),
            FlextQualityGradeError("test"),
            FlextQualityRuleError("test"),
        ]

        for exception in exceptions:
            assert isinstance(exception, FlextQualityError)
            assert isinstance(exception, Exception)

    def test_exception_raising(self) -> None:
        """Test that exceptions can be raised and caught correctly."""
        msg = "Test analysis error"
        with pytest.raises(FlextQualityAnalysisError) as exc_info:
            raise FlextQualityAnalysisError(msg)

        assert "Quality analysis: Test analysis error" in str(exc_info.value)

        # Test catching by base class
        msg = "Test metrics error"
        with pytest.raises(FlextQualityError):
            raise FlextQualityMetricsError(msg)

        # Test catching by Exception (specific error type)
        msg = "Test report error"
        with pytest.raises(FlextQualityReportError, match="Test report error"):
            raise FlextQualityReportError(msg)


class TestExceptionModuleExports:
    """Test that all exceptions are properly exported."""

    def test_all_exceptions_in_all_list(self) -> None:
        """Test that __all__ contains all exception classes."""
        from flext_quality.exceptions import __all__

        expected_exceptions = {
            "FlextQualityAnalysisError",
            "FlextQualityAuthenticationError",
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
        }

        assert set(__all__) == expected_exceptions

    def test_all_exceptions_importable(self) -> None:
        """Test that all exceptions can be imported from the module."""
        import flext_quality.exceptions as exc_module
        from flext_quality.exceptions import __all__

        for exception_name in __all__:
            # Test that the exception class exists and is callable
            exception_class = getattr(exc_module, exception_name)
            assert callable(exception_class)

            # Test that we can create an instance
            instance = exception_class("test message")
            assert isinstance(instance, Exception)
