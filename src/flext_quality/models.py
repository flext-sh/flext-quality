"""Pydantic models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality._models import (
    FlextQualityModelsBase,
    FlextQualityModelsPart01,
    FlextQualityModelsPart02,
)


class FlextQualityModels(
    FlextQualityModelsBase, FlextQualityModelsPart02, FlextQualityModelsPart01
):
    """Namespace for flext-quality models."""


m = FlextQualityModels

__all__: list[str] = ["FlextQualityModels", "m"]
