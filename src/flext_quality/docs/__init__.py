# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Docs package."""

from __future__ import annotations

import typing as _t

from flext_core.constants import FlextConstants as c
from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.models import FlextModels as m
from flext_core.protocols import FlextProtocols as p
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_core.typings import FlextTypes as t
from flext_core.utilities import FlextUtilities as u

if _t.TYPE_CHECKING:
    import flext_quality.docs.core as _flext_quality_docs_core

    core = _flext_quality_docs_core
    import flext_quality.docs.core.base_classes as _flext_quality_docs_core_base_classes

    base_classes = _flext_quality_docs_core_base_classes
    import flext_quality.docs.core.config_manager as _flext_quality_docs_core_config_manager

    config_manager = _flext_quality_docs_core_config_manager
    import flext_quality.docs.core.file_discovery as _flext_quality_docs_core_file_discovery

    file_discovery = _flext_quality_docs_core_file_discovery
    import flext_quality.docs.dashboard as _flext_quality_docs_dashboard

    dashboard = _flext_quality_docs_dashboard
    import flext_quality.docs.notifications as _flext_quality_docs_notifications

    notifications = _flext_quality_docs_notifications
    import flext_quality.docs.scheduled_maintenance as _flext_quality_docs_scheduled_maintenance

    scheduled_maintenance = _flext_quality_docs_scheduled_maintenance
    import flext_quality.docs.scripts as _flext_quality_docs_scripts

    scripts = _flext_quality_docs_scripts
    import flext_quality.docs.scripts.audit as _flext_quality_docs_scripts_audit

    audit = _flext_quality_docs_scripts_audit
    import flext_quality.docs.scripts.optimize as _flext_quality_docs_scripts_optimize

    optimize = _flext_quality_docs_scripts_optimize
    import flext_quality.docs.scripts.report as _flext_quality_docs_scripts_report

    report = _flext_quality_docs_scripts_report
    import flext_quality.docs.scripts.validate as _flext_quality_docs_scripts_validate

    validate = _flext_quality_docs_scripts_validate
    import flext_quality.docs.tools as _flext_quality_docs_tools

    tools = _flext_quality_docs_tools
    import flext_quality.docs.tools.content_analyzer as _flext_quality_docs_tools_content_analyzer

    content_analyzer = _flext_quality_docs_tools_content_analyzer
    import flext_quality.docs.tools.link_checker as _flext_quality_docs_tools_link_checker

    link_checker = _flext_quality_docs_tools_link_checker
    import flext_quality.docs.tools.style_validator as _flext_quality_docs_tools_style_validator

    style_validator = _flext_quality_docs_tools_style_validator

    _ = (
        FlextQualityAuditRules,
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
        FlextQualityConfigManager,
        FlextQualityContentAnalyzer,
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationDashboard,
        FlextQualityDocumentationFinder,
        FlextQualityDocumentationNotifier,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityFileStatistics,
        FlextQualityLinkChecker,
        FlextQualityLinkValidator,
        FlextQualityScheduledMaintenance,
        FlextQualityStyleGuide,
        FlextQualityStyleValidator,
        FlextQualityValidationConfig,
        MAX_BROKEN_LINKS_TO_SHOW,
        MIN_HEADINGS_FOR_TOC,
        analyze_file_content,
        analyze_files_content,
        audit,
        base_classes,
        c,
        config_manager,
        content_analyzer,
        core,
        d,
        dashboard,
        e,
        file_discovery,
        h,
        link_checker,
        logger,
        m,
        main,
        notifications,
        optimize,
        p,
        r,
        report,
        s,
        scheduled_maintenance,
        scripts,
        style_validator,
        t,
        tools,
        u,
        validate,
        validate_file_style,
        validate_files_style,
        validate_links_sync,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_quality.docs.core",
        "flext_quality.docs.scripts",
        "flext_quality.docs.tools",
    ),
    {
        "FlextQualityDocumentationDashboard": "flext_quality.docs.dashboard",
        "FlextQualityDocumentationNotifier": "flext_quality.docs.notifications",
        "FlextQualityScheduledMaintenance": "flext_quality.docs.scheduled_maintenance",
        "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.docs.notifications",
        "c": ("flext_core.constants", "FlextConstants"),
        "core": "flext_quality.docs.core",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard": "flext_quality.docs.dashboard",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "logger": "flext_quality.docs.scheduled_maintenance",
        "m": ("flext_core.models", "FlextModels"),
        "notifications": "flext_quality.docs.notifications",
        "p": ("flext_core.protocols", "FlextProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "scheduled_maintenance": "flext_quality.docs.scheduled_maintenance",
        "scripts": "flext_quality.docs.scripts",
        "t": ("flext_core.typings", "FlextTypes"),
        "tools": "flext_quality.docs.tools",
        "u": ("flext_core.utilities", "FlextUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
    "FlextQualityAuditRules",
    "FlextQualityBaseAnalyzer",
    "FlextQualityBaseAuditor",
    "FlextQualityBaseReporter",
    "FlextQualityBaseValidator",
    "FlextQualityConfigManager",
    "FlextQualityContentAnalyzer",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationFinder",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityFileStatistics",
    "FlextQualityLinkChecker",
    "FlextQualityLinkValidator",
    "FlextQualityScheduledMaintenance",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityValidationConfig",
    "analyze_file_content",
    "analyze_files_content",
    "audit",
    "base_classes",
    "c",
    "config_manager",
    "content_analyzer",
    "core",
    "d",
    "dashboard",
    "e",
    "file_discovery",
    "h",
    "link_checker",
    "logger",
    "m",
    "main",
    "notifications",
    "optimize",
    "p",
    "r",
    "report",
    "s",
    "scheduled_maintenance",
    "scripts",
    "style_validator",
    "t",
    "tools",
    "u",
    "validate",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
