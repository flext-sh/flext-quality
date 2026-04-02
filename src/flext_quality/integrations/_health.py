from __future__ import annotations

from flext_core import r
from flext_quality import FlextQualityMcpClient, c, t


def build_mcp_health_result(
    server_name: str,
    mcp_client: FlextQualityMcpClient,
) -> r[t.ContainerMapping]:
    mcp_health = mcp_client.health_check()
    if mcp_health.is_failure:
        return r[t.ContainerMapping].fail(mcp_health.error)
    health_data = mcp_health.value
    status = (
        c.Quality.IntegrationStatus.CONNECTED
        if health_data.get("available", False)
        else c.Quality.IntegrationStatus.DISCONNECTED
    )
    return r[t.ContainerMapping].ok({
        "server": server_name,
        "status": status,
        "available": health_data.get("available", False),
        "mcp_cli": health_data.get("mcp_cli", False),
    })
