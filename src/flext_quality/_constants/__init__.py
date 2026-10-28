# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._constants.base import FlextQualityConstantsBase
    from flext_quality._constants.enums import FlextQualityConstantsEnums
    from flext_quality._constants.values import FlextQualityConstantsValues


__all__: tuple[str, ...] = (
    "FlextQualityConstantsBase",
    "FlextQualityConstantsEnums",
    "FlextQualityConstantsValues",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityConstantsBase": ".base",
        "FlextQualityConstantsEnums": ".enums",
        "FlextQualityConstantsValues": ".values",
    }),
    public_exports=__all__,
)
