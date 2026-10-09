"""Quality domain models for flext-quality (part 2 of 2).

Pydantic-2 models for the documentation quality domain, split across
package parts to honor the fleet per-module LOC ceiling; the public
``flext_quality.models`` facade composes both parts through MRO.

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
from types import MappingProxyType
from typing import Annotated

from flext_web import FlextWebModels as _WebModels

from flext_quality import FlextQualityConstants as c, FlextQualityTypes as t
from flext_quality._models.flextqualitymodels_part_01 import FlextQualityModelsPart01


class FlextQualityModelsPart02(FlextQualityModelsPart01):
    """Namespace for flext-quality models (part 2)."""

    class Quality(FlextQualityModelsPart01.Quality):
        """Quality-specific models namespace (part 2)."""

        class ScheduleTaskConfig(_WebModels.ManagedModel):
            """Task configuration for scheduled documentation maintenance."""

            description: str = _WebModels.Field(
                description=(
                    "Human-readable description of what the scheduled task does."
                ),
            )
            command: str = _WebModels.Field(
                description="Shell command executed when the scheduled task runs.",
            )
            timeout: Annotated[
                t.PositiveInt,
                _WebModels.Field(
                    default=300,
                    description=(
                        "Maximum time, in seconds, the task command may run before "
                        "being terminated."
                    ),
                ),
            ]

        class ScheduleEntry(_WebModels.ManagedModel):
            """Single schedule entry definition."""

            enabled: bool = _WebModels.Field(
                default=True,
                description="Whether this schedule entry is active.",
            )
            time: str = _WebModels.Field(
                description="Time of day at which the scheduled tasks should run.",
            )
            tasks: t.StrSequence = _WebModels.Field(
                default_factory=tuple,
                description="Names of the tasks executed by this schedule entry.",
            )
            day: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Optional day of the week this schedule entry applies to; None "
                    "means every day."
                ),
            )

        class ErrorHandlingConfig(_WebModels.ManagedModel):
            """Error handling settings for scheduled maintenance."""

            max_retries: Annotated[
                t.NonNegativeInt,
                _WebModels.Field(
                    default=3,
                    description=(
                        "Maximum number of times a failed scheduled task is retried."
                    ),
                ),
            ]
            retry_delay: Annotated[
                t.NonNegativeInt,
                _WebModels.Field(
                    default=60,
                    description=(
                        "Delay, in seconds, between retry attempts for a failed "
                        "scheduled task."
                    ),
                ),
            ]
            fail_fast: bool = _WebModels.Field(
                default=False,
                description=(
                    "Whether to stop scheduled maintenance immediately on the first "
                    "task failure."
                ),
            )
            notify_on_failure: bool = _WebModels.Field(
                default=True,
                description=(
                    "Whether to send a notification when a scheduled task fails."
                ),
            )

        class LoggingConfig(_WebModels.ManagedModel):
            """Logging configuration for scheduled maintenance."""

            enabled: bool = _WebModels.Field(
                default=True,
                description=(
                    "Whether logging is enabled for scheduled maintenance runs."
                ),
            )
            log_file: str = _WebModels.Field(
                description=(
                    "Filesystem path of the log file written by scheduled maintenance."
                ),
            )
            max_log_size: str = _WebModels.Field(
                default="10MB",
                description=(
                    "Maximum size the log file may reach before rotation (e.g. '10MB')."
                ),
            )
            retention_days: Annotated[
                t.PositiveInt,
                _WebModels.Field(
                    default=30,
                    description=(
                        "Number of days rotated log files are retained before deletion."
                    ),
                ),
            ]

        class MaintenanceConfig(_WebModels.ManagedModel):
            """Root configuration for scheduled documentation maintenance."""

            enabled: bool = _WebModels.Field(
                default=True,
                description="Whether scheduled documentation maintenance is enabled.",
            )
            reports_dir: str = _WebModels.Field(
                description="Directory where maintenance reports are written.",
            )
            backup_dir: str = _WebModels.Field(
                description=(
                    "Directory where backups created during maintenance are stored."
                ),
            )
            schedules: MutableMapping[
                str,
                FlextQualityModelsPart02.Quality.ScheduleEntry,
            ] = _WebModels.Field(
                default_factory=dict[
                    str, "FlextQualityModelsPart02.Quality.ScheduleEntry"
                ],
                description=(
                    "Named schedule entries controlling when maintenance tasks run."
                ),
            )
            tasks: MutableMapping[
                str,
                FlextQualityModelsPart02.Quality.ScheduleTaskConfig,
            ] = _WebModels.Field(
                default_factory=dict[
                    str, "FlextQualityModelsPart02.Quality.ScheduleTaskConfig"
                ],
                description=(
                    "Named task definitions available to be run by schedule entries."
                ),
            )
            error_handling: FlextQualityModelsPart02.Quality.ErrorHandlingConfig = (
                _WebModels.Field(
                    description=(
                        "Error handling policy applied to scheduled maintenance task "
                        "failures."
                    ),
                )
            )
            logging: FlextQualityModelsPart02.Quality.LoggingConfig = _WebModels.Field(
                description=(
                    "Logging configuration applied to scheduled maintenance runs."
                ),
            )

        class ScheduleResults(_WebModels.ManagedModel):
            """Execution summary for scheduled maintenance runs."""

            start_time: str = _WebModels.Field(
                description="Timestamp at which the scheduled maintenance run started.",
            )
            tasks_completed: int = _WebModels.Field(
                default=0,
                description="Number of scheduled tasks that completed successfully.",
            )
            errors: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description="Error messages produced by failed scheduled tasks.",
            )
            warnings: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description=(
                    "Warning messages produced during the scheduled maintenance run."
                ),
            )
            end_time: str = _WebModels.Field(
                default="",
                description="Timestamp at which the scheduled maintenance run ended.",
            )
            duration_seconds: int = _WebModels.Field(
                default=0,
                description=(
                    "Total duration of the scheduled maintenance run, in seconds."
                ),
            )

        class ArgumentOptionSpec(_WebModels.ManagedModel):
            """Typed argparse option spec for quality tooling."""

            flags: t.StrSequence = _WebModels.Field(
                description=(
                    "Command-line flag strings for this option (e.g. '-v', "
                    "'--verbose')."
                ),
            )
            help: str = _WebModels.Field(
                description=(
                    "Help text describing the option, shown in command-line usage "
                    "output."
                ),
            )
            action: c.Quality.ArgumentAction | None = _WebModels.Field(
                default=None,
                description=(
                    "Argparse action to perform when the option is provided (e.g. "
                    "store_true)."
                ),
            )
            default: t.JsonValue | None = _WebModels.Field(
                default=None,
                description=(
                    "Default value used for the option when it is not provided."
                ),
            )
            value_type: c.Quality.ArgumentValueType | None = _WebModels.Field(
                default=None,
                description=(
                    "Type the option's value is converted to (e.g. string, integer, "
                    "boolean)."
                ),
            )
            nargs: int | str | None = _WebModels.Field(
                default=None,
                description=(
                    "Number of command-line arguments this option consumes, per "
                    "argparse nargs semantics."
                ),
            )
            choices: t.StrSequence | None = _WebModels.Field(
                default=None,
                description=(
                    "Restricted set of values the option accepts; None means any "
                    "value is accepted."
                ),
            )
            dest: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Name of the attribute the parsed option value is stored under; "
                    "None derives it from the flags."
                ),
            )

        class ArgumentParserSpec(_WebModels.ManagedModel):
            """Typed parser spec consumed by canonical quality utilities."""

            description: str = _WebModels.Field(
                description=(
                    "Human-readable description of the command-line parser's purpose."
                ),
            )
            options: t.SequenceOf[
                FlextQualityModelsPart02.Quality.ArgumentOptionSpec
            ] = _WebModels.Field(
                description=(
                    "Option specifications registered on the command-line parser."
                ),
            )

        class AuditRecommendation(_WebModels.ManagedModel):
            """Typed recommendation from documentation audit."""

            priority: str = _WebModels.Field(
                description=(
                    "Priority level of the recommendation (e.g. high, medium, low)."
                ),
            )
            category: str = _WebModels.Field(
                description=(
                    "Category the recommendation belongs to (e.g. content, style, "
                    "links)."
                ),
            )
            recommendation: str = _WebModels.Field(
                description=(
                    "Human-readable text describing the recommended improvement."
                ),
            )
            actions: t.StrSequence = _WebModels.Field(
                default_factory=tuple,
                description=(
                    "Concrete action items suggested to address the recommendation."
                ),
            )

        class AuditorResults(_WebModels.ManagedModel):
            """Results for documentation audit execution."""

            timestamp: str = _WebModels.Field(
                description="Timestamp at which the documentation audit was executed.",
            )
            files_analyzed: int = _WebModels.Field(
                default=0,
                description="Number of documentation files the audit analyzed.",
            )
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
                ],
                description=(
                    "Raw issue records collected during the audit, keyed by field name."
                ),
            )
            metrics: FlextQualityModelsPart02.Quality.AuditMetrics = _WebModels.Field(
                description=(
                    "Aggregate quality metrics computed from the audit's findings."
                ),
            )
            recommendations: MutableSequence[
                FlextQualityModelsPart02.Quality.AuditRecommendation
            ] = _WebModels.Field(
                default_factory=list[
                    "FlextQualityModelsPart02.Quality.AuditRecommendation"
                ],
                description="Recommendations generated from the audit's findings.",
            )

        class LinkRecord(_WebModels.ManagedModel):
            """Record of a link found in documentation."""

            text: str = _WebModels.Field(
                description="Visible text of the link as it appears in the document.",
            )
            url: str = _WebModels.Field(
                description="Target URL or path the link points to.",
            )
            type: str = _WebModels.Field(
                description="Kind of link (e.g. external, internal, anchor, image).",
            )
            file: str = _WebModels.Field(
                description="Path of the documentation file the link was found in.",
            )
            line_number: int | None = _WebModels.Field(
                default=None,
                description="One-based line number where the link was found.",
            )
            reference: str | None = _WebModels.Field(
                default=None,
                description="Reference label, for reference-style Markdown links.",
            )
            context: t.JsonMapping | None = _WebModels.Field(
                default=None,
                description=(
                    "Optional structured context data associated with the link."
                ),
            )

        class LinkCheckResult(_WebModels.ManagedModel):
            """Result of checking a single link."""

            valid: bool | None = _WebModels.Field(
                default=None,
                description=(
                    "Whether the link was found to be valid; None if not yet checked."
                ),
            )
            url: str | None = _WebModels.Field(
                default=None,
                description="Target URL or path that was checked.",
            )
            file: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Path of the documentation file the checked link was found in."
                ),
            )
            line: int | None = _WebModels.Field(
                default=None,
                description="One-based line number where the checked link was found.",
            )
            status_code: int | None = _WebModels.Field(
                default=None,
                description="HTTP status code returned when checking an external link.",
            )
            error: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Error message describing why the link check failed, when "
                    "applicable."
                ),
            )
            type: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Kind of link that was checked (e.g. external, internal, anchor, "
                    "image)."
                ),
            )
            target: str | None = _WebModels.Field(
                default=None,
                description="Resolved target the link points to.",
            )
            src: str | None = _WebModels.Field(
                default=None,
                description="Source attribute value for an image or media link.",
            )
            text: str | None = _WebModels.Field(
                default=None,
                description="Visible text of the checked link.",
            )
            anchor: str | None = _WebModels.Field(
                default=None,
                description="Heading anchor the link references, when applicable.",
            )
            warning: str | None = _WebModels.Field(
                default=None,
                description="Non-fatal warning raised while checking the link.",
            )
            context: t.JsonMapping = _WebModels.Field(
                default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
                description=(
                    "Additional structured context captured while checking the link."
                ),
            )
            response_time: float | None = _WebModels.Field(
                default=None,
                description=(
                    "Time taken, in seconds, to receive a response for the link check."
                ),
            )
            redirected: bool | None = _WebModels.Field(
                default=None,
                description=(
                    "Whether the link check followed one or more HTTP redirects."
                ),
            )
            final_url: str | None = _WebModels.Field(
                default=None,
                description="Final URL reached after following any redirects.",
            )
            content_type: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Content-Type header value returned by the checked link's response."
                ),
            )

        class LinkPerformanceMetrics(_WebModels.ManagedModel):
            """Measured link validation duration."""

            total_time: float = _WebModels.Field(
                default=0.0,
                description="Total time, in seconds, spent validating all links.",
            )
            average_response_time: float = _WebModels.Field(
                default=0.0,
                description=(
                    "Average response time, in seconds, across all checked links."
                ),
            )
            slowest_response: float = _WebModels.Field(
                default=0.0,
                description=(
                    "Slowest single response time, in seconds, observed while "
                    "checking links."
                ),
            )

        class ContentIssue(_WebModels.ManagedModel):
            """FlextQualityModelsPart02.Quality.Issue found in documentation content."""

            type: str = _WebModels.Field(
                description="Identifier of the content issue type.",
            )
            file: str | None = _WebModels.Field(
                default=None,
                description="Path of the documentation file the issue was found in.",
            )
            line: int | None = _WebModels.Field(
                default=None,
                description="One-based line number where the issue was found.",
            )
            content: str | None = _WebModels.Field(
                default=None,
                description="Text content associated with the issue.",
            )
            error: str | None = _WebModels.Field(
                default=None,
                description="Error message describing the issue, when applicable.",
            )
            word_count: int | None = _WebModels.Field(
                default=None,
                description=(
                    "Word count measured for the content associated with the issue."
                ),
            )
            readability_score: float | None = _WebModels.Field(
                default=None,
                description=(
                    "Readability score measured for the content associated with the "
                    "issue."
                ),
            )
            warning: str | None = _WebModels.Field(
                default=None,
                description="Non-fatal warning message associated with the issue.",
            )

        class LinkValidatorResults(_WebModels.ManagedModel):
            """Results for documentation link validation."""

            timestamp: str = _WebModels.Field(
                description="Timestamp at which the link validation run was executed.",
            )
            links_checked: int = _WebModels.Field(
                default=0,
                description="Total number of links checked during the run.",
            )
            valid_links: int = _WebModels.Field(
                default=0,
                description="Number of links found to be valid.",
            )
            broken_links: int = _WebModels.Field(
                default=0,
                description="Number of links found to be broken.",
            )
            warnings: int = _WebModels.Field(
                default=0,
                description="Number of non-fatal warnings raised during the run.",
            )
            errors: MutableSequence[
                FlextQualityModelsPart02.Quality.LinkCheckResult
            ] = _WebModels.Field(
                default_factory=list[
                    "FlextQualityModelsPart02.Quality.LinkCheckResult"
                ],
                description="Detailed results for links that failed validation.",
            )
            warnings_list: MutableSequence[
                FlextQualityModelsPart02.Quality.LinkCheckResult
            ] = _WebModels.Field(
                default_factory=list[
                    "FlextQualityModelsPart02.Quality.LinkCheckResult"
                ],
                description=(
                    "Detailed results for links that produced a non-fatal warning."
                ),
            )
            performance: FlextQualityModelsPart02.Quality.LinkPerformanceMetrics = (
                _WebModels.Field(
                    description=(
                        "Measured timing performance of the link validation run."
                    ),
                )
            )

        class ContentValidatorResults(_WebModels.ManagedModel):
            """Results for documentation content validation."""

            timestamp: str = _WebModels.Field(
                description=(
                    "Timestamp at which the content validation run was executed."
                ),
            )
            files_checked: int = _WebModels.Field(
                default=0,
                description="Number of documentation files checked during the run.",
            )
            content_issues: MutableSequence[
                FlextQualityModelsPart02.Quality.ContentIssue
            ] = _WebModels.Field(
                default_factory=list["FlextQualityModelsPart02.Quality.ContentIssue"],
                description="Content issues found across all checked files.",
            )
            quality_metrics: t.MutableScalarMapping = _WebModels.Field(
                default_factory=dict[str, t.Scalar],
                description=(
                    "Aggregate scalar quality metrics computed from the checked "
                    "content."
                ),
            )

        class ContentMetrics(_WebModels.ManagedModel):
            """Content quality metrics for a documentation file."""

            word_count: int = _WebModels.Field(
                default=0,
                description="Number of words in the document.",
            )
            sentence_count: int = _WebModels.Field(
                default=0,
                description="Number of sentences in the document.",
            )
            avg_words_per_sentence: float = _WebModels.Field(
                default=0.0,
                description="Average number of words per sentence in the document.",
            )
            readability_score: float = _WebModels.Field(
                default=0.0,
                description="Computed readability score for the document.",
            )
            has_code_blocks: bool = _WebModels.Field(
                default=False,
                description="Whether the document contains one or more code blocks.",
            )
            has_lists: bool = _WebModels.Field(
                default=False,
                description="Whether the document contains one or more lists.",
            )
            has_headers: bool = _WebModels.Field(
                default=False,
                description="Whether the document contains one or more headings.",
            )

        class ChannelConfig(_WebModels.ManagedModel):
            """Notification channel toggle configuration."""

            enabled: bool = _WebModels.Field(
                default=True,
                description="Whether this notification channel is active.",
            )

        class NotifierResults(_WebModels.ManagedModel):
            """Results for documentation notification runs."""

            notifications_sent: int = _WebModels.Field(
                default=0,
                description="Number of notifications successfully sent.",
            )
            errors: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description="Error messages produced while sending notifications.",
            )
            timestamp: str = _WebModels.Field(
                description="Timestamp at which the notification run was executed.",
            )

        class AuditRulesConfig(_WebModels.FlexibleInternalModel):
            """Configuration for audit rules and thresholds."""

            quality_thresholds: _Part02.Quality.QualityThresholdsConfig = (
                _WebModels.Field(
                    description=(
                        "Threshold limits applied when auditing documentation quality."
                    ),
                )
            )
            content_checks: FlextQualityModelsPart02.Quality.ContentChecksConfig = (
                _WebModels.Field(
                    description=(
                        "Toggles controlling which content checks are performed during "
                        "the audit."
                    ),
                )
            )
            severity_levels: FlextQualityModelsPart02.Quality.SeverityLevelsConfig = (
                _WebModels.Field(
                    description=(
                        "Mapping of issue type identifiers to severity level "
                        "categorization."
                    ),
                )
            )

        class StyleGuideConfig(_WebModels.FlexibleInternalModel):
            """Configuration for style guide rules."""

            markdown: FlextQualityModelsPart02.Quality.MarkdownStyleConfig = (
                _WebModels.Field(description="Preferred Markdown style conventions.")
            )
            accessibility: FlextQualityModelsPart02.Quality.AccessibilityConfig = (
                _WebModels.Field(
                    description=(
                        "Accessibility requirements applied by the style guide."
                    ),
                )
            )
            formatting: FlextQualityModelsPart02.Quality.FormattingConfig = (
                _WebModels.Field(
                    description="Formatting standards applied by the style guide.",
                )
            )
            headings: FlextQualityModelsPart02.Quality.HeadingsConfig = (
                _WebModels.Field(
                    description="Heading hierarchy policy applied by the style guide.",
                )
            )
            code: FlextQualityModelsPart02.Quality.CodeStyleConfig = _WebModels.Field(
                description="Code block style policy applied by the style guide.",
            )

        class ValidationConfig(_WebModels.FlexibleInternalModel):
            """Configuration for validation settings."""

            validation: FlextQualityModelsPart02.Quality.ValidationRunConfig = (
                _WebModels.Field(
                    description="Execution limits applied to validation runs.",
                )
            )
            link_validation: FlextQualityModelsPart02.Quality.LinkValidationConfig = (
                _WebModels.Field(
                    description="Settings controlling how links are validated.",
                )
            )
            content_analysis: FlextQualityModelsPart02.Quality.ContentAnalysisConfig = (
                _WebModels.Field(
                    description=(
                        "Settings controlling how document content is analyzed."
                    ),
                )
            )

        class OptimizerResults(_WebModels.ManagedModel):
            """Results of a documentation optimization run."""

            timestamp: str = _WebModels.Field(
                description=(
                    "Timestamp at which the documentation optimization run was "
                    "executed."
                ),
            )
            files_processed: int = _WebModels.Field(
                default=0,
                description="Number of documentation files processed during the run.",
            )
            changes_made: int = _WebModels.Field(
                default=0,
                description=(
                    "Number of changes applied to documentation files during the run."
                ),
            )
            backups_created: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description=(
                    "Paths of backup files created before modifying documentation."
                ),
            )
            optimizations: MutableSequence[t.MutableStrMapping] = _WebModels.Field(
                default_factory=list[t.MutableStrMapping],
                description=(
                    "Records describing each optimization applied during the run."
                ),
            )

        class ExecutionRequest(_WebModels.ManagedModel):
            """Request payload for a deferred command execution."""

            script_path: Path = _WebModels.Field(
                description="Filesystem path of the script to execute.",
            )
            runtime: str = _WebModels.Field(
                description=(
                    "Runtime used to execute the script (e.g. python, typescript, "
                    "ruff, basedpyright)."
                ),
            )
            args: t.StrSequence = _WebModels.Field(
                default_factory=tuple,
                description="Command-line arguments passed to the script.",
            )
            timeout_ms: int = _WebModels.Field(
                description=(
                    "Maximum time, in milliseconds, the execution may run before "
                    "being terminated."
                ),
            )

        class ExecutionResult(_WebModels.ManagedModel):
            """Structured result payload from a command execution."""

            success: bool = _WebModels.Field(
                description="Whether the executed command completed successfully.",
            )
            exit_code: int = _WebModels.Field(
                description="Process exit code returned by the executed command.",
            )
            stdout: str = _WebModels.Field(
                default="",
                description="Standard output captured from the executed command.",
            )
            stderr: str = _WebModels.Field(
                default="",
                description="Standard error output captured from the executed command.",
            )

        class McpToolCall(_WebModels.ManagedModel):
            """MCP tool invocation request contract."""

            server: str = _WebModels.Field(
                description="Identifier of the MCP server hosting the tool to invoke.",
            )
            tool: str = _WebModels.Field(
                description="Name of the MCP tool to invoke on the server.",
            )
            params: t.JsonMapping = _WebModels.Field(
                default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
                description="Parameters passed to the invoked MCP tool.",
            )

        class McpToolResult(_WebModels.ManagedModel):
            """MCP tool invocation response contract."""

            success: bool = _WebModels.Field(
                description="Whether the MCP tool invocation completed successfully.",
            )
            data: t.StrMapping | None = _WebModels.Field(
                default=None,
                description="Data payload returned by the MCP tool invocation.",
            )
            error: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Error message returned by the MCP tool invocation, when "
                    "applicable."
                ),
            )


_Part02 = FlextQualityModelsPart02

__all__: list[str] = ["FlextQualityModelsPart02"]
