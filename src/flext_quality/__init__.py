# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web import cli, d, e, h, r, web, x

    from flext_quality.__version__ import (
        FlextQualityVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_quality._config import FlextQualityConfig, config
    from flext_quality._settings import FlextQualitySettings, settings
    from flext_quality.api import FlextQuality, quality
    from flext_quality.base import FlextQualityServiceBase, s
    from flext_quality.cli import FlextQualityCli, main
    from flext_quality.config_models import FlextQualityConfigModels
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.typings import FlextQualityTypes, t
    from flext_quality.utilities import FlextQualityUtilities, u


__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityCli",
    "FlextQualityConfig",
    "FlextQualityConfigModels",
    "FlextQualityConstants",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "cli",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "web",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQuality": ".api",
        "FlextQualityCli": ".cli",
        "FlextQualityConfig": "._config",
        "FlextQualityConfigModels": ".config_models",
        "FlextQualityConstants": ".constants",
        "FlextQualityModels": ".models",
        "FlextQualityProtocols": ".protocols",
        "FlextQualityServiceBase": ".base",
        "FlextQualitySettings": "._settings",
        "FlextQualityTypes": ".typings",
        "FlextQualityUtilities": ".utilities",
        "FlextQualityVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "c": ".constants",
        "cli": "flext_web",
        "config": "._config",
        "d": "flext_web",
        "e": "flext_web",
        "h": "flext_web",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "quality": ".api",
        "r": "flext_web",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "web": "flext_web",
        "x": "flext_web",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_quality.__version__ import __version__
