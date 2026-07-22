# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality package."""

from __future__ import annotations

from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x
    from flext_quality._settings import (
        FlextQualitySettings as FlextQualitySettings,
        settings as settings,
    )
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
    from flext_quality.mcp.resources import (
        FlextQualityMcpResources as FlextQualityMcpResources,
    )
    from flext_quality.mcp.server import FlextQualityMcpServer as FlextQualityMcpServer
    from flext_quality.mcp.tools import FlextQualityMcpTools as FlextQualityMcpTools
    from flext_quality.models import FlextQualityModels as FlextQualityModels, m as m
    from flext_quality.protocols import (
        FlextQualityProtocols as FlextQualityProtocols,
        p,
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
    from flext_quality.typings import FlextQualityTypes as FlextQualityTypes, t as t
    from flext_quality.utilities import (
        FlextQualityUtilities as FlextQualityUtilities,
        u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".hooks", ".integrations", ".mcp", ".rules"),
    build_lazy_import_map({
        "._settings": ("FlextQualitySettings", "settings"),
        ".api": ("FlextQuality", "quality"),
        ".base": ("FlextQualityServiceBase", "s"),
        ".cli": ("FlextQualityCli", "main"),
        ".constants": ("FlextQualityConstants", "c"),
        ".hooks.base": ("FlextQualityBaseHook",),
        ".hooks.manager": ("FlextQualityHookManager",),
        ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
        ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
        ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
        ".integrations.mcp_client": ("FlextQualityMcpClient",),
        ".mcp.resources": ("FlextQualityMcpResources",),
        ".mcp.server": ("FlextQualityMcpServer",),
        ".mcp.tools": ("FlextQualityMcpTools",),
        ".models": ("FlextQualityModels", "m"),
        ".protocols": ("FlextQualityProtocols", "p"),
        ".rules.engine": ("FlextQualityRulesEngine",),
        ".rules.loader": ("FlextQualityRulesLoader",),
        ".rules.validators": ("FlextQualityValidators",),
        ".typings": ("FlextQualityTypes", "t"),
        ".utilities": ("FlextQualityUtilities", "u"),
        "flext_infra": ("d", "e", "h", "r", "x"),
    }),
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


__all__: tuple[str, ...] = (
    "FlextQuality",
    "FlextQualityBaseHook",
    "FlextQualityClaudeContextClient",
    "FlextQualityClaudeMemClient",
    "FlextQualityCli",
    "FlextQualityCodeExecutionBridge",
    "FlextQualityConstants",
    "FlextQualityHookManager",
    "FlextQualityMcpClient",
    "FlextQualityMcpResources",
    "FlextQualityMcpServer",
    "FlextQualityMcpTools",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityServiceBase",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
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
    "h",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
