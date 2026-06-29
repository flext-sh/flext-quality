# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_quality.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_web import d as d, e as e, h as h, r as r, x as x

    from flext_quality.api import FlextQuality as FlextQuality, quality as quality
    from flext_quality.base import (
        FlextQualityServiceBase as FlextQualityServiceBase,
        s as s,
    )
    from flext_quality.cli import FlextQualityCli as FlextQualityCli, main as main
    from flext_quality.constants import (
        FlextQualityConstants as FlextQualityConstants,
        c as c,
    )
    from flext_quality.models import FlextQualityModels as FlextQualityModels, m as m
    from flext_quality.protocols import (
        FlextQualityProtocols as FlextQualityProtocols,
        p as p,
    )
    from flext_quality.settings import FlextQualitySettings as FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes as FlextQualityTypes, t as t
    from flext_quality.utilities import (
        FlextQualityUtilities as FlextQualityUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextQuality",
            "quality",
        ),
        ".base": (
            "FlextQualityServiceBase",
            "s",
        ),
        ".cli": (
            "FlextQualityCli",
            "main",
        ),
        ".constants": (
            "FlextQualityConstants",
            "c",
        ),
        ".models": (
            "FlextQualityModels",
            "m",
        ),
        ".protocols": (
            "FlextQualityProtocols",
            "p",
        ),
        ".settings": ("FlextQualitySettings",),
        ".typings": (
            "FlextQualityTypes",
            "t",
        ),
        ".utilities": (
            "FlextQualityUtilities",
            "u",
        ),
        "flext_web": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityCli",
    "FlextQualityConstants",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
