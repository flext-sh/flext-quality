"""Test application handlers."""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_quality import (
    AnalyzeProjectHandler,
    GenerateReportHandler,
    RunLintingHandler,
    RunSecurityCheckHandler,
)


class TestAnalyzeProjectHandler:
    """Test analyze project handler."""

    def test_handler_initialization(self) -> None:
        """Test handler can be initialized."""
        handler = AnalyzeProjectHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_creates_analysis(self) -> None:
        """Test analyze_project method creates analysis successfully."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        result = await handler.analyze_project(project_id)

        assert result.is_success
        assert result.value is not None
        # Should return a QualityAnalysis entity
        assert hasattr(result.value, "id")
        assert hasattr(result.value, "project_id")
        assert result.value.project_id == str(project_id)


class TestGenerateReportHandler:
    """Test generate report handler."""

    def test_handler_initialization(self) -> None:
        """Test handler can be initialized."""
        handler = GenerateReportHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_creates_report(self) -> None:
        """Test generate_report method creates report successfully."""
        handler = GenerateReportHandler()
        analysis_id = uuid4()

        result = await handler.generate_report(analysis_id)

        assert result.is_success
        assert result.value is not None
        # Should return a QualityReport entity
        assert hasattr(result.value, "id")
        assert hasattr(result.value, "analysis_id")
        assert result.value.analysis_id == str(analysis_id)


class TestRunLintingHandler:
    """Test run linting handler."""

    def test_handler_initialization(self) -> None:
        """Test handler can be initialized."""
        handler = RunLintingHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_runs_linting(self) -> None:
        """Test run_linting method runs linting successfully."""
        handler = RunLintingHandler()
        project_id = uuid4()

        result = await handler.run_linting(project_id)

        assert result.is_success
        assert result.value is not None
        # Should return linting results
        assert isinstance(result.value, dict)
        assert "issues" in result.value


class TestRunSecurityCheckHandler:
    """Test run security check handler."""

    def test_handler_initialization(self) -> None:
        """Test handler can be initialized."""
        handler = RunSecurityCheckHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_runs_security_check(self) -> None:
        """Test run_security_check method runs security check successfully."""
        handler = RunSecurityCheckHandler()
        project_id = uuid4()

        result = await handler.run_security_check(project_id)

        assert result.is_success
        assert result.value is not None
        # Should return security analysis results
        assert isinstance(result.value, dict)
        assert "vulnerabilities" in result.value


class TestHandlerIntegration:
    """Test handlers integration."""

    def test_all_handlers_can_be_instantiated(self) -> None:
        """Test all handlers can be instantiated together."""
        handlers = [
            AnalyzeProjectHandler(),
            GenerateReportHandler(),
            RunLintingHandler(),
            RunSecurityCheckHandler(),
        ]

        assert len(handlers) == 4
        for handler in handlers:
            assert handler is not None

    @pytest.mark.asyncio
    async def test_all_handlers_return_success(self) -> None:
        """Test all handlers return success with real implementations."""
        project_id = uuid4()
        analysis_id = uuid4()

        # Test specific handler methods instead of generic handle
        analyze_handler = AnalyzeProjectHandler()
        result = await analyze_handler.analyze_project(project_id)
        assert result.is_success
        assert result.value is not None

        report_handler = GenerateReportHandler()
        result = await report_handler.generate_report(analysis_id)
        assert result.is_success
        assert result.value is not None

        linting_handler = RunLintingHandler()
        result = await linting_handler.run_linting(project_id)
        assert result.is_success
        assert result.value is not None

        security_handler = RunSecurityCheckHandler()
        result = await security_handler.run_security_check(project_id)
        assert result.is_success
        assert result.value is not None
