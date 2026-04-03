# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.constants import FlextConstants as c
from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports
from flext_core.mixins import FlextMixins as x
from flext_core.models import FlextModels as m
from flext_core.protocols import FlextProtocols as p
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_core.typings import FlextTypes as t
from flext_core.utilities import FlextUtilities as u
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

if _t.TYPE_CHECKING:
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_cli as _tests_unit_test_cli

    test_cli = _tests_unit_test_cli

    _ = (
        TestFlextQualityAPI,
        TestFlextQualityCliService,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
        TestMainFunction,
        c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        t,
        test_api,
        test_basic,
        test_cli,
        u,
        x,
    )
_LAZY_IMPORTS = {
    "TestFlextQualityAPI": "tests.unit.test_api",
    "TestFlextQualityCliService": "tests.unit.test_cli",
    "TestFlextQualityHookExecution": "tests.unit.test_api",
    "TestFlextQualityRulesConfig": "tests.unit.test_api",
    "TestFlextQualitySingleton": "tests.unit.test_api",
    "TestFlextQualityStdinProcessing": "tests.unit.test_api",
    "TestFlextQualityValidation": "tests.unit.test_api",
    "TestMainFunction": "tests.unit.test_cli",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_api": "tests.unit.test_api",
    "test_basic": "tests.unit.test_basic",
    "test_cli": "tests.unit.test_cli",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "test_api",
    "test_basic",
    "test_cli",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
