# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Mcp package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from flext_quality import resources, server, tools
    from flext_quality.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )
    from flext_quality.server import get_server, mcp
    from flext_quality.tools import (
        client,
        command_result,
        engine,
        execute_hook,
        params,
        result,
        search_code,
        search_limit,
        search_memory,
        validate_rules,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "c": ("flext_core.constants", "FlextConstants"),
    "client": "flext_quality.tools",
    "command_result": "flext_quality.tools",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "engine": "flext_quality.tools",
    "execute_hook": "flext_quality.tools",
    "get_hooks_config": "flext_quality.resources",
    "get_integrations_status": "flext_quality.resources",
    "get_rules_config": "flext_quality.resources",
    "get_server": "flext_quality.server",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "mcp": "flext_quality.server",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "params": "flext_quality.tools",
    "r": ("flext_core.result", "FlextResult"),
    "resources": "flext_quality.resources",
    "result": "flext_quality.tools",
    "s": ("flext_core.service", "FlextService"),
    "search_code": "flext_quality.tools",
    "search_limit": "flext_quality.tools",
    "search_memory": "flext_quality.tools",
    "server": "flext_quality.server",
    "t": ("flext_core.typings", "FlextTypes"),
    "tools": "flext_quality.tools",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate_rules": "flext_quality.tools",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
