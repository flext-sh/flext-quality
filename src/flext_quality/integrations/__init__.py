# AUTO-GENERATED FILE — Regenerate with: make gen
"""Integrations package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient as FlextQualityClaudeMemClient,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient as FlextQualityMcpClient,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".claude_context": ("FlextQualityClaudeContextClient",),
    ".claude_mem": ("FlextQualityClaudeMemClient",),
    ".code_execution": ("FlextQualityCodeExecutionBridge",),
    ".mcp_client": ("FlextQualityMcpClient",),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
