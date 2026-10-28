"""Claude Context integration client.

Provides integration with the claude-context MCP server for semantic
code search and codebase indexing capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import final

from flext_quality import c, m, p, t
from flext_quality.integrations import FlextQualityMcpClient


@final
class FlextQualityClaudeContextClient:
    """Client for claude-context MCP server integration.

    Provides semantic code search via the claude-context server.
    Uses mcp-cli for server communication.
    """

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the Claude Context client.

        Args:
            timeout_ms: Optional command timeout in milliseconds; defaults to
                the configured integration timeout.

        """
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_index_call(
        self,
        path: str | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build an index_codebase tool call.

        Args:
            path: Optional codebase path indexed by the tool.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        params: t.MutableJsonMapping = {}
        if path:
            params["path"] = path
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME,
            "index_codebase",
            params,
        )

    def build_search_call(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a search_code tool call.

        Args:
            query: Search query text.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        search_limit = limit or c.Quality.DEFAULT_SEARCH_LIMIT
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME,
            "search_code",
            {c.HandlerMode.QUERY: query, "limit": search_limit},
        )

    def build_status_call(self) -> p.Result[m.Quality.McpToolCall]:
        """Build a get_indexing_status tool call.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME,
            "get_indexing_status",
            {},
        )

    def build_index_command(self, path: str | None = None) -> p.Result[Sequence[str]]:
        """Get the mcp-cli command for codebase indexing.

        Args:
            path: Optional codebase path indexed by the command.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        return self.build_index_call(path).flat_map(self._mcp.build_call_command)

    def build_search_command(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[Sequence[str]]:
        """Get the mcp-cli command for code search.

        Args:
            query: Search query text.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        search_limit = limit or c.Quality.DEFAULT_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command,
        )

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check if claude-context is available.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return self._mcp.build_server_health_result(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME,
        )


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityClaudeContextClient"]
