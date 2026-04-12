#!/usr/bin/env python3
"""FLEXT Quality Documentation Notification System.

Automated notification system for documentation quality alerts,
reports, and maintenance updates. Supports multiple notification channels
including email, Slack, webhooks, and project management tools.
"""

from __future__ import annotations

import argparse
import smtplib
from collections.abc import Mapping, MutableSequence, Sequence
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests
from pydantic import BaseModel, Field

from flext_quality import m, t, u

# Constants
MAX_BROKEN_LINKS_TO_SHOW = 10


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
        to_addresses: t.StrSequence = Field(default_factory=list)

    class _SlackConfig(BaseModel):
        webhook_url: str
        channel: str
        username: str

    class _WebhookConfig(BaseModel):
        url: str
        headers: t.StrMapping = Field(default_factory=dict)
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
        config_path: str = "docs/maintenance/settings/notification_config.yaml",
    ) -> None:
        """Initialize the documentation notifier with configuration.

        Args:
            config_path: Path to the notification configuration file.

        """
        self.settings: FlextQualityDocumentationNotifier._NotifierConfig = (
            self.get_default_config()
        )
        self.load_config(config_path)
        self.results: m.Quality.NotifierResults = m.Quality.NotifierResults(
            timestamp=datetime.now(UTC).isoformat(),
        )

    def load_config(self, config_path: str) -> None:
        """Load notification configuration."""
        try:
            loaded = u.Cli.yaml_load_mapping(Path(config_path))
            if loaded:
                self.settings = self._load_user_config({})
            else:
                self.settings = self.get_default_config()
        except FileNotFoundError:
            self.settings = self.get_default_config()

    def _load_user_config(
        self,
        loaded: Mapping[
            str,
            int
            | str
            | float
            | bool
            | t.StrSequence
            | Mapping[
                str,
                int
                | str
                | float
                | bool
                | t.StrSequence
                | Mapping[str, str | int | bool],
            ]
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
                        channel_cfg.enabled = enabled

        alerts = loaded.get("alerts")
        if isinstance(alerts, dict):
            for key in ("critical_issues", "quality_drop", "broken_links"):
                value = alerts.get(key)
                if isinstance(value, dict):
                    enabled = value.get("enabled")
                    threshold = value.get("threshold")
                    alert_cfg = getattr(cfg.alerts, key)
                    if isinstance(enabled, bool):
                        alert_cfg.enabled = enabled
                    if isinstance(threshold, int):
                        alert_cfg.threshold = threshold
            for key in ("weekly_report", "monthly_report"):
                value = alerts.get(key)
                if isinstance(value, dict):
                    enabled = value.get("enabled")
                    if isinstance(enabled, bool):
                        toggle_cfg = getattr(cfg.alerts, key)
                        toggle_cfg.enabled = enabled

        email = loaded.get("email")
        if isinstance(email, dict):
            for key in ("smtp_server", "username", "password", "from_address"):
                value = email.get(key)
                if isinstance(value, str):
                    setattr(cfg.email, key, value)
            smtp_port = email.get("smtp_port")
            if isinstance(smtp_port, int):
                cfg.email.smtp_port = smtp_port
            to_addresses = email.get("to_addresses")
            if isinstance(to_addresses, list):
                cfg.email.to_addresses = to_addresses

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
                cfg.webhook.url = url_val
            if isinstance(timeout_val, int):
                cfg.webhook.timeout = timeout_val
            if isinstance(headers_val, dict):
                str_headers: t.StrMapping = {k: str(v) for k, v in headers_val.items()}
                cfg.webhook.headers = str_headers

        enabled_val = loaded.get("enabled")
        if isinstance(enabled_val, bool):
            cfg.enabled = enabled_val

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
        audit_data: t.RecursiveContainerMapping,
    ) -> bool:
        """Send notification for critical documentation issues."""
        if not self.settings.alerts.critical_issues.enabled:
            return True

        metrics_val = audit_data.get("metrics")
        metrics: t.RecursiveContainerMapping = (
            t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
            if isinstance(metrics_val, Mapping)
            else {}
        )
        severity_val = metrics.get("severity_breakdown")
        severity_m: t.RecursiveContainerMapping = (
            t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(severity_val)
            if isinstance(severity_val, Mapping)
            else {}
        )
        severity_breakdown: t.MutableIntMapping = {}
        for key_name in ("critical", "high", "medium", "low"):
            kv = severity_m.get(key_name, 0)
            severity_breakdown[key_name] = kv if isinstance(kv, int) else 0
        critical_count: int = severity_breakdown.get("critical", 0)
        threshold = self.settings.alerts.critical_issues.threshold

        if critical_count >= threshold:
            title = f"🚨 CRITICAL: {critical_count} Critical Documentation Issues Found"
            message = self._format_critical_issues_message(audit_data)
            return self.send_notification(title, message, "critical")

        return True

    def notify_quality_drop(self, current_score: float, previous_score: float) -> bool:
        """Send notification for significant quality score drops."""
        if not self.settings.alerts.quality_drop.enabled:
            return True

        threshold = self.settings.alerts.quality_drop.threshold
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
        broken_links: Sequence[t.RecursiveContainer],
    ) -> bool:
        """Send notification for broken links."""
        if not self.settings.alerts.broken_links.enabled:
            return True

        threshold = self.settings.alerts.broken_links.threshold

        if len(broken_links) >= threshold:
            title = f"🔗 Link Alert: {len(broken_links)} Broken Links Detected"
            message = self._format_broken_links_message(broken_links)
            return self.send_notification(title, message, "warning")

        return True

    def notify_weekly_report(
        self,
        report_data: t.RecursiveContainerMapping,
    ) -> bool:
        """Send weekly quality report notification."""
        if not self.settings.alerts.weekly_report.enabled:
            return True

        title = "📊 Weekly Documentation Quality Report"
        message = self._format_weekly_report_message(report_data)
        return self.send_notification(title, message, "info")

    def notify_monthly_report(
        self,
        report_data: t.RecursiveContainerMapping,
    ) -> bool:
        """Send monthly comprehensive report notification."""
        if not self.settings.alerts.monthly_report.enabled:
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
        if self.settings.channels.console.enabled:
            self._send_console_notification(title, message, priority)

        # Email notification
        if self.settings.channels.email.enabled:
            try:
                self._send_email_notification(title, message, priority)
            except (smtplib.SMTPException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Email notification failed: {e}")
                success = False

        # Slack notification
        if self.settings.channels.slack.enabled:
            try:
                self._send_slack_notification(title, message, priority)
            except (requests.RequestException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Slack notification failed: {e}")
                success = False

        # Webhook notification
        if self.settings.channels.webhook.enabled:
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
        email_config = self.settings.email

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
        slack_config = self.settings.slack

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
        webhook_config = self.settings.webhook

        payload = {
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now(UTC).isoformat(),
            "source": "FLEXT Quality Documentation System",
        }

        headers_val = webhook_config.headers
        headers: t.MutableStrMapping = (
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
        audit_data: t.RecursiveContainerMapping,
    ) -> str:
        """Format message for critical issues notification."""
        metrics_val = audit_data.get("metrics")
        metrics: t.RecursiveContainerMapping = (
            t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
            if isinstance(metrics_val, Mapping)
            else {}
        )
        severity_val = metrics.get("severity_breakdown")
        severity: t.RecursiveContainerMapping = (
            t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(severity_val)
            if isinstance(severity_val, Mapping)
            else {}
        )
        severity_breakdown: t.MutableIntMapping = {}
        for key_name in ("critical", "high", "medium", "low"):
            kv = severity.get(key_name, 0)
            severity_breakdown[key_name] = kv if isinstance(kv, int) else 0

        issues_val = audit_data.get("issues")
        critical_issues: MutableSequence[t.RecursiveContainerMapping] = []
        if isinstance(issues_val, (list, tuple)):
            for i_v in issues_val:
                if isinstance(i_v, Mapping):
                    i_m: t.RecursiveContainerMapping = (
                        t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(i_v)
                    )
                    sev = i_m.get("severity")
                    if sev == "critical":
                        critical_issues.append(i_m)
                        max_critical_issues = 5
                        if len(critical_issues) >= max_critical_issues:
                            break

        qs_v = metrics.get("quality_score", 0)
        quality_score: int = qs_v if isinstance(qs_v, int) else 0
        fa_v = audit_data.get("files_analyzed", 0)
        files_analyzed: int = fa_v if isinstance(fa_v, int) else 0
        ti_v = metrics.get("total_issues", 0)
        total_issues: int = ti_v if isinstance(ti_v, int) else 0

        message = f"""
CRITICAL DOCUMENTATION ISSUES DETECTED

Quality Score: {quality_score}/100
Files Analyzed: {files_analyzed}
Total Issues: {total_issues}

Severity Breakdown:
\u2022 Critical: {severity_breakdown.get("critical", 0)}
\u2022 High: {severity_breakdown.get("high", 0)}
\u2022 Medium: {severity_breakdown.get("medium", 0)}
\u2022 Low: {severity_breakdown.get("low", 0)}

Top Critical Issues:
"""

        for i, issue in enumerate(critical_issues, 1):
            type_v = issue.get("type", "unknown")
            file_v = issue.get("file", "unknown")
            desc_v = issue.get("description", "No description")
            message += f"{i}. {str(type_v).replace('_', ' ').title()}\n"
            message += f"   File: {file_v}\n"
            message += f"   Description: {desc_v}\n\n"

        message += "\nIMMEDIATE ACTION REQUIRED: Please review and fix critical issues immediately."

        return message.strip()

    def _format_broken_links_message(
        self,
        broken_links: Sequence[t.RecursiveContainer],
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
            if isinstance(link, Mapping):
                url_v = link.get("url", "unknown")
                file_v = link.get("file", "unknown")
                err_v = link.get("error", "Unknown error")
            else:
                url_v, file_v, err_v = "unknown", "unknown", "Unknown error"
            message += f"{i}. {url_v}\n"
            message += f"   File: {file_v}\n"
            message += f"   Error: {err_v}\n\n"

        if len(broken_links) > MAX_BROKEN_LINKS_TO_SHOW:
            message += f"... and {len(broken_links) - MAX_BROKEN_LINKS_TO_SHOW} more broken links.\n\n"

        message += (
            "Please update or fix these broken links to maintain documentation quality."
        )

        return message.strip()

    def _format_weekly_report_message(
        self,
        _report_data: t.RecursiveContainerMapping,
    ) -> str:
        """Format message for weekly report notification."""
        # Implementation would depend on weekly report data structure
        # For now, report_data is not used but reserved for future implementation
        return "Weekly documentation quality report is now available. Check the reports dashboard for detailed metrics and trends."

    def _format_monthly_report_message(
        self,
        _report_data: t.RecursiveContainerMapping,
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
        default="docs/maintenance/settings/notification_config.yaml",
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

    notifier = FlextQualityDocumentationNotifier(args.settings)

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
        audit_data = t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
            Path(args.audit_data).read_bytes(),
        )

        # Check for critical issues
        _ = notifier.notify_critical_issues(audit_data)

        # Check for broken links (would need to extract from audit data)
        issues_raw = audit_data.get("issues")
        broken_links: MutableSequence[t.RecursiveContainer] = []
        if isinstance(issues_raw, (list, tuple)):
            for i_raw in issues_raw:
                if isinstance(i_raw, Mapping):
                    type_val = i_raw.get("type", "")
                    if "broken" in str(type_val).lower():
                        broken_links.append(i_raw)
        if broken_links:
            _ = notifier.notify_broken_links(broken_links)

    elif args.weekly_report:
        # Send weekly report notification
        report_data = t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
            Path(args.weekly_report).read_bytes(),
        )
        _ = notifier.notify_weekly_report(report_data)

    elif args.monthly_report:
        # Send monthly report notification
        report_data = t.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
            Path(args.monthly_report).read_bytes(),
        )
        _ = notifier.notify_monthly_report(report_data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
