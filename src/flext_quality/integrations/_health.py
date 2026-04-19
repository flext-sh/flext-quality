from __future__ import annotations

from flext_quality import FlextQualityMcpClient, c, p, r, t


class FlextQualityIntegrationsHealth:
    """Internal health-result helpers for quality integrations."""

    @staticmethod
    def build_mcp_health_result(
        server_name: str,
        mcp_client: FlextQualityMcpClient,
    ) -> p.Result[Mapping[str, t.Container]]:
        """Build a normalized health result for a named MCP server."""
        mcp_health = mcp_client.health_check()
        if mcp_health.failure:
            return r[Mapping[str, t.Container]].fail(mcp_health.error)
        health_data = mcp_health.value
        status = (
            c.Quality.IntegrationStatus.CONNECTED
            if health_data.get("available", False)
            else c.Quality.IntegrationStatus.DISCONNECTED
        )
        return r[Mapping[str, t.Container]].ok({
            "server": server_name,
            "status": status,
            "available": health_data.get("available", False),
            "mcp_cli": health_data.get("mcp_cli", False),
        })


__all__: list[str] = ["FlextQualityIntegrationsHealth"]
