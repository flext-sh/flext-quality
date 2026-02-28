"""Integrations - External service clients (Claude Mem, Claude Context, etc.).

Provides clients for MCP servers and code execution capabilities
for quality analysis workflows.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        ExecutionRequest,
        ExecutionResult,
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient,
        McpToolCall,
        McpToolResult,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "ExecutionRequest": ("flext_quality.integrations.code_execution", "ExecutionRequest"),
    "ExecutionResult": ("flext_quality.integrations.code_execution", "ExecutionResult"),
    "FlextQualityClaudeContextClient": ("flext_quality.integrations.claude_context", "FlextQualityClaudeContextClient"),
    "FlextQualityClaudeMemClient": ("flext_quality.integrations.claude_mem", "FlextQualityClaudeMemClient"),
    "FlextQualityCodeExecutionBridge": ("flext_quality.integrations.code_execution", "FlextQualityCodeExecutionBridge"),
    "FlextQualityMcpClient": ("flext_quality.integrations.mcp_client", "FlextQualityMcpClient"),
    "McpToolCall": ("flext_quality.integrations.mcp_client", "McpToolCall"),
    "McpToolResult": ("flext_quality.integrations.mcp_client", "McpToolResult"),
}

__all__ = [
    "ExecutionRequest",
    "ExecutionResult",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
    "McpToolCall",
    "McpToolResult",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
