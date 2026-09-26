"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping, MutableSequence

# Why: mro-fix-27vfb — `Path` backs a real Pydantic model field
# (ExecutionRequest.script_path) and must resolve at runtime; a
# TYPE_CHECKING-only import leaves that field unresolved and the model
# unbuildable at first instantiation (model_rebuild() is prohibited).
from pathlib import Path
from typing import Annotated

from flext_infra import (
    FlextInfraModels as _InfraModels,
    FlextInfraUtilities as _InfraUtilities,
)
from flext_web import FlextWebModels as _WebModels

from flext_quality import FlextQualityConstants as c, FlextQualityTypes as t
from flext_quality._model_defaults import FlextQualityModelDefaults


class FlextQualityModels(_InfraModels, _WebModels):
    """Namespace for flext-quality models."""

    class Quality:
        """Quality-specific models namespace."""

        AuditMetrics = FlextQualityModelDefaults.AuditMetrics
        QualityThresholdsConfig = FlextQualityModelDefaults.QualityThresholdsConfig
        ContentChecksConfig = FlextQualityModelDefaults.ContentChecksConfig
        SeverityLevelsConfig = FlextQualityModelDefaults.SeverityLevelsConfig
        MarkdownStyleConfig = FlextQualityModelDefaults.MarkdownStyleConfig
        AccessibilityConfig = FlextQualityModelDefaults.AccessibilityConfig
        FormattingConfig = FlextQualityModelDefaults.FormattingConfig
        LinkValidationConfig = FlextQualityModelDefaults.LinkValidationConfig
        ContentAnalysisConfig = FlextQualityModelDefaults.ContentAnalysisConfig

        @staticmethod
        def _empty_list_str() -> MutableSequence[str]:
            return []

        @staticmethod
        def _empty_dict_str_str() -> t.StrMapping:
            return dict[str, str]()

        @staticmethod
        def _empty_list_dict_str_str() -> MutableSequence[t.MutableStrMapping]:
            return []

        class RuleDefinition(_InfraModels.BaseModel):
            """A rule definition from YAML."""

            name: str
            type: c.Quality.RuleType
            description: str
            pattern: str | None = None
            action: str
            enabled: bool = True

        class Issue(_InfraModels.BaseModel):
            """Canonical issue model for documentation tooling."""

            type: Annotated[
                str,
                _InfraUtilities.Field(
                    description="FlextQualityModels.Quality.Issue type identifier"
                ),
            ]
            severity: Annotated[
                str, _InfraUtilities.Field(description="Severity level identifier")
            ]
            file: Annotated[
                str,
                _InfraUtilities.Field(description="File path where issue was found"),
            ]
            line: Annotated[
                int | None,
                _InfraUtilities.Field(
                    description="FlextQualityModels.Quality.Issue line number"
                ),
            ] = None
            description: Annotated[
                str,
                _InfraUtilities.Field(
                    description="FlextQualityModels.Quality.Issue description"
                ),
            ] = ""
            recommendation: Annotated[
                str, _InfraUtilities.Field(description="Recommended fix")
            ] = ""
            context: Annotated[
                t.MappingKV[str, t.Primitives | None] | None,
                _InfraUtilities.Field(default=None),
            ]

            def to_dict(
                self,
            ) -> t.MappingKV[
                str, str | int | t.MappingKV[str, t.Primitives | None] | None
            ]:
                """Convert issue to dictionary representation."""
                context: t.MutableMappingKV[str, t.Primitives | None] = {}
                return {
                    "type": self.type,
                    "severity": self.severity,
                    "file": self.file,
                    "line": self.line,
                    "description": self.description,
                    "recommendation": self.recommendation,
                    "context": self.context if self.context is not None else context,
                }

        class ValidationResult(_InfraModels.BaseModel):
            """Canonical validation result for documentation tooling."""

            total_items: int = 0
            valid_items: int = 0
            invalid_items: int = 0
            issues: MutableSequence[FlextQualityModels.Quality.Issue] = (
                _InfraUtilities.Field(default_factory=list)
            )
            warnings: MutableSequence[str] = _InfraUtilities.Field(default_factory=list)
            errors: MutableSequence[str] = _InfraUtilities.Field(default_factory=list)
            metadata: MutableMapping[str, t.Primitives] = _InfraUtilities.Field(
                default_factory=dict
            )

            @property
            def success_rate(self) -> float:
                """Success rate as a percentage."""
                if self.total_items == 0:
                    return 100.0
                return (self.valid_items / self.total_items) * 100.0

            def add_issue(self, issue: FlextQualityModels.Quality.Issue) -> None:
                """Add an issue to the validation result."""
                self.issues.append(issue)
                if issue.severity == "critical":
                    self.invalid_items += 1
                else:
                    self.valid_items += 1

        class FileMetadata(_InfraModels.BaseModel):
            """Metadata about a documentation file."""

            path: str
            size: int = 0
            modified_time: float = 0.0
            extension: str = ""
            is_markdown: bool = False
            lines: int = 0
            words: int = 0

        class ScheduleTaskConfig(_InfraModels.BaseModel):
            """Task configuration for scheduled documentation maintenance."""

            description: str
            command: str
            timeout: Annotated[t.PositiveInt, _InfraUtilities.Field(default=300)]

        class ScheduleEntry(_InfraModels.BaseModel):
            """Single schedule entry definition."""

            enabled: bool = True
            time: str
            tasks: t.StrSequence = _InfraUtilities.Field(default_factory=list)
            day: str | None = None

        class ErrorHandlingConfig(_InfraModels.BaseModel):
            """Error handling settings for scheduled maintenance."""

            max_retries: Annotated[t.NonNegativeInt, _InfraUtilities.Field(default=3)]
            retry_delay: Annotated[t.NonNegativeInt, _InfraUtilities.Field(default=60)]
            fail_fast: bool = False
            notify_on_failure: bool = True

        class LoggingConfig(_InfraModels.BaseModel):
            """Logging configuration for scheduled maintenance."""

            enabled: bool = True
            log_file: str
            max_log_size: str = "10MB"
            retention_days: Annotated[t.PositiveInt, _InfraUtilities.Field(default=30)]

        class MaintenanceConfig(_InfraModels.BaseModel):
            """Root configuration for scheduled documentation maintenance."""

            enabled: bool = True
            reports_dir: str
            backup_dir: str
            schedules: MutableMapping[str, FlextQualityModels.Quality.ScheduleEntry] = (
                _InfraUtilities.Field(default_factory=dict)
            )
            tasks: MutableMapping[
                str, FlextQualityModels.Quality.ScheduleTaskConfig
            ] = _InfraUtilities.Field(default_factory=dict)
            error_handling: FlextQualityModels.Quality.ErrorHandlingConfig
            logging: FlextQualityModels.Quality.LoggingConfig

        class ScheduleResults(_InfraModels.BaseModel):
            """Execution summary for scheduled maintenance runs."""

            start_time: str
            tasks_completed: int = 0
            errors: MutableSequence[str] = _InfraUtilities.Field(default_factory=list)
            warnings: MutableSequence[str] = _InfraUtilities.Field(default_factory=list)
            end_time: str = ""
            duration_seconds: int = 0

        class ArgumentOptionSpec(_InfraModels.BaseModel):
            """Typed argparse option spec for quality tooling."""

            flags: t.StrSequence
            help: str
            action: c.Quality.ArgumentAction | None = None
            default: t.JsonValue | None = None
            value_type: c.Quality.ArgumentValueType | None = None
            nargs: int | str | None = None
            choices: t.StrSequence | None = None
            dest: str | None = None

        class ArgumentParserSpec(_InfraModels.BaseModel):
            """Typed parser spec consumed by canonical quality utilities."""

            description: str
            options: t.SequenceOf[FlextQualityModels.Quality.ArgumentOptionSpec]

        class AuditRecommendation(_InfraModels.BaseModel):
            """Typed recommendation from documentation audit."""

            priority: str
            category: str
            recommendation: str
            actions: t.StrSequence = _InfraUtilities.Field(default_factory=list)

        class AuditorResults(_InfraModels.BaseModel):
            """Results for documentation audit execution."""

            timestamp: str
            files_analyzed: int = 0
            issues: MutableSequence[
                MutableMapping[
                    str,
                    t.Primitives | t.StrSequence | t.SequenceOf[t.StrMapping] | None,
                ]
            ] = _InfraUtilities.Field(
                default_factory=list[
                    MutableMapping[
                        str,
                        t.Primitives
                        | t.StrSequence
                        | t.SequenceOf[t.StrMapping]
                        | None,
                    ]
                ]
            )
            metrics: FlextQualityModels.Quality.AuditMetrics = _InfraUtilities.Field(
                default_factory=FlextQualityModelDefaults.AuditMetrics
            )
            recommendations: MutableSequence[
                FlextQualityModels.Quality.AuditRecommendation
            ] = _InfraUtilities.Field(default_factory=list)

        class LinkRecord(_InfraModels.BaseModel):
            """Record of a link found in documentation."""

            text: str
            url: str
            type: str
            file: str
            line_number: int | None = None

        class LinkCheckResult(_InfraModels.BaseModel):
            """Result of checking a single link."""

            valid: bool | None = None
            url: str | None = None
            file: str | None = None
            line: int | None = None
            status_code: int | None = None
            error: str | None = None
            type: str | None = None
            target: str | None = None
            src: str | None = None
            text: str | None = None
            anchor: str | None = None
            warning: str | None = None

        class ContentIssue(_InfraModels.BaseModel):
            """FlextQualityModels.Quality.Issue found in documentation content."""

            type: str
            file: str | None = None
            line: int | None = None
            content: str | None = None
            error: str | None = None
            word_count: int | None = None
            readability_score: float | None = None
            warning: str | None = None

        class LinkValidatorResults(_InfraModels.BaseModel):
            """Results for documentation link validation."""

            timestamp: str
            links_checked: int = 0
            valid_links: int = 0
            broken_links: int = 0
            warnings: int = 0
            errors: MutableSequence[FlextQualityModels.Quality.LinkCheckResult] = (
                _InfraUtilities.Field(default_factory=list)
            )
            warnings_list: MutableSequence[
                FlextQualityModels.Quality.LinkCheckResult
            ] = _InfraUtilities.Field(default_factory=list)

        class ContentValidatorResults(_InfraModels.BaseModel):
            """Results for documentation content validation."""

            timestamp: str
            files_checked: int = 0
            content_issues: MutableSequence[FlextQualityModels.Quality.ContentIssue] = (
                _InfraUtilities.Field(default_factory=list)
            )
            quality_metrics: t.MutableScalarMapping = _InfraUtilities.Field(
                default_factory=dict
            )

        class ContentMetrics(_InfraModels.BaseModel):
            """Content quality metrics for a documentation file."""

            word_count: int = 0
            sentence_count: int = 0
            avg_words_per_sentence: float = 0.0
            readability_score: float = 0.0
            has_code_blocks: bool = False
            has_lists: bool = False
            has_headers: bool = False

        class ChannelConfig(_InfraModels.BaseModel):
            """Notification channel toggle configuration."""

            enabled: bool = True

        class NotifierResults(_InfraModels.BaseModel):
            """Results for documentation notification runs."""

            notifications_sent: int = 0
            errors: MutableSequence[str] = _InfraUtilities.Field(default_factory=list)
            timestamp: str

        class AuditRulesConfig(_InfraModels.BaseModel):
            """Configuration for audit rules and thresholds."""

            quality_thresholds: FlextQualityModels.Quality.QualityThresholdsConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.QualityThresholdsConfig
                )
            )
            content_checks: FlextQualityModels.Quality.ContentChecksConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.ContentChecksConfig
                )
            )
            severity_levels: FlextQualityModels.Quality.SeverityLevelsConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.SeverityLevelsConfig
                )
            )

        class StyleGuideConfig(_InfraModels.BaseModel):
            """Configuration for style guide rules."""

            markdown: FlextQualityModels.Quality.MarkdownStyleConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.MarkdownStyleConfig
                )
            )
            accessibility: FlextQualityModels.Quality.AccessibilityConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.AccessibilityConfig
                )
            )
            formatting: FlextQualityModels.Quality.FormattingConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.FormattingConfig
                )
            )

        class ValidationConfig(_InfraModels.BaseModel):
            """Configuration for validation settings."""

            link_validation: FlextQualityModels.Quality.LinkValidationConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.LinkValidationConfig
                )
            )
            content_analysis: FlextQualityModels.Quality.ContentAnalysisConfig = (
                _InfraUtilities.Field(
                    default_factory=FlextQualityModelDefaults.ContentAnalysisConfig
                )
            )

        class OptimizerResults(_InfraModels.BaseModel):
            """Results of a documentation optimization run."""

            timestamp: str
            files_processed: int = 0
            changes_made: int = 0
            backups_created: MutableSequence[str] = _InfraUtilities.Field(
                default_factory=list
            )
            optimizations: MutableSequence[t.MutableStrMapping] = _InfraUtilities.Field(
                default_factory=list[t.MutableStrMapping]
            )

        class ExecutionRequest(_InfraModels.BaseModel):
            """Request payload for a deferred command execution."""

            script_path: Path
            runtime: str
            args: t.StrSequence = _InfraUtilities.Field(default_factory=list)
            timeout_ms: int

        class ExecutionResult(_InfraModels.BaseModel):
            """Structured result payload from a command execution."""

            success: bool
            exit_code: int
            stdout: str = ""
            stderr: str = ""

        class McpToolCall(_InfraModels.BaseModel):
            """MCP tool invocation request contract."""

            server: str
            tool: str
            params: t.JsonMapping = _InfraUtilities.Field(default_factory=dict)

        class McpToolResult(_InfraModels.BaseModel):
            """MCP tool invocation response contract."""

            success: bool
            data: t.StrMapping | None = None
            error: str | None = None


m = FlextQualityModels

__all__: list[str] = ["FlextQualityModels", "m"]
