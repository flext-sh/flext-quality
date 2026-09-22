"""FlextQualityConfig — frozen config singleton for flext-quality (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Quality:`` key and
are exposed through the open ``config.Quality`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Quality.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliConfig, m

from flext_core import FlextSettings


class _QualityNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextQualityConfig(FlextSettings, FlextCliConfig):
    """Quality config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # Unlike never-instantiated namespace holders, ``__init__`` delegates to
    # ``super()`` so the frozen, YAML-validated pydantic construction still
    # runs, and the inherited pydantic ``__setattr__`` keeps the frozen guard.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    Quality: Annotated[
        _QualityNamespace,
        m.Field(
            description="Open namespace exposing ``config/*.yaml`` under ``Quality``."
        ),
    ] = _QualityNamespace()


config: FlextQualityConfig = FlextQualityConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_quality import config``."""

__all__: list[str] = ["FlextQualityConfig", "config"]
