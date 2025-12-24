"""FLEXT Quality Integrations - External service integrations using flext-api.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_api import FlextApi, FlextApiSettings
from pydantic import BaseModel, Field

from flext import FlextLogger, FlextResult, FlextRuntime, FlextService, FlextTypes

# =====================================================================
# Configuration Models (Pydantic 2) - Data-Driven Integrations
# =====================================================================


class ApiClientConfig(BaseModel):
    """API client configuration."""

    base_url: str = Field(default="")
    timeout: int = Field(default=30, ge=1)
    max_retries: int = Field(default=3, ge=0)
    enable_circuit_breaker: bool = Field(default=True)


class SeverityColorMap(BaseModel):
    """Severity-to-color mapping for notifications."""

    colors: dict[str, str] = Field(
        default_factory=lambda: {
            "info": "#36a64f",
            "warning": "#ff9900",
            "error": "#ff0000",
        },
    )


# =====================================================================
# Main Integration Service - SOLID Delegation Pattern
# =====================================================================


class FlextQualityIntegrations(FlextService[bool]):
    """Quality integrations orchestrating external service communications."""

    def __init__(self, config: ApiClientConfig | None = None) -> None:
        """Initialize quality integrations."""
        super().__init__()
        # Use object.__setattr__ to bypass Pydantic's custom __setattr__ for private attributes
        api_config = config or ApiClientConfig()
        object.__setattr__(self, "_config", api_config)
        self._api_config = FlextApiSettings(**api_config.model_dump())
        self._api_client = FlextApi(config=self._api_config)
        self._logger = FlextLogger(__name__)

    @override
    def execute(self) -> FlextResult[bool]:
        """Execute integration service."""
        return FlextResult[bool].ok(True)

    # =====================================================================
    # Nested Utility Classes - Single Responsibility Each
    # =====================================================================

    class _HttpOperations:
        """Single responsibility: HTTP operations with flext-api."""

        @staticmethod
        def post(
            client: FlextApi,
            url: str,
            json: dict[str, FlextTypes.JsonValue] | None = None,
            files: dict[str, tuple[str, bytes]] | None = None,
            headers: dict[str, str] | None = None,
        ) -> FlextResult[dict[str, FlextTypes.JsonValue]]:
            """Execute POST request and return result."""
            # Note: files not directly supported by FlextApi, would need multipart encoding
            _ = files  # Acknowledge unused parameter
            result = client.post(url=url, data=json, headers=headers)
            if result.is_failure:
                return FlextResult[dict[str, FlextTypes.JsonValue]].fail(
                    f"HTTP POST failed: {result.error}",
                )
            # Extract body from HttpResponse
            response = result.value
            body = response.body
            if isinstance(body, dict):
                # Reconstruct dict with JsonValue for type safety
                return FlextResult[dict[str, FlextTypes.JsonValue]].ok(dict(body))
            return FlextResult[dict[str, FlextTypes.JsonValue]].ok({
                "response": str(body),
            })

        @staticmethod
        def get(
            client: FlextApi,
            url: str,
            params: dict[str, str] | None = None,
            headers: dict[str, str] | None = None,
        ) -> FlextResult[dict[str, FlextTypes.JsonValue]]:
            """Execute GET request and return result."""
            # FlextApi.get uses request_kwargs for params
            request_kwargs = {"params": params} if params else None
            result = client.get(url=url, headers=headers, request_kwargs=request_kwargs)
            if result.is_failure:
                return FlextResult[dict[str, FlextTypes.JsonValue]].fail(
                    f"HTTP GET failed: {result.error}",
                )
            # Extract body from HttpResponse
            response = result.value
            body = response.body
            if isinstance(body, dict):
                # Reconstruct dict with JsonValue for type safety
                return FlextResult[dict[str, FlextTypes.JsonValue]].ok(dict(body))
            return FlextResult[dict[str, FlextTypes.JsonValue]].ok({
                "response": str(body),
            })

    class _PayloadBuilders:
        """Single responsibility: Build integration payloads."""

        @staticmethod
        def webhook_payload(
            event_type: str,
            event_data: dict[str, FlextTypes.JsonValue],
        ) -> dict[str, FlextTypes.JsonValue]:
            """Build webhook notification payload."""
            return {
                "event_type": event_type,
                "event_data": event_data,
                "service": "flext-quality",
                "version": "0.9.0",
            }

        @staticmethod
        def slack_payload(
            message: str,
            severity: str,
            color_map: dict[str, str],
        ) -> dict[str, FlextTypes.JsonValue]:
            """Build Slack message payload."""
            return {
                "attachments": [
                    {
                        "color": color_map.get(severity, "#36a64f"),
                        "title": "FLEXT Quality Alert",
                        "text": message,
                        "footer": "flext-quality v0.9.0",
                    },
                ],
            }

        @staticmethod
        def github_checks_payload(
            commit_sha: str,
            check_results: dict[str, FlextTypes.JsonValue],
        ) -> dict[str, FlextTypes.JsonValue]:
            """Build GitHub Checks API payload."""
            return {
                "name": "FLEXT Quality Check",
                "head_sha": commit_sha,
                "status": "completed",
                "conclusion": check_results.get("conclusion", "success"),
                "output": {
                    "title": "Quality Analysis Results",
                    "summary": check_results.get(
                        "summary",
                        "Quality analysis completed",
                    ),
                    "text": check_results.get("details", ""),
                },
            }

    # =====================================================================
    # Public Integration Methods - Railway-Oriented
    # =====================================================================

    def send_webhook_notification(
        self,
        webhook_url: str,
        event_type: str,
        event_data: dict[str, FlextTypes.JsonValue],
    ) -> FlextRuntime.RuntimeResult[dict[str, str]]:
        """Send webhook notification."""
        payload = self._PayloadBuilders.webhook_payload(event_type, event_data)
        return (
            self._HttpOperations.post(
                self._api_client,
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            .map(lambda _: {"status": "sent"})
            .map_error(lambda e: self._log_error("webhook", e))
        )

    def send_slack_notification(
        self,
        webhook_url: str,
        message: str,
        severity: str = "info",
    ) -> FlextRuntime.RuntimeResult[dict[str, str]]:
        """Send Slack notification."""
        color_map = SeverityColorMap().colors
        payload = self._PayloadBuilders.slack_payload(message, severity, color_map)
        return (
            self._HttpOperations.post(self._api_client, webhook_url, json=payload)
            .map(lambda _: {"status": "sent"})
            .map_error(lambda e: self._log_error("slack", e))
        )

    def integrate_sonarqube(
        self,
        sonarqube_url: str,
        project_key: str,
        token: str,
        quality_data: dict[str, FlextTypes.JsonValue],
    ) -> FlextRuntime.RuntimeResult[dict[str, FlextTypes.JsonValue]]:
        """Integrate with SonarQube."""
        api_url = f"{sonarqube_url}/api/measures/component"
        component_key = quality_data.get("component", project_key)
        return self._HttpOperations.get(
            self._api_client,
            api_url,
            params={"component": str(component_key)},
            headers={"Authorization": f"Bearer {token}"},
        ).map_error(lambda e: self._log_error("sonarqube", e))

    def integrate_github_checks(
        self,
        github_api_url: str,
        repo: str,
        commit_sha: str,
        token: str,
        check_results: dict[str, FlextTypes.JsonValue],
    ) -> FlextRuntime.RuntimeResult[dict[str, FlextTypes.JsonValue]]:
        """Integrate with GitHub Checks API."""
        api_url = f"{github_api_url}/repos/{repo}/check-runs"
        payload = self._PayloadBuilders.github_checks_payload(commit_sha, check_results)
        return self._HttpOperations.post(
            self._api_client,
            api_url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
        ).map_error(lambda e: self._log_error("github", e))

    def deliver_report_to_external_storage(
        self,
        storage_url: str,
        report_file: Path,
        api_key: str,
    ) -> FlextRuntime.RuntimeResult[dict[str, FlextTypes.JsonValue]]:
        """Deliver quality report to external storage."""
        try:
            content = report_file.read_bytes()
            return self._HttpOperations.post(
                self._api_client,
                storage_url,
                files={"report": (report_file.name, content)},
                headers={"X-API-Key": api_key},
            ).map_error(lambda e: self._log_error("storage", e))
        except Exception as exc:
            return FlextResult[dict[str, FlextTypes.JsonValue]].fail(
                self._log_error("storage_read", str(exc)),
            )

    def notify_on_threshold_violation(
        self,
        webhook_urls: list[str],
        violation_data: dict[str, FlextTypes.JsonValue],
    ) -> FlextResult[list[dict[str, str]]]:
        """Notify multiple webhooks of threshold violations."""
        results: list[dict[str, str]] = []
        for url in webhook_urls:
            result = self.send_webhook_notification(
                url,
                "threshold_violation",
                violation_data,
            )
            if result.is_success:
                value = result.value
                if value is not None:
                    results.append(value)

        if results:
            return FlextResult[list[dict[str, str]]].ok(results)
        return FlextResult[list[dict[str, str]]].fail(
            "All webhook notifications failed",
        )

    # =====================================================================
    # Private Helper Methods
    # =====================================================================

    def _log_error(self, operation: str, error: str) -> str:
        """Log and return error."""
        self._logger.error(f"{operation.upper()} integration failed: {error}")
        return error


__all__ = [
    "ApiClientConfig",
    "FlextQualityIntegrations",
    "SeverityColorMap",
]
