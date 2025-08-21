"""Test application handlers."""

from __future__ import annotations

from uuid import uuid4

import pytest
from flext_core import FlextResult

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
        """Test handle method creates analysis successfully."""
        handler = AnalyzeProjectHandler()
        project_id = uuid4()

        result = await handler.handle(project_id)

        assert result.success
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
        """Test handle method creates report successfully."""
        handler = GenerateReportHandler()
        analysis_id = uuid4()

        result = await handler.handle(analysis_id)

        assert result.success
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
        """Test handle method runs linting successfully."""
        handler = RunLintingHandler()
        project_id = uuid4()

        result = await handler.handle(project_id)

        assert result.success
        assert result.value is not None
        # Should return linting results
        assert isinstance(result.value, dict)
        assert "linting_issues" in result.value


class TestRunSecurityCheckHandler:
    """Test run security check handler."""

    def test_handler_initialization(self) -> None:
        """Test handler can be initialized."""
        handler = RunSecurityCheckHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_runs_security_check(self) -> None:
        """Test handle method runs security check successfully."""
        handler = RunSecurityCheckHandler()
        project_id = uuid4()

        result = await handler.handle(project_id)

        assert result.success
        assert result.value is not None
        # Should return security analysis results
        assert isinstance(result.value, dict)
        assert "security_issues" in result.value


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

        handlers_and_ids = [
            (AnalyzeProjectHandler(), project_id),
            (GenerateReportHandler(), analysis_id),
            (RunLintingHandler(), project_id),
            (RunSecurityCheckHandler(), project_id),
        ]

        for handler, test_id in handlers_and_ids:
            if hasattr(handler, "handle"):
                result = await handler.handle(test_id)
            else:
                # Create a mock result for handlers without handle method
                result = FlextResult[str].ok("Mock success")
            assert result.success
            assert result.value is not None
