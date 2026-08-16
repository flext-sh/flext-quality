"""Public documentation style-validation behavior."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_quality import u
from flext_quality.docs import FlextQualityStyleValidator


def test_validate_file_reports_markdown_structure_and_accessibility(
    tmp_path: Path,
) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "##No space\n# Start\n#### Skipped\n* first\n+ second\n```\ncode\n```\n"
        "See [here](guide.md).\n![](diagram.png)\ntext with trailing space  \n"
        + "x"
        * 100,
        encoding="utf-8",
    )
    shipped = u.Cli.yaml_load_mapping(
        Path(__file__).parents[2]
        / "src"
        / "flext_quality"
        / "docs"
        / "config"
        / "style_guide.yaml"
    )
    validator = FlextQualityStyleValidator()

    result = validator.validate_file(document)

    violation_types = {issue.type for issue in result.violations}
    accessibility_types = {issue.type for issue in result.issues}
    expected = {
        "heading_format",
        "heading_hierarchy",
        "list_marker_consistency",
        "line_too_long",
        "trailing_whitespace",
    }
    code = shipped["code"]
    assert isinstance(code, dict)
    if code["require_language_specifier"]:
        expected.add("code_block_language")
    assert expected.issubset(violation_types)
    assert {"missing_alt_text", "generic_link_text"}.issubset(accessibility_types)


def test_validate_files_batch_calculates_summary(tmp_path: Path) -> None:
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    first.write_text("# First\n", encoding="utf-8")
    second.write_text("![](image.png)\n", encoding="utf-8")
    validator = FlextQualityStyleValidator()

    result = validator.validate_files_batch([first, second])

    assert result.files_checked == 2
    assert result.summary.accessibility_issues == 1


def test_main_accepts_explicit_arguments(tmp_path: Path) -> None:
    clean = tmp_path / "clean.md"
    violating = tmp_path / "violating.md"
    clean.write_text("# Guide\n", encoding="utf-8")
    violating.write_text("##No space\n", encoding="utf-8")

    assert FlextQualityStyleValidator.main([str(clean)]) == 0
    assert FlextQualityStyleValidator.main([str(violating)]) == 1
    assert FlextQualityStyleValidator.main([]) == 1


def test_documented_relative_module_command_reports_clean_and_violating_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    clean = tmp_path / "clean.md"
    violating = tmp_path / "violating.md"
    clean.write_text("# Guide\n", encoding="utf-8")
    violating.write_text("##No space\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    clean_exit = FlextQualityStyleValidator.main([clean.name])
    violating_exit = FlextQualityStyleValidator.main([violating.name])

    assert clean_exit == 0
    assert violating_exit != 0


def test_generic_markdown_links_are_reported_without_matching_prose(
    tmp_path: Path,
) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "[here](one.md)\n[click here](two.md)\n[link](three.md)\n"
        "[read more](four.md)\n[configuration guide](five.md)\n"
        "Click here for ordinary prose.\n",
        encoding="utf-8",
    )

    result = FlextQualityStyleValidator().validate_file(document)

    generic_links = [
        issue.content for issue in result.issues if issue.type == "generic_link_text"
    ]
    assert generic_links == [
        "[here](one.md)",
        "[click here](two.md)",
        "[link](three.md)",
        "[read more](four.md)",
    ]


def test_code_fence_language_rule_ignores_closing_fence(tmp_path: Path) -> None:
    config = tmp_path / "style.yaml"
    config.write_text(u.Cli.yaml_dump_str(_minimal_style_config()), encoding="utf-8")
    document = tmp_path / "guide.md"
    document.write_text("```python\nprint('ok')\n```\n", encoding="utf-8")

    result = FlextQualityStyleValidator(str(config)).validate_file(document)

    assert all(issue.type != "code_block_language" for issue in result.violations)


def test_code_fence_language_rule_reports_only_unlabeled_opening(
    tmp_path: Path,
) -> None:
    config = tmp_path / "style.yaml"
    config.write_text(u.Cli.yaml_dump_str(_minimal_style_config()), encoding="utf-8")
    document = tmp_path / "guide.md"
    document.write_text("```\nplain\n```\n", encoding="utf-8")

    result = FlextQualityStyleValidator(str(config)).validate_file(document)

    language_issues = [
        issue for issue in result.violations if issue.type == "code_block_language"
    ]
    assert len(language_issues) == 1
    assert language_issues[0].line == 1


def _minimal_style_config() -> dict[str, dict[str, str | int | bool]]:
    return {
        "markdown": {
            "heading_style": "atx",
            "list_style": "dash",
            "emphasis_style": "*",
            "code_block_style": "fenced",
        },
        "formatting": {
            "max_line_length": 88,
            "trailing_spaces": False,
            "consistent_indentation": True,
        },
        "accessibility": {"require_alt_text": True, "descriptive_link_text": True},
        "headings": {
            "enforce_hierarchy": True,
            "first_heading_level": 1,
            "max_heading_level": 4,
        },
        "code": {"require_language_specifier": True},
    }


def test_heading_hierarchy_uses_typed_non_default_config(tmp_path: Path) -> None:
    config_data = _minimal_style_config()
    config_data["headings"] = {
        "enforce_hierarchy": True,
        "first_heading_level": 2,
        "max_heading_level": 3,
    }
    config = tmp_path / "style.yaml"
    config.write_text(u.Cli.yaml_dump_str(config_data), encoding="utf-8")
    document = tmp_path / "guide.md"
    document.write_text("# Too early\n## Start\n#### Too deep\n", encoding="utf-8")

    result = FlextQualityStyleValidator(str(config)).validate_file(document)

    heading_issues = [
        issue
        for issue in result.violations
        if issue.type in {"first_heading_level", "heading_level"}
    ]
    assert sorted((issue.type, issue.line) for issue in heading_issues) == [
        ("first_heading_level", 1),
        ("heading_level", 3),
    ]
