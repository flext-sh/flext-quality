# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
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
from flext_quality._exports import FLEXT_QUALITY_LAZY_IMPORTS

if TYPE_CHECKING:
    from flext_core._root_typing_parts import d as d, e as e, h as h, r as r, x as x
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
    from flext_quality.hooks.base import FlextQualityBaseHook as FlextQualityBaseHook
    from flext_quality.hooks.manager import (
        FlextQualityHookManager as FlextQualityHookManager,
    )
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient as FlextQualityClaudeMemClient,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient as FlextQualityMcpClient,
    )
    from flext_quality.mcp.resources import (
        FlextQualityMcpResources as FlextQualityMcpResources,
    )
    from flext_quality.mcp.server import FlextQualityMcpServer as FlextQualityMcpServer
    from flext_quality.mcp.tools import FlextQualityMcpTools as FlextQualityMcpTools
    from flext_quality.models import FlextQualityModels as FlextQualityModels, m as m
    from flext_quality.protocols import (
        FlextQualityProtocols as FlextQualityProtocols,
        p as p,
    )
    from flext_quality.rules.engine import (
        FlextQualityRulesEngine as FlextQualityRulesEngine,
    )
    from flext_quality.rules.loader import (
        FlextQualityRulesLoader as FlextQualityRulesLoader,
    )
    from flext_quality.rules.validators import (
        FlextQualityValidators as FlextQualityValidators,
    )
    from flext_quality.settings import FlextQualitySettings as FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes as FlextQualityTypes, t as t
    from flext_quality.utilities import (
        FlextQualityUtilities as FlextQualityUtilities,
        u as u,
    )


_LAZY_IMPORTS = FLEXT_QUALITY_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
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
    "quality",
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
    "r",
    "s",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
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
    public_exports=_PUBLIC_EXPORTS,
)
