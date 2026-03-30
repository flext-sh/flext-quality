# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit tests for flext-quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import test_api as test_api, test_cli as test_cli
    from tests.unit.test_api import (
        TestFlextQualityAPI as TestFlextQualityAPI,
        TestFlextQualityHookExecution as TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig as TestFlextQualityRulesConfig,
        TestFlextQualitySingleton as TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing as TestFlextQualityStdinProcessing,
        TestFlextQualityValidation as TestFlextQualityValidation,
    )
    from tests.unit.test_basic import test_basic as test_basic
    from tests.unit.test_cli import (
        TestFlextQualityCliService as TestFlextQualityCliService,
        TestMainFunction as TestMainFunction,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestFlextQualityAPI": ["tests.unit.test_api", "TestFlextQualityAPI"],
    "TestFlextQualityCliService": ["tests.unit.test_cli", "TestFlextQualityCliService"],
    "TestFlextQualityHookExecution": [
        "tests.unit.test_api",
        "TestFlextQualityHookExecution",
    ],
    "TestFlextQualityRulesConfig": [
        "tests.unit.test_api",
        "TestFlextQualityRulesConfig",
    ],
    "TestFlextQualitySingleton": ["tests.unit.test_api", "TestFlextQualitySingleton"],
    "TestFlextQualityStdinProcessing": [
        "tests.unit.test_api",
        "TestFlextQualityStdinProcessing",
    ],
    "TestFlextQualityValidation": ["tests.unit.test_api", "TestFlextQualityValidation"],
    "TestMainFunction": ["tests.unit.test_cli", "TestMainFunction"],
    "test_api": ["tests.unit.test_api", ""],
    "test_basic": ["tests.unit.test_basic", "test_basic"],
    "test_cli": ["tests.unit.test_cli", ""],
}

_EXPORTS: Sequence[str] = [
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "test_api",
    "test_basic",
    "test_cli",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
