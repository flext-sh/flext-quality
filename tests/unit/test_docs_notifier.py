"""Public documentation notifier behavior."""

from __future__ import annotations

from pathlib import Path

from flext_quality import u
from flext_quality.docs import FlextQualityDocumentationNotifier


def test_default_configuration_loads_nested_channel_settings() -> None:
    notifier = FlextQualityDocumentationNotifier()
    packaged = FlextQualityDocumentationNotifier(
        FlextQualityDocumentationNotifier.Run().settings_path
    )

    assert notifier.config == packaged.config
    assert notifier.config.channels.console.enabled
    assert notifier.send_notification("Title", "Message") is True


def test_main_uses_packaged_configuration() -> None:
    assert FlextQualityDocumentationNotifier.main(["run", "--test"]) == 0


def test_custom_thresholds_and_console_only_notifications() -> None:
    notifier = FlextQualityDocumentationNotifier()
    notifier.config.alerts.critical_issues.threshold = 2
    notifier.config.alerts.quality_drop.threshold = 5
    notifier.config.alerts.broken_links.threshold = 2

    critical = notifier.notify_critical_issues({
        "metrics": {"severity_breakdown": {"critical": 2}, "quality_score": 40},
        "issues": [],
        "files_analyzed": 1,
    })
    quality_drop = notifier.notify_quality_drop(80, 90)
    broken_links = notifier.notify_broken_links([
        {"url": "one", "file": "a.md"},
        {"url": "two", "file": "b.md"},
    ])

    assert critical is True
    assert quality_drop is True
    assert broken_links is True
    assert notifier.results.notifications_sent == 3
    assert notifier.results.errors == []


def test_send_notification_uses_console_channel_without_network() -> None:
    notifier = FlextQualityDocumentationNotifier()

    assert notifier.send_notification("Title", "Message") is True
    assert notifier.results.notifications_sent == 1


def test_global_disable_prevents_channel_dispatch(tmp_path: Path) -> None:
    packaged = u.Cli.yaml_load_mapping(
        Path(FlextQualityDocumentationNotifier.Run().settings_path)
    )
    config_path = tmp_path / "notification.yaml"
    config_path.write_text(
        u.Cli.yaml_dump_str({**packaged, "enabled": False}), encoding="utf-8"
    )
    notifier = FlextQualityDocumentationNotifier(str(config_path))

    assert notifier.send_notification("Title", "Message") is True
    assert notifier.results.notifications_sent == 0
