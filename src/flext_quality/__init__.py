# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality.api import FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )
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
        FlextQualityValidationConfig,
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
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
    )
    from flext_quality.docs.tools.content_analyzer import (
        FlextQualityContentAnalyzer,
        analyze_file_content,
        analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker,
        validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator,
        validate_file_style,
        validate_files_style,
    )
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager
    from flext_quality.integrations._health import build_mcp_health_result
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient
    from flext_quality.mcp.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )
    from flext_quality.mcp.server import get_server
    from flext_quality.mcp.tools import (
        execute_hook,
        search_code,
        search_memory,
        validate_rules,
    )
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.services.cli import FlextQualityCliService
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".docs",
        ".hooks",
        ".integrations",
        ".mcp",
        ".rules",
        ".services",
    ),
    {
        "FlextQuality": ".api",
        "FlextQualityConstants": ".constants",
        "FlextQualityModels": ".models",
        "FlextQualityProtocols": ".protocols",
        "FlextQualitySettings": ".settings",
        "FlextQualityTypes": ".typings",
        "FlextQualityUtilities": ".utilities",
        "c": (".constants", "FlextQualityConstants"),
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": (".models", "FlextQualityModels"),
        "p": (".protocols", "FlextQualityProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": (".typings", "FlextQualityTypes"),
        "u": (".utilities", "FlextQualityUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
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

__all__ = [
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
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationFinder",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityFileStatistics",
    "FlextQualityHookManager",
    "FlextQualityLinkChecker",
    "FlextQualityLinkValidator",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityScheduledMaintenance",
    "FlextQualitySettings",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityValidationConfig",
    "FlextQualityValidators",
    "analyze_file_content",
    "analyze_files_content",
    "build_mcp_health_result",
    "c",
    "d",
    "e",
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "h",
    "m",
    "p",
    "r",
    "s",
    "search_code",
    "search_memory",
    "t",
    "u",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "validate_rules",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
