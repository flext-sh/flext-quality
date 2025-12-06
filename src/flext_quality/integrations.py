"""FLEXT Quality Integrations - External service integrations using flext-api.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_api import FlextApiClient, FlextApiConfig
from flext_core import FlextLogger, FlextResult, FlextService
from pydantic import BaseModel, Field

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
        self._config = config or ApiClientConfig()
        self._api_config = FlextApiConfig(**self._config.model_dump())
        self._api_client = FlextApiClient(config=self._api_config)
        self._logger = FlextLogger(__name__)

    @property
    def logger(self) -> FlextLogger:
        """Get logger."""
        return self._logger

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
            client: FlextApiClient,
            url: str,
            json: dict[str, object] | None = None,
            files: dict[str, tuple[str, bytes]] | None = None,
            headers: dict[str, str] | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Execute POST request and return result."""
            result = client.post(url=url, json=json, files=files, headers=headers)
            return (
                result
                if result.is_success
                else FlextResult.fail(f"HTTP POST failed: {result.error}")
            )

        @staticmethod
        def get(
            client: FlextApiClient,
            url: str,
            params: dict[str, str] | None = None,
            headers: dict[str, str] | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Execute GET request and return result."""
            result = client.get(url=url, params=params, headers=headers)
            return (
                result
                if result.is_success
                else FlextResult.fail(f"HTTP GET failed: {result.error}")
            )

    class _PayloadBuilders:
        """Single responsibility: Build integration payloads."""

        @staticmethod
        def webhook_payload(
            event_type: str,
            event_data: dict[str, object],
        ) -> dict[str, object]:
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
        ) -> dict[str, object]:
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
            check_results: dict[str, object],
        ) -> dict[str, object]:
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
        event_data: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
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
    ) -> FlextResult[dict[str, object]]:
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
        quality_data: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Integrate with SonarQube."""
        api_url = f"{sonarqube_url}/api/measures/component"
        component_key = quality_data.get("component", project_key)
        return self._HttpOperations.get(
            self._api_client,
            api_url,
            params={"component": component_key},
            headers={"Authorization": f"Bearer {token}"},
        ).map_error(lambda e: self._log_error("sonarqube", e))

    def integrate_github_checks(
        self,
        github_api_url: str,
        repo: str,
        commit_sha: str,
        token: str,
        check_results: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
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
    ) -> FlextResult[dict[str, object]]:
        """Deliver quality report to external storage."""
        try:
            content = report_file.read_bytes()
            return self._HttpOperations.post(
                self._api_client,
                storage_url,
                files={"report": (report_file.name, content)},
                headers={"X-API-Key": api_key},
            ).map_error(lambda e: self._log_error("storage", e))
        except Exception as e:
            return FlextResult.fail(self._log_error("storage_read", str(e)))

    def notify_on_threshold_violation(
        self,
        webhook_urls: list[str],
        violation_data: dict[str, object],
    ) -> FlextResult[list[dict[str, object]]]:
        """Notify multiple webhooks of threshold violations."""
        results = [
            r.value
            for url in webhook_urls
            if (
                r := self.send_webhook_notification(
                    url,
                    "threshold_violation",
                    violation_data,
                )
            ).is_success
        ]

        return (
            FlextResult.ok(results)
            if results
            else FlextResult.fail("All webhook notifications failed")
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
