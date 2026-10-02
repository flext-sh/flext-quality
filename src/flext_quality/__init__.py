# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
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
    from flext_web import d, e, h, r, x

    from flext_quality import docs, hooks, integrations, mcp, rules
    from flext_quality._config import FlextQualityConfig, config
    from flext_quality._settings import FlextQualitySettings, settings
    from flext_quality.api import FlextQuality, quality
    from flext_quality.base import FlextQualityServiceBase, s
    from flext_quality.cli import FlextQualityCli, main
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.docs.core.config_manager import FlextQualityConfigManager
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import FlextQualityDocumentationValidator
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient
    from flext_quality.mcp.resources import FlextQualityMcpResources
    from flext_quality.mcp.server import FlextQualityMcpServer
    from flext_quality.mcp.tools import FlextQualityMcpTools
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.typings import FlextQualityTypes, t
    from flext_quality.utilities import FlextQualityUtilities, u


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
            "flext_web": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
