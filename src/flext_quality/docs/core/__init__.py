# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Quality Documentation Maintenance - Core Components.

Shared base classes and utilities for the maintenance system.
Provides common interfaces and functionality for documentation analysis,
reporting, and validation operations.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.docs.core import base_classes, config_manager, file_discovery
    from flext_quality.docs.core.base_classes import (
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityAuditRules": "flext_quality.docs.core.config_manager",
    "FlextQualityBaseAnalyzer": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseAuditor": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseReporter": "flext_quality.docs.core.base_classes",
    "FlextQualityBaseValidator": "flext_quality.docs.core.base_classes",
    "FlextQualityConfigManager": "flext_quality.docs.core.config_manager",
    "FlextQualityDocumentationFinder": "flext_quality.docs.core.file_discovery",
    "FlextQualityFileStatistics": "flext_quality.docs.core.file_discovery",
    "FlextQualityStyleGuide": "flext_quality.docs.core.config_manager",
    "FlextQualityValidationConfig": "flext_quality.docs.core.config_manager",
    "base_classes": "flext_quality.docs.core.base_classes",
    "config_manager": "flext_quality.docs.core.config_manager",
    "file_discovery": "flext_quality.docs.core.file_discovery",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
