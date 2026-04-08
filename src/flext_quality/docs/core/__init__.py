# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Core package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextQualityAuditRules": ".config_manager",
    "FlextQualityBaseAnalyzer": ".base_classes",
    "FlextQualityBaseAuditor": ".base_classes",
    "FlextQualityBaseReporter": ".base_classes",
    "FlextQualityBaseValidator": ".base_classes",
    "FlextQualityConfigManager": ".config_manager",
    "FlextQualityDocumentationFinder": ".file_discovery",
    "FlextQualityFileStatistics": ".file_discovery",
    "FlextQualityStyleGuide": ".config_manager",
    "FlextQualityValidationConfig": ".config_manager",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
