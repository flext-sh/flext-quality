# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Hooks system - Protocol-based hook lifecycle management."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.hooks import base as base, manager as manager
    from flext_quality.hooks.base import FlextQualityBaseHook as FlextQualityBaseHook
    from flext_quality.hooks.manager import (
        FlextQualityHookManager as FlextQualityHookManager,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityBaseHook": ["flext_quality.hooks.base", "FlextQualityBaseHook"],
    "FlextQualityHookManager": [
        "flext_quality.hooks.manager",
        "FlextQualityHookManager",
    ],
    "base": ["flext_quality.hooks.base", ""],
    "manager": ["flext_quality.hooks.manager", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityBaseHook",
    "FlextQualityHookManager",
    "base",
    "manager",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
