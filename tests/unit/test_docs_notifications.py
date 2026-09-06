"""Behavioral tests for ``FlextQualityDocumentationNotifier``.

Exercises real config loading/overriding, real threshold/formatting logic,
and the real ``requests`` library against invalid-scheme URLs (a fast,
deterministic, non-networked failure) — no mocks, no patched collaborators.
Email delivery is intentionally left untested: the production code opens a
real blocking SMTP socket with no timeout, which is unsafe to exercise in a
sandboxed, possibly network-restricted test run.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_quality import FlextQualityDocumentationNotifier
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path

    from flext_quality import t


class TestsFlextQualityDocumentationNotifier:
    """Contract tests for the documentation notification system."""

    def test_default_config_enables_only_console_channel(
        self, tmp_path: Path
    ) -> None:
        """A missing config file yields defaults with only console enabled."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.config.enabled, eq=True)
        tm.that(notifier.config.channels.console.enabled, eq=True)
        tm.that(notifier.config.channels.email.enabled, eq=False)
        tm.that(notifier.config.channels.slack.enabled, eq=False)
        tm.that(notifier.config.channels.webhook.enabled, eq=False)

    def test_get_default_config_thresholds(self, tmp_path: Path) -> None:
        """The default configuration ships the documented alert thresholds."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.config.alerts.critical_issues.threshold, eq=1)
        tm.that(notifier.config.alerts.quality_drop.threshold, eq=10)
        tm.that(notifier.config.alerts.broken_links.threshold, eq=5)

    def test_yaml_overrides_channel_toggles(self, tmp_path: Path) -> None:
        """A real YAML config file overrides channel enablement flags."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "enabled: false\n"
            "channels:\n"
            "  console:\n    enabled: false\n"
            "  slack:\n    enabled: true\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.config.enabled, eq=False)
        tm.that(notifier.config.channels.console.enabled, eq=False)
        tm.that(notifier.config.channels.slack.enabled, eq=True)

    def test_yaml_overrides_alert_thresholds(self, tmp_path: Path) -> None:
        """A real YAML config file overrides alert enablement and thresholds."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n"
            "  critical_issues:\n    enabled: false\n    threshold: 9\n"
            "  weekly_report:\n    enabled: false\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.config.alerts.critical_issues.enabled, eq=False)
        tm.that(notifier.config.alerts.critical_issues.threshold, eq=9)
        tm.that(notifier.config.alerts.weekly_report.enabled, eq=False)

    def test_yaml_overrides_slack_and_webhook_sections(self, tmp_path: Path) -> None:
        """A real YAML config file overrides slack and webhook settings."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "slack:\n"
            "  webhook_url: ''\n"
            "  channel: '#other-channel'\n"
            "  username: CustomBot\n"
            "webhook:\n"
            "  url: ''\n"
            "  timeout: 5\n"
            "  headers:\n    X-Custom: value\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.config.slack.channel, eq="#other-channel")
        tm.that(notifier.config.slack.username, eq="CustomBot")
        tm.that(notifier.config.webhook.timeout, eq=5)
        tm.that(notifier.config.webhook.headers.get("X-Custom"), eq="value")

    def test_notify_critical_issues_skips_when_alert_disabled(
        self, tmp_path: Path
    ) -> None:
        """A disabled critical-issues alert always reports success without sending."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  critical_issues:\n    enabled: false\n    threshold: 1\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.notify_critical_issues({}), eq=True)

    def test_notify_critical_issues_below_threshold_is_noop(
        self, tmp_path: Path
    ) -> None:
        """A critical count under threshold reports success without sending."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        audit_data: t.JsonMapping = {"metrics": {"severity_breakdown": {"critical": 0}}}
        tm.that(notifier.notify_critical_issues(audit_data), eq=True)
        tm.that(notifier.results.notifications_sent, eq=0)

    def test_notify_critical_issues_at_threshold_sends_console_notification(
        self, tmp_path: Path
    ) -> None:
        """Meeting the critical threshold sends through the default console channel."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        audit_data: t.JsonMapping = {
            "metrics": {
                "severity_breakdown": {"critical": 2, "high": 1},
                "quality_score": 40,
                "total_issues": 3,
            },
            "files_analyzed": 10,
            "issues": [
                {
                    "severity": "critical",
                    "type": "broken_link",
                    "file": "a.md",
                    "description": "bad link",
                }
            ],
        }
        tm.that(notifier.notify_critical_issues(audit_data), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_notify_quality_drop_skips_when_alert_disabled(
        self, tmp_path: Path
    ) -> None:
        """A disabled quality-drop alert always reports success without sending."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  quality_drop:\n    enabled: false\n    threshold: 10\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.notify_quality_drop(50.0, 90.0), eq=True)

    def test_notify_quality_drop_below_threshold_is_noop(
        self, tmp_path: Path
    ) -> None:
        """A drop smaller than the configured threshold sends nothing."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.notify_quality_drop(85.0, 90.0), eq=True)
        tm.that(notifier.results.notifications_sent, eq=0)

    def test_notify_quality_drop_at_threshold_sends_notification(
        self, tmp_path: Path
    ) -> None:
        """Meeting the drop threshold sends a real console notification."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.notify_quality_drop(50.0, 90.0), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_notify_broken_links_skips_when_alert_disabled(
        self, tmp_path: Path
    ) -> None:
        """A disabled broken-links alert always reports success without sending."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  broken_links:\n    enabled: false\n    threshold: 1\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.notify_broken_links([{"url": "x"}]), eq=True)

    def test_notify_broken_links_below_threshold_is_noop(
        self, tmp_path: Path
    ) -> None:
        """Fewer broken links than the threshold sends nothing."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.notify_broken_links([]), eq=True)
        tm.that(notifier.results.notifications_sent, eq=0)

    def test_notify_broken_links_at_threshold_formats_and_sends(
        self, tmp_path: Path
    ) -> None:
        """Meeting the broken-links threshold formats and sends a real message."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  broken_links:\n    enabled: true\n    threshold: 2\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        broken_links: t.JsonList = [
            {"url": "http://a", "file": "a.md", "error": "404"},
            {"url": "http://b", "file": "b.md", "error": "timeout"},
        ]
        tm.that(notifier.notify_broken_links(broken_links), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_notify_broken_links_handles_more_links_than_the_display_cap(
        self, tmp_path: Path
    ) -> None:
        """More broken links than the display cap still sends one notification."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        many_links: t.JsonList = [{"url": f"http://x{i}"} for i in range(15)]
        tm.that(notifier.notify_broken_links(many_links), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_notify_weekly_report_skips_when_alert_disabled(
        self, tmp_path: Path
    ) -> None:
        """A disabled weekly-report alert always reports success without sending."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  weekly_report:\n    enabled: false\n", encoding="utf-8"
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.notify_weekly_report({}), eq=True)
        tm.that(notifier.results.notifications_sent, eq=0)

    def test_notify_weekly_report_enabled_sends_notification(
        self, tmp_path: Path
    ) -> None:
        """An enabled weekly-report alert sends a real console notification."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.notify_weekly_report({}), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_notify_monthly_report_skips_when_alert_disabled(
        self, tmp_path: Path
    ) -> None:
        """A disabled monthly-report alert always reports success without sending."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "alerts:\n  monthly_report:\n    enabled: false\n", encoding="utf-8"
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        tm.that(notifier.notify_monthly_report({}), eq=True)
        tm.that(notifier.results.notifications_sent, eq=0)

    def test_notify_monthly_report_enabled_sends_notification(
        self, tmp_path: Path
    ) -> None:
        """An enabled monthly-report alert sends a real console notification."""
        notifier = FlextQualityDocumentationNotifier(str(tmp_path / "absent.yaml"))
        tm.that(notifier.notify_monthly_report({}), eq=True)
        tm.that(notifier.results.notifications_sent, eq=1)

    def test_send_notification_slack_failure_is_recorded(
        self, tmp_path: Path
    ) -> None:
        """A real (schemeless) slack webhook URL fails and is recorded as an error."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "channels:\n  slack:\n    enabled: true\n"
            "slack:\n  webhook_url: ''\n  channel: '#x'\n  username: bot\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        success = notifier.send_notification("title", "message")
        tm.that(success, eq=False)
        tm.that(len(notifier.results.errors), eq=1)
        tm.that(notifier.results.errors[0], has="Slack notification failed")

    def test_send_notification_webhook_failure_is_recorded(
        self, tmp_path: Path
    ) -> None:
        """A real (schemeless) webhook URL fails and is recorded as an error."""
        config_path = tmp_path / "notify.yaml"
        config_path.write_text(
            "channels:\n  webhook:\n    enabled: true\n"
            "webhook:\n  url: ''\n  timeout: 3\n",
            encoding="utf-8",
        )
        notifier = FlextQualityDocumentationNotifier(str(config_path))
        success = notifier.send_notification("title", "message")
        tm.that(success, eq=False)
        tm.that(notifier.results.errors[0], has="Webhook notification failed")

    def test_run_execute_sends_a_test_notification(self, tmp_path: Path) -> None:
        """``Run.execute()`` with ``test=True`` sends a real test notification."""
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml"), test=True
        )
        result = command.execute()
        tm.that(result.success, eq=True)
        tm.that(result.value, eq=True)

    def test_run_execute_processes_audit_data_file(self, tmp_path: Path) -> None:
        """``Run.execute()`` reads a real audit-data JSON file and notifies."""
        audit_path = tmp_path / "audit.json"
        audit_path.write_text(
            '{"metrics": {"severity_breakdown": {"critical": 0}}, '
            '"issues": [{"type": "broken_link"}]}',
            encoding="utf-8",
        )
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml"), audit_data=str(audit_path)
        )
        result = command.execute()
        tm.that(result.success, eq=True)

    def test_run_execute_fails_for_missing_audit_data_file(
        self, tmp_path: Path
    ) -> None:
        """``Run.execute()`` reports a failure for an unreadable audit-data path."""
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml"),
            audit_data=str(tmp_path / "missing.json"),
        )
        result = command.execute()
        tm.that(result.failure, eq=True)

    def test_run_execute_processes_weekly_report_file(self, tmp_path: Path) -> None:
        """``Run.execute()`` reads a real weekly-report JSON file and notifies."""
        report_path = tmp_path / "weekly.json"
        report_path.write_text("{}", encoding="utf-8")
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml"), weekly_report=str(report_path)
        )
        result = command.execute()
        tm.that(result.success, eq=True)

    def test_run_execute_processes_monthly_report_file(self, tmp_path: Path) -> None:
        """``Run.execute()`` reads a real monthly-report JSON file and notifies."""
        report_path = tmp_path / "monthly.json"
        report_path.write_text("{}", encoding="utf-8")
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml"), monthly_report=str(report_path)
        )
        result = command.execute()
        tm.that(result.success, eq=True)

    def test_run_execute_fails_when_no_action_selected(self, tmp_path: Path) -> None:
        """``Run.execute()`` fails when no action flag is provided."""
        command = FlextQualityDocumentationNotifier.Run(
            settings_path=str(tmp_path / "absent.yaml")
        )
        result = command.execute()
        tm.that(result.failure, eq=True)
        tm.that(result.error or "", has="No action selected")


__all__: list[str] = ["TestsFlextQualityDocumentationNotifier"]
