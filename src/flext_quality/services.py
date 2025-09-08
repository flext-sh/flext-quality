"""Application services for FLEXT-QUALITY v0.7.0.

Services following flext-cli patterns with multiple service classes per module.
Uses working flext-core imports: FlextResult, FlextLogger.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from pathlib import Path

from flext_core import FlextLogger, FlextProtocols, FlextResult, FlextTypes

from flext_quality.entities import (
    FlextQualityAnalysis,
    FlextQualityIssue,
    FlextQualityProject,
    FlextQualityReport,
)
from flext_quality.external_backend import ExternalBackend
from flext_quality.value_objects import (
    FlextIssueSeverity as IssueSeverity,
    FlextIssueType as IssueType,
)

logger = FlextLogger(__name__)

# Use flext-core protocols instead of local definitions
QualityServiceProtocol = FlextProtocols.Domain.Service
QualityAnalysisServiceProtocol = FlextProtocols.Application.Handler[str, object]
QualityProjectServiceProtocol = FlextProtocols.Domain.Service


class BasicQualityProjectService:
    """Service for managing quality projects using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._projects: dict[str, FlextQualityProject] = {}
        self._logger = FlextLogger(__name__)

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
            # Create project entity
            project = FlextQualityProject(
                id=name,
                name=name,
                path=Path(project_path),
                repository_url=repository_url,
                config_path=Path(config_path) if config_path else None,
                language=language,
                auto_analyze=auto_analyze,
                min_coverage=min_coverage,
                max_complexity=max_complexity,
                max_duplication=max_duplication,
            )

            # Store project
            self._projects[project.id] = project
            self._logger.info("Created project: %s", project.name)
            return FlextResult[FlextQualityProject].ok(project)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create project")
            return FlextResult[FlextQualityProject].fail(
                f"Failed to create project: {e}"
            )


class BasicQualityIssueService:
    """Service for managing quality issues using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._issues: dict[str, FlextQualityIssue] = {}
        self._logger = FlextLogger(__name__)

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

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing the issue or error

            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the issue or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing list of issues or error

            severity: Optional severity filter

        Returns:
            FlextResult containing list of issues or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the updated issue or error

            issue_id: Issue unique identifier

        Returns:
            FlextResult containing the updated issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the suppressed issue or error

            reason: Reason for suppression

        Returns:
            FlextResult containing the suppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

        Returns:
            FlextResult containing the unsuppressed issue or error

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
            self._logger.info("Issue unsuppressed: %s", issue_id)
            return FlextResult[FlextQualityIssue].ok(updated_issue)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to unsuppress issue")
            return FlextResult[FlextQualityIssue].fail(
                f"Failed to unsuppress issue: {e}"
            )


class BasicQualityAnalysisService:
    """Service for managing quality analyses using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._analyses: dict[str, FlextQualityAnalysis] = {}
        self._logger = FlextLogger(__name__)

    async def create_analysis(
        self,
        project_id: str,
        config: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextQualityAnalysis]:
        """Create a new quality analysis.

        Args:
            project_id: Project identifier
            config: Optional configuration overrides

        Returns:
            FlextResult containing the created analysis or error

        """
        try:
            analysis = FlextQualityAnalysis(
                id=f"{project_id}_analysis_{len(self._analyses)}",
                project_id=project_id,
                config=config or {},
            )

            # Store analysis
            self._analyses[analysis.id] = analysis
            self._logger.info("Created analysis: %s", analysis.id)
            return FlextResult[FlextQualityAnalysis].ok(analysis)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to create analysis")
            return FlextResult[FlextQualityAnalysis].fail(
                f"Failed to create analysis: {e}"
            )

    async def get_analyses_by_project(
        self, project_id: str
    ) -> FlextResult[list[FlextQualityAnalysis]]:
        """Get all analyses for a project.

        Args:
            project_id: Project identifier

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
            return FlextResult[list[FlextQualityAnalysis]].fail(
                f"Failed to list analyses: {e}"
            )


class BasicQualityReportService:
    """Service for managing quality reports using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with in-memory repository."""
        self._reports: dict[str, FlextQualityReport] = {}
        self._logger = FlextLogger(__name__)

    async def create_report(
        self,
        analysis_id: str,
        format_type: str,
        content: str,
        file_path: str | None = None,
        metadata: FlextTypes.Core.Dict | None = None,
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

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing the report or error

            report_id: Report unique identifier

        Returns:
            FlextResult containing the report or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing list of reports or error

            analysis_id: Analysis unique identifier

        Returns:
            FlextResult containing list of reports or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

        Returns:
            FlextResult containing success status or error

            report_id: Report unique identifier

        Returns:
            FlextResult containing success status or error

        """
        try:
            if report_id in self._reports:
                del self._reports[report_id]
                self._logger.info("Report deleted successfully: %s", report_id)
                success = True
                return FlextResult[bool].ok(success)
            return FlextResult[bool].fail("Report not found")
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to delete report")
            return FlextResult[bool].fail(f"Failed to delete report: {e}")


class ExternalAnalysisService:
    """Service for external backend analysis using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize service with external backend."""
        self._backend = ExternalBackend()
        self._logger = FlextLogger(__name__)

    async def analyze_with_backend(
        self,
        code: str,
        file_path: Path | None = None,
        backend_tool: str = "ruff",
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Analyze code using external backend tools.

        Args:
            code: Source code to analyze
            file_path: Optional file path for context
            backend_tool: Backend tool to use (ruff, mypy, bandit, vulture)

        Returns:
            FlextResult containing analysis results or error

        """
        try:
            self._logger.info("Running %s analysis", backend_tool)
            result = self._backend.analyze(code, file_path, tool=backend_tool)
            return FlextResult[FlextTypes.Core.Dict].ok(result)
        except (RuntimeError, ValueError, TypeError) as e:
            self._logger.exception("Failed to analyze with external backend")
            return FlextResult[FlextTypes.Core.Dict].fail(
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
