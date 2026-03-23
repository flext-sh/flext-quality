# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Quality Documentation Maintenance - Core Components.

Shared base classes and utilities for the maintenance system.
Provides common interfaces and functionality for documentation analysis,
reporting, and validation operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs.core.base_classes import (
        BaseAnalyzer,
        BaseAuditor,
        BaseReporter,
        BaseValidator,
        Config,
    )
    from flext_quality.docs.core.config_manager import (
        AuditRules,
        ConfigData,
        ConfigManager,
        ConfigPrimitive,
        ConfigSection,
        ConfigValue,
        RawConfigMap,
        RawSectionMap,
        RawSectionValue,
        StyleGuide,
        ValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        DocumentationFinder,
        FileStatistics,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AuditRules": ("flext_quality.docs.core.config_manager", "AuditRules"),
    "BaseAnalyzer": ("flext_quality.docs.core.base_classes", "BaseAnalyzer"),
    "BaseAuditor": ("flext_quality.docs.core.base_classes", "BaseAuditor"),
    "BaseReporter": ("flext_quality.docs.core.base_classes", "BaseReporter"),
    "BaseValidator": ("flext_quality.docs.core.base_classes", "BaseValidator"),
    "Config": ("flext_quality.docs.core.base_classes", "Config"),
    "ConfigData": ("flext_quality.docs.core.config_manager", "ConfigData"),
    "ConfigManager": ("flext_quality.docs.core.config_manager", "ConfigManager"),
    "ConfigPrimitive": ("flext_quality.docs.core.config_manager", "ConfigPrimitive"),
    "ConfigSection": ("flext_quality.docs.core.config_manager", "ConfigSection"),
    "ConfigValue": ("flext_quality.docs.core.config_manager", "ConfigValue"),
    "DocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "DocumentationFinder",
    ),
    "FileStatistics": ("flext_quality.docs.core.file_discovery", "FileStatistics"),
    "RawConfigMap": ("flext_quality.docs.core.config_manager", "RawConfigMap"),
    "RawSectionMap": ("flext_quality.docs.core.config_manager", "RawSectionMap"),
    "RawSectionValue": ("flext_quality.docs.core.config_manager", "RawSectionValue"),
    "StyleGuide": ("flext_quality.docs.core.config_manager", "StyleGuide"),
    "ValidationConfig": ("flext_quality.docs.core.config_manager", "ValidationConfig"),
}

__all__ = [
    "AuditRules",
    "BaseAnalyzer",
    "BaseAuditor",
    "BaseReporter",
    "BaseValidator",
    "Config",
    "ConfigData",
    "ConfigManager",
    "ConfigPrimitive",
    "ConfigSection",
    "ConfigValue",
    "DocumentationFinder",
    "FileStatistics",
    "RawConfigMap",
    "RawSectionMap",
    "RawSectionValue",
    "StyleGuide",
    "ValidationConfig",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
