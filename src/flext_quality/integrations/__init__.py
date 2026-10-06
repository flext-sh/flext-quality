# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.integrations package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient


__all__: tuple[str, ...] = (
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityMcpClient",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityClaudeContextClient": ".claude_context",
        "FlextQualityClaudeMemClient": ".claude_mem",
        "FlextQualityCodeExecutionBridge": ".code_execution",
        "FlextQualityMcpClient": ".mcp_client",
    }),
    public_exports=__all__,
)
