"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence

from flext_cli import FlextCliTypes
from flext_web import FlextWebTypes
from pydantic import ConfigDict, TypeAdapter

from flext_core import FlextTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    CONTAINER_MAPPING_ADAPTER: TypeAdapter[FlextTypes.ContainerMapping] = TypeAdapter(
        FlextTypes.ContainerMapping,
    )
    RELAXED_CONTAINER_MAPPING_ADAPTER: TypeAdapter[FlextTypes.ContainerMapping] = (
        TypeAdapter(
            FlextTypes.ContainerMapping,
            config=ConfigDict(strict=False),
        )
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[
        Sequence[FlextTypes.ContainerMapping]
    ] = TypeAdapter(Sequence[FlextTypes.ContainerMapping])
    RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[
        Sequence[FlextTypes.ContainerMapping]
    ] = TypeAdapter(
        Sequence[FlextTypes.ContainerMapping],
        config=ConfigDict(strict=False),
    )
    MUTABLE_OPTIONAL_FEATURE_FLAG_MAPPING_ADAPTER: TypeAdapter[
        FlextWebTypes.MutableOptionalFeatureFlagMapping
    ] = TypeAdapter(FlextWebTypes.MutableOptionalFeatureFlagMapping)
    NORMALIZED_VALUE_SEQUENCE_ADAPTER: TypeAdapter[
        Sequence[FlextTypes.NormalizedValue]
    ] = TypeAdapter(Sequence[FlextTypes.NormalizedValue])
    STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER: TypeAdapter[
        MutableSequence[FlextWebTypes.StrMapping]
    ] = TypeAdapter(MutableSequence[FlextWebTypes.StrMapping])

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = FlextTypes.ContainerMapping
        type HookOutput = FlextTypes.ContainerMapping
        type HookMatcher = FlextWebTypes.StrSequence | None
        type RuleConfig = FlextTypes.ContainerMapping
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = FlextTypes.ContainerMapping
        type McpResource = FlextWebTypes.StrMapping
        type MemoryQuery = Mapping[str, str | int | FlextWebTypes.StrSequence]
        type ContextQuery = FlextTypes.HeaderMapping
        type GenericItem = (
            FlextTypes.Container | Mapping[str, FlextTypes.Primitives | None]
        )
        type DocumentationReportValue = (
            str
            | int
            | float
            | bool
            | FlextWebTypes.StrSequence
            | Sequence[Mapping[str, FlextTypes.Primitives]]
            | Mapping[str, FlextTypes.Primitives]
            | None
        )

    REPORT_VALUE_MAPPING_ADAPTER: TypeAdapter[
        Mapping[str, Quality.DocumentationReportValue]
    ] = TypeAdapter(Mapping[str, Quality.DocumentationReportValue])


t = FlextQualityTypes
