"""Quality API module providing high-level interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

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

from .analyzer import CodeAnalyzer
from .entities import FlextQualityEntities
from .models import FlextQualityModels
from .services import FlextQualityServices
from .value_objects import FlextIssueSeverity, FlextIssueType


class FlextQuality(FlextService[None]):
    """Thin facade for quality operations with complete FLEXT integration.

    Integrates:
    - FlextBus: Event emission
    - FlextContainer: Dependency injection
    - FlextContext: Operation context
    - FlextDispatcher: Message routing
    - FlextProcessors: Processing utilities
    - FlextRegistry: Component registration
    - FlextLogger: Advanced logging
    """

    def __init__(self) -> None:
        """Initialize the Quality API with complete FLEXT ecosystem integration."""
        super().__init__()

        # Complete FLEXT ecosystem integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self._logger = FlextLogger(__name__)

        # Domain services
        self._services = FlextQualityServices()

    @property
    def project_service(self) -> FlextQualityServices.ProjectService:
        """Get project service instance."""
        return self._services.get_project_service()

    @property
    def analysis_service(self) -> FlextQualityServices.AnalysisService:
        """Get analysis service instance."""
        return self._services.get_analysis_service()

    @property
    def issue_service(self) -> FlextQualityServices.IssueService:
        """Get issue service instance."""
        return self._services.get_issue_service()

    @property
    def report_service(self) -> FlextQualityServices.ReportService:
        """Get report service instance."""
        return self._services.get_report_service()

    # Project operations
    def create_project(
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
    ) -> FlextResult[FlextQualityEntities.Project]:
        """Create a new quality project."""
        return self.project_service.create_project(
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

    def get_project(
        self,
        _project_id: UUID,
    ) -> FlextResult[FlextQualityEntities.Project]:
        """Get a project by ID."""
        return FlextResult[FlextQualityEntities.Project].fail(
            "get_project not implemented"
        )

    def list_projects(self) -> FlextResult[list[FlextQualityEntities.Project]]:
        """List all projects."""
        return FlextResult[list[FlextQualityEntities.Project]].fail(
            "list_projects not implemented"
        )

    def update_project(
        self,
        _project_id: UUID,
        _updates: FlextTypes.Dict,
    ) -> FlextResult[FlextQualityEntities.Project]:
        """Update a project."""
        return FlextResult[FlextQualityEntities.Project].fail(
            "update_project not implemented"
        )

    def delete_project(self, _project_id: UUID) -> FlextResult[bool]:
        """Delete a project."""
        return FlextResult[bool].fail("delete_project not implemented")

    # Analysis operations
    def create_analysis(
        self,
        project_id: UUID,
        _commit_hash: str | None = None,
        _branch: str | None = None,
        _pull_request_id: str | None = None,
        analysis_config: FlextTypes.JsonDict | None = None,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Create a new quality analysis."""
        return self.analysis_service.create_analysis(
            project_id=str(project_id),
            config=analysis_config
            if analysis_config is None
            else dict(analysis_config),
        )

    def update_metrics(
        self,
        _analysis_id: UUID,
        _total_files: int,
        _total_lines: int,
        _code_lines: int,
        _comment_lines: int,
        _blank_lines: int,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Update analysis metrics."""
        return FlextResult[FlextQualityEntities.Analysis].fail(
            "update_metrics not implemented"
        )

    def update_scores(
        self,
        _analysis_id: UUID,
        _coverage_score: float,
        complexity_score: float,
        _duplication_score: float,
        security_score: float,
        maintainability_score: float,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Update analysis quality scores."""
        # Calculate overall score as average
        (
            _coverage_score + complexity_score + security_score + maintainability_score
        ) / 4.0

        return FlextResult[FlextQualityEntities.Analysis].fail(
            "update_scores not implemented"
        )

    def update_issue_counts(
        self,
        _analysis_id: UUID,
        critical: int,
        high: int,
        medium: int,
        low: int,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Update analysis issue counts by severity."""
        critical + high + medium + low

        return FlextResult[FlextQualityEntities.Analysis].fail(
            "update_issue_counts not implemented"
        )

    def complete_analysis(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Mark analysis as completed."""
        return FlextResult[FlextQualityEntities.Analysis].fail(
            "complete_analysis not implemented"
        )

    def fail_analysis(
        self,
        _analysis_id: UUID,
        _error: str,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Mark analysis as failed."""
        return FlextResult[FlextQualityEntities.Analysis].fail(
            "fail_analysis not implemented"
        )

    def get_analysis(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Get an analysis by ID."""
        return FlextResult[FlextQualityEntities.Analysis].fail(
            "get_analysis not implemented"
        )

    def list_analyses(
        self,
        _project_id: UUID,
    ) -> FlextResult[list[FlextQualityEntities.Analysis]]:
        """List all analyses for a project."""
        return FlextResult[list[FlextQualityEntities.Analysis]].fail(
            "list_analyses not implemented"
        )

    # Issue operations
    def create_issue(
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
    ) -> FlextResult[FlextQualityEntities.Issue]:
        """Create a new quality issue."""
        # Convert string parameters to enum types

        try:
            FlextIssueSeverity(severity)
            FlextIssueType(issue_type)
        except ValueError as e:
            return FlextResult[FlextQualityEntities.Issue].fail(
                f"Invalid severity or issue type: {e}",
            )

        return FlextResult[FlextQualityEntities.Issue].fail(
            "create_issue not implemented"
        )

    def get_issue(self, _issue_id: UUID) -> FlextResult[FlextQualityEntities.Issue]:
        """Get an issue by ID."""
        return FlextResult[FlextQualityEntities.Issue].fail("get_issue not implemented")

    def list_issues(
        self,
        _analysis_id: UUID,
        severity: str | None = None,
        _issue_type: str | None = None,
        _file_path: str | None = None,
    ) -> FlextResult[list[FlextQualityEntities.Issue]]:
        """List issues for an analysis with optional filters."""
        # Convert string severity to enum if provided
        if severity:
            try:
                FlextIssueSeverity(severity)
            except ValueError:
                return FlextResult[list[FlextQualityEntities.Issue]].fail(
                    f"Invalid severity: {severity}",
                )

        return FlextResult[list[FlextQualityEntities.Issue]].fail(
            "list_issues not implemented"
        )

    def mark_issue_fixed(
        self, _issue_id: UUID
    ) -> FlextResult[FlextQualityEntities.Issue]:
        """Mark an issue as fixed."""
        return FlextResult[FlextQualityEntities.Issue].fail(
            "mark_fixed not implemented"
        )

    def suppress_issue(
        self,
        _issue_id: UUID,
        _reason: str,
    ) -> FlextResult[FlextQualityEntities.Issue]:
        """Suppress an issue with a reason."""
        return FlextResult[FlextQualityEntities.Issue].fail(
            "suppress_issue not implemented"
        )

    def unsuppress_issue(
        self, _issue_id: UUID
    ) -> FlextResult[FlextQualityEntities.Issue]:
        """Remove suppression from an issue."""
        return FlextResult[FlextQualityEntities.Issue].fail(
            "unsuppress_issue not implemented"
        )

    # Report operations
    def create_report(
        self,
        _analysis_id: UUID,
        _report_type: str,
        _report_format: str = "summary",
        _report_path: str | None = None,
        _report_size_bytes: int = 0,
    ) -> FlextResult[FlextQualityEntities.Report]:
        """Create a quality report."""
        return FlextResult[FlextQualityEntities.Report].fail(
            "create_report not implemented"
        )

    def get_report(self, _report_id: UUID) -> FlextResult[FlextQualityEntities.Report]:
        """Get a report by ID."""
        return FlextResult[FlextQualityEntities.Report].fail(
            "get_report not implemented"
        )

    def list_reports(
        self,
        _analysis_id: UUID,
    ) -> FlextResult[list[FlextQualityEntities.Report]]:
        """List all reports for an analysis."""
        return FlextResult[list[FlextQualityEntities.Report]].fail(
            "list_reports not implemented"
        )

    def delete_report(self, _report_id: UUID) -> FlextResult[bool]:
        """Delete a report."""
        return FlextResult[bool].fail("delete_report not implemented")

    # High-level operations
    def run_full_analysis(
        self,
        project_id: UUID,
        commit_hash: str | None = None,
        branch: str | None = None,
    ) -> FlextResult[FlextQualityEntities.Analysis]:
        """Run a complete quality analysis for a project."""
        # Create analysis
        result = self.create_analysis(
            project_id=project_id,
            _commit_hash=commit_hash,
            _branch=branch,
        )

        # Use is_failure for early return pattern (current flext-core API)
        if result.is_failure:
            return result
        analysis = result.value

        # Get the project to access its path
        project_result = self.get_project(project_id)
        if project_result.is_failure:
            return FlextResult[FlextQualityEntities.Analysis].fail(
                f"Failed to get project: {project_result.error}",
            )

        project = project_result.value

        # Integrate with real analysis tools using flext-core patterns
        # Execute analysis using CodeAnalyzer
        project_path = Path(project.project_path)
        analyzer = CodeAnalyzer(project_path)
        analysis_result = analyzer.analyze_project()

        # analysis_result is now AnalysisResults directly, not FlextResult
        analysis_results: FlextQualityModels.AnalysisResults = analysis_result

        # Update with real metrics from analysis
        # Note: analysis_results is a Pydantic model
        overall_metrics = analysis_results.overall_metrics
        duplication_issues: list = analysis_results.duplication_issues

        self.update_metrics(
            _analysis_id=UUID(str(analysis.id)),
            _total_files=overall_metrics.files_analyzed,
            _total_lines=overall_metrics.total_lines,
            _code_lines=overall_metrics.total_lines,  # CodeAnalyzer provides total lines
            _comment_lines=0,  # Would need detailed AST analysis
            _blank_lines=0,  # Would need detailed AST analysis
        )

        # Update with real scores from analysis
        self.update_scores(
            _analysis_id=UUID(str(analysis.id)),
            _coverage_score=overall_metrics.coverage_score,
            complexity_score=overall_metrics.complexity_score,
            _duplication_score=100.0
            - len(duplication_issues),  # Convert issues to score
            security_score=overall_metrics.security_score,
            maintainability_score=overall_metrics.maintainability_score,
        )

        # Count real issues by severity
        security_issues: list = analysis_results.security_issues
        complexity_issues: list = analysis_results.complexity_issues

        critical_issues = len(
            [i for i in security_issues if i.get("severity") == "critical"],
        )
        high_issues = len(
            [i for i in security_issues if i.get("severity") == "high"],
        )
        medium_issues = len(
            [i for i in security_issues if i.get("severity") == "medium"],
        )
        low_issues = len(
            [i for i in security_issues if i.get("severity") == "low"],
        )

        # Add complexity issues to high priority
        high_issues += len(complexity_issues)

        # Update with real issue counts
        self.update_issue_counts(
            _analysis_id=UUID(str(analysis.id)),
            critical=critical_issues,
            high=high_issues,
            medium=medium_issues,
            low=low_issues,
        )

        # Complete the analysis
        return self.complete_analysis(UUID(str(analysis.id)))
