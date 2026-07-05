# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_QUALITY_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".api": ("FlextQuality",),
        ".base": ("FlextQualityServiceBase",),
        ".cli": (
            "FlextQualityCli",
            "main",
        ),
        ".constants": (
            "FlextQualityConstants",
            "c",
        ),
        ".docs": ("docs",),
        ".hooks": ("hooks",),
        ".hooks.base": ("FlextQualityBaseHook",),
        ".hooks.manager": ("FlextQualityHookManager",),
        ".integrations": ("integrations",),
        ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
        ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
        ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
        ".integrations.mcp_client": ("FlextQualityMcpClient",),
        ".mcp": ("mcp",),
        ".mcp.resources": ("FlextQualityMcpResources",),
        ".mcp.server": ("FlextQualityMcpServer",),
        ".mcp.tools": ("FlextQualityMcpTools",),
        ".models": (
            "FlextQualityModels",
            "m",
        ),
        ".protocols": (
            "FlextQualityProtocols",
            "p",
        ),
        ".rules.engine": ("FlextQualityRulesEngine",),
        ".rules.loader": ("FlextQualityRulesLoader",),
        ".rules.validators": ("FlextQualityValidators",),
        ".settings": ("FlextQualitySettings",),
        ".typings": ("FlextQualityTypes",),
        ".utilities": ("FlextQualityUtilities",),
        "flext_core._root_typing_parts": (
            "d",
            "e",
            "h",
        ),
    },
)

__all__: list[str] = ["FLEXT_QUALITY_LAZY_IMPORTS_PART_01"]
