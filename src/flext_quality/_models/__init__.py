# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._models.base import FlextQualityModelsBase
    from flext_quality._models.flextqualitymodels_part_01 import (
        FlextQualityModelsPart01,
    )
    from flext_quality._models.flextqualitymodels_part_02 import (
        FlextQualityModelsPart02,
    )


__all__: tuple[str, ...] = (
    "FlextQualityModelsBase",
    "FlextQualityModelsPart01",
    "FlextQualityModelsPart02",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityModelsBase": ".base",
        "FlextQualityModelsPart01": ".flextqualitymodels_part_01",
        "FlextQualityModelsPart02": ".flextqualitymodels_part_02",
    }),
    public_exports=__all__,
)
