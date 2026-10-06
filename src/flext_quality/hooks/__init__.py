# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.hooks package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager


__all__: tuple[str, ...] = ("FlextQualityBaseHook", "FlextQualityHookManager")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityBaseHook": ".base",
        "FlextQualityHookManager": ".manager",
    }),
    public_exports=__all__,
)
