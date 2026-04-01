# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit tests for flext-quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.unit.test_api import (
        TestFlextQualityAPI,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
    )
    from tests.unit.test_basic import test_basic
    from tests.unit.test_cli import TestFlextQualityCliService, TestMainFunction

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestFlextQualityAPI": "tests.unit.test_api",
    "TestFlextQualityCliService": "tests.unit.test_cli",
    "TestFlextQualityHookExecution": "tests.unit.test_api",
    "TestFlextQualityRulesConfig": "tests.unit.test_api",
    "TestFlextQualitySingleton": "tests.unit.test_api",
    "TestFlextQualityStdinProcessing": "tests.unit.test_api",
    "TestFlextQualityValidation": "tests.unit.test_api",
    "TestMainFunction": "tests.unit.test_cli",
    "test_api": "tests.unit.test_api",
    "test_basic": "tests.unit.test_basic",
    "test_cli": "tests.unit.test_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
