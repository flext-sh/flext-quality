# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Mcp package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_quality.mcp.resources as _flext_quality_mcp_resources

    resources = _flext_quality_mcp_resources
    import flext_quality.mcp.server as _flext_quality_mcp_server
    from flext_quality.mcp.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )

    server = _flext_quality_mcp_server
    import flext_quality.mcp.tools as _flext_quality_mcp_tools
    from flext_quality.mcp.server import get_server

    tools = _flext_quality_mcp_tools
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_quality.mcp.tools import (
        execute_hook,
        search_code,
        search_memory,
        validate_rules,
    )
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

__all__ = [
    "c",
    "d",
    "e",
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "h",
    "m",
    "p",
    "r",
    "resources",
    "s",
    "search_code",
    "search_memory",
    "server",
    "t",
    "tools",
    "u",
    "validate_rules",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
