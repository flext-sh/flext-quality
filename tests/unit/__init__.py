# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import test_docs_auditor as test_docs_auditor
    from . import test_docs_config_manager as test_docs_config_manager
    from . import test_docs_entrypoints as test_docs_entrypoints
    from . import test_docs_link_checker as test_docs_link_checker
    from . import test_docs_notifier as test_docs_notifier
    from . import test_docs_optimizer as test_docs_optimizer
    from . import test_docs_readme as test_docs_readme
    from . import test_docs_reporter as test_docs_reporter
    from . import test_docs_scheduled_maintenance as test_docs_scheduled_maintenance
    from . import test_docs_style_validator as test_docs_style_validator
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_api import TestsFlextQualityApi
    from .test_basic import TestsFlextQualityBasic
    from .test_cli import TestsFlextQualityCli
    from .test_scheduled_maintenance_timeout import (
        TestsFlextQualityScheduledMaintenanceTimeout,
    )
__all__: tuple[str, ...] = (
    "TestsFlextQualityApi",
    "TestsFlextQualityBasic",
    "TestsFlextQualityCli",
    "TestsFlextQualityScheduledMaintenanceTimeout",
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
    "test_docs_auditor",
    "test_docs_config_manager",
    "test_docs_entrypoints",
    "test_docs_link_checker",
    "test_docs_notifier",
    "test_docs_optimizer",
    "test_docs_readme",
    "test_docs_reporter",
    "test_docs_scheduled_maintenance",
    "test_docs_style_validator",
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
            ".test_docs_auditor": ("test_docs_auditor",),
            ".test_docs_config_manager": ("test_docs_config_manager",),
            ".test_docs_entrypoints": ("test_docs_entrypoints",),
            ".test_docs_link_checker": ("test_docs_link_checker",),
            ".test_docs_notifier": ("test_docs_notifier",),
            ".test_docs_optimizer": ("test_docs_optimizer",),
            ".test_docs_readme": ("test_docs_readme",),
            ".test_docs_reporter": ("test_docs_reporter",),
            ".test_docs_scheduled_maintenance": ("test_docs_scheduled_maintenance",),
            ".test_docs_style_validator": ("test_docs_style_validator",),
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
