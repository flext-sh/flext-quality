#!/usr/bin/env python3
"""FLEXT Quality Documentation Notification System.

Automated notification system for documentation quality alerts,
reports, and maintenance updates. Supports multiple notification channels
including email, Slack, webhooks, and project management tools.
"""

import json
import smtplib
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import requests
import yaml


class DocumentationNotifier:
    """Automated notification system for documentation quality alerts."""

    def __init__(
        self, config_path: str = "docs/maintenance/config/notification_config.yaml"
    ) -> None:
        self.load_config(config_path)
        self.results = {
            "notifications_sent": 0,
            "errors": [],
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def load_config(self, config_path: str) -> None:
        """Load notification configuration."""
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.config = self.get_default_config()

    def get_default_config(self) -> dict[str, Any]:
        """Default notification configuration."""
        return {
            "enabled": True,
            "channels": {
                "console": {"enabled": True},
                "email": {"enabled": False},
                "slack": {"enabled": False},
                "webhook": {"enabled": False},
            },
            "alerts": {
                "critical_issues": {"enabled": True, "threshold": 1},
                "quality_drop": {"enabled": True, "threshold": 10},
                "broken_links": {"enabled": True, "threshold": 5},
                "weekly_report": {"enabled": True},
                "monthly_report": {"enabled": True},
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "from_address": "",
                "to_addresses": [],
            },
            "slack": {
                "webhook_url": "",
                "channel": "#docs-quality",
                "username": "FLEXT Quality Bot",
            },
            "webhook": {"url": "", "headers": {}, "timeout": 10},
        }

    def notify_critical_issues(self, audit_data: dict[str, Any]) -> bool:
        """Send notification for critical documentation issues."""
        if not self.config["alerts"]["critical_issues"]["enabled"]:
            return True

        severity_breakdown = audit_data.get("metrics", {}).get("severity_breakdown", {})
        critical_count = severity_breakdown.get("critical", 0)
        threshold = self.config["alerts"]["critical_issues"]["threshold"]

        if critical_count >= threshold:
            title = f"🚨 CRITICAL: {critical_count} Critical Documentation Issues Found"
            message = self._format_critical_issues_message(audit_data)
            return self.send_notification(title, message, "critical")

        return True

    def notify_quality_drop(self, current_score: float, previous_score: float) -> bool:
        """Send notification for significant quality score drops."""
        if not self.config["alerts"]["quality_drop"]["enabled"]:
            return True

        threshold = self.config["alerts"]["quality_drop"]["threshold"]
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

    def notify_broken_links(self, broken_links: list[dict[str, Any]]) -> bool:
        """Send notification for broken links."""
        if not self.config["alerts"]["broken_links"]["enabled"]:
            return True

        threshold = self.config["alerts"]["broken_links"]["threshold"]

        if len(broken_links) >= threshold:
            title = f"🔗 Link Alert: {len(broken_links)} Broken Links Detected"
            message = self._format_broken_links_message(broken_links)
            return self.send_notification(title, message, "warning")

        return True

    def notify_weekly_report(self, report_data: dict[str, Any]) -> bool:
        """Send weekly quality report notification."""
        if not self.config["alerts"]["weekly_report"]["enabled"]:
            return True

        title = "📊 Weekly Documentation Quality Report"
        message = self._format_weekly_report_message(report_data)
        return self.send_notification(title, message, "info")

    def notify_monthly_report(self, report_data: dict[str, Any]) -> bool:
        """Send monthly comprehensive report notification."""
        if not self.config["alerts"]["monthly_report"]["enabled"]:
            return True

        title = "📈 Monthly Documentation Quality Report"
        message = self._format_monthly_report_message(report_data)
        return self.send_notification(title, message, "info")

    def send_notification(
        self, title: str, message: str, priority: str = "info"
    ) -> bool:
        """Send notification through all enabled channels."""
        success = True

        # Console notification (always enabled)
        if self.config["channels"]["console"]["enabled"]:
            self._send_console_notification(title, message, priority)

        # Email notification
        if self.config["channels"]["email"]["enabled"]:
            try:
                self._send_email_notification(title, message, priority)
            except Exception as e:
                self.results["errors"].append(f"Email notification failed: {e}")
                success = False

        # Slack notification
        if self.config["channels"]["slack"]["enabled"]:
            try:
                self._send_slack_notification(title, message, priority)
            except Exception as e:
                self.results["errors"].append(f"Slack notification failed: {e}")
                success = False

        # Webhook notification
        if self.config["channels"]["webhook"]["enabled"]:
            try:
                self._send_webhook_notification(title, message, priority)
            except Exception as e:
                self.results["errors"].append(f"Webhook notification failed: {e}")
                success = False

        if success:
            self.results["notifications_sent"] += 1

        return success

    def _send_console_notification(
        self, title: str, message: str, priority: str
    ) -> None:
        """Send notification to console."""
        datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(priority, "📢")

    def _send_email_notification(self, title: str, message: str, priority: str) -> None:
        """Send notification via email."""
        email_config = self.config["email"]

        msg = MIMEMultipart()
        msg["From"] = email_config["from_address"]
        msg["To"] = ", ".join(email_config["to_addresses"])
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

        server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
        server.starttls()
        server.login(email_config["username"], email_config["password"])
        text = msg.as_string()
        server.sendmail(
            email_config["from_address"], email_config["to_addresses"], text
        )
        server.quit()

    def _send_slack_notification(self, title: str, message: str, priority: str) -> None:
        """Send notification to Slack."""
        slack_config = self.config["slack"]

        color = {"critical": "danger", "warning": "warning", "info": "good"}.get(
            priority, "good"
        )

        payload = {
            "channel": slack_config["channel"],
            "username": slack_config["username"],
            "attachments": [
                {
                    "color": color,
                    "title": title,
                    "text": message,
                    "footer": "FLEXT Quality Documentation System",
                    "ts": datetime.now(UTC).timestamp(),
                }
            ],
        }

        response = requests.post(slack_config["webhook_url"], json=payload, timeout=10)
        response.raise_for_status()

    def _send_webhook_notification(
        self, title: str, message: str, priority: str
    ) -> None:
        """Send notification via webhook."""
        webhook_config = self.config["webhook"]

        payload = {
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now(UTC).isoformat(),
            "source": "FLEXT Quality Documentation System",
        }

        headers = webhook_config.get("headers", {})
        headers["Content-Type"] = "application/json"

        response = requests.post(
            webhook_config["url"],
            json=payload,
            headers=headers,
            timeout=webhook_config["timeout"],
        )
        response.raise_for_status()

    def _format_critical_issues_message(self, audit_data: dict[str, Any]) -> str:
        """Format message for critical issues notification."""
        metrics = audit_data.get("metrics", {})
        severity_breakdown = metrics.get("severity_breakdown", {})

        issues = audit_data.get("issues", [])
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
                f"{i}. {issue.get('type', 'unknown').replace('_', ' ').title()}\n"
            )
            message += f"   File: {issue.get('file', 'unknown')}\n"
            message += (
                f"   Description: {issue.get('description', 'No description')}\n\n"
            )

        message += "\nIMMEDIATE ACTION REQUIRED: Please review and fix critical issues immediately."

        return message.strip()

    def _format_broken_links_message(self, broken_links: list[dict[str, Any]]) -> str:
        """Format message for broken links notification."""
        message = f"""
BROKEN LINKS DETECTED

Found {len(broken_links)} broken links that need attention:

"""

        for i, link in enumerate(broken_links[:10], 1):  # Show first 10
            message += f"{i}. {link.get('url', 'unknown')}\n"
            message += f"   File: {link.get('file', 'unknown')}\n"
            message += f"   Error: {link.get('error', 'Unknown error')}\n\n"

        if len(broken_links) > 10:
            message += f"... and {len(broken_links) - 10} more broken links.\n\n"

        message += (
            "Please update or fix these broken links to maintain documentation quality."
        )

        return message.strip()

    def _format_weekly_report_message(self, report_data: dict[str, Any]) -> str:
        """Format message for weekly report notification."""
        # Implementation would depend on weekly report data structure
        return "Weekly documentation quality report is now available. Check the reports dashboard for detailed metrics and trends."

    def _format_monthly_report_message(self, report_data: dict[str, Any]) -> str:
        """Format message for monthly report notification."""
        # Implementation would depend on monthly report data structure
        return "Monthly comprehensive documentation quality report is now available. Review trends and plan improvements for the next month."


def main() -> None:
    """Main entry point for notification system."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Notifications"
    )
    parser.add_argument(
        "--config",
        default="docs/maintenance/config/notification_config.yaml",
        help="Notification configuration file",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send test notification to verify configuration",
    )
    parser.add_argument("--audit-data", help="Path to audit data JSON file")
    parser.add_argument("--weekly-report", help="Path to weekly report JSON file")
    parser.add_argument("--monthly-report", help="Path to monthly report JSON file")

    args = parser.parse_args()

    notifier = DocumentationNotifier(args.config)

    if args.test:
        # Send test notification
        success = notifier.send_notification(
            "Test Notification",
            "This is a test notification from the FLEXT Quality Documentation System.\n\nIf you received this, the notification system is working correctly!",
            "info",
        )
        if success:
            pass
        else:
            for _error in notifier.results["errors"]:
                pass

    elif args.audit_data:
        # Process audit data and send appropriate notifications
        with Path(args.audit_data).open(encoding="utf-8") as f:
            audit_data = json.load(f)

        # Check for critical issues
        notifier.notify_critical_issues(audit_data)

        # Check for broken links (would need to extract from audit data)
        # This is a simplified example
        broken_links = [
            i
            for i in audit_data.get("issues", [])
            if "broken" in i.get("type", "").lower()
        ]
        if broken_links:
            notifier.notify_broken_links(broken_links)

    elif args.weekly_report:
        # Send weekly report notification
        with Path(args.weekly_report).open(encoding="utf-8") as f:
            report_data = json.load(f)
        notifier.notify_weekly_report(report_data)

    elif args.monthly_report:
        # Send monthly report notification
        with Path(args.monthly_report).open(encoding="utf-8") as f:
            report_data = json.load(f)
        notifier.notify_monthly_report(report_data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
