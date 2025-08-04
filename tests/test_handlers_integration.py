"""Integration tests for application handlers.

Real functional tests for all handler scenarios following flext-core patterns.
Tests error paths, success paths, and integration with real services.
"""

from __future__ import annotations

from unittest.mock import patch
from uuid import uuid4

from flext_core import FlextResult
from flext_quality.application.handlers import (
    AnalyzeProjectHandler,
    GenerateReportHandler,
    RunLintingHandler,
    RunSecurityCheckHandler,
)
from tests.conftest import (
    assert_result_failure_with_error,
    assert_result_success_with_data,
)


class TestAnalyzeProjectHandlerIntegration:
    """Integration tests for AnalyzeProjectHandler with real error scenarios."""

    async def test_handle_success_path(self) -> None:
        """Test successful project analysis flow."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        # This should work with the real service
        result = await handler.handle(project_id)

        # Should be success since service creates analysis
        analysis = assert_result_success_with_data(result)
        assert hasattr(analysis, "id")
        assert analysis.project_id == str(project_id)

    async def test_handle_service_failure_scenario(self) -> None:
        """Test handler when service fails to create analysis."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        # Mock the service to fail
        with patch.object(handler._analysis_service, "create_analysis") as mock_create:
            mock_create.return_value = FlextResult.fail("Service unavailable")

            result = await handler.handle(project_id)

            # Should propagate service failure
            error = assert_result_failure_with_error(result)
            assert "Service unavailable" in error

    async def test_handle_analysis_data_none_scenario(self) -> None:
        """Test handler when service returns None data."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        # Mock service to return success with None data
        with patch.object(handler._analysis_service, "create_analysis") as mock_create:
            mock_create.return_value = FlextResult.ok(None)

            result = await handler.handle(project_id)

            # Should fail with specific message
            error = assert_result_failure_with_error(result)
            assert "Analysis data is None" in error

    async def test_handle_unexpected_exception_scenario(self) -> None:
        """Test handler when service raises unexpected exception."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        # Mock service to raise exception
        with patch.object(handler._analysis_service, "create_analysis") as mock_create:
            mock_create.side_effect = RuntimeError("Database connection failed")

            result = await handler.handle(project_id)

            # Should catch and wrap exception
            error = assert_result_failure_with_error(result)
            assert "Unexpected error" in error
            assert "Database connection failed" in error


class TestGenerateReportHandlerIntegration:
    """Integration tests for GenerateReportHandler with real scenarios."""

    async def test_handle_success_path(self) -> None:
        """Test successful report generation."""
        handler = GenerateReportHandler()
        analysis_id = uuid4()

        result = await handler.handle(analysis_id)

        # Should succeed with real service
        report = assert_result_success_with_data(result)
        assert hasattr(report, "id")
        assert report.analysis_id == str(analysis_id)

    async def test_handle_service_failure_scenario(self) -> None:
        """Test handler when report service fails."""
        handler = GenerateReportHandler()
        analysis_id = uuid4()

        # Mock service to fail
        with patch.object(handler._report_service, "create_report") as mock_create:
            mock_create.return_value = FlextResult.fail("Analysis not found")

            result = await handler.handle(analysis_id)

            # Should propagate failure
            error = assert_result_failure_with_error(result)
            assert "Analysis not found" in error

    async def test_handle_report_data_none_scenario(self) -> None:
        """Test handler when service returns None report data."""
        handler = GenerateReportHandler()
        analysis_id = uuid4()

        # Mock service to return success with None
        with patch.object(handler._report_service, "create_report") as mock_create:
            mock_create.return_value = FlextResult.ok(None)

            result = await handler.handle(analysis_id)

            # Should fail with specific message
            error = assert_result_failure_with_error(result)
            assert "Report data is None" in error


class TestRunLintingHandlerIntegration:
    """Integration tests for RunLintingHandler with real scenarios."""

    async def test_handle_success_path(self) -> None:
        """Test successful linting execution."""
        handler = RunLintingHandler()
        project_id = uuid4()

        result = await handler.handle(project_id)

        # Should succeed with real service
        linting_data = assert_result_success_with_data(result)
        assert isinstance(linting_data, dict)
        assert "linting_issues" in linting_data

    async def test_handle_service_failure_scenario(self) -> None:
        """Test handler when linting service fails."""
        handler = RunLintingHandler()
        project_id = uuid4()

        # Mock service to fail
        with patch.object(handler._linting_service, "run_linting") as mock_lint:
            mock_lint.return_value = FlextResult.fail("Linting tool not found")

            result = await handler.handle(project_id)

            # Should propagate failure
            error = assert_result_failure_with_error(result)
            assert "Linting tool not found" in error

    async def test_handle_linting_data_none_scenario(self) -> None:
        """Test handler when linting service returns None data."""
        handler = RunLintingHandler()
        project_id = uuid4()

        # Mock service to return success with None
        with patch.object(handler._linting_service, "run_linting") as mock_lint:
            mock_lint.return_value = FlextResult.ok(None)

            result = await handler.handle(project_id)

            # Should fail with specific message
            error = assert_result_failure_with_error(result)
            assert "Linting data is None" in error


class TestRunSecurityCheckHandlerIntegration:
    """Integration tests for RunSecurityCheckHandler with real scenarios."""

    async def test_handle_success_path(self) -> None:
        """Test successful security check execution."""
        handler = RunSecurityCheckHandler()
        project_id = uuid4()

        result = await handler.handle(project_id)

        # Should succeed with real service
        security_data = assert_result_success_with_data(result)
        assert isinstance(security_data, dict)
        assert "security_issues" in security_data

    async def test_handle_service_failure_scenario(self) -> None:
        """Test handler when security service fails."""
        handler = RunSecurityCheckHandler()
        project_id = uuid4()

        # Mock service to fail
        with patch.object(
            handler._security_service,
            "analyze_security",
        ) as mock_security:
            mock_security.return_value = FlextResult.fail("Security scanner failed")

            result = await handler.handle(project_id)

            # Should propagate failure
            error = assert_result_failure_with_error(result)
            assert "Security scanner failed" in error

    async def test_handle_security_data_none_scenario(self) -> None:
        """Test handler when security service returns None data."""
        handler = RunSecurityCheckHandler()
        project_id = uuid4()

        # Mock service to return success with None
        with patch.object(
            handler._security_service,
            "analyze_security",
        ) as mock_security:
            mock_security.return_value = FlextResult.ok(None)

            result = await handler.handle(project_id)

            # Should fail with specific message
            error = assert_result_failure_with_error(result)
            assert "Security data is None" in error
