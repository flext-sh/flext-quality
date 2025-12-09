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

from typing import ClassVar, override
from uuid import NAMESPACE_DNS, UUID, uuid5

from flext_core import FlextLogger, r

from .base_service import FlextQualityBaseService
from .config import FlextQualityConfig
from .constants import c
from .models import m


class FlextQualityServices(FlextQualityBaseService[bool]):
    """Unified services with V2 FlextService pattern.

    Pure builder architecture: All operations via fluent builders.
    No convenience methods. No V1 patterns.
    Monadic composition via flat_map and map chains.

    Usage: Instantiate services object, use static builders for operations.
    """

    # FlextService V2: Property pattern (auto_execute=False)
    auto_execute: ClassVar[bool] = False

    @override
    def execute(self, data: object = None) -> r[bool]:
        """Execute services - returns True to indicate service is ready.

        V2 pattern: No meaningless data, just success/failure indication.
        """
        return r.ok(True)


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

    def build(self) -> r[m.ProjectModel]:
        """Build project using monadic validation chain.

        Returns:
            r[ProjectModel] via railway pattern:
            - Success: ProjectModel instance
            - Failure: Error message with validation details

        """
        return (
            self._validate_required_fields()
            .flat_map(lambda _: self._create_project_model())
            .map(self._log_project_creation)
        )

    def _validate_required_fields(self) -> r[bool]:
        """Validate required project fields (monadic step 1)."""
        if not self._name:
            return r.fail("Project name is required")
        if not self._path:
            return r.fail("Project path is required")
        return r.ok(True)

    def _create_project_model(self) -> r[m.ProjectModel]:
        """Create project model (monadic step 2)."""
        try:
            # Type narrowing after validation
            name = self._name if isinstance(self._name, str) else ""
            path = self._path if isinstance(self._path, str) else ""
            project = m.ProjectModel(
                id=f"project_{name.lower().replace(' ', '_')}",
                name=name,
                path=path,
                **self._kwargs,
            )
            return r.ok(project)
        except (ValueError, TypeError) as e:
            return r.fail(f"Project creation failed: {e}")

    def _log_project_creation(
        self,
        project: m.ProjectModel,
    ) -> m.ProjectModel:
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
            .with_status(m.AnalysisStatus.QUEUED)
            .build()
        )
    """

    def __init__(self, config: FlextQualityConfig, logger: FlextLogger) -> None:
        """Initialize analysis builder."""
        self._config = config
        self._logger = logger
        self._project_id: str | UUID | None = None
        self._status: c.Quality.Literals.AnalysisStatusLiteral | str = "queued"
        self._kwargs: dict[str, object] = {}

    def with_project_id(self, project_id: str | UUID) -> AnalysisServiceBuilder:
        """Set project ID (fluent)."""
        self._project_id = project_id
        return self

    def with_status(
        self,
        status: (c.Quality.Literals.AnalysisStatusLiteral | str | m.AnalysisStatus),
    ) -> AnalysisServiceBuilder:
        """Set analysis status (fluent)."""
        if isinstance(status, m.AnalysisStatus):
            self._status = status.value
        else:
            self._status = str(status)
        return self

    def with_config_dict(
        self,
        config_dict: dict[str, object],
    ) -> AnalysisServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> r[m.AnalysisModel]:
        """Build analysis using monadic validation chain.

        Returns:
            r[AnalysisModel] via railway pattern

        """
        return (
            self._validate_project_id()
            .flat_map(lambda _: self._validate_status())
            .flat_map(lambda _: self._create_analysis_model())
            .map(self._log_analysis_creation)
        )

    def _validate_project_id(self) -> r[bool]:
        """Validate project ID (monadic step 1)."""
        if not self._project_id:
            return r.fail("Project ID is required for analysis")
        return r.ok(True)

    def _validate_status(self) -> r[bool]:
        """Validate analysis status enum (monadic step 2)."""
        try:
            m.AnalysisStatus(self._status)
            return r.ok(True)
        except ValueError:
            return r.fail(f"Invalid analysis status: {self._status}")

    def _create_analysis_model(self) -> r[m.AnalysisModel]:
        """Create analysis model (monadic step 3)."""
        try:
            project_uuid = (
                self._project_id
                if isinstance(self._project_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._project_id))
            )
            analysis = m.AnalysisModel(
                project_id=project_uuid,
                status=self._status,
            )
            return r.ok(analysis)
        except (ValueError, TypeError) as e:
            return r.fail(f"Analysis creation failed: {e}")

    def _log_analysis_creation(
        self,
        analysis: m.AnalysisModel,
    ) -> m.AnalysisModel:
        """Log analysis creation and return (monadic final step)."""
        self._logger.info(
            "Analysis created successfully",
            analysis_id=str(analysis.id),
            project_id=str(analysis.project_id),
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

    def with_issue_type(
        self,
        issue_type: c.Quality.Literals.IssueTypeLiteral | str,
    ) -> IssueServiceBuilder:
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

    def build(self) -> r[m.IssueModel]:
        """Build issue using monadic validation chain.

        Returns:
            r[IssueModel] via railway pattern with multi-step validation

        """
        return (
            self._validate_required_fields()
            .flat_map(lambda _: self._validate_enums())
            .flat_map(lambda _: self._create_issue_model())
            .map(self._log_issue_creation)
        )

    def _validate_required_fields(self) -> r[bool]:
        """Validate all required fields (monadic step 1)."""
        if not self._analysis_id:
            return r.fail("Analysis ID is required")
        if not self._severity:
            return r.fail("Severity is required")
        if not self._issue_type:
            return r.fail("Issue type is required")
        if not self._file_path:
            return r.fail("File path is required")
        if not self._message:
            return r.fail("Message is required")
        return r.ok(True)

    def _validate_enums(self) -> r[bool]:
        """Validate enum values (monadic step 2)."""
        try:
            # Type narrowing for enum values
            severity = self._severity if isinstance(self._severity, str) else ""
            issue_type = self._issue_type if isinstance(self._issue_type, str) else ""
            m.IssueSeverity(severity)
            m.IssueType(issue_type)
            return r.ok(True)
        except ValueError as e:
            return r.fail(f"Invalid enum value: {e}")

    def _create_issue_model(self) -> r[m.IssueModel]:
        """Create issue model (monadic step 3)."""
        try:
            # Type narrowing after validation
            analysis_uuid = (
                self._analysis_id
                if isinstance(self._analysis_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._analysis_id))
            )
            severity = self._severity if isinstance(self._severity, str) else "MEDIUM"
            issue_type = self._issue_type if isinstance(self._issue_type, str) else "UNKNOWN"
            file_path = self._file_path if isinstance(self._file_path, str) else ""
            message = self._message if isinstance(self._message, str) else ""
            issue = m.IssueModel(
                analysis_id=analysis_uuid,
                severity=severity,
                issue_type=issue_type,
                file_path=file_path,
                message=message,
            )
            return r.ok(issue)
        except (ValueError, TypeError) as e:
            return r.fail(f"Issue creation failed: {e}")

    def _log_issue_creation(
        self,
        issue: m.IssueModel,
    ) -> m.IssueModel:
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
        self._format_type: c.Quality.Literals.ReportFormatLiteral | str = "HTML"
        self._kwargs: dict[str, object] = {}

    def with_analysis_id(self, analysis_id: str | UUID) -> ReportServiceBuilder:
        """Set analysis ID (fluent)."""
        self._analysis_id = analysis_id
        return self

    def with_format(
        self,
        format_type: c.Quality.Literals.ReportFormatLiteral | str,
    ) -> ReportServiceBuilder:
        """Set report format (fluent)."""
        self._format_type = format_type
        return self

    def with_config_dict(self, config_dict: dict[str, object]) -> ReportServiceBuilder:
        """Set additional configuration (fluent)."""
        self._kwargs.update(config_dict)
        return self

    def build(self) -> r[m.ReportModel]:
        """Build report using monadic validation chain.

        Returns:
            r[ReportModel] via railway pattern

        """
        return (
            self._validate_analysis_id()
            .flat_map(lambda _: self._validate_format())
            .flat_map(lambda _: self._create_report_model())
            .map(self._log_report_creation)
        )

    def _validate_analysis_id(self) -> r[bool]:
        """Validate analysis ID (monadic step 1)."""
        if not self._analysis_id:
            return r.fail("Analysis ID is required for report")
        return r.ok(True)

    def _validate_format(self) -> r[bool]:
        """Validate report format (monadic step 2)."""
        valid_formats = {"JSON", "HTML", "CSV"}
        if self._format_type.upper() not in valid_formats:
            return r.fail(
                f"Invalid format. Must be one of: {', '.join(valid_formats)}",
            )
        return r.ok(True)

    def _create_report_model(self) -> r[m.ReportModel]:
        """Create report model (monadic step 3)."""
        try:
            analysis_uuid = (
                self._analysis_id
                if isinstance(self._analysis_id, UUID)
                else uuid5(NAMESPACE_DNS, str(self._analysis_id))
            )
            report = m.ReportModel(
                analysis_id=analysis_uuid,
                format_type=self._format_type,
                **self._kwargs,
            )
            return r.ok(report)
        except (ValueError, TypeError) as e:
            return r.fail(f"Report creation failed: {e}")

    def _log_report_creation(
        self,
        report: m.ReportModel,
    ) -> m.ReportModel:
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
