"""Layer-zero schemas for YAML-owned quality configuration.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_quality/config_models
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

from pydantic import BaseModel, ConfigDict


class FlextQualityModelsConfig:
    """Configuration declarations independent of the model facade."""

    class QualityConfigNamespace(BaseModel):
        """Open, frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = ConfigDict(extra="allow", frozen=True)


__all__: list[str] = ["FlextQualityModelsConfig"]
