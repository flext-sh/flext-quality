# AUTO-GENERATED FILE — Regenerate with: make gen
"""Core package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules as FlextQualityAuditRules,
        FlextQualityConfigManager as FlextQualityConfigManager,
        FlextQualityConfigTypes as FlextQualityConfigTypes,
        FlextQualityStyleGuide as FlextQualityStyleGuide,
        FlextQualityValidationSettings as FlextQualityValidationSettings,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".config_manager": (
            "FlextQualityAuditRules",
            "FlextQualityConfigManager",
            "FlextQualityConfigTypes",
            "FlextQualityStyleGuide",
            "FlextQualityValidationSettings",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
