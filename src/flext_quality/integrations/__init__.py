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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.integrations import (
        _health,
        claude_context,
        claude_mem,
        code_execution,
        mcp_client,
    )
    from flext_quality.integrations._health import build_mcp_health_result
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient,
        McpToolCall,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityClaudeContextClient": "flext_quality.integrations.claude_context",
    "FlextQualityClaudeMemClient": "flext_quality.integrations.claude_mem",
    "FlextQualityCodeExecutionBridge": "flext_quality.integrations.code_execution",
    "FlextQualityMcpClient": "flext_quality.integrations.mcp_client",
    "McpToolCall": "flext_quality.integrations.claude_mem",
    "_health": "flext_quality.integrations._health",
    "build_mcp_health_result": "flext_quality.integrations._health",
    "claude_context": "flext_quality.integrations.claude_context",
    "claude_mem": "flext_quality.integrations.claude_mem",
    "code_execution": "flext_quality.integrations.code_execution",
    "mcp_client": "flext_quality.integrations.mcp_client",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
