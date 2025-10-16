"""FLEXT Quality Services - Application services following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import (
    FlextBus,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextLogger,
    FlextProcessors,
    FlextRegistry,
    FlextResult,
    FlextService,
    FlextTypes,
)

from .external_backend import FlextQualityExternalBackend
from .models import FlextQualityModels


class FlextQualityServices:
    """Unified quality services class following FLEXT pattern - ZERO DUPLICATION.

    Single responsibility: Quality domain services orchestration
    Contains all quality services as nested classes with shared resources.
    """

    _container: FlextContainer
    _bus: FlextBus

    def __init__(self, **_data: object) -> None:
        """Initialize quality services with complete flext-core integration."""
        # Complete flext-core integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self.logger = FlextLogger(__name__)

        # Shared storage for all services
        self._projects: dict[str, FlextQualityModels.Project] = {}
        self._issues: dict[str, FlextQualityModels.Issue] = {}
        self._analyses: dict[str, FlextQualityModels.Analysis] = {}
        self._reports: dict[str, FlextQualityModels.Report] = {}

    def get_projects(self) -> dict[str, FlextQualityModels.Project]:
        """Get projects dictionary."""
        return self._projects

    def set_project(self, name: str, project: FlextQualityModels.Project) -> None:
        """Set a project in the projects dictionary."""
        self._projects[name] = project

    def get_issues(self) -> dict[str, FlextQualityModels.Issue]:
        """Get issues dictionary."""
        return self._issues

    def set_issue(self, issue_id: str, issue: FlextQualityModels.Issue) -> None:
        """Set an issue in the issues dictionary."""
        self._issues[issue_id] = issue

    def get_analyses(self) -> dict[str, FlextQualityModels.Analysis]:
        """Get analyses dictionary."""
        return self._analyses

    def set_analysis(
        self, analysis_id: str, analysis: FlextQualityModels.Analysis
    ) -> None:
        """Set an analysis in the analyses dictionary."""
        self._analyses[analysis_id] = analysis

    def get_reports(self) -> dict[str, FlextQualityModels.Report]:
        """Get reports dictionary."""
        return self._reports

    def set_report(self, report_id: str, report: FlextQualityModels.Report) -> None:
        """Set a report in the reports dictionary."""
        self._reports[report_id] = report

    # =============================================================================
    # NESTED SERVICE CLASSES - All quality services consolidated
    # =============================================================================

    class ProjectService(FlextService[None]):
        """Service for managing quality projects using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            super().__init__()
            self._parent = parent
            # Initialize logger directly for type safety
            self.logger = FlextLogger(__name__)

        @property
        def logger(self) -> FlextLogger:
            """Get logger with type narrowing."""
            if self.logger is None:
                msg = "Logger must be initialized"
                raise RuntimeError(msg)
            return self.logger

        @override
        def execute(self, data: object) -> FlextResult[None]:
            """Execute service operation - not used for this service type."""
            return FlextResult[None].fail(
                "ProjectService does not support execute operation"
            )

        def create_project(
            self,
            name: str,
            project_path: str,
            repository_url: str | None = None,
            config_path: str | None = None,
            language: str = "python",
            *,
            auto_analyze: bool = True,
            _min_coverage: float = 95.0,
            _max_complexity: int = 10,
            _max_duplication: float = 5.0,
        ) -> FlextResult[FlextQualityModels.Project]:
            """Create a new quality project."""
            try:
                # Create project entity
                project = FlextQualityModels.Project(
                    name=name,
                    project_path=str(project_path),
                    repository_url=repository_url,
                    config_path=str(config_path) if config_path else None,
                    language=language,
                    auto_analyze=auto_analyze,
                )

                # Store project in shared storage
                self._parent.set_project(name, project)
                self.logger.info("Created project: %s", project.name)
                return FlextResult[FlextQualityModels.Project].ok(project)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to create project")
                return FlextResult[FlextQualityModels.Project].fail(
                    f"Failed to create project: {e}",
                )

    class IssueService(FlextService[None]):
        """Service for managing quality issues using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            super().__init__()
            self._parent = parent
            # Initialize logger directly for type safety
            self.logger = FlextLogger(__name__)

        @property
        def logger(self) -> FlextLogger:
            """Get logger with type narrowing."""
            if self.logger is None:
                msg = "Logger must be initialized"
                raise RuntimeError(msg)
            return self.logger

        def create_issue(
            self,
            analysis_id: str,
            file_path: str,
            line_number: int,
            column_number: int | None,
            severity: str,
            issue_type: str,
            message: str,
            rule: str | None = None,
            _source: str = "ruff",
        ) -> FlextResult[FlextQualityModels.Issue]:
            """Create a new quality issue."""
            try:
                # Create issue ID
                issue_id = f"{analysis_id}:{file_path}:{line_number}"

                # Create quality issue
                issue = FlextQualityModels.Issue(
                    analysis_id=analysis_id,
                    issue_type=issue_type,
                    severity=severity,
                    rule_id=rule or "unknown",
                    file_path=file_path,
                    line_number=line_number,
                    column_number=column_number,
                    message=message,
                )

                # Store issue in shared storage
                self._parent.set_issue(issue_id, issue)

                self.logger.debug(f"Created quality issue: {issue_id}")
                return FlextResult[FlextQualityModels.Issue].ok(issue)
            except Exception as e:
                self.logger.exception("Failed to create issue")
                return FlextResult[FlextQualityModels.Issue].fail(
                    f"Failed to create issue: {e}",
                )

        def get_issues_by_analysis(
            self,
            analysis_id: str,
        ) -> FlextResult[list[FlextQualityModels.Issue]]:
            """Get all issues for a specific analysis."""
            try:
                issues = [
                    issue
                    for issue in self._parent.get_issues().values()
                    if issue.analysis_id == analysis_id
                ]
                return FlextResult[list[FlextQualityModels.Issue]].ok(issues)
            except Exception as e:
                self.logger.exception(
                    "Failed to get issues for analysis %s",
                    analysis_id,
                )
                return FlextResult[list[FlextQualityModels.Issue]].fail(
                    f"Failed to get issues: {e}",
                )

        def get_issue(
            self,
            issue_id: str,
        ) -> FlextResult[FlextQualityModels.Issue | None]:
            """Get a specific issue by ID."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                return FlextResult[FlextQualityModels.Issue | None].ok(issue)
            except Exception as e:
                self.logger.exception(f"Failed to get issue {issue_id}")
                return FlextResult[FlextQualityModels.Issue | None].fail(
                    f"Failed to get issue: {e}",
                )

        def suppress_issue(
            self,
            issue_id: str,
            reason: str,
        ) -> FlextResult[FlextQualityModels.Issue]:
            """Suppress a specific issue."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                if not issue:
                    return FlextResult[FlextQualityModels.Issue].fail(
                        f"Issue not found: {issue_id}",
                    )

                suppressed_issue = issue.suppress(reason)
                self._parent.set_issue(issue_id, suppressed_issue)

                self.logger.debug(f"Suppressed issue: {issue_id}")
                return FlextResult[FlextQualityModels.Issue].ok(suppressed_issue)
            except Exception as e:
                self.logger.exception(f"Failed to suppress issue {issue_id}")
                return FlextResult[FlextQualityModels.Issue].fail(
                    f"Failed to suppress issue: {e}",
                )

        def unsuppress_issue(
            self,
            issue_id: str,
        ) -> FlextResult[FlextQualityModels.Issue]:
            """Unsuppress a quality issue."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                if not issue:
                    return FlextResult[FlextQualityModels.Issue].fail("Issue not found")

                # Update issue to unsuppressed status using model_copy
                updated_issue = issue.model_copy(
                    update={"is_suppressed": "False", "suppression_reason": "None"},
                )

                self._parent.set_issue(issue_id, updated_issue)
                self.logger.info("Issue unsuppressed: %s", issue_id)
                return FlextResult[FlextQualityModels.Issue].ok(updated_issue)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to unsuppress issue")
                return FlextResult[FlextQualityModels.Issue].fail(
                    f"Failed to unsuppress issue: {e}",
                )

    class AnalysisService(FlextService[None]):
        """Service for managing quality analyses using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            super().__init__()
            self._parent = parent
            # Initialize logger directly for type safety
            self.logger = FlextLogger(__name__)

        @property
        def logger(self) -> FlextLogger:
            """Get logger with type narrowing."""
            if self.logger is None:
                msg = "Logger must be initialized"
                raise RuntimeError(msg)
            return self.logger

        def create_analysis(
            self,
            project_id: str,
            config: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextQualityModels.Analysis]:
            """Create a new quality analysis."""
            try:
                analysis = FlextQualityModels.Analysis(
                    project_id=project_id,
                    analysis_config=config or {},
                )

                # Store analysis in shared storage
                analysis_id = (
                    f"{project_id}_analysis_{len(self._parent.get_analyses())}"
                )
                self._parent.set_analysis(analysis_id, analysis)
                self.logger.info("Created analysis: %s", analysis_id)
                return FlextResult[FlextQualityModels.Analysis].ok(analysis)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to create analysis")
                return FlextResult[FlextQualityModels.Analysis].fail(
                    f"Failed to create analysis: {e}",
                )

        def get_analyses_by_project(
            self,
            project_id: str,
        ) -> FlextResult[list[FlextQualityModels.Analysis]]:
            """Get all analyses for a project."""
            try:
                analyses = [
                    analysis
                    for analysis in self._parent.get_analyses().values()
                    if analysis.project_id == project_id
                ]
                return FlextResult[list[FlextQualityModels.Analysis]].ok(analyses)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to list analyses")
                return FlextResult[list[FlextQualityModels.Analysis]].fail(
                    f"Failed to list analyses: {e}",
                )

    class ReportService(FlextService[None]):
        """Service for managing quality reports using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            super().__init__()
            self._parent = parent
            # Initialize logger directly for type safety
            self.logger = FlextLogger(__name__)

        @property
        def logger(self) -> FlextLogger:
            """Get logger with type narrowing."""
            if self.logger is None:
                msg = "Logger must be initialized"
                raise RuntimeError(msg)
            return self.logger

        def create_report(
            self,
            analysis_id: str,
            format_type: str,
            content: str,
            file_path: str | None = None,
            _metadata: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextQualityModels.Report]:
            """Create a new quality report."""
            try:
                report = FlextQualityModels.Report(
                    analysis_id=analysis_id,
                    report_type=format_type,
                    report_format="summary",
                    report_path=file_path,
                    report_size_bytes=len(content.encode()) if content else 0,
                )

                # Store report in shared storage
                report_id = f"{analysis_id}_report_{len(self._parent.get_reports())}"
                self._parent.set_report(report_id, report)
                self.logger.info("Created report: %s", report_id)
                return FlextResult[FlextQualityModels.Report].ok(report)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to create report")
                return FlextResult[FlextQualityModels.Report].fail(
                    f"Failed to create report: {e}",
                )

        def get_reports_by_analysis(
            self,
            analysis_id: str,
        ) -> FlextResult[list[FlextQualityModels.Report]]:
            """Get all reports for an analysis."""
            try:
                reports = [
                    report
                    for report in self._parent.get_reports().values()
                    if report.analysis_id == analysis_id
                ]
                return FlextResult[list[FlextQualityModels.Report]].ok(reports)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to list reports")
                return FlextResult[list[FlextQualityModels.Report]].fail(
                    f"Failed to list reports: {e}",
                )

        def delete_report(self, report_id: str) -> FlextResult[bool]:
            """Delete a quality report."""
            try:
                reports = self._parent.get_reports()
                if report_id in reports:
                    del reports[report_id]
                    self.logger.info("Report deleted successfully: %s", report_id)
                    success = True
                    return FlextResult[bool].ok(success)
                return FlextResult[bool].fail("Report not found")
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to delete report")
                return FlextResult[bool].fail(f"Failed to delete report: {e}")

    class ExternalAnalysisService(FlextService[None]):
        """Service for external backend analysis using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with external backend."""
            super().__init__()
            self._parent = parent
            self._backend = FlextQualityExternalBackend()
            # Initialize logger directly for type safety
            self.logger = FlextLogger(__name__)

        @property
        def logger(self) -> FlextLogger:
            """Get logger with type narrowing."""
            if self.logger is None:
                msg = "Logger must be initialized"
                raise RuntimeError(msg)
            return self.logger

        def analyze_with_backend(
            self,
            code: str,
            file_path: Path | None = None,
            backend_tool: str = "ruff",
        ) -> FlextResult[FlextTypes.Dict]:
            """Analyze code using external backend tools."""
            try:
                self.logger.info("Running %s analysis", backend_tool)
                # analyze() returns dict[str, object] directly, not FlextResult
                result_dict: FlextTypes.Dict = self._backend.analyze(
                    code, file_path, tool=backend_tool
                )
                return FlextResult[FlextTypes.Dict].ok(result_dict)
            except (RuntimeError, ValueError, TypeError) as e:
                self.logger.exception("Failed to analyze with external backend")
                return FlextResult[FlextTypes.Dict].fail(
                    f"Failed to analyze with external backend {e}",
                )

    # =============================================================================
    # SERVICE FACTORY METHODS
    # =============================================================================

    def get_project_service(self) -> ProjectService:
        """Get project service instance."""
        return self.ProjectService(self)

    def get_issue_service(self) -> IssueService:
        """Get issue service instance."""
        return self.IssueService(self)

    def get_analysis_service(self) -> AnalysisService:
        """Get analysis service instance."""
        return self.AnalysisService(self)

    def get_report_service(self) -> ReportService:
        """Get report service instance."""
        return self.ReportService(self)

    def get_external_analysis_service(self) -> ExternalAnalysisService:
        """Get external analysis service instance."""
        return self.ExternalAnalysisService(self)


# ExternalAnalysisService removed for 1.0 production readiness
# Use FlextQualityServices.get_external_analysis_service() directly

# Legacy compatibility classes removed for 1.0 production readiness
# Use FlextQualityServices directly instead of deprecated facade classes


# FlextQualityModels.QualityReportService removed for 1.0 production readiness

# Aliases removed for 1.0 production readiness
# Use FlextQualityServices directly


# Export all classes via __all__
__all__ = [
    # Unified services class - main entry point
    "FlextQualityServices",
]
