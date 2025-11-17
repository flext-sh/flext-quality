"""FLEXT Quality Services - V2 Architecture with Pure Monadic & Builder Patterns.

SINGLE CLASS MODULE with FlextService V2 (no V1 methods), pure Railway-Oriented
Programming (ROP), and fluent builder patterns for composable, type-safe operations.

Architecture: Layer 3 (Application)
Pattern: V2 FlextService with monadic chains and fluent builders ONLY

Usage:
    services = FlextQualityServices(config)

    # Create project via builder chain
    project_result = (
        ProjectServiceBuilder(config, logger)
        .with_name("my_project")
        .with_path("/path/to/project")
        .build()
    )

    # Create analysis via monadic builder
    analysis_result = (
        AnalysisServiceBuilder(config, logger)
        .with_project_id(project_id)
        .build()
    )

    # Chain multiple operations monadically
    full_workflow = (
        ProjectServiceBuilder(config, logger)
        .with_name("project")
        .with_path("/path")
        .build()
        .flat_map(lambda proj: (
            AnalysisServiceBuilder(config, logger)
            .with_project_id(proj.id)
            .build()
        ))
        .flat_map(lambda analysis: (
            IssueServiceBuilder(config, logger)
            .with_analysis_id(analysis.id)
            .with_severity("HIGH")
            .with_issue_type("COMPLEXITY")
            .with_file_path("src/module.py")
            .with_message("High complexity function")
            .build()
        ))
        .map(lambda issue: issue.id)
    )

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override
from uuid import NAMESPACE_DNS, UUID, uuid5

from flext_core import FlextLogger, FlextResult

from .base_service import FlextQualityBaseService
from .config import FlextQualityConfig
from .models import FlextQualityModels


class FlextQualityServices(FlextQualityBaseService[bool]):
    """Unified services with V2 FlextService pattern.

    Pure builder architecture: All operations via fluent builders.
    No convenience methods. No V1 patterns.
    Monadic composition via flat_map and map chains.

    Usage: Instantiate services object, use static builders for operations.
    """

    # FlextService V2: Property pattern (auto_execute=False)
    auto_execute = False

    @override
    def execute(self, data: object = None) -> FlextResult[bool]:
        """Execute services - returns True to indicate service is ready.

        V2 pattern: No meaningless data, just success/failure indication.
        """
        return FlextResult.ok(True)


# ============================================================================
# PROJECT SERVICE - BUILDER + MONADIC PATTERN
# ============================================================================


class ProjectServiceBuilder:
    """Fluent builder for ProjectModel with monadic validation chain.

    Pattern: Builder + Railway-Oriented Programming
    Usage:
        result = (
            ProjectServiceBuilder(config, logger)
            .with_name("my_project")
            .with_path("/path/to/project")
            .with_config_dict({"key": "value"})
            .build()
        )
    """

    def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
        """Initialize project builder."""
        self._config = config
        self._logger = logger
        self._name: str | None = None
        self._path: str | None = None
        self._kwargs: dict[str, object] = {}

    def with_name(self, name: str) -> ProjectServiceBuilder:
        """Set project name (fluent)."""
        self._name = name
        return self

    def with_path(self, path: str) -> ProjectServiceBuilder:
        """Set project path (fluent)."""
        self._path = path
        return self

    def with_config_dict(self, config_dict: dict[str, object]) -> ProjectServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> FlextResult[FlextQualityModels.ProjectModel]:
        """Build project using monadic validation chain.

        Returns:
            FlextResult[ProjectModel] via railway pattern:
            - Success: ProjectModel instance
            - Failure: Error message with validation details

        """
        return (
            self._validate_required_fields()
            .flat_map(lambda _: self._create_project_model())
            .map(lambda project: self._log_project_creation(project))  # noqa: PLW0108
        )

    def _validate_required_fields(self) -> FlextResult[bool]:
        """Validate required project fields (monadic step 1)."""
        if not self._name:
            return FlextResult.fail("Project name is required")
        if not self._path:
            return FlextResult.fail("Project path is required")
        return FlextResult.ok(True)

    def _create_project_model(self) -> FlextResult[FlextQualityModels.ProjectModel]:
        """Create project model (monadic step 2)."""
        try:
            project = FlextQualityModels.ProjectModel(
                id=f"project_{self._name.lower().replace(' ', '_')}",
                name=self._name,
                path=self._path,
                **self._kwargs,
            )
            return FlextResult.ok(project)
        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Project creation failed: {e}")

    def _log_project_creation(
        self, project: FlextQualityModels.ProjectModel
    ) -> FlextQualityModels.ProjectModel:
        """Log project creation and return (monadic final step)."""
        self._logger.info(
            "Project created successfully",
            project_id=project.id,
            project_name=project.name,
        )
        return project


# ============================================================================
# ANALYSIS SERVICE - BUILDER + MONADIC PATTERN
# ============================================================================


class AnalysisServiceBuilder:
    """Fluent builder for AnalysisModel with monadic validation chain.

    Pattern: Builder + Railway-Oriented Programming
    Usage:
        result = (
            AnalysisServiceBuilder(config, logger)
            .with_project_id("project_123")
            .with_status(AnalysisStatus.QUEUED)
            .build()
        )
    """

    def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
        """Initialize analysis builder."""
        self._config = config
        self._logger = logger
        self._project_id: str | UUID | None = None
        self._status: str = "queued"
        self._kwargs: dict[str, object] = {}

    def with_project_id(self, project_id: str | UUID) -> AnalysisServiceBuilder:
        """Set project ID (fluent)."""
        self._project_id = project_id
        return self

    def with_status(
        self, status: str | FlextQualityModels.AnalysisStatus
    ) -> AnalysisServiceBuilder:
        """Set analysis status (fluent)."""
        self._status = str(status.value) if hasattr(status, "value") else str(status)
        return self

    def with_config_dict(
        self, config_dict: dict[str, object]
    ) -> AnalysisServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> FlextResult[FlextQualityModels.AnalysisModel]:
        """Build analysis using monadic validation chain.

        Returns:
            FlextResult[AnalysisModel] via railway pattern

        """
        return (
            self._validate_project_id()
            .flat_map(lambda _: self._validate_status())
            .flat_map(lambda _: self._create_analysis_model())
            .map(lambda analysis: self._log_analysis_creation(analysis))  # noqa: PLW0108
        )

    def _validate_project_id(self) -> FlextResult[bool]:
        """Validate project ID (monadic step 1)."""
        if not self._project_id:
            return FlextResult.fail("Project ID is required for analysis")
        return FlextResult.ok(True)

    def _validate_status(self) -> FlextResult[bool]:
        """Validate analysis status enum (monadic step 2)."""
        try:
            FlextQualityModels.AnalysisStatus(self._status)
            return FlextResult.ok(True)
        except ValueError:
            return FlextResult.fail(f"Invalid analysis status: {self._status}")

    def _create_analysis_model(self) -> FlextResult[FlextQualityModels.AnalysisModel]:
        """Create analysis model (monadic step 3)."""
        try:
            project_uuid = (
                self._project_id
                if isinstance(self._project_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._project_id))
            )
            analysis = FlextQualityModels.AnalysisModel(
                project_id=project_uuid,
                status=self._status,
                **self._kwargs,
            )
            return FlextResult.ok(analysis)
        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Analysis creation failed: {e}")

    def _log_analysis_creation(
        self, analysis: FlextQualityModels.AnalysisModel
    ) -> FlextQualityModels.AnalysisModel:
        """Log analysis creation and return (monadic final step)."""
        self._logger.info(
            "Analysis created successfully",
            analysis_id=analysis.id,
            project_id=analysis.project_id,
            status=self._status,
        )
        return analysis


# ============================================================================
# ISSUE SERVICE - BUILDER + MONADIC PATTERN
# ============================================================================


class IssueServiceBuilder:
    """Fluent builder for IssueModel with monadic validation chain.

    Pattern: Builder + Railway-Oriented Programming
    Usage:
        result = (
            IssueServiceBuilder(config, logger)
            .with_analysis_id("analysis_123")
            .with_severity("HIGH")
            .with_issue_type("high_complexity")
            .with_file_path("src/module.py")
            .with_message("Function complexity too high")
            .build()
        )
    """

    def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
        """Initialize issue builder."""
        self._config = config
        self._logger = logger
        self._analysis_id: str | UUID | None = None
        self._severity: str | None = None
        self._issue_type: str | None = None
        self._file_path: str | None = None
        self._message: str | None = None
        self._kwargs: dict[str, object] = {}

    def with_analysis_id(self, analysis_id: str | UUID) -> IssueServiceBuilder:
        """Set analysis ID (fluent)."""
        self._analysis_id = analysis_id
        return self

    def with_severity(self, severity: str) -> IssueServiceBuilder:
        """Set issue severity (fluent)."""
        self._severity = severity
        return self

    def with_issue_type(self, issue_type: str) -> IssueServiceBuilder:
        """Set issue type (fluent)."""
        self._issue_type = issue_type
        return self

    def with_file_path(self, file_path: str) -> IssueServiceBuilder:
        """Set file path where issue was found (fluent)."""
        self._file_path = file_path
        return self

    def with_message(self, message: str) -> IssueServiceBuilder:
        """Set issue message (fluent)."""
        self._message = message
        return self

    def with_config_dict(self, config_dict: dict[str, object]) -> IssueServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> FlextResult[FlextQualityModels.IssueModel]:
        """Build issue using monadic validation chain.

        Returns:
            FlextResult[IssueModel] via railway pattern with multi-step validation

        """
        return (
            self._validate_required_fields()
            .flat_map(lambda _: self._validate_enums())
            .flat_map(lambda _: self._create_issue_model())
            .map(lambda issue: self._log_issue_creation(issue))  # noqa: PLW0108
        )

    def _validate_required_fields(self) -> FlextResult[bool]:
        """Validate all required fields (monadic step 1)."""
        if not self._analysis_id:
            return FlextResult.fail("Analysis ID is required")
        if not self._severity:
            return FlextResult.fail("Severity is required")
        if not self._issue_type:
            return FlextResult.fail("Issue type is required")
        if not self._file_path:
            return FlextResult.fail("File path is required")
        if not self._message:
            return FlextResult.fail("Message is required")
        return FlextResult.ok(True)

    def _validate_enums(self) -> FlextResult[bool]:
        """Validate enum values (monadic step 2)."""
        try:
            FlextQualityModels.IssueSeverity(self._severity)
            FlextQualityModels.IssueType(self._issue_type)
            return FlextResult.ok(True)
        except ValueError as e:
            return FlextResult.fail(f"Invalid enum value: {e}")

    def _create_issue_model(self) -> FlextResult[FlextQualityModels.IssueModel]:
        """Create issue model (monadic step 3)."""
        try:
            analysis_uuid = (
                self._analysis_id
                if isinstance(self._analysis_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._analysis_id))
            )
            issue = FlextQualityModels.IssueModel(
                analysis_id=analysis_uuid,
                severity=self._severity,
                issue_type=self._issue_type,
                file_path=self._file_path,
                message=self._message,
                **self._kwargs,
            )
            return FlextResult.ok(issue)
        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Issue creation failed: {e}")

    def _log_issue_creation(
        self, issue: FlextQualityModels.IssueModel
    ) -> FlextQualityModels.IssueModel:
        """Log issue creation and return (monadic final step)."""
        self._logger.info(
            "Issue created successfully",
            issue_id=issue.id,
            severity=self._severity,
            issue_type=self._issue_type,
        )
        return issue


# ============================================================================
# REPORT SERVICE - BUILDER + MONADIC PATTERN
# ============================================================================


class ReportServiceBuilder:
    """Fluent builder for ReportModel with monadic validation chain.

    Pattern: Builder + Railway-Oriented Programming
    Usage:
        result = (
            ReportServiceBuilder(config, logger)
            .with_analysis_id("analysis_123")
            .with_format("HTML")
            .with_config_dict({"include_charts": True})
            .build()
        )
    """

    def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
        """Initialize report builder."""
        self._config = config
        self._logger = logger
        self._analysis_id: str | UUID | None = None
        self._format_type: str = "HTML"
        self._kwargs: dict[str, object] = {}

    def with_analysis_id(self, analysis_id: str | UUID) -> ReportServiceBuilder:
        """Set analysis ID (fluent)."""
        self._analysis_id = analysis_id
        return self

    def with_format(self, format_type: str) -> ReportServiceBuilder:
        """Set report format (fluent)."""
        self._format_type = format_type
        return self

    def with_config_dict(self, config_dict: dict[str, object]) -> ReportServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> FlextResult[FlextQualityModels.ReportModel]:
        """Build report using monadic validation chain.

        Returns:
            FlextResult[ReportModel] via railway pattern

        """
        return (
            self._validate_analysis_id()
            .flat_map(lambda _: self._validate_format())
            .flat_map(lambda _: self._create_report_model())
            .map(lambda report: self._log_report_creation(report))  # noqa: PLW0108
        )

    def _validate_analysis_id(self) -> FlextResult[bool]:
        """Validate analysis ID (monadic step 1)."""
        if not self._analysis_id:
            return FlextResult.fail("Analysis ID is required for report")
        return FlextResult.ok(True)

    def _validate_format(self) -> FlextResult[bool]:
        """Validate report format (monadic step 2)."""
        valid_formats = {"JSON", "HTML", "CSV"}
        if self._format_type.upper() not in valid_formats:
            return FlextResult.fail(
                f"Invalid format. Must be one of: {', '.join(valid_formats)}"
            )
        return FlextResult.ok(True)

    def _create_report_model(self) -> FlextResult[FlextQualityModels.ReportModel]:
        """Create report model (monadic step 3)."""
        try:
            analysis_uuid = (
                self._analysis_id
                if isinstance(self._analysis_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._analysis_id))
            )
            report = FlextQualityModels.ReportModel(
                analysis_id=analysis_uuid,
                format_type=self._format_type,
                **self._kwargs,
            )
            return FlextResult.ok(report)
        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Report creation failed: {e}")

    def _log_report_creation(
        self, report: FlextQualityModels.ReportModel
    ) -> FlextQualityModels.ReportModel:
        """Log report creation and return (monadic final step)."""
        self._logger.info(
            "Report created successfully",
            report_id=report.id,
            format=self._format_type,
        )
        return report


__all__ = [
    "AnalysisServiceBuilder",
    "FlextQualityServices",
    "IssueServiceBuilder",
    "ProjectServiceBuilder",
    "ReportServiceBuilder",
]
