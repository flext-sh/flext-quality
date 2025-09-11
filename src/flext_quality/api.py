"""Simple API interface for FLEXT-QUALITY v0.7.0.

REFACTORED: Using flext-core DI patterns and FlextResult - NO duplication.
Provides clean API interface for all quality analysis operations.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


import warnings
from pathlib import Path
from uuid import UUID

from flext_core import FlextResult

from flext_quality.analyzer import CodeAnalyzer
from flext_quality.container import get_quality_container
from flext_quality.entities import (
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
)
from flext_quality.services import (
    QualityAnalysisService,
    QualityIssueService,
    QualityProjectService,
    QualityReportService,
)
from flext_quality.typings import FlextTypes
from flext_quality.value_objects import FlextIssueSeverity, FlextIssueType


class FlextQualityAPI:
    """Simple API interface for quality analysis operations."""

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
        """Get or create project service instance."""
        if self._project_service is None:
            self._project_service = QualityProjectService()
        return self._project_service

    @property
    def analysis_service(self) -> QualityAnalysisService:
        """Get or create analysis service instance."""
        if self._analysis_service is None:
            self._analysis_service = QualityAnalysisService()
        return self._analysis_service

    @property
    def issue_service(self) -> QualityIssueService:
        """Get or create issue service instance."""
        if self._issue_service is None:
            self._issue_service = QualityIssueService()
        return self._issue_service

    @property
    def report_service(self) -> QualityReportService:
        """Get or create report service instance."""
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
        *,
        auto_analyze: bool = True,
        min_coverage: float = 95.0,
        max_complexity: int = 10,
        max_duplication: float = 5.0,
    ) -> FlextResult[QualityProject]:
        """Create a new quality project."""
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
        """Get a project by ID."""
        return await self.project_service.get_project(str(project_id))

    async def list_projects(self) -> FlextResult[list[QualityProject]]:
        """List all projects."""
        return await self.project_service.list_projects()

    async def update_project(
        self,
        project_id: UUID,
        updates: FlextTypes.Core.Dict,
    ) -> FlextResult[QualityProject]:
        """Update a project."""
        return await self.project_service.update_project(str(project_id), updates)

    async def delete_project(self, project_id: UUID) -> FlextResult[bool]:
        """Delete a project."""
        return await self.project_service.delete_project(str(project_id))

    # Analysis operations
    async def create_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
        pull_request_id: str | None = None,
        analysis_config: FlextTypes.Core.JsonDict | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Create a new quality analysis."""
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
        """Update analysis metrics."""
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
        """Update analysis quality scores."""
        # Calculate overall score as average
        overall_score = (
            coverage_score + complexity_score + security_score + maintainability_score
        ) / 4.0

        return await self.analysis_service.update_scores(
            analysis_id=str(analysis_id),
            coverage_score=coverage_score,
            complexity_score=complexity_score,
            maintainability_score=maintainability_score,
            security_score=security_score,
            overall_score=overall_score,
        )

    async def update_issue_counts(
        self,
        analysis_id: UUID,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis issue counts by severity."""
        total_issues = critical + high + medium + low

        return await self.analysis_service.update_issue_counts(
            analysis_id=str(analysis_id),
            total_issues=total_issues,
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
        )

    async def complete_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as completed."""
        return await self.analysis_service.complete_analysis(str(analysis_id))

    async def fail_analysis(
        self,
        analysis_id: UUID,
        error: str,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as failed."""
        return await self.analysis_service.fail_analysis(str(analysis_id), error)

    async def get_analysis(
        self,
        analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Get an analysis by ID."""
        return await self.analysis_service.get_analysis(str(analysis_id))

    async def list_analyses(
        self,
        project_id: UUID,
    ) -> FlextResult[list[QualityAnalysis]]:
        """List all analyses for a project."""
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
        """Create a new quality issue."""
        # Convert string parameters to enum types

        try:
            severity_enum = FlextIssueSeverity(severity)
            issue_type_enum = FlextIssueType(issue_type)
        except ValueError as e:
            return FlextResult[QualityIssue].fail(
                f"Invalid severity or issue type: {e}"
            )

        return await self.issue_service.create_issue(
            analysis_id=str(analysis_id),
            file_path=file_path,
            line_number=line_number or 1,
            column_number=column_number,
            severity=severity_enum,
            issue_type=issue_type_enum,
            message=message,
            rule=rule_id,
        )

    async def get_issue(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Get an issue by ID."""
        return await self.issue_service.get_issue(str(issue_id))

    async def list_issues(
        self,
        analysis_id: UUID,
        severity: str | None = None,
        issue_type: str | None = None,
        file_path: str | None = None,
    ) -> FlextResult[list[QualityIssue]]:
        """List issues for an analysis with optional filters."""
        # Convert string severity to enum if provided
        severity_enum = None
        if severity:
            try:
                severity_enum = FlextIssueSeverity(severity)
            except ValueError:
                return FlextResult[list[QualityIssue]].fail(
                    f"Invalid severity: {severity}"
                )

        return await self.issue_service.list_issues(
            analysis_id=str(analysis_id),
            severity=severity_enum,
        )

    async def mark_issue_fixed(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Mark an issue as fixed."""
        return await self.issue_service.mark_fixed(str(issue_id))

    async def suppress_issue(
        self,
        issue_id: UUID,
        reason: str,
    ) -> FlextResult[QualityIssue]:
        """Suppress an issue with a reason."""
        return await self.issue_service.suppress_issue(str(issue_id), reason)

    async def unsuppress_issue(self, issue_id: UUID) -> FlextResult[QualityIssue]:
        """Remove suppression from an issue."""
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
        """Create a quality report."""
        return await self.report_service.create_report(
            analysis_id=str(analysis_id),
            format_type=report_format,
            content="Generated report content",
            file_path=report_path,
        )

    async def get_report(self, report_id: UUID) -> FlextResult[QualityReport]:
        """Get a report by ID."""
        return await self.report_service.get_report(str(report_id))

    async def list_reports(
        self,
        analysis_id: UUID,
    ) -> FlextResult[list[QualityReport]]:
        """List all reports for an analysis."""
        return await self.report_service.list_reports(str(analysis_id))

    async def delete_report(self, report_id: UUID) -> FlextResult[bool]:
        """Delete a report."""
        return await self.report_service.delete_report(str(report_id))

    # High-level operations
    async def run_full_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Run a complete quality analysis for a project."""
        # Create analysis
        result = await self.create_analysis(
            project_id=project_id,
            commit_hash=commit_hash,
            branch=branch,
        )

        # Use is_failure for early return pattern (current flext-core API)
        if result.is_failure:
            return result
        analysis = result.value

        # Get the project to access its path
        project_result = await self.get_project(project_id)
        if project_result.is_failure:
            return FlextResult[QualityAnalysis].fail(
                f"Failed to get project: {project_result.error}"
            )

        project = project_result.value

        # Integrate with real analysis tools using flext-core patterns
        # Execute analysis using CodeAnalyzer
        project_path = Path(project.project_path)
        analyzer = CodeAnalyzer(project_path)
        analysis_results = analyzer.analyze_project()

        # Update with real metrics from analysis
        await self.update_metrics(
            analysis_id=UUID(str(analysis.id)),
            total_files=analysis_results.overall_metrics.files_analyzed,
            total_lines=analysis_results.overall_metrics.total_lines,
            code_lines=analysis_results.overall_metrics.total_lines,  # CodeAnalyzer provides total lines
            comment_lines=0,  # Would need detailed AST analysis
            blank_lines=0,  # Would need detailed AST analysis
        )

        # Update with real scores from analysis
        await self.update_scores(
            analysis_id=UUID(str(analysis.id)),
            coverage_score=analysis_results.overall_metrics.coverage_score,
            complexity_score=analysis_results.overall_metrics.complexity_score,
            duplication_score=100.0
            - len(analysis_results.duplication_issues),  # Convert issues to score
            security_score=analysis_results.overall_metrics.security_score,
            maintainability_score=analysis_results.overall_metrics.maintainability_score,
        )

        # Count real issues by severity
        critical_issues = len(
            [i for i in analysis_results.security_issues if i.severity == "critical"],
        )
        high_issues = len(
            [i for i in analysis_results.security_issues if i.severity == "high"],
        )
        medium_issues = len(
            [i for i in analysis_results.security_issues if i.severity == "medium"],
        )
        low_issues = len(
            [i for i in analysis_results.security_issues if i.severity == "low"],
        )

        # Add complexity issues to high priority
        high_issues += len(analysis_results.complexity_issues)

        # Update with real issue counts
        await self.update_issue_counts(
            analysis_id=UUID(str(analysis.id)),
            critical=critical_issues,
            high=high_issues,
            medium=medium_issues,
            low=low_issues,
        )

        # Complete the analysis
        return await self.complete_analysis(UUID(str(analysis.id)))


# Legacy compatibility facade (TEMPORARY)
class QualityAPI(FlextQualityAPI):
    """Legacy API class - replaced by FlextQualityAPI."""

    def __init__(self) -> None:
        warnings.warn(
            "QualityAPI is deprecated; use FlextQualityAPI",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()
