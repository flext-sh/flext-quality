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
    from flext_quality.docs import dashboard, notifications, scheduled_maintenance
    from flext_quality.docs.core import *
    from flext_quality.docs.dashboard import *
    from flext_quality.docs.notifications import *
    from flext_quality.docs.scheduled_maintenance import *
    from flext_quality.docs.scripts import *
    from flext_quality.docs.tools import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityAuditRules": "flext_quality.docs.core.config_manager",
    "FlextQualityBaseAnalyzer": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseAuditor": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseReporter": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseValidator": "flext_quality.docs.core.base_classes",
    "FlextQualityConfigManager": "flext_quality.docs.core.config_manager",
    "FlextQualityContentAnalyzer": "flext_quality.docs.tools.content_analyzer",
    "FlextQualityContentValidator": "flext_quality.docs.scripts.validate",
    "FlextQualityDocumentationAuditor": "flext_quality.docs.scripts.audit",
    "FlextQualityDocumentationDashboard": "flext_quality.docs.dashboard",
    "FlextQualityDocumentationFinder": "flext_quality.docs.core.file_discovery",
    "FlextQualityDocumentationNotifier": "flext_quality.docs.notifications",
    "FlextQualityDocumentationOptimizer": "flext_quality.docs.scripts.optimize",
    "FlextQualityDocumentationReporter": "flext_quality.docs.scripts.report",
    "FlextQualityFileStatistics": "flext_quality.docs.core.file_discovery",
    "FlextQualityLinkChecker": "flext_quality.docs.tools.link_checker",
    "FlextQualityLinkValidator": "flext_quality.docs.scripts.validate",
    "FlextQualityScheduledMaintenance": "flext_quality.docs.scheduled_maintenance",
    "FlextQualityStyleGuide": "flext_quality.docs.core.config_manager",
    "FlextQualityStyleValidator": "flext_quality.docs.tools.style_validator",
    "FlextQualityValidationConfig": "flext_quality.docs.core.config_manager",
    "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.docs.notifications",
    "MIN_HEADINGS_FOR_TOC": "flext_quality.docs.scripts.optimize",
    "ReportValue": "flext_quality.docs.scripts.report",
    "analyze_file_content": "flext_quality.docs.tools.content_analyzer",
    "analyze_files_content": "flext_quality.docs.tools.content_analyzer",
    "audit": "flext_quality.docs.scripts.audit",
    "base_classes": "flext_quality.docs.core.base_classes",
    "config_manager": "flext_quality.docs.core.config_manager",
    "content_analyzer": "flext_quality.docs.tools.content_analyzer",
    "core": "flext_quality.docs.core",
    "dashboard": "flext_quality.docs.dashboard",
    "file_discovery": "flext_quality.docs.core.file_discovery",
    "link_checker": "flext_quality.docs.tools.link_checker",
    "logger": "flext_quality.docs.scheduled_maintenance",
    "main": "flext_quality.docs.scripts.validate",
    "notifications": "flext_quality.docs.notifications",
    "optimize": "flext_quality.docs.scripts.optimize",
    "report": "flext_quality.docs.scripts.report",
    "scheduled_maintenance": "flext_quality.docs.scheduled_maintenance",
    "scripts": "flext_quality.docs.scripts",
    "style_validator": "flext_quality.docs.tools.style_validator",
    "tools": "flext_quality.docs.tools",
    "validate": "flext_quality.docs.scripts.validate",
    "validate_file_style": "flext_quality.docs.tools.style_validator",
    "validate_files_style": "flext_quality.docs.tools.style_validator",
    "validate_links_sync": "flext_quality.docs.tools.link_checker",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
