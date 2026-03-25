# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit tests for flext-quality package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
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
    "test_basic": ["tests.unit.test_basic", "test_basic"],
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
    "test_basic",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
