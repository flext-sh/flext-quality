"""Type definitions for flext-quality."""

from __future__ import annotations

from typing import TypeAlias

from flext_cli import FlextCliTypes
from flext_core import FlextTypes
from flext_web import FlextWebTypes


class FlextQualityTypes(FlextWebTypes, FlextCliTypes):
    """Namespace for flext-quality type definitions."""

    class Quality:
        """Quality-specific types namespace."""

        # Hook types
        HookInput: TypeAlias = dict[str, FlextTypes.JsonValue]
        HookOutput: TypeAlias = dict[str, FlextTypes.JsonValue]
        HookMatcher: TypeAlias = list[str] | None

        # Rule types
        RuleConfig: TypeAlias = dict[str, FlextTypes.JsonValue]
        RuleResult: TypeAlias = tuple[bool, str | None]

        # MCP types
        McpToolResult: TypeAlias = dict[str, FlextTypes.JsonValue]
        McpResource: TypeAlias = dict[str, str]

        # Integration types
        MemoryQuery: TypeAlias = dict[str, str | int | list[str]]
        ContextQuery: TypeAlias = dict[str, str | int]


# Short alias for imports
t = FlextQualityTypes
