"""FLEXT Quality Services - Consolidated application services orchestration.

SINGLE CLASS MODULE - All services consolidated here following SOLID principles.
Each inner service class has a SINGLE RESPONSIBILITY and delegates appropriately.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
)

from .config import FlextQualityConfig
from .models import FlextQualityModels


class FlextQualityServices(FlextService[None]):
    """Unified consolidated services - SINGLE CLASS per module.

    Architecture: Layer 3 (Application)
    Single Responsibility: Delegate all domain operations through focused inner services

    Inner services (nested classes):
    - ProjectService: Project lifecycle (SOLID: single responsibility)
    - AnalysisService: Analysis lifecycle (SOLID: single responsibility)
    - IssueService: Issue lifecycle (SOLID: single responsibility)
    - ReportService: Report lifecycle (SOLID: single responsibility)

    Each inner service DELEGATES to:
    - FlextQualityModels for domain model operations
    - FlextQualityConfig for configuration
    - External backends for actual quality tool execution
    """

    def __init__(self, config: FlextQualityConfig | None = None) -> None:
        """Initialize consolidated services with FLEXT integration.

        Args:
        config: Optional quality configuration (uses default if None)

        """
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._config = config or FlextQualityConfig()
        self._container = FlextContainer.get_global()

        # Initialize inner services (lazy delegation pattern)
        self._project_service = self.ProjectService(self._config, self._logger)
        self._analysis_service = self.AnalysisService(self._config, self._logger)
        self._issue_service = self.IssueService(self._config, self._logger)
        self._report_service = self.ReportService(self._config, self._logger)

    @override
    def execute(self, data: object) -> FlextResult[None]:
        """Execute services (main entry point)."""
        return FlextResult[None].ok(None)

    # =========================================================================
    # PUBLIC SERVICE ACCESSORS - Clean delegation pattern
    # =========================================================================

    @property
    def project_service(self) -> ProjectService:
        """Get project service (singleton per FlextQualityServices instance)."""
        return self._project_service

    @property
    def analysis_service(self) -> AnalysisService:
        """Get analysis service (singleton per FlextQualityServices instance)."""
        return self._analysis_service

    @property
    def issue_service(self) -> IssueService:
        """Get issue service (singleton per FlextQualityServices instance)."""
        return self._issue_service

    @property
    def report_service(self) -> ReportService:
        """Get report service (singleton per FlextQualityServices instance)."""
        return self._report_service

    # =========================================================================
    # INNER SERVICE: ProjectService - Single responsibility: Project lifecycle
    # =========================================================================

    class ProjectService(FlextService[None]):
        """Service for project management - SOLID: Single Responsibility."""

        def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
            """Initialize project service."""
            super().__init__()
            self._config = config
            self._logger = logger

        @override
        def execute(self, data: object) -> FlextResult[None]:
            """Execute project service."""
            return FlextResult[None].ok(None)

        def create_project(
            self,
            name: str,
            path: str,
            **kwargs: object,
        ) -> FlextResult[FlextQualityModels.ProjectModel]:
            """Create new project - DELEGATES to FlextQualityModels for validation."""
            try:
                project = FlextQualityModels.ProjectModel(
                    id=f"project_{name.lower().replace(' ', '_')}",
                    name=name,
                    path=path,
                    **kwargs,
                )
                self._logger.info("Created project", project_id=project.id, name=name)
                return FlextResult.ok(project)
            except (ValueError, TypeError) as e:
                error_msg = f"Project creation failed: {e}"
                self._logger.exception("Project creation failed", error=error_msg)
                return FlextResult.fail(error_msg)

        def get_project(
            self, project_id: str
        ) -> FlextResult[FlextQualityModels.ProjectModel | None]:
            """Get project by ID - DELEGATES to repository (future)."""
            # TODO: Implement repository pattern for persistence
            self._logger.debug("Getting project", project_id=project_id)
            return FlextResult.ok(None)

    # =========================================================================
    # INNER SERVICE: AnalysisService - Single responsibility: Analysis lifecycle
    # =========================================================================

    class AnalysisService(FlextService[None]):
        """Service for analysis management - SOLID: Single Responsibility."""

        def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
            """Initialize analysis service."""
            super().__init__()
            self._config = config
            self._logger = logger

        @override
        def execute(self, data: object) -> FlextResult[None]:
            """Execute analysis service."""
            return FlextResult[None].ok(None)

        def create_analysis(
            self,
            project_id: str,
            **kwargs: object,
        ) -> FlextResult[FlextQualityModels.AnalysisModel]:
            """Create new analysis - DELEGATES to FlextQualityModels for validation."""
            try:
                analysis = FlextQualityModels.AnalysisModel(
                    id=f"analysis_{project_id}",
                    project_id=project_id,
                    status=FlextQualityModels.AnalysisStatus.QUEUED,
                    **kwargs,
                )
                self._logger.info("Created analysis", analysis_id=analysis.id)
                return FlextResult.ok(analysis)
            except (ValueError, TypeError) as e:
                error_msg = f"Analysis creation failed: {e}"
                self._logger.exception("Analysis creation failed", error=error_msg)
                return FlextResult.fail(error_msg)

        def get_analysis(
            self, analysis_id: str
        ) -> FlextResult[FlextQualityModels.AnalysisModel | None]:
            """Get analysis by ID - DELEGATES to repository (future)."""
            self._logger.debug("Getting analysis", analysis_id=analysis_id)
            return FlextResult.ok(None)

    # =========================================================================
    # INNER SERVICE: IssueService - Single responsibility: Issue lifecycle
    # =========================================================================

    class IssueService(FlextService[None]):
        """Service for issue management - SOLID: Single Responsibility."""

        def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
            """Initialize issue service."""
            super().__init__()
            self._config = config
            self._logger = logger

        @override
        def execute(self, data: object) -> FlextResult[None]:
            """Execute issue service."""
            return FlextResult[None].ok(None)

        def create_issue(
            self,
            analysis_id: str,
            severity: str,
            issue_type: str,
            file_path: str,
            message: str,
            **kwargs: object,
        ) -> FlextResult[FlextQualityModels.IssueModel]:
            """Create quality issue - DELEGATES to FlextQualityModels for validation."""
            try:
                # Validate enums through FlextQualityModels
                FlextQualityModels.IssueSeverity(severity)
                FlextQualityModels.IssueType(issue_type)

                issue = FlextQualityModels.IssueModel(
                    id=f"issue_{analysis_id}",
                    analysis_id=analysis_id,
                    severity=severity,
                    issue_type=issue_type,
                    file_path=file_path,
                    message=message,
                    **kwargs,
                )
                self._logger.info("Created issue", issue_id=issue.id, severity=severity)
                return FlextResult.ok(issue)
            except (ValueError, TypeError) as e:
                error_msg = f"Issue creation failed: {e}"
                self._logger.exception("Issue creation failed", error=error_msg)
                return FlextResult.fail(error_msg)

        def get_issues(
            self, analysis_id: str
        ) -> FlextResult[list[FlextQualityModels.IssueModel]]:
            """Get issues for analysis - DELEGATES to repository (future)."""
            self._logger.debug("Getting issues", analysis_id=analysis_id)
            return FlextResult.ok([])

    # =========================================================================
    # INNER SERVICE: ReportService - Single responsibility: Report lifecycle
    # =========================================================================

    class ReportService(FlextService[None]):
        """Service for report management - SOLID: Single Responsibility."""

        def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
            """Initialize report service."""
            super().__init__()
            self._config = config
            self._logger = logger

        @override
        def execute(self, data: object) -> FlextResult[None]:
            """Execute report service."""
            return FlextResult[None].ok(None)

        def create_report(
            self,
            analysis_id: str,
            format_type: str = "HTML",
            **kwargs: object,
        ) -> FlextResult[FlextQualityModels.ReportModel]:
            """Create quality report - DELEGATES to FlextQualityModels for validation."""
            try:
                report = FlextQualityModels.ReportModel(
                    id=f"report_{analysis_id}",
                    analysis_id=analysis_id,
                    format_type=format_type,
                    **kwargs,
                )
                self._logger.info(
                    "Created report", report_id=report.id, format=format_type
                )
                return FlextResult.ok(report)
            except (ValueError, TypeError) as e:
                error_msg = f"Report creation failed: {e}"
                self._logger.exception("Report creation failed", error=error_msg)
                return FlextResult.fail(error_msg)

        def get_report(
            self, report_id: str
        ) -> FlextResult[FlextQualityModels.ReportModel | None]:
            """Get report by ID - DELEGATES to repository (future)."""
            self._logger.debug("Getting report", report_id=report_id)
            return FlextResult.ok(None)


__all__ = [
    "FlextQualityServices",
]
