"""Application handlers for FLEXT-QUALITY v0.7.0.

REFACTORED: Single CONSOLIDATED class following FLEXT_REFACTORING_PROMPT.md patterns.
Uses flext-core handler patterns - NO duplication, NO multiple separate classes.
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
    QualityAnalysisService,
    QualityReportService,
)

# Use flext-observability directly - no fallbacks
flext_create_log_entry = _flext_create_log_entry
flext_create_trace = _flext_create_trace

logger = get_logger(__name__)


class FlextQualityHandlers:
    """CONSOLIDATED handlers class following FLEXT_REFACTORING_PROMPT.md pattern.

    Single class containing ALL handler functionality to eliminate duplication
    and follow FLEXT ecosystem standards.
    """

    def __init__(self) -> None:
        """Initialize all services for handler operations."""
        self._analysis_service = QualityAnalysisService()
        self._report_service = QualityReportService()
        # Use placeholder services for now - these would be injected
        self._linting_service = None
        self._security_service = None

    async def analyze_project(self, project_id: UUID) -> FlextResult[QualityAnalysis]:
        """Handle project analysis command."""
        # Create trace for observability (optional dependency)
        flext_create_trace(
            operation_name="FlextQualityHandlers.analyze_project",
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
                message=f"Unexpected error in analyze_project: {e!s}",
                service="flext-quality",
                level="error",
            )
            logger.exception("Unexpected error in analyze_project")
            return FlextResult[QualityAnalysis].fail(f"Unexpected error: {e!s}")

    async def generate_report(self, analysis_id: UUID) -> FlextResult[QualityReport]:
        """Handle report generation command."""
        # Convert UUID to string for service compatibility
        analysis_id_str = str(analysis_id)

        # Create report for the analysis
        report_result = await self._report_service.create_report(
            analysis_id=analysis_id_str,
            format_type="html",
            content="comprehensive report",
        )

        # Use is_failure for early return pattern (current flext-core API)
        if report_result.is_failure:
            return report_result

        # Safe value extraction using current API
        report = report_result.value

        # Return the created report
        return FlextResult[QualityReport].ok(report)

    async def run_linting(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Handle linting command."""
        # Return placeholder result since linting service is not implemented
        return FlextResult[dict[str, object]].ok({
            "project_id": str(project_id),
            "status": "placeholder_implementation",
            "issues": [],
        })

    async def run_security_check(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Handle security check command."""
        # Return placeholder result since security service is not implemented
        return FlextResult[dict[str, object]].ok({
            "project_id": str(project_id),
            "status": "placeholder_implementation",
            "vulnerabilities": [],
        })


# Backward compatibility aliases - following flext-cli pattern
AnalyzeProjectHandler = FlextQualityHandlers
GenerateReportHandler = FlextQualityHandlers
RunLintingHandler = FlextQualityHandlers
RunSecurityCheckHandler = FlextQualityHandlers


# Export consolidated class and aliases
__all__ = [
    # Backward compatibility
    "AnalyzeProjectHandler",
    "FlextQualityHandlers",
    "GenerateReportHandler",
    "RunLintingHandler",
    "RunSecurityCheckHandler",
]
