# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from flext_quality import (
        FlextQuality,
        FlextQualityCli,
        FlextQualityConfig,
        FlextQualityConstants,
        FlextQualityModels,
        FlextQualityModelsConfig,
        FlextQualityProtocols,
        FlextQualityServiceBase,
        FlextQualitySettings,
        FlextQualityTypes,
        FlextQualityUtilities,
        FlextQualityVersion,
        config,
        main,
        quality,
        settings,
    )
    from flext_quality.docs import (
        FlextQualityDocumentationDashboard,
        FlextQualityDocumentationNotifier,
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.core import FlextQualityConfigManager
    from flext_quality.docs.scripts import (
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityDocumentationValidator,
    )
    from flext_quality.docs.tools import (
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
    )
    from flext_quality.hooks import FlextQualityBaseHook, FlextQualityHookManager
    from flext_quality.integrations import (
        FlextQualityClaudeContextClient,
        FlextQualityClaudeMemClient,
        FlextQualityCodeExecutionBridge,
        FlextQualityMcpClient,
    )
    from flext_quality.mcp import (
        FlextQualityMcpResources,
        FlextQualityMcpServer,
        FlextQualityMcpTools,
    )
    from flext_quality.rules import (
        FlextQualityRulesEngine,
        FlextQualityRulesLoader,
        FlextQualityValidators,
    )
    from tests.base import TestsFlextQualityServiceBase, s
    from tests.constants import TestsFlextQualityConstants, c
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.settings import TestsFlextQualitySettings
    from tests.typings import TestsFlextQualityTypes, t
    from tests.utilities import TestsFlextQualityUtilities, u


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
    "FlextQualityModelsConfig",
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
    "FlextQualityVersion",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "api",
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
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextQuality": "flext_quality",
        "FlextQualityBaseHook": "flext_quality.hooks",
        "FlextQualityClaudeContextClient": "flext_quality.integrations",
        "FlextQualityClaudeMemClient": "flext_quality.integrations",
        "FlextQualityCli": "flext_quality",
        "FlextQualityCodeExecutionBridge": "flext_quality.integrations",
        "FlextQualityConfig": "flext_quality",
        "FlextQualityConfigManager": "flext_quality.docs.core",
        "FlextQualityConstants": "flext_quality",
        "FlextQualityDocumentationAuditor": "flext_quality.docs.scripts",
        "FlextQualityDocumentationDashboard": "flext_quality.docs",
        "FlextQualityDocumentationNotifier": "flext_quality.docs",
        "FlextQualityDocumentationOptimizer": "flext_quality.docs.scripts",
        "FlextQualityDocumentationReporter": "flext_quality.docs.scripts",
        "FlextQualityDocumentationValidator": "flext_quality.docs.scripts",
        "FlextQualityHookManager": "flext_quality.hooks",
        "FlextQualityLinkChecker": "flext_quality.docs.tools",
        "FlextQualityMcpClient": "flext_quality.integrations",
        "FlextQualityMcpResources": "flext_quality.mcp",
        "FlextQualityMcpServer": "flext_quality.mcp",
        "FlextQualityMcpTools": "flext_quality.mcp",
        "FlextQualityModels": "flext_quality",
        "FlextQualityModelsConfig": "flext_quality",
        "FlextQualityProtocols": "flext_quality",
        "FlextQualityRulesEngine": "flext_quality.rules",
        "FlextQualityRulesLoader": "flext_quality.rules",
        "FlextQualityScheduledMaintenance": "flext_quality.docs",
        "FlextQualityServiceBase": "flext_quality",
        "FlextQualitySettings": "flext_quality",
        "FlextQualityStyleValidator": "flext_quality.docs.tools",
        "FlextQualityTypes": "flext_quality",
        "FlextQualityUtilities": "flext_quality",
        "FlextQualityValidators": "flext_quality.rules",
        "FlextQualityVersion": "flext_quality",
        "TestsFlextQualityConstants": ".constants",
        "TestsFlextQualityModels": ".models",
        "TestsFlextQualityProtocols": ".protocols",
        "TestsFlextQualityServiceBase": ".base",
        "TestsFlextQualitySettings": ".settings",
        "TestsFlextQualityTypes": ".typings",
        "TestsFlextQualityUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_quality",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_quality",
        "p": ".protocols",
        "quality": "flext_quality",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_quality",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
