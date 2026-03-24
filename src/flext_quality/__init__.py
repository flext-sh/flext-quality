# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x
    from flext_core import FlextTypes

    from flext_quality import docs, hooks, integrations, rules, services
    from flext_quality.api import FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )
    from flext_quality.docs import core, scripts, tools
    from flext_quality.docs.core.base_classes import (
        Config,
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
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier,
        NotifierResults,
    )
    from flext_quality.docs.scheduled_maintenance import (
        ErrorHandlingConfig,
        FlextQualityScheduledMaintenance,
        LoggingConfig,
        MaintenanceConfig,
        ScheduleEntry,
        ScheduleResults,
        ScheduleTaskConfig,
    )
    from flext_quality.docs.scripts.audit import (
        AccessibilityConfig,
        AuditMetrics,
        AuditorResults,
        AuditRecommendation,
        AuditRulesConfig,
        ContentAnalysisConfig,
        ContentChecksConfig,
        FlextQualityDocumentationAuditor,
        FormattingConfig,
        LinkValidationConfig,
        MarkdownStyleConfig,
        QualityThresholdsConfig,
        SeverityLevelsConfig,
        StyleGuideConfig,
        ValidationConfig,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationOptimizer,
        OptimizerResults,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter,
        ReportValue,
    )
    from flext_quality.docs.scripts.validate import (
        ContentIssue,
        ContentMetrics,
        ContentValidatorResults,
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
        LinkCheckResult,
        LinkRecord,
        LinkValidatorResults,
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
        ExecutionRequest,
        ExecutionResult,
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
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.services.cli import FlextQualityCliService, main
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "AccessibilityConfig": ("flext_quality.docs.scripts.audit", "AccessibilityConfig"),
    "AuditMetrics": ("flext_quality.docs.scripts.audit", "AuditMetrics"),
    "AuditRecommendation": ("flext_quality.docs.scripts.audit", "AuditRecommendation"),
    "AuditRulesConfig": ("flext_quality.docs.scripts.audit", "AuditRulesConfig"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "Config": ("flext_quality.docs.core.base_classes", "Config"),
    "ContentAnalysisConfig": (
        "flext_quality.docs.scripts.audit",
        "ContentAnalysisConfig",
    ),
    "ContentChecksConfig": ("flext_quality.docs.scripts.audit", "ContentChecksConfig"),
    "ContentIssue": ("flext_quality.docs.scripts.validate", "ContentIssue"),
    "ContentMetrics": ("flext_quality.docs.scripts.validate", "ContentMetrics"),
    "ContentValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "ContentValidatorResults",
    ),
    "ErrorHandlingConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ErrorHandlingConfig",
    ),
    "ExecutionRequest": (
        "flext_quality.integrations.code_execution",
        "ExecutionRequest",
    ),
    "ExecutionResult": ("flext_quality.integrations.code_execution", "ExecutionResult"),
    "FlextQuality": ("flext_quality.api", "FlextQuality"),
    "FlextQualityAuditRules": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityAuditRules",
    ),
    "FlextQualityBaseAnalyzer": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAnalyzer",
    ),
    "FlextQualityBaseAuditor": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAuditor",
    ),
    "FlextQualityBaseHook": ("flext_quality.hooks.base", "FlextQualityBaseHook"),
    "FlextQualityBaseReporter": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ),
    "FlextQualityBaseValidator": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ),
    "FlextQualityClaudeContextClient": (
        "flext_quality.integrations.claude_context",
        "FlextQualityClaudeContextClient",
    ),
    "FlextQualityClaudeMemClient": (
        "flext_quality.integrations.claude_mem",
        "FlextQualityClaudeMemClient",
    ),
    "FlextQualityCliService": ("flext_quality.services.cli", "FlextQualityCliService"),
    "FlextQualityCodeExecutionBridge": (
        "flext_quality.integrations.code_execution",
        "FlextQualityCodeExecutionBridge",
    ),
    "FlextQualityConfigManager": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ),
    "FlextQualityConstants": ("flext_quality.constants", "FlextQualityConstants"),
    "FlextQualityContentAnalyzer": (
        "flext_quality.docs.tools.content_analyzer",
        "FlextQualityContentAnalyzer",
    ),
    "FlextQualityContentValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityContentValidator",
    ),
    "FlextQualityDocumentationAuditor": (
        "flext_quality.docs.scripts.audit",
        "FlextQualityDocumentationAuditor",
    ),
    "FlextQualityDocumentationDashboard": (
        "flext_quality.docs.dashboard",
        "FlextQualityDocumentationDashboard",
    ),
    "FlextQualityDocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityDocumentationFinder",
    ),
    "FlextQualityDocumentationNotifier": (
        "flext_quality.docs.notifications",
        "FlextQualityDocumentationNotifier",
    ),
    "FlextQualityDocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "FlextQualityDocumentationOptimizer",
    ),
    "FlextQualityDocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "FlextQualityDocumentationReporter",
    ),
    "FlextQualityFileStatistics": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityFileStatistics",
    ),
    "FlextQualityHookManager": (
        "flext_quality.hooks.manager",
        "FlextQualityHookManager",
    ),
    "FlextQualityLinkChecker": (
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ),
    "FlextQualityLinkValidator": (
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ),
    "FlextQualityMcpClient": (
        "flext_quality.integrations.mcp_client",
        "FlextQualityMcpClient",
    ),
    "FlextQualityModels": ("flext_quality.models", "FlextQualityModels"),
    "FlextQualityProtocols": ("flext_quality.protocols", "FlextQualityProtocols"),
    "FlextQualityRulesEngine": (
        "flext_quality.rules.engine",
        "FlextQualityRulesEngine",
    ),
    "FlextQualityRulesLoader": (
        "flext_quality.rules.loader",
        "FlextQualityRulesLoader",
    ),
    "FlextQualityScheduledMaintenance": (
        "flext_quality.docs.scheduled_maintenance",
        "FlextQualityScheduledMaintenance",
    ),
    "FlextQualitySettings": ("flext_quality.settings", "FlextQualitySettings"),
    "FlextQualityStyleGuide": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ),
    "FlextQualityStyleValidator": (
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
    ),
    "FlextQualityTypes": ("flext_quality.typings", "FlextQualityTypes"),
    "FlextQualityUtilities": ("flext_quality.utilities", "FlextQualityUtilities"),
    "FlextQualityValidationConfig": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ),
    "FlextQualityValidators": (
        "flext_quality.rules.validators",
        "FlextQualityValidators",
    ),
    "FormattingConfig": ("flext_quality.docs.scripts.audit", "FormattingConfig"),
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkValidationConfig": (
        "flext_quality.docs.scripts.audit",
        "LinkValidationConfig",
    ),
    "LinkValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "LinkValidatorResults",
    ),
    "LoggingConfig": ("flext_quality.docs.scheduled_maintenance", "LoggingConfig"),
    "MAX_BROKEN_LINKS_TO_SHOW": (
        "flext_quality.docs.notifications",
        "MAX_BROKEN_LINKS_TO_SHOW",
    ),
    "MIN_HEADINGS_FOR_TOC": (
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ),
    "MaintenanceConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "MaintenanceConfig",
    ),
    "MarkdownStyleConfig": ("flext_quality.docs.scripts.audit", "MarkdownStyleConfig"),
    "McpToolCall": ("flext_quality.integrations.mcp_client", "McpToolCall"),
    "McpToolResult": ("flext_quality.integrations.mcp_client", "McpToolResult"),
    "NotifierResults": ("flext_quality.docs.notifications", "NotifierResults"),
    "OptimizerResults": ("flext_quality.docs.scripts.optimize", "OptimizerResults"),
    "QualityThresholdsConfig": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsConfig",
    ),
    "ReportValue": ("flext_quality.docs.scripts.report", "ReportValue"),
    "ScheduleEntry": ("flext_quality.docs.scheduled_maintenance", "ScheduleEntry"),
    "ScheduleResults": ("flext_quality.docs.scheduled_maintenance", "ScheduleResults"),
    "ScheduleTaskConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduleTaskConfig",
    ),
    "SeverityLevelsConfig": (
        "flext_quality.docs.scripts.audit",
        "SeverityLevelsConfig",
    ),
    "StyleGuideConfig": ("flext_quality.docs.scripts.audit", "StyleGuideConfig"),
    "ValidationConfig": ("flext_quality.docs.scripts.audit", "ValidationConfig"),
    "analyze_file_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ),
    "analyze_files_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ),
    "build_mcp_health_result": (
        "flext_quality.integrations._health",
        "build_mcp_health_result",
    ),
    "c": ("flext_quality.constants", "FlextQualityConstants"),
    "core": ("flext_quality.docs.core", ""),
    "d": ("flext_cli", "d"),
    "docs": ("flext_quality.docs", ""),
    "e": ("flext_cli", "e"),
    "execute_hook": ("flext_quality.mcp.tools", "execute_hook"),
    "get_hooks_config": ("flext_quality.mcp.resources", "get_hooks_config"),
    "get_integrations_status": (
        "flext_quality.mcp.resources",
        "get_integrations_status",
    ),
    "get_rules_config": ("flext_quality.mcp.resources", "get_rules_config"),
    "get_server": ("flext_quality.mcp.server", "get_server"),
    "h": ("flext_cli", "h"),
    "hooks": ("flext_quality.hooks", ""),
    "integrations": ("flext_quality.integrations", ""),
    "m": ("flext_quality.models", "FlextQualityModels"),
    "main": ("flext_quality.services.cli", "main"),
    "mcp": ("flext_quality.mcp.server", "mcp"),
    "p": ("flext_quality.protocols", "FlextQualityProtocols"),
    "r": ("flext_cli", "r"),
    "rules": ("flext_quality.rules", ""),
    "s": ("flext_cli", "s"),
    "scripts": ("flext_quality.docs.scripts", ""),
    "search_code": ("flext_quality.mcp.tools", "search_code"),
    "search_memory": ("flext_quality.mcp.tools", "search_memory"),
    "services": ("flext_quality.services", ""),
    "t": ("flext_quality.typings", "FlextQualityTypes"),
    "tools": ("flext_quality.docs.tools", ""),
    "u": ("flext_quality.utilities", "FlextQualityUtilities"),
    "validate_file_style": (
        "flext_quality.docs.tools.style_validator",
        "validate_file_style",
    ),
    "validate_files_style": (
        "flext_quality.docs.tools.style_validator",
        "validate_files_style",
    ),
    "validate_links_sync": (
        "flext_quality.docs.tools.link_checker",
        "validate_links_sync",
    ),
    "validate_rules": ("flext_quality.mcp.tools", "validate_rules"),
    "x": ("flext_cli", "x"),
}

__all__ = [
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
    "AccessibilityConfig",
    "AuditMetrics",
    "AuditRecommendation",
    "AuditRulesConfig",
    "AuditorResults",
    "Config",
    "ContentAnalysisConfig",
    "ContentChecksConfig",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidatorResults",
    "ErrorHandlingConfig",
    "ExecutionRequest",
    "ExecutionResult",
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
    "FormattingConfig",
    "LinkCheckResult",
    "LinkRecord",
    "LinkValidationConfig",
    "LinkValidatorResults",
    "LoggingConfig",
    "MaintenanceConfig",
    "MarkdownStyleConfig",
    "McpToolCall",
    "McpToolResult",
    "NotifierResults",
    "OptimizerResults",
    "QualityThresholdsConfig",
    "ReportValue",
    "ScheduleEntry",
    "ScheduleResults",
    "ScheduleTaskConfig",
    "SeverityLevelsConfig",
    "StyleGuideConfig",
    "ValidationConfig",
    "analyze_file_content",
    "analyze_files_content",
    "build_mcp_health_result",
    "c",
    "core",
    "d",
    "docs",
    "e",
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "h",
    "hooks",
    "integrations",
    "m",
    "main",
    "mcp",
    "p",
    "r",
    "rules",
    "s",
    "scripts",
    "search_code",
    "search_memory",
    "services",
    "t",
    "tools",
    "u",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "validate_rules",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
