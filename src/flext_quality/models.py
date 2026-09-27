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

from flext_web import FlextWebModels as _WebModels

from flext_quality import FlextQualityConstants as c, FlextQualityTypes as t


class FlextQualityModels(_WebModels):
    """Namespace for flext-quality models."""

    class Quality:
        """Quality-specific models namespace."""

        class AuditMetrics(_WebModels.ManagedModel):
            """Typed metrics for documentation audit results."""

            total_issues: int = 0
            severity_breakdown: t.MutableIntMapping = _WebModels.Field(default_factory=dict)
            quality_score: int = 0
            files_analyzed: int = 0
            issues_per_file: float = 0.0

        class QualityThresholdsConfig(_WebModels.ManagedModel):
            """Configuration for quality threshold limits."""

            max_age_days: int
            min_word_count: int
            max_broken_links: int
            min_completeness_score: float
            max_file_size_mb: int

        class ContentChecksConfig(_WebModels.ManagedModel):
            """Configuration for content validation checks."""

            check_freshness: bool
            check_completeness: bool
            check_consistency: bool
            check_links: bool
            check_structure: bool
            check_accessibility: bool

        class SeverityLevelsConfig(_WebModels.ManagedModel):
            """Configuration for severity level categorization."""

            critical: t.StrSequence
            high: t.StrSequence
            medium: t.StrSequence
            low: t.StrSequence

        class MarkdownStyleConfig(_WebModels.ManagedModel):
            """Configuration for Markdown style preferences."""

            heading_style: str
            list_style: str
            emphasis_style: str
            code_block_style: str
            link_style: str

        class AccessibilityConfig(_WebModels.ManagedModel):
            """Configuration for accessibility requirements."""

            require_alt_text: bool
            descriptive_link_text: bool
            proper_heading_hierarchy: bool
            min_alt_text_length: int
            max_alt_text_length: int
            check_color_contrast: bool
            minimum_contrast_ratio: float

        class FormattingConfig(_WebModels.ManagedModel):
            """Configuration for formatting standards."""

            max_line_length: int
            soft_line_limit: int
            consistent_indentation: bool
            trailing_spaces: bool
            trailing_newlines: bool
            indentation_type: str
            indentation_size: int
            blank_lines_before_headings: bool
            blank_lines_after_headings: bool
            blank_lines_around_lists: bool
            blank_lines_around_code_blocks: bool

        class HeadingsConfig(_WebModels.ManagedModel):
            """Documentation heading hierarchy policy."""

            enforce_hierarchy: bool
            require_space_after_hash: bool
            first_heading_level: int

        class CodeStyleConfig(_WebModels.ManagedModel):
            """Documentation code block policy."""

            require_language_specifier: bool

        class StyleIssue(_WebModels.ManagedModel):
            """A documentation style violation."""

            type: str
            line: int
            content: str
            message: str
            severity: str

        class StyleFileResults(_WebModels.ManagedModel):
            """Style findings for one file."""

            file: str
            violations: MutableSequence[FlextQualityModels.Quality.StyleIssue]
            issues: MutableSequence[FlextQualityModels.Quality.StyleIssue]
            suggestions: MutableSequence[str]

        class StyleSummaryMetrics(_WebModels.ManagedModel):
            """Counts for a style validation run."""

            total_violations: int
            critical_issues: int
            warnings: int
            suggestions_count: int
            accessibility_issues: int

        class StyleValidationResults(_WebModels.ManagedModel):
            """Aggregated style findings."""

            files_checked: int
            style_violations: MutableSequence[FlextQualityModels.Quality.StyleIssue]
            accessibility_issues: MutableSequence[FlextQualityModels.Quality.StyleIssue]
            formatting_errors: MutableSequence[FlextQualityModels.Quality.StyleIssue]
            suggestions: MutableSequence[str]
            summary: FlextQualityModels.Quality.StyleSummaryMetrics

        class LinkValidationConfig(_WebModels.ManagedModel):
            """Configuration for link validation settings."""

            timeout: int
            user_agent: str
            check_external: bool
            check_internal: bool
            check_images: bool
            follow_redirects: bool
            max_redirects: int
            acceptable_status_codes: t.SequenceOf[int]
            validate_content_type: bool
            expected_content_types: t.StrSequence
            allowed_domains: t.StrSequence
            blocked_domains: t.StrSequence

        class ValidationRunConfig(_WebModels.ManagedModel):
            """Execution limits for validation operations."""

            max_concurrent_requests: t.PositiveInt

        class ContentAnalysisConfig(_WebModels.ManagedModel):
            """Configuration for content analysis parameters."""

            min_section_depth: int
            required_sections: t.StrSequence
            min_word_count: int
            check_readability: bool
            readability_target_score: int
            check_todos: bool
            check_fixmes: bool

        class RuleDefinition(_WebModels.ManagedModel):
            """A rule definition from YAML."""

            name: str
            type: c.Quality.RuleType
            description: str
            pattern: str | None = None
            action: str
            enabled: bool = True

        class Issue(_WebModels.ManagedModel):
            """Canonical issue model for documentation tooling."""

            type: Annotated[
                str,
                _WebModels.Field(
                    description="FlextQualityModels.Quality.Issue type identifier"
                ),
            ]
            severity: Annotated[
                str, _WebModels.Field(description="Severity level identifier")
            ]
            file: Annotated[
                str,
                _WebModels.Field(description="File path where issue was found"),
            ]
            line: Annotated[
                int | None,
                _WebModels.Field(
                    description="FlextQualityModels.Quality.Issue line number"
                ),
            ] = None
            description: Annotated[
                str,
                _WebModels.Field(
                    description="FlextQualityModels.Quality.Issue description"
                ),
            ] = ""
            recommendation: Annotated[
                str, _WebModels.Field(description="Recommended fix")
            ] = ""
            context: Annotated[
                t.MappingKV[str, t.Primitives | None] | None,
                _WebModels.Field(default=None),
            ]

        class ValidationResult(_WebModels.ManagedModel):
            """Canonical validation result for documentation tooling."""

            total_items: int = 0
            valid_items: int = 0
            invalid_items: int = 0
            issues: MutableSequence[FlextQualityModels.Quality.Issue] = (
                _WebModels.Field(default_factory=list)
            )
            warnings: MutableSequence[str] = _WebModels.Field(default_factory=list)
            errors: MutableSequence[str] = _WebModels.Field(default_factory=list)
            metadata: MutableMapping[str, t.Primitives] = _WebModels.Field(
                default_factory=dict
            )

        class FileMetadata(_WebModels.ManagedModel):
            """Metadata about a documentation file."""

            path: str
            size: int = 0
            modified_time: float = 0.0
            extension: str = ""
            is_markdown: bool = False
            lines: int = 0
            words: int = 0

        class ScheduleTaskConfig(_WebModels.ManagedModel):
            """Task configuration for scheduled documentation maintenance."""

            description: str
            command: str
            timeout: Annotated[t.PositiveInt, _WebModels.Field(default=300)]

        class ScheduleEntry(_WebModels.ManagedModel):
            """Single schedule entry definition."""

            enabled: bool = True
            time: str
            tasks: t.StrSequence = _WebModels.Field(default_factory=list)
            day: str | None = None

        class ErrorHandlingConfig(_WebModels.ManagedModel):
            """Error handling settings for scheduled maintenance."""

            max_retries: Annotated[t.NonNegativeInt, _WebModels.Field(default=3)]
            retry_delay: Annotated[t.NonNegativeInt, _WebModels.Field(default=60)]
            fail_fast: bool = False
            notify_on_failure: bool = True

        class LoggingConfig(_WebModels.ManagedModel):
            """Logging configuration for scheduled maintenance."""

            enabled: bool = True
            log_file: str
            max_log_size: str = "10MB"
            retention_days: Annotated[t.PositiveInt, _WebModels.Field(default=30)]

        class MaintenanceConfig(_WebModels.ManagedModel):
            """Root configuration for scheduled documentation maintenance."""

            enabled: bool = True
            reports_dir: str
            backup_dir: str
            schedules: MutableMapping[str, FlextQualityModels.Quality.ScheduleEntry] = (
                _WebModels.Field(default_factory=dict)
            )
            tasks: MutableMapping[
                str, FlextQualityModels.Quality.ScheduleTaskConfig
            ] = _WebModels.Field(default_factory=dict)
            error_handling: FlextQualityModels.Quality.ErrorHandlingConfig
            logging: FlextQualityModels.Quality.LoggingConfig

        class ScheduleResults(_WebModels.ManagedModel):
            """Execution summary for scheduled maintenance runs."""

            start_time: str
            tasks_completed: int = 0
            errors: MutableSequence[str] = _WebModels.Field(default_factory=list)
            warnings: MutableSequence[str] = _WebModels.Field(default_factory=list)
            end_time: str = ""
            duration_seconds: int = 0

        class ArgumentOptionSpec(_WebModels.ManagedModel):
            """Typed argparse option spec for quality tooling."""

            flags: t.StrSequence
            help: str
            action: c.Quality.ArgumentAction | None = None
            default: t.JsonValue | None = None
            value_type: c.Quality.ArgumentValueType | None = None
            nargs: int | str | None = None
            choices: t.StrSequence | None = None
            dest: str | None = None

        class ArgumentParserSpec(_WebModels.ManagedModel):
            """Typed parser spec consumed by canonical quality utilities."""

            description: str
            options: t.SequenceOf[FlextQualityModels.Quality.ArgumentOptionSpec]

        class AuditRecommendation(_WebModels.ManagedModel):
            """Typed recommendation from documentation audit."""

            priority: str
            category: str
            recommendation: str
            actions: t.StrSequence = _WebModels.Field(default_factory=list)

        class AuditorResults(_WebModels.ManagedModel):
            """Results for documentation audit execution."""

            timestamp: str
            files_analyzed: int = 0
            issues: MutableSequence[
                MutableMapping[
                    str,
                    t.Primitives | t.StrSequence | t.SequenceOf[t.StrMapping] | None,
                ]
            ] = _WebModels.Field(
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
            metrics: FlextQualityModels.Quality.AuditMetrics = _WebModels.Field(
                default_factory=AuditMetrics
            )
            recommendations: MutableSequence[
                FlextQualityModels.Quality.AuditRecommendation
            ] = _WebModels.Field(default_factory=list)

        class LinkRecord(_WebModels.ManagedModel):
            """Record of a link found in documentation."""

            text: str
            url: str
            type: str
            file: str
            line_number: int | None = None
            reference: str | None = None
            context: t.JsonMapping | None = None

        class LinkCheckResult(_WebModels.ManagedModel):
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
            context: t.JsonMapping = _WebModels.Field(default_factory=dict)
            response_time: float | None = None
            redirected: bool | None = None
            final_url: str | None = None
            content_type: str | None = None

        class LinkPerformanceMetrics(_WebModels.ManagedModel):
            """Measured link validation duration."""

            total_time: float = 0.0
            average_response_time: float = 0.0
            slowest_response: float = 0.0

        class ContentIssue(_WebModels.ManagedModel):
            """FlextQualityModels.Quality.Issue found in documentation content."""

            type: str
            file: str | None = None
            line: int | None = None
            content: str | None = None
            error: str | None = None
            word_count: int | None = None
            readability_score: float | None = None
            warning: str | None = None

        class LinkValidatorResults(_WebModels.ManagedModel):
            """Results for documentation link validation."""

            timestamp: str
            links_checked: int = 0
            valid_links: int = 0
            broken_links: int = 0
            warnings: int = 0
            errors: MutableSequence[FlextQualityModels.Quality.LinkCheckResult] = (
                _WebModels.Field(default_factory=list)
            )
            warnings_list: MutableSequence[
                FlextQualityModels.Quality.LinkCheckResult
            ] = _WebModels.Field(default_factory=list)
            performance: FlextQualityModels.Quality.LinkPerformanceMetrics = (
                _WebModels.Field(default_factory=LinkPerformanceMetrics)
            )

        class ContentValidatorResults(_WebModels.ManagedModel):
            """Results for documentation content validation."""

            timestamp: str
            files_checked: int = 0
            content_issues: MutableSequence[FlextQualityModels.Quality.ContentIssue] = (
                _WebModels.Field(default_factory=list)
            )
            quality_metrics: t.MutableScalarMapping = _WebModels.Field(
                default_factory=dict
            )

        class ContentMetrics(_WebModels.ManagedModel):
            """Content quality metrics for a documentation file."""

            word_count: int = 0
            sentence_count: int = 0
            avg_words_per_sentence: float = 0.0
            readability_score: float = 0.0
            has_code_blocks: bool = False
            has_lists: bool = False
            has_headers: bool = False

        class ChannelConfig(_WebModels.ManagedModel):
            """Notification channel toggle configuration."""

            enabled: bool = True

        class NotifierResults(_WebModels.ManagedModel):
            """Results for documentation notification runs."""

            notifications_sent: int = 0
            errors: MutableSequence[str] = _WebModels.Field(default_factory=list)
            timestamp: str

        class AuditRulesConfig(_WebModels.FlexibleInternalModel):
            """Configuration for audit rules and thresholds."""

            quality_thresholds: FlextQualityModels.Quality.QualityThresholdsConfig
            content_checks: FlextQualityModels.Quality.ContentChecksConfig
            severity_levels: FlextQualityModels.Quality.SeverityLevelsConfig

        class StyleGuideConfig(_WebModels.FlexibleInternalModel):
            """Configuration for style guide rules."""

            markdown: FlextQualityModels.Quality.MarkdownStyleConfig
            accessibility: FlextQualityModels.Quality.AccessibilityConfig
            formatting: FlextQualityModels.Quality.FormattingConfig
            headings: FlextQualityModels.Quality.HeadingsConfig
            code: FlextQualityModels.Quality.CodeStyleConfig

        class ValidationConfig(_WebModels.FlexibleInternalModel):
            """Configuration for validation settings."""

            validation: FlextQualityModels.Quality.ValidationRunConfig
            link_validation: FlextQualityModels.Quality.LinkValidationConfig
            content_analysis: FlextQualityModels.Quality.ContentAnalysisConfig

        class OptimizerResults(_WebModels.ManagedModel):
            """Results of a documentation optimization run."""

            timestamp: str
            files_processed: int = 0
            changes_made: int = 0
            backups_created: MutableSequence[str] = _WebModels.Field(
                default_factory=list
            )
            optimizations: MutableSequence[t.MutableStrMapping] = _WebModels.Field(
                default_factory=list[t.MutableStrMapping]
            )

        class ExecutionRequest(_WebModels.ManagedModel):
            """Request payload for a deferred command execution."""

            script_path: Path
            runtime: str
            args: t.StrSequence = _WebModels.Field(default_factory=list)
            timeout_ms: int

        class ExecutionResult(_WebModels.ManagedModel):
            """Structured result payload from a command execution."""

            success: bool
            exit_code: int
            stdout: str = ""
            stderr: str = ""

        class McpToolCall(_WebModels.ManagedModel):
            """MCP tool invocation request contract."""

            server: str
            tool: str
            params: t.JsonMapping = _WebModels.Field(default_factory=dict)

        class McpToolResult(_WebModels.ManagedModel):
            """MCP tool invocation response contract."""

            success: bool
            data: t.StrMapping | None = None
            error: str | None = None


m = FlextQualityModels

__all__: list[str] = ["FlextQualityModels", "m"]
