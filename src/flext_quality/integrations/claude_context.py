"""Claude Context integration client.

Provides integration with the claude-context MCP server for semantic
code search and codebase indexing capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import final

from flext_quality import c, m, p, t
from flext_quality.integrations.mcp_client import FlextQualityMcpClient


@final
class FlextQualityClaudeContextClient:
    """Client for claude-context MCP server integration.

    Provides semantic code search via the claude-context server.
    Uses mcp-cli for server communication.
    """

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the Claude Context client."""
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_index_call(
        self, path: str | None = None
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build an index_codebase tool call."""
        params: t.MutableJsonMapping = {}
        if path:
            params["path"] = path
        result: p.Result[m.Quality.McpToolCall] = self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME, "index_codebase", params
        )
        return result

    def build_search_call(
        self, query: str, *, limit: int | None = None
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a search_code tool call."""
        search_limit = limit or c.Quality.DEFAULT_SEARCH_LIMIT
        result: p.Result[m.Quality.McpToolCall] = self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME,
            "search_code",
            {"query": query, "limit": search_limit},
        )
        return result

    def build_status_call(self) -> p.Result[m.Quality.McpToolCall]:
        """Build a get_indexing_status tool call."""
        result: p.Result[m.Quality.McpToolCall] = self._mcp.build_tool_call(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME, "get_indexing_status", {}
        )
        return result

    def get_index_command(self, path: str | None = None) -> p.Result[t.StrSequence]:
        """Get the mcp-cli command for codebase indexing."""
        return self.build_index_call(path).flat_map(self._mcp.build_call_command)

    def get_search_command(
        self, query: str, *, limit: int | None = None
    ) -> p.Result[t.StrSequence]:
        """Get the mcp-cli command for code search."""
        search_limit = limit or c.Quality.DEFAULT_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command
        )

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check if claude-context is available."""
        result: p.Result[t.JsonMapping] = self._mcp.build_server_health_result(
            c.Quality.CLAUDE_CONTEXT_SERVER_NAME
        )
        return result
