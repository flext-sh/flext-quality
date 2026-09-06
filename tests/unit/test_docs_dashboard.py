"""Behavioral tests for ``FlextQualityDocumentationDashboard``.

Exercises the real Flask application via its test client, real filesystem
report scanning against ``tmp_path``, and the ``Run`` CLI command — no
mocks, no patched collaborators.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from flext_quality import FlextQualityDocumentationDashboard
from flext_tests import tm

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextQualityDocumentationDashboard:
    """Contract tests for the documentation health dashboard."""

    def test_get_current_metrics_reports_no_audit_data(self, tmp_path: Path) -> None:
        """With no audit report present, metrics report a zeroed default."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        metrics = dashboard.get_current_metrics()
        tm.that(metrics.get("quality_score"), eq=0)
        tm.that(metrics.get("status"), eq="No audit data available")

    def test_get_current_metrics_parses_a_real_latest_audit_file(
        self, tmp_path: Path
    ) -> None:
        """A real ``latest_audit.json`` file is parsed into the metrics payload."""
        (tmp_path / "latest_audit.json").write_text(
            json.dumps({
                "files_analyzed": 12,
                "timestamp": "2026-01-01T00:00:00",
                "metrics": {
                    "quality_score": 87,
                    "total_issues": 4,
                    "severity_breakdown": {"critical": 1, "high": 3},
                },
            }),
            encoding="utf-8",
        )
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        metrics = dashboard.get_current_metrics()
        tm.that(metrics.get("quality_score"), eq=87)
        tm.that(metrics.get("files_analyzed"), eq=12)
        tm.that(metrics.get("status"), eq="Current")

    def test_get_current_metrics_reports_error_for_malformed_json(
        self, tmp_path: Path
    ) -> None:
        """Malformed JSON in the latest audit report yields an error status."""
        (tmp_path / "latest_audit.json").write_text("not json at all", encoding="utf-8")
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        metrics = dashboard.get_current_metrics()
        tm.that(metrics.get("status") or "", has="Error")

    def test_get_quality_trends_with_no_reports_is_empty(self, tmp_path: Path) -> None:
        """No matching report files yield a trend payload with zero data points."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        trends = dashboard.get_quality_trends(days=7)
        tm.that(trends.get("period_days"), eq=7)
        tm.that(trends.get("data_points"), eq=0)
        tm.that(trends.get("trends"), eq=[])

    def test_get_quality_trends_reads_real_report_files(self, tmp_path: Path) -> None:
        """A recent, well-formed report file contributes one trend entry."""
        report = {
            "metrics": {
                "quality_score": 91,
                "total_issues": 2,
                "severity_breakdown": {"critical": 0, "high": 2},
            }
        }
        report_file = tmp_path / "audit_report_20260101_120000.json"
        report_file.write_text(json.dumps(report), encoding="utf-8")
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        trends = dashboard.get_quality_trends(days=3650)
        tm.that(trends.get("data_points"), eq=1)
        trend_entries = trends.get("trends")
        tm.that(trend_entries, is_=list)
        assert isinstance(trend_entries, list)
        first_entry = trend_entries[0]
        tm.that(first_entry, is_=dict)
        assert isinstance(first_entry, dict)
        tm.that(first_entry.get("quality_score"), eq=91)

    def test_get_recent_reports_with_no_reports_is_empty(self, tmp_path: Path) -> None:
        """No matching report files yield an empty recent-reports listing."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        tm.that(dashboard.get_recent_reports(), eq=[])

    def test_get_recent_reports_sorts_newest_first_and_respects_limit(
        self, tmp_path: Path
    ) -> None:
        """Recent reports are sorted newest-first and truncated at ``limit``."""
        for stamp, score in (
            ("20260101_000000", 50),
            ("20260103_000000", 70),
            ("20260102_000000", 60),
        ):
            report_file = tmp_path / f"audit_report_{stamp}.json"
            report_file.write_text(
                json.dumps({
                    "metrics": {"quality_score": score, "total_issues": 1},
                    "files_analyzed": 5,
                }),
                encoding="utf-8",
            )
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        reports = dashboard.get_recent_reports(limit=2)
        tm.that(len(reports), eq=2)
        tm.that(reports[0]["quality_score"], eq=70)
        tm.that(reports[1]["quality_score"], eq=60)

    def test_get_dashboard_html_returns_nonempty_page(self, tmp_path: Path) -> None:
        """The dashboard HTML template renders a nonempty document."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        html = dashboard.get_dashboard_html()
        tm.that(html, has="FLEXT Quality Documentation Dashboard")

    def test_index_route_serves_dashboard_html(self, tmp_path: Path) -> None:
        """The Flask ``/`` route serves the rendered dashboard page."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        client = dashboard.app.test_client()
        response = client.get("/")
        tm.that(response.status_code, eq=200)
        tm.that(response.get_data(as_text=True), has="Dashboard")

    def test_api_metrics_route_returns_json(self, tmp_path: Path) -> None:
        """The Flask ``/api/metrics`` route returns the metrics payload as JSON."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        client = dashboard.app.test_client()
        response = client.get("/api/metrics")
        tm.that(response.status_code, eq=200)
        payload = json.loads(response.get_data(as_text=True))
        tm.that(payload.get("status"), eq="No audit data available")

    def test_api_trends_route_honors_days_query_param(self, tmp_path: Path) -> None:
        """The Flask ``/api/trends`` route reads the ``days`` query parameter."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        client = dashboard.app.test_client()
        response = client.get("/api/trends?days=5")
        tm.that(response.status_code, eq=200)
        payload = json.loads(response.get_data(as_text=True))
        tm.that(payload.get("period_days"), eq=5)

    def test_api_reports_route_honors_limit_query_param(self, tmp_path: Path) -> None:
        """The Flask ``/api/reports`` route reads the ``limit`` query parameter."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        client = dashboard.app.test_client()
        response = client.get("/api/reports?limit=1")
        tm.that(response.status_code, eq=200)
        payload = json.loads(response.get_data(as_text=True))
        tm.that(payload, eq=[])

    def test_logger_property_returns_module_logger(self, tmp_path: Path) -> None:
        """The dashboard exposes its module logger through a public property."""
        dashboard = FlextQualityDocumentationDashboard(str(tmp_path))
        tm.that(dashboard.logger is not None, eq=True)

    def test_run_command_model_carries_declared_defaults(self) -> None:
        """The ``Run`` command model exposes its documented default fields."""
        command = FlextQualityDocumentationDashboard.Run()
        tm.that(command.host, eq="localhost")
        tm.that(command.port, eq=8080)
        tm.that(command.debug, eq=False)
        tm.that(command.reports_dir, eq="docs/maintenance/reports/")


__all__: list[str] = ["TestsFlextQualityDocumentationDashboard"]
