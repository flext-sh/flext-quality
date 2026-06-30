# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_QUALITY_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".api": ("FlextQuality",),
        ".base": ("FlextQualityServiceBase",),
        ".cli": ("FlextQualityCli",),
        ".constants": ("FlextQualityConstants",),
        ".docs.core.config_manager": (
            "FlextQualityAuditRules",
            "FlextQualityConfigManager",
            "FlextQualityConfigTypes",
            "FlextQualityStyleGuide",
        ),
        ".docs.dashboard": ("FlextQualityDocumentationDashboard",),
        ".docs.notifications": ("FlextQualityDocumentationNotifier",),
        ".docs.scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
        ".docs.scripts.audit": ("FlextQualityDocumentationAuditor",),
        ".docs.scripts.optimize": ("FlextQualityDocumentationOptimizer",),
        ".docs.scripts.report": ("FlextQualityDocumentationReporter",),
        ".docs.scripts.validate": (
            "FlextQualityContentValidator",
            "FlextQualityDocumentationValidator",
            "FlextQualityLinkValidator",
        ),
        ".docs.tools.link_checker": ("FlextQualityLinkChecker",),
        ".docs.tools.style_validator": ("FlextQualityStyleValidator",),
        ".hooks.base": ("FlextQualityBaseHook",),
        ".hooks.manager": ("FlextQualityHookManager",),
        ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
        ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
        ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
        ".integrations.mcp_client": ("FlextQualityMcpClient",),
        ".models": ("FlextQualityModels",),
        ".protocols": ("FlextQualityProtocols",),
        ".rules.engine": ("FlextQualityRulesEngine",),
        ".rules.loader": ("FlextQualityRulesLoader",),
        ".settings": ("FlextQualitySettings",),
        ".typings": ("FlextQualityTypes",),
        ".utilities": ("FlextQualityUtilities",),
    },
)

__all__: list[str] = ["FLEXT_QUALITY_LAZY_IMPORTS_PART_01"]
