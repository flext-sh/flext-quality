"""Public documentation optimizer behavior."""

from __future__ import annotations

from pathlib import Path

from flext_quality.docs.scripts.optimize import FlextQualityDocumentationOptimizer


def test_formatting_uses_explicit_document_root(tmp_path: Path) -> None:
    root = tmp_path / "docs"
    root.mkdir()
    document = root / "guide.md"
    document.write_text("# Guide  \n", encoding="utf-8")
    optimizer = FlextQualityDocumentationOptimizer(backup=False, document_root=root)

    result = optimizer.optimize_formatting([document])

    assert document.read_text(encoding="utf-8") == "# Guide\n"
    assert result.optimizations[0]["file"] == "guide.md"


def test_file_outside_default_root_uses_absolute_path(tmp_path: Path) -> None:
    document = tmp_path / "external.md"
    document.write_text("# External  \n", encoding="utf-8")
    optimizer = FlextQualityDocumentationOptimizer(backup=True)

    result = optimizer.optimize_formatting([document])

    assert result.optimizations[0]["file"] == str(document.resolve())
    assert result.backups_created == [str(document.with_suffix(".md.backup").resolve())]


def test_accessibility_structure_metadata_and_reports(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "# Guide\n![](my-image.png)\n[here](target.md)\n## Section\n", encoding="utf-8"
    )
    optimizer = FlextQualityDocumentationOptimizer(backup=False, document_root=tmp_path)

    optimizer.enhance_accessibility([document])
    optimizer.optimize_content_structure([document])
    optimizer.update_metadata([document])
    report = optimizer.generate_report()
    saved = optimizer.save_report(str(tmp_path / "reports"))

    content = document.read_text(encoding="utf-8")
    assert "![My Image](my-image.png)" in content
    assert "[learn more](target.md)" in content
    assert "<!-- Updated:" in content
    assert '"files_processed"' in report
    assert saved.success
    assert Path(saved.value).exists()


def test_table_of_contents_updates_long_document(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "# Guide\n\n## One\n## Two\n## Three\n## Four\n## Five\n## Six\n",
        encoding="utf-8",
    )
    optimizer = FlextQualityDocumentationOptimizer(backup=False, document_root=tmp_path)

    optimizer.update_table_of_contents([document])

    assert "## Table of Contents" in document.read_text(encoding="utf-8")


def test_table_of_contents_replaces_stale_entries_idempotently(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "# Guide\n\n## Table of Contents\n\n- [Stale](#stale)\n\n---\n\n"
        "## One\n## Two\n## Three\n## Four\n## Five\n## Six\n",
        encoding="utf-8",
    )
    optimizer = FlextQualityDocumentationOptimizer(backup=False, document_root=tmp_path)

    optimizer.update_table_of_contents([document])
    first = document.read_text(encoding="utf-8")
    optimizer.update_table_of_contents([document])
    second = document.read_text(encoding="utf-8")

    assert first == second
    assert "[Stale](#stale)" not in first
    assert "[Table of Contents](#table-of-contents)" not in first


def test_run_and_main_apply_document_root(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text("# Guide  \n", encoding="utf-8")
    reports = tmp_path / "reports"

    result = FlextQualityDocumentationOptimizer.Run(
        fix_formatting=True,
        backup=False,
        document_root=str(tmp_path),
        output=str(reports),
    ).execute()

    assert result.success
    assert document.read_text(encoding="utf-8") == "# Guide\n"
    assert (
        FlextQualityDocumentationOptimizer.main([
            "run",
            "--fix-formatting",
            "--no-backup",
            "--document-root",
            str(tmp_path),
            "--output",
            str(reports),
        ])
        == 0
    )
