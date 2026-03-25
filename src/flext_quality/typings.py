"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from flext_cli import FlextCliTypes
from flext_core import FlextTypes
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = Mapping[str, FlextTypes.NormalizedValue]
        type HookOutput = Mapping[str, FlextTypes.NormalizedValue]
        type HookMatcher = FlextWebTypes.StrSequence | None
        type RuleConfig = Mapping[str, FlextTypes.NormalizedValue]
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = Mapping[str, FlextTypes.NormalizedValue]
        type McpResource = FlextWebTypes.StrMapping
        type MemoryQuery = Mapping[str, str | int | FlextWebTypes.StrSequence]
        type ContextQuery = Mapping[str, str | int]
        type GenericItem = (
            FlextTypes.Primitives | Path | Mapping[str, FlextTypes.Primitives | None]
        )


t = FlextQualityTypes
