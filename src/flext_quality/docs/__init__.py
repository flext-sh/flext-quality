# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
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
        main as main,
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

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
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
    "FlextQualityBaseReporter": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ],
    "FlextQualityBaseValidator": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ],
    "FlextQualityConfigManager": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ],
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
    "FlextQualityLinkChecker": [
        "flext_quality.docs.tools.link_checker",
        "FlextQualityLinkChecker",
    ],
    "FlextQualityLinkValidator": [
        "flext_quality.docs.scripts.validate",
        "FlextQualityLinkValidator",
    ],
    "FlextQualityScheduledMaintenance": [
        "flext_quality.docs.scheduled_maintenance",
        "FlextQualityScheduledMaintenance",
    ],
    "FlextQualityStyleGuide": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ],
    "FlextQualityStyleValidator": [
        "flext_quality.docs.tools.style_validator",
        "FlextQualityStyleValidator",
    ],
    "FlextQualityValidationConfig": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ],
    "MAX_BROKEN_LINKS_TO_SHOW": [
        "flext_quality.docs.notifications",
        "MAX_BROKEN_LINKS_TO_SHOW",
    ],
    "MIN_HEADINGS_FOR_TOC": [
        "flext_quality.docs.scripts.optimize",
        "MIN_HEADINGS_FOR_TOC",
    ],
    "ReportValue": ["flext_quality.docs.scripts.report", "ReportValue"],
    "analyze_file_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_file_content",
    ],
    "analyze_files_content": [
        "flext_quality.docs.tools.content_analyzer",
        "analyze_files_content",
    ],
    "audit": ["flext_quality.docs.scripts.audit", ""],
    "base_classes": ["flext_quality.docs.core.base_classes", ""],
    "config_manager": ["flext_quality.docs.core.config_manager", ""],
    "content_analyzer": ["flext_quality.docs.tools.content_analyzer", ""],
    "core": ["flext_quality.docs.core", ""],
    "dashboard": ["flext_quality.docs.dashboard", ""],
    "file_discovery": ["flext_quality.docs.core.file_discovery", ""],
    "link_checker": ["flext_quality.docs.tools.link_checker", ""],
    "logger": ["flext_quality.docs.scheduled_maintenance", "logger"],
    "main": ["flext_quality.docs.scripts.validate", "main"],
    "notifications": ["flext_quality.docs.notifications", ""],
    "optimize": ["flext_quality.docs.scripts.optimize", ""],
    "report": ["flext_quality.docs.scripts.report", ""],
    "scheduled_maintenance": ["flext_quality.docs.scheduled_maintenance", ""],
    "scripts": ["flext_quality.docs.scripts", ""],
    "style_validator": ["flext_quality.docs.tools.style_validator", ""],
    "tools": ["flext_quality.docs.tools", ""],
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
}

_EXPORTS: Sequence[str] = [
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
    "MAX_BROKEN_LINKS_TO_SHOW",
    "MIN_HEADINGS_FOR_TOC",
    "ReportValue",
    "analyze_file_content",
    "analyze_files_content",
    "audit",
    "base_classes",
    "config_manager",
    "content_analyzer",
    "core",
    "dashboard",
    "file_discovery",
    "link_checker",
    "logger",
    "main",
    "notifications",
    "optimize",
    "report",
    "scheduled_maintenance",
    "scripts",
    "style_validator",
    "tools",
    "validate",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
