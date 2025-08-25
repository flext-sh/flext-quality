"""Application handlers for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core handler patterns - NO duplication.
    Clean architecture with command/query handling.
"""

from __future__ import annotations

from uuid import UUID

from flext_core import FlextResult, get_logger
from flext_observability import (
    flext_create_log_entry as _flext_create_log_entry,
    flext_create_trace as _flext_create_trace,
)

from flext_quality.entities import QualityAnalysis, QualityReport
from flext_quality.services import (
    LintingServiceImpl,
    QualityAnalysisService,
    QualityReportService,
    SecurityAnalyzerServiceImpl,
)

# Use flext-observability directly - no fallbacks
flext_create_log_entry = _flext_create_log_entry
flext_create_trace = _flext_create_trace

logger = get_logger(__name__)


# Using flext-core handlers directly - no fallbacks


# Real handlers using actual services
class AnalyzeProjectHandler:
    """Handler for analyzing projects."""

    def __init__(self) -> None:
        """Initialize handler with analysis service."""
        self._analysis_service = QualityAnalysisService()

    async def handle(self, project_id: UUID) -> FlextResult[QualityAnalysis]:
        """Handle project analysis command."""
        # Create trace for observability (optional dependency)
        flext_create_trace(
            operation_name="AnalyzeProjectHandler.handle",
            service_name="flext-quality",
            config={"project_id": str(project_id)},
        )

        # Log operation start
        flext_create_log_entry(
            message=f"Starting project analysis for {project_id}",
            service="flext-quality",
            level="info",
        )

        try:
            # Convert UUID to string for service compatibility
            project_id_str = str(project_id)

            # Create and start analysis
            analysis_result = await self._analysis_service.create_analysis(
                project_id=project_id_str,
            )

            # Use is_failure for early return pattern (current flext-core API)
            if analysis_result.is_failure:
                flext_create_log_entry(
                    message=f"Failed to create analysis: {analysis_result.error}",
                    service="flext-quality",
                    level="error",
                )
                return analysis_result

            # Safe value extraction using current API
            analysis = analysis_result.value

            flext_create_log_entry(
                message=f"Successfully created analysis for project {project_id}",
                service="flext-quality",
                level="info",
            )

            # Return the created analysis
            return FlextResult[QualityAnalysis].ok(analysis)

        except Exception as e:
            flext_create_log_entry(
                message=f"Unexpected error in AnalyzeProjectHandler: {e!s}",
                service="flext-quality",
                level="error",
            )
            logger.exception("Unexpected error in AnalyzeProjectHandler")
            return FlextResult[QualityAnalysis].fail(f"Unexpected error: {e!s}")


class GenerateReportHandler:
    """Handler for generating reports."""

    def __init__(self) -> None:
        """Initialize handler with report service."""
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

        # Use is_failure for early return pattern (current flext-core API)
        if report_result.is_failure:
            return report_result

        # Safe value extraction using current API
        report = report_result.value

        # Return the created report
        return FlextResult[QualityReport].ok(report)


class RunLintingHandler:
    """Handler for running linting checks."""

    def __init__(self) -> None:
        """Initialize handler with linting service implementation."""
        self._linting_service = LintingServiceImpl()

    async def handle(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Handle linting command."""
        # Convert UUID to string for service compatibility
        project_id_str = str(project_id)

        # Use analyzer to get project path (simplified)
        # In real implementation, this would get project info from repository
        project_path = f"/projects/{project_id_str}"  # Placeholder path

        # Run linting analysis
        linting_result = await self._linting_service.run_linting(project_path)

        # Use is_failure for early return pattern (current flext-core API)
        if linting_result.is_failure:
            return linting_result

        # Safe value extraction using current API
        linting_issues = linting_result.value

        # Return linting results
        return FlextResult[dict[str, object]].ok(linting_issues)


class RunSecurityCheckHandler:
    """Handler for running security checks."""

    def __init__(self) -> None:
        """Initialize handler with security analyzer service."""
        self._security_service = SecurityAnalyzerServiceImpl()

    async def handle(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Handle security check command."""
        # Convert UUID to string for service compatibility
        project_id_str = str(project_id)

        # Use analyzer to get project path (simplified)
        # In real implementation, this would get project info from repository
        project_path = f"/projects/{project_id_str}"  # Placeholder path

        # Run security analysis
        security_result = await self._security_service.analyze_security(project_path)

        # Use is_failure for early return pattern (current flext-core API)
        if security_result.is_failure:
            return security_result

        # Safe value extraction using current API
        security_issues = security_result.value

        # Return security analysis results
        return FlextResult[dict[str, object]].ok(security_issues)
