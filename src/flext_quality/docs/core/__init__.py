# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality.docs.core package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.core.config_manager import FlextQualityConfigManager


__all__: tuple[str, ...] = ("FlextQualityConfigManager",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextQualityConfigManager": ".config_manager"}),
    public_exports=__all__,
)
