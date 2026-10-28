# AUTO-GENERATED FILE — Regenerate with: make gen
"""Type definitions for flext-quality.

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

from flext_web import t as flext_web_t

from flext_quality._typings import FlextQualityTypingsQuality


class FlextQualityTypes(flext_web_t):
    """Namespace for flext-quality type definitions."""

    class Quality(FlextQualityTypingsQuality):
        """Quality-specific types namespace (project slot)."""


t = FlextQualityTypes
__all__: list[str] = ["FlextQualityTypes", "t"]
