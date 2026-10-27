"""MCP tools for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_quality import c, t, u
from flext_quality.hooks import FlextQualityHookManager
from flext_quality.integrations import (
    FlextQualityClaudeContextClient,
    FlextQualityClaudeMemClient,
)
from flext_quality.mcp import FlextQualityMcpServer
from flext_quality.rules import FlextQualityRulesEngine


class FlextQualityMcpTools:
    """MCP tools namespace for flext-quality."""

    _mcp = FlextQualityMcpServer.resolve_server()

    @staticmethod
    def _build_search_payload(
        client: FlextQualityClaudeContextClient | FlextQualityClaudeMemClient,
        query: str,
        *,
        limit: int,
        search_type: str | None = None,
    ) -> t.JsonMapping:
        """Assemble the normalized search tool call and command payload.

        Args:
            client: Integration client providing the search call builders.
            query: Search query text.
            limit: Maximum number of results requested.
            search_type: Optional search type inserted into the params.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        result = client.build_search_call(query=query, limit=limit)
        if result.failure:
            return {"error": result.error}
        command_result = client.build_search_command(query=query, limit=limit)
        if command_result.failure:
            return {"error": command_result.error}
        params = u.normalize_to_json_value(result.value.params)
        params_map: t.JsonMapping = params if isinstance(params, Mapping) else {}
        params_payload: t.JsonDict = dict(params_map)
        if search_type is not None:
            params_payload["search_type"] = search_type
        return {
            "server": result.value.server,
            "tool": result.value.tool,
            "params": params_payload,
            c.HandlerMode.COMMAND: u.normalize_to_json_value(command_result.value),
        }

    @_mcp.tool()
    @staticmethod
    def search_memory(
        query: str,
        *,
        search_type: str = "observations",
        limit: int | None = None,
    ) -> t.JsonMapping:
        """Build command to search cross-session memory via claude-mem.

        Args:
            query: Search query text.
            search_type: Search type selecting the memory index.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        return FlextQualityMcpTools._build_search_payload(
            FlextQualityClaudeMemClient(),
            query,
            limit=limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT,
            search_type=search_type,
        )

    @_mcp.tool()
    @staticmethod
    def search_code(query: str, *, limit: int | None = None) -> t.JsonMapping:
        """Build command for semantic code search via claude-context.

        Args:
            query: Search query text.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        return FlextQualityMcpTools._build_search_payload(
            FlextQualityClaudeContextClient(),
            query,
            limit=limit or c.Quality.DEFAULT_SEARCH_LIMIT,
        )

    @_mcp.tool()
    @staticmethod
    def execute_hook(event: str, input_data: t.JsonMapping) -> t.JsonMapping:
        """Execute a hook manually.

        Args:
            event: Hook event name to dispatch.
            input_data: Hook input payload forwarded to the hooks.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        manager = FlextQualityHookManager()
        result = manager.execute(event=event, input_data=input_data)
        if result.failure:
            error_msg = result.error if result.error is not None else "Unknown error"
            output: t.JsonMapping = {"error": error_msg}
            return output
        return result.value

    @_mcp.tool()
    @staticmethod
    def validate_rules(
        path: str,
        *,
        context: t.JsonMapping | None = None,
    ) -> t.JsonMapping:
        """Validate code against YAML rules.

        Args:
            path: File or directory path to validate.
            context: Optional validation context attached to violations.

        Returns:
            The resulting ``t.JsonMapping``.

        """
        engine = FlextQualityRulesEngine()
        result = engine.validate(path=path, context=context)
        if result.failure:
            return {"error": result.error}
        return {
            "violations": [
                u.normalize_to_json_value(violation) for violation in result.value
            ],
        }


__all__: list[str] = ["FlextQualityMcpTools"]
