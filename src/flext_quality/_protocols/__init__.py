# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Protocols package.

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
    from flext_quality._protocols.quality import FlextQualityProtocolsQuality


__all__: tuple[str, ...] = ("FlextQualityProtocolsQuality",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextQualityProtocolsQuality": ".quality"}),
    public_exports=__all__,
)
