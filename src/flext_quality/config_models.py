"""Layer-zero schemas for YAML-owned quality configuration.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_quality/config_models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field


class FlextQualityModelsConfig:
    """Configuration declarations independent of the model facade."""

    class Policy(BaseModel):
        """Frozen, closed base of every YAML-owned quality policy model."""

        model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    class NotificationChannel(Policy):
        """One notification channel toggle."""

        enabled: bool = Field(description="Whether the channel delivers.")

    class NotificationThreshold(Policy):
        """An alert that fires at or above a count threshold."""

        enabled: bool = Field(description="Whether the alert fires.")
        threshold: int = Field(ge=0, description="Count that triggers the alert.")

    class NotificationToggle(Policy):
        """An alert that is only switched on or off."""

        enabled: bool = Field(description="Whether the alert fires.")

    class NotificationChannels(Policy):
        """Delivery channel toggles."""

        console: FlextQualityModelsConfig.NotificationChannel
        email: FlextQualityModelsConfig.NotificationChannel
        slack: FlextQualityModelsConfig.NotificationChannel
        webhook: FlextQualityModelsConfig.NotificationChannel

    class NotificationAlerts(Policy):
        """Alert thresholds and report toggles."""

        critical_issues: FlextQualityModelsConfig.NotificationThreshold
        quality_drop: FlextQualityModelsConfig.NotificationThreshold
        broken_links: FlextQualityModelsConfig.NotificationThreshold
        weekly_report: FlextQualityModelsConfig.NotificationToggle
        monthly_report: FlextQualityModelsConfig.NotificationToggle

    class NotificationEmail(Policy):
        """SMTP relay delivery settings."""

        smtp_server: str = Field(description="SMTP relay host.")
        smtp_port: int = Field(ge=1, le=65535, description="SMTP relay port.")
        username: str = Field(description="SMTP login name.")
        password: str | None = Field(description="SMTP password; absent until set.")
        from_address: str = Field(description="Sender address.")
        to_addresses: Sequence[str] = Field(description="Recipient addresses.")

    class NotificationSlack(Policy):
        """Slack incoming-webhook delivery settings."""

        webhook_url: str = Field(description="Slack incoming-webhook URL.")
        channel: str = Field(description="Slack channel name.")
        username: str = Field(description="Bot display name.")

    class NotificationWebhook(Policy):
        """Generic webhook delivery settings."""

        url: str = Field(description="Webhook URL.")
        headers: Mapping[str, str] = Field(description="Extra request headers.")
        timeout: int = Field(ge=1, description="Request timeout in seconds.")

    class Notifications(Policy):
        """Documentation-quality notification policy."""

        enabled: bool = Field(description="Whether any notification is sent.")
        channels: FlextQualityModelsConfig.NotificationChannels
        alerts: FlextQualityModelsConfig.NotificationAlerts
        email: FlextQualityModelsConfig.NotificationEmail
        slack: FlextQualityModelsConfig.NotificationSlack
        webhook: FlextQualityModelsConfig.NotificationWebhook

    class QualityConfigNamespace(BaseModel):
        """Frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = ConfigDict(extra="allow", frozen=True)

        notifications: FlextQualityModelsConfig.Notifications = Field(
            description="Documentation-quality notification policy.",
        )


__all__: list[str] = ["FlextQualityModelsConfig"]
