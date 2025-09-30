"""Quality API module providing high-level interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override
from uuid import UUID

from flext_core import FlextResult, FlextTypes
from flext_quality import (
    QualityAnalysis,
    QualityIssue,
    QualityProject,
    QualityReport,
)
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.container import get_quality_container
from flext_quality.services import FlextQualityServices
from flext_quality.value_objects import FlextIssueSeverity, FlextIssueType

# Type aliases for backward compatibility


class FlextQualityAPI:
    """Simple API interface for quality analysis operations."""

    @override
    def __init__(self: object) -> None:
        """Initialize the Quality API with container-based DI."""
        self._container = get_quality_container()
        self._services = FlextQualityServices()

    @property
    def project_service(self: object) -> FlextQualityServices.ProjectService:
        """Get project service instance."""
        return self._services.get_project_service()

    @property
    def analysis_service(self: object) -> FlextQualityServices.AnalysisService:
        """Get analysis service instance."""
        return self._services.get_analysis_service()

    @property
    def issue_service(self: object) -> object:
        """Get issue service instance."""
        return self._services.get_issue_service()

    @property
    def report_service(self: object) -> object:
        """Get report service instance."""
        return self._services.get_report_service()

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
            _min_coverage=min_coverage,
            _max_complexity=max_complexity,
            _max_duplication=max_duplication,
        )

    async def get_project(
        self,
        _project_id: UUID,
    ) -> FlextResult[QualityProject]:
        """Get a project by ID."""
        return FlextResult[QualityProject].fail("get_project not implemented")

    async def list_projects(self) -> FlextResult[list[QualityProject]]:
        """List all projects."""
        return FlextResult[list[QualityProject]].fail("list_projects not implemented")

    async def update_project(
        self,
        _project_id: UUID,
        _updates: FlextTypes.Core.Dict,
    ) -> FlextResult[QualityProject]:
        """Update a project."""
        return FlextResult[QualityProject].fail("update_project not implemented")

    async def delete_project(self, _project_id: UUID) -> FlextResult[bool]:
        """Delete a project."""
        return FlextResult[bool].fail("delete_project not implemented")

    # Analysis operations
    async def create_analysis(
        self,
        project_id: UUID,
        _commit_hash: str | None = None,
        _branch: str | None = None,
        _pull_request_id: str | None = None,
        analysis_config: FlextTypes.Core.JsonDict | None = None,
    ) -> FlextResult[QualityAnalysis]:
        """Create a new quality analysis."""
        return await self.analysis_service.create_analysis(
            project_id=str(project_id),
            config=analysis_config
            if analysis_config is None
            else dict(analysis_config),
        )

    async def update_metrics(
        self,
        _analysis_id: UUID,
        _total_files: int,
        _total_lines: int,
        _code_lines: int,
        _comment_lines: int,
        _blank_lines: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis metrics."""
        return FlextResult[QualityAnalysis].fail("update_metrics not implemented")

    async def update_scores(
        self,
        _analysis_id: UUID,
        _coverage_score: float,
        complexity_score: float,
        _duplication_score: float,
        security_score: float,
        maintainability_score: float,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis quality scores."""
        # Calculate overall score as average
        (
            _coverage_score + complexity_score + security_score + maintainability_score
        ) / 4.0

        return FlextResult[QualityAnalysis].fail("update_scores not implemented")

    async def update_issue_counts(
        self,
        _analysis_id: UUID,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[QualityAnalysis]:
        """Update analysis issue counts by severity."""
        critical + high + medium + low

        return FlextResult[QualityAnalysis].fail("update_issue_counts not implemented")

    async def complete_analysis(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as completed."""
        return FlextResult[QualityAnalysis].fail("complete_analysis not implemented")

    async def fail_analysis(
        self,
        _analysis_id: UUID,
        _error: str,
    ) -> FlextResult[QualityAnalysis]:
        """Mark analysis as failed."""
        return FlextResult[QualityAnalysis].fail("fail_analysis not implemented")

    async def get_analysis(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[QualityAnalysis]:
        """Get an analysis by ID."""
        return FlextResult[QualityAnalysis].fail("get_analysis not implemented")

    async def list_analyses(
        self,
        _project_id: UUID,
    ) -> FlextResult[list[QualityAnalysis]]:
        """List all analyses for a project."""
        return FlextResult[list[QualityAnalysis]].fail("list_analyses not implemented")

    # Issue operations
    async def create_issue(
        self,
        _analysis_id: UUID,
        issue_type: str,
        severity: str,
        _rule_id: str,
        _file_path: str,
        _message: str,
        _line_number: int | None = None,
        _column_number: int | None = None,
        _end_line_number: int | None = None,
        _end_column_number: int | None = None,
        _code_snippet: str | None = None,
        _suggestion: str | None = None,
    ) -> FlextResult[QualityIssue]:
        """Create a new quality issue."""
        # Convert string parameters to enum types

        try:
            FlextIssueSeverity(severity)
            FlextIssueType(issue_type)
        except ValueError as e:
            return FlextResult[QualityIssue].fail(
                f"Invalid severity or issue type: {e}",
            )

        return FlextResult[QualityIssue].fail("create_issue not implemented")

    async def get_issue(self, _issue_id: UUID) -> FlextResult[QualityIssue]:
        """Get an issue by ID."""
        return FlextResult[QualityIssue].fail("get_issue not implemented")

    async def list_issues(
        self,
        _analysis_id: UUID,
        severity: str | None = None,
        _issue_type: str | None = None,
        _file_path: str | None = None,
    ) -> FlextResult[list[QualityIssue]]:
        """List issues for an analysis with optional filters."""
        # Convert string severity to enum if provided
        if severity:
            try:
                FlextIssueSeverity(severity)
            except ValueError:
                return FlextResult[list[QualityIssue]].fail(
                    f"Invalid severity: {severity}",
                )

        return FlextResult[list[QualityIssue]].fail("list_issues not implemented")

    async def mark_issue_fixed(self, _issue_id: UUID) -> FlextResult[QualityIssue]:
        """Mark an issue as fixed."""
        return FlextResult[QualityIssue].fail("mark_fixed not implemented")

    async def suppress_issue(
        self,
        _issue_id: UUID,
        _reason: str,
    ) -> FlextResult[QualityIssue]:
        """Suppress an issue with a reason."""
        return FlextResult[QualityIssue].fail("suppress_issue not implemented")

    async def unsuppress_issue(self, _issue_id: UUID) -> FlextResult[QualityIssue]:
        """Remove suppression from an issue."""
        return FlextResult[QualityIssue].fail("unsuppress_issue not implemented")

    # Report operations
    async def create_report(
        self,
        _analysis_id: UUID,
        _report_type: str,
        _report_format: str = "summary",
        _report_path: str | None = None,
        _report_size_bytes: int = 0,
    ) -> FlextResult[QualityReport]:
        """Create a quality report."""
        return FlextResult[QualityReport].fail("create_report not implemented")

    async def get_report(self, _report_id: UUID) -> FlextResult[QualityReport]:
        """Get a report by ID."""
        return FlextResult[QualityReport].fail("get_report not implemented")

    async def list_reports(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[list[QualityReport]]:
        """List all reports for an analysis."""
        return FlextResult[list[QualityReport]].fail("list_reports not implemented")

    async def delete_report(self, _report_id: UUID) -> FlextResult[bool]:
        """Delete a report."""
        return FlextResult[bool].fail("delete_report not implemented")

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
            _commit_hash=commit_hash,
            _branch=branch,
        )

        # Use is_failure for early return pattern (current flext-core API)
        if result.is_failure:
            return result
        analysis = result.value

        # Get the project to access its path
        project_result: FlextResult[object] = await self.get_project(project_id)
        if project_result.is_failure:
            return FlextResult[QualityAnalysis].fail(
                f"Failed to get project: {project_result.error}",
            )

        project = project_result.value

        # Integrate with real analysis tools using flext-core patterns
        # Execute analysis using CodeAnalyzer
        project_path = Path(project.project_path)
        analyzer = CodeAnalyzer(project_path)
        analysis_results: FlextResult[object] = analyzer.analyze_project()

        # Update with real metrics from analysis
        await self.update_metrics(
            _analysis_id=UUID(str(analysis.id)),
            _total_files=analysis_results.overall_metrics.files_analyzed,
            _total_lines=analysis_results.overall_metrics.total_lines,
            _code_lines=analysis_results.overall_metrics.total_lines,  # CodeAnalyzer provides total lines
            _comment_lines=0,  # Would need detailed AST analysis
            _blank_lines=0,  # Would need detailed AST analysis
        )

        # Update with real scores from analysis
        await self.update_scores(
            _analysis_id=UUID(str(analysis.id)),
            _coverage_score=analysis_results.overall_metrics.coverage_score,
            complexity_score=analysis_results.overall_metrics.complexity_score,
            _duplication_score=100.0
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
            _analysis_id=UUID(str(analysis.id)),
            critical=critical_issues,
            high=high_issues,
            medium=medium_issues,
            low=low_issues,
        )

        # Complete the analysis
        return await self.complete_analysis(UUID(str(analysis.id)))


# Backward compatibility alias for existing code
QualityAPI = FlextQualityAPI
