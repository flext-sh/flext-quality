# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""MCP Server module - FastMCP-based server for Claude Code integration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.mcp import resources, server, tools
    from flext_quality.mcp.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )
    from flext_quality.mcp.server import get_server, mcp
    from flext_quality.mcp.tools import (
        execute_hook,
        search_code,
        search_memory,
        validate_rules,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "execute_hook": "flext_quality.mcp.tools",
    "get_hooks_config": "flext_quality.mcp.resources",
    "get_integrations_status": "flext_quality.mcp.resources",
    "get_rules_config": "flext_quality.mcp.resources",
    "get_server": "flext_quality.mcp.server",
    "mcp": "flext_quality.mcp.server",
    "resources": "flext_quality.mcp.resources",
    "search_code": "flext_quality.mcp.tools",
    "search_memory": "flext_quality.mcp.tools",
    "server": "flext_quality.mcp.server",
    "tools": "flext_quality.mcp.tools",
    "validate_rules": "flext_quality.mcp.tools",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
