"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping

from flext_cli import FlextCliTypes
from flext_web import FlextWebTypes

from flext_core import FlextTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = FlextTypes.ContainerValueMapping
        type HookOutput = FlextTypes.ContainerValueMapping
        type HookMatcher = FlextWebTypes.StrSequence | None
        type RuleConfig = FlextTypes.ContainerValueMapping
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = FlextTypes.ContainerValueMapping
        type McpResource = FlextWebTypes.StrMapping
        type MemoryQuery = Mapping[str, str | int | FlextWebTypes.StrSequence]
        type ContextQuery = FlextTypes.HeaderMapping
        type GenericItem = (
            FlextTypes.Container | Mapping[str, FlextTypes.Primitives | None]
        )


t = FlextQualityTypes
