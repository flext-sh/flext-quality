# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integrations - External service clients (Claude Mem, Claude Context, etc.).

Provides clients for MCP servers and code execution capabilities
for quality analysis workflows.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.integrations import (
        claude_context as claude_context,
        claude_mem as claude_mem,
        code_execution as code_execution,
        mcp_client as mcp_client,
    )
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient as FlextQualityClaudeMemClient,
        McpToolCall as McpToolCall,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient as FlextQualityMcpClient,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityClaudeContextClient": [
        "flext_quality.integrations.claude_context",
        "FlextQualityClaudeContextClient",
    ],
    "FlextQualityClaudeMemClient": [
        "flext_quality.integrations.claude_mem",
        "FlextQualityClaudeMemClient",
    ],
    "FlextQualityCodeExecutionBridge": [
        "flext_quality.integrations.code_execution",
        "FlextQualityCodeExecutionBridge",
    ],
    "FlextQualityMcpClient": [
        "flext_quality.integrations.mcp_client",
        "FlextQualityMcpClient",
    ],
    "McpToolCall": ["flext_quality.integrations.claude_mem", "McpToolCall"],
    "claude_context": ["flext_quality.integrations.claude_context", ""],
    "claude_mem": ["flext_quality.integrations.claude_mem", ""],
    "code_execution": ["flext_quality.integrations.code_execution", ""],
    "mcp_client": ["flext_quality.integrations.mcp_client", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
    "McpToolCall",
    "claude_context",
    "claude_mem",
    "code_execution",
    "mcp_client",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
