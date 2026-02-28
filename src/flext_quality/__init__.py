"""FLEXT Quality - Unified orchestration platform for Claude Code tooling.

Exposes `FlextQuality` as the main API facade, along with domain models,
settings, and utilities. Uses flext-core patterns: `FlextResult[T]`
railway pattern, `FlextSettings`.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import (
        FlextDecorators as d,
        FlextExceptions as e,
        FlextHandlers as h,
        FlextMixins as x,
        FlextResult as r,
        FlextService as s,
    )

    from flext_quality.api import FlextQuality
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )

__version__ = "0.9.0"

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextQuality": ("flext_quality.api", "FlextQuality"),
    "FlextQualityConstants": ("flext_quality.constants", "FlextQualityConstants"),
    "FlextQualityModels": ("flext_quality.models", "FlextQualityModels"),
    "FlextQualityProtocols": ("flext_quality.protocols", "FlextQualityProtocols"),
    "FlextQualitySettings": ("flext_quality.settings", "FlextQualitySettings"),
    "FlextQualityTypes": ("flext_quality.typings", "FlextQualityTypes"),
    "FlextQualityUtilities": ("flext_quality.utilities", "FlextQualityUtilities"),
    "c": ("flext_quality.constants", "FlextQualityConstants"),
    "d": ("flext_core", "FlextDecorators"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "FlextHandlers"),
    "m": ("flext_quality.models", "FlextQualityModels"),
    "p": ("flext_quality.protocols", "FlextQualityProtocols"),
    "r": ("flext_core", "FlextResult"),
    "s": ("flext_core", "FlextService"),
    "t": ("flext_quality.typings", "FlextQualityTypes"),
    "u": ("flext_quality.utilities", "FlextQualityUtilities"),
    "x": ("flext_core", "FlextMixins"),
}

__all__ = [
    "FlextQuality",
    "FlextQualityConstants",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "__version__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
