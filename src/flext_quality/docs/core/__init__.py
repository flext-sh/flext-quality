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
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.core import (
        base_classes as base_classes,
        config_manager as config_manager,
        file_discovery as file_discovery,
    )
    from flext_quality.docs.core.base_classes import (
        FlextQualityBaseAnalyzer as FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor as FlextQualityBaseAuditor,
        FlextQualityBaseReporter as FlextQualityBaseReporter,
        FlextQualityBaseValidator as FlextQualityBaseValidator,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules as FlextQualityAuditRules,
        FlextQualityConfigManager as FlextQualityConfigManager,
        FlextQualityStyleGuide as FlextQualityStyleGuide,
        FlextQualityValidationConfig as FlextQualityValidationConfig,
    )
    from flext_quality.docs.core.file_discovery import (
        FlextQualityDocumentationFinder as FlextQualityDocumentationFinder,
        FlextQualityFileStatistics as FlextQualityFileStatistics,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityAuditRules": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityAuditRules",
    ],
    "FlextQualityBaseAnalyzer": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAnalyzer",
    ],
    "FlextQualityBaseAuditor": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAuditor",
    ],
    "FlextQualityBaseReporter": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ],
    "FlextQualityBaseValidator": [
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ],
    "FlextQualityConfigManager": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ],
    "FlextQualityDocumentationFinder": [
        "flext_quality.docs.core.file_discovery",
        "FlextQualityDocumentationFinder",
    ],
    "FlextQualityFileStatistics": [
        "flext_quality.docs.core.file_discovery",
        "FlextQualityFileStatistics",
    ],
    "FlextQualityStyleGuide": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ],
    "FlextQualityValidationConfig": [
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ],
    "base_classes": ["flext_quality.docs.core.base_classes", ""],
    "config_manager": ["flext_quality.docs.core.config_manager", ""],
    "file_discovery": ["flext_quality.docs.core.file_discovery", ""],
}

_EXPORTS: Sequence[str] = [
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
    "base_classes",
    "config_manager",
    "file_discovery",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
