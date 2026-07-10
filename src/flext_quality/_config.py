"""FlextQualityConfig — frozen config singleton for flext-quality (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Quality:`` key and
are exposed through the open ``config.Quality`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Quality.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_cli import FlextCliConfig


class _QualityNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextQualityConfig(FlextCliConfig):
    """Quality config auto-loaded model-less from ``config/*.yaml``."""

    Quality: _QualityNamespace = _QualityNamespace()


config: FlextQualityConfig = FlextQualityConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_quality import config``."""

__all__: list[str] = ["FlextQualityConfig", "config"]
