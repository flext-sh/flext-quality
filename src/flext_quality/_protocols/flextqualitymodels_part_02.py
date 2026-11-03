# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_quality/_protocols/flextqualitymodels_part_02
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_web import FlextWebProtocols

from flext_quality import t

if TYPE_CHECKING:
    from flext_quality._constants import FlextQualityConstantsEnums
    from flext_quality._protocols import FlextQualityProtocolsFlextqualitymodelsPart01


class FlextQualityProtocolsFlextqualitymodelsPart02:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ScheduleTaskConfig(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        description: str
        command: str

        @property
        def timeout(self) -> t.PositiveInt:
            """Structural member projected from the owning model.

            Maximum time, in seconds, the task command may run before being
            terminated.
            """
            ...

    @runtime_checkable
    class ScheduleEntry(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        enabled: bool
        time: str
        tasks: Sequence[str]
        day: str | None

    @runtime_checkable
    class ErrorHandlingConfig(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def max_retries(self) -> t.NonNegativeInt:
            """Maximum number of times a failed scheduled task is retried."""
            ...

        @property
        def retry_delay(self) -> t.NonNegativeInt:
            """Structural member projected from the owning model.

            Delay, in seconds, between retry attempts for a failed scheduled task.
            """
            ...

        fail_fast: bool
        notify_on_failure: bool

    @runtime_checkable
    class LoggingConfig(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        enabled: bool
        log_file: str
        max_log_size: str

        @property
        def retention_days(self) -> t.PositiveInt:
            """Number of days rotated log files are retained before deletion."""
            ...

    @runtime_checkable
    class MaintenanceConfig(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        enabled: bool
        reports_dir: str
        backup_dir: str

        @property
        def schedules(
            self,
        ) -> Mapping[str, FlextQualityProtocolsFlextqualitymodelsPart02.ScheduleEntry]:
            """Named schedule entries controlling when maintenance tasks run."""
            ...

        @property
        def tasks(
            self,
        ) -> Mapping[
            str, FlextQualityProtocolsFlextqualitymodelsPart02.ScheduleTaskConfig
        ]:
            """Named task definitions available to be run by schedule entries."""
            ...

        @property
        def error_handling(
            self,
        ) -> FlextQualityProtocolsFlextqualitymodelsPart02.ErrorHandlingConfig:
            """Structural member projected from the owning model.

            Error handling policy applied to scheduled maintenance task failures.
            """
            ...

        @property
        def logging(
            self,
        ) -> FlextQualityProtocolsFlextqualitymodelsPart02.LoggingConfig:
            """Logging configuration applied to scheduled maintenance runs."""
            ...

    @runtime_checkable
    class ScheduleResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        start_time: str
        tasks_completed: int
        errors: MutableSequence[str]
        warnings: MutableSequence[str]
        end_time: str
        duration_seconds: int

    @runtime_checkable
    class ArgumentOptionSpec(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        flags: Sequence[str]
        help: str

        @property
        def action(self) -> FlextQualityConstantsEnums.ArgumentAction | None:
            """Structural member projected from the owning model.

            Argparse action to perform when the option is provided (e.g.
            store_true).
            """
            ...

        default: t.JsonValue | None

        @property
        def value_type(self) -> FlextQualityConstantsEnums.ArgumentValueType | None:
            """Structural member projected from the owning model.

            Type the option's value is converted to (e.g. string, integer, boolean).
            """
            ...

        nargs: int | str | None
        choices: Sequence[str] | None
        dest: str | None

    @runtime_checkable
    class ArgumentParserSpec(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        description: str

        @property
        def options(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart02.ArgumentOptionSpec]:
            """Option specifications registered on the command-line parser."""
            ...

    @runtime_checkable
    class AuditRecommendation(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        priority: str
        category: str
        recommendation: str
        actions: Sequence[str]

    @runtime_checkable
    class AuditorResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        timestamp: str
        files_analyzed: int
        issues: MutableSequence[
            MutableMapping[
                str, t.Primitives | Sequence[str] | Sequence[Mapping[str, str]] | None
            ]
        ]

        @property
        def metrics(self) -> FlextQualityProtocolsFlextqualitymodelsPart01.AuditMetrics:
            """Aggregate quality metrics computed from the audit's findings."""
            ...

        @property
        def recommendations(
            self,
        ) -> Sequence[
            FlextQualityProtocolsFlextqualitymodelsPart02.AuditRecommendation
        ]:
            """Recommendations generated from the audit's findings."""
            ...

    @runtime_checkable
    class LinkRecord(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        text: str
        url: str
        type: str
        file: str
        line_number: int | None
        reference: str | None
        context: t.JsonMapping | None

    @runtime_checkable
    class LinkCheckResult(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

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
        context: t.JsonMapping
        response_time: float | None
        redirected: bool | None
        final_url: str | None
        content_type: str | None

    @runtime_checkable
    class LinkPerformanceMetrics(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        total_time: float
        average_response_time: float
        slowest_response: float

    @runtime_checkable
    class ContentIssue(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        type: str
        file: str | None
        line: int | None
        content: str | None
        error: str | None
        word_count: int | None
        readability_score: float | None
        warning: str | None

    @runtime_checkable
    class LinkValidatorResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        timestamp: str
        links_checked: int
        valid_links: int
        broken_links: int
        warnings: int

        @property
        def errors(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart02.LinkCheckResult]:
            """Detailed results for links that failed validation."""
            ...

        @property
        def warnings_list(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart02.LinkCheckResult]:
            """Detailed results for links that produced a non-fatal warning."""
            ...

        @property
        def performance(
            self,
        ) -> FlextQualityProtocolsFlextqualitymodelsPart02.LinkPerformanceMetrics:
            """Measured timing performance of the link validation run."""
            ...

    @runtime_checkable
    class ContentValidatorResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        timestamp: str
        files_checked: int

        @property
        def content_issues(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart02.ContentIssue]:
            """Content issues found across all checked files."""
            ...

        quality_metrics: MutableMapping[str, t.Scalar]

    @runtime_checkable
    class ContentMetrics(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        word_count: int
        sentence_count: int
        avg_words_per_sentence: float
        readability_score: float
        has_code_blocks: bool
        has_lists: bool
        has_headers: bool

    @runtime_checkable
    class ChannelConfig(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        enabled: bool

    @runtime_checkable
    class NotifierResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        notifications_sent: int
        errors: MutableSequence[str]
        timestamp: str

    @runtime_checkable
    class OptimizerResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        timestamp: str
        files_processed: int
        changes_made: int
        backups_created: MutableSequence[str]
        optimizations: MutableSequence[t.MutableStrMapping]

    @runtime_checkable
    class ExecutionRequest(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        script_path: Path
        runtime: str
        args: Sequence[str]
        timeout_ms: int

    @runtime_checkable
    class ExecutionResult(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        success: bool
        exit_code: int
        stdout: str
        stderr: str

    @runtime_checkable
    class McpToolCall(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        server: str
        tool: str
        params: t.JsonMapping

    @runtime_checkable
    class McpToolResult(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        success: bool
        data: Mapping[str, str] | None
        error: str | None


__all__: list[str] = [
    "FlextQualityProtocolsFlextqualitymodelsPart02",
]
