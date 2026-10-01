"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from ._models.flextqualitymodels_part_02 import FlextQualityModelsPart02


class FlextQualityModels(FlextQualityModelsPart02):
    """Namespace for flext-quality models."""


m = FlextQualityModels

__all__: list[str] = ["FlextQualityModels", "m"]
