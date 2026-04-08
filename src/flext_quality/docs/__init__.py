# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Docs package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
