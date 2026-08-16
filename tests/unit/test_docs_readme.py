"""Packaged documentation-tool guide behavior."""

from __future__ import annotations

from pathlib import Path

from flext_quality import u


def test_docs_readme_uses_current_project_and_public_surfaces() -> None:
    project_root = Path(__file__).parents[2]
    metadata = u.Cli.toml_read_json(project_root / "pyproject.toml").unwrap()
    project = metadata["project"]
    assert isinstance(project, dict)
    python_range = project["requires-python"]
    readme = (project_root / "src" / "flext_quality" / "docs" / "README.md").read_text(
        encoding="utf-8"
    )

    assert f"Python `{python_range}`" in readme
    assert "src/flext_quality/docs/config/" in readme
    for command in (
        "make setup",
        "make gen WHAT=check",
        "make check",
        "make test FILE=tests/unit/test_docs_auditor.py",
        "make build WHAT=artifacts",
    ):
        assert command in readme
    for module in (
        "flext_quality.docs.scripts.audit",
        "flext_quality.docs.scripts.optimize",
        "flext_quality.docs.scripts.validate",
        "flext_quality.docs.scripts.report",
        "flext_quality.docs.notifications",
        "flext_quality.docs.tools.style_validator",
    ):
        assert module in readme
    for stale in (
        "pip install",
        "Python 3.8",
        "docs/maintenance",
        "demo.py",
        "cron:",
        "backward compatibility",
    ):
        assert stale not in readme
