"""FLEXT Quality Integrations - External service integrations using flext-api.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""
# ruff: noqa: S101

from __future__ import annotations

from pathlib import Path
from typing import cast

from flext_api import FlextApiClient, FlextApiConfig
from flext_core import FlextCore


class FlextQualityIntegrations(FlextCore.Service[None]):
    """Quality integrations service using flext-api for external communications.

    Provides:
    - Webhook notifications for quality events
    - External quality service integrations (SonarQube, GitHub, etc.)
    - Slack/Teams notifications
    - Report delivery to external platforms
    """

    def __init__(self) -> None:
        """Initialize quality integrations with flext-api."""
        super().__init__()
        self.logger = FlextCore.Logger(__name__)

        # Initialize flext-api configuration as dict
        api_config_dict: FlextCore.Types.Dict = {
            "base_url": "",  # Will be set per integration
            "timeout": 30,
            "max_retries": 3,
            "enable_circuit_breaker": True,
        }
        self._api_config = FlextApiConfig(**api_config_dict)

        # Initialize API client
        self._api_client = FlextApiClient(config=self._api_config)

    @property
    def logger(self) -> FlextCore.Logger:
        """Get logger with type narrowing."""
        assert self.logger is not None
        return self.logger

    def send_webhook_notification(
        self,
        webhook_url: str,
        event_type: str,
        event_data: FlextCore.Types.Dict,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Send webhook notification using flext-api.

        Args:
            webhook_url: Webhook endpoint URL
            event_type: Type of quality event (analysis_complete, threshold_violation, etc.)
            event_data: Event payload data

        Returns:
            FlextCore.Result with webhook response data

        """
        try:
            payload = {
                "event_type": event_type,
                "event_data": event_data,
                "service": "flext-quality",
                "version": "0.9.0",
            }

            # Use flext-api for HTTP request with retry logic
            response_result = self._api_client.post(
                url=webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            if response_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Webhook failed: {response_result.error}"
                )

            self.logger.info(f"Webhook sent successfully: {event_type}")
            # Cast HttpResponse to dict for type safety
            response_dict = cast("FlextCore.Types.Dict", response_result.value)
            return FlextCore.Result[FlextCore.Types.Dict].ok(response_dict)

        except Exception as e:
            self.logger.exception("Webhook notification failed")
            return FlextCore.Result[FlextCore.Types.Dict].fail(f"Webhook error: {e}")

    def send_slack_notification(
        self,
        webhook_url: str,
        message: str,
        severity: str = "info",
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Send Slack notification using flext-api.

        Args:
            webhook_url: Slack webhook URL
            message: Notification message
            severity: Message severity (info, warning, error)

        Returns:
            FlextCore.Result with Slack API response

        """
        try:
            # Format Slack message with severity colors
            color_map = {
                "info": "#36a64f",  # Green
                "warning": "#ff9900",  # Orange
                "error": "#ff0000",  # Red
            }

            payload = {
                "attachments": [
                    {
                        "color": color_map.get(severity, "#36a64f"),
                        "title": "FLEXT Quality Alert",
                        "text": message,
                        "footer": "flext-quality v0.9.0",
                    }
                ]
            }

            response_result = self._api_client.post(
                url=webhook_url,
                json=payload,
            )

            if response_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Slack notification failed: {response_result.error}"
                )

            self.logger.info("Slack notification sent successfully")
            return FlextCore.Result[FlextCore.Types.Dict].ok({"status": "sent"})

        except Exception as e:
            self.logger.exception("Slack notification failed")
            return FlextCore.Result[FlextCore.Types.Dict].fail(f"Slack error: {e}")

    def integrate_sonarqube(
        self,
        sonarqube_url: str,
        project_key: str,
        token: str,
        quality_data: FlextCore.Types.Dict,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Integrate with SonarQube using flext-api.

        Args:
            sonarqube_url: SonarQube server URL
            project_key: SonarQube project key
            token: SonarQube authentication token
            quality_data: Quality analysis data to send

        Returns:
            FlextCore.Result with SonarQube API response

        """
        try:
            # Construct SonarQube API endpoint
            api_url = f"{sonarqube_url}/api/measures/component"

            # Use flext-api with authentication header
            # Note: quality_data could be used for additional parameters or payload
            # For now, we use it to potentially override project_key
            component_key = quality_data.get("component", project_key)

            response_result = self._api_client.get(
                url=api_url,
                params={"component": component_key},
                headers={"Authorization": f"Bearer {token}"},
            )

            if response_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"SonarQube integration failed: {response_result.error}"
                )

            self.logger.info(
                f"SonarQube integration successful for project: {project_key}"
            )
            # Cast HttpResponse to dict for type safety
            response_dict = cast("FlextCore.Types.Dict", response_result.value)
            return FlextCore.Result[FlextCore.Types.Dict].ok(response_dict)

        except Exception as e:
            self.logger.exception("SonarQube integration failed")
            return FlextCore.Result[FlextCore.Types.Dict].fail(f"SonarQube error: {e}")

    def integrate_github_checks(
        self,
        github_api_url: str,
        repo: str,
        commit_sha: str,
        token: str,
        check_results: FlextCore.Types.Dict,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Integrate with GitHub Checks API using flext-api.

        Args:
            github_api_url: GitHub API base URL
            repo: Repository name (owner/repo)
            commit_sha: Commit SHA to attach check to
            token: GitHub authentication token
            check_results: Quality check results

        Returns:
            FlextCore.Result with GitHub API response

        """
        try:
            # Construct GitHub Checks API endpoint
            api_url = f"{github_api_url}/repos/{repo}/check-runs"

            payload = {
                "name": "FLEXT Quality Check",
                "head_sha": commit_sha,
                "status": "completed",
                "conclusion": check_results.get("conclusion", "success"),
                "output": {
                    "title": "Quality Analysis Results",
                    "summary": check_results.get(
                        "summary", "Quality analysis completed"
                    ),
                    "text": check_results.get("details", ""),
                },
            }

            response_result = self._api_client.post(
                url=api_url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            )

            if response_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"GitHub Checks integration failed: {response_result.error}"
                )

            self.logger.info(f"GitHub Checks updated for commit: {commit_sha}")
            # Cast HttpResponse to dict for type safety
            response_dict = cast("FlextCore.Types.Dict", response_result.value)
            return FlextCore.Result[FlextCore.Types.Dict].ok(response_dict)

        except Exception as e:
            self.logger.exception("GitHub Checks integration failed")
            return FlextCore.Result[FlextCore.Types.Dict].fail(f"GitHub error: {e}")

    def deliver_report_to_external_storage(
        self,
        storage_url: str,
        report_file: Path,
        api_key: str,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Deliver quality report to external storage using flext-api.

        Args:
            storage_url: External storage API URL
            report_file: Path to report file to upload
            api_key: Storage API key

        Returns:
            FlextCore.Result with upload response

        """
        try:
            # Read report file
            with report_file.open("rb") as f:
                report_content = f.read()

            # Use flext-api for file upload
            response_result = self._api_client.post(
                url=storage_url,
                files={"report": (report_file.name, report_content)},
                headers={"X-API-Key": api_key},
            )

            if response_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Report delivery failed: {response_result.error}"
                )

            self.logger.info(f"Report delivered successfully: {report_file.name}")
            # Cast HttpResponse to dict for type safety
            response_dict = cast("FlextCore.Types.Dict", response_result.value)
            return FlextCore.Result[FlextCore.Types.Dict].ok(response_dict)

        except Exception as e:
            self.logger.exception("Report delivery failed")
            return FlextCore.Result[FlextCore.Types.Dict].fail(f"Delivery error: {e}")

    def notify_on_threshold_violation(
        self,
        webhook_urls: FlextCore.Types.StringList,
        violation_data: FlextCore.Types.Dict,
    ) -> FlextCore.Result[list[FlextCore.Types.Dict]]:
        """Notify multiple webhooks of quality threshold violations.

        Args:
            webhook_urls: List of webhook URLs to notify
            violation_data: Threshold violation details

        Returns:
            FlextCore.Result with list of webhook responses

        """
        results: list[FlextCore.Types.Dict] = []

        for webhook_url in webhook_urls:
            result = self.send_webhook_notification(
                webhook_url=webhook_url,
                event_type="threshold_violation",
                event_data=violation_data,
            )

            if result.is_success:
                results.append(result.value)
            else:
                self.logger.warning(
                    f"Webhook notification failed for {webhook_url}: {result.error}"
                )

        if not results:
            return FlextCore.Result[list[FlextCore.Types.Dict]].fail(
                "All webhook notifications failed"
            )

        return FlextCore.Result[list[FlextCore.Types.Dict]].ok(results)


__all__ = ["FlextQualityIntegrations"]
