# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Quality - Unified orchestration platform for Claude Code tooling.

Exposes `FlextQuality` as the main API facade, along with domain models,
settings, and utilities. Uses flext-core patterns: `r[T]`
railway pattern, `FlextSettings`.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality.api import FlextQuality
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.hooks.base import BaseHookImpl
    from flext_quality.hooks.manager import HookManager
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        ExecutionRequest,
        ExecutionResult,
        ExecutionResult as r,
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient,
        McpToolCall,
        McpToolResult,
    )
    from flext_quality.mcp.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )
    from flext_quality.mcp.server import get_server, mcp
    from flext_quality.mcp.tools import (
        execute_hook,
        search_code,
        search_memory,
        validate_rules,
    )
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.services.cli import (
        FlextQualityCliService,
        FlextQualityCliService as s,
    )
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, t
    from flext_quality.utilities import FlextQualityUtilities, u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "BaseHookImpl": ("flext_quality.hooks.base", "BaseHookImpl"),
    "ExecutionRequest": ("flext_quality.integrations.code_execution", "ExecutionRequest"),
    "ExecutionResult": ("flext_quality.integrations.code_execution", "ExecutionResult"),
    "FlextQuality": ("flext_quality.api", "FlextQuality"),
    "FlextQualityClaudeContextClient": ("flext_quality.integrations.claude_context", "FlextQualityClaudeContextClient"),
    "FlextQualityClaudeMemClient": ("flext_quality.integrations.claude_mem", "FlextQualityClaudeMemClient"),
    "FlextQualityCliService": ("flext_quality.services.cli", "FlextQualityCliService"),
    "FlextQualityCodeExecutionBridge": ("flext_quality.integrations.code_execution", "FlextQualityCodeExecutionBridge"),
    "FlextQualityConstants": ("flext_quality.constants", "FlextQualityConstants"),
    "FlextQualityMcpClient": ("flext_quality.integrations.mcp_client", "FlextQualityMcpClient"),
    "FlextQualityModels": ("flext_quality.models", "FlextQualityModels"),
    "FlextQualityProtocols": ("flext_quality.protocols", "FlextQualityProtocols"),
    "FlextQualityRulesEngine": ("flext_quality.rules.engine", "FlextQualityRulesEngine"),
    "FlextQualityRulesLoader": ("flext_quality.rules.loader", "FlextQualityRulesLoader"),
    "FlextQualitySettings": ("flext_quality.settings", "FlextQualitySettings"),
    "FlextQualityTypes": ("flext_quality.typings", "FlextQualityTypes"),
    "FlextQualityUtilities": ("flext_quality.utilities", "FlextQualityUtilities"),
    "FlextQualityValidators": ("flext_quality.rules.validators", "FlextQualityValidators"),
    "HookManager": ("flext_quality.hooks.manager", "HookManager"),
    "McpToolCall": ("flext_quality.integrations.mcp_client", "McpToolCall"),
    "McpToolResult": ("flext_quality.integrations.mcp_client", "McpToolResult"),
    "c": ("flext_quality.constants", "c"),
    "execute_hook": ("flext_quality.mcp.tools", "execute_hook"),
    "get_hooks_config": ("flext_quality.mcp.resources", "get_hooks_config"),
    "get_integrations_status": ("flext_quality.mcp.resources", "get_integrations_status"),
    "get_rules_config": ("flext_quality.mcp.resources", "get_rules_config"),
    "get_server": ("flext_quality.mcp.server", "get_server"),
    "m": ("flext_quality.models", "m"),
    "mcp": ("flext_quality.mcp.server", "mcp"),
    "p": ("flext_quality.protocols", "p"),
    "r": ("flext_quality.integrations.code_execution", "ExecutionResult"),
    "s": ("flext_quality.services.cli", "FlextQualityCliService"),
    "search_code": ("flext_quality.mcp.tools", "search_code"),
    "search_memory": ("flext_quality.mcp.tools", "search_memory"),
    "t": ("flext_quality.typings", "t"),
    "u": ("flext_quality.utilities", "u"),
    "validate_rules": ("flext_quality.mcp.tools", "validate_rules"),
}

__all__ = [
    "BaseHookImpl",
    "ExecutionRequest",
    "ExecutionResult",
    "FlextQuality",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCliService",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConstants",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityValidators",
    "HookManager",
    "McpToolCall",
    "McpToolResult",
    "c",
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "m",
    "mcp",
    "p",
    "r",
    "s",
    "search_code",
    "search_memory",
    "t",
    "u",
    "validate_rules",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
