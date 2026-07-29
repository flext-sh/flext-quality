# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_infra import d as d
    from flext_infra import e as e
    from flext_infra import h as h
    from flext_infra import r as r
    from flext_infra import x as x

    from ._config import FlextQualityConfig as FlextQualityConfig
    from ._config import config as config
    from ._settings import FlextQualitySettings as FlextQualitySettings
    from ._settings import settings as settings
    from .api import FlextQuality as FlextQuality
    from .api import quality as quality
    from .base import FlextQualityServiceBase as FlextQualityServiceBase

    s: type[FlextQualityServiceBase]
    from .cli import FlextQualityCli as FlextQualityCli
    from .cli import main as main
    from .constants import FlextQualityConstants as FlextQualityConstants

    c: type[FlextQualityConstants]
    from .models import FlextQualityModels as FlextQualityModels

    m: type[FlextQualityModels]
    from .protocols import FlextQualityProtocols as FlextQualityProtocols

    p: type[FlextQualityProtocols]
    from .typings import FlextQualityTypes as FlextQualityTypes

    t: type[FlextQualityTypes]
    from .utilities import FlextQualityUtilities as FlextQualityUtilities

    u: type[FlextQualityUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextQualityConfig", "config"),
    "._settings": ("FlextQualitySettings", "settings"),
    ".api": ("FlextQuality", "quality"),
    ".base": ("FlextQualityServiceBase", "s"),
    ".cli": ("FlextQualityCli", "main"),
    ".constants": ("FlextQualityConstants", "c"),
    ".models": ("FlextQualityModels", "m"),
    ".protocols": ("FlextQualityProtocols", "p"),
    ".typings": ("FlextQualityTypes", "t"),
    ".utilities": ("FlextQualityUtilities", "u"),
    "flext_infra": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityCli",
    "FlextQualityConfig",
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
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
