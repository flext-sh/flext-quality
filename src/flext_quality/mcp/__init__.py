# AUTO-GENERATED FILE — Regenerate with: make gen
"""Mcp package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "execute_hook": ".tools",
    "get_hooks_config": ".resources",
    "get_integrations_status": ".resources",
    "get_rules_config": ".resources",
    "get_server": ".server",
    "search_code": ".tools",
    "search_memory": ".tools",
    "validate_rules": ".tools",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
