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
    settings = manager.fetch_config()
    config_json: str = t.Quality.CONTAINER_MAPPING_ADAPTER.dump_json(
        dict(settings),
        indent=c.Quality.JSON_INDENT,
    ).decode("utf-8")
    return config_json


@_mcp.resource("settings://rules")
def get_rules_config() -> str:
    """Get current rules configuration."""
    engine = FlextQualityRulesEngine()
    rules = engine.get_rules()
    rules_json: str = t.Quality.CONTAINER_MAPPING_SEQUENCE_ADAPTER.dump_json(
        [rule.model_dump() for rule in rules],
        indent=c.Quality.JSON_INDENT,
    ).decode("utf-8")
    return rules_json


@_mcp.resource("status://integrations")
def get_integrations_status() -> str:
    """Get status of all integrations."""
    mem_client = FlextQualityClaudeMemClient()
    mem_health = mem_client.health_check()
    mem_status = (
        u.normalize_to_json_value(mem_health.value)
        if mem_health.success
        else u.normalize_to_json_value({"error": mem_health.error})
    )
    ctx_client = FlextQualityClaudeContextClient()
    ctx_health = ctx_client.health_check()
    ctx_status = (
        u.normalize_to_json_value(ctx_health.value)
        if ctx_health.success
        else u.normalize_to_json_value({"error": ctx_health.error})
    )
    status = {
        "claude_mem": mem_status,
        "claude_context": ctx_status,
    }
    status_json: str = t.Quality.CONTAINER_MAPPING_ADAPTER.dump_json(
        status,
        indent=c.Quality.JSON_INDENT,
    ).decode("utf-8")
    return status_json
