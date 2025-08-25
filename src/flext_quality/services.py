"""Application services for FLEXT-QUALITY v0.7.0.

Services following flext-cli patterns with multiple service classes per module.
Uses working flext-core imports: FlextResult, get_logger.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from uuid import uuid4

from flext_core import FlextProtocols, FlextResult, get_logger

from flext_quality.entities import (
    FlextAnalysisStatus,
    FlextQualityAnalysis,
    FlextQualityIssue,
    FlextQualityProject,
    FlextQualityReport,
)
from flext_quality.external_backend import ExternalBackend
from flext_quality.typings import FlextTypes
from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
)

logger = get_logger(__name__)

# Use flext-core protocols instead of local definitions
QualityServiceProtocol = FlextProtocols.Domain.Service
QualityAnalysisServiceProtocol = FlextProtocols.Application.Handler[str, object]
QualityProjectServiceProtocol = FlextProtocols.Domain.Service


class BasicQualityProjectService:
    """Service for managing quality projects using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._projects: dict[str, FlextQualityProject] = {}
        self._logger = get_logger(__name__)

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
    ) -> FlextResult[FlextQualityProject]:
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
            self._logger.info(f"Creating project: {name}")

            project = FlextQualityProject(
                id=str(uuid4()),
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
            self._logger.info(f"Project created successfully: {project.id}")
            return FlextResult[FlextQualityProject].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create project")
            return FlextResult[FlextQualityProject].fail(f"Failed to create project {e}")

    async def get_project(self, project_id: str) -> FlextResult[FlextQualityProject]:
        """Get a project by ID.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing the project or error

        """
        try:
            project = self._projects.get(project_id)
            if project is None:
                return FlextResult[FlextQualityProject].fail(
                    f"Project not found: {project_id}"
                )
            return FlextResult[FlextQualityProject].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get project")
            return FlextResult[FlextQualityProject].fail(f"Failed to get project {e}")

    async def list_projects(self) -> FlextResult[list[FlextQualityProject]]:
        """List all projects.

        Returns:
            FlextResult containing list of projects or error

        """
        try:
            projects = list(self._projects.values())
            return FlextResult[list[FlextQualityProject]].ok(projects)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to list projects")
            return FlextResult[list[FlextQualityProject]].fail(
                f"Failed to list projects {e}"
            )

    async def update_project(
        self,
        project_id: str,
        updates: dict[str, object],
    ) -> FlextResult[FlextQualityProject]:
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
                return FlextResult[FlextQualityProject].fail("Project not found")

            # Use model_copy to create updated version (immutable pattern)
            updated_project = project.model_copy(update=updates)

            # Store the updated project
            self._projects[project_id] = updated_project

            self._logger.info(f"Project updated successfully: {project_id}")
            return FlextResult[FlextQualityProject].ok(updated_project)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to update project")
            return FlextResult[FlextQualityProject].fail(f"Failed to update project: {e}")

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
                self._logger.info(f"Project deleted successfully: {project_id}")
                success = True
                return FlextResult[bool].ok(success)
            return FlextResult[bool].fail("Project not found")
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to delete project")
            return FlextResult[bool].fail(f"Failed to delete project: {e}")


class BasicQualityAnalysisService:
    """Service for managing quality analyses using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._analyses: dict[str, FlextQualityAnalysis] = {}
        self._logger = get_logger(__name__)

    async def create_analysis(
        self,
        project_id: str,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: FlextTypes.Core.JsonDict | None = None,
    ) -> FlextResult[FlextQualityAnalysis]:
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
            self._logger.info(f"Creating analysis for project: {project_id}")

            analysis = FlextQualityAnalysis(
                id=str(uuid4()),
                project_id=project_id,
                commit_hash=commit_hash,
                branch=branch,
                pull_request_id=pull_request_id,
                status=FlextAnalysisStatus.QUEUED,
                analysis_config=analysis_config or {},
            )

            self._analyses[str(analysis.id)] = analysis
            self._logger.info(f"Analysis created successfully: {analysis.id}")
            return FlextResult[FlextQualityAnalysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create analysis")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to create analysis {e}")

    async def get_analysis(self, analysis_id: str) -> FlextResult[FlextQualityAnalysis]:
        """Get analysis by ID.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing the analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if analysis is None:
                return FlextResult[FlextQualityAnalysis].fail(
                    f"Analysis not found: {analysis_id}"
                )
            return FlextResult[FlextQualityAnalysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get analysis")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to get analysis {e}")

    async def update_analysis_status(
        self,
        analysis_id: str,
        status: FlextAnalysisStatus,
        error_message: str | None = None,
    ) -> FlextResult[FlextQualityAnalysis]:
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
                return FlextResult[FlextQualityAnalysis].fail("Analysis not found")

            # Use model_copy for immutable updates
            updated_analysis = analysis.model_copy(
                update={"status": status, "error_message": error_message}
            )

            self._analyses[analysis_id] = updated_analysis
            self._logger.info(f"Analysis status updated: {analysis_id} -> {status}")
            return FlextResult[FlextQualityAnalysis].ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to update analysis")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to update analysis: {e}")

    async def update_metrics(
        self,
        analysis_id: str,
        total_files: int,
        total_lines: int,
        code_lines: int,
        comment_lines: int,
        blank_lines: int,
    ) -> FlextResult[FlextQualityAnalysis]:
        """Update analysis metrics.

        Args:
            analysis_id: Analysis unique identifier
            total_files: Total number of files
            total_lines: Total lines of code
            code_lines: Lines of actual code
            comment_lines: Lines of comments
            blank_lines: Blank lines

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult[FlextQualityAnalysis].fail("Analysis not found")

            # Update metrics using model_copy
            updated_analysis = analysis.model_copy(
                update={
                    "total_files": total_files,
                    "total_lines": total_lines,
                    "code_lines": code_lines,
                    "comment_lines": comment_lines,
                    "blank_lines": blank_lines,
                }
            )

            self._analyses[analysis_id] = updated_analysis
            self._logger.info(f"Analysis metrics updated: {analysis_id}")
            return FlextResult[FlextQualityAnalysis].ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to update analysis metrics")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to update metrics: {e}")

    async def update_scores(
        self,
        analysis_id: str,
        coverage_score: float,
        complexity_score: float,
        maintainability_score: float,
        security_score: float,
        overall_score: float,
    ) -> FlextResult[FlextQualityAnalysis]:
        """Update analysis scores.

        Args:
            analysis_id: Analysis unique identifier
            coverage_score: Coverage score percentage
            complexity_score: Complexity score percentage
            maintainability_score: Maintainability score percentage
            security_score: Security score percentage
            overall_score: Overall quality score percentage

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult[FlextQualityAnalysis].fail("Analysis not found")

            # Update scores using model_copy
            updated_analysis = analysis.model_copy(
                update={
                    "coverage_score": coverage_score,
                    "complexity_score": complexity_score,
                    "maintainability_score": maintainability_score,
                    "security_score": security_score,
                    "overall_score": overall_score,
                }
            )

            self._analyses[analysis_id] = updated_analysis
            self._logger.info(f"Analysis scores updated: {analysis_id}")
            return FlextResult[FlextQualityAnalysis].ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to update analysis scores")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to update scores: {e}")

    async def update_issue_counts(
        self,
        analysis_id: str,
        total_issues: int,
        critical_issues: int,
        high_issues: int,
        medium_issues: int,
        low_issues: int,
    ) -> FlextResult[FlextQualityAnalysis]:
        """Update analysis issue counts.

        Args:
            analysis_id: Analysis unique identifier
            total_issues: Total number of issues
            critical_issues: Number of critical issues
            high_issues: Number of high priority issues
            medium_issues: Number of medium priority issues
            low_issues: Number of low priority issues

        Returns:
            FlextResult containing the updated analysis or error

        """
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult[FlextQualityAnalysis].fail("Analysis not found")

            # Update issue counts using model_copy
            updated_analysis = analysis.model_copy(
                update={
                    "total_issues": total_issues,
                    "critical_issues": critical_issues,
                    "high_issues": high_issues,
                    "medium_issues": medium_issues,
                    "low_issues": low_issues,
                }
            )

            self._analyses[analysis_id] = updated_analysis
            self._logger.info(f"Analysis issue counts updated: {analysis_id}")
            return FlextResult[FlextQualityAnalysis].ok(updated_analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to update analysis issue counts")
            return FlextResult[FlextQualityAnalysis].fail(f"Failed to update issue counts: {e}")

    async def complete_analysis(self, analysis_id: str) -> FlextResult[FlextQualityAnalysis]:
        """Complete an analysis.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing the completed analysis or error

        """
        return await self.update_analysis_status(
            analysis_id=analysis_id,
            status=FlextAnalysisStatus.COMPLETED,
        )

    async def fail_analysis(
        self,
        analysis_id: str,
        error_message: str,
    ) -> FlextResult[FlextQualityAnalysis]:
        """Fail an analysis with error message.

        Args:
            analysis_id: Analysis unique identifier
            error_message: Error message describing the failure

        Returns:
            FlextResult containing the failed analysis or error

        """
        return await self.update_analysis_status(
            analysis_id=analysis_id,
            status=FlextAnalysisStatus.FAILED,
            error_message=error_message,
        )

    async def list_analyses(self, project_id: str) -> FlextResult[list[FlextQualityAnalysis]]:
        """List all analyses for a project.

        Args:
            project_id: Project unique identifier

        Returns:
            FlextResult containing list of analyses or error

        """
        try:
            analyses = [
                analysis
                for analysis in self._analyses.values()
                if analysis.project_id == project_id
            ]
            return FlextResult[list[FlextQualityAnalysis]].ok(analyses)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to list analyses")
            return FlextResult[list[FlextQualityAnalysis]].fail(f"Failed to list analyses: {e}")


class BasicQualityIssueService:
    """Service for managing quality issues using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._issues: dict[str, FlextQualityIssue] = {}
        self._logger = get_logger(__name__)

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
        source: str = "ruff",  # noqa: ARG002
    ) -> FlextResult[FlextQualityIssue]:
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
            issue = FlextQualityIssue(
                id=str(uuid4()),
                analysis_id=analysis_id,
                file_path=file_path,
                line_number=line_number,
                column_number=column_number,
                severity=severity,
                issue_type=issue_type,
                rule_id=rule or "unknown",
                message=message,
            )

            self._issues[str(issue.id)] = issue
            return FlextResult[FlextQualityIssue].ok(issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create issue")
            return FlextResult[FlextQualityIssue].fail(f"Failed to create issue {e}")

    async def get_issues_for_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[FlextQualityIssue]]:
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
                if issue.analysis_id == analysis_id
            ]
            return FlextResult[list[FlextQualityIssue]].ok(issues)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get issues for analysis")
            return FlextResult[list[FlextQualityIssue]].fail(
                f"Failed to get issues for analysis {e}"
            )

    async def get_issue(self, issue_id: str) -> FlextResult[FlextQualityIssue]:
        """Get an issue by ID.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if issue is None:
                return FlextResult[FlextQualityIssue].fail(f"Issue not found: {issue_id}")
            return FlextResult[FlextQualityIssue].ok(issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get issue")
            return FlextResult[FlextQualityIssue].fail(f"Failed to get issue: {e}")

    async def list_issues(
        self,
        analysis_id: str | None = None,
        severity: IssueSeverity | None = None,
    ) -> FlextResult[list[FlextQualityIssue]]:
        """List issues with optional filtering.

        Args:
            analysis_id: Optional analysis ID filter
            severity: Optional severity filter

        Returns:
            FlextResult containing list of issues or error

        """
        try:
            issues = list(self._issues.values())

            # Apply filters
            if analysis_id:
                issues = [issue for issue in issues if issue.analysis_id == analysis_id]
            if severity:
                issues = [issue for issue in issues if issue.severity == severity]

            return FlextResult[list[FlextQualityIssue]].ok(issues)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to list issues")
            return FlextResult[list[FlextQualityIssue]].fail(f"Failed to list issues: {e}")

    async def mark_fixed(self, issue_id: str) -> FlextResult[FlextQualityIssue]:
        """Mark an issue as fixed.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the updated issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult[FlextQualityIssue].fail("Issue not found")

            # Update issue status using model_copy
            updated_issue = issue.model_copy(update={"is_suppressed": False})

            self._issues[issue_id] = updated_issue
            self._logger.info(f"Issue marked as fixed: {issue_id}")
            return FlextResult[FlextQualityIssue].ok(updated_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to mark issue as fixed")
            return FlextResult[FlextQualityIssue].fail(f"Failed to mark issue as fixed: {e}")

    async def suppress_issue(
        self,
        issue_id: str,
        reason: str,
    ) -> FlextResult[FlextQualityIssue]:
        """Suppress an issue with reason.

        Args:
            issue_id: Issue unique identifier
            reason: Reason for suppression

        Returns:
            FlextResult containing the suppressed issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult[FlextQualityIssue].fail("Issue not found")

            # Update issue to suppressed status using model_copy
            updated_issue = issue.model_copy(
                update={"is_suppressed": True, "suppression_reason": reason}
            )

            self._issues[issue_id] = updated_issue
            self._logger.info(f"Issue suppressed: {issue_id} - {reason}")
            return FlextResult[FlextQualityIssue].ok(updated_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to suppress issue")
            return FlextResult[FlextQualityIssue].fail(f"Failed to suppress issue: {e}")

    async def unsuppress_issue(self, issue_id: str) -> FlextResult[FlextQualityIssue]:
        """Unsuppress an issue.

        Args:
            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the unsuppressed issue or error

        """
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult[FlextQualityIssue].fail("Issue not found")

            # Update issue to unsuppressed status using model_copy
            updated_issue = issue.model_copy(
                update={"is_suppressed": False, "suppression_reason": None}
            )

            self._issues[issue_id] = updated_issue
            self._logger.info(f"Issue unsuppressed: {issue_id}")
            return FlextResult[FlextQualityIssue].ok(updated_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to unsuppress issue")
            return FlextResult[FlextQualityIssue].fail(f"Failed to unsuppress issue: {e}")


class BasicQualityReportService:
    """Service for managing quality reports using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._reports: dict[str, FlextQualityReport] = {}
        self._logger = get_logger(__name__)

    async def create_report(
        self,
        analysis_id: str,
        format_type: str,
        content: str,  # noqa: ARG002
        file_path: str | None = None,
        metadata: dict[str, object] | None = None,  # noqa: ARG002
    ) -> FlextResult[FlextQualityReport]:
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
            report = FlextQualityReport(
                id=str(uuid4()),
                analysis_id=analysis_id,
                report_type=format_type,
                report_path=file_path,
            )

            self._reports[str(report.id)] = report
            self._logger.info(f"Report created successfully: {report.id}")
            return FlextResult[FlextQualityReport].ok(report)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create report")
            return FlextResult[FlextQualityReport].fail(f"Failed to create report {e}")

    async def get_reports_for_analysis(
        self,
        analysis_id: str,
    ) -> FlextResult[list[FlextQualityReport]]:
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
                if report.analysis_id == analysis_id
            ]
            return FlextResult[list[FlextQualityReport]].ok(reports)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get reports for analysis")
            return FlextResult[list[FlextQualityReport]].fail(
                f"Failed to get reports for analysis {e}"
            )

    async def get_report(self, report_id: str) -> FlextResult[FlextQualityReport]:
        """Get a report by ID.

        Args:
            report_id: Report unique identifier

        Returns:
            FlextResult containing the report or error

        """
        try:
            report = self._reports.get(report_id)
            if report is None:
                return FlextResult[FlextQualityReport].fail(f"Report not found: {report_id}")
            return FlextResult[FlextQualityReport].ok(report)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to get report")
            return FlextResult[FlextQualityReport].fail(f"Failed to get report: {e}")

    async def list_reports(self, analysis_id: str) -> FlextResult[list[FlextQualityReport]]:
        """List all reports for an analysis.

        Args:
            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of reports or error

        """
        return await self.get_reports_for_analysis(analysis_id)

    async def delete_report(self, report_id: str) -> FlextResult[bool]:
        """Delete a report.

        Args:
            report_id: Report unique identifier

        Returns:
            FlextResult containing success status or error

        """
        try:
            if report_id in self._reports:
                del self._reports[report_id]
                self._logger.info(f"Report deleted successfully: {report_id}")
                return FlextResult[bool].ok(True)
            return FlextResult[bool].fail("Report not found")
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to delete report")
            return FlextResult[bool].fail(f"Failed to delete report: {e}")


class ExternalAnalysisService:
    """Service for external backend analysis using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with external backend."""
        self._backend = ExternalBackend()
        self._logger = get_logger(__name__)

    async def analyze_with_backend(
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
            self._logger.info(f"Running {backend_tool} analysis")
            result = self._backend.analyze(code, file_path, tool=backend_tool)
            return FlextResult[dict[str, object]].ok(result)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to analyze with external backend")
            return FlextResult[dict[str, object]].fail(
                f"Failed to analyze with external backend {e}"
            )


# Legacy compatibility - using warnings like flext-cli
class FlextQualityProjectService(BasicQualityProjectService):
    """Legacy compatibility facade - DEPRECATED."""

    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityProjectService is deprecated; use FlextQualityProjectService directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityAnalysisService(BasicQualityAnalysisService):
    """Legacy compatibility facade - DEPRECATED."""

    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityAnalysisService is deprecated; use FlextQualityAnalysisService directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityIssueService(BasicQualityIssueService):
    """Legacy compatibility facade - DEPRECATED."""

    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityIssueService is deprecated; use FlextQualityIssueService directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


class FlextQualityReportService(BasicQualityReportService):
    """Legacy compatibility facade - DEPRECATED."""

    def __init__(self) -> None:
        warnings.warn(
            "FlextQualityReportService is deprecated; use FlextQualityReportService directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


# Aliases for backward compatibility (like flext-cli pattern)
QualityProjectService = BasicQualityProjectService
QualityAnalysisService = BasicQualityAnalysisService
QualityIssueService = BasicQualityIssueService
QualityReportService = BasicQualityReportService


# Export all classes via __all__
__all__ = [
    "BasicQualityAnalysisService",
    "BasicQualityIssueService",
    # Basic service implementations (real classes)
    "BasicQualityProjectService",
    "BasicQualityReportService",
    "ExternalAnalysisService",
    # Legacy compatibility
    "FlextQualityAnalysisService",
    "FlextQualityIssueService",
    "FlextQualityProjectService",
    "FlextQualityReportService",
    # Compatibility aliases
    "QualityAnalysisService",
    "QualityIssueService",
    "QualityProjectService",
    "QualityReportService",
]
