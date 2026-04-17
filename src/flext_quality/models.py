"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import Annotated, ClassVar

from flext_cli import m, u
from flext_web import FlextWebModels

from flext_quality import c, t


class FlextQualityModels(m, FlextWebModels):
    """Namespace for flext-quality models."""

    class Quality:
        """Quality-specific models namespace."""

        @staticmethod
        def _empty_list_str() -> MutableSequence[str]:
            return []

        @staticmethod
        def _empty_dict_str_str() -> t.StrMapping:
            return {}

        @staticmethod
        def _empty_list_dict_str_str() -> MutableSequence[t.MutableStrMapping]:
            return []

        class HookConfig(m.BaseModel):
            """Configuration for a hook."""

            event: c.Quality.HookEvent
            matcher: t.StrSequence | None = None
            command: str
            timeout_ms: Annotated[
                int,
                u.Field(default=c.Quality.Defaults.HOOK_TIMEOUT_MS),
            ]
            enabled: bool = True

        class HookResult(m.BaseModel):
            """Result from hook execution."""

            continue_execution: Annotated[bool, u.Field(alias="continue")]
            system_message: Annotated[str | None, u.Field(alias="systemMessage")] = None
            blocked_reason: str | None = None

            model_config: ClassVar[dict[str, bool]] = {"populate_by_name": True}

        class RuleDefinition(m.BaseModel):
            """A rule definition from YAML."""

            name: str
            type: c.Quality.RuleType
            description: str
            pattern: str | None = None
            action: str
            enabled: bool = True

        class IntegrationConfig(m.BaseModel):
            """Configuration for an integration."""

            name: str
            enabled: bool = True
            host: str = "localhost"
            port: int
            timeout_ms: Annotated[
                int,
                u.Field(default=c.Quality.Defaults.INTEGRATION_TIMEOUT_MS),
            ]

        class MemoryObservation(m.BaseModel):
            """An observation from claude-mem."""

            id: str
            type: str
            title: str
            content: str
            concepts: t.StrSequence = u.Field(default_factory=list)
            files: t.StrSequence = u.Field(default_factory=list)
            timestamp: str

        class ContextSearchResult(m.BaseModel):
            """A search result from claude-context."""

            file_path: str
            snippet: str
            score: float
            line_number: int | None = None

        class Issue(m.BaseModel):
            """Canonical issue model for documentation tooling."""

            type: Annotated[str, u.Field(description="Issue type identifier")]
            severity: Annotated[str, u.Field(description="Severity level identifier")]
            file: Annotated[str, u.Field(description="File path where issue was found")]
            line: Annotated[int | None, u.Field(description="Issue line number")] = None
            description: Annotated[str, u.Field(description="Issue description")] = ""
            recommendation: Annotated[str, u.Field(description="Recommended fix")] = ""
            context: Annotated[
                Mapping[str, t.Primitives | None] | None,
                u.Field(default=None),
            ]

            def to_dict(
                self,
            ) -> Mapping[str, str | int | Mapping[str, t.Primitives | None] | None]:
                """Convert issue to dictionary representation."""
                return {
                    "type": self.type,
                    "severity": self.severity,
                    "file": self.file,
                    "line": self.line,
                    "description": self.description,
                    "recommendation": self.recommendation,
                    "context": self.context if self.context is not None else {},
                }

        class ValidationResult(m.BaseModel):
            """Canonical validation result for documentation tooling."""

            total_items: int = 0
            valid_items: int = 0
            invalid_items: int = 0
            issues: MutableSequence[FlextQualityModels.Quality.Issue] = u.Field(
                default_factory=lambda: list[FlextQualityModels.Quality.Issue]()
            )
            warnings: MutableSequence[str] = u.Field(default_factory=list)
            errors: MutableSequence[str] = u.Field(default_factory=list)
            metadata: MutableMapping[str, t.Primitives] = u.Field(default_factory=dict)

            @property
            def success_rate(self) -> float:
                """Calculate success rate as a percentage."""
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

        class FileMetadata(m.BaseModel):
            """Metadata about a documentation file."""

            path: str
            size: int = 0
            modified_time: float = 0.0
            extension: str = ""
            is_markdown: bool = False
            lines: int = 0
            words: int = 0

            @classmethod
            def from_path(cls, path: Path) -> FlextQualityModels.Quality.FileMetadata:
                """Build metadata from a filesystem path."""
                size = path.stat().st_size if path.exists() else 0
                modified_time = path.stat().st_mtime if path.exists() else 0.0
                extension = path.suffix.lower()
                is_markdown = extension in {".md", ".mdx"}
                lines = 0
                words = 0
                if path.exists():
                    try:
                        content = path.read_text(encoding="utf-8")
                        lines = content.count("\n") + 1
                        words = len(content.split())
                    except (OSError, UnicodeDecodeError):
                        pass
                return cls(
                    path=str(path),
                    size=size,
                    modified_time=modified_time,
                    extension=extension,
                    is_markdown=is_markdown,
                    lines=lines,
                    words=words,
                )

        class ScheduleTaskConfig(m.BaseModel):
            """Task configuration for scheduled documentation maintenance."""

            description: str
            command: str
            timeout: Annotated[t.PositiveInt, u.Field(default=300)]

        class ScheduleEntry(m.BaseModel):
            """Single schedule entry definition."""

            enabled: bool = True
            time: str
            tasks: t.StrSequence = u.Field(default_factory=list)
            day: str | None = None

        class ErrorHandlingConfig(m.BaseModel):
            """Error handling settings for scheduled maintenance."""

            max_retries: Annotated[t.NonNegativeInt, u.Field(default=3)]
            retry_delay: Annotated[t.NonNegativeInt, u.Field(default=60)]
            fail_fast: bool = False
            notify_on_failure: bool = True

        class LoggingConfig(m.BaseModel):
            """Logging configuration for scheduled maintenance."""

            enabled: bool = True
            log_file: str
            max_log_size: str = "10MB"
            retention_days: Annotated[t.PositiveInt, u.Field(default=30)]

        class MaintenanceConfig(m.BaseModel):
            """Root configuration for scheduled documentation maintenance."""

            enabled: bool = True
            reports_dir: str
            backup_dir: str
            schedules: MutableMapping[str, FlextQualityModels.Quality.ScheduleEntry] = (
                u.Field(default_factory=dict)
            )
            tasks: MutableMapping[
                str,
                FlextQualityModels.Quality.ScheduleTaskConfig,
            ] = u.Field(default_factory=dict)
            error_handling: FlextQualityModels.Quality.ErrorHandlingConfig
            logging: FlextQualityModels.Quality.LoggingConfig

        class ScheduleResults(m.BaseModel):
            """Execution summary for scheduled maintenance runs."""

            start_time: str
            tasks_completed: int = 0
            errors: MutableSequence[str] = u.Field(default_factory=list)
            warnings: MutableSequence[str] = u.Field(default_factory=list)
            end_time: str = ""
            duration_seconds: int = 0

        class AuditMetrics(m.BaseModel):
            """Typed metrics for documentation audit results."""

            total_issues: int = 0
            severity_breakdown: t.MutableIntMapping = u.Field(default_factory=dict)
            quality_score: int = 0
            files_analyzed: int = 0
            issues_per_file: float = 0.0

        class AuditRecommendation(m.BaseModel):
            """Typed recommendation from documentation audit."""

            priority: str
            category: str
            recommendation: str
            actions: t.StrSequence = u.Field(default_factory=list)

        class AuditorResults(m.BaseModel):
            """Results for documentation audit execution."""

            timestamp: str
            files_analyzed: int = 0
            issues: MutableSequence[
                MutableMapping[
                    str,
                    t.Primitives | t.StrSequence | Sequence[t.StrMapping] | None,
                ]
            ] = u.Field(
                default_factory=lambda: list[
                    MutableMapping[
                        str,
                        t.Primitives | t.StrSequence | Sequence[t.StrMapping] | None,
                    ]
                ]()
            )
            metrics: FlextQualityModels.Quality.AuditMetrics = u.Field(
                default_factory=lambda: FlextQualityModels.Quality.AuditMetrics()
            )
            recommendations: MutableSequence[
                FlextQualityModels.Quality.AuditRecommendation
            ] = u.Field(
                default_factory=lambda: list[
                    FlextQualityModels.Quality.AuditRecommendation
                ]()
            )

        class LinkRecord(m.BaseModel):
            """Record of a link found in documentation."""

            text: str
            url: str
            type: str
            file: str
            line_number: int | None = None

        class LinkCheckResult(m.BaseModel):
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

        class ContentIssue(m.BaseModel):
            """Issue found in documentation content."""

            type: str
            file: str | None = None
            line: int | None = None
            content: str | None = None
            error: str | None = None
            word_count: int | None = None
            readability_score: float | None = None
            warning: str | None = None

        class LinkValidatorResults(m.BaseModel):
            """Results for documentation link validation."""

            timestamp: str
            links_checked: int = 0
            valid_links: int = 0
            broken_links: int = 0
            warnings: int = 0
            errors: MutableSequence[FlextQualityModels.Quality.LinkCheckResult] = (
                u.Field(
                    default_factory=lambda: list[
                        FlextQualityModels.Quality.LinkCheckResult
                    ]()
                )
            )
            warnings_list: MutableSequence[
                FlextQualityModels.Quality.LinkCheckResult
            ] = u.Field(
                default_factory=lambda: list[
                    FlextQualityModels.Quality.LinkCheckResult
                ]()
            )

        class ContentValidatorResults(m.BaseModel):
            """Results for documentation content validation."""

            timestamp: str
            files_checked: int = 0
            content_issues: MutableSequence[FlextQualityModels.Quality.ContentIssue] = (
                u.Field(
                    default_factory=lambda: list[
                        FlextQualityModels.Quality.ContentIssue
                    ]()
                )
            )
            quality_metrics: t.MutableScalarMapping = u.Field(default_factory=dict)

        class ContentMetrics(m.BaseModel):
            """Content quality metrics for a documentation file."""

            word_count: int = 0
            sentence_count: int = 0
            avg_words_per_sentence: float = 0.0
            readability_score: float = 0.0
            has_code_blocks: bool = False
            has_lists: bool = False
            has_headers: bool = False

        class FileStatistics(m.BaseModel):
            """Statistics payload for discovered documentation files."""

            total_files: int
            total_size: int | None = None
            total_lines: int | None = None
            total_words: int | None = None
            markdown_files: int | None = None
            other_files: int | None = None
            size_distribution: t.IntMapping | None = None
            categories: t.IntMapping | None = None
            avg_file_size: float | None = None
            avg_lines_per_file: float | None = None
            avg_words_per_file: float | None = None

        class ChannelConfig(m.BaseModel):
            """Notification channel toggle configuration."""

            enabled: bool = True

        class AlertThresholdConfig(m.BaseModel):
            """Threshold-based alert configuration."""

            enabled: bool = True
            threshold: Annotated[t.NonNegativeInt, u.Field(default=0)]

        class AlertToggleConfig(m.BaseModel):
            """Simple on/off alert configuration."""

            enabled: bool = True

        class AlertsConfig(m.BaseModel):
            """All alert toggles for documentation notifications."""

            critical_issues: FlextQualityModels.Quality.AlertThresholdConfig
            quality_drop: FlextQualityModels.Quality.AlertThresholdConfig
            broken_links: FlextQualityModels.Quality.AlertThresholdConfig
            weekly_report: FlextQualityModels.Quality.AlertToggleConfig
            monthly_report: FlextQualityModels.Quality.AlertToggleConfig

        class EmailConfig(m.BaseModel):
            """SMTP notification configuration."""

            smtp_server: str
            smtp_port: int
            username: str
            password: str
            from_address: str
            to_addresses: t.StrSequence = u.Field(default_factory=list)

        class SlackConfig(m.BaseModel):
            """Slack notification configuration."""

            webhook_url: str
            channel: str
            username: str

        class WebhookConfig(m.BaseModel):
            """Generic webhook configuration."""

            url: str
            headers: t.StrMapping = u.Field(default_factory=dict)
            timeout: Annotated[t.PositiveInt, u.Field(default=30)]

        class ChannelsConfig(m.BaseModel):
            """Enabled channels for documentation notifications."""

            console: FlextQualityModels.Quality.ChannelConfig
            email: FlextQualityModels.Quality.ChannelConfig
            slack: FlextQualityModels.Quality.ChannelConfig
            webhook: FlextQualityModels.Quality.ChannelConfig

        class NotifierConfig(m.BaseModel):
            """Root notification configuration."""

            enabled: bool = True
            channels: FlextQualityModels.Quality.ChannelsConfig
            alerts: FlextQualityModels.Quality.AlertsConfig
            email: FlextQualityModels.Quality.EmailConfig
            slack: FlextQualityModels.Quality.SlackConfig
            webhook: FlextQualityModels.Quality.WebhookConfig

        class NotifierResults(m.BaseModel):
            """Results for documentation notification runs."""

            notifications_sent: int = 0
            errors: MutableSequence[str] = u.Field(default_factory=list)
            timestamp: str

        class QualityThresholdsConfig(m.BaseModel):
            """Configuration for quality threshold limits."""

            max_age_days: int = 90
            min_word_count: int = 100
            max_broken_links: int = 0
            min_completeness_score: float = 0.8

        class ContentChecksConfig(m.BaseModel):
            """Configuration for content validation checks."""

            check_freshness: bool = True
            check_completeness: bool = True
            check_consistency: bool = True
            check_links: bool = True

        class SeverityLevelsConfig(m.BaseModel):
            """Configuration for severity level categorization."""

            critical: t.StrSequence = u.Field(default_factory=list)
            high: t.StrSequence = u.Field(default_factory=list)
            medium: t.StrSequence = u.Field(default_factory=list)
            low: t.StrSequence = u.Field(default_factory=list)

        class AuditRulesConfig(m.BaseModel):
            """Configuration for audit rules and thresholds."""

            quality_thresholds: FlextQualityModels.Quality.QualityThresholdsConfig = (
                u.Field(
                    default_factory=lambda: (
                        FlextQualityModels.Quality.QualityThresholdsConfig()
                    ),
                )
            )
            content_checks: FlextQualityModels.Quality.ContentChecksConfig = u.Field(
                default_factory=lambda: FlextQualityModels.Quality.ContentChecksConfig()
            )
            severity_levels: FlextQualityModels.Quality.SeverityLevelsConfig = u.Field(
                default_factory=lambda: (
                    FlextQualityModels.Quality.SeverityLevelsConfig()
                )
            )

        class MarkdownStyleConfig(m.BaseModel):
            """Configuration for Markdown style preferences."""

            heading_style: str = "atx"
            list_style: str = "dash"
            emphasis_style: str = "*"
            code_block_style: str = "fenced"

        class AccessibilityConfig(m.BaseModel):
            """Configuration for accessibility requirements."""

            require_alt_text: bool = True
            descriptive_links: bool = True
            heading_structure: bool = True

        class FormattingConfig(m.BaseModel):
            """Configuration for formatting standards."""

            max_line_length: int = 88
            consistent_indentation: bool = True
            trailing_spaces: bool = False

        class StyleGuideConfig(m.BaseModel):
            """Configuration for style guide rules."""

            markdown: FlextQualityModels.Quality.MarkdownStyleConfig = u.Field(
                default_factory=lambda: FlextQualityModels.Quality.MarkdownStyleConfig()
            )
            accessibility: FlextQualityModels.Quality.AccessibilityConfig = u.Field(
                default_factory=lambda: FlextQualityModels.Quality.AccessibilityConfig()
            )
            formatting: FlextQualityModels.Quality.FormattingConfig = u.Field(
                default_factory=lambda: FlextQualityModels.Quality.FormattingConfig()
            )

        class LinkValidationConfig(m.BaseModel):
            """Configuration for link validation settings."""

            timeout: int = 10
            retry_attempts: int = 3
            user_agent: str = "FLEXT-Quality-Doc-Auditor/1.0"
            check_external: bool = True
            check_internal: bool = True
            check_images: bool = True

        class ContentAnalysisConfig(m.BaseModel):
            """Configuration for content analysis parameters."""

            min_section_depth: int = 2
            required_sections: t.StrSequence = u.Field(
                default_factory=lambda: ["Overview", "Installation", "Usage"]
            )
            check_todos: bool = True
            check_fixmes: bool = True

        class ValidationConfig(m.BaseModel):
            """Configuration for validation settings."""

            link_validation: FlextQualityModels.Quality.LinkValidationConfig = u.Field(
                default_factory=lambda: (
                    FlextQualityModels.Quality.LinkValidationConfig()
                )
            )
            content_analysis: FlextQualityModels.Quality.ContentAnalysisConfig = (
                u.Field(
                    default_factory=lambda: (
                        FlextQualityModels.Quality.ContentAnalysisConfig()
                    )
                )
            )

        class OptimizerResults(m.BaseModel):
            """Results of a documentation optimization run."""

            timestamp: str
            files_processed: int = 0
            changes_made: int = 0
            backups_created: MutableSequence[str] = u.Field(default_factory=list)
            optimizations: MutableSequence[t.MutableStrMapping] = u.Field(
                default_factory=lambda: list[t.MutableStrMapping]()
            )

        class ExecutionRequest(m.BaseModel):
            """Request payload for a deferred command execution."""

            script_path: Path
            runtime: str
            args: t.StrSequence = u.Field(default_factory=list)
            timeout_ms: int

        class ExecutionResult(m.BaseModel):
            """Structured result payload from a command execution."""

            success: bool
            exit_code: int
            stdout: str = ""
            stderr: str = ""

        class McpToolCall(m.BaseModel):
            """MCP tool invocation request contract."""

            server: str
            tool: str
            params: t.RecursiveContainerMapping = u.Field(default_factory=dict)

        class McpToolResult(m.BaseModel):
            """MCP tool invocation response contract."""

            success: bool
            data: t.StrMapping | None = None
            error: str | None = None


m = FlextQualityModels

__all__: list[str] = ["FlextQualityModels", "m"]
