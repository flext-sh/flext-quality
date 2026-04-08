# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Mcp package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "execute_hook": ("flext_quality.mcp.tools", "execute_hook"),
    "get_hooks_config": ("flext_quality.mcp.resources", "get_hooks_config"),
    "get_integrations_status": (
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ),
    "get_rules_config": ("flext_quality.mcp.resources", "get_rules_config"),
    "get_server": ("flext_quality.mcp.server", "get_server"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "resources": "flext_quality.mcp.resources",
    "s": ("flext_core.service", "FlextService"),
    "search_code": ("flext_quality.mcp.tools", "search_code"),
    "search_memory": ("flext_quality.mcp.tools", "search_memory"),
    "server": "flext_quality.mcp.server",
    "t": ("flext_core.typings", "FlextTypes"),
    "tools": "flext_quality.mcp.tools",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate_rules": ("flext_quality.mcp.tools", "validate_rules"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
