# VERIFIED_NEW_MODULE
# LEGACY_PROFILE - docs_maintenance profile following existing patterns
"""Markdown Structure Validation Profile.

AST-based markdown validation for structure, headers, and cross-references.
Uses FlextQualityMarkdownParser for accurate structural analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar, TypedDict

from flext_core import FlextResult

from flext_quality.constants import c
from flext_quality.docs_maintenance.utils import get_docs_dir
from flext_quality.tools.markdown_tools import (
    FlextQualityMarkdownParser,
)

logger = logging.getLogger(__name__)


class FlextQualityMarkdownValidation:
    """Facade for markdown validation types and operations.

    Provides centralized access to all markdown validation
    components following FLEXT facade pattern.
    """

    class ValidationIssue(TypedDict):
        """Information about a markdown validation issue."""

        file: str
        line: int
        severity: str
        message: str
        rule: str

    class ValidationSummary(TypedDict):
        """Summary of markdown validation results."""

        total_files: int
        files_with_issues: int
        total_issues: int
        issues_by_severity: dict[str, int]
        pass_rate: float

    @dataclass
    class ValidationResult:
        """Result of markdown validation for a single file."""

        file_path: str
        is_valid: bool
        issues: list[FlextQualityMarkdownValidation.ValidationIssue]
        headers_count: int
        links_count: int
        code_blocks_count: int
        validated_at: str

    @dataclass
    class ValidationReport:
        """Complete markdown validation report."""

        summary: FlextQualityMarkdownValidation.ValidationSummary
        results: list[FlextQualityMarkdownValidation.ValidationResult]
        generated_at: str
        docs_directory: str

    class Validator:
        """Full markdown validation using AST.

        Validates:
        - Header hierarchy (no skipping levels)
        - Single H1 rule
        - Broken anchor links
        - Empty headers
        - Code block language specification
        """

        RULE_SINGLE_H1: ClassVar[str] = "single-h1"
        RULE_HEADER_HIERARCHY: ClassVar[str] = "header-hierarchy"
        RULE_NO_EMPTY_HEADERS: ClassVar[str] = "no-empty-headers"
        RULE_VALID_ANCHORS: ClassVar[str] = "valid-anchors"
        RULE_CODE_BLOCK_LANG: ClassVar[str] = "code-block-language"
        RULE_BROKEN_LINK: ClassVar[str] = "broken-internal-link"
        RULE_GENERAL: ClassVar[str] = "general"

        def __init__(self, docs_dir: Path | None = None) -> None:
            """Initialize markdown validator.

            Args:
                docs_dir: Documentation directory (defaults to project docs/)

            """
            self._docs_dir = docs_dir or get_docs_dir()
            self._parser = FlextQualityMarkdownParser()

        def validate_structure(
            self,
            path: Path,
        ) -> FlextResult[FlextQualityMarkdownValidation.ValidationResult]:
            """Validate markdown structure for a single file.

            Args:
                path: Path to markdown file

            Returns:
                FlextResult with validation result

            """
            try:
                if not path.exists():
                    return FlextResult.fail(f"File not found: {path}")

                content = path.read_text(encoding="utf-8")
                issues: list[FlextQualityMarkdownValidation.ValidationIssue] = []

                # Validate structure using parser
                structure_result = self._parser.validate_structure(content)
                if structure_result.is_failure:
                    return FlextResult.fail(structure_result.error)

                for issue_msg in structure_result.value:
                    # Parse issue message to extract line number
                    line_num = 0
                    if issue_msg.startswith("Line "):
                        parts = issue_msg.split(":", 1)
                        line_str = parts[0].replace("Line ", "").strip()
                        line_num = int(line_str) if line_str.isdigit() else 0

                    severity = "error" if "broken" in issue_msg.lower() else "warning"
                    rule = self._determine_rule(issue_msg)

                    issues.append(FlextQualityMarkdownValidation.ValidationIssue(
                        file=str(path),
                        line=line_num,
                        severity=severity,
                        message=issue_msg,
                        rule=rule,
                    ))

                # Count elements
                headers_result = self._parser.extract_headers(content)
                links_result = self._parser.extract_links(content)
                code_blocks_result = self._parser.extract_code_blocks(content)

                headers_count = (
                    len(headers_result.value) if headers_result.is_success else 0
                )
                links_count = len(links_result.value) if links_result.is_success else 0
                code_blocks_count = (
                    len(code_blocks_result.value) if code_blocks_result.is_success else 0
                )

                # Additional validation: code blocks without language
                if code_blocks_result.is_success:
                    issues.extend(
                        FlextQualityMarkdownValidation.ValidationIssue(
                            file=str(path),
                            line=0,
                            severity="info",
                            message="Code block without language specification",
                            rule=self.RULE_CODE_BLOCK_LANG,
                        )
                        for block in code_blocks_result.value
                        if block.get("language") == "text"
                    )

                return FlextResult.ok(FlextQualityMarkdownValidation.ValidationResult(
                    file_path=str(path),
                    is_valid=len([i for i in issues if i["severity"] == "error"]) == 0,
                    issues=issues,
                    headers_count=headers_count,
                    links_count=links_count,
                    code_blocks_count=code_blocks_count,
                    validated_at=datetime.now(UTC).isoformat(),
                ))

            except Exception as e:
                return FlextResult.fail(f"Validation failed: {e}")

        def validate_code_blocks(
            self,
            path: Path,
        ) -> FlextResult[list[FlextQualityMarkdownValidation.ValidationIssue]]:
            """Validate code blocks in a markdown file.

            Args:
                path: Path to markdown file

            Returns:
                FlextResult with list of code block issues

            """
            try:
                content = path.read_text(encoding="utf-8")
                code_blocks_result = self._parser.extract_code_blocks(content)

                if code_blocks_result.is_failure:
                    return FlextResult.fail(code_blocks_result.error)

                issues: list[FlextQualityMarkdownValidation.ValidationIssue] = []
                for block in code_blocks_result.value:
                    lang = str(block.get("language", ""))
                    if lang == "text" or not lang:
                        issues.append(FlextQualityMarkdownValidation.ValidationIssue(
                            file=str(path),
                            line=0,
                            severity="info",
                            message="Code block without language specification",
                            rule=self.RULE_CODE_BLOCK_LANG,
                        ))

                return FlextResult.ok(issues)

            except Exception as e:
                return FlextResult.fail(f"Code block validation failed: {e}")

        def validate_cross_references(
            self,
            path: Path,
        ) -> FlextResult[list[FlextQualityMarkdownValidation.ValidationIssue]]:
            """Validate internal cross-references in a markdown file.

            Args:
                path: Path to markdown file

            Returns:
                FlextResult with list of cross-reference issues

            """
            try:
                content = path.read_text(encoding="utf-8")
                links_result = self._parser.extract_links(content)

                if links_result.is_failure:
                    return FlextResult.fail(links_result.error)

                issues: list[FlextQualityMarkdownValidation.ValidationIssue] = []
                for link in links_result.value:
                    if link["type"] == "internal":
                        target_url = str(link["url"]).split("#")[0]
                        target_path = (path.parent / target_url).resolve()
                        if not target_path.exists():
                            # Narrow line type from GeneralValueType to int
                            line_num = link["line"]
                            if not isinstance(line_num, int):
                                line_num = 0
                            issues.append(FlextQualityMarkdownValidation.ValidationIssue(
                                file=str(path),
                                line=line_num,
                                severity="error",
                                message=f"Broken internal link: {link['url']}",
                                rule=self.RULE_BROKEN_LINK,
                            ))

                return FlextResult.ok(issues)

            except Exception as e:
                return FlextResult.fail(f"Cross-reference validation failed: {e}")

        def validate_directory(
            self,
            directory: Path | None = None,
            *,
            pattern: str = c.Quality.Markdown.DEFAULT_GLOB_PATTERN,
        ) -> FlextResult[FlextQualityMarkdownValidation.ValidationReport]:
            """Validate all markdown files in a directory.

            Args:
                directory: Directory to validate (defaults to docs_dir)
                pattern: Glob pattern for markdown files

            Returns:
                FlextResult with complete validation report

            """
            try:
                target_dir = directory or self._docs_dir
                if not target_dir.exists():
                    return FlextResult.fail(f"Directory not found: {target_dir}")

                md_files = list(target_dir.glob(pattern))
                results: list[FlextQualityMarkdownValidation.ValidationResult] = []
                issues_by_severity: dict[str, int] = {
                    "error": 0,
                    "warning": 0,
                    "info": 0,
                }
                files_with_issues = 0
                total_issues = 0

                for md_file in md_files:
                    result = self.validate_structure(md_file)
                    if result.is_success:
                        file_result = result.value
                        results.append(file_result)
                        if file_result.issues:
                            files_with_issues += 1
                            total_issues += len(file_result.issues)
                            for issue in file_result.issues:
                                severity = issue["severity"]
                                issues_by_severity[severity] = (
                                    issues_by_severity.get(severity, 0) + 1
                                )

                pass_rate = (
                    ((len(md_files) - files_with_issues) / len(md_files) * 100)
                    if md_files
                    else 100.0
                )

                summary = FlextQualityMarkdownValidation.ValidationSummary(
                    total_files=len(md_files),
                    files_with_issues=files_with_issues,
                    total_issues=total_issues,
                    issues_by_severity=issues_by_severity,
                    pass_rate=pass_rate,
                )

                return FlextResult.ok(FlextQualityMarkdownValidation.ValidationReport(
                    summary=summary,
                    results=results,
                    generated_at=datetime.now(UTC).isoformat(),
                    docs_directory=str(target_dir),
                ))

            except Exception as e:
                return FlextResult.fail(f"Directory validation failed: {e}")

        def _determine_rule(self, message: str) -> str:
            """Determine validation rule from issue message.

            Args:
                message: Issue message

            Returns:
                Rule identifier string

            """
            message_lower = message.lower()
            if "h1" in message_lower:
                return self.RULE_SINGLE_H1
            if "hierarchy" in message_lower:
                return self.RULE_HEADER_HIERARCHY
            if "empty" in message_lower:
                return self.RULE_NO_EMPTY_HEADERS
            if "anchor" in message_lower or "broken" in message_lower:
                return self.RULE_VALID_ANCHORS
            return self.RULE_GENERAL

    class CLI:
        """CLI operations for markdown validation."""

        @staticmethod
        def run(args: argparse.Namespace) -> int:
            """Run markdown validation from CLI args.

            Args:
                args: Parsed command line arguments

            Returns:
                Exit code (0 for success)

            """
            target = Path(args.path)
            validator = FlextQualityMarkdownValidation.Validator()

            if target.is_file():
                file_result = validator.validate_structure(target)
                if file_result.is_success:
                    data = file_result.value
                    if args.format == "json":
                        logger.info(json.dumps(asdict(data), indent=2))  # DEBUG
                    else:
                        status = "Valid" if data.is_valid else "Invalid"
                        logger.info(f"{data.file_path}: {status}")  # DEBUG
                        for issue in data.issues:
                            if not args.quiet or issue["severity"] == "error":
                                logger.info(  # DEBUG
                                    f"  [{issue['severity']}] "
                                    f"Line {issue['line']}: {issue['message']}",
                                )
                    return 0
                logger.error(f"Error: {file_result.error}")  # DEBUG
                return 1

            result: FlextResult[FlextQualityMarkdownValidation.ValidationReport] = (
                validator.validate_directory(target)
            )
            if result.is_success:
                report = result.value
                if args.format == "json":
                    logger.info(json.dumps(asdict(report), indent=2))  # DEBUG
                else:
                    logger.info("=== Markdown Validation Report ===")  # DEBUG
                    logger.info(f"Directory: {report.docs_directory}")  # DEBUG
                    logger.info(  # DEBUG
                        f"Files validated: {report.summary['total_files']}",
                    )
                    logger.info(  # DEBUG
                        f"Files with issues: {report.summary['files_with_issues']}",
                    )
                    logger.info(  # DEBUG
                        f"Pass rate: {report.summary['pass_rate']:.1f}%",
                    )
                    logger.info("Issues by severity:")  # DEBUG
                    for sev, count in report.summary["issues_by_severity"].items():
                        logger.info(f"  {sev}: {count}")  # DEBUG
                return 0

            logger.error(f"Error: {result.error}")  # DEBUG
            return 1

        @staticmethod
        def create_parser() -> argparse.ArgumentParser:
            """Create argument parser for CLI.

            Returns:
                Configured ArgumentParser

            """
            parser = argparse.ArgumentParser(
                description="Validate markdown structure using AST analysis",
            )
            parser.add_argument(
                "path",
                nargs="?",
                default=".",
                help="File or directory to validate",
            )
            parser.add_argument(
                "--format",
                choices=["json", "text"],
                default="text",
                help="Output format",
            )
            parser.add_argument(
                "--quiet",
                action="store_true",
                help="Only show errors",
            )
            return parser
