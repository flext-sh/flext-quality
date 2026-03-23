"""Type definitions for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from flext_cli import FlextCliTypes
from flext_core import t as core_t
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = Mapping[str, core_t.NormalizedValue]
        type HookOutput = Mapping[str, core_t.NormalizedValue]
        type HookMatcher = Sequence[str] | None
        type RuleConfig = Mapping[str, core_t.NormalizedValue]
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = Mapping[str, core_t.NormalizedValue]
        type McpResource = Mapping[str, str]
        type MemoryQuery = Mapping[str, str | int | Sequence[str]]
        type ContextQuery = Mapping[str, str | int]
        type GenericItem = (
            core_t.Primitives | Path | Mapping[str, core_t.Primitives | None]
        )


t = FlextQualityTypes
