"""FLEXT Quality Style Validation Tool.

Comprehensive style checking and consistency validation for documentation.
Enforces style guides, formatting standards, and accessibility requirements.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import operator
import sys
from collections.abc import MutableSequence
from pathlib import Path

from flext_quality import FlextQualityConfigManager, c, m, t, u


class FlextQualityStyleValidator:
    """Documentation style validation and consistency checking system."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        """Initialize style validation from declared, validated configuration."""
        self.settings: m.Quality.StyleGuideConfig = FlextQualityConfigManager(
            config_dir,
        ).resolve_style_guide()
        self.results: m.Quality.StyleValidationResults = (
            m.Quality.StyleValidationResults(
                files_checked=0,
                style_violations=[],
                accessibility_issues=[],
                formatting_errors=[],
                suggestions=[],
                summary=m.Quality.StyleSummaryMetrics(
                    total_violations=0,
                    critical_issues=0,
                    warnings=0,
                    suggestions_count=0,
                    accessibility_issues=0,
                ),
            )
        )

    def validate_file(self, file_path: Path) -> m.Quality.StyleFileResults:
        """Validate a single documentation file.

        Returns:
            The resulting ``m.Quality.StyleFileResults``.
        """
        content = u.Cli.files_read_text(file_path).value
        filename = str(file_path)

        violations_list: MutableSequence[m.Quality.StyleIssue] = []
        issues_list: MutableSequence[m.Quality.StyleIssue] = []
        suggestions_list: MutableSequence[str] = []
        file_results = m.Quality.StyleFileResults(
            file=filename,
            violations=violations_list,
            issues=issues_list,
            suggestions=suggestions_list,
        )

        file_results.violations.extend(self._check_markdown_formatting(content))
        file_results.violations.extend(self._check_heading_consistency(content))
        file_results.violations.extend(self._check_list_consistency(content))
        file_results.violations.extend(self._check_code_formatting(content))
        file_results.issues.extend(self._check_accessibility(content))
        file_results.violations.extend(self._check_line_length(content))
        file_results.violations.extend(self._check_whitespace(content))

        file_results.suggestions = list(
            self._generate_suggestions(file_results.violations),
        )

        self.results.files_checked += 1
        self.results.style_violations.extend(file_results.violations)
        self.results.accessibility_issues.extend(file_results.issues)
        self.results.suggestions.extend(file_results.suggestions)

        return file_results

    def _check_markdown_formatting(
        self,
        content: str,
    ) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check basic markdown formatting consistency.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            emphasis_style = self.settings.markdown.emphasis_style
            if emphasis_style == "*" and u.Quality.compile_pattern(
                r"(?<!\\)_[^_]+_(?!\\)",
            ).search(line):
                violations.append(
                    m.Quality.StyleIssue(
                        type="emphasis_style",
                        line=i,
                        content=line.strip(),
                        message="Use * for emphasis instead of _",
                        severity="low",
                    ),
                )

            if (
                self.settings.headings.require_space_after_hash
                and line.startswith("#")
                and not u.Quality.compile_pattern(r"^#{1,6}\s").match(line)
            ):
                violations.append(
                    m.Quality.StyleIssue(
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
    ) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check heading hierarchy and consistency.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        headings: t.SequenceOf[tuple[int, str, int]] = [
            (
                len(match.group(1)),
                match.group(2).strip(),
                content[: match.start()].count("\n") + 1,
            )
            for match in u.Quality.compile_pattern(
                r"^(#{1,6})\s+(.+)$",
                multiline=True,
            ).finditer(content)
        ]

        if self.settings.headings.enforce_hierarchy:
            expected_level = 1
            for level, text, line_num in headings:
                if level > expected_level + 1:
                    violations.append(
                        m.Quality.StyleIssue(
                            type="heading_hierarchy",
                            line=line_num,
                            content=f"{'#' * level} {text}",
                            message=(
                                f"Heading skips level (expected H{expected_level} "
                                f"or H{expected_level + 1}, got H{level})"
                            ),
                            severity="medium",
                        ),
                    )
                expected_level = level

        if headings and headings[0][0] != self.settings.headings.first_heading_level:
            violations.append(
                m.Quality.StyleIssue(
                    type="first_heading_level",
                    line=headings[0][2],
                    content=f"{'#' * headings[0][0]} {headings[0][1]}",
                    message=(
                        f"Document should start with "
                        f"H{self.settings.headings.first_heading_level} heading"
                    ),
                    severity="low",
                ),
            )

        return violations

    def _check_list_consistency(
        self,
        content: str,
    ) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check list formatting consistency.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        list_items: t.SequenceOf[tuple[str, str, int]] = [
            (match.group(1), match.group(2), content[: match.start()].count("\n") + 1)
            for match in u.Quality.compile_pattern(
                r"^(\s*)([-\*\+])\s+",
                multiline=True,
            ).finditer(content)
        ]

        if not list_items:
            return violations

        markers = [item[1] for item in list_items]
        preferred_marker = self.settings.markdown.list_style

        marker_map = {"dash": "-", "asterisk": "*", "plus": "+"}
        preferred = marker_map[preferred_marker]

        inconsistent_markers = [m for m in markers if m != preferred]
        if inconsistent_markers:
            violations.append(
                m.Quality.StyleIssue(
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
    ) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check code block and inline code formatting.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        code_block_style = self.settings.markdown.code_block_style
        if (
            code_block_style == "fenced"
            and self.settings.code.require_language_specifier
        ):
            code_blocks = u.Quality.compile_pattern(
                r"```\n(.*?)\n```",
                dotall=True,
            ).findall(content)
            violations.extend(
                m.Quality.StyleIssue(
                    type="code_block_language",
                    line=content[: content.find(block)].count("\n") + 1,
                    content="```" + block[:50] + "...",
                    message="Code blocks should specify language (```language)",
                    severity="low",
                )
                for block in code_blocks
                if not u.Quality.compile_pattern(r"```\w+").match(
                    content[content.find(block) - 10 : content.find(block)],
                )
            )

        inline_code = u.Quality.compile_pattern(r"`[^`]+`").findall(content)
        if inline_code:
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if (
                    "`" in line
                    and u.Quality.compile_pattern(r"[a-zA-Z0-9]`[^`]+`").search(line)
                    and not u.Quality.compile_pattern(r"\s`[^`]+`").search(line)
                ):
                    violations.append(
                        m.Quality.StyleIssue(
                            type="inline_code_spacing",
                            line=i,
                            content=line.strip(),
                            message="Add space before inline code",
                            severity="low",
                        ),
                    )

        return violations

    def _check_accessibility(self, content: str) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check accessibility compliance.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        issues: MutableSequence[m.Quality.StyleIssue] = []

        if self.settings.accessibility.require_alt_text:
            images_without_alt = u.Quality.compile_pattern(r"!\[\]\([^)]+\)").findall(
                content,
            )
            if images_without_alt:
                for img in images_without_alt:
                    line_num = content[: content.find(img)].count("\n") + 1
                    issues.append(
                        m.Quality.StyleIssue(
                            type="missing_alt_text",
                            line=line_num,
                            content=img,
                            message="Images must have descriptive alt text",
                            severity="high",
                        ),
                    )

        if self.settings.accessibility.descriptive_link_text:
            generic_links = u.Quality.compile_pattern(
                r"\[here|click here|link|read more\]\([^)]+\)",
                ignorecase=True,
            ).findall(content)
            for link in generic_links:
                line_num = content[: content.find(link)].count("\n") + 1
                issues.append(
                    m.Quality.StyleIssue(
                        type="generic_link_text",
                        line=line_num,
                        content=link,
                        message="Use descriptive link text instead of generic terms",
                        severity="medium",
                    ),
                )

        return issues

    def _check_line_length(self, content: str) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check line length compliance.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        max_length = self.settings.formatting.max_line_length
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if len(line) > max_length and not (
                line.strip().startswith(("```", "|", "http", "https"))
                or "|" in line
                or line.count("`")
                >= c.Quality.STYLE_VALIDATOR_MIN_INLINE_CODE_BACKTICKS
            ):
                violations.append(
                    m.Quality.StyleIssue(
                        type="line_too_long",
                        line=i,
                        content=line[
                            : c.Quality.STYLE_VALIDATOR_MAX_LINE_PREVIEW_LENGTH
                        ]
                        + "..."
                        if len(line) > c.Quality.STYLE_VALIDATOR_MAX_LINE_PREVIEW_LENGTH
                        else line,
                        message=(
                            f"Line exceeds {max_length} characters ({len(line)} chars)"
                        ),
                        severity="low",
                    ),
                )

        return violations

    def _check_whitespace(self, content: str) -> t.SequenceOf[m.Quality.StyleIssue]:
        """Check whitespace formatting.

        Returns:
            The resulting ``t.SequenceOf[m.Quality.StyleIssue]``.
        """
        violations: MutableSequence[m.Quality.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if not self.settings.formatting.trailing_spaces and line.rstrip() != line:
                violations.append(
                    m.Quality.StyleIssue(
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
                        m.Quality.StyleIssue(
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
        violations: t.SequenceOf[m.Quality.StyleIssue],
    ) -> t.StrSequence:
        """Generate improvement suggestions based on violations.

        Returns:
            The resulting ``t.StrSequence``.
        """
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
            preferred = self.settings.markdown.list_style
            suggestions.append(f"Use consistent list markers ({preferred}) throughout")

        if violation_types.get("missing_alt_text", 0) > 0:
            suggestions.append(
                "Add descriptive alt text to all images for accessibility",
            )

        if (
            violation_types.get("line_too_long", 0)
            > c.Quality.STYLE_VALIDATOR_MAX_LINE_TOO_LONG_VIOLATIONS
        ):
            suggestions.append("Consider breaking long lines or using line wrapping")

        return suggestions

    def validate_files_batch(
        self,
        file_paths: t.SequenceOf[Path],
    ) -> m.Quality.StyleValidationResults:
        """Validate multiple files and aggregate results.

        Returns:
            The resulting ``m.Quality.StyleValidationResults``.
        """
        for file_path in file_paths:
            self.validate_file(file_path)

        style_violations = self.results.style_violations
        accessibility_issues = self.results.accessibility_issues
        suggestions = self.results.suggestions

        self.results.summary.total_violations = len(style_violations)
        self.results.summary.accessibility_issues = len(accessibility_issues)
        self.results.summary.suggestions_count = len(suggestions)

        all_violations: MutableSequence[m.Quality.StyleIssue] = []
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
        """Generate style validation report.

        Returns:
            The resulting ``str``.

        Raises:
            ValueError: If Unsupported report format.
        """
        if output_format == "summary":
            return self._generate_summary_report()
        if output_format == "json":
            return self.results.model_dump_json(indent=2)
        msg = f"Unsupported report format: {output_format}"
        raise ValueError(msg)

    def _generate_summary_report(self) -> str:
        """Generate human-readable summary.

        Returns:
            The resulting ``str``.
        """
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

    @staticmethod
    def validate_file_style(
        file_path: str,
        config_dir: str | None = None,
    ) -> m.Quality.StyleFileResults:
        """Validate a single file.

        Returns:
            The resulting ``m.Quality.StyleFileResults``.
        """
        validator = FlextQualityStyleValidator(config_dir)
        return validator.validate_file(Path(file_path))

    @staticmethod
    def validate_files_style(
        file_paths: t.StrSequence,
        config_dir: str | None = None,
    ) -> m.Quality.StyleValidationResults:
        """Validate multiple files.

        Returns:
            The resulting ``m.Quality.StyleValidationResults``.
        """
        validator = FlextQualityStyleValidator(config_dir)
        paths = [Path(fp) for fp in file_paths]
        return validator.validate_files_batch(paths)

    @staticmethod
    def main() -> int:
        """Run the CLI entrypoint without exporting temporary module names.

        Returns:
            The resulting ``int``.
        """
        if len(sys.argv) < c.Quality.STYLE_VALIDATOR_MIN_COMMAND_LINE_ARGS:
            return 1

        file_path = sys.argv[1]
        config_dir = (
            sys.argv[c.Quality.STYLE_VALIDATOR_CONFIG_ARG_INDEX]
            if len(sys.argv) > c.Quality.STYLE_VALIDATOR_CONFIG_ARG_INDEX
            else None
        )

        results = FlextQualityStyleValidator.validate_file_style(file_path, config_dir)
        sys.stdout.write(results.model_dump_json(indent=2) + "\n")
        return int(bool(results.violations or results.issues))


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).


if __name__ == "__main__":
    raise SystemExit(FlextQualityStyleValidator.main())

__all__: list[str] = ["FlextQualityStyleValidator"]
