"""FLEXT Quality Documentation Notification System.

Automated notification system for documentation quality alerts,
reports, and maintenance updates. Supports multiple notification channels
including email, Slack, webhooks, and project management tools.
"""

from __future__ import annotations

import smtplib
from collections.abc import Mapping, MutableSequence
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Annotated, override

import requests

from flext_cli import cli
from flext_quality import c, m, p, r, s, t, u


class FlextQualityDocumentationNotifier:
    """Automated notification system for documentation quality alerts."""

    class _ChannelConfig(m.BaseModel):
        enabled: bool

    class _AlertThresholdConfig(m.BaseModel):
        enabled: bool
        threshold: int

    class _AlertToggleConfig(m.BaseModel):
        enabled: bool

    class _AlertsConfig(m.BaseModel):
        critical_issues: FlextQualityDocumentationNotifier._AlertThresholdConfig
        quality_drop: FlextQualityDocumentationNotifier._AlertThresholdConfig
        broken_links: FlextQualityDocumentationNotifier._AlertThresholdConfig
        weekly_report: FlextQualityDocumentationNotifier._AlertToggleConfig
        monthly_report: FlextQualityDocumentationNotifier._AlertToggleConfig

    class _EmailConfig(m.BaseModel):
        smtp_server: str
        smtp_port: int
        username: str
        password: str
        from_address: str
        to_addresses: t.StrSequence = u.Field(default_factory=tuple)

    class _SlackConfig(m.BaseModel):
        webhook_url: str
        channel: str
        username: str

    class _WebhookConfig(m.BaseModel):
        url: str
        headers: t.StrMapping = u.Field(default_factory=dict)
        timeout: int

    class _ChannelsConfig(m.BaseModel):
        console: FlextQualityDocumentationNotifier._ChannelConfig
        email: FlextQualityDocumentationNotifier._ChannelConfig
        slack: FlextQualityDocumentationNotifier._ChannelConfig
        webhook: FlextQualityDocumentationNotifier._ChannelConfig

    class _NotifierConfig(m.BaseModel):
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
        # Wire config_path: load YAML overrides into the typed notifier config.
        loaded = u.Cli.yaml_load_mapping(Path(config_path))
        self._config = self._load_user_config(loaded)
        self.results: m.Quality.NotifierResults = m.Quality.NotifierResults(
            timestamp=u.now().isoformat(),
        )

    def _load_user_config(
        self,
        loaded: t.JsonMapping,
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
                cfg.email.to_addresses = [
                    address for address in to_addresses if isinstance(address, str)
                ]

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
        audit_data: t.JsonMapping,
    ) -> bool:
        """Send notification for critical documentation issues."""
        if not self._config.alerts.critical_issues.enabled:
            return True

        metrics_val = audit_data.get("metrics")
        metrics: t.JsonMapping = (
            t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
            if isinstance(metrics_val, Mapping)
            else {}
        )
        severity_val = metrics.get("severity_breakdown")
        severity_m: t.JsonMapping = (
            t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(severity_val)
            if isinstance(severity_val, Mapping)
            else {}
        )
        severity_breakdown: t.MutableIntMapping = {}
        for key_name in ("critical", "high", "medium", "low"):
            kv = severity_m.get(key_name, 0)
            severity_breakdown[key_name] = kv if isinstance(kv, int) else 0
        critical_count: int = severity_breakdown.get("critical", 0)
        threshold = self._config.alerts.critical_issues.threshold

        if critical_count >= threshold:
            title = f"🚨 CRITICAL: {critical_count} Critical Documentation Issues Found"
            message = self._format_critical_issues_message(audit_data)
            return self.send_notification(
                title,
                message,
                c.Quality.NotificationPriority.CRITICAL.value,
            )

        return True

    def notify_quality_drop(self, current_score: float, previous_score: float) -> bool:
        """Send notification for significant quality score drops."""
        if not self._config.alerts.quality_drop.enabled:
            return True

        threshold = self._config.alerts.quality_drop.threshold
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
            return self.send_notification(
                title,
                message,
                c.Quality.NotificationPriority.WARNING.value,
            )

        return True

    def notify_broken_links(
        self,
        broken_links: t.JsonList,
    ) -> bool:
        """Send notification for broken links."""
        if not self._config.alerts.broken_links.enabled:
            return True

        threshold = self._config.alerts.broken_links.threshold

        if len(broken_links) >= threshold:
            title = f"🔗 Link Alert: {len(broken_links)} Broken Links Detected"
            message = self._format_broken_links_message(broken_links)
            return self.send_notification(
                title,
                message,
                c.Quality.NotificationPriority.WARNING.value,
            )

        return True

    def notify_weekly_report(
        self,
        report_data: t.JsonMapping,
    ) -> bool:
        """Send weekly quality report notification."""
        if not self._config.alerts.weekly_report.enabled:
            return True

        title = "📊 Weekly Documentation Quality Report"
        message = self._format_weekly_report_message(report_data)
        return self.send_notification(
            title,
            message,
            c.Quality.NotificationPriority.INFO.value,
        )

    def notify_monthly_report(
        self,
        report_data: t.JsonMapping,
    ) -> bool:
        """Send monthly comprehensive report notification."""
        if not self._config.alerts.monthly_report.enabled:
            return True

        title = "📈 Monthly Documentation Quality Report"
        message = self._format_monthly_report_message(report_data)
        return self.send_notification(
            title,
            message,
            c.Quality.NotificationPriority.INFO.value,
        )

    def send_notification(
        self,
        title: str,
        message: str,
        priority: str = c.Quality.NotificationPriority.INFO.value,
    ) -> bool:
        """Send notification through all enabled channels."""
        success = True

        # Console notification (always enabled)
        if self._config.channels.console.enabled:
            self._send_console_notification(title, message, priority)

        # Email notification
        if self._config.channels.email.enabled:
            try:
                self._send_email_notification(title, message, priority)
            except (smtplib.SMTPException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Email notification failed: {e}")
                success = False

        # Slack notification
        if self._config.channels.slack.enabled:
            try:
                self._send_slack_notification(title, message, priority)
            except (requests.RequestException, ConnectionError, OSError) as e:
                self.results.errors.append(f"Slack notification failed: {e}")
                success = False

        # Webhook notification
        if self._config.channels.webhook.enabled:
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
        email_config = self._config.email

        msg = MIMEMultipart()
        msg["From"] = email_config.from_address
        msg["To"] = ", ".join(x for x in (email_config.to_addresses or []))
        msg["Subject"] = f"[{priority.upper()}] {title}"

        body = f"""
FLEXT Quality Documentation Alert

{title}

{message}

---
This is an automated notification from the FLEXT Quality Documentation Maintenance System.
Timestamp: {u.now().isoformat()}
        """.strip()

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(
            email_config.smtp_server,
            email_config.smtp_port,
        )
        server.starttls()
        server.login(
            email_config.username,
            email_config.password,
        )
        text = msg.as_string()
        server.sendmail(
            email_config.from_address,
            list(email_config.to_addresses or []),
            text,
        )
        server.quit()

    def _send_slack_notification(self, title: str, message: str, priority: str) -> None:
        """Send notification to Slack."""
        slack_config = self._config.slack

        color = {
            c.Quality.NotificationPriority.CRITICAL.value: "danger",
            c.Quality.NotificationPriority.WARNING.value: "warning",
            c.Quality.NotificationPriority.INFO.value: "good",
        }.get(
            priority,
            "good",
        )

        payload: t.JsonMapping = {
            "channel": slack_config.channel,
            "username": slack_config.username,
            "attachments": [
                {
                    "color": color,
                    "title": title,
                    "text": message,
                    "footer": "FLEXT Quality Documentation System",
                    "ts": u.now().timestamp(),
                },
            ],
        }

        response = requests.post(
            slack_config.webhook_url,
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
        webhook_config = self._config.webhook

        payload = {
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": u.now().isoformat(),
            "source": "FLEXT Quality Documentation System",
        }

        headers_val = webhook_config.headers
        headers: t.MutableStrMapping = (
            dict(headers_val) if isinstance(headers_val, dict) else {}
        )
        headers["Content-Type"] = "application/json"

        timeout = webhook_config.timeout

        response = requests.post(
            webhook_config.url,
            json=payload,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()

    def _format_critical_issues_message(
        self,
        audit_data: t.JsonMapping,
    ) -> str:
        """Format message for critical issues notification."""
        metrics_val = audit_data.get("metrics")
        metrics: t.JsonMapping = (
            t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
            if isinstance(metrics_val, Mapping)
            else {}
        )
        severity_val = metrics.get("severity_breakdown")
        severity: t.JsonMapping = (
            t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(severity_val)
            if isinstance(severity_val, Mapping)
            else {}
        )
        severity_breakdown: t.MutableIntMapping = {}
        for key_name in ("critical", "high", "medium", "low"):
            kv = severity.get(key_name, 0)
            severity_breakdown[key_name] = kv if isinstance(kv, int) else 0

        issues_val = audit_data.get("issues")
        critical_issues: MutableSequence[t.JsonMapping] = []
        if isinstance(issues_val, list):
            issues_seq: t.SequenceOf[t.JsonMapping] = (
                t.Quality.RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER.validate_python(
                    issues_val,
                )
            )
            for i_m in issues_seq:
                sev = i_m.get("severity")
                if sev == c.Quality.NotificationPriority.CRITICAL.value:
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
        broken_links: t.JsonList,
    ) -> str:
        """Format message for broken links notification."""
        message = f"""
BROKEN LINKS DETECTED

Found {len(broken_links)} broken links that need attention:

"""

        for i, link in enumerate(
            broken_links[: c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW],
            1,
        ):  # Show first MAX_BROKEN_LINKS
            if isinstance(link, Mapping):
                url_v = link.get("url", "unknown")
                file_v = link.get("file", "unknown")
                err_v = link.get("error", "Unknown error")
            else:
                url_v, file_v, err_v = "unknown", "unknown", "Unknown error"
            message += f"{i}. {url_v}\n"
            message += f"   File: {file_v}\n"
            message += f"   Error: {err_v}\n\n"

        if len(broken_links) > c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW:
            remaining_links = (
                len(broken_links) - c.Quality.THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW
            )
            message += f"... and {remaining_links} more broken links.\n\n"

        message += (
            "Please update or fix these broken links to maintain documentation quality."
        )

        return message.strip()

    def _format_weekly_report_message(
        self,
        _report_data: t.JsonMapping,
    ) -> str:
        """Format message for weekly report notification."""
        # Implementation would depend on weekly report data structure
        # For now, report_data is not used but reserved for future implementation
        return "Weekly documentation quality report is now available. Check the reports dashboard for detailed metrics and trends."

    def _format_monthly_report_message(
        self,
        _report_data: t.JsonMapping,
    ) -> str:
        """Format message for monthly report notification."""
        # Implementation would depend on monthly report data structure
        return "Monthly comprehensive documentation quality report is now available. Review trends and plan improvements for the next month."

    class Run(s[bool]):
        """CLI command for FLEXT Quality documentation notifications."""

        settings_path: Annotated[
            str,
            u.Field(
                alias="settings",
                description="Notification settings file",
                validate_default=True,
            ),
        ] = "docs/maintenance/settings/notification_config.yaml"
        test: bool = u.Field(
            False,
            description="Send a test notification",
            validate_default=True,
        )
        audit_data: str | None = u.Field(
            None,
            description="Audit data JSON file",
            validate_default=True,
        )
        weekly_report: str | None = u.Field(
            None,
            description="Weekly report JSON file",
            validate_default=True,
        )
        monthly_report: str | None = u.Field(
            None,
            description="Monthly report JSON file",
            validate_default=True,
        )

        @override
        def execute(self) -> p.Result[bool]:
            """Dispatch to the appropriate notification action."""
            notifier = FlextQualityDocumentationNotifier(self.settings_path)
            if self.test:
                notifier.send_notification(
                    "Test Notification",
                    (
                        "This is a test notification from the FLEXT Quality "
                        "Documentation System.\n\nIf you received this, the "
                        "notification system is working correctly."
                    ),
                    c.Quality.NotificationPriority.INFO.value,
                )
                return r[bool].ok(value=True)
            if self.audit_data:
                audit_read = u.Cli.files_read_text(Path(self.audit_data))
                if audit_read.failure:
                    return r[bool].fail(
                        audit_read.error or f"cannot read {self.audit_data}",
                    )
                audit_data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                    audit_read.value,
                )
                _ = notifier.notify_critical_issues(audit_data)
                issues_raw = audit_data.get("issues")
                broken_links: MutableSequence[t.JsonValue] = []
                if isinstance(issues_raw, t.SEQUENCE_PAIR_TYPES):
                    for i_raw in issues_raw:
                        if isinstance(i_raw, Mapping):
                            type_val = i_raw.get("type", "")
                            if "broken" in str(type_val).lower():
                                broken_links.append(dict(i_raw))
                if broken_links:
                    _ = notifier.notify_broken_links(broken_links)
                return r[bool].ok(value=True)
            if self.weekly_report:
                weekly_read = u.Cli.files_read_text(Path(self.weekly_report))
                if weekly_read.failure:
                    return r[bool].fail(
                        weekly_read.error or f"cannot read {self.weekly_report}",
                    )
                report_data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                    weekly_read.value,
                )
                _ = notifier.notify_weekly_report(report_data)
                return r[bool].ok(value=True)
            if self.monthly_report:
                monthly_read = u.Cli.files_read_text(Path(self.monthly_report))
                if monthly_read.failure:
                    return r[bool].fail(
                        monthly_read.error or f"cannot read {self.monthly_report}",
                    )
                report_data = t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_json(
                    monthly_read.value,
                )
                _ = notifier.notify_monthly_report(report_data)
                return r[bool].ok(value=True)
            return r[bool].fail(
                "No action selected (use --test, --audit-data, --weekly-report or --monthly-report)",
            )

    @staticmethod
    def main(args: t.StrSequence | None = None) -> int:
        """Run the notification system via the canonical cli facade."""
        exit_code: int = u.Quality.execute_result_command(
            args=args,
            app_name="flext-quality-notifications",
            app_help="FLEXT Quality Documentation Notifications",
            route=m.Cli.ResultCommandRoute(
                name="run",
                help_text="Send a documentation notification",
                model_cls=FlextQualityDocumentationNotifier.Run,
                handler=lambda params: params.execute(),
            ),
        )
        return exit_code


if __name__ == "__main__":
    cli.exit(FlextQualityDocumentationNotifier.main())
