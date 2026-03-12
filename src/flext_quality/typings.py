"""Type definitions for flext-quality."""

from __future__ import annotations

from typing import TypeAlias

from flext_cli import FlextCliTypes
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        HookInput: TypeAlias = dict[str, object]
        HookOutput: TypeAlias = dict[str, object]
        HookMatcher: TypeAlias = list[str] | None
        RuleConfig: TypeAlias = dict[str, object]
        RuleResult: TypeAlias = tuple[bool, str | None]
        McpToolResult: TypeAlias = dict[str, object]
        McpResource: TypeAlias = dict[str, str]
        MemoryQuery: TypeAlias = dict[str, str | int | list[str]]
        ContextQuery: TypeAlias = dict[str, str | int]


t = FlextQualityTypes
