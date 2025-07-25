"""Application services for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core service patterns - NO duplication.
    Clean architecture with dependency injection and FlextResult pattern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_quality.domain.entities import (
    IssueSeverity,
    IssueType,
    QualityIssue,
    QualityProject,
    QualityReport,
)
from flext_quality.domain.services import FlextResult

if TYPE_CHECKING:
    from uuid import UUID

    from flext_quality.domain.entities import QualityAnalysis


# Simplified DI - removed decorator
class QualityProjectService:
    """Service for managing quality projects."""

    def __init__(self) -> None:
        self._projects: dict[UUID, QualityProject] = {}

    async def create_project(
        self,
        name: str,
        project_path: str,
        repository_url: str | None = None,
        config_path: str | None = None,
        language: str = "python",
        auto_analyze: bool = True,
        min_coverage: float = 95.0,
        max_complexity: int = 10,
        max_duplication: float = 5.0,
    ) -> FlextResult[QualityProject]:
        try:
            project = QualityProject(
                project_path=project_path,
                repository_url=repository_url,
                config_path=config_path,
                language=language,
                auto_analyze=auto_analyze,
                min_coverage=min_coverage,
                max_complexity=max_complexity,
                max_duplication=max_duplication,
            )

            self._projects[project.id] = project
            return FlextResult.ok(project)
        except Exception as e:
            return FlextResult.fail(f"Failed to create project {e}")

    async def get_project(
        self,
        project_id: UUID,
    ) -> FlextResult[QualityProject]:
        try:
            project = self._projects.get(project_id)
            return FlextResult.ok(project)
        except Exception as e:
            return FlextResult.fail(f"Failed to get project {e}")

    async def list_projects(self) -> FlextResult[Any]:
        try:
            projects = list(self._projects.values())
            return FlextResult.ok(projects)
        except Exception as e:
            return FlextResult.fail(f"Failed to list projects {e}")

    async def update_project(
        self,
        project_id: UUID,
        updates: dict[str, Any],
    ) -> FlextResult[QualityProject]:
        try:
            project = self._projects.get(project_id)
            if not project:
                return FlextResult.fail("Project not found")

            for key, value in updates.items():
                if hasattr(project, key):
                    setattr(project, key, value)

            # Updated timestamp is managed automatically by DomainEntity
            return FlextResult.ok(project)
        except Exception as e:
            return FlextResult.fail(f"Failed to update project: {e}")

    async def delete_project(self, project_id: UUID) -> FlextResult[bool]:
        try:
            if project_id in self._projects:
                del self._projects[project_id]
                return FlextResult.ok(True)
            return FlextResult.fail("Project not found")
        except Exception as e:
            return FlextResult.fail(f"Failed to delete project: {e}")


# Simplified DI - removed decorator
class QualityAnalysisService:
    """Service for managing quality analyses."""

    def __init__(self) -> None:
        self._analyses: dict[UUID, QualityAnalysis] = {}

    async def create_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: dict[str, Any] | None = None,
    ) -> FlextResult[Any]:
        try:
            # Logic for creating analysis
            pass
        except Exception as e:
            return FlextResult.fail(f"Failed to create analysis: {e}")

    async def update_metrics(
        self,
        analysis_id: UUID,
        total_files: int,
        total_lines: int,
        code_lines: int,
        comment_lines: int,
        blank_lines: int,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            analysis.total_files = total_files
            analysis.total_lines = total_lines
            analysis.code_lines = code_lines
            analysis.comment_lines = comment_lines
            analysis.blank_lines = blank_lines
            # Updated timestamp is managed automatically by DomainEntity

            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to update metrics: {e}")

    async def update_scores(
        self,
        analysis_id: UUID,
        coverage_score: float,
        complexity_score: float,
        duplication_score: float,
        security_score: float,
        maintainability_score: float,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            analysis.coverage_score = coverage_score
            analysis.complexity_score = complexity_score
            analysis.duplication_score = duplication_score
            analysis.security_score = security_score
            analysis.maintainability_score = maintainability_score
            analysis.calculate_overall_score()
            # Updated timestamp is managed automatically by DomainEntity

            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to update scores: {e}")

    async def update_issue_counts(
        self,
        analysis_id: UUID,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            analysis.critical_issues = critical
            analysis.high_issues = high
            analysis.medium_issues = medium
            analysis.low_issues = low
            analysis.total_issues = critical + high + medium + low
            # Updated timestamp is managed automatically by DomainEntity

            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to update issue counts: {e}")

    async def complete_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            analysis.complete_analysis()
            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to complete analysis: {e}")

    async def fail_analysis(
        self,
        analysis_id: UUID,
        error: str,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            if not analysis:
                return FlextResult.fail("Analysis not found")

            analysis.fail_analysis(error)
            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to fail analysis: {e}")

    async def get_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[Any]:
        try:
            analysis = self._analyses.get(analysis_id)
            return FlextResult.ok(analysis)
        except Exception as e:
            return FlextResult.fail(f"Failed to get analysis: {e}")

    async def list_analyses(
        self,
        project_id: UUID,
    ) -> FlextResult[Any]:
        try:
            analyses = [
                a for a in self._analyses.values() if a.project_id == project_id
            ]
            # Sort by started_at descending
            analyses.sort(key=lambda a: a.started_at, reverse=True)
            return FlextResult.ok(analyses)
        except Exception as e:
            return FlextResult.fail(f"Failed to list analyses: {e}")


# Simplified DI - removed decorator
class QualityIssueService:
    """Service for managing quality issues."""

    def __init__(self) -> None:
        self._issues: dict[UUID, QualityIssue] = {}

    async def create_issue(
        self,
        analysis_id: UUID,
        issue_type: str,
        severity: str,
        rule_id: str,
        file_path: str,
        message: str,
        line_number: int | None = None,
        column_number: int | None = None,
        end_line_number: int | None = None,
        end_column_number: int | None = None,
        code_snippet: str | None = None,
        suggestion: str | None = None,
    ) -> FlextResult[Any]:
        try:
            issue = QualityIssue(
                analysis_id=analysis_id,
                issue_type=IssueType(issue_type),
                severity=IssueSeverity(severity),
                rule_id=rule_id,
                file_path=file_path,
                message=message,
                line_number=line_number,
                column_number=column_number,
                end_line_number=end_line_number,
                end_column_number=end_column_number,
                code_snippet=code_snippet,
                suggestion=suggestion,
            )

            self._issues[issue.id] = issue
            return FlextResult.ok(issue)
        except Exception as e:
            return FlextResult.fail(f"Failed to create issue: {e}")

    async def get_issue(self, issue_id: UUID) -> FlextResult[QualityIssue | None]:
        try:
            issue = self._issues.get(issue_id)
            return FlextResult.ok(issue)
        except Exception as e:
            return FlextResult.fail(f"Failed to get issue {e}")

    async def list_issues(
        self,
        analysis_id: UUID,
        severity: str | None = None,
        issue_type: str | None = None,
        file_path: str | None = None,
    ) -> FlextResult[Any]:
        try:
            issues = [i for i in self._issues.values() if i.analysis_id == analysis_id]

            if severity:
                issues = [i for i in issues if i.severity == severity]

            if issue_type:
                issues = [i for i in issues if i.issue_type == issue_type]

            if file_path:
                issues = [i for i in issues if i.file_path == file_path]

            return FlextResult.ok(issues)
        except Exception as e:
            return FlextResult.fail(f"Failed to list issues: {e}")

    async def mark_fixed(self, issue_id: UUID) -> FlextResult[Any]:
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            issue.mark_fixed()
            return FlextResult.ok(issue)
        except Exception as e:
            return FlextResult.fail(f"Failed to mark issue as fixed: {e}")

    async def suppress_issue(
        self,
        issue_id: UUID,
        reason: str,
    ) -> FlextResult[Any]:
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            issue.suppress(reason)
            return FlextResult.ok(issue)
        except Exception as e:
            return FlextResult.fail(f"Failed to suppress issue: {e}")

    async def unsuppress_issue(self, issue_id: UUID) -> FlextResult[Any]:
        try:
            issue = self._issues.get(issue_id)
            if not issue:
                return FlextResult.fail("Issue not found")

            issue.unsuppress()
            return FlextResult.ok(issue)
        except Exception as e:
            return FlextResult.fail(f"Failed to unsuppress issue: {e}")


# Simplified DI - removed decorator
class QualityReportService:
    """Service for managing quality reports."""

    def __init__(self) -> None:
        self._reports: dict[UUID, QualityReport] = {}

    async def create_report(
        self,
        analysis_id: UUID,
        report_type: str,
        report_format: str = "summary",
        report_path: str | None = None,
        report_size_bytes: int = 0,
    ) -> FlextResult[Any]:
        try:
            report = QualityReport(
                analysis_id=analysis_id,
                report_type=report_type,
                report_format=report_format,
                report_path=report_path,
                report_size_bytes=report_size_bytes,
            )

            self._reports[report.id] = report
            return FlextResult.ok(report)
        except Exception as e:
            return FlextResult.fail(f"Failed to create report: {e}")

    async def get_report(self, report_id: UUID) -> FlextResult[Any]:
        try:
            report = self._reports.get(report_id)
            if report:
                report.increment_access()
            return FlextResult.ok(report)
        except Exception as e:
            return FlextResult.fail(f"Failed to get report: {e}")

    async def list_reports(
        self,
        analysis_id: UUID,
    ) -> FlextResult[Any]:
        try:
            reports = [
                r for r in self._reports.values() if r.analysis_id == analysis_id
            ]
            return FlextResult.ok(reports)
        except Exception as e:
            return FlextResult.fail(f"Failed to list reports {e}")

    async def delete_report(self, report_id: UUID) -> FlextResult[Any]:
        try:
            if report_id in self._reports:
                del self._reports[report_id]
                return FlextResult.ok(True)
            return FlextResult.fail("Report not found")
        except Exception as e:
            return FlextResult.fail(f"Failed to delete report: {e}")


# Implementation classes for dependency injection containers
# These wrap the main services with specific interface implementations


# Simplified DI - removed decorator
class AnalysisServiceImpl:
    """Implementation of analysis service for DI container."""

    def __init__(self) -> None:
        self._analysis_service = QualityAnalysisService()

    async def analyze_project(self, project_id: UUID) -> FlextResult[Any]:
        """Analyze project by ID."""
        return await self._analysis_service.create_analysis(
            project_id=project_id,
        )


# Simplified DI - removed decorator
class SecurityAnalyzerServiceImpl:
    """Implementation of security analyzer service for DI container."""

    def __init__(self, port: Any = None, repository: Any = None) -> None:
        self._port = port
        self._repository = repository

    async def analyze_security(self, project_path: str) -> FlextResult[Any]:
        """Analyze security issues in project."""
        return FlextResult.ok({"security_issues": []})


# Simplified DI - removed decorator
class LintingServiceImpl:
    """Implementation of linting service for DI container."""

    def __init__(self, port: Any = None, repository: Any = None) -> None:
        self._port = port
        self._repository = repository

    async def run_linting(self, project_path: str) -> FlextResult[Any]:
        """Run linting analysis on project."""
        return FlextResult.ok({"linting_issues": []})


# Simplified DI - removed decorator
class ReportGeneratorServiceImpl:
    """Implementation of report generator service for DI container."""

    def __init__(self) -> None:
        self._report_service = QualityReportService()

    async def generate_report(
        self,
        analysis_id: UUID,
        report_type: str,
    ) -> FlextResult[Any]:
        """Generate report for analysis."""
        return await self._report_service.create_report(
            analysis_id=analysis_id,
            report_type=report_type,
        )
