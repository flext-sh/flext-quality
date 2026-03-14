"""Type definitions for flext-quality."""

from __future__ import annotations

from typing import TypeAlias

from flext_core import t as core_t
from flext_cli import FlextCliTypes
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        HookInput: TypeAlias = dict[str, core_t.NormalizedValue]
        HookOutput: TypeAlias = dict[str, core_t.NormalizedValue]
        HookMatcher: TypeAlias = list[str] | None
        RuleConfig: TypeAlias = dict[str, core_t.NormalizedValue]
        RuleResult: TypeAlias = tuple[bool, str | None]
        McpToolResult: TypeAlias = dict[str, core_t.NormalizedValue]
        McpResource: TypeAlias = dict[str, str]
        MemoryQuery: TypeAlias = dict[str, str | int | list[str]]
        ContextQuery: TypeAlias = dict[str, str | int]


t = FlextQualityTypes
