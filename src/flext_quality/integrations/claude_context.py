"""Claude Context integration client.

Provides integration with the claude-context MCP server for semantic
code search and codebase indexing capabilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import final

from flext_core import FlextResult as r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.integrations.mcp_client import (
    FlextQualityMcpClient,
    McpToolCall,
)


@final
class FlextQualityClaudeContextClient:
    """Client for claude-context MCP server integration.

    Provides semantic code search via the claude-context server.
    Uses mcp-cli for server communication.
    """

    SERVER_NAME = "claude-context"

    def __init__(
        self,
        *,
        timeout_ms: int | None = None,
    ) -> None:
        """Initialize the Claude Context client."""
        self._mcp = FlextQualityMcpClient(timeout_ms=timeout_ms)

    def build_search_call(
        self,
        query: str,
        *,
        limit: int = 20,
    ) -> r[McpToolCall]:
        """Build a search_code tool call."""
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "search_code",
            {
                "query": query,
                "limit": limit,
            },
        )

    def build_index_call(
        self,
        path: str | None = None,
    ) -> r[McpToolCall]:
        """Build an index_codebase tool call."""
        params: dict[str, object] = {}
        if path:
            params["path"] = path

        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "index_codebase",
            params,
        )

    def build_status_call(self) -> r[McpToolCall]:
        """Build a get_indexing_status tool call."""
        return self._mcp.build_tool_call(
            self.SERVER_NAME,
            "get_indexing_status",
            {},
        )

    def get_search_command(
        self,
        query: str,
        *,
        limit: int = 20,
    ) -> r[list[str]]:
        """Get the mcp-cli command for code search."""
        call_result = self.build_search_call(query, limit=limit)
        if call_result.is_failure:
            return r[list[str]].fail(call_result.error)

        return self._mcp.build_call_command(call_result.value)

    def get_index_command(
        self,
        path: str | None = None,
    ) -> r[list[str]]:
        """Get the mcp-cli command for codebase indexing."""
        call_result = self.build_index_call(path)
        if call_result.is_failure:
            return r[list[str]].fail(call_result.error)

        return self._mcp.build_call_command(call_result.value)

    def health_check(self) -> r[dict[str, object]]:
        """Check if claude-context is available."""
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
