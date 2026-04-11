# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_quality.test_api import (
        TestFlextQualityAPI,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
    )
    from flext_quality.test_basic import test_basic
    from flext_quality.test_cli import TestFlextQualityCliService, TestMainFunction
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": (
            "TestFlextQualityAPI",
            "TestFlextQualityHookExecution",
            "TestFlextQualityRulesConfig",
            "TestFlextQualitySingleton",
            "TestFlextQualityStdinProcessing",
            "TestFlextQualityValidation",
        ),
        ".test_basic": ("test_basic",),
        ".test_cli": (
            "TestFlextQualityCliService",
            "TestMainFunction",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "test_basic",
]
