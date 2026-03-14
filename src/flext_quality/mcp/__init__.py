# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""MCP Server module - FastMCP-based server for Claude Code integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
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

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "execute_hook": ("flext_quality.mcp.tools", "execute_hook"),
    "get_hooks_config": ("flext_quality.mcp.resources", "get_hooks_config"),
    "get_integrations_status": (
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ),
    "get_rules_config": ("flext_quality.mcp.resources", "get_rules_config"),
    "get_server": ("flext_quality.mcp.server", "get_server"),
    "mcp": ("flext_quality.mcp.server", "mcp"),
    "search_code": ("flext_quality.mcp.tools", "search_code"),
    "search_memory": ("flext_quality.mcp.tools", "search_memory"),
    "validate_rules": ("flext_quality.mcp.tools", "validate_rules"),
}

__all__ = [
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "mcp",
    "search_code",
    "search_memory",
    "validate_rules",
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
