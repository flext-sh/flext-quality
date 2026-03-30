# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""MCP Server module - FastMCP-based server for Claude Code integration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.mcp import (
        resources as resources,
        server as server,
        tools as tools,
    )
    from flext_quality.mcp.resources import (
        get_hooks_config as get_hooks_config,
        get_integrations_status as get_integrations_status,
        get_rules_config as get_rules_config,
    )
    from flext_quality.mcp.server import get_server as get_server, mcp as mcp
    from flext_quality.mcp.tools import (
        execute_hook as execute_hook,
        search_code as search_code,
        search_memory as search_memory,
        validate_rules as validate_rules,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "execute_hook": ["flext_quality.mcp.tools", "execute_hook"],
    "get_hooks_config": ["flext_quality.mcp.resources", "get_hooks_config"],
    "get_integrations_status": [
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ],
    "get_rules_config": ["flext_quality.mcp.resources", "get_rules_config"],
    "get_server": ["flext_quality.mcp.server", "get_server"],
    "mcp": ["flext_quality.mcp.server", "mcp"],
    "resources": ["flext_quality.mcp.resources", ""],
    "search_code": ["flext_quality.mcp.tools", "search_code"],
    "search_memory": ["flext_quality.mcp.tools", "search_memory"],
    "server": ["flext_quality.mcp.server", ""],
    "tools": ["flext_quality.mcp.tools", ""],
    "validate_rules": ["flext_quality.mcp.tools", "validate_rules"],
}

_EXPORTS: Sequence[str] = [
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "mcp",
    "resources",
    "search_code",
    "search_memory",
    "server",
    "tools",
    "validate_rules",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
