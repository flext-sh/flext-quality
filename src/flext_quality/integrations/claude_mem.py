"""Claude Memory integration client.

Provides integration with the claude-mem MCP server for cross-session
memory and observation persistence.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import final

from flext_quality import c, m, p, t
from flext_quality.integrations import FlextQualityMcpClient


@final
class FlextQualityClaudeMemClient:
    """Client for claude-mem MCP server integration.

    Provides cross-session memory search via the claude-mem server.
    Uses mcp-cli for server communication.
    """

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the Claude Mem client.

        Args:
            timeout_ms: Optional command timeout in milliseconds; defaults to
                the configured integration timeout.

        """
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_get_observations_call(
        self,
        ids: Sequence[int],
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a get_observations tool call.

        Args:
            ids: Observation identifiers fetched by the tool.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        normalized_ids: t.JsonValueList = list(ids)
        params = {"ids": normalized_ids}
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_MEM_SERVER_NAME,
            "get_observations",
            params,
        )

    def build_search_call(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a search tool call.

        Args:
            query: Search query text.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        search_limit = limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT
        # Why: mro-4p0t — bind JsonMapping for build_tool_call params.
        params: t.MutableJsonMapping = {
            c.HandlerMode.QUERY: query,
            "limit": search_limit,
        }
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_MEM_SERVER_NAME,
            "search",
            params,
        )

    def build_timeline_call(
        self,
        anchor: int,
        *,
        depth_before: int | None = None,
        depth_after: int | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build a timeline tool call.

        Args:
            anchor: Observation identifier anchoring the timeline.
            depth_before: Number of observations before the anchor; defaults
                to the configured depth.
            depth_after: Number of observations after the anchor; defaults to
                the configured depth.

        Returns:
            The resulting ``p.Result[m.Quality.McpToolCall]``.

        """
        before = depth_before or c.Quality.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.DEFAULT_TIMELINE_DEPTH
        params = {"anchor": anchor, "depth_before": before, "depth_after": after}
        return self._mcp.build_tool_call(
            c.Quality.CLAUDE_MEM_SERVER_NAME,
            "timeline",
            params,
        )

    def build_observations_command(
        self,
        ids: Sequence[int],
    ) -> p.Result[Sequence[str]]:
        """Get the mcp-cli command for fetching observations.

        Args:
            ids: Observation identifiers fetched by the command.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        return self.build_get_observations_call(ids).flat_map(
            self._mcp.build_call_command,
        )

    def build_search_command(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> p.Result[Sequence[str]]:
        """Get the mcp-cli command for memory search.

        Args:
            query: Search query text.
            limit: Maximum number of results; defaults to the configured limit.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        search_limit = limit or c.Quality.DEFAULT_MEMORY_SEARCH_LIMIT
        return self.build_search_call(query, limit=search_limit).flat_map(
            self._mcp.build_call_command,
        )

    def build_timeline_command(
        self,
        anchor: int,
        *,
        depth_before: int | None = None,
        depth_after: int | None = None,
    ) -> p.Result[Sequence[str]]:
        """Get the mcp-cli command for timeline query.

        Args:
            anchor: Observation identifier anchoring the timeline.
            depth_before: Number of observations before the anchor; defaults
                to the configured depth.
            depth_after: Number of observations after the anchor; defaults to
                the configured depth.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        before = depth_before or c.Quality.DEFAULT_TIMELINE_DEPTH
        after = depth_after or c.Quality.DEFAULT_TIMELINE_DEPTH
        return self.build_timeline_call(
            anchor,
            depth_before=before,
            depth_after=after,
        ).flat_map(self._mcp.build_call_command)

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check if claude-mem is available.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return self._mcp.build_server_health_result(c.Quality.CLAUDE_MEM_SERVER_NAME)


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityClaudeMemClient"]
