#!/usr/bin/env python3
"""FLEXT Quality Style Validation Tool.

Comprehensive style checking and consistency validation for documentation.
Enforces style guides, formatting standards, and accessibility requirements.
"""

from __future__ import annotations

import operator
import re
import sys
from collections.abc import (
    MutableSequence,
    Sequence,
)
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

from flext_quality import m, t, u


class FlextQualityStyleValidator:
    """Documentation style validation and consistency checking system."""

    class StyleIssue(m.BaseModel):
        """Represents a single style issue or violation."""

        type: str
        line: int
        content: str
        message: str
        severity: str

    class FileResults(m.BaseModel):
        """Results from validating a single file."""

        file: str
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue]
        issues: MutableSequence[FlextQualityStyleValidator.StyleIssue]
        suggestions: MutableSequence[str]

    class MarkdownConfig(m.BaseModel):
        """Markdown formatting configuration."""

        heading_style: str | None = None
        list_style: str | None = None
        emphasis_style: str | None = None
        code_block_style: str | None = None

    class FormattingConfig(m.BaseModel):
        """Formatting configuration."""

        max_line_length: int | None = None
        trailing_spaces: bool | None = None
        consistent_indentation: bool | None = None

    class AccessibilityConfig(m.BaseModel):
        """Accessibility configuration."""

        require_alt_text: bool | None = None
        descriptive_links: bool | None = None
        heading_structure: bool | None = None
        proper_headings: bool | None = None

    class HeadingsConfig(m.BaseModel):
        """Headings configuration."""

        enforce_hierarchy: bool | None = None

    class StyleConfig(m.BaseModel):
        """Complete style configuration."""

        markdown: FlextQualityStyleValidator.MarkdownConfig | None = None
        formatting: FlextQualityStyleValidator.FormattingConfig | None = None
        accessibility: FlextQualityStyleValidator.AccessibilityConfig | None = None
        headings: FlextQualityStyleValidator.HeadingsConfig | None = None

    class SummaryMetrics(m.BaseModel):
        """Summary metrics for validation results."""

        total_violations: int
        critical_issues: int
        warnings: int
        suggestions_count: int
        accessibility_issues: int

    class ValidationResults(m.BaseModel):
        """Complete validation results."""

        files_checked: int
        style_violations: MutableSequence[FlextQualityStyleValidator.StyleIssue]
        accessibility_issues: MutableSequence[FlextQualityStyleValidator.StyleIssue]
        formatting_errors: MutableSequence[FlextQualityStyleValidator.StyleIssue]
        suggestions: MutableSequence[str]
        summary: FlextQualityStyleValidator.SummaryMetrics

    RESULTS_ADAPTER: ClassVar[m.TypeAdapter[ValidationResults]] = m.TypeAdapter(
        ValidationResults
    )

    # Constants for magic numbers
    MIN_INLINE_CODE_BACKTICKS: int = 2
    MAX_LINE_PREVIEW_LENGTH: int = 50
    MAX_LINE_TOO_LONG_VIOLATIONS: int = 5
    MIN_COMMAND_LINE_ARGS: int = 2
    CONFIG_ARG_INDEX: int = 2

    def __init__(
        self,
        config_path: str | None = "docs/maintenance/settings/style_guide.yaml",
    ) -> None:
        """Initialize style validator with configuration.

        Args:
            config_path: Path to style guide configuration file

        """
        self.settings: FlextQualityStyleValidator.StyleConfig = (
            FlextQualityStyleValidator.StyleConfig()
        )
        self.load_config(config_path)
        self.results: FlextQualityStyleValidator.ValidationResults = (
            FlextQualityStyleValidator.ValidationResults(
                files_checked=0,
                style_violations=[],
                accessibility_issues=[],
                formatting_errors=[],
                suggestions=[],
                summary=FlextQualityStyleValidator.SummaryMetrics(
                    total_violations=0,
                    critical_issues=0,
                    warnings=0,
                    suggestions_count=0,
                    accessibility_issues=0,
                ),
            )
        )

    def load_config(self, config_path: str | None) -> None:
        """Load style guide configuration."""
        if config_path is None:
            self.settings = FlextQualityStyleValidator.StyleConfig(
                markdown=FlextQualityStyleValidator.MarkdownConfig(
                    heading_style="atx",
                    list_style="dash",
                    emphasis_style="*",
                ),
                accessibility=FlextQualityStyleValidator.AccessibilityConfig(
                    require_alt_text=True,
                    descriptive_links=True,
                    heading_structure=True,
                ),
            )
            return
        try:
            loaded_obj = u.Cli.yaml_load_mapping(Path(config_path))
            if loaded_obj:
                self.settings = self._normalize_config(loaded_obj)
            else:
                self._set_default_config()
        except (FileNotFoundError, KeyError, OSError):
            self._set_default_config()

    def _normalize_config(
        self,
        raw: t.JsonMapping,
    ) -> FlextQualityStyleValidator.StyleConfig:
        markdown_raw = raw.get("markdown")
        markdown = (
            FlextQualityStyleValidator.MarkdownConfig.model_validate(markdown_raw)
            if isinstance(markdown_raw, dict)
            else None
        )

        formatting_raw = raw.get("formatting")
        formatting = (
            FlextQualityStyleValidator.FormattingConfig.model_validate(formatting_raw)
            if isinstance(formatting_raw, dict)
            else None
        )

        accessibility_raw = raw.get("accessibility")
        accessibility = (
            FlextQualityStyleValidator.AccessibilityConfig.model_validate(
                accessibility_raw,
            )
            if isinstance(accessibility_raw, dict)
            else None
        )

        headings_raw = raw.get("headings")
        headings = (
            FlextQualityStyleValidator.HeadingsConfig.model_validate(headings_raw)
            if isinstance(headings_raw, dict)
            else None
        )

        return FlextQualityStyleValidator.StyleConfig(
            markdown=markdown,
            formatting=formatting,
            accessibility=accessibility,
            headings=headings,
        )

    def _set_default_config(self) -> None:
        """Set default configuration."""
        self.settings = FlextQualityStyleValidator.StyleConfig(
            markdown=FlextQualityStyleValidator.MarkdownConfig(
                heading_style="atx",
                list_style="dash",
                emphasis_style="*",
                code_block_style="fenced",
            ),
            formatting=FlextQualityStyleValidator.FormattingConfig(
                max_line_length=88,
                trailing_spaces=False,
                consistent_indentation=True,
            ),
            accessibility=FlextQualityStyleValidator.AccessibilityConfig(
                require_alt_text=True,
                descriptive_links=True,
                proper_headings=True,
            ),
        )

    def validate_file(
        self,
        file_path: Path,
    ) -> FlextQualityStyleValidator.FileResults:
        """Validate a single documentation file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = (file_path.relative_to(file_path.parents[2]),)

            violations_list: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []
            issues_list: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []
            suggestions_list: MutableSequence[str] = []
            file_results: FlextQualityStyleValidator.FileResults = (
                FlextQualityStyleValidator.FileResults.model_validate({
                    "file": filename,
                    "violations": violations_list,
                    "issues": issues_list,
                    "suggestions": suggestions_list,
                })
            )

            file_results.violations.extend(self._check_markdown_formatting(content))
            file_results.violations.extend(self._check_heading_consistency(content))
            file_results.violations.extend(self._check_list_consistency(content))
            file_results.violations.extend(self._check_code_formatting(content))
            file_results.issues.extend(self._check_accessibility(content))
            file_results.violations.extend(self._check_line_length(content))
            file_results.violations.extend(self._check_whitespace(content))

            file_results.suggestions = list(
                self._generate_suggestions(
                    file_results.violations,
                ),
            )

            self.results.files_checked += 1
            self.results.style_violations.extend(file_results.violations)
            self.results.accessibility_issues.extend(file_results.issues)
            self.results.suggestions.extend(file_results.suggestions)

            return file_results

        except (
            FileNotFoundError,
            PermissionError,
            UnicodeDecodeError,
            OSError,
            ValueError,
        ):
            return FlextQualityStyleValidator.FileResults(
                file=str(file_path),
                violations=[],
                issues=[],
                suggestions=[],
            )

    def _check_markdown_formatting(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check basic markdown formatting consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            emphasis_style = (
                self.settings.markdown.emphasis_style
                if self.settings.markdown
                else None
            )
            if emphasis_style == "*" and re.search(
                r"(?<!\\)_[^_]+_(?!\\)",
                line,
            ):
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="emphasis_style",
                        line=i,
                        content=line.strip(),
                        message="Use * for emphasis instead of _",
                        severity="low",
                    ),
                )

            if line.startswith("#") and not re.match(r"^#{1,6}\s", line):
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="heading_format",
                        line=i,
                        content=line.strip(),
                        message="Headings should have a space after #",
                        severity="medium",
                    ),
                )

        return violations

    def _check_heading_consistency(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check heading hierarchy and consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        headings: Sequence[tuple[int, str, int]] = [
            (
                len(match.group(1)),
                match.group(2).strip(),
                content[: match.start()].count("\n") + 1,
            )
            for match in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
        ]

        enforce_hierarchy = (
            self.settings.headings.enforce_hierarchy if self.settings.headings else True
        )
        if enforce_hierarchy is not False:
            expected_level = 1
            for level, text, line_num in headings:
                if level > expected_level + 1:
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="heading_hierarchy",
                            line=line_num,
                            content=f"{'#' * level} {text}",
                            message=f"Heading skips level (expected H{expected_level} or H{expected_level + 1}, got H{level})",
                            severity="medium",
                        ),
                    )
                expected_level = level

        if headings and headings[0][0] != 1:
            violations.append(
                FlextQualityStyleValidator.StyleIssue(
                    type="first_heading_level",
                    line=headings[0][2],
                    content=f"{'#' * headings[0][0]} {headings[0][1]}",
                    message="Document should start with H1 heading",
                    severity="low",
                ),
            )

        return violations

    def _check_list_consistency(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check list formatting consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        list_items: Sequence[tuple[str, str, int]] = [
            (
                match.group(1),
                match.group(2),
                content[: match.start()].count("\n") + 1,
            )
            for match in re.finditer(r"^(\s*)([-\*\+])\s+", content, re.MULTILINE)
        ]

        if not list_items:
            return violations

        markers = [item[1] for item in list_items]
        preferred_marker = (
            self.settings.markdown.list_style if self.settings.markdown else "dash"
        )

        marker_map = {"dash": "-", "asterisk": "*", "plus": "+"}
        preferred = marker_map.get(preferred_marker or "dash", "-")

        inconsistent_markers = [m for m in markers if m != preferred]
        if inconsistent_markers:
            violations.append(
                FlextQualityStyleValidator.StyleIssue(
                    type="list_marker_consistency",
                    line=list_items[0][2],
                    content=f"List using {inconsistent_markers[0]}",
                    message=f"Use {preferred} for list markers instead of mixed styles",
                    severity="low",
                ),
            )

        return violations

    def _check_code_formatting(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check code block and inline code formatting."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        code_block_style = (
            self.settings.markdown.code_block_style
            if self.settings.markdown
            else "fenced"
        )
        if code_block_style == "fenced":
            code_blocks = re.findall(r"```\n(.*?)\n```", content, re.DOTALL)
            violations.extend(
                FlextQualityStyleValidator.StyleIssue(
                    type="code_block_language",
                    line=content[: content.find(block)].count("\n") + 1,
                    content="```" + block[:50] + "...",
                    message="Code blocks should specify language (```language)",
                    severity="low",
                )
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
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="inline_code_spacing",
                            line=i,
                            content=line.strip(),
                            message="Add space before inline code",
                            severity="low",
                        ),
                    )

        return violations

    def _check_accessibility(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check accessibility compliance."""
        issues: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        require_alt_text = (
            self.settings.accessibility.require_alt_text
            if self.settings.accessibility
            else True
        )
        if require_alt_text is not False:
            images_without_alt = re.findall(r"!\[\]\([^)]+\)", content)
            if images_without_alt:
                for img in images_without_alt:
                    line_num = content[: content.find(img)].count("\n") + 1
                    issues.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="missing_alt_text",
                            line=line_num,
                            content=img,
                            message="Images must have descriptive alt text",
                            severity="high",
                        ),
                    )

        descriptive_links = (
            self.settings.accessibility.descriptive_links
            if self.settings.accessibility
            else True
        )
        if descriptive_links is not False:
            generic_links = re.findall(
                r"\[here|click here|link|read more\]\([^)]+\)",
                content,
                re.IGNORECASE,
            )
            for link in generic_links:
                line_num = content[: content.find(link)].count("\n") + 1
                issues.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="generic_link_text",
                        line=line_num,
                        content=link,
                        message="Use descriptive link text instead of generic terms",
                        severity="medium",
                    ),
                )

        return issues

    def _check_line_length(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check line length compliance."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        max_length_val = (
            self.settings.formatting.max_line_length if self.settings.formatting else 88
        )
        max_length = max_length_val or 88
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if len(line) > max_length and not (
                line.strip().startswith(("```", "|", "http", "https"))
                or "|" in line
                or line.count("`") >= self.MIN_INLINE_CODE_BACKTICKS
            ):
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="line_too_long",
                        line=i,
                        content=line[: self.MAX_LINE_PREVIEW_LENGTH] + "..."
                        if len(line) > self.MAX_LINE_PREVIEW_LENGTH
                        else line,
                        message=f"Line exceeds {max_length} characters ({len(line)} chars)",
                        severity="low",
                    ),
                )

        return violations

    def _check_whitespace(
        self,
        content: str,
    ) -> Sequence[FlextQualityStyleValidator.StyleIssue]:
        """Check whitespace formatting."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            trailing_spaces = (
                self.settings.formatting.trailing_spaces
                if self.settings.formatting
                else False
            )
            if trailing_spaces is False and line.rstrip() != line:
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="trailing_whitespace",
                        line=i,
                        content=line,
                        message="Remove trailing whitespace",
                        severity="low",
                    ),
                )

            if i < len(lines) - 1:
                current_blank = not line.strip()
                next_blank = not lines[i].strip()
                if current_blank and next_blank:
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="multiple_blank_lines",
                            line=i,
                            content="",
                            message="Multiple consecutive blank lines",
                            severity="low",
                        ),
                    )

        return violations

    def _generate_suggestions(
        self,
        violations: Sequence[FlextQualityStyleValidator.StyleIssue],
    ) -> t.StrSequence:
        """Generate improvement suggestions based on violations."""
        suggestions: MutableSequence[str] = []

        violation_types: t.MutableIntMapping = {}
        for violation in violations:
            v_type = violation.type
            violation_types[v_type] = violation_types.get(v_type, 0) + 1

        if violation_types.get("emphasis_style", 0) > 0:
            suggestions.append(
                "Standardize emphasis markers (*bold* and _italic_ vs mixed usage)",
            )

        if violation_types.get("heading_hierarchy", 0) > 0:
            suggestions.append("Fix heading hierarchy to avoid skipping levels")

        if violation_types.get("list_marker_consistency", 0) > 0:
            preferred = (
                self.settings.markdown.list_style if self.settings.markdown else "dash"
            )
            suggestions.append(f"Use consistent list markers ({preferred}) throughout")

        if violation_types.get("missing_alt_text", 0) > 0:
            suggestions.append(
                "Add descriptive alt text to all images for accessibility",
            )

        if violation_types.get("line_too_long", 0) > self.MAX_LINE_TOO_LONG_VIOLATIONS:
            suggestions.append("Consider breaking long lines or using line wrapping")

        return suggestions

    def validate_files_batch(
        self,
        file_paths: Sequence[Path],
    ) -> FlextQualityStyleValidator.ValidationResults:
        """Validate multiple files and aggregate results."""
        for file_path in file_paths:
            self.validate_file(file_path)

        style_violations = self.results.style_violations
        accessibility_issues = self.results.accessibility_issues
        suggestions = self.results.suggestions

        self.results.summary.total_violations = len(style_violations)
        self.results.summary.accessibility_issues = len(accessibility_issues)
        self.results.summary.suggestions_count = len(suggestions)

        all_violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []
        all_violations.extend(style_violations)
        all_violations.extend(accessibility_issues)

        for violation in all_violations:
            severity = violation.severity
            if severity == "critical":
                self.results.summary.critical_issues += 1
            elif severity == "high":
                self.results.summary.warnings += 1

        return self.results

    def generate_report(self, output_format: str = "json") -> str:
        """Generate style validation report."""
        if output_format == "summary":
            return self._generate_summary_report()
        report_text: str = (
            self.RESULTS_ADAPTER.dump_json(self.results, indent=2).decode()
            if output_format == "json"
            else self.RESULTS_ADAPTER.dump_json(self.results).decode()
        )
        return report_text

    def _generate_summary_report(self) -> str:
        """Generate human-readable summary."""
        summary = self.results.summary

        report = f"""
Style Validation Summary
========================

Files Checked: {self.results.files_checked}
Total Violations: {summary.total_violations}
Accessibility Issues: {summary.accessibility_issues}
Critical Issues: {summary.critical_issues}
Warnings: {summary.warnings}
Suggestions: {summary.suggestions_count}

Top Issues:
"""

        # Count issue types
        issue_types: t.MutableIntMapping = {}
        for violation in [
            *self.results.style_violations,
            *self.results.accessibility_issues,
        ]:
            v_type = violation.type
            issue_types[v_type] = issue_types.get(v_type, 0) + 1

        # Show top 5 issues
        sorted_issues = sorted(
            issue_types.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )
        for issue_type, count in sorted_issues[:5]:
            report += f"- {issue_type.replace('_', ' ').title()}: {count}\n"

        if self.results.suggestions:
            report += "\nSuggestions:\n"
            for suggestion in self.results.suggestions[:3]:
                report += f"- {suggestion}\n"

        return report

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> Path:
        """Save style validation report."""
        Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"style_validation_{timestamp}.json"
        filepath = Path(output_path) / filename

        filepath.write_bytes(self.RESULTS_ADAPTER.dump_json(self.results, indent=2))

        return filepath


def validate_file_style(
    file_path: str,
    config_path: str | None = None,
) -> FlextQualityStyleValidator.FileResults:
    """Convenience function to validate a single file."""
    validator = FlextQualityStyleValidator(config_path)
    return validator.validate_file(Path(file_path))


def validate_files_style(
    file_paths: t.StrSequence,
    config_path: str | None = None,
) -> FlextQualityStyleValidator.ValidationResults:
    """Convenience function to validate multiple files."""
    validator = FlextQualityStyleValidator(config_path)
    paths = [Path(fp) for fp in file_paths]
    return validator.validate_files_batch(paths)


def _main() -> int:
    """Run the CLI entrypoint without exporting temporary module names."""
    if len(sys.argv) < FlextQualityStyleValidator.MIN_COMMAND_LINE_ARGS:
        return 1

    file_path = sys.argv[1]
    config_path = (
        sys.argv[FlextQualityStyleValidator.CONFIG_ARG_INDEX]
        if len(sys.argv) > FlextQualityStyleValidator.CONFIG_ARG_INDEX
        else None
    )

    results = validate_file_style(file_path, config_path)

    for _violation in results.violations[:3]:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
