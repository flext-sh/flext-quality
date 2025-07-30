"""Application handlers for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core handler patterns - NO duplication.
    Clean architecture with command/query handling.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextResult, TAnyDict
from flext_observability import flext_create_log_entry, flext_create_trace

from flext_quality.application.services import (
    LintingServiceImpl,
    QualityAnalysisService,
    QualityReportService,
    SecurityAnalyzerServiceImpl,
)

if TYPE_CHECKING:
    from flext_quality.domain.entities import QualityAnalysis, QualityReport

# Using flext-core handlers directly - no fallbacks

if TYPE_CHECKING:
    from uuid import UUID


# Real handlers using actual services
class AnalyzeProjectHandler:
    """Handler for analyzing projects."""

    def __init__(self) -> None:
        self._analysis_service = QualityAnalysisService()

    async def handle(self, project_id: UUID) -> FlextResult[QualityAnalysis]:
        """Handle project analysis command."""
        # Create trace for observability
        flext_create_trace(
            trace_id=f"analyze_project_{project_id}",
            operation="AnalyzeProjectHandler.handle",
            config={"project_id": str(project_id)},
        )

        # Log operation start
        flext_create_log_entry(
            message=f"Starting project analysis for {project_id}",
            level="info",
            context={"handler": "AnalyzeProjectHandler", "project_id": str(project_id)},
        )

        try:
            # Convert UUID to string for service compatibility
            project_id_str = str(project_id)

            # Create and start analysis
            analysis_result = await self._analysis_service.create_analysis(
                project_id=project_id_str,
            )

            if analysis_result.is_failure:
                flext_create_log_entry(
                    message=f"Failed to create analysis: {analysis_result.error}",
                    level="error",
                    context={"handler": "AnalyzeProjectHandler", "project_id": str(project_id)},
                )
                return analysis_result

            analysis = analysis_result.data
            if analysis is None:
                return FlextResult.fail("Analysis data is None")

            flext_create_log_entry(
                message=f"Successfully created analysis for project {project_id}",
                level="info",
                context={"handler": "AnalyzeProjectHandler", "project_id": str(project_id), "analysis_id": getattr(analysis, "id", None)},
            )

            # Return the created analysis
            return FlextResult.ok(analysis)

        except Exception as e:
            flext_create_log_entry(
                message=f"Unexpected error in AnalyzeProjectHandler: {e!s}",
                level="error",
                context={"handler": "AnalyzeProjectHandler", "project_id": str(project_id), "error": str(e)},
            )
            return FlextResult.fail(f"Unexpected error: {e!s}")


class GenerateReportHandler:
    """Handler for generating reports."""

    def __init__(self) -> None:
        self._report_service = QualityReportService()

    async def handle(self, analysis_id: UUID) -> FlextResult[QualityReport]:
        """Handle report generation command."""
        # Convert UUID to string for service compatibility
        analysis_id_str = str(analysis_id)

        # Create report for the analysis
        report_result = await self._report_service.create_report(
            analysis_id=analysis_id_str,
            report_type="comprehensive",
            report_format="html",
        )

        if report_result.is_failure:
            return report_result

        report = report_result.data
        if report is None:
            return FlextResult.fail("Report data is None")

        # Return the created report
        return FlextResult.ok(report)


class RunLintingHandler:
    """Handler for running linting checks."""

    def __init__(self) -> None:
        self._linting_service = LintingServiceImpl()

    async def handle(self, project_id: UUID) -> FlextResult[TAnyDict]:
        """Handle linting command."""
        # Convert UUID to string for service compatibility
        project_id_str = str(project_id)

        # Use analyzer to get project path (simplified)
        # In real implementation, this would get project info from repository
        project_path = f"/projects/{project_id_str}"  # Placeholder path

        # Run linting analysis
        linting_result = await self._linting_service.run_linting(project_path)

        if linting_result.is_failure:
            return linting_result

        linting_issues = linting_result.data
        if linting_issues is None:
            return FlextResult.fail("Linting data is None")

        # Return linting results
        return FlextResult.ok(linting_issues)


class RunSecurityCheckHandler:
    """Handler for running security checks."""

    def __init__(self) -> None:
        self._security_service = SecurityAnalyzerServiceImpl()

    async def handle(self, project_id: UUID) -> FlextResult[TAnyDict]:
        """Handle security check command."""
        # Convert UUID to string for service compatibility
        project_id_str = str(project_id)

        # Use analyzer to get project path (simplified)
        # In real implementation, this would get project info from repository
        project_path = f"/projects/{project_id_str}"  # Placeholder path

        # Run security analysis
        security_result = await self._security_service.analyze_security(project_path)

        if security_result.is_failure:
            return security_result

        security_issues = security_result.data
        if security_issues is None:
            return FlextResult.fail("Security data is None")

        # Return security analysis results
        return FlextResult.ok(security_issues)
