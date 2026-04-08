# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Docs package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import flext_quality.docs.core as _flext_quality_docs_core

    core = _flext_quality_docs_core
    import flext_quality.docs.dashboard as _flext_quality_docs_dashboard
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
    )

    dashboard = _flext_quality_docs_dashboard
    import flext_quality.docs.notifications as _flext_quality_docs_notifications
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard

    notifications = _flext_quality_docs_notifications
    import flext_quality.docs.scheduled_maintenance as _flext_quality_docs_scheduled_maintenance
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier,
    )

    scheduled_maintenance = _flext_quality_docs_scheduled_maintenance
    import flext_quality.docs.scripts as _flext_quality_docs_scripts
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )

    scripts = _flext_quality_docs_scripts
    import flext_quality.docs.tools as _flext_quality_docs_tools
    from flext_quality.docs.scripts import (
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
    )

    tools = _flext_quality_docs_tools
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_quality.docs.tools import (
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_file_content,
        analyze_files_content,
        validate_file_style,
        validate_files_style,
        validate_links_sync,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_quality.docs.core",
        "flext_quality.docs.scripts",
        "flext_quality.docs.tools",
    ),
    {
        "FlextQualityDocumentationDashboard": (
            "flext_quality.docs.dashboard",
            "FlextQualityDocumentationDashboard",
        ),
        "FlextQualityDocumentationNotifier": (
            "flext_quality.docs.notifications",
            "FlextQualityDocumentationNotifier",
        ),
        "FlextQualityScheduledMaintenance": (
            "flext_quality.docs.scheduled_maintenance",
            "FlextQualityScheduledMaintenance",
        ),
        "MAX_BROKEN_LINKS_TO_SHOW": (
            "flext_quality.docs.notifications",
            "MAX_BROKEN_LINKS_TO_SHOW",
        ),
        "c": ("flext_core.constants", "FlextConstants"),
        "core": "flext_quality.docs.core",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard": "flext_quality.docs.dashboard",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
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
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "MAX_BROKEN_LINKS_TO_SHOW",
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
    "c",
    "core",
    "d",
    "dashboard",
    "e",
    "h",
    "m",
    "notifications",
    "p",
    "r",
    "s",
    "scheduled_maintenance",
    "scripts",
    "t",
    "tools",
    "u",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
