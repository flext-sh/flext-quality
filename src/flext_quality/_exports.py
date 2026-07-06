# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
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
        ".docs": ("docs",),
        ".hooks": ("hooks",),
        ".hooks.base": ("FlextQualityBaseHook",),
        ".hooks.manager": ("FlextQualityHookManager",),
        ".integrations": ("integrations",),
        ".integrations.claude_context": ("FlextQualityClaudeContextClient",),
        ".integrations.claude_mem": ("FlextQualityClaudeMemClient",),
        ".integrations.code_execution": ("FlextQualityCodeExecutionBridge",),
        ".integrations.mcp_client": ("FlextQualityMcpClient",),
        ".mcp": ("mcp",),
        ".mcp.resources": ("FlextQualityMcpResources",),
        ".mcp.server": ("FlextQualityMcpServer",),
        ".mcp.tools": ("FlextQualityMcpTools",),
        ".models": (
            "FlextQualityModels",
            "m",
        ),
        ".protocols": (
            "FlextQualityProtocols",
            "p",
        ),
        ".rules": ("rules",),
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
        "flext_infra": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

FLEXT_QUALITY_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".hooks",
        ".integrations",
        ".mcp",
        ".rules",
    ),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="flext_quality",
)

__all__: list[str] = ["FLEXT_QUALITY_LAZY_IMPORTS"]
