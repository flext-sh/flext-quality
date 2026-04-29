"""Base MCP client for communicating with MCP servers.

Provides a unified interface for calling MCP server tools
via the mcp-cli command-line interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
from collections.abc import (
    Mapping,
    MutableSequence,
)
from typing import final

from flext_quality import c, e, m, p, r, t


@final
class FlextQualityMcpClient:
    """Base client for MCP server communication.

    Uses mcp-cli for actual server communication.
    Provides unified error handling and result parsing.
    """

    def __init__(self, *, timeout_ms: int | None = None) -> None:
        """Initialize the MCP client."""
        self._timeout_ms = timeout_ms or c.Quality.MCP_TIMEOUT_MS

    def build_call_command(
        self, call: m.Quality.McpToolCall
    ) -> p.Result[t.StrSequence]:
        """Build the mcp-cli command for a tool call."""
        if not self.is_mcp_cli_available():
            return e.fail_not_found("executable", "mcp-cli")
        tool_path = f"{call.server}/{call.tool}"
        params_json = t.Quality.CONTAINER_MAPPING_ADAPTER.dump_json(call.params).decode(
            "utf-8"
        )
        return r[t.StrSequence].ok(["mcp-cli", "call", tool_path, params_json])

    def build_info_command(self, server: str, tool: str) -> p.Result[t.StrSequence]:
        """Build the mcp-cli info command for a tool."""
        if not self.is_mcp_cli_available():
            return e.fail_not_found("executable", "mcp-cli")
        tool_path = f"{server}/{tool}"
        return r[t.StrSequence].ok(["mcp-cli", "info", tool_path])

    def build_tool_call(
        self,
        server: str,
        tool: str,
        params: t.JsonMapping | None = None,
    ) -> p.Result[m.Quality.McpToolCall]:
        """Build an MCP tool call request."""
        call_params = (
            dict(t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(params))
            if isinstance(params, Mapping)
            else dict(t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python({}))
        )
        return r[m.Quality.McpToolCall].ok(
            m.Quality.McpToolCall.model_validate({
                "server": server,
                "tool": tool,
                "params": call_params,
            }),
        )

    def health_check(self) -> p.Result[t.JsonMapping]:
        """Check if MCP infrastructure is available."""
        available = self.is_mcp_cli_available()
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if available
            else c.Quality.IntegrationStatus.DISCONNECTED
        )
        return r[t.JsonMapping].ok({
            "status": status,
            "available": available,
            "mcp_cli": available,
            "timeout_ms": self._timeout_ms,
        })

    def build_server_health_result(self, server_name: str) -> p.Result[t.JsonMapping]:
        """Build a normalized health result for a named MCP server."""
        mcp_health = self.health_check()
        if mcp_health.failure:
            return r[t.JsonMapping].fail(mcp_health.error)
        health_data = mcp_health.value
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if health_data.get("available", False)
            else c.Quality.IntegrationStatus.DISCONNECTED
        )
        return r[t.JsonMapping].ok({
            "server": server_name,
            "status": status,
            "available": health_data.get("available", False),
            "mcp_cli": health_data.get("mcp_cli", False),
        })

    def is_mcp_cli_available(self) -> bool:
        """Check if mcp-cli is available in PATH."""
        return shutil.which("mcp-cli") is not None

    def parse_result(
        self, output: str, exit_code: int
    ) -> p.Result[m.Quality.McpToolResult]:
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
            parsed: t.JsonMapping = t.Quality.CONTAINER_MAPPING_ADAPTER.validate_json(
                output
            )
            result_data: t.StrMapping = {k: str(v) for k, v in parsed.items()}
            return r[m.Quality.McpToolResult].ok(
                m.Quality.McpToolResult.model_validate({
                    "success": True,
                    "data": result_data,
                    "error": None,
                }),
            )
        except ValueError:
            try:
                parsed_list: t.JsonList = (
                    t.Quality.NORMALIZED_VALUE_SEQUENCE_ADAPTER.validate_json(
                        output,
                    )
                )
                coerced_data: MutableSequence[t.StrMapping] = []
                for item in parsed_list:
                    if isinstance(item, Mapping):
                        validated_item: t.JsonMapping = (
                            t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(item)
                        )
                        coerced_data.append({
                            key: str(value) for key, value in validated_item.items()
                        })
                    else:
                        coerced_data.append({"value": str(item)})
                return r[m.Quality.McpToolResult].ok(
                    m.Quality.McpToolResult(
                        success=True,
                        data={
                            "items": t.Quality.STR_MAPPING_MUTABLE_SEQUENCE_ADAPTER.dump_json(
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
