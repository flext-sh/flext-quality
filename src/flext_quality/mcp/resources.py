"""MCP resources for flext-quality."""

from __future__ import annotations

import json

from flext_quality import c
from flext_quality.hooks.manager import HookManager
from flext_quality.integrations.claude_context import FlextQualityClaudeContextClient
from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
from flext_quality.mcp.server import mcp
from flext_quality.rules.engine import FlextQualityRulesEngine


@mcp.resource("config://hooks")
def get_hooks_config() -> str:
    """Get current hooks configuration."""
    manager = HookManager()
    config = manager.get_config()
    return json.dumps(config, indent=c.Quality.Defaults.JSON_INDENT)


@mcp.resource("config://rules")
def get_rules_config() -> str:
    """Get current rules configuration."""
    engine = FlextQualityRulesEngine()
    rules = engine.get_rules()
    return json.dumps(
        [rule.model_dump() for rule in rules],
        indent=c.Quality.Defaults.JSON_INDENT,
    )


@mcp.resource("status://integrations")
def get_integrations_status() -> str:
    """Get status of all integrations."""
    status: dict[str, object] = {}

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

    return json.dumps(status, indent=c.Quality.Defaults.JSON_INDENT)
