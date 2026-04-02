"""Base MCP client for communicating with MCP servers.

Provides a unified interface for calling MCP server tools
via the mcp-cli command-line interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
from collections.abc import Mapping, MutableSequence, Sequence
from typing import final

from flext_core import r
from flext_quality import c, m, t


@final
class FlextQualityMcpClient:
    """Base client for MCP server communication.

    Uses mcp-cli for actual server communication.
    Provides unified error handling and result parsing.
    """

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the MCP client."""
        self._timeout_ms = timeout_ms or c.Quality.Defaults.MCP_TIMEOUT_MS

    def build_call_command(self, call: m.Quality.McpToolCall) -> r[t.StrSequence]:
        """Build the mcp-cli command for a tool call."""
        if not self.is_mcp_cli_available():
            return r[t.StrSequence].fail("mcp-cli not found in PATH")
        tool_path = f"{call.server}/{call.tool}"
        params_json = t.CONTAINER_MAPPING_ADAPTER.dump_json(call.params).decode("utf-8")
        return r[t.StrSequence].ok(["mcp-cli", "call", tool_path, params_json])

    def build_info_command(self, server: str, tool: str) -> r[t.StrSequence]:
        """Build the mcp-cli info command for a tool."""
        if not self.is_mcp_cli_available():
            return r[t.StrSequence].fail("mcp-cli not found in PATH")
        tool_path = f"{server}/{tool}"
        return r[t.StrSequence].ok(["mcp-cli", "info", tool_path])

    def build_tool_call(
        self,
        server: str,
        tool: str,
        params: t.ContainerMapping | None = None,
    ) -> r[m.Quality.McpToolCall]:
        """Build an MCP tool call request."""
        call_params: t.ContainerMapping = {}
        if isinstance(params, Mapping):
            validated_params: t.ContainerMapping = (
                t.CONTAINER_MAPPING_ADAPTER.validate_python(params)
            )
            call_params = dict(validated_params)
        return r[m.Quality.McpToolCall].ok(
            m.Quality.McpToolCall.model_validate({
                "server": server,
                "tool": tool,
                "params": call_params,
            }),
        )

    def health_check(self) -> r[t.ContainerMapping]:
        """Check if MCP infrastructure is available."""
        available = self.is_mcp_cli_available()
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if available
            else c.Quality.IntegrationStatus.DISCONNECTED
        )
        return r[t.ContainerMapping].ok({
            "status": status,
            "available": available,
            "mcp_cli": available,
            "timeout_ms": self._timeout_ms,
        })

    def is_mcp_cli_available(self) -> bool:
        """Check if mcp-cli is available in PATH."""
        return shutil.which("mcp-cli") is not None

    def parse_result(self, output: str, exit_code: int) -> r[m.Quality.McpToolResult]:
        """Parse the output from an mcp-cli call."""
        if exit_code != 0:
            return r[m.Quality.McpToolResult].ok(
                m.Quality.McpToolResult(
                    success=False,
                    data=None,
                    error=output or f"Command failed with exit code {exit_code}",
                ),
            )
        try:
            parsed: t.ContainerMapping = t.CONTAINER_MAPPING_ADAPTER.validate_json(
                output
            )
            result_data: t.StrMapping = {str(k): str(v) for k, v in parsed.items()}
            return r[m.Quality.McpToolResult].ok(
                m.Quality.McpToolResult.model_validate({
                    "success": True,
                    "data": result_data,
                    "error": None,
                }),
            )
        except ValueError:
            try:
                parsed_list: Sequence[t.NormalizedValue] = (
                    t.NORMALIZED_VALUE_SEQUENCE_ADAPTER.validate_json(
                        output,
                    )
                )
                coerced_data: MutableSequence[t.StrMapping] = []
                for item in parsed_list:
                    if isinstance(item, Mapping):
                        validated_item: t.ContainerMapping = (
                            t.CONTAINER_MAPPING_ADAPTER.validate_python(item)
                        )
                        coerced_data.append({
                            str(key): str(value)
                            for key, value in validated_item.items()
                        })
                    else:
                        coerced_data.append({"value": str(item)})
                return r[m.Quality.McpToolResult].ok(
                    m.Quality.McpToolResult(
                        success=True,
                        data={
                            "items": t.STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER.dump_json(
                                coerced_data
                            ).decode("utf-8"),
                        },
                        error=None,
                    ),
                )
            except ValueError:
                return r[m.Quality.McpToolResult].ok(
                    m.Quality.McpToolResult(
                        success=True,
                        data={"raw": output},
                        error=None,
                    ),
                )
