# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.rules package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .engine import FlextQualityRulesEngine as FlextQualityRulesEngine
    from .loader import FlextQualityRulesLoader as FlextQualityRulesLoader
    from .validators import FlextQualityValidators as FlextQualityValidators

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".engine": ("FlextQualityRulesEngine",),
    ".loader": ("FlextQualityRulesLoader",),
    ".validators": ("FlextQualityValidators",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
