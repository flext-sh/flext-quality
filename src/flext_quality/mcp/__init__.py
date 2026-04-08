# AUTO-GENERATED FILE — Regenerate with: make gen
"""Mcp package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".resources": (
            "get_hooks_config",
            "get_integrations_status",
            "get_rules_config",
        ),
        ".server": ("get_server",),
        ".tools": (
            "execute_hook",
            "search_code",
            "search_memory",
            "validate_rules",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
