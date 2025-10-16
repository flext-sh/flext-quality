#!/usr/bin/env python3
"""FLEXT Quality Style Validation Tool.

Comprehensive style checking and consistency validation for documentation.
Enforces style guides, formatting standards, and accessibility requirements.
"""

import json
import operator
import re
from datetime import UTC, datetime
from pathlib import Path

import yaml
from flext_core import FlextTypes


class StyleValidator:
    """Documentation style validation and consistency checking system."""

    # Constants for magic numbers
    MIN_INLINE_CODE_BACKTICKS: int = 2
    MAX_LINE_PREVIEW_LENGTH: int = 50
    MAX_LINE_TOO_LONG_VIOLATIONS: int = 5
    MIN_COMMAND_LINE_ARGS: int = 2
    CONFIG_ARG_INDEX: int = 2

    def __init__(
        self, config_path: str = "docs/maintenance/config/style_guide.yaml"
    ) -> None:
        self.load_config(config_path)
        self.results = {
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
            },
        }

    def load_config(self, config_path: str) -> None:
        """Load style guide configuration."""
        try:
            with Path(config_path).open(encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except (FileNotFoundError, KeyError):
            # Default configuration
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

    def validate_file(self, file_path: Path) -> dict[str, object]:
        """Validate a single documentation file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = str(
                file_path.relative_to(file_path.parents[2])
            )  # Relative to project root

            file_results = {
                "file": filename,
                "violations": [],
                "issues": [],
                "suggestions": [],
            }

            # Run all validation checks
            file_results["violations"].extend(self._check_markdown_formatting(content))
            file_results["violations"].extend(self._check_heading_consistency(content))
            file_results["violations"].extend(self._check_list_consistency(content))
            file_results["violations"].extend(self._check_code_formatting(content))
            file_results["issues"].extend(self._check_accessibility(content))
            file_results["violations"].extend(self._check_line_length(content))
            file_results["violations"].extend(self._check_whitespace(content))

            # Generate suggestions
            file_results["suggestions"] = self._generate_suggestions(
                file_results["violations"]
            )

            # Add to global results
            self.results["files_checked"] += 1
            self.results["style_violations"].extend(file_results["violations"])
            self.results["accessibility_issues"].extend(file_results["issues"])
            self.results["suggestions"].extend(file_results["suggestions"])

            return file_results

        except Exception as e:
            return {
                "file": str(file_path),
                "error": str(e),
                "violations": [],
                "issues": [],
                "suggestions": [],
            }

    def _check_markdown_formatting(self, content: str) -> list[dict[str, object]]:
        """Check basic markdown formatting consistency."""
        violations = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for mixed emphasis styles
            if self.config["markdown"]["emphasis_style"] == "*" and re.search(
                r"(?<!\\)_[^_]+_(?!\\)", line
            ):
                # Should not have _emphasis_ if * is preferred
                violations.append({
                    "type": "emphasis_style",
                    "line": i,
                    "content": line.strip(),
                    "message": "Use * for emphasis instead of _",
                    "severity": "low",
                })

            # Check heading formatting
            if line.startswith("#") and not re.match(r"^#{1,6}\s", line):
                violations.append({
                    "type": "heading_format",
                    "line": i,
                    "content": line.strip(),
                    "message": "Headings should have a space after #",
                    "severity": "medium",
                })

        return violations

    def _check_heading_consistency(self, content: str) -> list[dict[str, object]]:
        """Check heading hierarchy and consistency."""
        violations = []

        # Extract headings
        headings = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            line_num = content[: match.start()].count("\n") + 1
            headings.append((level, text, line_num))

        # Check hierarchy
        if self.config.get("headings", {}).get("enforce_hierarchy", True):
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

        # Check for H1 as first heading
        if headings and headings[0][0] != 1:
            violations.append({
                "type": "first_heading_level",
                "line": headings[0][2],
                "content": f"{'#' * headings[0][0]} {headings[0][1]}",
                "message": "Document should start with H1 heading",
                "severity": "low",
            })

        return violations

    def _check_list_consistency(self, content: str) -> list[dict[str, object]]:
        """Check list formatting consistency."""
        violations = []

        # Find all list items
        list_items = []
        for match in re.finditer(r"^(\s*)([-\*\+])\s+", content, re.MULTILINE):
            indent = match.group(1)
            marker = match.group(2)
            line_num = content[: match.start()].count("\n") + 1
            list_items.append((indent, marker, line_num))

        if not list_items:
            return violations

        # Check for consistent markers
        markers = [item[1] for item in list_items]
        preferred_marker = self.config["markdown"]["list_style"]

        marker_map = {"dash": "-", "asterisk": "*", "plus": "+"}
        preferred = marker_map.get(preferred_marker, "-")

        inconsistent_markers = [m for m in markers if m != preferred]
        if inconsistent_markers:
            violations.append({
                "type": "list_marker_consistency",
                "line": list_items[0][2],  # First occurrence
                "content": f"List using {inconsistent_markers[0]}",
                "message": f"Use {preferred} for list markers instead of mixed styles",
                "severity": "low",
            })

        return violations

    def _check_code_formatting(self, content: str) -> list[dict[str, object]]:
        """Check code block and inline code formatting."""
        violations = []

        # Check fenced code blocks
        if self.config["markdown"]["code_block_style"] == "fenced":
            # Find code blocks without language specifiers
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
                    r"```\w+", content[content.find(block) - 10 : content.find(block)]
                )
            )

        # Check inline code formatting
        inline_code = re.findall(r"`[^`]+`", content)
        if inline_code:
            # Check for proper spacing around inline code
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                # Find inline code in this line
                if (
                    "`" in line
                    and re.search(r"[a-zA-Z0-9]`[^`]+`", line)  # Letter before code
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

    def _check_accessibility(self, content: str) -> list[dict[str, object]]:
        """Check accessibility compliance."""
        issues = []

        # Check images for alt text
        if self.config["accessibility"]["require_alt_text"]:
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

        # Check for generic link text
        if self.config["accessibility"]["descriptive_links"]:
            generic_links = re.findall(
                r"\[here|click here|link|read more\]\([^)]+\)", content, re.IGNORECASE
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

    def _check_line_length(self, content: str) -> list[dict[str, object]]:
        """Check line length compliance."""
        violations = []

        max_length = self.config["formatting"]["max_line_length"]
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if (
                len(line) > max_length
                and not (
                    line.strip().startswith(("```", "|", "http", "https"))
                    or "|" in line  # Table rows
                    or line.count("`") >= self.MIN_INLINE_CODE_BACKTICKS
                )  # Code spans
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

    def _check_whitespace(self, content: str) -> list[dict[str, object]]:
        """Check whitespace formatting."""
        violations = []

        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check trailing spaces
            if (
                self.config["formatting"]["trailing_spaces"] is False
                and line.rstrip() != line
            ):
                violations.append({
                    "type": "trailing_whitespace",
                    "line": i,
                    "content": line,
                    "message": "Remove trailing whitespace",
                    "severity": "low",
                })

            # Check multiple consecutive blank lines
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

    def _generate_suggestions(self, violations: list[dict]) -> FlextTypes.StringList:
        """Generate improvement suggestions based on violations."""
        suggestions = []

        violation_types = {}
        for violation in violations:
            v_type = violation["type"]
            violation_types[v_type] = violation_types.get(v_type, 0) + 1

        # Generate suggestions based on violation patterns
        if violation_types.get("emphasis_style", 0) > 0:
            suggestions.append(
                "Standardize emphasis markers (*bold* and _italic_ vs mixed usage)"
            )

        if violation_types.get("heading_hierarchy", 0) > 0:
            suggestions.append("Fix heading hierarchy to avoid skipping levels")

        if violation_types.get("list_marker_consistency", 0) > 0:
            preferred = self.config["markdown"]["list_style"]
            suggestions.append(f"Use consistent list markers ({preferred}) throughout")

        if violation_types.get("missing_alt_text", 0) > 0:
            suggestions.append(
                "Add descriptive alt text to all images for accessibility"
            )

        if violation_types.get("line_too_long", 0) > self.MAX_LINE_TOO_LONG_VIOLATIONS:
            suggestions.append("Consider breaking long lines or using line wrapping")

        return suggestions

    def validate_files_batch(self, file_paths: list[Path]) -> dict[str, object]:
        """Validate multiple files and aggregate results."""
        for file_path in file_paths:
            self.validate_file(file_path)

        # Update summary
        self.results["summary"]["total_violations"] = len(
            self.results["style_violations"]
        )
        self.results["summary"]["accessibility_issues"] = len(
            self.results["accessibility_issues"]
        )
        self.results["summary"]["suggestions_count"] = len(self.results["suggestions"])

        # Count severity levels
        for violation in (
            self.results["style_violations"] + self.results["accessibility_issues"]
        ):
            severity = violation.get("severity", "low")
            if severity == "critical":
                self.results["summary"]["critical_issues"] += 1
            elif severity == "high":
                self.results["summary"]["warnings"] += 1

        return self.results

    def generate_report(self, output_format: str = "json") -> str:
        """Generate style validation report."""
        if output_format == "json":
            return json.dumps(self.results, indent=2, default=str)
        if output_format == "summary":
            return self._generate_summary_report()
        return json.dumps(self.results, default=str)

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
        issue_types = {}
        for violation in (
            self.results["style_violations"] + self.results["accessibility_issues"]
        ):
            v_type = violation["type"]
            issue_types[v_type] = issue_types.get(v_type, 0) + 1

        # Show top 5 issues
        sorted_issues = sorted(
            issue_types.items(), key=operator.itemgetter(1), reverse=True
        )
        for issue_type, count in sorted_issues[:5]:
            report += f"- {issue_type.replace('_', ' ').title()}: {count}\n"

        if self.results["suggestions"]:
            report += "\nSuggestions:\n"
            for suggestion in self.results["suggestions"][:3]:
                report += f"- {suggestion}\n"

        return report

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> None:
        """Save style validation report."""
        Path(output_path).mkdir(exist_ok=True, parents=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"style_validation_{timestamp}.json"
        filepath = Path(output_path) / filename

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)

        return filepath


def validate_file_style(
    file_path: str, config_path: str | None = None
) -> dict[str, object]:
    """Convenience function to validate a single file."""
    validator = StyleValidator(config_path)
    return validator.validate_file(Path(file_path))


def validate_files_style(
    file_paths: FlextTypes.StringList, config_path: str | None = None
) -> dict[str, object]:
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
