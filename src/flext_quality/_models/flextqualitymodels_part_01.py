"""Quality domain models for flext-quality (part 1 of 2).

Pydantic-2 models for the documentation quality domain, split across
package parts to honor the fleet per-module LOC ceiling; the public
``flext_quality.models`` facade composes both parts through MRO.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping, MutableSequence
from typing import Annotated

from flext_web import FlextWebModels as _WebModels

from flext_quality import c, t
from flext_quality._models import FlextQualityModelsBase


class FlextQualityModelsPart01(_WebModels):
    """Namespace for flext-quality models (part 1)."""

    class Quality(FlextQualityModelsBase):
        """Quality-specific models namespace (part 1)."""

        class AuditMetrics(_WebModels.ManagedModel):
            """Typed metrics for documentation audit results."""

            total_issues: int = _WebModels.Field(
                default=0,
                description="Total number of documentation issues found by the audit.",
            )
            severity_breakdown: MutableMapping[str, int] = _WebModels.Field(
                default_factory=dict[str, int],
                description=(
                    "Count of issues found for each severity level (e.g. critical, "
                    "high, medium, low)."
                ),
            )
            quality_score: int = _WebModels.Field(
                default=0,
                description=(
                    "Overall documentation quality score from 0 to 100, higher is "
                    "better."
                ),
            )
            files_analyzed: int = _WebModels.Field(
                default=0,
                description="Number of documentation files the audit inspected.",
            )
            issues_per_file: float = _WebModels.Field(
                default=0.0,
                description="Average number of issues found per analyzed file.",
            )

        class StyleIssue(_WebModels.ManagedModel):
            """A documentation style violation."""

            type: str = _WebModels.Field(
                description="Identifier of the style rule that was violated.",
            )
            line: int = _WebModels.Field(
                description="One-based line number where the violation occurred.",
            )
            content: str = _WebModels.Field(
                description="Text content of the offending line.",
            )
            message: str = _WebModels.Field(
                description="Human-readable description of the violation.",
            )
            severity: str = _WebModels.Field(
                description=(
                    "Severity level of the violation (e.g. critical, high, medium, "
                    "low)."
                ),
            )

        class StyleFileResults(_WebModels.ManagedModel):
            """Style findings for one file."""

            file: str = _WebModels.Field(
                description="Path of the documentation file that was checked.",
            )
            violations: MutableSequence[FlextQualityModelsPart01.Quality.StyleIssue] = (
                _WebModels.Field(description="Style rule violations found in the file.")
            )
            issues: MutableSequence[FlextQualityModelsPart01.Quality.StyleIssue] = (
                _WebModels.Field(
                    description=(
                        "All style issues found in the file, including violations and "
                        "warnings."
                    ),
                )
            )
            suggestions: MutableSequence[str] = _WebModels.Field(
                description=(
                    "Human-readable suggestions for improving the file's style."
                ),
            )

        class StyleSummaryMetrics(_WebModels.ManagedModel):
            """Counts for a style validation run."""

            total_violations: int = _WebModels.Field(
                description=(
                    "Total number of style violations found across all checked files."
                ),
            )
            critical_issues: int = _WebModels.Field(
                description="Number of style issues classified as critical severity.",
            )
            warnings: int = _WebModels.Field(
                description="Number of style warnings raised during the run.",
            )
            suggestions_count: int = _WebModels.Field(
                description=(
                    "Number of style improvement suggestions generated during the run."
                ),
            )
            accessibility_issues: int = _WebModels.Field(
                description=(
                    "Number of accessibility-related style issues found during the run."
                ),
            )

        class StyleValidationResults(_WebModels.ManagedModel):
            """Aggregated style findings."""

            files_checked: int = _WebModels.Field(
                description=(
                    "Number of documentation files inspected during the style "
                    "validation run."
                ),
            )
            style_violations: MutableSequence[
                FlextQualityModelsPart01.Quality.StyleIssue
            ] = _WebModels.Field(
                description="Style rule violations found across all checked files.",
            )
            accessibility_issues: MutableSequence[
                FlextQualityModelsPart01.Quality.StyleIssue
            ] = _WebModels.Field(
                description=(
                    "Accessibility-related issues found across all checked files."
                ),
            )
            formatting_errors: MutableSequence[
                FlextQualityModelsPart01.Quality.StyleIssue
            ] = _WebModels.Field(
                description=(
                    "Formatting rule violations found across all checked files."
                ),
            )
            suggestions: MutableSequence[str] = _WebModels.Field(
                description=(
                    "Human-readable suggestions for improving style across all "
                    "checked files."
                ),
            )
            summary: FlextQualityModelsPart01.Quality.StyleSummaryMetrics = (
                _WebModels.Field(
                    description=(
                        "Aggregate counts summarizing the style validation run."
                    ),
                )
            )

        class RuleDefinition(_WebModels.ManagedModel):
            """A rule definition from YAML."""

            name: str = _WebModels.Field(
                description="Unique name identifying the rule.",
            )
            type: c.Quality.RuleType = _WebModels.Field(
                description=(
                    "Category of quality rule (e.g. content, style, link, "
                    "accessibility)."
                ),
            )
            description: str = _WebModels.Field(
                description="Human-readable explanation of what the rule checks.",
            )
            pattern: str | None = _WebModels.Field(
                default=None,
                description=(
                    "Optional regular expression pattern the rule matches against, "
                    "when applicable."
                ),
            )
            action: str = _WebModels.Field(
                description=(
                    "Action to take when the rule matches (e.g. flag as error or "
                    "warning)."
                ),
            )
            enabled: bool = _WebModels.Field(
                default=True,
                description="Whether this rule is active during validation runs.",
            )

        class Issue(_WebModels.ManagedModel):
            """Canonical issue model for documentation tooling."""

            type: Annotated[
                str,
                _WebModels.Field(
                    description=(
                        "FlextQualityModelsPart01.Quality.Issue type identifier"
                    ),
                ),
            ]
            severity: Annotated[
                str,
                _WebModels.Field(description="Severity level identifier"),
            ]
            file: Annotated[
                str,
                _WebModels.Field(description="File path where issue was found"),
            ]
            line: Annotated[
                int | None,
                _WebModels.Field(
                    description="FlextQualityModelsPart01.Quality.Issue line number",
                ),
            ] = None
            description: Annotated[
                str,
                _WebModels.Field(
                    description="FlextQualityModelsPart01.Quality.Issue description",
                ),
            ] = ""
            recommendation: Annotated[
                str,
                _WebModels.Field(description="Recommended fix"),
            ] = ""
            context: Annotated[
                t.MappingKV[str, t.Primitives | None] | None,
                _WebModels.Field(
                    default=None,
                    description=(
                        "Optional structured context data associated with the issue."
                    ),
                ),
            ]

        class ValidationResult(_WebModels.ManagedModel):
            """Canonical validation result for documentation tooling."""

            total_items: int = _WebModels.Field(
                default=0,
                description="Total number of items evaluated by the validation run.",
            )
            valid_items: int = _WebModels.Field(
                default=0,
                description="Number of items that passed validation.",
            )
            invalid_items: int = _WebModels.Field(
                default=0,
                description="Number of items that failed validation.",
            )
            issues: MutableSequence[FlextQualityModelsPart01.Quality.Issue] = (
                _WebModels.Field(
                    default_factory=list["FlextQualityModelsPart01.Quality.Issue"],
                    description="Issues found during the validation run.",
                )
            )
            warnings: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description=(
                    "Non-fatal warning messages produced during the validation run."
                ),
            )
            errors: MutableSequence[str] = _WebModels.Field(
                default_factory=list[str],
                description="Fatal error messages produced during the validation run.",
            )
            metadata: MutableMapping[str, t.Primitives] = _WebModels.Field(
                default_factory=dict[str, t.Primitives],
                description="Additional metadata describing the validation run.",
            )

        class FileMetadata(_WebModels.ManagedModel):
            """Metadata about a documentation file."""

            path: str = _WebModels.Field(
                description="Filesystem path of the documentation file.",
            )
            size: int = _WebModels.Field(default=0, description="File size in bytes.")
            modified_time: float = _WebModels.Field(
                default=0.0,
                description="Last modification time of the file, as a Unix timestamp.",
            )
            extension: str = _WebModels.Field(
                default="",
                description="File extension, including the leading dot (e.g. '.md').",
            )
            is_markdown: bool = _WebModels.Field(
                default=False,
                description="Whether the file is a Markdown document.",
            )
            lines: int = _WebModels.Field(
                default=0,
                description="Number of lines in the file.",
            )
            words: int = _WebModels.Field(
                default=0,
                description="Number of words in the file.",
            )


_Part01 = FlextQualityModelsPart01

__all__: list[str] = ["FlextQualityModelsPart01"]
