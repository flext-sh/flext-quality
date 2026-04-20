"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)

from flext_cli import m, t
from flext_web import FlextWebTypes


class FlextQualityTypes(t, FlextWebTypes):
    """Namespace for flext-quality type definitions."""

    CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.Container]] = m.TypeAdapter(
        Mapping[str, t.Container],
    )
    RELAXED_CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.Container]] = (
        m.TypeAdapter(
            Mapping[str, t.Container],
            config=m.ConfigDict(strict=False),
        )
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
        Sequence[Mapping[str, t.Container]]
    ] = m.TypeAdapter(Sequence[Mapping[str, t.Container]])
    RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
        Sequence[Mapping[str, t.Container]]
    ] = m.TypeAdapter(
        Sequence[Mapping[str, t.Container]],
        config=m.ConfigDict(strict=False),
    )
    MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER: m.TypeAdapter[
        t.MutableOptionalFeatureFlagMapping
    ] = m.TypeAdapter(t.MutableOptionalFeatureFlagMapping)
    NORMALIZED_VALUE_SEQUENCE_ADAPTER: m.TypeAdapter[Sequence[t.RecursiveValue]] = (
        m.TypeAdapter(Sequence[t.RecursiveValue])
    )
    STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
        MutableSequence[t.StrMapping]
    ] = m.TypeAdapter(MutableSequence[t.StrMapping])

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = Mapping[str, t.Container]
        type HookOutput = Mapping[str, t.Container]
        type HookMatcher = t.StrSequence | None
        type RuleConfig = Mapping[str, t.Container]
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = Mapping[str, t.Container]
        type McpResource = t.StrMapping
        type MemoryQuery = Mapping[str, str | int | t.StrSequence]
        type ContextQuery = t.HeaderMapping
        type GenericItem = t.Container | Mapping[str, t.Primitives | None]
        type DocumentationReportValue = (
            str
            | int
            | float
            | bool
            | t.StrSequence
            | Sequence[Mapping[str, t.Primitives]]
            | Mapping[str, t.Primitives]
            | None
        )

    REPORT_VALUE_MAPPING_ADAPTER: m.TypeAdapter[
        Mapping[str, Quality.DocumentationReportValue]
    ] = m.TypeAdapter(Mapping[str, Quality.DocumentationReportValue])


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
