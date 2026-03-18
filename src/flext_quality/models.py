"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import FlextCliModels
from flext_web import FlextWebModels
from pydantic import BaseModel, Field

from flext_quality import c
from flext_quality.docs.core.base_classes import (
    FileMetadata as _DocsFileMetadata,
    Issue as _DocsIssue,
    ValidationResult as _DocsValidationResult,
)


class FlextQualityModels(FlextWebModels, FlextCliModels):
    """Namespace for flext-quality models.

    Usage:
        from flext_quality import m

        config = m.Quality.HookConfig(event=c.Quality.HookEvent.PRE_TOOL_USE, command="...")
        rule = m.Quality.RuleDefinition(name="rule1", type=c.Quality.RuleType.BLOCKING, ...)
    """

    class Quality:
        """Quality-specific models namespace."""

        class HookConfig(BaseModel):
            """Configuration for a hook."""

            event: c.Quality.HookEvent
            matcher: list[str] | None = None
            command: str
            timeout_ms: Annotated[
                int, Field(default=c.Quality.Defaults.HOOK_TIMEOUT_MS)
            ]
            enabled: bool = True

        class HookResult(BaseModel):
            """Result from hook execution."""

            continue_execution: Annotated[bool, Field(alias="continue")]
            system_message: Annotated[
                str | None, Field(default=None, alias="systemMessage")
            ]
            blocked_reason: str | None = None

            model_config = {"populate_by_name": True}

        class RuleDefinition(BaseModel):
            """A rule definition from YAML."""

            name: str
            type: c.Quality.RuleType
            description: str
            pattern: str | None = None
            action: str
            enabled: bool = True

        class IntegrationConfig(BaseModel):
            """Configuration for an integration."""

            name: str
            enabled: bool = True
            host: str = "localhost"
            port: int
            timeout_ms: Annotated[
                int, Field(default=c.Quality.Defaults.INTEGRATION_TIMEOUT_MS)
            ]

        class MemoryObservation(BaseModel):
            """An observation from claude-mem."""

            id: str
            type: str
            title: str
            content: str
            concepts: Annotated[list[str], Field(default_factory=list)]
            files: Annotated[list[str], Field(default_factory=list)]
            timestamp: str

        class ContextSearchResult(BaseModel):
            """A search result from claude-context."""

            file_path: str
            snippet: str
            score: float
            line_number: int | None = None

        class Issue(_DocsIssue):
            """Canonical issue model exposed through flext-quality namespace."""

        class ValidationResult(_DocsValidationResult):
            """Canonical validation result model exposed through flext-quality."""

        class FileMetadata(_DocsFileMetadata):
            """Canonical file metadata model exposed through flext-quality."""

        class ScheduleTaskConfig(BaseModel):
            """Task configuration for scheduled documentation maintenance."""

            description: str
            command: str
            timeout: int = Field(default=300, ge=1)

        class ScheduleEntry(BaseModel):
            """Single schedule entry definition."""

            enabled: bool = True
            time: str
            tasks: list[str] = Field(default_factory=list)
            day: str | None = None

        class ErrorHandlingConfig(BaseModel):
            """Error handling settings for scheduled maintenance."""

            max_retries: int = Field(default=3, ge=0)
            retry_delay: int = Field(default=60, ge=0)
            fail_fast: bool = False
            notify_on_failure: bool = True

        class LoggingConfig(BaseModel):
            """Logging configuration for scheduled maintenance."""

            enabled: bool = True
            log_file: str
            max_log_size: str = "10MB"
            retention_days: int = Field(default=30, ge=1)

        class MaintenanceConfig(BaseModel):
            """Root configuration for scheduled documentation maintenance."""

            enabled: bool = True
            reports_dir: str
            backup_dir: str
            schedules: dict[str, FlextQualityModels.Quality.ScheduleEntry] = Field(
                default_factory=dict
            )
            tasks: dict[str, FlextQualityModels.Quality.ScheduleTaskConfig] = Field(
                default_factory=dict
            )
            error_handling: FlextQualityModels.Quality.ErrorHandlingConfig
            logging: FlextQualityModels.Quality.LoggingConfig

        class ScheduleResults(BaseModel):
            """Execution summary for scheduled maintenance runs."""

            start_time: str
            tasks_completed: int = 0
            errors: list[str] = Field(default_factory=list)
            warnings: list[str] = Field(default_factory=list)
            end_time: str = ""
            duration_seconds: int = 0

        class LinkRecord(BaseModel):
            """Canonical representation of a discovered documentation link."""

            text: str
            url: str
            type: str
            file: str
            line_number: int | None = None

        class LinkCheckResult(BaseModel):
            """Canonical result model for link validation outcomes."""

            valid: bool = False
            url: str = ""
            file: str = ""
            line: int | None = None
            status_code: int | None = None
            error: str | None = None
            type: str | None = None
            target: str | None = None
            src: str | None = None
            anchor: str | None = None
            warning: str | None = None
            text: str | None = None

        class ContentIssue(BaseModel):
            """Canonical issue model for content validation operations."""

            type: str
            file: str = ""
            line: int | None = None
            content: str | None = None
            error: str | None = None
            warning: str | None = None
            word_count: int | None = None
            readability_score: float | None = None

        class LinkValidatorResults(BaseModel):
            """Results for documentation link validation."""

            timestamp: str
            links_checked: int = 0
            valid_links: int = 0
            broken_links: int = 0
            warnings: int = 0
            errors: list[FlextQualityModels.Quality.LinkCheckResult] = Field(
                default_factory=list
            )
            warnings_list: list[FlextQualityModels.Quality.LinkCheckResult] = Field(
                default_factory=list
            )

        class ContentValidatorResults(BaseModel):
            """Results for documentation content validation."""

            timestamp: str
            files_checked: int = 0
            content_issues: list[FlextQualityModels.Quality.ContentIssue] = Field(
                default_factory=list
            )
            quality_metrics: dict[str, int | float | bool] = Field(default_factory=dict)

        class ContentMetrics(BaseModel):
            """Content quality metrics for a documentation file."""

            word_count: int = 0
            sentence_count: int = 0
            avg_words_per_sentence: float = 0.0
            readability_score: float = 0.0
            has_code_blocks: bool = False
            has_lists: bool = False
            has_headers: bool = False

        class FileStatistics(BaseModel):
            """Statistics payload for discovered documentation files."""

            total_files: int
            total_size: int | None = None
            total_lines: int | None = None
            total_words: int | None = None
            markdown_files: int | None = None
            other_files: int | None = None
            size_distribution: dict[str, int] | None = None
            categories: dict[str, int] | None = None
            avg_file_size: float | None = None
            avg_lines_per_file: float | None = None
            avg_words_per_file: float | None = None

        class NotifierResults(BaseModel):
            """Results for documentation notification runs."""

            notifications_sent: int = 0
            errors: list[str] = Field(default_factory=list)
            timestamp: str


m = FlextQualityModels

__all__ = ["FlextQualityModels", "m"]
