"""MCP resources for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence

from pydantic import TypeAdapter

from flext_quality import (
    FlextQualityClaudeContextClient,
    FlextQualityClaudeMemClient,
    FlextQualityRulesEngine,
    c,
    mcp,
    t,
)
from flext_quality.hooks.manager import FlextQualityHookManager


@mcp.resource("config://hooks")
def get_hooks_config() -> str:
    """Get current hooks configuration."""
    manager = FlextQualityHookManager()
    config = manager.get_config()
    return (
        TypeAdapter(Mapping[str, t.NormalizedValue])
        .dump_json(dict(config), indent=c.Quality.Defaults.JSON_INDENT)
        .decode("utf-8")
    )


@mcp.resource("config://rules")
def get_rules_config() -> str:
    """Get current rules configuration."""
    engine = FlextQualityRulesEngine()
    rules = engine.get_rules()
    return (
        TypeAdapter(Sequence[t.ContainerMapping])
        .dump_json(
            [rule.model_dump() for rule in rules],
            indent=c.Quality.Defaults.JSON_INDENT,
        )
        .decode("utf-8")
    )


@mcp.resource("status://integrations")
def get_integrations_status() -> str:
    """Get status of all integrations."""
    status: MutableMapping[str, t.Container | t.ContainerMapping] = {}
    mem_client = FlextQualityClaudeMemClient()
    mem_health = mem_client.health_check()
    status["claude_mem"] = (
        mem_health.value if mem_health.is_success else {"error": mem_health.error}
    )
    ctx_client = FlextQualityClaudeContextClient()
    ctx_health = ctx_client.health_check()
    status["claude_context"] = (
        ctx_health.value if ctx_health.is_success else {"error": ctx_health.error}
    )
    return (
        TypeAdapter(Mapping[str, t.NormalizedValue])
        .dump_json(status, indent=c.Quality.Defaults.JSON_INDENT)
        .decode("utf-8")
    )
