"""MCP resources for flext-quality."""

from __future__ import annotations

from collections.abc import MutableMapping

from flext_quality import (
    FlextQualityClaudeContextClient,
    FlextQualityClaudeMemClient,
    FlextQualityHookManager,
    FlextQualityRulesEngine,
    c,
    t,
)
from flext_quality.mcp.server import get_server as _get_server

_mcp = _get_server()


@_mcp.resource("settings://hooks")
def get_hooks_config() -> str:
    """Get current hooks configuration."""
    manager = FlextQualityHookManager()
    settings = manager.get_config()
    return t.CONTAINER_MAPPING_ADAPTER.dump_json(
        dict(settings),
        indent=c.Quality.Defaults.JSON_INDENT,
    ).decode("utf-8")


@_mcp.resource("settings://rules")
def get_rules_config() -> str:
    """Get current rules configuration."""
    engine = FlextQualityRulesEngine()
    rules = engine.get_rules()
    return t.CONTAINER_MAPPING_SEQUENCE_ADAPTER.dump_json(
        [rule.model_dump() for rule in rules],
        indent=c.Quality.Defaults.JSON_INDENT,
    ).decode("utf-8")


@_mcp.resource("status://integrations")
def get_integrations_status() -> str:
    """Get status of all integrations."""
    status: MutableMapping[str, t.Container | t.ContainerMapping] = {}
    mem_client = FlextQualityClaudeMemClient()
    mem_health = mem_client.health_check()
    status["claude_mem"] = (
        mem_health.value if mem_health.success else {"error": mem_health.error}
    )
    ctx_client = FlextQualityClaudeContextClient()
    ctx_health = ctx_client.health_check()
    status["claude_context"] = (
        ctx_health.value if ctx_health.success else {"error": ctx_health.error}
    )
    return t.CONTAINER_MAPPING_ADAPTER.dump_json(
        status,
        indent=c.Quality.Defaults.JSON_INDENT,
    ).decode("utf-8")
