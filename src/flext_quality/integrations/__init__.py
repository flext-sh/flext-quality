# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.integrations package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .claude_context import FlextQualityClaudeContextClient
    from .claude_mem import FlextQualityClaudeMemClient
    from .code_execution import FlextQualityCodeExecutionBridge
    from .mcp_client import FlextQualityMcpClient
__all__: tuple[str, ...] = (
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".claude_context": ("FlextQualityClaudeContextClient",),
            ".claude_mem": ("FlextQualityClaudeMemClient",),
            ".code_execution": ("FlextQualityCodeExecutionBridge",),
            ".mcp_client": ("FlextQualityMcpClient",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
