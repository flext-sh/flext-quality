"""FLEXT Quality Style Validation Tool.

Comprehensive style checking and consistency validation for documentation.
Enforces style guides, formatting standards, and accessibility requirements.
"""

from __future__ import annotations

import operator
import sys
from collections.abc import MutableSequence
from pathlib import Path

from flext_quality import c, m, t, u

_STYLE_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "style_guide.yaml"
)


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

        heading_style: str
        list_style: str
        emphasis_style: str
        code_block_style: str

    class FormattingConfig(m.BaseModel):
        """Formatting configuration."""

        max_line_length: int
        trailing_spaces: bool
        consistent_indentation: bool

    class AccessibilityConfig(m.BaseModel):
        """Accessibility configuration."""

        require_alt_text: bool
        descriptive_link_text: bool

    class HeadingsConfig(m.BaseModel):
        """Headings configuration."""

        enforce_hierarchy: bool
        max_heading_level: int
        first_heading_level: int

    class CodeConfig(m.BaseModel):
        """Code fence requirements loaded from the packaged style guide."""

        require_language_specifier: bool

    class StyleConfig(m.BaseModel):
        """Complete style configuration."""

        markdown: FlextQualityStyleValidator.MarkdownConfig
        formatting: FlextQualityStyleValidator.FormattingConfig
        accessibility: FlextQualityStyleValidator.AccessibilityConfig
        headings: FlextQualityStyleValidator.HeadingsConfig
        code: FlextQualityStyleValidator.CodeConfig

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

    def __init__(self, config_path: str | None = str(_STYLE_CONFIG_PATH)) -> None:
        """Initialize style validator with configuration.

        Args:
            config_path: Path to style guide configuration file

        """
        self.settings: FlextQualityStyleValidator.StyleConfig
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
        resolved_path = Path(config_path) if config_path else _STYLE_CONFIG_PATH
        loaded_obj = u.Cli.yaml_load_mapping(resolved_path)
        self.settings = self._normalize_config(loaded_obj)

    def _normalize_config(
        self, raw: t.JsonMapping
    ) -> FlextQualityStyleValidator.StyleConfig:
        settings: FlextQualityStyleValidator.StyleConfig = (
            FlextQualityStyleValidator.StyleConfig.model_validate(raw)
        )
        return settings

    def validate_file(self, file_path: Path) -> FlextQualityStyleValidator.FileResults:
        """Validate a single documentation file."""
        read = u.Cli.files_read_text(file_path)
        if read.failure:
            return FlextQualityStyleValidator.FileResults(
                file=str(file_path),
                violations=[],
                issues=[
                    FlextQualityStyleValidator.StyleIssue(
                        type="file-read-error",
                        line=0,
                        content="",
                        message=f"Failed to read file: {read.error}",
                        severity="error",
                    )
                ],
                suggestions=[],
            )
        content = read.value
        resolved = file_path.resolve()
        try:
            filename = str(resolved.relative_to(u.Quality.project_root()))
        except ValueError:
            filename = str(resolved)

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
            self._generate_suggestions(file_results.violations)
        )

        self.results.files_checked += 1
        self.results.style_violations.extend(file_results.violations)
        self.results.accessibility_issues.extend(file_results.issues)
        self.results.suggestions.extend(file_results.suggestions)

        return file_results

    def _check_markdown_formatting(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check basic markdown formatting consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            emphasis_style = self.settings.markdown.emphasis_style
            if emphasis_style == "*" and u.Quality.compile_pattern(
                r"(?<!\\)_[^_]+_(?!\\)"
            ).search(line):
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="emphasis_style",
                        line=i,
                        content=line.strip(),
                        message="Use * for emphasis instead of _",
                        severity="low",
                    )
                )

            if line.startswith("#") and not u.Quality.compile_pattern(
                r"^#{1,6}\s"
            ).match(line):
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="heading_format",
                        line=i,
                        content=line.strip(),
                        message="Headings should have a space after #",
                        severity="medium",
                    )
                )

        return violations

    def _check_heading_consistency(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check heading hierarchy and consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        headings: t.SequenceOf[tuple[int, str, int]] = [
            (
                len(match.group(1)),
                match.group(2).strip(),
                content[: match.start()].count("\n") + 1,
            )
            for match in u.Quality.compile_pattern(
                r"^(#{1,6})\s+(.+)$", multiline=True
            ).finditer(content)
        ]

        if self.settings.headings.enforce_hierarchy:
            expected_level = self.settings.headings.first_heading_level
            for level, text, line_num in headings:
                if level > self.settings.headings.max_heading_level:
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="heading_level",
                            line=line_num,
                            content=f"{'#' * level} {text}",
                            message=f"Heading exceeds H{self.settings.headings.max_heading_level}",
                            severity="medium",
                        )
                    )
                if level > expected_level + 1:
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="heading_hierarchy",
                            line=line_num,
                            content=f"{'#' * level} {text}",
                            message=f"Heading skips level (expected H{expected_level} or H{expected_level + 1}, got H{level})",
                            severity="medium",
                        )
                    )
                expected_level = level

        if headings and headings[0][0] != self.settings.headings.first_heading_level:
            violations.append(
                FlextQualityStyleValidator.StyleIssue(
                    type="first_heading_level",
                    line=headings[0][2],
                    content=f"{'#' * headings[0][0]} {headings[0][1]}",
                    message=f"Document should start with H{self.settings.headings.first_heading_level} heading",
                    severity="low",
                )
            )

        return violations

    def _check_list_consistency(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check list formatting consistency."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        list_items: t.SequenceOf[tuple[str, str, int]] = [
            (match.group(1), match.group(2), content[: match.start()].count("\n") + 1)
            for match in u.Quality.compile_pattern(
                r"^(\s*)([-\*\+])\s+", multiline=True
            ).finditer(content)
        ]

        if not list_items:
            return violations

        markers = [item[1] for item in list_items]
        marker_map = {"dash": "-", "asterisk": "*", "plus": "+"}
        preferred = marker_map[self.settings.markdown.list_style]

        inconsistent_markers = [m for m in markers if m != preferred]
        if inconsistent_markers:
            violations.append(
                FlextQualityStyleValidator.StyleIssue(
                    type="list_marker_consistency",
                    line=list_items[0][2],
                    content=f"List using {inconsistent_markers[0]}",
                    message=f"Use {preferred} for list markers instead of mixed styles",
                    severity="low",
                )
            )

        return violations

    def _check_code_formatting(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check code block and inline code formatting."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        if (
            self.settings.markdown.code_block_style == "fenced"
            and self.settings.code.require_language_specifier
        ):
            fence_open = False
            for match in u.Quality.compile_pattern(
                r"^```([^\n]*)$", multiline=True
            ).finditer(content):
                fence_info = match.group(1).strip()
                if not fence_open and not fence_info:
                    violations.append(
                        FlextQualityStyleValidator.StyleIssue(
                            type="code_block_language",
                            line=content[: match.start()].count("\n") + 1,
                            content="```",
                            message="Code blocks should specify language (```language)",
                            severity="low",
                        )
                    )
                fence_open = not fence_open

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
                        FlextQualityStyleValidator.StyleIssue(
                            type="inline_code_spacing",
                            line=i,
                            content=line.strip(),
                            message="Add space before inline code",
                            severity="low",
                        )
                    )

        return violations

    def _check_accessibility(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check accessibility compliance."""
        issues: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        if self.settings.accessibility.require_alt_text:
            images_without_alt = u.Quality.compile_pattern(r"!\[\]\([^)]+\)").findall(
                content
            )
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
                        )
                    )

        if self.settings.accessibility.descriptive_link_text:
            generic_links = u.Quality.compile_pattern(
                r"\[(?:here|click here|link|read more)\]\([^)]+\)", ignorecase=True
            ).findall(content)
            for link in generic_links:
                line_num = content[: content.find(link)].count("\n") + 1
                issues.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="generic_link_text",
                        line=line_num,
                        content=link,
                        message="Use descriptive link text instead of generic terms",
                        severity="medium",
                    )
                )

        return issues

    def _check_line_length(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check line length compliance."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

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
                    FlextQualityStyleValidator.StyleIssue(
                        type="line_too_long",
                        line=i,
                        content=line[
                            : c.Quality.STYLE_VALIDATOR_MAX_LINE_PREVIEW_LENGTH
                        ]
                        + "..."
                        if len(line) > c.Quality.STYLE_VALIDATOR_MAX_LINE_PREVIEW_LENGTH
                        else line,
                        message=f"Line exceeds {max_length} characters ({len(line)} chars)",
                        severity="low",
                    )
                )

        return violations

    def _check_whitespace(
        self, content: str
    ) -> t.SequenceOf[FlextQualityStyleValidator.StyleIssue]:
        """Check whitespace formatting."""
        violations: MutableSequence[FlextQualityStyleValidator.StyleIssue] = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if not self.settings.formatting.trailing_spaces and line.rstrip() != line:
                violations.append(
                    FlextQualityStyleValidator.StyleIssue(
                        type="trailing_whitespace",
                        line=i,
                        content=line,
                        message="Remove trailing whitespace",
                        severity="low",
                    )
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
                        )
                    )

        return violations

    def _generate_suggestions(
        self, violations: t.SequenceOf[FlextQualityStyleValidator.StyleIssue]
    ) -> t.StrSequence:
        """Generate improvement suggestions based on violations."""
        suggestions: MutableSequence[str] = []

        violation_types: t.MutableIntMapping = {}
        for violation in violations:
            v_type = violation.type
            violation_types[v_type] = violation_types.get(v_type, 0) + 1

        if violation_types.get("emphasis_style", 0) > 0:
            suggestions.append(
                "Standardize emphasis markers (*bold* and _italic_ vs mixed usage)"
            )

        if violation_types.get("heading_hierarchy", 0) > 0:
            suggestions.append("Fix heading hierarchy to avoid skipping levels")

        if violation_types.get("list_marker_consistency", 0) > 0:
            preferred = self.settings.markdown.list_style
            suggestions.append(f"Use consistent list markers ({preferred}) throughout")

        if violation_types.get("missing_alt_text", 0) > 0:
            suggestions.append(
                "Add descriptive alt text to all images for accessibility"
            )

        if (
            violation_types.get("line_too_long", 0)
            > c.Quality.STYLE_VALIDATOR_MAX_LINE_TOO_LONG_VIOLATIONS
        ):
            suggestions.append("Consider breaking long lines or using line wrapping")

        return suggestions

    def validate_files_batch(
        self, file_paths: t.SequenceOf[Path]
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
        adapter = m.TypeAdapter(FlextQualityStyleValidator.ValidationResults)
        report_text: str = (
            adapter.dump_json(self.results, indent=2).decode()
            if output_format == "json"
            else adapter.dump_json(self.results).decode()
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
            issue_types.items(), key=operator.itemgetter(1), reverse=True
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
        file_path: str, config_path: str | None = None
    ) -> FlextQualityStyleValidator.FileResults:
        """Validate a single file."""
        validator = FlextQualityStyleValidator(config_path)
        return validator.validate_file(Path(file_path))

    @staticmethod
    def validate_files_style(
        file_paths: t.StrSequence, config_path: str | None = None
    ) -> FlextQualityStyleValidator.ValidationResults:
        """Validate multiple files."""
        validator = FlextQualityStyleValidator(config_path)
        paths = [Path(fp) for fp in file_paths]
        return validator.validate_files_batch(paths)

    @staticmethod
    def main(args: t.StrSequence | None = None) -> int:
        """Run the CLI entrypoint without exporting temporary module names."""
        command_args = list(args) if args is not None else sys.argv[1:]
        if len(command_args) < 1:
            return 1

        file_path = command_args[0]
        config_path = command_args[1] if len(command_args) > 1 else None

        results = FlextQualityStyleValidator.validate_file_style(file_path, config_path)

        return 1 if results.violations or results.issues else 0


if __name__ == "__main__":
    raise SystemExit(FlextQualityStyleValidator.main(sys.argv[1:]))
