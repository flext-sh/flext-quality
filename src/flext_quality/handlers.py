"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from typing import override
from uuid import UUID

from flext_core import FlextCore
from flext_observability import (
    flext_create_log_entry as _flext_create_log_entry,
    flext_create_trace as _flext_create_trace,
)

from .models import FlextQualityModels
from .services import FlextQualityServices

# Type aliases for convenience
QualityAnalysis = FlextQualityModels.Analysis
QualityReport = FlextQualityModels.Report


class FlextQualityHandlers:
    """CONSOLIDATED handlers class following FLEXT_REFACTORING_PROMPT.md pattern.

    Single class containing ALL handler functionality to eliminate duplication
    and follow FLEXT ecosystem standards.
    """

    class _ObservabilityHelper:
        """Nested helper class for observability operations."""

        @staticmethod
        def create_log_entry(message: str, service: str, level: str) -> None:
            """Create log entry using flext-observability."""
            # Note: service parameter not used by flext_create_log_entry API
            _ = service
            _flext_create_log_entry(message=message, level=level)

        @staticmethod
        def create_trace(
            operation_name: str,
            service_name: str,
            config: FlextCore.Types.StringDict,
        ) -> None:
            """Create trace using flext-observability."""
            # Map to actual flext_create_trace API parameters
            _ = config  # config parameter not used by API
            _flext_create_trace(
                name=service_name,
                operation=operation_name,
            )

    @override
    def __init__(self) -> None:
        """Initialize all services for handler operations."""
        self._services = FlextQualityServices()
        self._analysis_service = self._services.get_analysis_service()
        self._report_service = self._services.get_report_service()
        # Use placeholder services for now - these would be injected
        self._linting_service = None
        self._security_service = None
        self.logger = FlextCore.Logger(__name__)
        self._observability = self._ObservabilityHelper()

    def analyze_project(self, project_id: UUID) -> FlextCore.Result[QualityAnalysis]:
        """Handle project analysis command."""
        # Create trace for observability (optional dependency)
        self._observability.create_trace(
            operation_name="FlextQualityHandlers.analyze_project",
            service_name="flext-quality",
            config={"project_id": str(project_id)},
        )

        # Log operation start
        self._observability.create_log_entry(
            message=f"Starting project analysis for {project_id}",
            service="flext-quality",
            level="info",
        )

        try:
            # Convert UUID to string for service compatibility
            project_id_str = str(project_id)

            # Create and start analysis
            analysis_result = self._analysis_service.create_analysis(
                project_id=project_id_str,
            )

            # Use is_failure for early return pattern (current flext-core API)
            if analysis_result.is_failure:
                self._observability.create_log_entry(
                    message=f"Failed to create analysis: {analysis_result.error}",
                    service="flext-quality",
                    level="error",
                )
                return analysis_result

            # Safe value extraction using current API
            analysis = analysis_result.value

            self._observability.create_log_entry(
                message=f"Successfully created analysis for project {project_id}",
                service="flext-quality",
                level="info",
            )

            # Return the created analysis
            return FlextCore.Result[QualityAnalysis].ok(analysis)

        except Exception as e:
            self._observability.create_log_entry(
                message=f"Unexpected error in analyze_project: {e!s}",
                service="flext-quality",
                level="error",
            )
            self.logger.exception("Unexpected error in analyze_project")
            return FlextCore.Result[QualityAnalysis].fail(f"Unexpected error: {e!s}")

    def generate_report(self, analysis_id: UUID) -> FlextCore.Result[QualityReport]:
        """Handle report generation command."""
        # Convert UUID to string for service compatibility
        analysis_id_str = str(analysis_id)

        # Create report for the analysis
        report_result = self._report_service.create_report(
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
        return FlextCore.Result[QualityReport].ok(report)

    def run_linting(self, project_id: UUID) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Handle linting command."""
        # Return placeholder result since linting service is not implemented
        linting_data: FlextCore.Types.Dict = {
            "project_id": str(project_id),
            "status": "placeholder_implementation",
            "issues": [],
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(linting_data)

    def run_security_check(
        self,
        project_id: UUID,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Handle security check command."""
        # Return placeholder result since security service is not implemented
        security_data: FlextCore.Types.Dict = {
            "project_id": str(project_id),
            "status": "placeholder_implementation",
            "vulnerabilities": [],
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(security_data)


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
