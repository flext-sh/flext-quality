"""FLEXT Quality event handlers with observability integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeVar
from uuid import UUID

from flext_core import FlextLogger, FlextResult, FlextRuntime
from flext_observability import (
    flext_create_trace,
)
from pydantic import BaseModel, Field

from .config import FlextQualityConfig
from .models import m
from .services import AnalysisServiceBuilder, FlextQualityServices, ReportServiceBuilder

_T = TypeVar("_T")

# =====================================================================
# Configuration Models (Pydantic 2) - Data-Driven Handlers
# =====================================================================


class ObservabilityConfig(BaseModel):
    """Observability configuration for handlers."""

    service_name: str = Field(default="flext-quality")
    log_level: str = Field(
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

    def get_services(self) -> object:
        """Get services instance."""
        return self._services

    # =====================================================================
    # Nested Utility Classes - Single Responsibility
    # =====================================================================

    class _ObservabilityManager:
        """Single responsibility: Manage observability operations."""

        @staticmethod
        def log_operation(
            message: str,
            level: str,
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
            _services: object,
        ) -> FlextResult[m.AnalysisModel]:
            """Execute project analysis using builder pattern."""
            config = FlextQualityConfig()
            logger = FlextLogger(__name__)
            return (
                AnalysisServiceBuilder(config, logger)
                .with_project_id(project_id)
                .build()
            )

    class _ReportOrchestrator:
        """Single responsibility: Orchestrate report operations."""

        @staticmethod
        def execute_report_generation(
            analysis_id: UUID,
            _services: object,
        ) -> FlextResult[m.ReportModel]:
            """Execute report generation using builder pattern."""
            config = FlextQualityConfig()
            logger = FlextLogger(__name__)
            return (
                ReportServiceBuilder(config, logger)
                .with_analysis_id(analysis_id)
                .with_format("HTML")
                .build()
            )

    # =====================================================================
    # Main Handler Methods - Railway-Oriented Programming
    # =====================================================================

    def analyze_project(
        self,
        project_id: UUID,
    ) -> FlextRuntime.RuntimeResult[m.AnalysisModel]:
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
    ) -> FlextRuntime.RuntimeResult[m.ReportModel]:
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

    def _log_success(self, context: HandlerContext, result: _T) -> _T:
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
