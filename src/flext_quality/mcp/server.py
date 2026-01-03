"""FastMCP server for flext-quality."""

from __future__ import annotations

from fastmcp import FastMCP

from flext_quality.constants import FlextQualityConstants as c

# Initialize FastMCP server
mcp = FastMCP(name=c.Quality.Mcp.SERVER_NAME, version=c.Quality.Mcp.SERVER_VERSION)


def get_server() -> FastMCP:
    """Get the MCP server instance."""
    return mcp
