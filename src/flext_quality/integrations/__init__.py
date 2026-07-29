# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.integrations package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .claude_context import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from .claude_mem import FlextQualityClaudeMemClient as FlextQualityClaudeMemClient
    from .code_execution import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from .mcp_client import FlextQualityMcpClient as FlextQualityMcpClient

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".claude_context": ("FlextQualityClaudeContextClient",),
    ".claude_mem": ("FlextQualityClaudeMemClient",),
    ".code_execution": ("FlextQualityCodeExecutionBridge",),
    ".mcp_client": ("FlextQualityMcpClient",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
