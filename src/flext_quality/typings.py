"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from flext_infra import m, t
from flext_web import t as web_t


class FlextQualityTypes(t, web_t):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace (project slot)."""

        type HookInput = t.JsonMapping
        type HookOutput = t.JsonMapping
        type RuleConfig = t.JsonMapping
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = t.JsonMapping
        type GenericItem = t.JsonValue | t.MappingKV[str, t.Primitives | None]
        type DocumentationReportValue = (
            str
            | int
            | float
            | bool
            | t.StrSequence
            | t.SequenceOf[Mapping[str, t.Primitives]]
            | t.MappingKV[str, t.Primitives]
            | None
        )

        CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
            t.JsonMapping,
        )
        RELAXED_CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
            t.JsonMapping,
            config=m.ConfigDict(strict=False),
        )
        CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
            t.SequenceOf[t.JsonMapping]
        ] = m.TypeAdapter(t.SequenceOf[t.JsonMapping])
        RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
            t.SequenceOf[t.JsonMapping]
        ] = m.TypeAdapter(
            t.SequenceOf[t.JsonMapping],
            config=m.ConfigDict(strict=False),
        )
        MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER: m.TypeAdapter[
            t.MutableOptionalFeatureFlagMapping
        ] = m.TypeAdapter(t.MutableOptionalFeatureFlagMapping)
        NORMALIZED_VALUE_SEQUENCE_ADAPTER: m.TypeAdapter[t.JsonList] = m.TypeAdapter(
            t.JsonList
        )
        STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
            t.MutableSequenceOf[t.StrMapping]
        ] = m.TypeAdapter(t.MutableSequenceOf[t.StrMapping])
        REPORT_VALUE_MAPPING_ADAPTER: m.TypeAdapter[
            t.MappingKV[str, DocumentationReportValue]
        ] = m.TypeAdapter(
            t.MappingKV[str, DocumentationReportValue],
        )


t = FlextQualityTypes

__all__: list[str] = ["FlextQualityTypes", "t"]
