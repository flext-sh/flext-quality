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
    from flext_infra import d, e, h, r, x

    from ._settings import FlextQualitySettings, settings
    from .api import FlextQuality, quality
    from .base import FlextQualityServiceBase, s
    from .cli import FlextQualityCli, main
    from .constants import FlextQualityConstants, FlextQualityConstants as c
    from .hooks.manager import FlextQualityHookManager
    from .integrations.claude_context import FlextQualityClaudeContextClient
    from .integrations.claude_mem import FlextQualityClaudeMemClient
    from .integrations.code_execution import FlextQualityCodeExecutionBridge
    from .integrations.mcp_client import FlextQualityMcpClient
    from .models import FlextQualityModels, FlextQualityModels as m
    from .protocols import FlextQualityProtocols, FlextQualityProtocols as p
    from .rules.engine import FlextQualityRulesEngine
    from .rules.loader import FlextQualityRulesLoader
    from .typings import FlextQualityTypes, FlextQualityTypes as t
    from .utilities import FlextQualityUtilities, FlextQualityUtilities as u

    _ = (
        c,
        FlextQualityConstants,
        t,
        FlextQualityTypes,
        p,
        FlextQualityProtocols,
        m,
        FlextQualityModels,
        u,
        FlextQualityUtilities,
        d,
        e,
        h,
        r,
        x,
        s,
        FlextQualityServiceBase,
        main,
        FlextQualityCli,
        FlextQualitySettings,
        settings,
        FlextQuality,
        quality,
        FlextQualityHookManager,
        FlextQualityRulesLoader,
        FlextQualityRulesEngine,
        FlextQualityCodeExecutionBridge,
        FlextQualityClaudeContextClient,
        FlextQualityClaudeMemClient,
        FlextQualityMcpClient,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._settings": (
        "FlextQualitySettings",
        "settings",
    ),
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
    ".hooks.manager": ("FlextQualityHookManager",),
    ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
    ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
    ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
    ".integrations.mcp_client": ("FlextQualityMcpClient",),
    ".models": (
        "FlextQualityModels",
        "m",
    ),
    ".protocols": (
        "FlextQualityProtocols",
        "p",
    ),
    ".rules.engine": ("FlextQualityRulesEngine",),
    ".rules.loader": ("FlextQualityRulesLoader",),
    ".typings": (
        "FlextQualityTypes",
        "t",
    ),
    ".utilities": (
        "FlextQualityUtilities",
        "u",
    ),
    "flext_infra": (
        "d",
        "e",
        "h",
        "r",
        "x",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConstants",
    "FlextQualityHookManager",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
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
    "build_lazy_import_map",
    "c",
    "d",
    "e",
    "h",
    "install_lazy_exports",
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

__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConstants",
    "FlextQualityHookManager",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
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
    "settings",
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
