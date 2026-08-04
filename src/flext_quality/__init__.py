# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x

    from ._config import FlextQualityConfig as FlextQualityConfig, config as config
    from ._settings import (
        FlextQualitySettings as FlextQualitySettings,
        settings as settings,
    )
    from .api import FlextQuality as FlextQuality, quality as quality
    from .base import FlextQualityServiceBase as FlextQualityServiceBase

    s: type[FlextQualityServiceBase]
    from .cli import FlextQualityCli as FlextQualityCli, main as main
    from .constants import FlextQualityConstants as FlextQualityConstants

    c: type[FlextQualityConstants]
    from .models import FlextQualityModels as FlextQualityModels

    m: type[FlextQualityModels]
    from .protocols import FlextQualityProtocols as FlextQualityProtocols

    p: type[FlextQualityProtocols]
    from .typings import FlextQualityTypes as FlextQualityTypes

    t: type[FlextQualityTypes]
    from .hooks import FlextQualityBaseHook as FlextQualityBaseHook
    from .hooks import FlextQualityHookManager as FlextQualityHookManager
    from .integrations import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from .integrations import FlextQualityClaudeMemClient as FlextQualityClaudeMemClient
    from .integrations import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from .integrations import FlextQualityMcpClient as FlextQualityMcpClient
    from .mcp import FlextQualityMcpResources as FlextQualityMcpResources
    from .mcp import FlextQualityMcpServer as FlextQualityMcpServer
    from .mcp import FlextQualityMcpTools as FlextQualityMcpTools
    from .rules import FlextQualityRulesEngine as FlextQualityRulesEngine
    from .rules import FlextQualityRulesLoader as FlextQualityRulesLoader
    from .rules import FlextQualityValidators as FlextQualityValidators
    from .utilities import FlextQualityUtilities as FlextQualityUtilities

    u: type[FlextQualityUtilities]

# Why: mro-4p0t — re-export domain services imported from flext_quality subpackages.
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
    ".hooks": ("FlextQualityBaseHook", "FlextQualityHookManager"),
    ".integrations": (
        "FlextQualityClaudeContextClient",
        "FlextQualityClaudeMemClient",
        "FlextQualityCodeExecutionBridge",
        "FlextQualityMcpClient",
    ),
    ".rules": (
        "FlextQualityRulesEngine",
        "FlextQualityRulesLoader",
        "FlextQualityValidators",
    ),
    ".mcp": (
        "FlextQualityMcpResources",
        "FlextQualityMcpServer",
        "FlextQualityMcpTools",
    ),
    "flext_infra": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityBaseHook",
    "FlextQualityCli",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfig",
    "FlextQualityConstants",
    "FlextQualityHookManager",
    "FlextQualityMcpClient",
    "FlextQualityMcpResources",
    "FlextQualityMcpServer",
    "FlextQualityMcpTools",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityValidators",
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
