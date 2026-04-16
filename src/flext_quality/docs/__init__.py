# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docs package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".core",
        ".tools",
        "scripts",
    ),
    build_lazy_import_map(
        {
            ".core.base_classes": (
                "FlextQualityBaseAnalyzer",
                "FlextQualityBaseAuditor",
                "FlextQualityBaseReporter",
                "FlextQualityBaseValidator",
            ),
            ".core.config_manager": (
                "FlextQualityAuditRules",
                "FlextQualityConfigManager",
                "FlextQualityStyleGuide",
                "FlextQualityValidationSettings",
            ),
            ".core.file_discovery": (
                "FlextQualityDocumentationFinder",
                "FlextQualityFileStatistics",
            ),
            ".dashboard": ("FlextQualityDocumentationDashboard",),
            ".notifications": ("FlextQualityDocumentationNotifier",),
            ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".tools.content_analyzer": ("FlextQualityContentAnalyzer",),
            ".tools.link_checker": ("FlextQualityLinkChecker",),
            ".tools.style_validator": ("FlextQualityStyleValidator",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
