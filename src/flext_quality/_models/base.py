"""Base models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import m


class FlextQualityModelsBase:
    """Base models for flext-quality."""

    class ConfigNamespace(m.BaseModel):
        """Open, frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = m.ConfigDict(extra="allow", frozen=True)


__all__: list[str] = ["FlextQualityModelsBase"]
