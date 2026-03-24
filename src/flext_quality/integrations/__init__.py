# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Integrations - External service clients (Claude Mem, Claude Context, etc.).

Provides clients for MCP servers and code execution capabilities
for quality analysis workflows.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

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

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
