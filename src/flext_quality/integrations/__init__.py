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
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
