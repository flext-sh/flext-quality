# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_api import TestsFlextQualityApi
    from .test_basic import TestsFlextQualityBasic
    from .test_cli import TestsFlextQualityCli
    from .test_code_execution import TestsFlextQualityCodeExecutionBridge
    from .test_docs_config_manager import TestsFlextQualityConfigManager
    from .test_docs_dashboard import TestsFlextQualityDocumentationDashboard
    from .test_docs_notifications import TestsFlextQualityDocumentationNotifier
    from .test_hooks import TestsFlextQualityBaseHook, TestsFlextQualityHookManager
    from .test_integrations import TestsFlextQualityIntegrations
    from .test_mcp_layer import (
        TestsFlextQualityMcpResources,
        TestsFlextQualityMcpServer,
        TestsFlextQualityMcpTools,
    )
    from .test_rules_engine_validators import (
        TestsFlextQualityRulesEngine,
        TestsFlextQualityRulesLoader,
        TestsFlextQualityValidators,
    )
    from .test_scheduled_maintenance_timeout import (
        TestsFlextQualityScheduledMaintenanceTimeout,
    )
__all__: tuple[str, ...] = (
    "TestsFlextQualityApi",
    "TestsFlextQualityBaseHook",
    "TestsFlextQualityBasic",
    "TestsFlextQualityCli",
    "TestsFlextQualityCodeExecutionBridge",
    "TestsFlextQualityConfigManager",
    "TestsFlextQualityDocumentationDashboard",
    "TestsFlextQualityDocumentationNotifier",
    "TestsFlextQualityHookManager",
    "TestsFlextQualityIntegrations",
    "TestsFlextQualityMcpResources",
    "TestsFlextQualityMcpServer",
    "TestsFlextQualityMcpTools",
    "TestsFlextQualityRulesEngine",
    "TestsFlextQualityRulesLoader",
    "TestsFlextQualityScheduledMaintenanceTimeout",
    "TestsFlextQualityValidators",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_api": ("TestsFlextQualityApi",),
            ".test_basic": ("TestsFlextQualityBasic",),
            ".test_cli": ("TestsFlextQualityCli",),
            ".test_code_execution": ("TestsFlextQualityCodeExecutionBridge",),
            ".test_docs_config_manager": ("TestsFlextQualityConfigManager",),
            ".test_docs_dashboard": ("TestsFlextQualityDocumentationDashboard",),
            ".test_docs_notifications": ("TestsFlextQualityDocumentationNotifier",),
            ".test_hooks": (
                "TestsFlextQualityBaseHook",
                "TestsFlextQualityHookManager",
            ),
            ".test_integrations": ("TestsFlextQualityIntegrations",),
            ".test_mcp_layer": (
                "TestsFlextQualityMcpResources",
                "TestsFlextQualityMcpServer",
                "TestsFlextQualityMcpTools",
            ),
            ".test_rules_engine_validators": (
                "TestsFlextQualityRulesEngine",
                "TestsFlextQualityRulesLoader",
                "TestsFlextQualityValidators",
            ),
            ".test_scheduled_maintenance_timeout": (
                "TestsFlextQualityScheduledMaintenanceTimeout",
            ),
            "flext_tests": (
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "t",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
