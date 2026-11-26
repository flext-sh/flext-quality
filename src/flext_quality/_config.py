"""FlextQualityConfig — frozen config singleton for flext-quality (ADR-005 §7).

Business rules live in ``config/*.yaml`` under the ``Quality:`` key. Typed domains
such as ``config.Quality.notifications`` are validated by their layer-zero models in
``config_models``; the namespace stays open for the remaining keys.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import FlextCliConfig
from pydantic import Field

from flext_quality.config_models import FlextQualityModelsConfig


class FlextQualityConfig(FlextCliConfig):
    """Quality config auto-loaded model-less from ``config/*.yaml``.

    The fleet-converged config inherits only the declared frozen config
    capability base (``config_bases`` precedence: meltano -> cli -> core); the
    adjustable runtime settings keep their own independent ``_settings.py``
    lifecycle.
    """

    Quality: Annotated[
        FlextQualityModelsConfig.QualityConfigNamespace,
        Field(
            description="Namespace exposing ``config/*.yaml`` under ``Quality``.",
        ),
    ]


config: FlextQualityConfig = FlextQualityConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_quality import config``."""

__all__: list[str] = ["FlextQualityConfig", "config"]
