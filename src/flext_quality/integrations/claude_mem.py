"""Claude Memory integration client.

Provides integration with the claude-mem MCP server for cross-session
memory and observation persistence.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import final

from flext_quality import (
    FlextQualityMcpClient,
    c,
    m,
    p,
    t,
)


@final
class FlextQualityClaudeMemClient:
    """Client for claude-mem MCP server integration.

    Provides cross-session memory search via the claude-mem server.
    Uses mcp-cli for server communication.
    """

    SERVER_NAME = "claude-mem"

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the Claude Mem client."""
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_get_observations_call(
        self, ids: t.SequenceOf[int]
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a get_observations tool call."""
        normalized_ids: list[t.JsonValue] = list(ids)
        params = {"ids": normalized_ids}
        return self._mcp.build_tool_call(self.SERVER_NAME, "get_observations", params)

    def build_search_call(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a search tool call."""
        search_limit = limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT
        params = {
            "query": query,
            "limit": search_limit,
        }
        return self._mcp.build_tool_call(self.SERVER_NAME, "search", params)

    def build_timeline_call(
        self,
        anchor: int,
        *,
        depth_before: int | None = None,
        depth_after: int | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a timeline tool call."""
        before = depth_before or c.Quality.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.DEFAULT_TIMELINE_DEPTH
        params = {
            "anchor": anchor,
            "depth_before": before,
            "depth_after": after,
        }
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "timeline",
            params,
        )

    def get_observations_command(
        self, ids: t.SequenceOf[int]
    ) -> p.Result[t.StrSequence]:
        """Get the mcp-cli command for fetching observations."""
        return self.build_get_observations_call(ids).flat_map(
            self._mcp.build_call_command,
        )

    def get_search_command(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[t.StrSequence]:
        """Get the mcp-cli command for memory search."""
        search_limit = limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command,
        )

    def get_timeline_command(
        self,
        anchor: int,
        *,
        depth_before: int | None = None,
        depth_after: int | None = None,
    ) -> p.Result[t.StrSequence]:
        """Get the mcp-cli command for timeline query."""
        before = depth_before or c.Quality.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.DEFAULT_TIMELINE_DEPTH
        return self.build_timeline_call(
            anchor,
            depth_before=before,
            depth_after=after,
        ).flat_map(self._mcp.build_call_command)

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check if claude-mem is available."""
        return self._mcp.build_server_health_result(self.SERVER_NAME)
