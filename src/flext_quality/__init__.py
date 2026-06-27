# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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

if _t.TYPE_CHECKING:
    from flext_web import d as d, e as e, h as h, r as r, x as x

    from flext_quality.api import FlextQuality as FlextQuality, quality as quality
    from flext_quality.base import (
        FlextQualityServiceBase as FlextQualityServiceBase,
        s as s,
    )
    from flext_quality.cli import FlextQualityCli as FlextQualityCli, main as main
    from flext_quality.constants import (
        FlextQualityConstants as FlextQualityConstants,
        c as c,
    )
    from flext_quality.docs.core.config_manager import (
        FlextQualityAuditRules as FlextQualityAuditRules,
        FlextQualityConfigManager as FlextQualityConfigManager,
        FlextQualityConfigTypes as FlextQualityConfigTypes,
        FlextQualityStyleGuide as FlextQualityStyleGuide,
        FlextQualityValidationSettings as FlextQualityValidationSettings,
    )
    from flext_quality.docs.dashboard import (
        FlextQualityDocumentationDashboard as FlextQualityDocumentationDashboard,
    )
    from flext_quality.docs.notifications import (
        FlextQualityDocumentationNotifier as FlextQualityDocumentationNotifier,
    )
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance as FlextQualityScheduledMaintenance,
    )
    from flext_quality.docs.scripts.audit import (
        FlextQualityDocumentationAuditor as FlextQualityDocumentationAuditor,
    )
    from flext_quality.docs.scripts.optimize import (
        FlextQualityDocumentationOptimizer as FlextQualityDocumentationOptimizer,
    )
    from flext_quality.docs.scripts.report import (
        FlextQualityDocumentationReporter as FlextQualityDocumentationReporter,
    )
    from flext_quality.docs.scripts.validate import (
        FlextQualityContentValidator as FlextQualityContentValidator,
        FlextQualityDocumentationValidator as FlextQualityDocumentationValidator,
        FlextQualityLinkValidator as FlextQualityLinkValidator,
    )
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker as FlextQualityLinkChecker,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator as FlextQualityStyleValidator,
    )
    from flext_quality.hooks.base import FlextQualityBaseHook as FlextQualityBaseHook
    from flext_quality.hooks.manager import (
        FlextQualityHookManager as FlextQualityHookManager,
    )
    from flext_quality.integrations.claude_context import (
        FlextQualityClaudeContextClient as FlextQualityClaudeContextClient,
    )
    from flext_quality.integrations.claude_mem import (
        FlextQualityClaudeMemClient as FlextQualityClaudeMemClient,
    )
    from flext_quality.integrations.code_execution import (
        FlextQualityCodeExecutionBridge as FlextQualityCodeExecutionBridge,
    )
    from flext_quality.integrations.mcp_client import (
        FlextQualityMcpClient as FlextQualityMcpClient,
    )
    from flext_quality.mcp.server import get_server as get_server
    from flext_quality.models import FlextQualityModels as FlextQualityModels, m as m
    from flext_quality.protocols import (
        FlextQualityProtocols as FlextQualityProtocols,
        p as p,
    )
    from flext_quality.rules.engine import (
        FlextQualityRulesEngine as FlextQualityRulesEngine,
    )
    from flext_quality.rules.loader import (
        FlextQualityRulesLoader as FlextQualityRulesLoader,
    )
    from flext_quality.rules.validators import (
        FlextQualityValidators as FlextQualityValidators,
    )
    from flext_quality.settings import FlextQualitySettings as FlextQualitySettings
    from flext_quality.typings import FlextQualityTypes as FlextQualityTypes, t as t
    from flext_quality.utilities import (
        FlextQualityUtilities as FlextQualityUtilities,
        u as u,
    )
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
                "FlextQualityConfigTypes",
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
                "FlextQualityDocumentationValidator",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)

__all__: list[str] = [
    "FlextQuality",
    "FlextQualityAuditRules",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConfigManager",
    "FlextQualityConfigTypes",
    "FlextQualityConstants",
    "FlextQualityContentValidator",
    "FlextQualityDocumentationAuditor",
    "FlextQualityDocumentationDashboard",
    "FlextQualityDocumentationNotifier",
    "FlextQualityDocumentationOptimizer",
    "FlextQualityDocumentationReporter",
    "FlextQualityDocumentationValidator",
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
