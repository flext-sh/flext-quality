"""Type definitions for flext-quality."""

from __future__ import annotations

from flext_cli import FlextCliTypes
from flext_core import t as core_t
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        type HookInput = dict[str, core_t.NormalizedValue]
        type HookOutput = dict[str, core_t.NormalizedValue]
        type HookMatcher = list[str] | None
        type RuleConfig = dict[str, core_t.NormalizedValue]
        type RuleResult = tuple[bool, str | None]
        type McpToolResult = dict[str, core_t.NormalizedValue]
        type McpResource = dict[str, str]
        type MemoryQuery = dict[str, str | int | list[str]]
        type ContextQuery = dict[str, str | int]


t = FlextQualityTypes
