# AUTO-GENERATED FILE — Regenerate with: make gen
"""Integrations package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".claude_context": ("FlextQualityClaudeContextClient",),
        ".claude_mem": ("FlextQualityClaudeMemClient",),
        ".code_execution": ("FlextQualityCodeExecutionBridge",),
        ".mcp_client": ("FlextQualityMcpClient",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
