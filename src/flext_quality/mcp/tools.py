"""MCP tools for flext-quality."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

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


@_mcp.tool()
def search_memory(
    query: str,
    *,
    search_type: str = "observations",
    limit: int | None = None,
) -> t.JsonMapping:
    """Build command to search cross-session memory via claude-mem.

    Returns the mcp-cli command that can be used to execute the search.
    The actual execution is left to the caller for security.
    """
    client = FlextQualityClaudeMemClient()
    search_limit = limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT
    result = client.build_search_call(query=query, limit=search_limit)
    if result.failure:
        return {"error": result.error}
    command_result = client.get_search_command(query=query, limit=search_limit)
    if command_result.failure:
        return {"error": command_result.error}
    params = u.normalize_to_json_value(result.value.params)
    command = u.normalize_to_json_value(command_result.value)
    return {
        "server": result.value.server,
        "tool": result.value.tool,
        "params": {**params, "search_type": search_type}
        if isinstance(params, Mapping)
        else {"search_type": search_type},
        "command": command,
    }


@_mcp.tool()
def search_code(
    query: str,
    *,
    limit: int | None = None,
) -> t.JsonMapping:
    """Build command for semantic code search via claude-context.

    Returns the mcp-cli command that can be used to execute the search.
    The actual execution is left to the caller for security.
    """
    client = FlextQualityClaudeContextClient()
    search_limit = limit or c.Quality.DEFAULT_SEARCH_LIMIT
    result = client.build_search_call(query=query, limit=search_limit)
    if result.failure:
        return {"error": result.error}
    command_result = client.get_search_command(query=query, limit=search_limit)
    if command_result.failure:
        return {"error": command_result.error}
    params = u.normalize_to_json_value(result.value.params)
    command = u.normalize_to_json_value(command_result.value)
    return {
        "server": result.value.server,
        "tool": result.value.tool,
        "params": params if isinstance(params, Mapping) else {},
        "command": command,
    }


@_mcp.tool()
def execute_hook(event: str, input_data: t.Quality.HookInput) -> t.Quality.HookOutput:
    """Execute a hook manually."""
    manager = FlextQualityHookManager()
    result = manager.execute(event=event, input_data=input_data)
    if result.failure:
        error_msg = result.error if result.error is not None else "Unknown error"
        output: t.Quality.HookOutput = {"error": error_msg}
        return output
    return result.value


@_mcp.tool()
def validate_rules(
    path: str,
    *,
    context: t.JsonMapping | None = None,
) -> t.JsonMapping:
    """Validate code against YAML rules."""
    engine = FlextQualityRulesEngine()
    result = engine.validate(path=path, context=context)
    if result.failure:
        return {"error": result.error}
    return {"violations": u.normalize_to_json_value(result.value)}
