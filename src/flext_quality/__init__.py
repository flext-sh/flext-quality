# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import flext_quality.api as _flext_quality_api

    api = _flext_quality_api
    import flext_quality.constants as _flext_quality_constants
    from flext_quality.api import FlextQuality

    constants = _flext_quality_constants
    import flext_quality.docs as _flext_quality_docs
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )

    docs = _flext_quality_docs
    import flext_quality.docs.core as _flext_quality_docs_core
    from flext_quality.docs import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationDashboard,
        FlextQualityDocumentationNotifier,
        FlextQualityScheduledMaintenance,
        dashboard,
        logger,
        notifications,
        scheduled_maintenance,
    )

    core = _flext_quality_docs_core
    import flext_quality.docs.scripts as _flext_quality_docs_scripts
    from flext_quality.docs.core import (
        FlextQualityAuditRules,
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
        FlextQualityConfigManager,
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
        base_classes,
        config_manager,
        file_discovery,
    )

    scripts = _flext_quality_docs_scripts
    import flext_quality.docs.tools as _flext_quality_docs_tools
    from flext_quality.docs.scripts import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
        audit,
        optimize,
        report,
        validate,
    )

    tools = _flext_quality_docs_tools
    import flext_quality.hooks as _flext_quality_hooks
    from flext_quality.docs.tools import (
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_file_content,
        analyze_files_content,
        content_analyzer,
        link_checker,
        style_validator,
        validate_file_style,
        validate_files_style,
        validate_links_sync,
    )

    hooks = _flext_quality_hooks
    import flext_quality.integrations as _flext_quality_integrations
    from flext_quality.hooks import (
        FlextQualityBaseHook,
        FlextQualityHookManager,
        base,
        manager,
    )

    integrations = _flext_quality_integrations
    import flext_quality.models as _flext_quality_models
    from flext_quality.integrations import (
        FlextQualityClaudeContextClient,
        FlextQualityClaudeMemClient,
        FlextQualityCodeExecutionBridge,
        FlextQualityMcpClient,
        McpToolCall,
        build_mcp_health_result,
        claude_context,
        claude_mem,
        code_execution,
        mcp_client,
    )
    from flext_quality.mcp import (
        execute_hook,
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
        get_server,
        mcp,
        resources,
        search_code,
        search_memory,
        server,
        validate_rules,
    )

    models = _flext_quality_models
    import flext_quality.protocols as _flext_quality_protocols
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m

    protocols = _flext_quality_protocols
    import flext_quality.rules as _flext_quality_rules
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )

    rules = _flext_quality_rules
    import flext_quality.services as _flext_quality_services
    from flext_quality.rules import (
        FlextQualityRulesEngine,
        FlextQualityRulesLoader,
        FlextQualityValidators,
        engine,
        loader,
        validators,
    )

    services = _flext_quality_services
    import flext_quality.settings as _flext_quality_settings
    from flext_quality.services import FlextQualityCliService, cli, main

    settings = _flext_quality_settings
    import flext_quality.typings as _flext_quality_typings
    from flext_quality.settings import FlextQualitySettings

    typings = _flext_quality_typings
    import flext_quality.utilities as _flext_quality_utilities
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t

    utilities = _flext_quality_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_quality.docs",
        "flext_quality.hooks",
        "flext_quality.integrations",
        "flext_quality.mcp",
        "flext_quality.rules",
        "flext_quality.services",
    ),
    {
        "FlextQuality": "flext_quality.api",
        "FlextQualityConstants": "flext_quality.constants",
        "FlextQualityModels": "flext_quality.models",
        "FlextQualityProtocols": "flext_quality.protocols",
        "FlextQualitySettings": "flext_quality.settings",
        "FlextQualityTypes": "flext_quality.typings",
        "FlextQualityUtilities": "flext_quality.utilities",
        "api": "flext_quality.api",
        "c": ("flext_quality.constants", "FlextQualityConstants"),
        "constants": "flext_quality.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docs": "flext_quality.docs",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "hooks": "flext_quality.hooks",
        "integrations": "flext_quality.integrations",
        "m": ("flext_quality.models", "FlextQualityModels"),
        "models": "flext_quality.models",
        "p": ("flext_quality.protocols", "FlextQualityProtocols"),
        "protocols": "flext_quality.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "rules": "flext_quality.rules",
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_quality.services",
        "settings": "flext_quality.settings",
        "t": ("flext_quality.typings", "FlextQualityTypes"),
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityUtilities"),
        "utilities": "flext_quality.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
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
    "McpToolCall",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
