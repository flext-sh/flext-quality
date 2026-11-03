# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_quality/_protocols/flextqualitymodels_part_01
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_web import FlextWebProtocols

from flext_quality import t

if TYPE_CHECKING:
    from flext_quality._constants import FlextQualityConstantsEnums


class FlextQualityProtocolsFlextqualitymodelsPart01:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AuditMetrics(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        total_issues: int
        severity_breakdown: MutableMapping[str, int]
        quality_score: int
        files_analyzed: int
        issues_per_file: float

    @runtime_checkable
    class StyleIssue(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        type: str
        line: int
        content: str
        message: str
        severity: str

    @runtime_checkable
    class StyleFileResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        file: str

        @property
        def violations(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.StyleIssue]:
            """Style rule violations found in the file."""
            ...

        @property
        def issues(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.StyleIssue]:
            """Structural member projected from the owning model.

            All style issues found in the file, including violations and warnings.
            """
            ...

        suggestions: MutableSequence[str]

    @runtime_checkable
    class StyleSummaryMetrics(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        total_violations: int
        critical_issues: int
        warnings: int
        suggestions_count: int
        accessibility_issues: int

    @runtime_checkable
    class StyleValidationResults(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        files_checked: int

        @property
        def style_violations(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.StyleIssue]:
            """Style rule violations found across all checked files."""
            ...

        @property
        def accessibility_issues(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.StyleIssue]:
            """Accessibility-related issues found across all checked files."""
            ...

        @property
        def formatting_errors(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.StyleIssue]:
            """Formatting rule violations found across all checked files."""
            ...

        suggestions: MutableSequence[str]

        @property
        def summary(
            self,
        ) -> FlextQualityProtocolsFlextqualitymodelsPart01.StyleSummaryMetrics:
            """Aggregate counts summarizing the style validation run."""
            ...

    @runtime_checkable
    class RuleDefinition(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        name: str

        @property
        def type(self) -> FlextQualityConstantsEnums.RuleType:
            """Structural member projected from the owning model.

            Category of quality rule (e.g. content, style, link, accessibility).
            """
            ...

        description: str
        pattern: str | None
        action: str
        enabled: bool

    @runtime_checkable
    class Issue(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> str:
            """FlextQualityModelsPart01.Quality.Issue type identifier."""
            ...

        @property
        def severity(self) -> str:
            """Severity level identifier."""
            ...

        @property
        def file(self) -> str:
            """File path where issue was found."""
            ...

        @property
        def line(self) -> int | None:
            """FlextQualityModelsPart01.Quality.Issue line number."""
            ...

        @property
        def description(self) -> str:
            """FlextQualityModelsPart01.Quality.Issue description."""
            ...

        @property
        def recommendation(self) -> str:
            """Recommended fix."""
            ...

        @property
        def context(self) -> Mapping[str, t.Primitives | None] | None:
            """Optional structured context data associated with the issue."""
            ...

    @runtime_checkable
    class ValidationResult(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        total_items: int
        valid_items: int
        invalid_items: int

        @property
        def issues(
            self,
        ) -> Sequence[FlextQualityProtocolsFlextqualitymodelsPart01.Issue]:
            """Issues found during the validation run."""
            ...

        warnings: MutableSequence[str]
        errors: MutableSequence[str]
        metadata: MutableMapping[str, t.Primitives]

    @runtime_checkable
    class FileMetadata(FlextWebProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        path: str
        size: int
        modified_time: float
        extension: str
        is_markdown: bool
        lines: int
        words: int


__all__: list[str] = [
    "FlextQualityProtocolsFlextqualitymodelsPart01",
]
