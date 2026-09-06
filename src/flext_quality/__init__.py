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
    from . import docs as docs
    from . import hooks as hooks
    from . import integrations as integrations
    from . import mcp as mcp
    from . import rules as rules
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
    "TYPE_CHECKING",
    "ClassVar",
    "Final",
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
