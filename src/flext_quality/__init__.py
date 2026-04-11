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
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_quality.api import FlextQuality
    from flext_quality.audit import FlextQualityDocumentationAuditor
    from flext_quality.base import FlextQualityBaseHook
    from flext_quality.base_classes import (
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
    )
    from flext_quality.claude_context import FlextQualityClaudeContextClient
    from flext_quality.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.cli import FlextQualityCliService
    from flext_quality.code_execution import FlextQualityCodeExecutionBridge
    from flext_quality.config_manager import (
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationSettings,
    )
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.content_analyzer import (
        FlextQualityContentAnalyzer,
        analyze_file_content,
        analyze_files_content,
    )
    from flext_quality.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.engine import FlextQualityRulesEngine
    from flext_quality.file_discovery import (
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
    )
    from flext_quality.link_checker import FlextQualityLinkChecker, validate_links_sync
    from flext_quality.loader import FlextQualityRulesLoader
    from flext_quality.manager import FlextQualityHookManager
    from flext_quality.mcp_client import FlextQualityMcpClient
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.notifications import FlextQualityDocumentationNotifier
    from flext_quality.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.report import FlextQualityDocumentationReporter
    from flext_quality.resources import (
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
    )
    from flext_quality.scheduled_maintenance import FlextQualityScheduledMaintenance
    from flext_quality.server import get_server
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.style_validator import (
        FlextQualityStyleValidator,
        validate_file_style,
        validate_files_style,
    )
    from flext_quality.tools import (
        execute_hook,
        search_code,
        search_memory,
        validate_rules,
    )
    from flext_quality.typings import FlextQualityTypes, t
    from flext_quality.utilities import FlextQualityUtilities, u
    from flext_quality.validate import (
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
    )
    from flext_quality.validators import FlextQualityValidators
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
            ".api": ("FlextQuality",),
            ".audit": ("FlextQualityDocumentationAuditor",),
            ".base": ("FlextQualityBaseHook",),
            ".base_classes": (
                "FlextQualityBaseAnalyzer",
                "FlextQualityBaseAuditor",
                "FlextQualityBaseReporter",
                "FlextQualityBaseValidator",
            ),
            ".claude_context": ("FlextQualityClaudeContextClient",),
            ".claude_mem": ("FlextQualityClaudeMemClient",),
            ".cli": ("FlextQualityCliService",),
            ".code_execution": ("FlextQualityCodeExecutionBridge",),
            ".config_manager": (
                "FlextQualityAuditRules",
                "FlextQualityConfigManager",
                "FlextQualityStyleGuide",
                "FlextQualityValidationSettings",
            ),
            ".constants": (
                "FlextQualityConstants",
                "c",
            ),
            ".content_analyzer": (
                "FlextQualityContentAnalyzer",
                "analyze_file_content",
                "analyze_files_content",
            ),
            ".dashboard": ("FlextQualityDocumentationDashboard",),
            ".engine": ("FlextQualityRulesEngine",),
            ".file_discovery": (
                "FlextQualityDocumentationFinder",
                "FlextQualityFileStatistics",
            ),
            ".link_checker": (
                "FlextQualityLinkChecker",
                "validate_links_sync",
            ),
            ".loader": ("FlextQualityRulesLoader",),
            ".manager": ("FlextQualityHookManager",),
            ".mcp_client": ("FlextQualityMcpClient",),
            ".models": (
                "FlextQualityModels",
                "m",
            ),
            ".notifications": ("FlextQualityDocumentationNotifier",),
            ".optimize": ("FlextQualityDocumentationOptimizer",),
            ".protocols": (
                "FlextQualityProtocols",
                "p",
            ),
            ".report": ("FlextQualityDocumentationReporter",),
            ".resources": (
                "get_hooks_config",
                "get_integrations_status",
                "get_rules_config",
            ),
            ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".server": ("get_server",),
            ".settings": ("FlextQualitySettings",),
            ".style_validator": (
                "FlextQualityStyleValidator",
                "validate_file_style",
                "validate_files_style",
            ),
            ".tools": (
                "execute_hook",
                "search_code",
                "search_memory",
                "validate_rules",
            ),
            ".typings": (
                "FlextQualityTypes",
                "t",
            ),
            ".utilities": (
                "FlextQualityUtilities",
                "u",
            ),
            ".validate": (
                "FlextQualityContentValidator",
                "FlextQualityLinkValidator",
            ),
            ".validators": ("FlextQualityValidators",),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
            "flext_core.service": ("s",),
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
    "FlextQualityValidationSettings",
    "FlextQualityValidators",
    "analyze_file_content",
    "analyze_files_content",
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
