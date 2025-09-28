"""Quality domain services following flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextProtocols,
    FlextResult,
    FlextTypes,
)
from flext_quality.entities import (
    FlextQualityAnalysis,
    FlextQualityIssue,
    FlextQualityProject,
    FlextQualityReport,
)
from flext_quality.external_backend import ExternalBackend
from flext_quality.value_objects import IssueSeverity, IssueType

logger = FlextLogger(__name__)

# Use flext-core protocols instead of local definitions
QualityServiceProtocol = FlextProtocols.Domain.Service
QualityAnalysisServiceProtocol = FlextProtocols.Application.Handler["str", "object"]
QualityProjectServiceProtocol = FlextProtocols.Domain.Service


class FlextQualityServices:
    """Unified quality services class following FLEXT pattern - ZERO DUPLICATION.

    Single responsibility: Quality domain services orchestration
    Contains all quality services as nested classes with shared resources.
    """

    @override
    def __init__(self, **data: object) -> None:
        """Initialize quality services with dependency injection."""
        super().__init__(**data)  # Pass data to parent
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Shared storage for all services
        self._projects: dict[str, FlextQualityProject] = {}
        self._issues: dict[str, FlextQualityIssue] = {}
        self._analyses: dict[str, FlextQualityAnalysis] = {}
        self._reports: dict[str, FlextQualityReport] = {}

    def get_projects(self) -> dict[str, FlextQualityProject]:
        """Get projects dictionary."""
        return self._projects

    def set_project(self, name: str, project: FlextQualityProject) -> None:
        """Set a project in the projects dictionary."""
        self._projects[name] = project

    def get_issues(self) -> dict[str, FlextQualityIssue]:
        """Get issues dictionary."""
        return self._issues

    def set_issue(self, issue_id: str, issue: FlextQualityIssue) -> None:
        """Set an issue in the issues dictionary."""
        self._issues[issue_id] = issue

    def get_analyses(self) -> dict[str, FlextQualityAnalysis]:
        """Get analyses dictionary."""
        return self._analyses

    def set_analysis(self, analysis_id: str, analysis: FlextQualityAnalysis) -> None:
        """Set an analysis in the analyses dictionary."""
        self._analyses[analysis_id] = analysis

    def get_reports(self) -> dict[str, FlextQualityReport]:
        """Get reports dictionary."""
        return self._reports

    def set_report(self, report_id: str, report: FlextQualityReport) -> None:
        """Set a report in the reports dictionary."""
        self._reports[report_id] = report

    # =============================================================================
    # NESTED SERVICE CLASSES - All quality services consolidated
    # =============================================================================

    class ProjectService:
        """Service for managing quality projects using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            self._parent = parent
            self._logger = parent._logger

        async def create_project(
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
        ) -> FlextResult[FlextQualityProject]:
            """Create a new quality project."""
            try:
                # Create project entity
                project = FlextQualityProject(
                    name=name,
                    project_path=str(project_path),
                    repository_url=repository_url,
                    config_path=str(config_path) if config_path else None,
                    language=language,
                    auto_analyze=auto_analyze,
                )

                # Store project in shared storage
                self._parent.set_project(name, project)
                self._logger.info("Created project: %s", project.name)
                return FlextResult[FlextQualityProject].ok(project)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to create project")
                return FlextResult[FlextQualityProject].fail(
                    f"Failed to create project: {e}",
                )

    class IssueService:
        """Service for managing quality issues using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            self._parent = parent
            self._logger = parent._logger

        async def create_issue(
            self,
            analysis_id: str,
            file_path: str,
            line_number: int,
            column_number: int | None,
            severity: IssueSeverity,
            issue_type: IssueType,
            message: str,
            rule: str | None = None,
            _source: str = "ruff",
        ) -> FlextResult[FlextQualityIssue]:
            """Create a new quality issue."""
            try:
                # Create issue ID
                issue_id = f"{analysis_id}:{file_path}:{line_number}"

                # Create quality issue
                issue = FlextQualityIssue(
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

                self._logger.debug(f"Created quality issue: {issue_id}")
                return FlextResult[FlextQualityIssue].ok(issue)
            except Exception as e:
                self._logger.exception("Failed to create issue")
                return FlextResult[FlextQualityIssue].fail(
                    f"Failed to create issue: {e}",
                )

        async def get_issues_by_analysis(
            self,
            analysis_id: str,
        ) -> FlextResult[list[FlextQualityIssue]]:
            """Get all issues for a specific analysis."""
            try:
                issues = [
                    issue
                    for issue in self._parent.get_issues().values()
                    if issue.analysis_id == analysis_id
                ]
                return FlextResult[list[FlextQualityIssue]].ok(issues)
            except Exception as e:
                self._logger.exception(
                    "Failed to get issues for analysis %s",
                    analysis_id,
                )
                return FlextResult[list[FlextQualityIssue]].fail(
                    f"Failed to get issues: {e}",
                )

        async def get_issue(
            self,
            issue_id: str,
        ) -> FlextResult[FlextQualityIssue | None]:
            """Get a specific issue by ID."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                return FlextResult[FlextQualityIssue | None].ok(issue)
            except Exception as e:
                self._logger.exception("Failed to get issue %s", issue_id)
                return FlextResult[FlextQualityIssue | None].fail(
                    f"Failed to get issue: {e}",
                )

        async def suppress_issue(
            self,
            issue_id: str,
            reason: str,
        ) -> FlextResult[FlextQualityIssue]:
            """Suppress a specific issue."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                if not issue:
                    return FlextResult[FlextQualityIssue].fail(
                        f"Issue not found: {issue_id}",
                    )

                suppressed_issue = issue.suppress(reason)
                self._parent.set_issue(issue_id, suppressed_issue)

                self._logger.debug(f"Suppressed issue: {issue_id}")
                return FlextResult[FlextQualityIssue].ok(suppressed_issue)
            except Exception as e:
                self._logger.exception("Failed to suppress issue %s", issue_id)
                return FlextResult[FlextQualityIssue].fail(
                    f"Failed to suppress issue: {e}",
                )

        async def unsuppress_issue(
            self,
            issue_id: str,
        ) -> FlextResult[FlextQualityIssue]:
            """Unsuppress a quality issue."""
            try:
                issue = self._parent.get_issues().get(issue_id)
                if not issue:
                    return FlextResult[FlextQualityIssue].fail("Issue not found")

                # Update issue to unsuppressed status using model_copy
                updated_issue = issue.model_copy(
                    update={"is_suppressed": "False", "suppression_reason": "None"},
                )

                self._parent.set_issue(issue_id, updated_issue)
                self._logger.info("Issue unsuppressed: %s", issue_id)
                return FlextResult[FlextQualityIssue].ok(updated_issue)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to unsuppress issue")
                return FlextResult[FlextQualityIssue].fail(
                    f"Failed to unsuppress issue: {e}",
                )

    class AnalysisService:
        """Service for managing quality analyses using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            self._parent = parent
            self._logger = parent._logger

        async def create_analysis(
            self,
            project_id: str,
            config: FlextTypes.Core.Dict | None = None,
        ) -> FlextResult[FlextQualityAnalysis]:
            """Create a new quality analysis."""
            try:
                analysis = FlextQualityAnalysis(
                    project_id=project_id,
                    analysis_config=config or {},
                )

                # Store analysis in shared storage
                analysis_id = (
                    f"{project_id}_analysis_{len(self._parent.get_analyses())}"
                )
                self._parent.set_analysis(analysis_id, analysis)
                self._logger.info("Created analysis: %s", analysis_id)
                return FlextResult[FlextQualityAnalysis].ok(analysis)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to create analysis")
                return FlextResult[FlextQualityAnalysis].fail(
                    f"Failed to create analysis: {e}",
                )

        async def get_analyses_by_project(
            self,
            project_id: str,
        ) -> FlextResult[list[FlextQualityAnalysis]]:
            """Get all analyses for a project."""
            try:
                analyses = [
                    analysis
                    for analysis in self._parent.get_analyses().values()
                    if analysis.project_id == project_id
                ]
                return FlextResult[list[FlextQualityAnalysis]].ok(analyses)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to list analyses")
                return FlextResult[list[FlextQualityAnalysis]].fail(
                    f"Failed to list analyses: {e}",
                )

    class ReportService:
        """Service for managing quality reports using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with parent reference."""
            self._parent = parent
            self._logger = parent._logger

        async def create_report(
            self,
            analysis_id: str,
            format_type: str,
            content: str,
            file_path: str | None = None,
            _metadata: FlextTypes.Core.Dict | None = None,
        ) -> FlextResult[FlextQualityReport]:
            """Create a new quality report."""
            try:
                report = FlextQualityReport(
                    analysis_id=analysis_id,
                    report_type=format_type,
                    report_format="summary",
                    report_path=file_path,
                    report_size_bytes=len(content.encode()) if content else 0,
                )

                # Store report in shared storage
                report_id = f"{analysis_id}_report_{len(self._parent.get_reports())}"
                self._parent.set_report(report_id, report)
                self._logger.info("Created report: %s", report_id)
                return FlextResult[FlextQualityReport].ok(report)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to create report")
                return FlextResult[FlextQualityReport].fail(
                    f"Failed to create report: {e}",
                )

        async def get_reports_by_analysis(
            self,
            analysis_id: str,
        ) -> FlextResult[list[FlextQualityReport]]:
            """Get all reports for an analysis."""
            try:
                reports = [
                    report
                    for report in self._parent.get_reports().values()
                    if report.analysis_id == analysis_id
                ]
                return FlextResult[list[FlextQualityReport]].ok(reports)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to list reports")
                return FlextResult[list[FlextQualityReport]].fail(
                    f"Failed to list reports: {e}",
                )

        async def delete_report(self, report_id: str) -> FlextResult[bool]:
            """Delete a quality report."""
            try:
                reports = self._parent.get_reports()
                if report_id in reports:
                    del reports[report_id]
                    self._logger.info("Report deleted successfully: %s", report_id)
                    success = True
                    return FlextResult[bool].ok(success)
                return FlextResult[bool].fail("Report not found")
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to delete report")
                return FlextResult[bool].fail(f"Failed to delete report: {e}")

    class ExternalAnalysisService:
        """Service for external backend analysis using flext-core patterns."""

        @override
        def __init__(self, parent: FlextQualityServices) -> None:
            """Initialize service with external backend."""
            self._parent = parent
            self._backend = ExternalBackend()
            self._logger = parent._logger

        async def analyze_with_backend(
            self,
            code: str,
            file_path: Path | None = None,
            backend_tool: str = "ruff",
        ) -> FlextResult[FlextTypes.Core.Dict]:
            """Analyze code using external backend tools."""
            try:
                self._logger.info("Running %s analysis", backend_tool)
                result: FlextResult[object] = self._backend.analyze(
                    code, file_path, tool=backend_tool
                )
                return FlextResult[FlextTypes.Core.Dict].ok(result)
            except (RuntimeError, ValueError, TypeError) as e:
                self._logger.exception("Failed to analyze with external backend")
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Failed to analyze with external backend {e}",
                )

    # =============================================================================
    # SERVICE FACTORY METHODS
    # =============================================================================

    def get_project_service(self: object) -> ProjectService:
        """Get project service instance."""
        return self.ProjectService(self)

    def get_issue_service(self: object) -> IssueService:
        """Get issue service instance."""
        return self.IssueService(self)

    def get_analysis_service(self: object) -> AnalysisService:
        """Get analysis service instance."""
        return self.AnalysisService(self)

    def get_report_service(self: object) -> ReportService:
        """Get report service instance."""
        return self.ReportService(self)

    def get_external_analysis_service(self: object) -> ExternalAnalysisService:
        """Get external analysis service instance."""
        return self.ExternalAnalysisService(self)


# ExternalAnalysisService removed for 1.0 production readiness
# Use FlextQualityServices.get_external_analysis_service() directly

# Legacy compatibility classes removed for 1.0 production readiness
# Use FlextQualityServices directly instead of deprecated facade classes


# FlextQualityReportService removed for 1.0 production readiness

# Aliases removed for 1.0 production readiness
# Use FlextQualityServices directly


# Export all classes via __all__
__all__ = [
    # Unified services class - main entry point
    "FlextQualityServices",
]
