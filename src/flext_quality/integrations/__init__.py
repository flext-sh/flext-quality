# AUTO-GENERATED FILE — Regenerate with: make gen
"""Integrations package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityClaudeContextClient": ".claude_context",
    "FlextQualityClaudeMemClient": ".claude_mem",
    "FlextQualityCodeExecutionBridge": ".code_execution",
    "FlextQualityMcpClient": ".mcp_client",
    "build_mcp_health_result": "._health",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
