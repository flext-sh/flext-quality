"""Claude Memory integration client.

Provides integration with the claude-mem MCP server for cross-session
memory and observation persistence.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import final

from flext_core.constants import c
from flext_core.result import r
from flext_core.typings import t

from flext_quality.integrations._health import build_mcp_health_result
from flext_quality.integrations.mcp_client import FlextQualityMcpClient, McpToolCall


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

    def build_get_observations_call(self, ids: list[int]) -> r[McpToolCall]:
        """Build a get_observations tool call."""
        normalized_ids: list[t.NormalizedValue] = list(ids)
        params: dict[str, t.NormalizedValue] = {"ids": normalized_ids}
        return self._mcp.build_tool_call(self.SERVER_NAME, "get_observations", params)

    def build_search_call(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> r[McpToolCall]:
        """Build a search tool call."""
        search_limit = limit or c.Quality.Defaults.DEFAULT_MEMORY_SEARCH_LIMIT
        params: dict[str, t.NormalizedValue] = {
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
    ) -> r[McpToolCall]:
        """Build a timeline tool call."""
        before = depth_before or c.Quality.Defaults.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.Defaults.DEFAULT_TIMELINE_DEPTH
        params: dict[str, t.NormalizedValue] = {
            "anchor": anchor,
            "depth_before": before,
            "depth_after": after,
        }
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "timeline",
            params,
        )

    def get_observations_command(self, ids: list[int]) -> r[list[str]]:
        """Get the mcp-cli command for fetching observations."""
        return self.build_get_observations_call(ids).flat_map(
            self._mcp.build_call_command,
        )

    def get_search_command(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> r[list[str]]:
        """Get the mcp-cli command for memory search."""
        search_limit = limit or c.Quality.Defaults.DEFAULT_MEMORY_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command,
        )

    def get_timeline_command(
        self,
        anchor: int,
        *,
        depth_before: int | None = None,
        depth_after: int | None = None,
    ) -> r[list[str]]:
        """Get the mcp-cli command for timeline query."""
        before = depth_before or c.Quality.Defaults.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.Defaults.DEFAULT_TIMELINE_DEPTH
        return self.build_timeline_call(
            anchor,
            depth_before=before,
            depth_after=after,
        ).flat_map(self._mcp.build_call_command)

    def health_check(self) -> r[Mapping[str, t.NormalizedValue]]:
        """Check if claude-mem is available."""
        return build_mcp_health_result(self.SERVER_NAME, self._mcp)
