# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import core as core
    from . import scripts as scripts
    from . import tools as tools
    from .core.config_manager import FlextQualityConfigManager
    from .dashboard import FlextQualityDocumentationDashboard
    from .notifications import FlextQualityDocumentationNotifier
    from .scheduled_maintenance import FlextQualityScheduledMaintenance
    from .scripts.audit import FlextQualityDocumentationAuditor
    from .scripts.optimize import FlextQualityDocumentationOptimizer
    from .scripts.report import FlextQualityDocumentationReporter
    from .scripts.validate import FlextQualityDocumentationValidator
    from .tools.link_checker import FlextQualityLinkChecker
    from .tools.style_validator import FlextQualityStyleValidator
__all__: tuple[str, ...] = (
    "FlextQualityConfigManager",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
    "FlextQualityLinkChecker",
    "FlextQualityScheduledMaintenance",
    "FlextQualityStyleValidator",
    "core",
    "scripts",
    "tools",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
