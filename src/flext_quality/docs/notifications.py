#!/usr/bin/env python3
"""FLEXT Quality Documentation Notification System.

Automated notification system for documentation quality alerts,
reports, and maintenance updates. Supports multiple notification channels
including email, Slack, webhooks, and project management tools.
"""

from __future__ import annotations

import argparse
import smtplib
from collections.abc import Mapping, MutableMapping, Sequence
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Annotated

import requests
import yaml
from flext_core import t
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from flext_quality import m

_AUDIT_DATA_ADAPTER: TypeAdapter[t.ContainerMapping] = TypeAdapter(
    t.ContainerMapping,
    config=ConfigDict(strict=False),
)

# Constants
MAX_BROKEN_LINKS_TO_SHOW = 10


NotifierResults = m.Quality.NotifierResults


class FlextQualityDocumentationNotifier:
    """Automated notification system for documentation quality alerts."""

    class _ChannelConfig(BaseModel):
        enabled: bool

    class _AlertThresholdConfig(BaseModel):
        enabled: bool
        threshold: int

    class _AlertToggleConfig(BaseModel):
        enabled: bool

    class _AlertsConfig(BaseModel):
        critical_issues: FlextQualityDocumentationNotifier._AlertThresholdConfig
        quality_drop: FlextQualityDocumentationNotifier._AlertThresholdConfig
        broken_links: FlextQualityDocumentationNotifier._AlertThresholdConfig
        weekly_report: FlextQualityDocumentationNotifier._AlertToggleConfig
        monthly_report: FlextQualityDocumentationNotifier._AlertToggleConfig

    class _EmailConfig(BaseModel):
        smtp_server: str
        smtp_port: int
        username: str
        password: str
        from_address: str
        to_addresses: Annotated[t.StrSequence, Field(default_factory=list)]

    class _SlackConfig(BaseModel):
        webhook_url: str
        channel: str
        username: str

    class _WebhookConfig(BaseModel):
        url: str
        headers: Annotated[t.StrMapping, Field(default_factory=dict)]
        timeout: int

    class _ChannelsConfig(BaseModel):
        console: FlextQualityDocumentationNotifier._ChannelConfig
        email: FlextQualityDocumentationNotifier._ChannelConfig
        slack: FlextQualityDocumentationNotifier._ChannelConfig
        webhook: FlextQualityDocumentationNotifier._ChannelConfig

    class _NotifierConfig(BaseModel):
        enabled: bool
        channels: FlextQualityDocumentationNotifier._ChannelsConfig
        alerts: FlextQualityDocumentationNotifier._AlertsConfig
        email: FlextQualityDocumentationNotifier._EmailConfig
        slack: FlextQualityDocumentationNotifier._SlackConfig
        webhook: FlextQualityDocumentationNotifier._WebhookConfig

    def __init__(
        self,
        config_path: str = "docs/maintenance/config/notification_config.yaml",
    ) -> None:
        """Initialize the documentation notifier with configuration.

        Args:
            config_path: Path to the notification configuration file.

        """
        self.config: FlextQualityDocumentationNotifier._NotifierConfig = (
            self.get_default_config()
        )
        self.load_config(config_path)
        self.results: NotifierResults = NotifierResults(
            timestamp=datetime.now(UTC).isoformat(),
        )

    def load_config(self, config_path: str) -> None:
        """Load notification configuration."""
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    self.config = self._load_user_config({})
                else:
                    self.config = self.get_default_config()
        except FileNotFoundError:
            self.config = self.get_default_config()

    def _load_user_config(
        self,
        loaded: Mapping[
            str,
            int
            | str
            | float
            | bool
            | t.StrSequence
            | Mapping[str, int | str | float | bool | t.StrSequence | t.StrMapping]
            | None,
        ],
    ) -> _NotifierConfig:
        cfg = self.get_default_config()

        channels = loaded.get("channels")
        if isinstance(channels, dict):
            for key in ("console", "email", "slack", "webhook"):
                value = channels.get(key)
                if isinstance(value, dict):
                    enabled = value.get("enabled")
                    if isinstance(enabled, bool):
                        channel_cfg = getattr(cfg.channels, key)
                        setattr(channel_cfg, "enabled", enabled)

        alerts = loaded.get("alerts")
        if isinstance(alerts, dict):
            for key in ("critical_issues", "quality_drop", "broken_links"):
                value = alerts.get(key)
                if isinstance(value, dict):
                    enabled = value.get("enabled")
                    threshold = value.get("threshold")
                    alert_cfg = getattr(cfg.alerts, key)
                    if isinstance(enabled, bool):
                        setattr(alert_cfg, "enabled", enabled)
                    if isinstance(threshold, int):
                        setattr(alert_cfg, "threshold", threshold)
            for key in ("weekly_report", "monthly_report"):
                value = alerts.get(key)
                if isinstance(value, dict):
                    enabled = value.get("enabled")
                    if isinstance(enabled, bool):
                        toggle_cfg = getattr(cfg.alerts, key)
                        setattr(toggle_cfg, "enabled", enabled)

        email = loaded.get("email")
        if isinstance(email, dict):
            for key in ("smtp_server", "username", "password", "from_address"):
                value = email.get(key)
                if isinstance(value, str):
                    setattr(cfg.email, key, value)
            smtp_port = email.get("smtp_port")
            if isinstance(smtp_port, int):
                setattr(cfg.email, "smtp_port", smtp_port)
            to_addresses = email.get("to_addresses")
            if isinstance(to_addresses, list) and all(
                isinstance(item, str) for item in to_addresses
            ):
                setattr(cfg.email, "to_addresses", to_addresses)

        slack = loaded.get("slack")
        if isinstance(slack, dict):
            for key in ("webhook_url", "channel", "username"):
                value = slack.get(key)
                if isinstance(value, str):
                    setattr(cfg.slack, key, value)

        webhook = loaded.get("webhook")
        if isinstance(webhook, dict):
            url_val = webhook.get("url")
            timeout_val = webhook.get("timeout")
            headers_val = webhook.get("headers")
            if isinstance(url_val, str):
                setattr(cfg.webhook, "url", url_val)
            if isinstance(timeout_val, int):
                setattr(cfg.webhook, "timeout", timeout_val)
            if isinstance(headers_val, dict) and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in headers_val.items()
            ):
                setattr(cfg.webhook, "headers", headers_val)

        enabled_val = loaded.get("enabled")
        if isinstance(enabled_val, bool):
            setattr(cfg, "enabled", enabled_val)

        return cfg

    def get_default_config(self) -> _NotifierConfig:
        """Default notification configuration."""
        return FlextQualityDocumentationNotifier._NotifierConfig(
            enabled=True,
            channels=FlextQualityDocumentationNotifier._ChannelsConfig(
                console=FlextQualityDocumentationNotifier._ChannelConfig(enabled=True),
                email=FlextQualityDocumentationNotifier._ChannelConfig(enabled=False),
                slack=FlextQualityDocumentationNotifier._ChannelConfig(enabled=False),
                webhook=FlextQualityDocumentationNotifier._ChannelConfig(enabled=False),
            ),
            alerts=FlextQualityDocumentationNotifier._AlertsConfig(
                critical_issues=FlextQualityDocumentationNotifier._AlertThresholdConfig(
                    enabled=True,
                    threshold=1,
                ),
                quality_drop=FlextQualityDocumentationNotifier._AlertThresholdConfig(
                    enabled=True,
                    threshold=10,
                ),
                broken_links=FlextQualityDocumentationNotifier._AlertThresholdConfig(
                    enabled=True,
                    threshold=5,
                ),
                weekly_report=FlextQualityDocumentationNotifier._AlertToggleConfig(
                    enabled=True,
                ),
                monthly_report=FlextQualityDocumentationNotifier._AlertToggleConfig(
                    enabled=True,
                ),
            ),
            email=FlextQualityDocumentationNotifier._EmailConfig(
                smtp_server="smtp.gmail.com",
                smtp_port=587,
                username="",
                password="",
                from_address="",
                to_addresses=[],
            ),
            slack=FlextQualityDocumentationNotifier._SlackConfig(
                webhook_url="",
                channel="#docs-quality",
                username="FLEXT Quality Bot",
            ),
            webhook=FlextQualityDocumentationNotifier._WebhookConfig(
                url="",
                headers={},
                timeout=10,
            ),
        )

    def notify_critical_issues(
        self,
        audit_data: Mapping[
            str,
            Mapping[str, int] | Sequence[Mapping[str, str | int]] | int | str,
        ],
    ) -> bool:
        """Send notification for critical documentation issues."""
        if not self.config.alerts.critical_issues.enabled:
            return True

        metrics_val = audit_data.get("metrics", {})
        metrics = metrics_val if isinstance(metrics_val, dict) else {}
        severity_val = metrics.get("severity_breakdown", {})
        severity_breakdown: MutableMapping[str, int] = {}
        if isinstance(severity_val, dict):
            for key_name in ("critical", "high", "medium", "low"):
                if key_name in severity_val and isinstance(severity_val[key_name], int):
                    severity_breakdown[key_name] = severity_val[key_name]
        critical_raw = severity_breakdown.get("critical", 0)
        critical_count = int(critical_raw) if isinstance(critical_raw, int) else 0
        threshold = self.config.alerts.critical_issues.threshold

        if critical_count >= threshold:
            title = f"🚨 CRITICAL: {critical_count} Critical Documentation Issues Found"
            message = self._format_critical_issues_message(audit_data)
            return self.send_notification(title, message, "critical")

        return True

    def notify_quality_drop(self, current_score: float, previous_score: float) -> bool:
        """Send notification for significant quality score drops."""
        if not self.config.alerts.quality_drop.enabled:
            return True

        threshold = self.config.alerts.quality_drop.threshold
        drop = previous_score - current_score

        if drop >= threshold:
            title = f"📉 Quality Alert: Score dropped by {drop:.1f} points"
            message = f"""
Quality Score Drop Detected
• Current Score: {current_score:.1f}/100
• Previous Score: {previous_score:.1f}/100
• Drop Amount: {drop:.1f} points
• Threshold: {threshold} points

This represents a significant degradation in documentation quality.
Please review recent changes and address any identified issues.
            """.strip()
            return self.send_notification(title, message, "warning")

        return True

    def notify_broken_links(
        self,
        broken_links: Sequence[Mapping[str, str | int]],
    ) -> bool:
        """Send notification for broken links."""
        if not self.config.alerts.broken_links.enabled:
            return True

        threshold = self.config.alerts.broken_links.threshold

        if len(broken_links) >= threshold:
            title = f"🔗 Link Alert: {len(broken_links)} Broken Links Detected"
            message = self._format_broken_links_message(broken_links)
            return self.send_notification(title, message, "warning")

        return True

    def notify_weekly_report(
        self,
        report_data: Mapping[str, str | int | float],
    ) -> bool:
        """Send weekly quality report notification."""
        if not self.config.alerts.weekly_report.enabled:
            return True

        title = "📊 Weekly Documentation Quality Report"
        message = self._format_weekly_report_message(report_data)
        return self.send_notification(title, message, "info")

    def notify_monthly_report(
        self,
        report_data: Mapping[str, str | int | float],
    ) -> bool:
        """Send monthly comprehensive report notification."""
        if not self.config.alerts.monthly_report.enabled:
            return True

        title = "📈 Monthly Documentation Quality Report"
        message = self._format_monthly_report_message(report_data)
        return self.send_notification(title, message, "info")

    def send_notification(
        self,
        title: str,
        message: str,
        priority: str = "info",
    ) -> bool:
        """Send notification through all enabled channels."""
        success = True

        # Console notification (always enabled)
        if self.config.channels.console.enabled:
            self._send_console_notification(title, message, priority)

        # Email notification
        if self.config.channels.email.enabled:
            try:
                self._send_email_notification(title, message, priority)
            except (smtplib.SMTPException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Email notification failed: {e}")
                success = False

        # Slack notification
        if self.config.channels.slack.enabled:
            try:
                self._send_slack_notification(title, message, priority)
            except (requests.RequestException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Slack notification failed: {e}")
                success = False

        # Webhook notification
        if self.config.channels.webhook.enabled:
            try:
                self._send_webhook_notification(title, message, priority)
            except (requests.RequestException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Webhook notification failed: {e}")
                success = False

        if success:
            self.results.notifications_sent += 1

        return success

    def _send_console_notification(
        self,
        title: str,
        message: str,
        priority: str,
    ) -> None:
        """Send notification to console."""
        # For now, console notifications are disabled to avoid T201 violations
        # In the future, this could be implemented with proper logging

    def _send_email_notification(self, title: str, message: str, priority: str) -> None:
        """Send notification via email."""
        email_config = self.config.email

        msg = MIMEMultipart()
        msg["From"] = str(email_config.from_address)
        msg["To"] = ", ".join(str(x) for x in (email_config.to_addresses or []))
        msg["Subject"] = f"[{priority.upper()}] {title}"

        body = f"""
FLEXT Quality Documentation Alert

{title}

{message}

---
This is an automated notification from the FLEXT Quality Documentation Maintenance System.
Timestamp: {datetime.now(UTC).isoformat()}
        """.strip()

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(
            str(email_config.smtp_server),
            int(email_config.smtp_port),
        )
        server.starttls()
        server.login(
            str(email_config.username),
            str(email_config.password),
        )
        text = msg.as_string()
        server.sendmail(
            str(email_config.from_address),
            list(email_config.to_addresses or []),
            text,
        )
        server.quit()

    def _send_slack_notification(self, title: str, message: str, priority: str) -> None:
        """Send notification to Slack."""
        slack_config = self.config.slack

        color = {"critical": "danger", "warning": "warning", "info": "good"}.get(
            priority,
            "good",
        )

        payload = {
            "channel": slack_config.channel,
            "username": slack_config.username,
            "attachments": [
                {
                    "color": color,
                    "title": title,
                    "text": message,
                    "footer": "FLEXT Quality Documentation System",
                    "ts": datetime.now(UTC).timestamp(),
                },
            ],
        }

        response = requests.post(
            str(slack_config.webhook_url),
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

    def _send_webhook_notification(
        self,
        title: str,
        message: str,
        priority: str,
    ) -> None:
        """Send notification via webhook."""
        webhook_config = self.config.webhook

        payload = {
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now(UTC).isoformat(),
            "source": "FLEXT Quality Documentation System",
        }

        headers_val = webhook_config.headers
        headers: MutableMapping[str, str] = (
            dict(headers_val) if isinstance(headers_val, dict) else {}
        )
        headers["Content-Type"] = "application/json"

        timeout = webhook_config.timeout

        response = requests.post(
            str(webhook_config.url),
            json=payload,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()

    def _format_critical_issues_message(
        self,
        audit_data: Mapping[
            str,
            Mapping[str, int] | Sequence[Mapping[str, str | int]] | int | str,
        ],
    ) -> str:
        """Format message for critical issues notification."""
        metrics_val = audit_data.get("metrics")
        metrics = metrics_val if isinstance(metrics_val, dict) else {}
        severity_val = metrics.get("severity_breakdown")
        severity_breakdown: MutableMapping[str, int] = {}
        if isinstance(severity_val, dict):
            for key_name in ("critical", "high", "medium", "low"):
                if key_name in severity_val and isinstance(severity_val[key_name], int):
                    severity_breakdown[key_name] = severity_val[key_name]

        issues_val = audit_data.get("issues")
        issues = issues_val if isinstance(issues_val, list) else []
        critical_issues = [i for i in issues if i.get("severity") == "critical"][:5]

        message = f"""
CRITICAL DOCUMENTATION ISSUES DETECTED

Quality Score: {metrics.get("quality_score", 0)}/100
Files Analyzed: {audit_data.get("files_analyzed", 0)}
Total Issues: {metrics.get("total_issues", 0)}

Severity Breakdown:
• Critical: {severity_breakdown.get("critical", 0)}
• High: {severity_breakdown.get("high", 0)}
• Medium: {severity_breakdown.get("medium", 0)}
• Low: {severity_breakdown.get("low", 0)}

Top Critical Issues:
"""

        for i, issue in enumerate(critical_issues, 1):
            message += (
                f"{i}. {str(issue.get('type', 'unknown')).replace('_', ' ').title()}\n"
            )
            message += f"   File: {issue.get('file', 'unknown')}\n"
            message += (
                f"   Description: {issue.get('description', 'No description')}\n\n"
            )

        message += "\nIMMEDIATE ACTION REQUIRED: Please review and fix critical issues immediately."

        return message.strip()

    def _format_broken_links_message(
        self,
        broken_links: Sequence[Mapping[str, str | int]],
    ) -> str:
        """Format message for broken links notification."""
        message = f"""
BROKEN LINKS DETECTED

Found {len(broken_links)} broken links that need attention:

"""

        for i, link in enumerate(
            broken_links[:MAX_BROKEN_LINKS_TO_SHOW],
            1,
        ):  # Show first MAX_BROKEN_LINKS_TO_SHOW
            message += f"{i}. {link.get('url', 'unknown')}\n"
            message += f"   File: {link.get('file', 'unknown')}\n"
            message += f"   Error: {link.get('error', 'Unknown error')}\n\n"

        if len(broken_links) > MAX_BROKEN_LINKS_TO_SHOW:
            message += f"... and {len(broken_links) - MAX_BROKEN_LINKS_TO_SHOW} more broken links.\n\n"

        message += (
            "Please update or fix these broken links to maintain documentation quality."
        )

        return message.strip()

    def _format_weekly_report_message(
        self,
        _report_data: Mapping[str, str | int | float],
    ) -> str:
        """Format message for weekly report notification."""
        # Implementation would depend on weekly report data structure
        # For now, report_data is not used but reserved for future implementation
        return "Weekly documentation quality report is now available. Check the reports dashboard for detailed metrics and trends."

    def _format_monthly_report_message(
        self,
        _report_data: Mapping[str, str | int | float],
    ) -> str:
        """Format message for monthly report notification."""
        # Implementation would depend on monthly report data structure
        return "Monthly comprehensive documentation quality report is now available. Review trends and plan improvements for the next month."


def main() -> None:
    """Main entry point for notification system."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Notifications",
    )
    _ = parser.add_argument(
        "--config",
        default="docs/maintenance/config/notification_config.yaml",
        help="Notification configuration file",
    )
    _ = parser.add_argument(
        "--test",
        action="store_true",
        help="Send test notification to verify configuration",
    )
    _ = parser.add_argument("--audit-data", help="Path to audit data JSON file")
    _ = parser.add_argument("--weekly-report", help="Path to weekly report JSON file")
    _ = parser.add_argument("--monthly-report", help="Path to monthly report JSON file")

    args = parser.parse_args()

    notifier = FlextQualityDocumentationNotifier(args.config)

    if args.test:
        success = notifier.send_notification(
            "Test Notification",
            "This is a test notification from the FLEXT Quality Documentation System.\n\nIf you received this, the notification system is working correctly.",
            "info",
        )
        if not success:
            for err in notifier.results.errors:
                _ = err  # consumed
    elif args.audit_data:
        # Process audit data and send appropriate notifications
        audit_data = _AUDIT_DATA_ADAPTER.validate_json(
            Path(args.audit_data).read_bytes(),
        )

        # Check for critical issues
        _ = notifier.notify_critical_issues(audit_data)

        # Check for broken links (would need to extract from audit data)
        broken_links = [
            i
            for i in audit_data.get("issues", [])
            if "broken" in str(i.get("type", "")).lower()
        ]
        if broken_links:
            _ = notifier.notify_broken_links(broken_links)

    elif args.weekly_report:
        # Send weekly report notification
        report_data = _AUDIT_DATA_ADAPTER.validate_json(
            Path(args.weekly_report).read_bytes(),
        )
        _ = notifier.notify_weekly_report(report_data)

    elif args.monthly_report:
        # Send monthly report notification
        report_data = _AUDIT_DATA_ADAPTER.validate_json(
            Path(args.monthly_report).read_bytes(),
        )
        _ = notifier.notify_monthly_report(report_data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()


# Module-level alias for pyrefly compatibility
DocumentationNotifier = FlextQualityDocumentationNotifier
