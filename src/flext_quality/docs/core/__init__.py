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
    "base_classes": "flext_quality.docs.core.base_classes",
    "c": ("flext_core.constants", "FlextConstants"),
    "config_manager": "flext_quality.docs.core.config_manager",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "file_discovery": "flext_quality.docs.core.file_discovery",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
