"""Protocols for flext-quality."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol, runtime_checkable

from flext_infra import p as infra_p
from flext_web import p as web_p

if TYPE_CHECKING:
    from collections.abc import MutableMapping, MutableSequence
    from pathlib import Path

    from flext_quality import c, m, t


class FlextQualityProtocols(infra_p, web_p):
    """Namespace for flext-quality protocols."""

    @runtime_checkable
    class Quality(Protocol):
        """Quality-specific protocols namespace."""

        @runtime_checkable
        class ArgumentOptionSpec(Protocol):
            """Structural contract for quality argparse option specs."""

            flags: t.StrSequence
            help: str
            action: c.Quality.ArgumentAction | None
            default: t.JsonValue | None
            value_type: c.Quality.ArgumentValueType | None
            nargs: int | str | None
            choices: t.StrSequence | None
            dest: str | None

        @runtime_checkable
        class ArgumentParserSpec(Protocol):
            """Structural contract for quality argparse parser specs."""

            description: str
            options: t.SequenceOf[FlextQualityProtocols.Quality.ArgumentOptionSpec]

        @runtime_checkable
        class ValidatorBase(Protocol):
            """Abstract base protocol for rule validators."""

            @property
            def name(self) -> str:
                """The validator name."""
                ...

            def validate(
                self, content: str, file_path: t.Cli.TextPath | None = None
            ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
                """Validate content and return violations."""
                ...

        @runtime_checkable
        class HookImpl(Protocol):
            """Abstract base protocol for hook implementations."""

            event: ClassVar[type]
            matcher: ClassVar[t.StrSequence | None]

            def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.JsonMapping) -> bool:
                """Check if hook should run for this input."""
                ...

        @runtime_checkable
        class DocsConfig(Protocol):
            """Protocol for documentation configuration objects."""

            def get(
                self, key: str, *, default: str | float | bool | None = None
            ) -> t.Primitives | None:
                """Get a configuration value."""
                ...

            def __getitem__(self, key: str) -> None:
                """Get a configuration value with bracket notation."""
                ...

        @runtime_checkable
        class BaseHook(Protocol):
            """Protocol for hook implementations."""

            event: str
            matcher: t.StrSequence | None

            def execute(self, input_data: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute the hook logic."""
                ...

            def should_run(self, input_data: t.JsonMapping) -> bool:
                """Check if hook should run for this input."""
                ...

        @runtime_checkable
        class RuleValidator(Protocol):
            """Protocol for rule validators."""

            rule_type: str

            def validate(
                self, settings: t.JsonMapping, context: t.JsonMapping
            ) -> p.Result[t.Quality.RuleResult]:
                """Validate according to rule."""
                ...

        @runtime_checkable
        class IntegrationClient(Protocol):
            """Protocol for external integrations."""

            def connect(self) -> p.Result[bool]:
                """Connect to external service."""
                ...

            def disconnect(self) -> p.Result[bool]:
                """Disconnect from external service."""
                ...

            def health_check(self) -> p.Result[t.StrMapping]:
                """Check integration health."""
                ...

        @runtime_checkable
        class McpTool(Protocol):
            """Protocol for MCP tools."""

            name: str
            description: str

            def execute(self, params: t.JsonMapping) -> p.Result[t.JsonMapping]:
                """Execute MCP tool."""
                ...

        @runtime_checkable
        class RuleDefinition(infra_p.BaseModel, Protocol):
            """Structural contract for a documentation quality rule definition."""

            name: str
            type: c.Quality.RuleType
            description: str
            pattern: str | None
            action: str
            enabled: bool

        @runtime_checkable
        class NotifierResults(infra_p.BaseModel, Protocol):
            """Structural contract for documentation notifier results."""

            notifications_sent: int
            errors: MutableSequence[str]
            timestamp: str

        @runtime_checkable
        class MaintenanceConfig(infra_p.BaseModel, Protocol):
            """Structural contract for scheduled maintenance configuration."""

            enabled: bool
            reports_dir: str
            backup_dir: str
            schedules: MutableMapping[str, m.Quality.ScheduleEntry]
            tasks: MutableMapping[str, m.Quality.ScheduleTaskConfig]
            error_handling: m.Quality.ErrorHandlingConfig
            logging: m.Quality.LoggingConfig

        @runtime_checkable
        class ScheduleResults(infra_p.BaseModel, Protocol):
            """Structural contract for scheduled maintenance execution results."""

            start_time: str
            tasks_completed: int
            errors: MutableSequence[str]
            warnings: MutableSequence[str]
            end_time: str
            duration_seconds: int

        @runtime_checkable
        class ScheduleTaskConfig(infra_p.BaseModel, Protocol):
            """Structural contract for a scheduled maintenance task configuration."""

            description: str
            command: str
            timeout: t.PositiveInt

        @runtime_checkable
        class AuditRulesConfig(infra_p.BaseModel, Protocol):
            """Structural contract for audit rules and thresholds configuration."""

            quality_thresholds: m.Quality.QualityThresholdsConfig
            content_checks: m.Quality.ContentChecksConfig
            severity_levels: m.Quality.SeverityLevelsConfig

        @runtime_checkable
        class StyleGuideConfig(infra_p.BaseModel, Protocol):
            """Structural contract for style guide configuration."""

            markdown: m.Quality.MarkdownStyleConfig
            accessibility: m.Quality.AccessibilityConfig
            formatting: m.Quality.FormattingConfig

        @runtime_checkable
        class ValidationConfig(infra_p.BaseModel, Protocol):
            """Structural contract for validation settings configuration."""

            link_validation: m.Quality.LinkValidationConfig
            content_analysis: m.Quality.ContentAnalysisConfig

        @runtime_checkable
        class AuditMetrics(infra_p.BaseModel, Protocol):
            """Structural contract for documentation audit metrics."""

            total_issues: int
            severity_breakdown: t.MutableIntMapping
            quality_score: int
            files_analyzed: int
            issues_per_file: float

        @runtime_checkable
        class AuditRecommendation(infra_p.BaseModel, Protocol):
            """Structural contract for a documentation audit recommendation."""

            priority: str
            category: str
            recommendation: str
            actions: t.StrSequence

        @runtime_checkable
        class AuditorResults(infra_p.BaseModel, Protocol):
            """Structural contract for documentation audit execution results."""

            timestamp: str
            files_analyzed: int
            issues: MutableSequence[
                MutableMapping[
                    str,
                    t.Primitives | t.StrSequence | t.SequenceOf[t.StrMapping] | None,
                ]
            ]
            metrics: m.Quality.AuditMetrics
            recommendations: MutableSequence[m.Quality.AuditRecommendation]

        @runtime_checkable
        class LinkRecord(infra_p.BaseModel, Protocol):
            """Structural contract for a documentation link record."""

            text: str
            url: str
            type: str
            file: str
            line_number: int | None

        @runtime_checkable
        class LinkCheckResult(infra_p.BaseModel, Protocol):
            """Structural contract for a single link check result."""

            valid: bool | None
            url: str | None
            file: str | None
            line: int | None
            status_code: int | None
            error: str | None
            type: str | None
            target: str | None
            src: str | None
            text: str | None
            anchor: str | None
            warning: str | None

        @runtime_checkable
        class LinkValidatorResults(infra_p.BaseModel, Protocol):
            """Structural contract for documentation link validation results."""

            timestamp: str
            links_checked: int
            valid_links: int
            broken_links: int
            warnings: int
            errors: MutableSequence[m.Quality.LinkCheckResult]
            warnings_list: MutableSequence[m.Quality.LinkCheckResult]

        @runtime_checkable
        class ContentIssue(infra_p.BaseModel, Protocol):
            """Structural contract for a documentation content issue."""

            type: str
            file: str | None
            line: int | None
            content: str | None
            error: str | None
            word_count: int | None
            readability_score: float | None
            warning: str | None

        @runtime_checkable
        class ContentValidatorResults(infra_p.BaseModel, Protocol):
            """Structural contract for documentation content validation results."""

            timestamp: str
            files_checked: int
            content_issues: MutableSequence[m.Quality.ContentIssue]
            quality_metrics: t.MutableScalarMapping

        @runtime_checkable
        class ContentMetrics(infra_p.BaseModel, Protocol):
            """Structural contract for content quality metrics."""

            word_count: int
            sentence_count: int
            avg_words_per_sentence: float
            readability_score: float
            has_code_blocks: bool
            has_lists: bool
            has_headers: bool

        @runtime_checkable
        class McpToolCall(infra_p.BaseModel, Protocol):
            """Structural contract for an MCP tool invocation request."""

            server: str
            tool: str
            params: t.JsonMapping

        @runtime_checkable
        class McpToolResult(infra_p.BaseModel, Protocol):
            """Structural contract for an MCP tool invocation response."""

            success: bool
            data: t.StrMapping | None
            error: str | None

        @runtime_checkable
        class OptimizerResults(infra_p.BaseModel, Protocol):
            """Structural contract for documentation optimization results."""

            timestamp: str
            files_processed: int
            changes_made: int
            backups_created: MutableSequence[str]
            optimizations: MutableSequence[t.MutableStrMapping]

        @runtime_checkable
        class ExecutionRequest(infra_p.BaseModel, Protocol):
            """Structural contract for a deferred command execution request."""

            script_path: Path
            runtime: str
            args: t.StrSequence
            timeout_ms: int


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
