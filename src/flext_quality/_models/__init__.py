# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._models._quality_namespace import FlextQualityNamespace
    from flext_quality._models.flextqualitymodels_part_01 import (
        FlextQualityModelsPart01,
    )
    from flext_quality._models.flextqualitymodels_part_02 import (
        FlextQualityModelsPart02,
    )


__all__: tuple[str, ...] = (
    "FlextQualityModelsPart01",
    "FlextQualityModelsPart02",
    "FlextQualityNamespace",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityModelsPart01": ".flextqualitymodels_part_01",
        "FlextQualityModelsPart02": ".flextqualitymodels_part_02",
        "FlextQualityNamespace": "._quality_namespace",
    }),
    public_exports=__all__,
)
