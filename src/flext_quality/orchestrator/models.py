"""Compatibility wrapper for orchestrator models.

DEPRECATED: Import from flext_quality._models.plugin instead.

This module provides backwards compatibility for code that imports:
    from flext_quality.orchestrator.models import PluginCategory, ...

Migration path:
    from flext_quality._models.plugin import FlextQualityPlugin
    Category = FlextQualityPlugin.Category
    Metadata = FlextQualityPlugin.Metadata
    Violation = FlextQualityPlugin.Violation
    ValidationResult = FlextQualityPlugin.ValidationResult
"""
from __future__ import annotations

import warnings

from flext_quality._models.plugin import FlextQualityPlugin

# Emit deprecation warning on import
warnings.warn(
    "flext_quality.orchestrator.models is deprecated. "
    "Use flext_quality._models.plugin.FlextQualityPlugin instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Aliases for backwards compatibility
PluginCategory = FlextQualityPlugin.Category
PluginMetadata = FlextQualityPlugin.Metadata
Violation = FlextQualityPlugin.Violation
ValidationResult = FlextQualityPlugin.ValidationResult

__all__ = [
    "PluginCategory",
    "PluginMetadata",
    "Violation",
    "ValidationResult",
]
