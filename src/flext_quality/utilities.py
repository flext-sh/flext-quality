# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utility functions for flext-quality.

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

from flext_web import u as flext_web_u

from flext_quality._utilities import FlextQualityUtilitiesQuality


class FlextQualityUtilities(flext_web_u):
    """Namespace for flext-quality utilities."""

    class Quality(FlextQualityUtilitiesQuality):
        """Quality-specific utilities namespace."""


u = FlextQualityUtilities
__all__: list[str] = ["FlextQualityUtilities", "u"]
