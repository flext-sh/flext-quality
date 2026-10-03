"""FastMCP server for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from fastmcp import FastMCP

from flext_quality import c

_mcp = FastMCP(name=c.Quality.MCP_SERVER_NAME, version=c.Quality.MCP_SERVER_VERSION)


class FlextQualityMcpServer:
    """MCP server namespace for flext-quality."""

    @staticmethod
    def resolve_server() -> FastMCP:
        """Get the MCP server instance.

        Returns:
            The resulting ``FastMCP``.
        """
        return _mcp


__all__: list[str] = ["FlextQualityMcpServer"]
