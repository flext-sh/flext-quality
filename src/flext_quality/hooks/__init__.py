# AUTO-GENERATED FILE — Regenerate with: make gen
"""Hooks package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": ("FlextQualityBaseHook",),
        ".manager": ("FlextQualityHookManager",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
