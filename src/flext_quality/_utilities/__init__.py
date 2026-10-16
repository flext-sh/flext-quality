# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._utilities.quality import FlextQualityUtilitiesQuality


__all__: tuple[str, ...] = ("FlextQualityUtilitiesQuality",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextQualityUtilitiesQuality": ".quality"}),
    public_exports=__all__,
)
