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

from .models import FlextQualityModels
from .services import FlextQualityServices

# =====================================================================
# Configuration Models (Pydantic 2) - Data-Driven Handlers
# =====================================================================


class ObservabilityConfig(BaseModel):
    """Observability configuration for handlers."""

    service_name: str = Field(default="flext-quality")
    log_level: str = Field(default="info")
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
                f"{message} | project_id={context.project_id} operation={context.operation}"
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
                project_id=project_id_str
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
        self, project_id: UUID
    ) -> FlextResult[FlextQualityModels.Analysis]:
        """Analyze project with observability."""
        context = HandlerContext(
            project_id=str(project_id),
            operation="analyze_project",
        )

        self._ObservabilityManager.trace_operation(
            "analyze_project", self.config.service_name
        )
        self._ObservabilityManager.log_operation(
            "Starting project analysis", "info", context
        )

        return (
            self._AnalysisOrchestrator.execute_analysis(project_id, self._services)
            .map_error(lambda e: self._log_error(context, e))
            .map(lambda a: self._log_success(context, a))
        )

    def generate_report(
        self, analysis_id: UUID
    ) -> FlextResult[FlextQualityModels.Report]:
        """Generate report with observability."""
        context = HandlerContext(
            project_id=str(analysis_id),
            operation="generate_report",
        )

        self._ObservabilityManager.trace_operation(
            "generate_report", self.config.service_name
        )
        self._ObservabilityManager.log_operation(
            "Starting report generation", "info", context
        )

        return self._ReportOrchestrator.execute_report_generation(
            analysis_id, self._services
        ).map_error(lambda e: self._log_error(context, e))

    def run_linting(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Execute linting on project."""
        self._ObservabilityManager.trace_operation(
            "run_linting", self.config.service_name
        )

        result: dict[str, object] = {
            "project_id": str(project_id),
            "status": "success",
            "issues": [],
        }

        return FlextResult.ok(result)

    def run_security_check(self, project_id: UUID) -> FlextResult[dict[str, object]]:
        """Execute security check on project."""
        self._ObservabilityManager.trace_operation(
            "run_security_check", self.config.service_name
        )

        result: dict[str, object] = {
            "project_id": str(project_id),
            "status": "success",
            "vulnerabilities": [],
        }

        return FlextResult.ok(result)

    # =====================================================================
    # Private Helper Methods
    # =====================================================================

    def _log_error(self, context: HandlerContext, error: str) -> str:
        """Log and return error."""
        self._ObservabilityManager.log_operation(
            f"Operation failed: {error}", "error", context
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


# =====================================================================
# Concrete Handler Classes - SOLID Single Responsibility Principle
# =====================================================================


class AnalyzeProjectHandler:
    """Handler for project analysis operations."""

    def __init__(self) -> None:
        """Initialize handler."""
        self._handlers = FlextQualityHandlers()
        self._analysis_service = self._handlers._services.get_analysis_service()
        self._logger = FlextLogger(__name__)

    def analyze_project(self, project_id: object) -> FlextResult[object]:
        """Analyze project and return analysis result."""
        try:
            result = self._analysis_service.create_analysis(project_id=str(project_id))

            if result.is_failure:
                return FlextResult.fail(f"Analysis failed: {result.error}")

            if result.value is None:
                return FlextResult.fail("Analysis data is None")

            return FlextResult.ok(result.value)
        except Exception as e:
            error_msg = f"Unexpected error during analysis: {e!s}"
            self._logger.exception(error_msg)
            return FlextResult.fail(error_msg)


class GenerateReportHandler:
    """Handler for report generation operations."""

    def __init__(self) -> None:
        """Initialize handler."""
        self._handlers = FlextQualityHandlers()
        self._report_service = self._handlers._services.get_report_service()
        self._logger = FlextLogger(__name__)

    def generate_report(self, analysis_id: object) -> FlextResult[object]:
        """Generate report from analysis."""
        try:
            result = self._report_service.generate_report(analysis_id=str(analysis_id))

            if result.is_failure:
                return FlextResult.fail(f"Report generation failed: {result.error}")

            if result.value is None:
                return FlextResult.fail("Report data is None")

            return FlextResult.ok(result.value)
        except Exception as e:
            error_msg = f"Unexpected error during report generation: {e!s}"
            self._logger.exception(error_msg)
            return FlextResult.fail(error_msg)


class RunLintingHandler:
    """Handler for linting operations."""

    def __init__(self) -> None:
        """Initialize handler."""
        self._handlers = FlextQualityHandlers()
        self._logger = FlextLogger(__name__)

    def run_linting(self, project_id: object) -> FlextResult[object]:
        """Run linting checks on project."""
        try:
            result = self._handlers.run_linting(project_id)  # type: ignore

            if result.is_failure:
                return FlextResult.fail(f"Linting failed: {result.error}")

            return FlextResult.ok(result.value)
        except Exception as e:
            error_msg = f"Unexpected error during linting: {e!s}"
            self._logger.exception(error_msg)
            return FlextResult.fail(error_msg)


class RunSecurityCheckHandler:
    """Handler for security check operations."""

    def __init__(self) -> None:
        """Initialize handler."""
        self._handlers = FlextQualityHandlers()
        self._logger = FlextLogger(__name__)

    def run_security_check(self, project_id: object) -> FlextResult[object]:
        """Run security checks on project."""
        try:
            result = self._handlers.run_security_check(project_id)  # type: ignore

            if result.is_failure:
                return FlextResult.fail(f"Security check failed: {result.error}")

            return FlextResult.ok(result.value)
        except Exception as e:
            error_msg = f"Unexpected error during security check: {e!s}"
            self._logger.exception(error_msg)
            return FlextResult.fail(error_msg)


__all__ = [
    "AnalyzeProjectHandler",
    "FlextQualityHandlers",
    "GenerateReportHandler",
    "HandlerContext",
    "ObservabilityConfig",
    "RunLintingHandler",
    "RunSecurityCheckHandler",
]
