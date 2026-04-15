# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_web import d, e, h, r, s, t, u, x

    from flext_quality.api import FlextQuality, quality
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.docs.core.base_classes import (
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationSettings,
    )
    from flext_quality.docs.core.file_discovery import (
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
    )
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.tools.content_analyzer import FlextQualityContentAnalyzer
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.services.cli import FlextQualityCliService
    from flext_quality.settings import FlextQualitySettings
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".docs",
        ".hooks",
        ".integrations",
        ".mcp",
        ".rules",
        ".services",
    ),
    build_lazy_import_map(
        {
            ".api": (
                "FlextQuality",
                "quality",
            ),
            ".constants": (
                "FlextQualityConstants",
                "c",
            ),
            ".models": (
                "FlextQualityModels",
                "m",
            ),
            ".protocols": (
                "FlextQualityProtocols",
                "p",
            ),
            ".settings": ("FlextQualitySettings",),
            "flext_web": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "t",
                "u",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextQuality",
    "FlextQualityAuditRules",
    "FlextQualityBaseAnalyzer",
    "FlextQualityBaseAuditor",
    "FlextQualityBaseHook",
    "FlextQualityBaseReporter",
    "FlextQualityBaseValidator",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCliService",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfigManager",
    "FlextQualityConstants",
    "FlextQualityContentAnalyzer",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationFinder",
    "FlextQualityDocumentationNotifier",
    "FlextQualityFileStatistics",
    "FlextQualityHookManager",
    "FlextQualityLinkChecker",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityScheduledMaintenance",
    "FlextQualitySettings",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityValidationSettings",
    "FlextQualityValidators",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "quality",
    "r",
    "s",
    "t",
    "u",
    "x",
]
