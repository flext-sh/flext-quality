# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integrations package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
