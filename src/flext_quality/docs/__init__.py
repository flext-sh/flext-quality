# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docs package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_quality.docs.core.config_manager import FlextQualityConfigManager
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import FlextQualityDocumentationValidator
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".core",
        ".scripts",
        ".tools",
    ),
    build_lazy_import_map(
        {
            ".core": ("core",),
            ".core.config_manager": ("FlextQualityConfigManager",),
            ".dashboard": ("FlextQualityDocumentationDashboard",),
            ".notifications": ("FlextQualityDocumentationNotifier",),
            ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".scripts": ("scripts",),
            ".scripts.audit": ("FlextQualityDocumentationAuditor",),
            ".scripts.optimize": ("FlextQualityDocumentationOptimizer",),
            ".scripts.report": ("FlextQualityDocumentationReporter",),
            ".scripts.validate": ("FlextQualityDocumentationValidator",),
            ".tools": ("tools",),
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
