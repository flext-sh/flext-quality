"""Utility functions for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebUtilities

from flext_quality._utilities.quality import FlextQualityUtilitiesQuality


class FlextQualityUtilities(FlextWebUtilities):
    """Namespace for flext-quality utilities."""

    class Quality(FlextQualityUtilitiesQuality):
        """Quality-specific utilities namespace."""


u = FlextQualityUtilities

__all__: list[str] = ["FlextQualityUtilities", "u"]
