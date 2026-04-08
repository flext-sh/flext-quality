# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import flext_quality.api as _flext_quality_api

    api = _flext_quality_api
    import flext_quality.constants as _flext_quality_constants
    from flext_quality.api import FlextQuality

    constants = _flext_quality_constants
    import flext_quality.docs as _flext_quality_docs
    from flext_quality.constants import (
        FlextQualityConstants,
        FlextQualityConstants as c,
    )

    docs = _flext_quality_docs
    import flext_quality.hooks as _flext_quality_hooks
    from flext_quality.docs import (
        FlextQualityDocumentationDashboard,
        FlextQualityDocumentationNotifier,
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.core import (
        FlextQualityAuditRules,
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
        FlextQualityConfigManager,
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
    )
    from flext_quality.docs.scripts import (
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
    )
    from flext_quality.docs.tools import (
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_file_content,
        analyze_files_content,
        validate_file_style,
        validate_files_style,
        validate_links_sync,
    )

    hooks = _flext_quality_hooks
    import flext_quality.integrations as _flext_quality_integrations
    from flext_quality.hooks import FlextQualityBaseHook, FlextQualityHookManager

    integrations = _flext_quality_integrations
    import flext_quality.mcp as _flext_quality_mcp
    from flext_quality.integrations import (
        FlextQualityClaudeContextClient,
        FlextQualityClaudeMemClient,
        FlextQualityCodeExecutionBridge,
        FlextQualityMcpClient,
    )

    mcp = _flext_quality_mcp
    import flext_quality.models as _flext_quality_models
    from flext_quality.mcp import (
        execute_hook,
        get_hooks_config,
        get_integrations_status,
        get_rules_config,
        get_server,
        search_code,
        search_memory,
        validate_rules,
    )

    models = _flext_quality_models
    import flext_quality.protocols as _flext_quality_protocols
    from flext_quality.models import FlextQualityModels, FlextQualityModels as m

    protocols = _flext_quality_protocols
    import flext_quality.rules as _flext_quality_rules
    from flext_quality.protocols import (
        FlextQualityProtocols,
        FlextQualityProtocols as p,
    )

    rules = _flext_quality_rules
    import flext_quality.services as _flext_quality_services
    from flext_quality.rules import (
        FlextQualityRulesEngine,
        FlextQualityRulesLoader,
        FlextQualityValidators,
    )

    services = _flext_quality_services
    import flext_quality.settings as _flext_quality_settings
    from flext_quality.services import FlextQualityCliService

    settings = _flext_quality_settings
    import flext_quality.typings as _flext_quality_typings
    from flext_quality.settings import FlextQualitySettings

    typings = _flext_quality_typings
    import flext_quality.utilities as _flext_quality_utilities
    from flext_quality.typings import FlextQualityTypes, FlextQualityTypes as t

    utilities = _flext_quality_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality.utilities import (
        FlextQualityUtilities,
        FlextQualityUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_quality.docs",
        "flext_quality.hooks",
        "flext_quality.integrations",
        "flext_quality.mcp",
        "flext_quality.rules",
        "flext_quality.services",
    ),
    {
        "FlextQuality": ("flext_quality.api", "FlextQuality"),
        "FlextQualityConstants": ("flext_quality.constants", "FlextQualityConstants"),
        "FlextQualityModels": ("flext_quality.models", "FlextQualityModels"),
        "FlextQualityProtocols": ("flext_quality.protocols", "FlextQualityProtocols"),
        "FlextQualitySettings": ("flext_quality.settings", "FlextQualitySettings"),
        "FlextQualityTypes": ("flext_quality.typings", "FlextQualityTypes"),
        "FlextQualityUtilities": ("flext_quality.utilities", "FlextQualityUtilities"),
        "api": "flext_quality.api",
        "c": ("flext_quality.constants", "FlextQualityConstants"),
        "constants": "flext_quality.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docs": "flext_quality.docs",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "hooks": "flext_quality.hooks",
        "integrations": "flext_quality.integrations",
        "m": ("flext_quality.models", "FlextQualityModels"),
        "mcp": "flext_quality.mcp",
        "models": "flext_quality.models",
        "p": ("flext_quality.protocols", "FlextQualityProtocols"),
        "protocols": "flext_quality.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "rules": "flext_quality.rules",
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_quality.services",
        "settings": "flext_quality.settings",
        "t": ("flext_quality.typings", "FlextQualityTypes"),
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityUtilities"),
        "utilities": "flext_quality.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "FlextQuality",
    "FlextQualityAuditRules",
    "FlextQualityBaseAnalyzer",
    "FlextQualityBaseAuditor",
    "FlextQualityBaseHook",
    "FlextQualityBaseReporter",
    "FlextQualityBaseValidator",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCliService",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfigManager",
    "FlextQualityConstants",
    "FlextQualityContentAnalyzer",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationFinder",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityFileStatistics",
    "FlextQualityHookManager",
    "FlextQualityLinkChecker",
    "FlextQualityLinkValidator",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityScheduledMaintenance",
    "FlextQualitySettings",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityValidationConfig",
    "FlextQualityValidators",
    "analyze_file_content",
    "analyze_files_content",
    "api",
    "c",
    "constants",
    "d",
    "docs",
    "e",
    "execute_hook",
    "get_hooks_config",
    "get_integrations_status",
    "get_rules_config",
    "get_server",
    "h",
    "hooks",
    "integrations",
    "m",
    "mcp",
    "models",
    "p",
    "protocols",
    "r",
    "rules",
    "s",
    "search_code",
    "search_memory",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "validate_file_style",
    "validate_files_style",
    "validate_links_sync",
    "validate_rules",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
