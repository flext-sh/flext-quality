from __future__ import annotations

from flext_quality import m


class _QualityNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less.

    Copyright (c) 2026 FLEXT Team. All rights reserved.
    SPDX-License-Identifier: MIT
    """

    model_config = m.ConfigDict(extra="allow", frozen=True)
