# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import core as core, scripts as scripts, tools as tools
    from .core.config_manager import (
        FlextQualityConfigManager as FlextQualityConfigManager,
    )
    from .dashboard import (
        FlextQualityDocumentationDashboard as FlextQualityDocumentationDashboard,
    )
    from .notifications import (
        FlextQualityDocumentationNotifier as FlextQualityDocumentationNotifier,
    )
    from .scheduled_maintenance import (
        FlextQualityScheduledMaintenance as FlextQualityScheduledMaintenance,
    )
    from .tools.link_checker import FlextQualityLinkChecker as FlextQualityLinkChecker
    from .tools.style_validator import (
        FlextQualityStyleValidator as FlextQualityStyleValidator,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".core": ("core",),
    ".core.config_manager": ("FlextQualityConfigManager",),
    ".dashboard": ("FlextQualityDocumentationDashboard",),
    ".notifications": ("FlextQualityDocumentationNotifier",),
    ".scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
    ".scripts": ("scripts",),
    ".tools": ("tools",),
    ".tools.link_checker": ("FlextQualityLinkChecker",),
    ".tools.style_validator": ("FlextQualityStyleValidator",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQualityConfigManager",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityLinkChecker",
    "FlextQualityScheduledMaintenance",
    "FlextQualityStyleValidator",
    "core",
    "scripts",
    "tools",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
