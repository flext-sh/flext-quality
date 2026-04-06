# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integrations package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_quality.integrations._health as _flext_quality_integrations__health

    _health = _flext_quality_integrations__health
    import flext_quality.integrations.claude_context as _flext_quality_integrations_claude_context
    from flext_quality.integrations._health import build_mcp_health_result

    claude_context = _flext_quality_integrations_claude_context
    import flext_quality.integrations.claude_mem as _flext_quality_integrations_claude_mem
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )

    claude_mem = _flext_quality_integrations_claude_mem
    import flext_quality.integrations.code_execution as _flext_quality_integrations_code_execution
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient,
        McpToolCall,
    )

    code_execution = _flext_quality_integrations_code_execution
    import flext_quality.integrations.mcp_client as _flext_quality_integrations_mcp_client
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )

    mcp_client = _flext_quality_integrations_mcp_client
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
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient
_LAZY_IMPORTS = {
    "FlextQualityClaudeContextClient": (
        "flext_quality.integrations.claude_context",
        "FlextQualityClaudeContextClient",
    ),
    "FlextQualityClaudeMemClient": (
        "flext_quality.integrations.claude_mem",
        "FlextQualityClaudeMemClient",
    ),
    "FlextQualityCodeExecutionBridge": (
        "flext_quality.integrations.code_execution",
        "FlextQualityCodeExecutionBridge",
    ),
    "FlextQualityMcpClient": (
        "flext_quality.integrations.mcp_client",
        "FlextQualityMcpClient",
    ),
    "McpToolCall": ("flext_quality.integrations.claude_mem", "McpToolCall"),
    "_health": "flext_quality.integrations._health",
    "build_mcp_health_result": (
        "flext_quality.integrations._health",
        "build_mcp_health_result",
    ),
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

__all__ = [
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
    "McpToolCall",
    "_health",
    "build_mcp_health_result",
    "c",
    "claude_context",
    "claude_mem",
    "code_execution",
    "d",
    "e",
    "h",
    "m",
    "mcp_client",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
