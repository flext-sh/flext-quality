"""FLEXT Quality event handlers with observability integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from uuid import UUID

from flext_core import FlextLogger, FlextResult
from flext_observability import (
    flext_create_trace,
)
from pydantic import BaseModel, Field

from .constants import FlextQualityConstants
from .models import FlextQualityModels
from .services import FlextQualityServices

# =====================================================================
# Configuration Models (Pydantic 2) - Data-Driven Handlers
# =====================================================================


class ObservabilityConfig(BaseModel):
    """Observability configuration for handlers."""

    service_name: str = Field(default="flext-quality")
    log_level: FlextQualityConstants.Literals.LogLevelLiteral | str = Field(
        default="info",
    )
    enable_traces: bool = Field(default=True)


class HandlerContext(BaseModel):
    """Handler execution context."""

    project_id: str
    operation: str
    metadata: dict[str, str] = Field(default_factory=dict)


# =====================================================================
# Main Handlers - SOLID Delegation with Observability
# =====================================================================


class FlextQualityHandlers:
    """Quality handlers orchestrating analysis and reporting operations."""

    def __init__(
        self,
        config: ObservabilityConfig | None = None,
    ) -> None:
        """Initialize handlers."""
        self.config = config or ObservabilityConfig()
        self._services = FlextQualityServices()
        self._logger = FlextLogger(__name__)

    def get_analysis_service(self) -> object:
        """Get analysis service instance."""
        return self._services.get_analysis_service()

    def get_report_service(self) -> object:
        """Get report service instance."""
        return self._services.get_report_service()

    # =====================================================================
    # Nested Utility Classes - Single Responsibility
    # =====================================================================

    class _ObservabilityManager:
        """Single responsibility: Manage observability operations."""

        @staticmethod
        def log_operation(
            message: str,
            level: FlextQualityConstants.Literals.LogLevelLiteral | str,
            context: HandlerContext,
        ) -> None:
            """Log operation with context."""
            # Use logger for operation logging with context
            logger = FlextLogger(__name__)
            logger_method = getattr(logger, level.lower(), logger.info)
            logger_method(
                f"{message} | project_id={context.project_id} operation={context.operation}",
            )

        @staticmethod
        def trace_operation(
            operation_name: str,
            service_name: str,
        ) -> None:
            """Create trace for operation."""
            # Create span for operation tracing
            flext_create_trace(
                name=f"{service_name}:{operation_name}",
                attributes={"operation": operation_name, "service": service_name},
            )

    class _AnalysisOrchestrator:
        """Single responsibility: Orchestrate analysis operations."""

        @staticmethod
        def execute_analysis(
            project_id: UUID,
            services: FlextQualityServices,
        ) -> FlextResult[FlextQualityModels.Analysis]:
            """Execute project analysis."""
            project_id_str = str(project_id)
            return services.get_analysis_service().create_analysis(
                project_id=project_id_str,
            )

    class _ReportOrchestrator:
        """Single responsibility: Orchestrate report operations."""

        @staticmethod
        def execute_report_generation(
            analysis_id: UUID,
            services: FlextQualityServices,
        ) -> FlextResult[FlextQualityModels.Report]:
            """Execute report generation."""
            analysis_id_str = str(analysis_id)
            return services.get_report_service().create_report(
                analysis_id=analysis_id_str,
                format_type="html",
                content="complete report",
            )

    # =====================================================================
    # Main Handler Methods - Railway-Oriented Programming
    # =====================================================================

    def analyze_project(
        self,
        project_id: UUID,
    ) -> FlextResult[FlextQualityModels.Analysis]:
        """Analyze project with observability."""
        context = HandlerContext(
            project_id=str(project_id),
            operation="analyze_project",
        )

        self._ObservabilityManager.trace_operation(
            "analyze_project",
            self.config.service_name,
        )
        self._ObservabilityManager.log_operation(
            "Starting project analysis",
            "info",
            context,
        )

        return (
            self._AnalysisOrchestrator.execute_analysis(project_id, self._services)
            .map_error(lambda e: self._log_error(context, e))
            .map(lambda a: self._log_success(context, a))
        )

    def generate_report(
        self,
        analysis_id: UUID,
    ) -> FlextResult[FlextQualityModels.Report]:
        """Generate report with observability."""
        context = HandlerContext(
            project_id=str(analysis_id),
            operation="generate_report",
        )

        self._ObservabilityManager.trace_operation(
            "generate_report",
            self.config.service_name,
        )
        self._ObservabilityManager.log_operation(
            "Starting report generation",
            "info",
            context,
        )

        return self._ReportOrchestrator.execute_report_generation(
            analysis_id,
            self._services,
        ).map_error(lambda e: self._log_error(context, e))

    # =====================================================================
    # Private Helper Methods
    # =====================================================================

    def _log_error(self, context: HandlerContext, error: str) -> str:
        """Log and return error."""
        self._ObservabilityManager.log_operation(
            f"Operation failed: {error}",
            "error",
            context,
        )
        self._logger.error(f"Handler error in {context.operation}: {error}")
        return error

    def _log_success(self, context: HandlerContext, result: object) -> object:
        """Log and return success result."""
        self._ObservabilityManager.log_operation(
            "Operation completed successfully",
            "info",
            context,
        )
        return result


__all__ = [
    "FlextQualityHandlers",
    "HandlerContext",
    "ObservabilityConfig",
]
