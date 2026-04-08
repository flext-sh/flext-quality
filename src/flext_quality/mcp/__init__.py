# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Mcp package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "execute_hook": ("flext_quality.mcp.tools", "execute_hook"),
    "get_hooks_config": ("flext_quality.mcp.resources", "get_hooks_config"),
    "get_integrations_status": (
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ),
    "get_rules_config": ("flext_quality.mcp.resources", "get_rules_config"),
    "get_server": ("flext_quality.mcp.server", "get_server"),
    "search_code": ("flext_quality.mcp.tools", "search_code"),
    "search_memory": ("flext_quality.mcp.tools", "search_memory"),
    "validate_rules": ("flext_quality.mcp.tools", "validate_rules"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
