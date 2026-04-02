# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x

    from flext_core import FlextTypes
    from flext_quality import (
        api,
        constants,
        docs,
        hooks,
        integrations,
        models,
        protocols,
        rules,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_quality.api import FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )
    from flext_quality.docs import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationDashboard,
        FlextQualityDocumentationNotifier,
        FlextQualityScheduledMaintenance,
        core,
        dashboard,
        logger,
        notifications,
        scheduled_maintenance,
        scripts,
        tools,
    )
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
    from flext_quality.docs.scripts import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
        ReportValue,
        audit,
        optimize,
        report,
        validate,
    )
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
    from flext_quality.hooks import (
        FlextQualityBaseHook,
        FlextQualityHookManager,
        base,
        manager,
    )
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
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )
    from flext_quality.rules import (
        FlextQualityRulesEngine,
        FlextQualityRulesLoader,
        FlextQualityValidators,
        engine,
        loader,
        validators,
    )
    from flext_quality.services import FlextQualityCliService, cli, main
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
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
        "d": "flext_cli",
        "docs": "flext_quality.docs",
        "e": "flext_cli",
        "h": "flext_cli",
        "hooks": "flext_quality.hooks",
        "integrations": "flext_quality.integrations",
        "m": ("flext_quality.models", "FlextQualityModels"),
        "models": "flext_quality.models",
        "p": ("flext_quality.protocols", "FlextQualityProtocols"),
        "protocols": "flext_quality.protocols",
        "r": "flext_cli",
        "rules": "flext_quality.rules",
        "s": "flext_cli",
        "services": "flext_quality.services",
        "settings": "flext_quality.settings",
        "t": ("flext_quality.typings", "FlextQualityTypes"),
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityUtilities"),
        "utilities": "flext_quality.utilities",
        "x": "flext_cli",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
