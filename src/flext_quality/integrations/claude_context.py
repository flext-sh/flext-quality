"""Claude Context integration client.

Provides integration with the claude-context MCP server for semantic
code search and codebase indexing capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import final

from flext_core import r

from flext_quality import (
    FlextQualityMcpClient,
    McpToolCall,
    build_mcp_health_result,
    c,
    t,
)


@final
class FlextQualityClaudeContextClient:
    """Client for claude-context MCP server integration.

    Provides semantic code search via the claude-context server.
    Uses mcp-cli for server communication.
    """

    SERVER_NAME = "claude-context"

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the Claude Context client."""
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_index_call(self, path: str | None = None) -> r[McpToolCall]:
        """Build an index_codebase tool call."""
        params: t.ContainerMapping = {}
        if path:
            params["path"] = path
        return self._mcp.build_tool_call(self.SERVER_NAME, "index_codebase", params)

    def build_search_call(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> r[McpToolCall]:
        """Build a search_code tool call."""
        search_limit = limit or c.Quality.Defaults.DEFAULT_SEARCH_LIMIT
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "search_code",
            {"query": query, "limit": search_limit},
        )

    def build_status_call(self) -> r[McpToolCall]:
        """Build a get_indexing_status tool call."""
        return self._mcp.build_tool_call(self.SERVER_NAME, "get_indexing_status", {})

    def get_index_command(self, path: str | None = None) -> r[Sequence[str]]:
        """Get the mcp-cli command for codebase indexing."""
        return self.build_index_call(path).flat_map(self._mcp.build_call_command)

    def get_search_command(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> r[Sequence[str]]:
        """Get the mcp-cli command for code search."""
        search_limit = limit or c.Quality.Defaults.DEFAULT_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command,
        )

    def health_check(self) -> r[t.ContainerMapping]:
        """Check if claude-context is available."""
        return build_mcp_health_result(self.SERVER_NAME, self._mcp)
