"""MCP resources for flext-quality."""

from __future__ import annotations

from flext_quality import (
    FlextQualityClaudeContextClient,
    FlextQualityClaudeMemClient,
    FlextQualityHookManager,
    FlextQualityRulesEngine,
    c,
    get_server as _get_server,
    t,
    u,
)

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
    status: dict[str, t.JsonValue] = {}
    mem_client = FlextQualityClaudeMemClient()
    mem_health = mem_client.health_check()
    mem_status: t.JsonValue = (
        u.Cli.normalize_json_value(mem_health.value)
        if mem_health.success
        else {"error": mem_health.error}
    )
    status["claude_mem"] = mem_status
    ctx_client = FlextQualityClaudeContextClient()
    ctx_health = ctx_client.health_check()
    ctx_status: t.JsonValue = (
        u.Cli.normalize_json_value(ctx_health.value)
        if ctx_health.success
        else {"error": ctx_health.error}
    )
    status["claude_context"] = ctx_status
    return t.CONTAINER_MAPPING_ADAPTER.dump_json(
        status,
        indent=c.Quality.Defaults.JSON_INDENT,
    ).decode("utf-8")
