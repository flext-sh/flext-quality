# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Quality Documentation Maintenance - Core Components.

Shared base classes and utilities for the maintenance system.
Provides common interfaces and functionality for documentation analysis,
reporting, and validation operations.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
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
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        AuditRules,
        ConfigData,
        ConfigManager,
        ConfigPrimitive,
        ConfigSection,
        ConfigValue,
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
        RawConfigMap,
        RawSectionMap,
        RawSectionValue,
        StyleGuide,
        ValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        DocumentationFinder,
        FileStatistics,
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
    )

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
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
    "DocumentationFinder": ("flext_quality.docs.core.file_discovery", "DocumentationFinder"),
    "FileStatistics": ("flext_quality.docs.core.file_discovery", "FileStatistics"),
    "FlextQualityAuditRules": ("flext_quality.docs.core.config_manager", "FlextQualityAuditRules"),
    "FlextQualityBaseAnalyzer": ("flext_quality.docs.core.base_classes", "FlextQualityBaseAnalyzer"),
    "FlextQualityBaseAuditor": ("flext_quality.docs.core.base_classes", "FlextQualityBaseAuditor"),
    "FlextQualityBaseReporter": ("flext_quality.docs.core.base_classes", "FlextQualityBaseReporter"),
    "FlextQualityBaseValidator": ("flext_quality.docs.core.base_classes", "FlextQualityBaseValidator"),
    "FlextQualityConfigManager": ("flext_quality.docs.core.config_manager", "FlextQualityConfigManager"),
    "FlextQualityDocumentationFinder": ("flext_quality.docs.core.file_discovery", "FlextQualityDocumentationFinder"),
    "FlextQualityFileStatistics": ("flext_quality.docs.core.file_discovery", "FlextQualityFileStatistics"),
    "FlextQualityStyleGuide": ("flext_quality.docs.core.config_manager", "FlextQualityStyleGuide"),
    "FlextQualityValidationConfig": ("flext_quality.docs.core.config_manager", "FlextQualityValidationConfig"),
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
    "FlextQualityAuditRules",
    "FlextQualityBaseAnalyzer",
    "FlextQualityBaseAuditor",
    "FlextQualityBaseReporter",
    "FlextQualityBaseValidator",
    "FlextQualityConfigManager",
    "FlextQualityDocumentationFinder",
    "FlextQualityFileStatistics",
    "FlextQualityStyleGuide",
    "FlextQualityValidationConfig",
    "RawConfigMap",
    "RawSectionMap",
    "RawSectionValue",
    "StyleGuide",
    "ValidationConfig",
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
