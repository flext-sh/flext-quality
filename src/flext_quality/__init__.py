# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x
    from flext_core.typings import FlextTypes

    from flext_quality import docs, hooks, integrations, rules, services
    from flext_quality.api import FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )
    from flext_quality.docs import core, scripts, tools
    from flext_quality.docs.core.base_classes import (
        BaseAnalyzer,
        BaseAuditor,
        BaseReporter,
        BaseValidator,
        Config,
    )
    from flext_quality.docs.core.config_manager import (
        AuditRules,
        ConfigManager,
        StyleGuide,
    )
    from flext_quality.docs.core.file_discovery import (
        DocumentationFinder,
        FileStatistics,
    )
    from flext_quality.docs.dashboard import DocumentationDashboard
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        DocumentationNotifier,
        NotifierResults,
    )
    from flext_quality.docs.scheduled_maintenance import (
        ErrorHandlingConfig,
        LoggingConfig,
        MaintenanceConfig,
        ScheduledMaintenance,
        ScheduleEntry,
        ScheduleResults,
        ScheduleTaskConfig,
    )
    from flext_quality.docs.scripts.audit import (
        AuditorResults,
        AuditRulesConfig,
        ContentAnalysisConfig,
        ContentChecksConfig,
        DocumentationAuditor,
        LinkValidationConfig,
        MarkdownStyleConfig,
        QualityThresholdsConfig,
        SeverityLevelsConfig,
        StyleGuideConfig,
        ValidationConfig,
    )
    from flext_quality.docs.scripts.optimize import (
        MIN_HEADINGS_FOR_TOC,
        DocumentationOptimizer,
        OptimizerResults,
    )
    from flext_quality.docs.scripts.report import (
        AuditSummary,
        DocumentationReporter,
        OptimizationSummary,
        Recommendation,
        ReportData,
        TrendData,
        TrendEntry,
        ValidationSummary,
    )
    from flext_quality.docs.scripts.validate import (
        ContentIssue,
        ContentMetrics,
        ContentValidator,
        ContentValidatorResults,
        LinkCheckResult,
        LinkRecord,
        LinkValidator,
        LinkValidatorResults,
    )
    from flext_quality.docs.tools.content_analyzer import (
        AnalysisDict,
        CompletenessDict,
        ConfigDict,
        ContentAnalyzer,
        IssueDict,
        MetricsDict,
        ReadabilityDict,
        RecommendationDict,
        StructureDict,
        analyze_file_content,
        analyze_files_content,
    )
    from flext_quality.docs.tools.link_checker import (
        LinkChecker,
        LinkConfigDict,
        LinkInfoDict,
        LinkInfoDictRequired,
        LinkResultDict,
        LinkResultDictRequired,
        PerformanceMetricsDict,
        ResultsDict,
        validate_links_sync,
    )
    from flext_quality.docs.tools.style_validator import (
        AccessibilityConfig,
        FileResults,
        FormattingConfig,
        HeadingsConfig,
        MarkdownConfig,
        StyleConfig,
        StyleIssue,
        StyleValidator,
        SummaryMetrics,
        ValidationResults,
        validate_file_style,
        validate_files_style,
    )
    from flext_quality.hooks.base import BaseHookImpl
    from flext_quality.hooks.manager import HookManager
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

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AccessibilityConfig": (
        "flext_quality.docs.tools.style_validator",
        "AccessibilityConfig",
    ),
    "AnalysisDict": ("flext_quality.docs.tools.content_analyzer", "AnalysisDict"),
    "AuditRules": ("flext_quality.docs.core.config_manager", "AuditRules"),
    "AuditRulesConfig": ("flext_quality.docs.scripts.audit", "AuditRulesConfig"),
    "AuditSummary": ("flext_quality.docs.scripts.report", "AuditSummary"),
    "AuditorResults": ("flext_quality.docs.scripts.audit", "AuditorResults"),
    "BaseAnalyzer": ("flext_quality.docs.core.base_classes", "BaseAnalyzer"),
    "BaseAuditor": ("flext_quality.docs.core.base_classes", "BaseAuditor"),
    "BaseHookImpl": ("flext_quality.hooks.base", "BaseHookImpl"),
    "BaseReporter": ("flext_quality.docs.core.base_classes", "BaseReporter"),
    "BaseValidator": ("flext_quality.docs.core.base_classes", "BaseValidator"),
    "CompletenessDict": (
        "flext_quality.docs.tools.content_analyzer",
        "CompletenessDict",
    ),
    "Config": ("flext_quality.docs.core.base_classes", "Config"),
    "ConfigDict": ("flext_quality.docs.tools.content_analyzer", "ConfigDict"),
    "ConfigManager": ("flext_quality.docs.core.config_manager", "ConfigManager"),
    "ContentAnalysisConfig": (
        "flext_quality.docs.scripts.audit",
        "ContentAnalysisConfig",
    ),
    "ContentAnalyzer": ("flext_quality.docs.tools.content_analyzer", "ContentAnalyzer"),
    "ContentChecksConfig": ("flext_quality.docs.scripts.audit", "ContentChecksConfig"),
    "ContentIssue": ("flext_quality.docs.scripts.validate", "ContentIssue"),
    "ContentMetrics": ("flext_quality.docs.scripts.validate", "ContentMetrics"),
    "ContentValidator": ("flext_quality.docs.scripts.validate", "ContentValidator"),
    "ContentValidatorResults": (
        "flext_quality.docs.scripts.validate",
        "ContentValidatorResults",
    ),
    "DocumentationAuditor": (
        "flext_quality.docs.scripts.audit",
        "DocumentationAuditor",
    ),
    "DocumentationDashboard": (
        "flext_quality.docs.dashboard",
        "DocumentationDashboard",
    ),
    "DocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "DocumentationFinder",
    ),
    "DocumentationNotifier": (
        "flext_quality.docs.notifications",
        "DocumentationNotifier",
    ),
    "DocumentationOptimizer": (
        "flext_quality.docs.scripts.optimize",
        "DocumentationOptimizer",
    ),
    "DocumentationReporter": (
        "flext_quality.docs.scripts.report",
        "DocumentationReporter",
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
    "FileResults": ("flext_quality.docs.tools.style_validator", "FileResults"),
    "FileStatistics": ("flext_quality.docs.core.file_discovery", "FileStatistics"),
    "FlextQuality": ("flext_quality.api", "FlextQuality"),
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
    "FlextQualityConstants": ("flext_quality.constants", "FlextQualityConstants"),
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
    "FlextQualitySettings": ("flext_quality.settings", "FlextQualitySettings"),
    "FlextQualityTypes": ("flext_quality.typings", "FlextQualityTypes"),
    "FlextQualityUtilities": ("flext_quality.utilities", "FlextQualityUtilities"),
    "FlextQualityValidators": (
        "flext_quality.rules.validators",
        "FlextQualityValidators",
    ),
    "FormattingConfig": (
        "flext_quality.docs.tools.style_validator",
        "FormattingConfig",
    ),
    "HeadingsConfig": ("flext_quality.docs.tools.style_validator", "HeadingsConfig"),
    "HookManager": ("flext_quality.hooks.manager", "HookManager"),
    "IssueDict": ("flext_quality.docs.tools.content_analyzer", "IssueDict"),
    "LinkCheckResult": ("flext_quality.docs.scripts.validate", "LinkCheckResult"),
    "LinkChecker": ("flext_quality.docs.tools.link_checker", "LinkChecker"),
    "LinkConfigDict": ("flext_quality.docs.tools.link_checker", "LinkConfigDict"),
    "LinkInfoDict": ("flext_quality.docs.tools.link_checker", "LinkInfoDict"),
    "LinkInfoDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkInfoDictRequired",
    ),
    "LinkRecord": ("flext_quality.docs.scripts.validate", "LinkRecord"),
    "LinkResultDict": ("flext_quality.docs.tools.link_checker", "LinkResultDict"),
    "LinkResultDictRequired": (
        "flext_quality.docs.tools.link_checker",
        "LinkResultDictRequired",
    ),
    "LinkValidationConfig": (
        "flext_quality.docs.scripts.audit",
        "LinkValidationConfig",
    ),
    "LinkValidator": ("flext_quality.docs.scripts.validate", "LinkValidator"),
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
    "MarkdownConfig": ("flext_quality.docs.tools.style_validator", "MarkdownConfig"),
    "MarkdownStyleConfig": ("flext_quality.docs.scripts.audit", "MarkdownStyleConfig"),
    "McpToolCall": ("flext_quality.integrations.mcp_client", "McpToolCall"),
    "McpToolResult": ("flext_quality.integrations.mcp_client", "McpToolResult"),
    "MetricsDict": ("flext_quality.docs.tools.content_analyzer", "MetricsDict"),
    "NotifierResults": ("flext_quality.docs.notifications", "NotifierResults"),
    "OptimizationSummary": ("flext_quality.docs.scripts.report", "OptimizationSummary"),
    "OptimizerResults": ("flext_quality.docs.scripts.optimize", "OptimizerResults"),
    "PerformanceMetricsDict": (
        "flext_quality.docs.tools.link_checker",
        "PerformanceMetricsDict",
    ),
    "QualityThresholdsConfig": (
        "flext_quality.docs.scripts.audit",
        "QualityThresholdsConfig",
    ),
    "ReadabilityDict": ("flext_quality.docs.tools.content_analyzer", "ReadabilityDict"),
    "Recommendation": ("flext_quality.docs.scripts.report", "Recommendation"),
    "RecommendationDict": (
        "flext_quality.docs.tools.content_analyzer",
        "RecommendationDict",
    ),
    "ReportData": ("flext_quality.docs.scripts.report", "ReportData"),
    "ResultsDict": ("flext_quality.docs.tools.link_checker", "ResultsDict"),
    "ScheduleEntry": ("flext_quality.docs.scheduled_maintenance", "ScheduleEntry"),
    "ScheduleResults": ("flext_quality.docs.scheduled_maintenance", "ScheduleResults"),
    "ScheduleTaskConfig": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduleTaskConfig",
    ),
    "ScheduledMaintenance": (
        "flext_quality.docs.scheduled_maintenance",
        "ScheduledMaintenance",
    ),
    "SeverityLevelsConfig": (
        "flext_quality.docs.scripts.audit",
        "SeverityLevelsConfig",
    ),
    "StructureDict": ("flext_quality.docs.tools.content_analyzer", "StructureDict"),
    "StyleConfig": ("flext_quality.docs.tools.style_validator", "StyleConfig"),
    "StyleGuide": ("flext_quality.docs.core.config_manager", "StyleGuide"),
    "StyleGuideConfig": ("flext_quality.docs.scripts.audit", "StyleGuideConfig"),
    "StyleIssue": ("flext_quality.docs.tools.style_validator", "StyleIssue"),
    "StyleValidator": ("flext_quality.docs.tools.style_validator", "StyleValidator"),
    "SummaryMetrics": ("flext_quality.docs.tools.style_validator", "SummaryMetrics"),
    "TrendData": ("flext_quality.docs.scripts.report", "TrendData"),
    "TrendEntry": ("flext_quality.docs.scripts.report", "TrendEntry"),
    "ValidationConfig": ("flext_quality.docs.scripts.audit", "ValidationConfig"),
    "ValidationResults": (
        "flext_quality.docs.tools.style_validator",
        "ValidationResults",
    ),
    "ValidationSummary": ("flext_quality.docs.scripts.report", "ValidationSummary"),
    "analyze_file_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ),
    "analyze_files_content": (
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
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
    "AnalysisDict",
    "AuditRules",
    "AuditRulesConfig",
    "AuditSummary",
    "AuditorResults",
    "BaseAnalyzer",
    "BaseAuditor",
    "BaseHookImpl",
    "BaseReporter",
    "BaseValidator",
    "CompletenessDict",
    "Config",
    "ConfigDict",
    "ConfigManager",
    "ContentAnalysisConfig",
    "ContentAnalyzer",
    "ContentChecksConfig",
    "ContentIssue",
    "ContentMetrics",
    "ContentValidator",
    "ContentValidatorResults",
    "DocumentationAuditor",
    "DocumentationDashboard",
    "DocumentationFinder",
    "DocumentationNotifier",
    "DocumentationOptimizer",
    "DocumentationReporter",
    "ErrorHandlingConfig",
    "ExecutionRequest",
    "ExecutionResult",
    "FileResults",
    "FileStatistics",
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
    "FormattingConfig",
    "HeadingsConfig",
    "HookManager",
    "IssueDict",
    "LinkCheckResult",
    "LinkChecker",
    "LinkConfigDict",
    "LinkInfoDict",
    "LinkInfoDictRequired",
    "LinkRecord",
    "LinkResultDict",
    "LinkResultDictRequired",
    "LinkValidationConfig",
    "LinkValidator",
    "LinkValidatorResults",
    "LoggingConfig",
    "MaintenanceConfig",
    "MarkdownConfig",
    "MarkdownStyleConfig",
    "McpToolCall",
    "McpToolResult",
    "MetricsDict",
    "NotifierResults",
    "OptimizationSummary",
    "OptimizerResults",
    "PerformanceMetricsDict",
    "QualityThresholdsConfig",
    "ReadabilityDict",
    "Recommendation",
    "RecommendationDict",
    "ReportData",
    "ResultsDict",
    "ScheduleEntry",
    "ScheduleResults",
    "ScheduleTaskConfig",
    "ScheduledMaintenance",
    "SeverityLevelsConfig",
    "StructureDict",
    "StyleConfig",
    "StyleGuide",
    "StyleGuideConfig",
    "StyleIssue",
    "StyleValidator",
    "SummaryMetrics",
    "TrendData",
    "TrendEntry",
    "ValidationConfig",
    "ValidationResults",
    "ValidationSummary",
    "analyze_file_content",
    "analyze_files_content",
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


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
