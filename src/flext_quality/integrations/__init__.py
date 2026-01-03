"""Integrations - External service clients (Claude Mem, Claude Context, etc.).

Provides clients for MCP servers and code execution capabilities
for quality analysis workflows.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.integrations.claude_context import FlextQualityClaudeContextClient
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
