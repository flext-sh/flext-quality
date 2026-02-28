"""MCP tools for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping

from flext_quality import c, t
from flext_quality.hooks.manager import HookManager
from flext_quality.integrations.claude_context import FlextQualityClaudeContextClient
from flext_quality.integrations.claude_mem import FlextQualityClaudeMemClient
from flext_quality.mcp.server import mcp
from flext_quality.rules.engine import FlextQualityRulesEngine


@mcp.tool()
def search_memory(
    query: str,
    *,
    search_type: str = "observations",
    limit: int | None = None,
) -> Mapping[str, object]:
    """Build command to search cross-session memory via claude-mem.

    Returns the mcp-cli command that can be used to execute the search.
    The actual execution is left to the caller for security.
    """
    client = FlextQualityClaudeMemClient()
    search_limit = limit or c.Quality.Defaults.DEFAULT_MEMORY_SEARCH_LIMIT
    result = client.build_search_call(query=query, limit=search_limit)
    if result.is_failure:
        return {"error": result.error}

    command_result = client.get_search_command(query=query, limit=search_limit)
    if command_result.is_failure:
        return {"error": command_result.error}

    params = dict(result.value.params)
    params["search_type"] = search_type

    return {
        "server": result.value.server,
        "tool": result.value.tool,
        "params": params,
        "command": command_result.value,
    }


@mcp.tool()
def search_code(
    query: str,
    *,
    limit: int | None = None,
) -> Mapping[str, object]:
    """Build command for semantic code search via claude-context.

    Returns the mcp-cli command that can be used to execute the search.
    The actual execution is left to the caller for security.
    """
    client = FlextQualityClaudeContextClient()
    search_limit = limit or c.Quality.Defaults.DEFAULT_SEARCH_LIMIT
    result = client.build_search_call(query=query, limit=search_limit)
    if result.is_failure:
        return {"error": result.error}

    command_result = client.get_search_command(query=query, limit=search_limit)
    if command_result.is_failure:
        return {"error": command_result.error}

    return {
        "server": result.value.server,
        "tool": result.value.tool,
        "params": result.value.params,
        "command": command_result.value,
    }


@mcp.tool()
def execute_hook(
    event: str,
    input_data: t.Quality.HookInput,
) -> t.Quality.HookOutput:
    """Execute a hook manually."""
    manager = HookManager()
    result = manager.execute(event=event, input_data=input_data)
    if result.is_failure:
        return {"error": result.error}
    return result.value


@mcp.tool()
def validate_rules(
    path: str,
    *,
    context: Mapping[str, object] | None = None,
) -> Mapping[str, object]:
    """Validate code against YAML rules."""
    engine = FlextQualityRulesEngine()
    result = engine.validate(path=path, context=context)
    if result.is_failure:
        return {"error": result.error}
    return {"violations": result.value}
