"""Application services for FLEXT-QUALITY v0.7.0.

CONSOLIDATED: Single class containing ALL quality services following FLEXT patterns.
Inherits from FlextDomainService for enterprise-grade service foundation.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from uuid import uuid4

from flext_core import FlextDomainService, FlextEntityId, FlextResult

from flext_quality.entities import (
    AnalysisStatus,
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
)
from flext_quality.external_backend import ExternalBackend
from flext_quality.typings import FlextTypes
from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
)


class FlextQualityServices(FlextDomainService[FlextResult[object]]):
    """Single consolidated class containing ALL quality services.
    
    Consolidates ALL service operations into one class following FLEXT patterns.
    Individual service methods provide organization while maintaining single entry point.
    """
    
    def __init__(self) -> None:
        """Initialize consolidated services with repositories."""
        super().__init__()
        # In-memory repositories for all entities
        self._projects: dict[str, QualityProject] = {}
        self._analyses: dict[str, QualityAnalysis] = {}
        self._issues: dict[str, QualityIssue] = {}
        self._reports: dict[str, QualityReport] = {}
    
    # =============================================================================
    # PROJECT SERVICE METHODS
    # =============================================================================
    
    async def create_project(
        self,
        name: str,
        project_path: str,
        repository_url: str | None = None,
        config_path: str | None = None,
        language: str = "python",
        *,
        auto_analyze: bool = True,
        min_coverage: float = 95.0,
        max_complexity: int = 10,
        max_duplication: float = 5.0,
    ) -> FlextResult[QualityProject]:
        """Create a new quality project.

        Args:
            name: Project name
            project_path: Path to the project directory
            repository_url: Optional repository URL
            config_path: Optional configuration file path
            language: Project language (default: python)
            auto_analyze: Whether to auto-analyze on changes
            min_coverage: Minimum coverage threshold
            max_complexity: Maximum complexity threshold
            max_duplication: Maximum duplication threshold

        Returns:
            FlextResult containing the created project or error

        """
        try:
            project = QualityProject(
                id=FlextEntityId(str(uuid4())),
                name=name,
                project_path=project_path,
                repository_url=repository_url,
                config_path=config_path,
                language=language,
                auto_analyze=auto_analyze,
                min_coverage=min_coverage,
                max_complexity=max_complexity,
                max_duplication=max_duplication,
            )

            self._projects[str(project.id)] = project
            return FlextResult[QualityProject].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityProject].fail(f"Failed to create project {e}")

    async def get_project(
        self,
        project_id: str,
    ) -> FlextResult[QualityProject]:
        """Get a project by ID.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing the project or error

        """
        try:
            project = self._projects.get(project_id)
            if project is None:
                return FlextResult[QualityProject].fail(
                    f"Project not found: {project_id}"
                )
            return FlextResult[QualityProject].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityProject].fail(f"Failed to get project {e}")

    async def list_projects(self) -> FlextResult[list[QualityProject]]:
        """List all projects.

        Returns:
            FlextResult containing list of projects or error

        """
        try:
            projects = list(self._projects.values())
            return FlextResult[list[QualityProject]].ok(projects)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[list[QualityProject]].fail(
                f"Failed to list projects {e}"
            )

    async def update_project(
        self,
        project_id: str,
        updates: dict[str, object],
    ) -> FlextResult[QualityProject]:
        """Update an existing project.

        Args:
            project_id: Project unique identifier
            updates: Dictionary of fields to update

        Returns:
            FlextResult containing the updated project or error

        """
        try:
            project = self._projects.get(project_id)
            if not project:
                return FlextResult[QualityProject].fail("Project not found")

            # Use model_copy to create updated version (immutable pattern)
            updated_project = project.model_copy(update=updates)

            # Store the updated project
            self._projects[project_id] = updated_project

            return FlextResult[QualityProject].ok(updated_project)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityProject].fail(f"Failed to update project: {e}")

    async def delete_project(self, project_id: str) -> FlextResult[bool]:
        """Delete a project.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing success status or error

        """
        try:
            if project_id in self._projects:
                del self._projects[project_id]
                success = True
                return FlextResult[bool].ok(success)
            return FlextResult[bool].fail("Project not found")
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to delete project: {e}")

    # =============================================================================
    # ANALYSIS SERVICE METHODS
    # =============================================================================

    async def create_analysis(
        self,
        project_id: str,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: FlextTypes.Core.JsonDict | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Create a new quality analysis.

        Args:
            project_id: Project unique identifier
            commit_hash: Optional commit hash
            branch: Optional branch name
            pull_request_id: Optional pull request ID
            analysis_config: Optional analysis configuration

        Returns:
            FlextResult containing the created analysis or error

        """
        try:
            analysis = QualityAnalysis(
                id=FlextEntityId(str(uuid4())),
                project_id=FlextEntityId(project_id),
                commit_hash=commit_hash,
                branch=branch,
                pull_request_id=pull_request_id,
                status=AnalysisStatus.PENDING,
                analysis_config=analysis_config or {},
            )

            self._analyses[str(analysis.id)] = analysis
            return FlextResult[QualityAnalysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityAnalysis].fail(f"Failed to create analysis {e}")

    async def get_analysis(self, analysis_id: str) -> FlextResult[QualityAnalysis]:
        """Get analysis by ID.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing the analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if analysis is None:
                return FlextResult[QualityAnalysis].fail(
                    f"Analysis not found: {analysis_id}"
                )
            return FlextResult[QualityAnalysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityAnalysis].fail(f"Failed to get analysis {e}")

    async def update_analysis_status(
        self,
        analysis_id: str,
        status: AnalysisStatus,
        error_message: str | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis status.

        Args:
            analysis_id: Analysis unique identifier
            status: New analysis status
            error_message: Optional error message

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult[QualityAnalysis].fail("Analysis not found")

            # Use model_copy for immutable updates
            updated_analysis = analysis.model_copy(
                update={"status": status, "error_message": error_message}
            )

            self._analyses[analysis_id] = updated_analysis
            return FlextResult[QualityAnalysis].ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityAnalysis].fail(f"Failed to update analysis: {e}")

    # =============================================================================
    # ISSUE SERVICE METHODS
    # =============================================================================

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
        source: str = "ruff",
    ) -> FlextResult[QualityIssue]:
        """Create a new quality issue.

        Args:
            analysis_id: Analysis unique identifier
            file_path: File path where issue was found
            line_number: Line number of the issue
            column_number: Optional column number
            severity: Issue severity level
            issue_type: Type of quality issue
            message: Issue description message
            rule: Optional rule that triggered this issue
            source: Analysis backend that detected the issue

        Returns:
            FlextResult containing the created issue or error

        """
        try:
            issue = QualityIssue(
                id=FlextEntityId(str(uuid4())),
                analysis_id=FlextEntityId(analysis_id),
                file_path=file_path,
                line_number=line_number,
                column_number=column_number,
                severity=severity,
                issue_type=issue_type,
                message=message,
                rule=rule,
                source=source,
            )

            self._issues[str(issue.id)] = issue
            return FlextResult[QualityIssue].ok(issue)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityIssue].fail(f"Failed to create issue {e}")

    async def get_issues_for_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[QualityIssue]]:
        """Get all issues for an analysis.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of issues or error

        """
        try:
            issues = [
                issue
                for issue in self._issues.values()
                if str(issue.analysis_id) == analysis_id
            ]
            return FlextResult[list[QualityIssue]].ok(issues)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[list[QualityIssue]].fail(
                f"Failed to get issues for analysis {e}"
            )

    # =============================================================================
    # REPORT SERVICE METHODS
    # =============================================================================

    async def create_report(
        self,
        analysis_id: str,
        format_type: str,
        content: str,
        file_path: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> FlextResult[QualityReport]:
        """Create a new quality report.

        Args:
            analysis_id: Analysis unique identifier
            format_type: Report format (HTML, JSON, PDF)
            content: Report content
            file_path: Optional path to saved report file
            metadata: Optional report metadata

        Returns:
            FlextResult containing the created report or error

        """
        try:
            report = QualityReport(
                id=FlextEntityId(str(uuid4())),
                analysis_id=FlextEntityId(analysis_id),
                format_type=format_type,
                content=content,
                file_path=file_path,
                metadata=metadata or {},
            )

            self._reports[str(report.id)] = report
            return FlextResult[QualityReport].ok(report)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[QualityReport].fail(f"Failed to create report {e}")

    async def get_reports_for_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[QualityReport]]:
        """Get all reports for an analysis.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of reports or error

        """
        try:
            reports = [
                report
                for report in self._reports.values()
                if str(report.analysis_id) == analysis_id
            ]
            return FlextResult[list[QualityReport]].ok(reports)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[list[QualityReport]].fail(
                f"Failed to get reports for analysis {e}"
            )

    # =============================================================================
    # EXTERNAL ANALYSIS SERVICE METHODS
    # =============================================================================

    async def analyze_with_external_backend(
        self,
        code: str,
        file_path: Path | None = None,
        backend_tool: str = "ruff",
    ) -> FlextResult[dict[str, object]]:
        """Analyze code using external backend tools.

        Args:
            code: Source code to analyze
            file_path: Optional file path for context
            backend_tool: Backend tool to use (ruff, mypy, bandit, vulture)

        Returns:
            FlextResult containing analysis results or error

        """
        try:
            backend = ExternalBackend()
            result = backend.analyze(code, file_path, tool=backend_tool)
            return FlextResult[dict[str, object]].ok(result)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to analyze with external backend {e}"
            )


# Legacy compatibility facades (TEMPORARY - will be removed)
class FlextQualityProjectService(FlextQualityServices):
    """Legacy compatibility facade - DEPRECATED."""
    
    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityProjectService is deprecated; use FlextQualityServices directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityAnalysisService(FlextQualityServices):
    """Legacy compatibility facade - DEPRECATED."""
    
    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityAnalysisService is deprecated; use FlextQualityServices directly", 
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityIssueService(FlextQualityServices):
    """Legacy compatibility facade - DEPRECATED."""
    
    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityIssueService is deprecated; use FlextQualityServices directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityReportService(FlextQualityServices):
    """Legacy compatibility facade - DEPRECATED."""
    
    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityReportService is deprecated; use FlextQualityServices directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


# Additional legacy aliases for backward compatibility
QualityProjectService = FlextQualityProjectService
QualityAnalysisService = FlextQualityAnalysisService
QualityIssueService = FlextQualityIssueService
QualityReportService = FlextQualityReportService

# Legacy service implementations that were at the end of the original file
BasePortService = FlextQualityServices  # Base port service is now the consolidated services
AnalysisServiceImpl = FlextQualityServices
SecurityAnalyzerServiceImpl = FlextQualityServices  
LintingServiceImpl = FlextQualityServices
ReportGeneratorServiceImpl = FlextQualityServices