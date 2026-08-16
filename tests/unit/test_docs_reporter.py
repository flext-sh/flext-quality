"""Public documentation reporter behavior."""

from __future__ import annotations

import json
from pathlib import Path

from flext_quality.docs.scripts.report import FlextQualityDocumentationReporter


def _write_latest_reports(reports_dir: Path) -> None:
    reports_dir.mkdir()
    (reports_dir / "latest_audit.json").write_text(
        json.dumps({
            "metrics": {"quality_score": 82},
            "issues": [],
            "files_analyzed": 3,
        }),
        encoding="utf-8",
    )
    (reports_dir / "latest_validation.json").write_text(
        json.dumps({"link_validation": {"links_checked": 7, "errors": []}}),
        encoding="utf-8",
    )
    (reports_dir / "latest_optimization.json").write_text(
        json.dumps({"changes_made": 2, "optimizations": [{"type": "formatting"}]}),
        encoding="utf-8",
    )


def test_generates_html_json_and_markdown_reports(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    _write_latest_reports(reports_dir)
    reporter = FlextQualityDocumentationReporter(str(reports_dir))

    html = reporter.generate_quality_report("html")
    json_report = reporter.generate_quality_report("json")
    markdown = reporter.generate_quality_report("markdown")

    assert "<!DOCTYPE html>" in html
    assert '"overall_score": 82' in json_report
    assert "Overall Quality Score:** 82%" in markdown


def test_generates_trend_analysis_and_saves_report(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    _write_latest_reports(reports_dir)
    (reports_dir / "audit_20990101_000000.json").write_text(
        json.dumps({"metrics": {"quality_score": 90}, "issues": []}), encoding="utf-8"
    )
    reporter = FlextQualityDocumentationReporter(str(reports_dir))

    trends = reporter.generate_trend_report(days=30000)
    saved = reporter.save_report(trends, "trends", "md")

    assert "Quality Score Trends" in trends
    assert saved.success
    assert saved.value.read_text(encoding="utf-8") == trends
