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

if TYPE_CHECKING:
    from flext_quality import c, t


class FlextQualityProtocolsFlextqualitymodelsPart01:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AuditMetrics(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        total_issues: int
        severity_breakdown: MutableMapping[str, int]
        quality_score: int
        files_analyzed: int
        issues_per_file: float

    @runtime_checkable
    class StyleIssue(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: str
        line: int
        content: str
        message: str
        severity: str

    @runtime_checkable
    class StyleFileResults(FlextWebProtocols.BaseModel, Protocol):
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
    class StyleSummaryMetrics(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        total_violations: int
        critical_issues: int
        warnings: int
        suggestions_count: int
        accessibility_issues: int

    @runtime_checkable
    class StyleValidationResults(FlextWebProtocols.BaseModel, Protocol):
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
    class RuleDefinition(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        type: c.Quality.RuleType
        description: str
        pattern: str | None
        action: str
        enabled: bool

    @runtime_checkable
    class Issue(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: str
        severity: str
        file: str
        line: int | None
        description: str
        recommendation: str
        context: Mapping[str, t.Primitives | None] | None

    @runtime_checkable
    class ValidationResult(FlextWebProtocols.BaseModel, Protocol):
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
    class FileMetadata(FlextWebProtocols.BaseModel, Protocol):
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
