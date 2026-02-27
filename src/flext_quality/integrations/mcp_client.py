"""Base MCP client for communicating with MCP servers.

Provides a unified interface for calling MCP server tools
via the mcp-cli command-line interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Mapping
from typing import final

from flext_core import r
from pydantic import BaseModel, ConfigDict, Field

from flext_quality.constants import c


class McpToolCall(BaseModel):
    """Represents a call to an MCP server tool."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    server: str = Field(..., description="MCP server name")
    tool: str = Field(..., description="Tool name on the server")
    params: dict[str, object] = Field(
        default_factory=dict, description="Tool parameters"
    )


class McpToolResult(BaseModel):
    """Result from an MCP tool call."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    success: bool = Field(..., description="Whether the tool call succeeded")
    data: dict[str, object] | list[dict[str, object]] | None = Field(
        default=None,
        description="Result data from the tool call",
    )
    error: str | None = Field(default=None, description="Error message if call failed")


@final
class FlextQualityMcpClient:
    """Base client for MCP server communication.

    Uses mcp-cli for actual server communication.
    Provides unified error handling and result parsing.
    """

    def __init__(
        self,
        *,
        timeout_ms: int | None = None,
    ) -> None:
        """Initialize the MCP client."""
        self._timeout_ms = timeout_ms or c.Quality.Defaults.MCP_TIMEOUT_MS

    def is_mcp_cli_available(self) -> bool:
        """Check if mcp-cli is available in PATH."""
        return shutil.which("mcp-cli") is not None

    def build_tool_call(
        self,
        server: str,
        tool: str,
        params: dict[str, object] | None = None,
    ) -> r[McpToolCall]:
        """Build an MCP tool call request."""
        return r[McpToolCall].ok(
            McpToolCall(
                server=server,
                tool=tool,
                params=params or {},
            )
        )

    def build_call_command(
        self,
        call: McpToolCall,
    ) -> r[list[str]]:
        """Build the mcp-cli command for a tool call."""
        if not self.is_mcp_cli_available():
            return r[list[str]].fail("mcp-cli not found in PATH")

        tool_path = f"{call.server}/{call.tool}"
        params_json = json.dumps(call.params)

        return r[list[str]].ok(["mcp-cli", "call", tool_path, params_json])

    def build_info_command(
        self,
        server: str,
        tool: str,
    ) -> r[list[str]]:
        """Build the mcp-cli info command for a tool."""
        if not self.is_mcp_cli_available():
            return r[list[str]].fail("mcp-cli not found in PATH")

        tool_path = f"{server}/{tool}"
        return r[list[str]].ok(["mcp-cli", "info", tool_path])

    def parse_result(
        self,
        output: str,
        exit_code: int,
    ) -> r[McpToolResult]:
        """Parse the output from an mcp-cli call."""
        if exit_code != 0:
            return r[McpToolResult].ok(
                McpToolResult(
                    success=False,
                    data=None,
                    error=output or f"Command failed with exit code {exit_code}",
                )
            )

        try:
            data: object = json.loads(output)
            match data:
                case dict():
                    return r[McpToolResult].ok(
                        McpToolResult(
                            success=True,
                            data=data,
                            error=None,
                        )
                    )
                case list():
                    return r[McpToolResult].ok(
                        McpToolResult(
                            success=True,
                            data=data,
                            error=None,
                        )
                    )
                case _:
                    return r[McpToolResult].ok(
                        McpToolResult(
                            success=True,
                            data={"value": data},
                            error=None,
                        )
                    )
        except json.JSONDecodeError:
            # Return raw output as data if not valid JSON
            return r[McpToolResult].ok(
                McpToolResult(
                    success=True,
                    data={"raw": output},
                    error=None,
                )
            )

    def health_check(self) -> r[Mapping[str, object]]:
        """Check if MCP infrastructure is available."""
        available = self.is_mcp_cli_available()
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if available
            else c.Quality.IntegrationStatus.DISCONNECTED
        )

        return r[Mapping[str, object]].ok({
            "status": status,
            "available": available,
            "mcp_cli": available,
            "timeout_ms": self._timeout_ms,
        })
