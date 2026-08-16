"""Public documentation auditor behavior."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from flext_quality import u
from flext_quality.docs.scripts.audit import FlextQualityDocumentationAuditor


def test_document_root_discovers_only_requested_tree(tmp_path: Path) -> None:
    document = tmp_path / "docs" / "guide.md"
    document.parent.mkdir()
    document.write_text("# Guide\n", encoding="utf-8")
    auditor = FlextQualityDocumentationAuditor(document_root=tmp_path)

    assert auditor.find_documentation_files() == [document]


def test_checks_freshness_completeness_consistency_and_internal_links(
    tmp_path: Path,
) -> None:
    document = tmp_path / "README.md"
    document.write_text(
        "## Start\nTODO: finish\n![](missing.png)\n[missing](other.md)\n",
        encoding="utf-8",
    )
    os.utime(document, (0, 0))
    auditor = FlextQualityDocumentationAuditor(document_root=tmp_path)

    auditor.check_content_freshness([document])
    auditor.check_content_completeness([document])
    auditor.check_content_consistency([document])
    auditor.check_links_and_references([document])

    issue_types = {issue["type"] for issue in auditor.results.issues}
    assert {
        "outdated_content",
        "insufficient_content",
        "missing_sections",
        "todo_markers",
        "accessibility_issues",
        "heading_hierarchy",
        "broken_internal_link",
        "missing_image",
    }.issubset(issue_types)
    assert all(issue.get("file") == "README.md" for issue in auditor.results.issues)


def test_heading_hierarchy_uses_non_default_style_guide_owner(tmp_path: Path) -> None:
    packaged_config = (
        Path(__file__).parents[2] / "src" / "flext_quality" / "docs" / "config"
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    for name in ("audit_rules.yaml", "validation_config.yaml"):
        (config_dir / name).write_text(
            (packaged_config / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    style = dict(u.Cli.yaml_load_mapping(packaged_config / "style_guide.yaml"))
    style["headings"] = {
        "enforce_hierarchy": True,
        "first_heading_level": 2,
        "max_heading_level": 3,
    }
    (config_dir / "style_guide.yaml").write_text(
        u.Cli.yaml_dump_str(style), encoding="utf-8"
    )
    document = tmp_path / "guide.md"
    document.write_text("# Too early\n## Start\n#### Too deep\n", encoding="utf-8")
    auditor = FlextQualityDocumentationAuditor(
        config_path=config_dir, document_root=tmp_path
    )

    auditor.check_content_consistency([document])

    hierarchy = [
        issue
        for issue in auditor.results.issues
        if issue["type"] == "heading_hierarchy"
    ]
    assert len(hierarchy) == 1
    hierarchy_issues = hierarchy[0]["issues"]
    assert isinstance(hierarchy_issues, list)
    assert len(hierarchy_issues) == 3


def test_external_file_does_not_raise_relative_path_error(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    document = tmp_path / "external.md"
    document.write_text("short", encoding="utf-8")
    auditor = FlextQualityDocumentationAuditor(document_root=root)

    auditor.check_content_completeness([document])

    assert auditor.results.issues[0]["file"] == str(document.resolve())


def test_nested_internal_links_resolve_from_source_document_outside_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document_root = tmp_path / "project"
    source = document_root / "docs" / "guides" / "index.md"
    valid_target = document_root / "docs" / "reference" / "api.md"
    source.parent.mkdir(parents=True)
    valid_target.parent.mkdir(parents=True)
    source.write_text(
        "[API](../reference/api.md#usage)\n[Missing](../reference/missing.md#topic)\n",
        encoding="utf-8",
    )
    valid_target.write_text("# API\n", encoding="utf-8")
    outside_cwd = tmp_path / "outside"
    outside_cwd.mkdir()
    monkeypatch.chdir(outside_cwd)
    auditor = FlextQualityDocumentationAuditor(document_root=document_root)

    auditor.check_links_and_references([source, valid_target])

    broken_links = [
        issue
        for issue in auditor.results.issues
        if issue["type"] == "broken_internal_link"
    ]
    assert len(broken_links) == 1
    assert broken_links[0]["file"] == "docs/guides/index.md"
    assert broken_links[0]["target"] == "../reference/missing.md#topic"


def test_metrics_recommendations_and_reports(tmp_path: Path) -> None:
    auditor = FlextQualityDocumentationAuditor(document_root=tmp_path)
    auditor.results.files_analyzed = 2
    auditor.results.issues.extend([
        {"type": "broken_internal_link", "severity": "high", "file": "a.md"},
        {"type": "outdated_content", "severity": "medium", "file": "b.md"},
    ])

    auditor.calculate_quality_metrics()
    auditor.generate_recommendations()
    html = auditor.generate_report("html")
    json_report = auditor.generate_report("json")
    saved = auditor.save_report("json", str(tmp_path / "reports"))
    quality_score = auditor.results.metrics.quality_score

    assert quality_score > 0
    assert {rec.category for rec in auditor.results.recommendations} == {
        "link_maintenance",
        "content_freshness",
    }
    assert "<!DOCTYPE html>" in html
    assert f'"quality_score": {quality_score}' in json_report
    assert saved.success


def test_run_and_main_apply_document_root(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text("# Guide\n", encoding="utf-8")
    reports = tmp_path / "reports"

    result = FlextQualityDocumentationAuditor.Run(
        check_completeness=True, document_root=str(tmp_path), output=str(reports)
    ).execute()

    assert result.success
    assert (
        FlextQualityDocumentationAuditor.main([
            "run",
            "--check-completeness",
            "--document-root",
            str(tmp_path),
            "--output",
            str(reports),
        ])
        == 0
    )
