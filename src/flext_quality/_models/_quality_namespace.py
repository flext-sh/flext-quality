from __future__ import annotations

from flext_quality import m


class _QualityNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less.

    Copyright (c) 2026 FLEXT Team. All rights reserved.
    SPDX-License-Identifier: MIT
    """

    model_config = m.ConfigDict(extra="allow", frozen=True)


def quality_namespace() -> _QualityNamespace:
    """Build the open, frozen ``Quality`` config namespace instance.

    Returns:
        The resulting ``_QualityNamespace``.
    """
    return _QualityNamespace()


__all__: list[str] = ["_QualityNamespace", "quality_namespace"]
