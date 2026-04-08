# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Core package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityAuditRules": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityAuditRules",
    ),
    "FlextQualityBaseAnalyzer": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAnalyzer",
    ),
    "FlextQualityBaseAuditor": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseAuditor",
    ),
    "FlextQualityBaseReporter": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseReporter",
    ),
    "FlextQualityBaseValidator": (
        "flext_quality.docs.core.base_classes",
        "FlextQualityBaseValidator",
    ),
    "FlextQualityConfigManager": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityConfigManager",
    ),
    "FlextQualityDocumentationFinder": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityDocumentationFinder",
    ),
    "FlextQualityFileStatistics": (
        "flext_quality.docs.core.file_discovery",
        "FlextQualityFileStatistics",
    ),
    "FlextQualityStyleGuide": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityStyleGuide",
    ),
    "FlextQualityValidationConfig": (
        "flext_quality.docs.core.config_manager",
        "FlextQualityValidationConfig",
    ),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
