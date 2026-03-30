# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality import (
        api as api,
        constants as constants,
        docs as docs,
        hooks as hooks,
        integrations as integrations,
        models as models,
        protocols as protocols,
        rules as rules,
        services as services,
        settings as settings,
        typings as typings,
        utilities as utilities,
    )
    from flext_quality.api import FlextQuality as FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants as FlextQualityConstants,
        FlextQualityConstants as c,
    )
    from flext_quality.docs import (
        core as core,
        dashboard as dashboard,
        notifications as notifications,
        scheduled_maintenance as scheduled_maintenance,
        scripts as scripts,
        tools as tools,
    )
    from flext_quality.docs.core import (
        base_classes as base_classes,
        config_manager as config_manager,
        file_discovery as file_discovery,
    )
    from flext_quality.docs.core.base_classes import (
        FlextQualityBaseAnalyzer as FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor as FlextQualityBaseAuditor,
        FlextQualityBaseReporter as FlextQualityBaseReporter,
        FlextQualityBaseValidator as FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules as FlextQualityAuditRules,
        FlextQualityConfigManager as FlextQualityConfigManager,
        FlextQualityStyleGuide as FlextQualityStyleGuide,
        FlextQualityValidationConfig as FlextQualityValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        FlextQualityDocumentationFinder as FlextQualityDocumentationFinder,
        FlextQualityFileStatistics as FlextQualityFileStatistics,
    )
    from flext_quality.docs.dashboard import (
        FlextQualityDocumentationDashboard as FlextQualityDocumentationDashboard,
    )
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW as MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier as FlextQualityDocumentationNotifier,
    )
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance as FlextQualityScheduledMaintenance,
        logger as logger,
    )
    from flext_quality.docs.scripts import (
        audit as audit,
        optimize as optimize,
        report as report,
        validate as validate,
    )
    from flext_quality.docs.scripts.audit import (
        FlextQualityDocumentationAuditor as FlextQualityDocumentationAuditor,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC as MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer as FlextQualityDocumentationOptimizer,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter as FlextQualityDocumentationReporter,
        ReportValue as ReportValue,
    )
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator as FlextQualityContentValidator,
        FlextQualityLinkValidator as FlextQualityLinkValidator,
    )
    from flext_quality.docs.tools import (
        content_analyzer as content_analyzer,
        link_checker as link_checker,
        style_validator as style_validator,
    )
    from flext_quality.docs.tools.content_analyzer import (
        FlextQualityContentAnalyzer as FlextQualityContentAnalyzer,
        analyze_file_content as analyze_file_content,
        analyze_files_content as analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker as FlextQualityLinkChecker,
        validate_links_sync as validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator as FlextQualityStyleValidator,
        validate_file_style as validate_file_style,
        validate_files_style as validate_files_style,
    )
    from flext_quality.hooks import base as base, manager as manager
    from flext_quality.hooks.base import FlextQualityBaseHook as FlextQualityBaseHook
    from flext_quality.hooks.manager import (
        FlextQualityHookManager as FlextQualityHookManager,
    )
    from flext_quality.integrations import (
        claude_context as claude_context,
        claude_mem as claude_mem,
        code_execution as code_execution,
        mcp_client as mcp_client,
    )
    from flext_quality.integrations._health import (
        build_mcp_health_result as build_mcp_health_result,
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
    from flext_quality.mcp import resources as resources, server as server
    from flext_quality.mcp.resources import (
        get_hooks_config as get_hooks_config,
        get_integrations_status as get_integrations_status,
        get_rules_config as get_rules_config,
    )
    from flext_quality.mcp.server import get_server as get_server, mcp as mcp
    from flext_quality.mcp.tools import (
        execute_hook as execute_hook,
        search_code as search_code,
        search_memory as search_memory,
        validate_rules as validate_rules,
    )
    from flext_quality.models import (
        FlextQualityModels as FlextQualityModels,
        FlextQualityModels as m,
    )
    from flext_quality.protocols import (
        FlextQualityProtocols as FlextQualityProtocols,
        FlextQualityProtocols as p,
    )
    from flext_quality.rules import (
        engine as engine,
        loader as loader,
        validators as validators,
    )
    from flext_quality.rules.engine import (
        FlextQualityRulesEngine as FlextQualityRulesEngine,
    )
    from flext_quality.rules.loader import (
        FlextQualityRulesLoader as FlextQualityRulesLoader,
    )
    from flext_quality.rules.validators import (
        FlextQualityValidators as FlextQualityValidators,
    )
    from flext_quality.services import cli as cli
    from flext_quality.services.cli import (
        FlextQualityCliService as FlextQualityCliService,
        main as main,
    )
    from flext_quality.settings import FlextQualitySettings as FlextQualitySettings
    from flext_quality.typings import (
        FlextQualityTypes as FlextQualityTypes,
        FlextQualityTypes as t,
    )
    from flext_quality.utilities import (
        FlextQualityUtilities as FlextQualityUtilities,
        FlextQualityUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQuality": ["flext_quality.api", "FlextQuality"],
    "FlextQualityAuditRules": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityAuditRules",
    ],
    "FlextQualityBaseAnalyzer": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAnalyzer",
    ],
    "FlextQualityBaseAuditor": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAuditor",
    ],
    "FlextQualityBaseHook": ["flext_quality.hooks.base", "FlextQualityBaseHook"],
    "FlextQualityBaseReporter": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ],
    "FlextQualityBaseValidator": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ],
    "FlextQualityClaudeContextClient": [
        "flext_quality.integrations.claude_context",
        "FlextQualityClaudeContextClient",
    ],
    "FlextQualityClaudeMemClient": [
        "flext_quality.integrations.claude_mem",
        "FlextQualityClaudeMemClient",
    ],
    "FlextQualityCliService": ["flext_quality.services.cli", "FlextQualityCliService"],
    "FlextQualityCodeExecutionBridge": [
        "flext_quality.integrations.code_execution",
        "FlextQualityCodeExecutionBridge",
    ],
    "FlextQualityConfigManager": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ],
    "FlextQualityConstants": ["flext_quality.constants", "FlextQualityConstants"],
    "FlextQualityContentAnalyzer": [
        "flext_quality.docs.tools.content_analyzer",
        "FlextQualityContentAnalyzer",
    ],
    "FlextQualityContentValidator": [
        "flext_quality.docs.scripts.validate",
        "FlextQualityContentValidator",
    ],
    "FlextQualityDocumentationAuditor": [
        "flext_quality.docs.scripts.audit",
        "FlextQualityDocumentationAuditor",
    ],
    "FlextQualityDocumentationDashboard": [
        "flext_quality.docs.dashboard",
        "FlextQualityDocumentationDashboard",
    ],
    "FlextQualityDocumentationFinder": [
        "flext_quality.docs.core.file_discovery",
        "FlextQualityDocumentationFinder",
    ],
    "FlextQualityDocumentationNotifier": [
        "flext_quality.docs.notifications",
        "FlextQualityDocumentationNotifier",
    ],
    "FlextQualityDocumentationOptimizer": [
        "flext_quality.docs.scripts.optimize",
        "FlextQualityDocumentationOptimizer",
    ],
    "FlextQualityDocumentationReporter": [
        "flext_quality.docs.scripts.report",
        "FlextQualityDocumentationReporter",
    ],
    "FlextQualityFileStatistics": [
        "flext_quality.docs.core.file_discovery",
        "FlextQualityFileStatistics",
    ],
    "FlextQualityHookManager": [
        "flext_quality.hooks.manager",
        "FlextQualityHookManager",
    ],
    "FlextQualityLinkChecker": [
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ],
    "FlextQualityLinkValidator": [
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ],
    "FlextQualityMcpClient": [
        "flext_quality.integrations.mcp_client",
        "FlextQualityMcpClient",
    ],
    "FlextQualityModels": ["flext_quality.models", "FlextQualityModels"],
    "FlextQualityProtocols": ["flext_quality.protocols", "FlextQualityProtocols"],
    "FlextQualityRulesEngine": [
        "flext_quality.rules.engine",
        "FlextQualityRulesEngine",
    ],
    "FlextQualityRulesLoader": [
        "flext_quality.rules.loader",
        "FlextQualityRulesLoader",
    ],
    "FlextQualityScheduledMaintenance": [
        "flext_quality.docs.scheduled_maintenance",
        "FlextQualityScheduledMaintenance",
    ],
    "FlextQualitySettings": ["flext_quality.settings", "FlextQualitySettings"],
    "FlextQualityStyleGuide": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ],
    "FlextQualityStyleValidator": [
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
    ],
    "FlextQualityTypes": ["flext_quality.typings", "FlextQualityTypes"],
    "FlextQualityUtilities": ["flext_quality.utilities", "FlextQualityUtilities"],
    "FlextQualityValidationConfig": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ],
    "FlextQualityValidators": [
        "flext_quality.rules.validators",
        "FlextQualityValidators",
    ],
    "MAX_BROKEN_LINKS_TO_SHOW": [
        "flext_quality.docs.notifications",
        "MAX_BROKEN_LINKS_TO_SHOW",
    ],
    "MIN_HEADINGS_FOR_TOC": [
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ],
    "McpToolCall": ["flext_quality.integrations.claude_mem", "McpToolCall"],
    "ReportValue": ["flext_quality.docs.scripts.report", "ReportValue"],
    "analyze_file_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ],
    "analyze_files_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ],
    "api": ["flext_quality.api", ""],
    "audit": ["flext_quality.docs.scripts.audit", ""],
    "base": ["flext_quality.hooks.base", ""],
    "base_classes": ["flext_quality.docs.core.base_classes", ""],
    "build_mcp_health_result": [
        "flext_quality.integrations._health",
        "build_mcp_health_result",
    ],
    "c": ["flext_quality.constants", "FlextQualityConstants"],
    "claude_context": ["flext_quality.integrations.claude_context", ""],
    "claude_mem": ["flext_quality.integrations.claude_mem", ""],
    "cli": ["flext_quality.services.cli", ""],
    "code_execution": ["flext_quality.integrations.code_execution", ""],
    "config_manager": ["flext_quality.docs.core.config_manager", ""],
    "constants": ["flext_quality.constants", ""],
    "content_analyzer": ["flext_quality.docs.tools.content_analyzer", ""],
    "core": ["flext_quality.docs.core", ""],
    "d": ["flext_cli", "d"],
    "dashboard": ["flext_quality.docs.dashboard", ""],
    "docs": ["flext_quality.docs", ""],
    "e": ["flext_cli", "e"],
    "engine": ["flext_quality.rules.engine", ""],
    "execute_hook": ["flext_quality.mcp.tools", "execute_hook"],
    "file_discovery": ["flext_quality.docs.core.file_discovery", ""],
    "get_hooks_config": ["flext_quality.mcp.resources", "get_hooks_config"],
    "get_integrations_status": [
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ],
    "get_rules_config": ["flext_quality.mcp.resources", "get_rules_config"],
    "get_server": ["flext_quality.mcp.server", "get_server"],
    "h": ["flext_cli", "h"],
    "hooks": ["flext_quality.hooks", ""],
    "integrations": ["flext_quality.integrations", ""],
    "link_checker": ["flext_quality.docs.tools.link_checker", ""],
    "loader": ["flext_quality.rules.loader", ""],
    "logger": ["flext_quality.docs.scheduled_maintenance", "logger"],
    "m": ["flext_quality.models", "FlextQualityModels"],
    "main": ["flext_quality.services.cli", "main"],
    "manager": ["flext_quality.hooks.manager", ""],
    "mcp": ["flext_quality.mcp.server", "mcp"],
    "mcp_client": ["flext_quality.integrations.mcp_client", ""],
    "models": ["flext_quality.models", ""],
    "notifications": ["flext_quality.docs.notifications", ""],
    "optimize": ["flext_quality.docs.scripts.optimize", ""],
    "p": ["flext_quality.protocols", "FlextQualityProtocols"],
    "protocols": ["flext_quality.protocols", ""],
    "r": ["flext_cli", "r"],
    "report": ["flext_quality.docs.scripts.report", ""],
    "resources": ["flext_quality.mcp.resources", ""],
    "rules": ["flext_quality.rules", ""],
    "s": ["flext_cli", "s"],
    "scheduled_maintenance": ["flext_quality.docs.scheduled_maintenance", ""],
    "scripts": ["flext_quality.docs.scripts", ""],
    "search_code": ["flext_quality.mcp.tools", "search_code"],
    "search_memory": ["flext_quality.mcp.tools", "search_memory"],
    "server": ["flext_quality.mcp.server", ""],
    "services": ["flext_quality.services", ""],
    "settings": ["flext_quality.settings", ""],
    "style_validator": ["flext_quality.docs.tools.style_validator", ""],
    "t": ["flext_quality.typings", "FlextQualityTypes"],
    "tools": ["flext_quality.docs.tools", ""],
    "typings": ["flext_quality.typings", ""],
    "u": ["flext_quality.utilities", "FlextQualityUtilities"],
    "utilities": ["flext_quality.utilities", ""],
    "validate": ["flext_quality.docs.scripts.validate", ""],
    "validate_file_style": [
        "flext_quality.docs.tools.style_validator",
        "validate_file_style",
    ],
    "validate_files_style": [
        "flext_quality.docs.tools.style_validator",
        "validate_files_style",
    ],
    "validate_links_sync": [
        "flext_quality.docs.tools.link_checker",
        "validate_links_sync",
    ],
    "validate_rules": ["flext_quality.mcp.tools", "validate_rules"],
    "validators": ["flext_quality.rules.validators", ""],
    "x": ["flext_cli", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
    "McpToolCall",
    "ReportValue",
    "analyze_file_content",
    "analyze_files_content",
    "api",
    "audit",
    "base",
    "base_classes",
    "build_mcp_health_result",
    "c",
    "claude_context",
    "claude_mem",
    "cli",
    "code_execution",
    "config_manager",
    "constants",
    "content_analyzer",
    "core",
    "d",
    "dashboard",
    "docs",
    "e",
    "engine",
    "execute_hook",
    "file_discovery",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "h",
    "hooks",
    "integrations",
    "link_checker",
    "loader",
    "logger",
    "m",
    "main",
    "manager",
    "mcp",
    "mcp_client",
    "models",
    "notifications",
    "optimize",
    "p",
    "protocols",
    "r",
    "report",
    "resources",
    "rules",
    "s",
    "scheduled_maintenance",
    "scripts",
    "search_code",
    "search_memory",
    "server",
    "services",
    "settings",
    "style_validator",
    "t",
    "tools",
    "typings",
    "u",
    "utilities",
    "validate",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "validate_rules",
    "validators",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
