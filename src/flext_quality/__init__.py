# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from types import MappingProxyType
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
    from flext_infra import d, e, h, r, x
    from flext_web import c as web_c

    from . import (
        docs as docs,
        hooks as hooks,
        integrations as integrations,
        mcp as mcp,
        rules as rules,
    )
    from ._config import FlextQualityConfig, config
    from ._settings import FlextQualitySettings, settings
    from .api import FlextQuality, quality
    from .base import FlextQualityServiceBase, FlextQualityServiceBase as s
    from .cli import FlextQualityCli, main
    from .constants import FlextQualityConstants, FlextQualityConstants as c
    from .docs.core.config_manager import FlextQualityConfigManager
    from .docs.dashboard import FlextQualityDocumentationDashboard
    from .docs.notifications import FlextQualityDocumentationNotifier
    from .docs.scheduled_maintenance import FlextQualityScheduledMaintenance
    from .docs.scripts.audit import FlextQualityDocumentationAuditor
    from .docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from .docs.scripts.report import FlextQualityDocumentationReporter
    from .docs.scripts.validate import FlextQualityDocumentationValidator
    from .docs.tools.link_checker import FlextQualityLinkChecker
    from .docs.tools.style_validator import FlextQualityStyleValidator
    from .hooks.base import FlextQualityBaseHook
    from .hooks.manager import FlextQualityHookManager
    from .integrations.claude_context import FlextQualityClaudeContextClient
    from .integrations.claude_mem import FlextQualityClaudeMemClient
    from .integrations.code_execution import FlextQualityCodeExecutionBridge
    from .integrations.mcp_client import FlextQualityMcpClient
    from .mcp.resources import FlextQualityMcpResources
    from .mcp.server import FlextQualityMcpServer
    from .mcp.tools import FlextQualityMcpTools
    from .models import FlextQualityModels, FlextQualityModels as m
    from .protocols import FlextQualityProtocols, FlextQualityProtocols as p
    from .rules.engine import FlextQualityRulesEngine
    from .rules.loader import FlextQualityRulesLoader
    from .rules.validators import FlextQualityValidators
    from .typings import FlextQualityTypes, FlextQualityTypes as t
    from .utilities import FlextQualityUtilities, FlextQualityUtilities as u
__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfig",
    "FlextQualityConfigManager",
    "FlextQualityConstants",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
    "FlextQualityHookManager",
    "FlextQualityLinkChecker",
    "FlextQualityMcpClient",
    "FlextQualityMcpResources",
    "FlextQualityMcpServer",
    "FlextQualityMcpTools",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityScheduledMaintenance",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityStyleValidator",
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
    "docs",
    "e",
    "h",
    "hooks",
    "integrations",
    "m",
    "main",
    "mcp",
    "p",
    "quality",
    "r",
    "rules",
    "s",
    "settings",
    "t",
    "u",
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
            ".docs": ("docs",),
            ".docs.core.config_manager": ("FlextQualityConfigManager",),
            ".docs.dashboard": ("FlextQualityDocumentationDashboard",),
            ".docs.notifications": ("FlextQualityDocumentationNotifier",),
            ".docs.scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".docs.scripts.audit": ("FlextQualityDocumentationAuditor",),
            ".docs.scripts.optimize": ("FlextQualityDocumentationOptimizer",),
            ".docs.scripts.report": ("FlextQualityDocumentationReporter",),
            ".docs.scripts.validate": ("FlextQualityDocumentationValidator",),
            ".docs.tools.link_checker": ("FlextQualityLinkChecker",),
            ".docs.tools.style_validator": ("FlextQualityStyleValidator",),
            ".hooks": ("hooks",),
            ".hooks.base": ("FlextQualityBaseHook",),
            ".hooks.manager": ("FlextQualityHookManager",),
            ".integrations": ("integrations",),
            ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
            ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
            ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
            ".integrations.mcp_client": ("FlextQualityMcpClient",),
            ".mcp": ("mcp",),
            ".mcp.resources": ("FlextQualityMcpResources",),
            ".mcp.server": ("FlextQualityMcpServer",),
            ".mcp.tools": ("FlextQualityMcpTools",),
            ".models": ("FlextQualityModels", "m"),
            ".protocols": ("FlextQualityProtocols", "p"),
            ".rules": ("rules",),
            ".rules.engine": ("FlextQualityRulesEngine",),
            ".rules.loader": ("FlextQualityRulesLoader",),
            ".rules.validators": ("FlextQualityValidators",),
            ".typings": ("FlextQualityTypes", "t"),
            ".utilities": ("FlextQualityUtilities", "u"),
            "flext_infra": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({"flext_web": (("web_c", "c"),)}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
