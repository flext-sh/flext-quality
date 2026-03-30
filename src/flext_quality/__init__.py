# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import *

    from flext_quality import (
        api,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_quality.api import *
    from flext_quality.constants import *
    from flext_quality.docs import *
    from flext_quality.hooks import *
    from flext_quality.integrations import *
    from flext_quality.mcp import *
    from flext_quality.models import *
    from flext_quality.protocols import *
    from flext_quality.rules import *
    from flext_quality.services import *
    from flext_quality.settings import *
    from flext_quality.typings import *
    from flext_quality.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQuality": "flext_quality.api",
    "FlextQualityAuditRules": "flext_quality.docs.core.config_manager",
    "FlextQualityBaseAnalyzer": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseAuditor": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseHook": "flext_quality.hooks.base",
    "FlextQualityBaseReporter": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseValidator": "flext_quality.docs.core.base_classes",
    "FlextQualityClaudeContextClient": "flext_quality.integrations.claude_context",
    "FlextQualityClaudeMemClient": "flext_quality.integrations.claude_mem",
    "FlextQualityCliService": "flext_quality.services.cli",
    "FlextQualityCodeExecutionBridge": "flext_quality.integrations.code_execution",
    "FlextQualityConfigManager": "flext_quality.docs.core.config_manager",
    "FlextQualityConstants": "flext_quality.constants",
    "FlextQualityContentAnalyzer": "flext_quality.docs.tools.content_analyzer",
    "FlextQualityContentValidator": "flext_quality.docs.scripts.validate",
    "FlextQualityDocumentationAuditor": "flext_quality.docs.scripts.audit",
    "FlextQualityDocumentationDashboard": "flext_quality.docs.dashboard",
    "FlextQualityDocumentationFinder": "flext_quality.docs.core.file_discovery",
    "FlextQualityDocumentationNotifier": "flext_quality.docs.notifications",
    "FlextQualityDocumentationOptimizer": "flext_quality.docs.scripts.optimize",
    "FlextQualityDocumentationReporter": "flext_quality.docs.scripts.report",
    "FlextQualityFileStatistics": "flext_quality.docs.core.file_discovery",
    "FlextQualityHookManager": "flext_quality.hooks.manager",
    "FlextQualityLinkChecker": "flext_quality.docs.tools.link_checker",
    "FlextQualityLinkValidator": "flext_quality.docs.scripts.validate",
    "FlextQualityMcpClient": "flext_quality.integrations.mcp_client",
    "FlextQualityModels": "flext_quality.models",
    "FlextQualityProtocols": "flext_quality.protocols",
    "FlextQualityRulesEngine": "flext_quality.rules.engine",
    "FlextQualityRulesLoader": "flext_quality.rules.loader",
    "FlextQualityScheduledMaintenance": "flext_quality.docs.scheduled_maintenance",
    "FlextQualitySettings": "flext_quality.settings",
    "FlextQualityStyleGuide": "flext_quality.docs.core.config_manager",
    "FlextQualityStyleValidator": "flext_quality.docs.tools.style_validator",
    "FlextQualityTypes": "flext_quality.typings",
    "FlextQualityUtilities": "flext_quality.utilities",
    "FlextQualityValidationConfig": "flext_quality.docs.core.config_manager",
    "FlextQualityValidators": "flext_quality.rules.validators",
    "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.docs.notifications",
    "MIN_HEADINGS_FOR_TOC": "flext_quality.docs.scripts.optimize",
    "McpToolCall": "flext_quality.integrations.claude_mem",
    "ReportValue": "flext_quality.docs.scripts.report",
    "analyze_file_content": "flext_quality.docs.tools.content_analyzer",
    "analyze_files_content": "flext_quality.docs.tools.content_analyzer",
    "api": "flext_quality.api",
    "audit": "flext_quality.docs.scripts.audit",
    "base": "flext_quality.hooks.base",
    "base_classes": "flext_quality.docs.core.base_classes",
    "build_mcp_health_result": "flext_quality.integrations._health",
    "c": ["flext_quality.constants", "FlextQualityConstants"],
    "claude_context": "flext_quality.integrations.claude_context",
    "claude_mem": "flext_quality.integrations.claude_mem",
    "cli": "flext_quality.services.cli",
    "code_execution": "flext_quality.integrations.code_execution",
    "config_manager": "flext_quality.docs.core.config_manager",
    "constants": "flext_quality.constants",
    "content_analyzer": "flext_quality.docs.tools.content_analyzer",
    "core": "flext_quality.docs.core",
    "d": "flext_cli",
    "dashboard": "flext_quality.docs.dashboard",
    "docs": "flext_quality.docs",
    "e": "flext_cli",
    "engine": "flext_quality.rules.engine",
    "execute_hook": "flext_quality.mcp.tools",
    "file_discovery": "flext_quality.docs.core.file_discovery",
    "get_hooks_config": "flext_quality.mcp.resources",
    "get_integrations_status": "flext_quality.mcp.resources",
    "get_rules_config": "flext_quality.mcp.resources",
    "get_server": "flext_quality.mcp.server",
    "h": "flext_cli",
    "hooks": "flext_quality.hooks",
    "integrations": "flext_quality.integrations",
    "link_checker": "flext_quality.docs.tools.link_checker",
    "loader": "flext_quality.rules.loader",
    "logger": "flext_quality.docs.scheduled_maintenance",
    "m": ["flext_quality.models", "FlextQualityModels"],
    "main": "flext_quality.services.cli",
    "manager": "flext_quality.hooks.manager",
    "mcp": "flext_quality.mcp.server",
    "mcp_client": "flext_quality.integrations.mcp_client",
    "models": "flext_quality.models",
    "notifications": "flext_quality.docs.notifications",
    "optimize": "flext_quality.docs.scripts.optimize",
    "p": ["flext_quality.protocols", "FlextQualityProtocols"],
    "protocols": "flext_quality.protocols",
    "r": "flext_cli",
    "report": "flext_quality.docs.scripts.report",
    "resources": "flext_quality.mcp.resources",
    "rules": "flext_quality.rules",
    "s": "flext_cli",
    "scheduled_maintenance": "flext_quality.docs.scheduled_maintenance",
    "scripts": "flext_quality.docs.scripts",
    "search_code": "flext_quality.mcp.tools",
    "search_memory": "flext_quality.mcp.tools",
    "server": "flext_quality.mcp.server",
    "services": "flext_quality.services",
    "settings": "flext_quality.settings",
    "style_validator": "flext_quality.docs.tools.style_validator",
    "t": ["flext_quality.typings", "FlextQualityTypes"],
    "tools": "flext_quality.docs.tools",
    "typings": "flext_quality.typings",
    "u": ["flext_quality.utilities", "FlextQualityUtilities"],
    "utilities": "flext_quality.utilities",
    "validate": "flext_quality.docs.scripts.validate",
    "validate_file_style": "flext_quality.docs.tools.style_validator",
    "validate_files_style": "flext_quality.docs.tools.style_validator",
    "validate_links_sync": "flext_quality.docs.tools.link_checker",
    "validate_rules": "flext_quality.mcp.tools",
    "validators": "flext_quality.rules.validators",
    "x": "flext_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
