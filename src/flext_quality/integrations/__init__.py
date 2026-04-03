# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integrations package."""

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
    from flext_quality.integrations import (
        _health,
        claude_context,
        claude_mem,
        code_execution,
        mcp_client,
    )
    from flext_quality.integrations._health import build_mcp_health_result
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient,
        McpToolCall,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextQualityClaudeContextClient": "flext_quality.integrations.claude_context",
    "FlextQualityClaudeMemClient": "flext_quality.integrations.claude_mem",
    "FlextQualityCodeExecutionBridge": "flext_quality.integrations.code_execution",
    "FlextQualityMcpClient": "flext_quality.integrations.mcp_client",
    "McpToolCall": "flext_quality.integrations.claude_mem",
    "_health": "flext_quality.integrations._health",
    "build_mcp_health_result": "flext_quality.integrations._health",
    "c": ("flext_core.constants", "FlextConstants"),
    "claude_context": "flext_quality.integrations.claude_context",
    "claude_mem": "flext_quality.integrations.claude_mem",
    "code_execution": "flext_quality.integrations.code_execution",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "mcp_client": "flext_quality.integrations.mcp_client",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
