# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_web import d, e, h, r, x

    from flext_quality.__version__ import (
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_quality.api import FlextQuality, quality
    from flext_quality.base import FlextQualityServiceBase, s
    from flext_quality.cli import FlextQualityCli, main
    from flext_quality.constants import FlextQualityConstants, c
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules,
        FlextQualityConfigManager,
        FlextQualityStyleGuide,
        FlextQualityValidationSettings,
    )
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import FlextQualityDocumentationNotifier
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor
    from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer
    from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator,
        FlextQualityLinkValidator,
    )
    from flext_quality.docs.tools.link_checker import FlextQualityLinkChecker
    from flext_quality.docs.tools.style_validator import FlextQualityStyleValidator
    from flext_quality.hooks.base import FlextQualityBaseHook
    from flext_quality.hooks.manager import FlextQualityHookManager
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import FlextQualityMcpClient
    from flext_quality.mcp.server import get_server
    from flext_quality.models import FlextQualityModels, m
    from flext_quality.protocols import FlextQualityProtocols, p
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators
    from flext_quality.settings import FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes, t
    from flext_quality.utilities import FlextQualityUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".docs",
        ".hooks",
        ".integrations",
        ".mcp",
        ".rules",
    ),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".api": (
                "FlextQuality",
                "quality",
            ),
            ".base": (
                "FlextQualityServiceBase",
                "s",
            ),
            ".cli": (
                "FlextQualityCli",
                "main",
            ),
            ".constants": (
                "FlextQualityConstants",
                "c",
            ),
            ".docs.core.config_manager": (
                "FlextQualityAuditRules",
                "FlextQualityConfigManager",
                "FlextQualityStyleGuide",
                "FlextQualityValidationSettings",
            ),
            ".docs.dashboard": ("FlextQualityDocumentationDashboard",),
            ".docs.notifications": ("FlextQualityDocumentationNotifier",),
            ".docs.scheduled_maintenance": ("FlextQualityScheduledMaintenance",),
            ".docs.scripts.audit": ("FlextQualityDocumentationAuditor",),
            ".docs.scripts.optimize": ("FlextQualityDocumentationOptimizer",),
            ".docs.scripts.report": ("FlextQualityDocumentationReporter",),
            ".docs.scripts.validate": (
                "FlextQualityContentValidator",
                "FlextQualityLinkValidator",
            ),
            ".docs.tools.link_checker": ("FlextQualityLinkChecker",),
            ".docs.tools.style_validator": ("FlextQualityStyleValidator",),
            ".hooks.base": ("FlextQualityBaseHook",),
            ".hooks.manager": ("FlextQualityHookManager",),
            ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
            ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
            ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
            ".integrations.mcp_client": ("FlextQualityMcpClient",),
            ".mcp.server": ("get_server",),
            ".models": (
                "FlextQualityModels",
                "m",
            ),
            ".protocols": (
                "FlextQualityProtocols",
                "p",
            ),
            ".rules.engine": ("FlextQualityRulesEngine",),
            ".rules.loader": ("FlextQualityRulesLoader",),
            ".rules.validators": ("FlextQualityValidators",),
            ".settings": ("FlextQualitySettings",),
            ".typings": (
                "FlextQualityTypes",
                "t",
            ),
            ".utilities": (
                "FlextQualityUtilities",
                "u",
            ),
            "flext_web": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextQuality",
    "FlextQualityAuditRules",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfigManager",
    "FlextQualityConstants",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityHookManager",
    "FlextQualityLinkChecker",
    "FlextQualityLinkValidator",
    "FlextQualityMcpClient",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityScheduledMaintenance",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityStyleGuide",
    "FlextQualityStyleValidator",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "FlextQualityValidationSettings",
    "FlextQualityValidators",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "get_server",
    "h",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "t",
    "u",
    "x",
]
