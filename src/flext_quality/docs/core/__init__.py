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
    from flext_core.typings import FlextTypes

    from flext_quality.docs.core.base_classes import (
        BaseAnalyzer,
        BaseAuditor,
        BaseReporter,
        BaseValidator,
        Config,
    )
    from flext_quality.docs.core.config_manager import (
        AuditRules,
        ConfigManager,
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
    "ConfigManager": ("flext_quality.docs.core.config_manager", "ConfigManager"),
    "DocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "DocumentationFinder",
    ),
    "FileStatistics": ("flext_quality.docs.core.file_discovery", "FileStatistics"),
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
    "ConfigManager",
    "DocumentationFinder",
    "FileStatistics",
    "StyleGuide",
    "ValidationConfig",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
