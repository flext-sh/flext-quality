"""FastMCP server for flext-quality."""

from __future__ import annotations

from fastmcp import FastMCP

from flext_quality import c

_mcp = FastMCP(name=c.Quality.MCP_SERVER_NAME, version=c.Quality.MCP_SERVER_VERSION)


class FlextQualityMcpServer:
    """MCP server namespace for flext-quality."""

    @staticmethod
    def get_server() -> FastMCP:
        """Get the MCP server instance."""
        return _mcp


__all__: list[str] = ["FlextQualityMcpServer"]
