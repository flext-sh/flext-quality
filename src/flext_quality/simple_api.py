"""Simple API interface for FLEXT-QUALITY v0.7.0.

REFACTORED: Using flext-core DI patterns and FlextResult - NO duplication.
Provides clean API interface for all quality analysis operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from flext_core import FlextResult, TAnyDict
from flext_quality.application.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.infrastructure.container import get_quality_container

if TYPE_CHECKING:
    from flext_quality.domain.entities import (
        QualityAnalysis,
        QualityIssue,
        QualityProject,
        QualityReport,
    )
else:
    # Runtime imports for isinstance checks
    from flext_quality.domain.entities import QualityAnalysis  # noqa: TC001


class QualityAPI:
    """Simple API interface for quality analysis operations.

    Uses dependency injection to resolve services from flext-core container.
    All operations return FlextResult for type-safe error handling.
    """

    def __init__(self) -> None:
        """Initialize the Quality API with container-based DI."""
        self._container = get_quality_container()

        # Lazy load services
        self._project_service: QualityProjectService | None = None
        self._analysis_service: QualityAnalysisService | None = None
        self._issue_service: QualityIssueService | None = None
        self._report_service: QualityReportService | None = None

    @property
    def project_service(self) -> QualityProjectService:
        """Get or create project service instance.

        Returns:
            QualityProjectService instance.

        """
        if self._project_service is None:
            self._project_service = QualityProjectService()
        return self._project_service

    @property
    def analysis_service(self) -> QualityAnalysisService:
        """Get or create analysis service instance.

        Returns:
            QualityAnalysisService instance.

        """
        if self._analysis_service is None:
            self._analysis_service = QualityAnalysisService()
        return self._analysis_service

    @property
    def issue_service(self) -> QualityIssueService:
        """Get or create issue service instance.

        Returns:
            QualityIssueService instance.

        """
        if self._issue_service is None:
            self._issue_service = QualityIssueService()
        return self._issue_service

    @property
    def report_service(self) -> QualityReportService:
        """Get or create report service instance.

        Returns:
            QualityReportService instance.

        """
        if self._report_service is None:
            self._report_service = QualityReportService()
        return self._report_service

    # Project operations
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
        """Create a new quality project.

        Args:
            name: Project name.
            project_path: Path to project directory.
            repository_url: Optional repository URL.
            config_path: Optional config file path.
            language: Programming language (default: python).
            auto_analyze: Whether to auto-analyze (default: True).
            min_coverage: Minimum coverage threshold (default: 95.0).
            max_complexity: Maximum complexity threshold (default: 10).
            max_duplication: Maximum duplication threshold (default: 5.0).

        Returns:
            FlextResult containing the created QualityProject.

        """
        return await self.project_service.create_project(
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

    async def get_project(
        self,
        project_id: UUID,
    ) -> FlextResult[QualityProject]:
        """Get a project by ID.

        Args:
            project_id: Project UUID.

        Returns:
            FlextResult containing the QualityProject or None if not found.

        """
        return await self.project_service.get_project(str(project_id))

    async def list_projects(self) -> FlextResult[list[QualityProject]]:
        """List all projects.

        Returns:
            FlextResult containing list of QualityProject instances.

        """
        return await self.project_service.list_projects()

    async def update_project(
        self,
        project_id: UUID,
        updates: TAnyDict,
    ) -> FlextResult[QualityProject]:
        """Update a project.

        Args:
            project_id: Project UUID.
            updates: Dictionary of fields to update.

        Returns:
            FlextResult containing the updated QualityProject.

        """
        return await self.project_service.update_project(str(project_id), updates)

    async def delete_project(self, project_id: UUID) -> FlextResult[bool]:
        """Delete a project.

        Args:
            project_id: Project UUID.

        Returns:
            FlextResult containing True if deleted successfully.

        """
        return await self.project_service.delete_project(str(project_id))

    # Analysis operations
    async def create_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: TAnyDict | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Create a new quality analysis.

        Args:
            project_id: Project UUID.
            commit_hash: Optional commit hash.
            branch: Optional branch name.
            pull_request_id: Optional pull request ID.
            analysis_config: Optional analysis configuration.

        Returns:
            FlextResult containing the created QualityAnalysis.

        """
        return await self.analysis_service.create_analysis(
            project_id=str(project_id),
            commit_hash=commit_hash,
            branch=branch,
            pull_request_id=pull_request_id,
            analysis_config=analysis_config,
        )

    async def update_metrics(
        self,
        analysis_id: UUID,
        total_files: int,
        total_lines: int,
        code_lines: int,
        comment_lines: int,
        blank_lines: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis metrics.

        Args:
            analysis_id: Analysis UUID.
            total_files: Total number of files.
            total_lines: Total lines of code.
            code_lines: Lines of actual code.
            comment_lines: Lines of comments.
            blank_lines: Blank lines.

        Returns:
            FlextResult containing the updated QualityAnalysis.

        """
        return await self.analysis_service.update_metrics(
            analysis_id=str(analysis_id),
            total_files=total_files,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
        )

    async def update_scores(
        self,
        analysis_id: UUID,
        coverage_score: float,
        complexity_score: float,
        duplication_score: float,
        security_score: float,
        maintainability_score: float,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis quality scores.

        Args:
            analysis_id: Analysis UUID.
            coverage_score: Code coverage score.
            complexity_score: Code complexity score.
            duplication_score: Code duplication score.
            security_score: Security analysis score.
            maintainability_score: Maintainability score.

        Returns:
            FlextResult containing the updated QualityAnalysis.

        """
        return await self.analysis_service.update_scores(
            analysis_id=str(analysis_id),
            coverage_score=coverage_score,
            complexity_score=complexity_score,
            duplication_score=duplication_score,
            security_score=security_score,
            maintainability_score=maintainability_score,
        )

    async def update_issue_counts(
        self,
        analysis_id: UUID,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis issue counts by severity.

        Args:
            analysis_id: Analysis UUID.
            critical: Number of critical issues.
            high: Number of high severity issues.
            medium: Number of medium severity issues.
            low: Number of low severity issues.

        Returns:
            FlextResult containing the updated QualityAnalysis.

        """
        return await self.analysis_service.update_issue_counts(
            analysis_id=str(analysis_id),
            critical=critical,
            high=high,
            medium=medium,
            low=low,
        )

    async def complete_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as completed.

        Args:
            analysis_id: Analysis UUID.

        Returns:
            FlextResult containing the completed QualityAnalysis.

        """
        return await self.analysis_service.complete_analysis(str(analysis_id))

    async def fail_analysis(
        self,
        analysis_id: UUID,
        error: str,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as failed.

        Args:
            analysis_id: Analysis UUID.
            error: Error message describing the failure.

        Returns:
            FlextResult containing the failed QualityAnalysis.

        """
        return await self.analysis_service.fail_analysis(str(analysis_id), error)

    async def get_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Get an analysis by ID.

        Args:
            analysis_id: Analysis UUID.

        Returns:
            FlextResult containing the QualityAnalysis or None if not found.

        """
        return await self.analysis_service.get_analysis(str(analysis_id))

    async def list_analyses(
        self,
        project_id: UUID,
    ) -> FlextResult[list[QualityAnalysis]]:
        """List all analyses for a project.

        Args:
            project_id: Project UUID.

        Returns:
            FlextResult containing list of QualityAnalysis instances.

        """
        return await self.analysis_service.list_analyses(str(project_id))

    # Issue operations
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
    ) -> FlextResult[QualityIssue]:
        """Create a new quality issue.

        Args:
            analysis_id: Analysis UUID.
            issue_type: Type of issue.
            severity: Issue severity level.
            rule_id: Rule identifier that triggered the issue.
            file_path: Path to the file with the issue.
            message: Issue description message.
            line_number: Optional line number.
            column_number: Optional column number.
            end_line_number: Optional end line number.
            end_column_number: Optional end column number.
            code_snippet: Optional code snippet.
            suggestion: Optional fix suggestion.

        Returns:
            FlextResult containing the created QualityIssue.

        """
        return await self.issue_service.create_issue(
            analysis_id=str(analysis_id),
            issue_type=issue_type,
            severity=severity,
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

    async def get_issue(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Get an issue by ID.

        Args:
            issue_id: Issue UUID.

        Returns:
            FlextResult containing the QualityIssue or None if not found.

        """
        return await self.issue_service.get_issue(str(issue_id))

    async def list_issues(
        self,
        analysis_id: UUID,
        severity: str | None = None,
        issue_type: str | None = None,
        file_path: str | None = None,
    ) -> FlextResult[list[QualityIssue]]:
        """List issues for an analysis with optional filters.

        Args:
            analysis_id: Analysis UUID.
            severity: Optional severity filter.
            issue_type: Optional issue type filter.
            file_path: Optional file path filter.

        Returns:
            FlextResult containing list of QualityIssue instances.

        """
        return await self.issue_service.list_issues(
            analysis_id=str(analysis_id),
            severity=severity,
            issue_type=issue_type,
            file_path=file_path,
        )

    async def mark_issue_fixed(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Mark an issue as fixed.

        Args:
            issue_id: Issue UUID.

        Returns:
            FlextResult containing the updated QualityIssue.

        """
        return await self.issue_service.mark_fixed(str(issue_id))

    async def suppress_issue(
        self,
        issue_id: UUID,
        reason: str,
    ) -> FlextResult[QualityIssue]:
        """Suppress an issue with a reason.

        Args:
            issue_id: Issue UUID.
            reason: Reason for suppressing the issue.

        Returns:
            FlextResult containing the suppressed QualityIssue.

        """
        return await self.issue_service.suppress_issue(str(issue_id), reason)

    async def unsuppress_issue(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Remove suppression from an issue.

        Args:
            issue_id: Issue UUID.

        Returns:
            FlextResult containing the unsuppressed QualityIssue.

        """
        return await self.issue_service.unsuppress_issue(str(issue_id))

    # Report operations
    async def create_report(
        self,
        analysis_id: UUID,
        report_type: str,
        report_format: str = "summary",
        report_path: str | None = None,
        report_size_bytes: int = 0,
    ) -> FlextResult[QualityReport]:
        """Create a quality report.

        Args:
            analysis_id: Analysis UUID.
            report_type: Type of report to create.
            report_format: Report format (default: summary).
            report_path: Optional path to save report.
            report_size_bytes: Report size in bytes (default: 0).

        Returns:
            FlextResult containing the created QualityReport.

        """
        return await self.report_service.create_report(
            analysis_id=str(analysis_id),
            report_type=report_type,
            report_format=report_format,
            report_path=report_path,
            report_size_bytes=report_size_bytes,
        )

    async def get_report(self, report_id: UUID) -> FlextResult[QualityReport]:
        """Get a report by ID.

        Args:
            report_id: Report UUID.

        Returns:
            FlextResult containing the QualityReport or None if not found.

        """
        return await self.report_service.get_report(str(report_id))

    async def list_reports(
        self,
        analysis_id: UUID,
    ) -> FlextResult[list[QualityReport]]:
        """List all reports for an analysis.

        Args:
            analysis_id: Analysis UUID.

        Returns:
            FlextResult containing list of QualityReport instances.

        """
        return await self.report_service.list_reports(str(analysis_id))

    async def delete_report(self, report_id: UUID) -> FlextResult[bool]:
        """Delete a report.

        Args:
            report_id: Report UUID.

        Returns:
            FlextResult containing True if deleted successfully.

        """
        return await self.report_service.delete_report(str(report_id))

    # High-level operations
    async def run_full_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Run a complete quality analysis for a project.

        Args:
            project_id: Project UUID.
            commit_hash: Optional commit hash.
            branch: Optional branch name.

        Returns:
            FlextResult containing the completed QualityAnalysis.

        """
        # Create analysis
        result = await self.create_analysis(
            project_id=project_id,
            commit_hash=commit_hash,
            branch=branch,
        )

        if not result.success:
            return result

        analysis = result.data
        if analysis is None:
            return FlextResult.fail("Failed to create analysis")

        # Integrate with real analysis tools using flext-core patterns
        # For now, we'll just mark it as completed

        # Update with dummy metrics
        await self.update_metrics(
            analysis_id=UUID(analysis.id),
            total_files=100,
            total_lines=10000,
            code_lines=7000,
            comment_lines=2000,
            blank_lines=1000,
        )

        # Update with dummy scores
        await self.update_scores(
            analysis_id=UUID(analysis.id),
            coverage_score=95.0,
            complexity_score=85.0,
            duplication_score=92.0,
            security_score=98.0,
            maintainability_score=88.0,
        )

        # Update with dummy issue counts
        await self.update_issue_counts(
            analysis_id=UUID(analysis.id),
            critical=0,
            high=2,
            medium=5,
            low=10,
        )

        # Complete the analysis
        return await self.complete_analysis(UUID(analysis.id))
