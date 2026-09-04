# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

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
    from . import mcp as mcp
    from enum import StrEnum, auto, unique
    from flext_infra import d, e, h, r, x
    from flext_web import c as web_c
    from typing import ClassVar, Final, TYPE_CHECKING

    from ._config import FlextQualityConfig, config
    from ._settings import FlextQualitySettings, settings
    from .api import FlextQuality, quality
    from .base import FlextQualityServiceBase, FlextQualityServiceBase as s
    from .cli import FlextQualityCli, main
    from .constants import FlextQualityConstants, FlextQualityConstants as c
    from .mcp.resources import FlextQualityMcpResources
    from .mcp.server import FlextQualityMcpServer
    from .mcp.tools import FlextQualityMcpTools
    from .models import FlextQualityModels, FlextQualityModels as m
    from .protocols import FlextQualityProtocols, FlextQualityProtocols as p
    from .typings import FlextQualityTypes, FlextQualityTypes as t
    from .utilities import FlextQualityUtilities, FlextQualityUtilities as u
__all__: tuple[str, ...] = (
    "TYPE_CHECKING",
    "ClassVar",
    "Final",
    "FlextQuality",
    "FlextQualityCli",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityMcpResources",
    "FlextQualityMcpServer",
    "FlextQualityMcpTools",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "MappingProxyType",
    "StrEnum",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "auto",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "mcp",
    "p",
    "quality",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "unique",
    "web_c",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextQualityConfig", "config"),
            "._settings": ("FlextQualitySettings", "settings"),
            ".api": ("FlextQuality", "quality"),
            ".base": ("FlextQualityServiceBase", "s"),
            ".cli": ("FlextQualityCli", "main"),
            ".constants": ("FlextQualityConstants", "c"),
            ".mcp": ("mcp",),
            ".mcp.resources": ("FlextQualityMcpResources",),
            ".mcp.server": ("FlextQualityMcpServer",),
            ".mcp.tools": ("FlextQualityMcpTools",),
            ".models": ("FlextQualityModels", "m"),
            ".protocols": ("FlextQualityProtocols", "p"),
            ".typings": ("FlextQualityTypes", "t"),
            ".utilities": ("FlextQualityUtilities", "u"),
            "enum": ("StrEnum", "auto", "unique"),
            "flext_infra": ("d", "e", "h", "r", "x"),
            "types": ("MappingProxyType",),
            "typing": ("ClassVar", "Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({"flext_web": (("web_c", "c"),)}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
