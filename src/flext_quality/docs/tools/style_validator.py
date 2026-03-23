#!/usr/bin/env python3
"""FLEXT Quality Style Validation Tool.

Comprehensive style checking and consistency validation for documentation.
Enforces style guides, formatting standards, and accessibility requirements.
"""

from __future__ import annotations

import operator
import re
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

import yaml
from pydantic import TypeAdapter


class StyleIssue(TypedDict):
    """Represents a single style issue or violation."""

    type: str
    line: int
    content: str
    message: str
    severity: str


class FileResults(TypedDict):
    """Results from validating a single file."""

    file: str
    violations: Sequence[StyleIssue]
    issues: Sequence[StyleIssue]
    suggestions: Sequence[str]


class MarkdownConfig(TypedDict, total=False):
    """Markdown formatting configuration."""

    heading_style: str
    list_style: str
    emphasis_style: str
    code_block_style: str


class FormattingConfig(TypedDict, total=False):
    """Formatting configuration."""

    max_line_length: int
    trailing_spaces: bool
    consistent_indentation: bool


class AccessibilityConfig(TypedDict, total=False):
    """Accessibility configuration."""

    require_alt_text: bool
    descriptive_links: bool
    heading_structure: bool
    proper_headings: bool


class HeadingsConfig(TypedDict, total=False):
    """Headings configuration."""

    enforce_hierarchy: bool


class StyleConfig(TypedDict, total=False):
    """Complete style configuration."""

    markdown: MarkdownConfig
    formatting: FormattingConfig
    accessibility: AccessibilityConfig
    headings: HeadingsConfig


class SummaryMetrics(TypedDict):
    """Summary metrics for validation results."""

    total_violations: int
    critical_issues: int
    warnings: int
    suggestions_count: int
    accessibility_issues: int


class ValidationResults(TypedDict):
    """Complete validation results."""

    files_checked: int
    style_violations: Sequence[StyleIssue]
    accessibility_issues: Sequence[StyleIssue]
    formatting_errors: Sequence[StyleIssue]
    suggestions: Sequence[str]
    summary: SummaryMetrics


_RESULTS_ADAPTER: TypeAdapter[ValidationResults] = TypeAdapter(ValidationResults)


class StyleValidator:
    """Documentation style validation and consistency checking system."""

    # Constants for magic numbers
    MIN_INLINE_CODE_BACKTICKS: int = 2
    MAX_LINE_PREVIEW_LENGTH: int = 50
    MAX_LINE_TOO_LONG_VIOLATIONS: int = 5
    MIN_COMMAND_LINE_ARGS: int = 2
    CONFIG_ARG_INDEX: int = 2

    def __init__(
        self,
        config_path: str | None = "docs/maintenance/config/style_guide.yaml",
    ) -> None:
        """Initialize style validator with configuration.

        Args:
            config_path: Path to style guide configuration file

        """
        self.config: StyleConfig = {}
        self.load_config(config_path)
        self.results: ValidationResults = {
            "files_checked": 0,
            "style_violations": [],
            "accessibility_issues": [],
            "formatting_errors": [],
            "suggestions": [],
            "summary": {
                "total_violations": 0,
                "critical_issues": 0,
                "warnings": 0,
                "suggestions_count": 0,
                "accessibility_issues": 0,
            },
        }

    def load_config(self, config_path: str | None) -> None:
        """Load style guide configuration."""
        if config_path is None:
            self.config = {
                "markdown": {
                    "heading_style": "atx",
                    "list_style": "dash",
                    "emphasis_style": "*",
                },
                "accessibility": {
                    "require_alt_text": True,
                    "descriptive_links": True,
                    "heading_structure": True,
                },
            }
            return
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                loaded_obj: Mapping[str, Mapping[str, str | int | bool]] | None = (
                    yaml.safe_load(f)
                )
                if isinstance(loaded_obj, dict):
                    self.config = self._normalize_config(loaded_obj)
                else:
                    self._set_default_config()
        except (FileNotFoundError, KeyError, OSError):
            self._set_default_config()

    def _normalize_config(
        self, raw: Mapping[str, Mapping[str, str | int | bool]]
    ) -> StyleConfig:
        config: StyleConfig = {}

        markdown_raw = raw.get("markdown")
        if isinstance(markdown_raw, dict):
            markdown: MarkdownConfig = {}
            heading_style = markdown_raw.get("heading_style")
            list_style = markdown_raw.get("list_style")
            emphasis_style = markdown_raw.get("emphasis_style")
            code_block_style = markdown_raw.get("code_block_style")
            if isinstance(heading_style, str):
                markdown["heading_style"] = heading_style
            if isinstance(list_style, str):
                markdown["list_style"] = list_style
            if isinstance(emphasis_style, str):
                markdown["emphasis_style"] = emphasis_style
            if isinstance(code_block_style, str):
                markdown["code_block_style"] = code_block_style
            config["markdown"] = markdown

        formatting_raw = raw.get("formatting")
        if isinstance(formatting_raw, dict):
            formatting: FormattingConfig = {}
            max_line_length = formatting_raw.get("max_line_length")
            trailing_spaces = formatting_raw.get("trailing_spaces")
            consistent_indentation = formatting_raw.get("consistent_indentation")
            if isinstance(max_line_length, int):
                formatting["max_line_length"] = max_line_length
            if isinstance(trailing_spaces, bool):
                formatting["trailing_spaces"] = trailing_spaces
            if isinstance(consistent_indentation, bool):
                formatting["consistent_indentation"] = consistent_indentation
            config["formatting"] = formatting

        accessibility_raw = raw.get("accessibility")
        if isinstance(accessibility_raw, dict):
            accessibility: AccessibilityConfig = {}
            require_alt_text = accessibility_raw.get("require_alt_text")
            descriptive_links = accessibility_raw.get("descriptive_links")
            heading_structure = accessibility_raw.get("heading_structure")
            proper_headings = accessibility_raw.get("proper_headings")
            if isinstance(require_alt_text, bool):
                accessibility["require_alt_text"] = require_alt_text
            if isinstance(descriptive_links, bool):
                accessibility["descriptive_links"] = descriptive_links
            if isinstance(heading_structure, bool):
                accessibility["heading_structure"] = heading_structure
            if isinstance(proper_headings, bool):
                accessibility["proper_headings"] = proper_headings
            config["accessibility"] = accessibility

        headings_raw = raw.get("headings")
        if isinstance(headings_raw, dict):
            headings: HeadingsConfig = {}
            enforce_hierarchy = headings_raw.get("enforce_hierarchy")
            if isinstance(enforce_hierarchy, bool):
                headings["enforce_hierarchy"] = enforce_hierarchy
            config["headings"] = headings

        return config

    def _set_default_config(self) -> None:
        """Set default configuration."""
        self.config = {
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
            "accessibility": {
                "require_alt_text": True,
                "descriptive_links": True,
                "proper_headings": True,
            },
        }

    def validate_file(self, file_path: Path) -> FileResults:
        """Validate a single documentation file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = str(
                file_path.relative_to(file_path.parents[2]),
            )

            violations_list: Sequence[StyleIssue] = []
            issues_list: Sequence[StyleIssue] = []
            suggestions_list: Sequence[str] = []
            file_results: FileResults = {
                "file": filename,
                "violations": violations_list,
                "issues": issues_list,
                "suggestions": suggestions_list,
            }

            file_results["violations"].extend(self._check_markdown_formatting(content))
            file_results["violations"].extend(self._check_heading_consistency(content))
            file_results["violations"].extend(self._check_list_consistency(content))
            file_results["violations"].extend(self._check_code_formatting(content))
            file_results["issues"].extend(self._check_accessibility(content))
            file_results["violations"].extend(self._check_line_length(content))
            file_results["violations"].extend(self._check_whitespace(content))

            file_results["suggestions"] = self._generate_suggestions(
                file_results["violations"],
            )

            self.results["files_checked"] += 1
            self.results["style_violations"].extend(file_results["violations"])
            self.results["accessibility_issues"].extend(file_results["issues"])
            self.results["suggestions"].extend(file_results["suggestions"])

            return file_results

        except (
            FileNotFoundError,
            PermissionError,
            UnicodeDecodeError,
            OSError,
            ValueError,
        ):
            return {
                "file": str(file_path),
                "violations": [],
                "issues": [],
                "suggestions": [],
            }

    def _check_markdown_formatting(self, content: str) -> Sequence[StyleIssue]:
        """Check basic markdown formatting consistency."""
        violations: Sequence[StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            markdown_config = self.config.get("markdown", {})
            emphasis_style = markdown_config.get("emphasis_style", "*")
            if emphasis_style == "*" and re.search(
                r"(?<!\\)_[^_]+_(?!\\)",
                line,
            ):
                violations.append({
                    "type": "emphasis_style",
                    "line": i,
                    "content": line.strip(),
                    "message": "Use * for emphasis instead of _",
                    "severity": "low",
                })

            if line.startswith("#") and not re.match(r"^#{1,6}\s", line):
                violations.append({
                    "type": "heading_format",
                    "line": i,
                    "content": line.strip(),
                    "message": "Headings should have a space after #",
                    "severity": "medium",
                })

        return violations

    def _check_heading_consistency(self, content: str) -> Sequence[StyleIssue]:
        """Check heading hierarchy and consistency."""
        violations: Sequence[StyleIssue] = []

        headings: Sequence[tuple[int, str, int]] = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            line_num = content[: match.start()].count("\n") + 1
            headings.append((level, text, line_num))

        headings_config = self.config.get("headings", {})
        enforce_hierarchy = headings_config.get("enforce_hierarchy", True)
        if enforce_hierarchy:
            expected_level = 1
            for level, text, line_num in headings:
                if level > expected_level + 1:
                    violations.append({
                        "type": "heading_hierarchy",
                        "line": line_num,
                        "content": f"{'#' * level} {text}",
                        "message": f"Heading skips level (expected H{expected_level} or H{expected_level + 1}, got H{level})",
                        "severity": "medium",
                    })
                expected_level = level

        if headings and headings[0][0] != 1:
            violations.append({
                "type": "first_heading_level",
                "line": headings[0][2],
                "content": f"{'#' * headings[0][0]} {headings[0][1]}",
                "message": "Document should start with H1 heading",
                "severity": "low",
            })

        return violations

    def _check_list_consistency(self, content: str) -> Sequence[StyleIssue]:
        """Check list formatting consistency."""
        violations: Sequence[StyleIssue] = []

        list_items: Sequence[tuple[str, str, int]] = []
        for match in re.finditer(r"^(\s*)([-\*\+])\s+", content, re.MULTILINE):
            indent = match.group(1)
            marker = match.group(2)
            line_num = content[: match.start()].count("\n") + 1
            list_items.append((indent, marker, line_num))

        if not list_items:
            return violations

        markers = [item[1] for item in list_items]
        markdown_config = self.config.get("markdown", {})
        preferred_marker = markdown_config.get("list_style", "dash")

        marker_map = {"dash": "-", "asterisk": "*", "plus": "+"}
        preferred = marker_map.get(preferred_marker, "-")

        inconsistent_markers = [m for m in markers if m != preferred]
        if inconsistent_markers:
            violations.append({
                "type": "list_marker_consistency",
                "line": list_items[0][2],
                "content": f"List using {inconsistent_markers[0]}",
                "message": f"Use {preferred} for list markers instead of mixed styles",
                "severity": "low",
            })

        return violations

    def _check_code_formatting(self, content: str) -> Sequence[StyleIssue]:
        """Check code block and inline code formatting."""
        violations: Sequence[StyleIssue] = []

        markdown_config = self.config.get("markdown", {})
        code_block_style = markdown_config.get("code_block_style", "fenced")
        if code_block_style == "fenced":
            code_blocks = re.findall(r"```\n(.*?)\n```", content, re.DOTALL)
            violations.extend(
                {
                    "type": "code_block_language",
                    "line": content[: content.find(block)].count("\n") + 1,
                    "content": "```" + block[:50] + "...",
                    "message": "Code blocks should specify language (```language)",
                    "severity": "low",
                }
                for block in code_blocks
                if not re.match(
                    r"```\w+",
                    content[content.find(block) - 10 : content.find(block)],
                )
            )

        inline_code = re.findall(r"`[^`]+`", content)
        if inline_code:
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if (
                    "`" in line
                    and re.search(r"[a-zA-Z0-9]`[^`]+`", line)
                    and not re.search(r"\s`[^`]+`", line)
                ):
                    violations.append({
                        "type": "inline_code_spacing",
                        "line": i,
                        "content": line.strip(),
                        "message": "Add space before inline code",
                        "severity": "low",
                    })

        return violations

    def _check_accessibility(self, content: str) -> Sequence[StyleIssue]:
        """Check accessibility compliance."""
        issues: Sequence[StyleIssue] = []

        accessibility_config = self.config.get("accessibility", {})
        require_alt_text = accessibility_config.get("require_alt_text", True)
        if require_alt_text:
            images_without_alt = re.findall(r"!\[\]\([^)]+\)", content)
            if images_without_alt:
                for img in images_without_alt:
                    line_num = content[: content.find(img)].count("\n") + 1
                    issues.append({
                        "type": "missing_alt_text",
                        "line": line_num,
                        "content": img,
                        "message": "Images must have descriptive alt text",
                        "severity": "high",
                    })

        descriptive_links = accessibility_config.get("descriptive_links", True)
        if descriptive_links:
            generic_links = re.findall(
                r"\[here|click here|link|read more\]\([^)]+\)",
                content,
                re.IGNORECASE,
            )
            for link in generic_links:
                line_num = content[: content.find(link)].count("\n") + 1
                issues.append({
                    "type": "generic_link_text",
                    "line": line_num,
                    "content": link,
                    "message": "Use descriptive link text instead of generic terms",
                    "severity": "medium",
                })

        return issues

    def _check_line_length(self, content: str) -> Sequence[StyleIssue]:
        """Check line length compliance."""
        violations: Sequence[StyleIssue] = []

        formatting_config = self.config.get("formatting", {})
        max_length_val = formatting_config.get("max_line_length", 88)
        max_length = int(max_length_val)
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if len(line) > max_length and not (
                line.strip().startswith(("```", "|", "http", "https"))
                or "|" in line
                or line.count("`") >= self.MIN_INLINE_CODE_BACKTICKS
            ):
                violations.append({
                    "type": "line_too_long",
                    "line": i,
                    "content": line[: self.MAX_LINE_PREVIEW_LENGTH] + "..."
                    if len(line) > self.MAX_LINE_PREVIEW_LENGTH
                    else line,
                    "message": f"Line exceeds {max_length} characters ({len(line)} chars)",
                    "severity": "low",
                })

        return violations

    def _check_whitespace(self, content: str) -> Sequence[StyleIssue]:
        """Check whitespace formatting."""
        violations: Sequence[StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            formatting_config = self.config.get("formatting", {})
            trailing_spaces = formatting_config.get("trailing_spaces", False)
            if trailing_spaces is False and line.rstrip() != line:
                violations.append({
                    "type": "trailing_whitespace",
                    "line": i,
                    "content": line,
                    "message": "Remove trailing whitespace",
                    "severity": "low",
                })

            if i < len(lines) - 1:
                current_blank = not line.strip()
                next_blank = not lines[i].strip()
                if current_blank and next_blank:
                    violations.append({
                        "type": "multiple_blank_lines",
                        "line": i,
                        "content": "",
                        "message": "Multiple consecutive blank lines",
                        "severity": "low",
                    })

        return violations

    def _generate_suggestions(self, violations: Sequence[StyleIssue]) -> Sequence[str]:
        """Generate improvement suggestions based on violations."""
        suggestions: Sequence[str] = []

        violation_types: Mapping[str, int] = {}
        for violation in violations:
            v_type = violation["type"]
            violation_types[v_type] = violation_types.get(v_type, 0) + 1

        if violation_types.get("emphasis_style", 0) > 0:
            suggestions.append(
                "Standardize emphasis markers (*bold* and _italic_ vs mixed usage)",
            )

        if violation_types.get("heading_hierarchy", 0) > 0:
            suggestions.append("Fix heading hierarchy to avoid skipping levels")

        if violation_types.get("list_marker_consistency", 0) > 0:
            markdown_config = self.config.get("markdown", {})
            preferred = markdown_config.get("list_style", "dash")
            suggestions.append(f"Use consistent list markers ({preferred}) throughout")

        if violation_types.get("missing_alt_text", 0) > 0:
            suggestions.append(
                "Add descriptive alt text to all images for accessibility",
            )

        if violation_types.get("line_too_long", 0) > self.MAX_LINE_TOO_LONG_VIOLATIONS:
            suggestions.append("Consider breaking long lines or using line wrapping")

        return suggestions

    def validate_files_batch(self, file_paths: Sequence[Path]) -> ValidationResults:
        """Validate multiple files and aggregate results."""
        for file_path in file_paths:
            self.validate_file(file_path)

        style_violations = self.results["style_violations"]
        accessibility_issues = self.results["accessibility_issues"]
        suggestions = self.results["suggestions"]

        self.results["summary"]["total_violations"] = len(style_violations)
        self.results["summary"]["accessibility_issues"] = len(accessibility_issues)
        self.results["summary"]["suggestions_count"] = len(suggestions)

        all_violations: Sequence[StyleIssue] = []
        all_violations.extend(style_violations)
        all_violations.extend(accessibility_issues)

        for violation in all_violations:
            severity = violation.get("severity", "low")
            if severity == "critical":
                self.results["summary"]["critical_issues"] += 1
            elif severity == "high":
                self.results["summary"]["warnings"] += 1

        return self.results

    def generate_report(self, output_format: str = "json") -> str:
        """Generate style validation report."""
        if output_format == "json":
            return _RESULTS_ADAPTER.dump_json(self.results, indent=2).decode()
        if output_format == "summary":
            return self._generate_summary_report()
        return _RESULTS_ADAPTER.dump_json(self.results).decode()

    def _generate_summary_report(self) -> str:
        """Generate human-readable summary."""
        summary = self.results["summary"]

        report = f"""
Style Validation Summary
========================

Files Checked: {self.results["files_checked"]}
Total Violations: {summary["total_violations"]}
Accessibility Issues: {summary["accessibility_issues"]}
Critical Issues: {summary["critical_issues"]}
Warnings: {summary["warnings"]}
Suggestions: {summary["suggestions_count"]}

Top Issues:
"""

        # Count issue types
        issue_types: Mapping[str, int] = {}
        for violation in (
            self.results["style_violations"] + self.results["accessibility_issues"]
        ):
            v_type = violation["type"]
            issue_types[v_type] = issue_types.get(v_type, 0) + 1

        # Show top 5 issues
        sorted_issues = sorted(
            issue_types.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )
        for issue_type, count in sorted_issues[:5]:
            report += f"- {issue_type.replace('_', ' ').title()}: {count}\n"

        if self.results["suggestions"]:
            report += "\nSuggestions:\n"
            for suggestion in self.results["suggestions"][:3]:
                report += f"- {suggestion}\n"

        return report

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> Path:
        """Save style validation report."""
        Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"style_validation_{timestamp}.json"
        filepath = Path(output_path) / filename

        filepath.write_bytes(_RESULTS_ADAPTER.dump_json(self.results, indent=2))

        return filepath


def validate_file_style(
    file_path: str,
    config_path: str | None = None,
) -> FileResults:
    """Convenience function to validate a single file."""
    validator = StyleValidator(config_path)
    return validator.validate_file(Path(file_path))


def validate_files_style(
    file_paths: Sequence[str],
    config_path: str | None = None,
) -> ValidationResults:
    """Convenience function to validate multiple files."""
    validator = StyleValidator(config_path)
    paths = [Path(fp) for fp in file_paths]
    return validator.validate_files_batch(paths)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < StyleValidator.MIN_COMMAND_LINE_ARGS:
        sys.exit(1)

    file_path = sys.argv[1]
    config_path = (
        sys.argv[StyleValidator.CONFIG_ARG_INDEX]
        if len(sys.argv) > StyleValidator.CONFIG_ARG_INDEX
        else None
    )

    results = validate_file_style(file_path, config_path)

    for _violation in results["violations"][:3]:  # Show first 3
        pass
