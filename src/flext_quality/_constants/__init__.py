# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._constants.base import FlextQualityConstantsBase
    from flext_quality._constants.values import FlextQualityConstantsValues


__all__: tuple[str, ...] = ("FlextQualityConstantsBase", "FlextQualityConstantsValues")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityConstantsBase": ".base",
        "FlextQualityConstantsValues": ".values",
    }),
    public_exports=__all__,
)
