"""Claude Memory integration client.

Provides integration with the claude-mem MCP server for cross-session
memory and observation persistence.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import final

from flext_core import r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.integrations.mcp_client import (
    FlextQualityMcpClient,
    McpToolCall,
)


@final
class FlextQualityClaudeMemClient:
    """Client for claude-mem MCP server integration.

    Provides cross-session memory search via the claude-mem server.
    Uses mcp-cli for server communication.
    """

    SERVER_NAME = "claude-mem"

    def __init__(
        self,
        *,
        timeout_ms: int | None = None,
    ) -> None:
        """Initialize the Claude Mem client."""
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_search_call(
        self,
        query: str,
        *,
        limit: int = 10,
    ) -> r[McpToolCall]:
        """Build a search tool call."""
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "search",
            {
                "query": query,
                "limit": limit,
            },
        )

    def build_timeline_call(
        self,
        anchor: int,
        *,
        depth_before: int = 5,
        depth_after: int = 5,
    ) -> r[McpToolCall]:
        """Build a timeline tool call."""
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "timeline",
            {
                "anchor": anchor,
                "depth_before": depth_before,
                "depth_after": depth_after,
            },
        )

    def build_get_observations_call(
        self,
        ids: list[int],
    ) -> r[McpToolCall]:
        """Build a get_observations tool call."""
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "get_observations",
            {
                "ids": ids,
            },
        )

    def get_search_command(
        self,
        query: str,
        *,
        limit: int = 10,
    ) -> r[list[str]]:
        """Get the mcp-cli command for memory search."""
        call_result = self.build_search_call(query, limit=limit)
        if call_result.is_failure:
            return r[list[str]].fail(call_result.error)

        return self._mcp.build_call_command(call_result.value)

    def get_timeline_command(
        self,
        anchor: int,
        *,
        depth_before: int = 5,
        depth_after: int = 5,
    ) -> r[list[str]]:
        """Get the mcp-cli command for timeline query."""
        call_result = self.build_timeline_call(
            anchor,
            depth_before=depth_before,
            depth_after=depth_after,
        )
        if call_result.is_failure:
            return r[list[str]].fail(call_result.error)

        return self._mcp.build_call_command(call_result.value)

    def get_observations_command(
        self,
        ids: list[int],
    ) -> r[list[str]]:
        """Get the mcp-cli command for fetching observations."""
        call_result = self.build_get_observations_call(ids)
        if call_result.is_failure:
            return r[list[str]].fail(call_result.error)

        return self._mcp.build_call_command(call_result.value)

    def health_check(self) -> r[dict[str, object]]:
        """Check if claude-mem is available."""
        mcp_health = self._mcp.health_check()
        if mcp_health.is_failure:
            return r[dict[str, object]].fail(mcp_health.error)

        health_data = mcp_health.value
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if health_data.get("available", False)
            else c.Quality.IntegrationStatus.DISCONNECTED
        )

        return r[dict[str, object]].ok({
            "server": self.SERVER_NAME,
            "status": status,
            "available": health_data.get("available", False),
            "mcp_cli": health_data.get("mcp_cli", False),
        })
