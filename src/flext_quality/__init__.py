# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality import (
        api,
        audit,
        base,
        base_classes,
        claude_context,
        claude_mem,
        cli,
        code_execution,
        config_manager,
        constants,
        content_analyzer,
        core,
        dashboard,
        docs,
        file_discovery,
        hooks,
        integrations,
        link_checker,
        loader,
        manager,
        mcp_client,
        models,
        notifications,
        optimize,
        protocols,
        report,
        resources,
        rules,
        scheduled_maintenance,
        scripts,
        services,
        settings,
        style_validator,
        tools,
        typings,
        utilities,
        validate,
        validators,
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
        desc_v,
        err_v,
        file_v,
        issuesChart,
        logger,
        notify_broken_links,
        qualityChart,
        run,
        server,
        type_v,
        url_v,
    )
    from flext_quality.docs.core import (
        FlextQualityAuditRules,
        FlextQualityBaseAuditor,
        FlextQualityFileStatistics,
    )
    from flext_quality.docs.scripts import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
        critical,
        critical_high_issues,
        doc_files,
        high,
        project_root,
        quality_score,
        run_any_check,
        run_any_optimization,
        severity_breakdown,
        should_fail,
    )
    from flext_quality.docs.tools import (
        MIN_ARGS,
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_files_content,
        analyzer,
        checker,
        config_path,
        context,
        error_msg,
        file,
        file_path,
        issue_types,
        issues,
        key,
        paths,
        recommendations,
        results,
        reverse,
        save_report,
        sorted_issues,
        suggestions,
        test_links,
        text,
        type as type_,
        url,
        v_type,
        validate_files_style,
        validator,
    )
    from flext_quality.hooks import FlextQualityBaseHook, FlextQualityHookManager
    from flext_quality.integrations import (
        FlextQualityClaudeContextClient,
        FlextQualityClaudeMemClient,
        FlextQualityCodeExecutionBridge,
        FlextQualityMcpClient,
        McpToolCall,
        build_mcp_health_result,
        health_data,
        mcp_health,
        status,
    )
    from flext_quality.mcp import (
        client,
        command_result,
        engine,
        execute_hook,
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
        get_server,
        mcp,
        params,
        search_code,
        search_limit,
        search_memory,
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
    )
    from flext_quality.services import (
        FlextQualityCliService,
        main,
        message_type,
        result,
        target_path,
    )
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
        "audit": "flext_quality.audit",
        "base": "flext_quality.base",
        "base_classes": "flext_quality.base_classes",
        "c": ("flext_quality.constants", "FlextQualityConstants"),
        "claude_context": "flext_quality.claude_context",
        "claude_mem": "flext_quality.claude_mem",
        "cli": "flext_quality.cli",
        "code_execution": "flext_quality.code_execution",
        "config_manager": "flext_quality.config_manager",
        "constants": "flext_quality.constants",
        "content_analyzer": "flext_quality.content_analyzer",
        "core": "flext_quality.core",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard": "flext_quality.dashboard",
        "docs": "flext_quality.docs",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "file_discovery": "flext_quality.file_discovery",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "hooks": "flext_quality.hooks",
        "integrations": "flext_quality.integrations",
        "link_checker": "flext_quality.link_checker",
        "loader": "flext_quality.loader",
        "m": ("flext_quality.models", "FlextQualityModels"),
        "manager": "flext_quality.manager",
        "mcp_client": "flext_quality.mcp_client",
        "models": "flext_quality.models",
        "notifications": "flext_quality.notifications",
        "optimize": "flext_quality.optimize",
        "p": ("flext_quality.protocols", "FlextQualityProtocols"),
        "protocols": "flext_quality.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "report": "flext_quality.report",
        "resources": "flext_quality.resources",
        "rules": "flext_quality.rules",
        "s": ("flext_core.service", "FlextService"),
        "scheduled_maintenance": "flext_quality.scheduled_maintenance",
        "scripts": "flext_quality.scripts",
        "services": "flext_quality.services",
        "settings": "flext_quality.settings",
        "style_validator": "flext_quality.style_validator",
        "t": ("flext_quality.typings", "FlextQualityTypes"),
        "tools": "flext_quality.tools",
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityUtilities"),
        "utilities": "flext_quality.utilities",
        "validate": "flext_quality.validate",
        "validators": "flext_quality.validators",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
