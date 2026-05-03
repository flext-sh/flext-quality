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
        ".scripts",
        ".tools",
    ),
    build_lazy_import_map(
        {
            ".core.config_manager": (
                "FlextQualityAuditRules",
                "FlextQualityConfigManager",
                "FlextQualityStyleGuide",
                "FlextQualityValidationSettings",
            ),
            ".dashboard": ("FlextQualityDocumentationDashboard",),
            ".notifications": ("FlextQualityDocumentationNotifier",),
            ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".scripts.audit": ("FlextQualityDocumentationAuditor",),
            ".scripts.optimize": ("FlextQualityDocumentationOptimizer",),
            ".scripts.report": ("FlextQualityDocumentationReporter",),
            ".scripts.validate": (
                "FlextQualityContentValidator",
                "FlextQualityLinkValidator",
            ),
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
