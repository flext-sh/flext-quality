# VERIFIED_NEW_MODULE
# LEGACY_PROFILE - docs_maintenance profile following existing patterns
"""Markdown Auto-Formatting Profile.

Auto-format markdown files to FLEXT standards using mdformat.
Provides dry-run, backup, and batch formatting capabilities.

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
from typing import TypedDict

from flext_core import FlextResult

from flext_quality.constants import c
from flext_quality.docs_maintenance.utils import get_docs_dir
from flext_quality.tools.markdown_tools import (
    FlextQualityMarkdownFormatter,
)

logger = logging.getLogger(__name__)


class FlextQualityMarkdownFormatting:
    """Facade for markdown formatting types and operations.

    Provides centralized access to all markdown formatting
    components following FLEXT facade pattern.
    """

    class FormatResult(TypedDict):
        """Result of formatting a single file."""

        path: str
        modified: bool
        message: str
        original_lines: int
        formatted_lines: int

    class FormatSummary(TypedDict):
        """Summary of formatting operation."""

        total_files: int
        modified: int
        unchanged: int
        errors: int
        dry_run: bool

    @dataclass
    class FormatReport:
        """Complete formatting report."""

        summary: FlextQualityMarkdownFormatting.FormatSummary
        results: list[FlextQualityMarkdownFormatting.FormatResult]
        errors: list[dict[str, str]]
        generated_at: str
        docs_directory: str

    class Formatter:
        """Auto-format markdown files to FLEXT standard.

        Features:
        - Consistent line wrapping (88 chars)
        - Standardized heading spacing
        - List formatting normalization
        - Code block alignment
        """

        def __init__(self, docs_dir: Path | None = None) -> None:
            """Initialize markdown formatter.

            Args:
                docs_dir: Documentation directory (defaults to project docs/)

            """
            self._docs_dir = docs_dir or get_docs_dir()
            self._formatter = FlextQualityMarkdownFormatter()

        def format_file(
            self,
            path: Path,
            *,
            dry_run: bool = False,
            wrap_width: int = c.Quality.Markdown.DEFAULT_WRAP_WIDTH,  # CONFIG
        ) -> FlextResult[FlextQualityMarkdownFormatting.FormatResult]:
            """Format a single markdown file.

            Args:
                path: Path to markdown file
                dry_run: If True, preview without modifying
                wrap_width: Line wrap width

            Returns:
                FlextResult with formatting result

            """
            result = self._formatter.format_file(
                path,
                dry_run=dry_run,
                wrap_width=wrap_width,
            )

            if result.is_failure:
                return FlextResult.fail(result.error)

            data = result.value
            return FlextResult.ok(FlextQualityMarkdownFormatting.FormatResult(
                path=str(data.get("path", path)),
                modified=bool(data.get("modified", False)),
                message=str(data.get("message", "")),
                original_lines=int(data.get("original_lines", 0)),
                formatted_lines=int(data.get("formatted_lines", 0)),
            ))

        def format_directory(
            self,
            directory: Path | None = None,
            *,
            dry_run: bool = False,
            wrap_width: int = c.Quality.Markdown.DEFAULT_WRAP_WIDTH,  # CONFIG
            pattern: str = c.Quality.Markdown.DEFAULT_GLOB_PATTERN,
        ) -> FlextResult[FlextQualityMarkdownFormatting.FormatReport]:
            """Format all markdown files in a directory.

            Args:
                directory: Directory to format (defaults to docs_dir)
                dry_run: If True, preview without modifying
                wrap_width: Line wrap width
                pattern: Glob pattern for markdown files

            Returns:
                FlextResult with complete formatting report

            """
            try:
                target_dir = directory or self._docs_dir
                if not target_dir.exists():
                    return FlextResult.fail(f"Directory not found: {target_dir}")

                md_files = list(target_dir.glob(pattern))
                results: list[FlextQualityMarkdownFormatting.FormatResult] = []
                errors: list[dict[str, str]] = []
                modified_count = 0
                unchanged_count = 0

                for md_file in md_files:
                    result = self.format_file(
                        md_file,
                        dry_run=dry_run,
                        wrap_width=wrap_width,
                    )
                    if result.is_success:
                        file_result = result.value
                        results.append(file_result)
                        if file_result["modified"]:
                            modified_count += 1
                        else:
                            unchanged_count += 1
                    else:
                        errors.append({
                            "path": str(md_file),
                            "error": result.error,
                        })

                summary = FlextQualityMarkdownFormatting.FormatSummary(
                    total_files=len(md_files),
                    modified=modified_count,
                    unchanged=unchanged_count,
                    errors=len(errors),
                    dry_run=dry_run,
                )

                return FlextResult.ok(FlextQualityMarkdownFormatting.FormatReport(
                    summary=summary,
                    results=results,
                    errors=errors,
                    generated_at=datetime.now(UTC).isoformat(),
                    docs_directory=str(target_dir),
                ))

            except Exception as e:
                return FlextResult.fail(f"Directory formatting failed: {e}")

    class CLI:
        """CLI operations for markdown formatting."""

        @staticmethod
        def run(args: argparse.Namespace) -> int:
            """Run markdown formatting from CLI args.

            Args:
                args: Parsed command line arguments

            Returns:
                Exit code (0 for success)

            """
            target = Path(args.path)
            formatter = FlextQualityMarkdownFormatting.Formatter()

            if target.is_file():
                result = formatter.format_file(target, dry_run=args.dry_run)
                if result.is_success:
                    data = result.value
                    if args.format == "json":
                        logger.info(json.dumps(data, indent=2))  # DEBUG
                    else:
                        status = "modified" if data["modified"] else "unchanged"
                        mode = "(dry-run)" if args.dry_run else ""
                        logger.info(f"{data['path']}: {status} {mode}")  # DEBUG
                    return 0
                logger.error(f"Error: {result.error}")  # DEBUG
                return 1

            result = formatter.format_directory(target, dry_run=args.dry_run)
            if result.is_success:
                report = result.value
                if args.format == "json":
                    logger.info(json.dumps(asdict(report), indent=2))  # DEBUG
                else:
                    mode = "(DRY-RUN)" if report.summary["dry_run"] else ""
                    logger.info(f"=== Markdown Formatting Report {mode} ===")  # DEBUG
                    logger.info(f"Directory: {report.docs_directory}")  # DEBUG
                    logger.info(  # DEBUG
                        f"Total files: {report.summary['total_files']}",
                    )
                    logger.info(f"Modified: {report.summary['modified']}")  # DEBUG
                    logger.info(f"Unchanged: {report.summary['unchanged']}")  # DEBUG
                    if report.errors:
                        logger.info(f"Errors: {report.summary['errors']}")  # DEBUG
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
                description="Auto-format markdown files to FLEXT standards",
            )
            parser.add_argument(
                "path",
                nargs="?",
                default=".",
                help="File or directory to format",
            )
            parser.add_argument(
                "--dry-run",
                action="store_true",
                help="Preview changes without modifying files",
            )
            parser.add_argument(
                "--format",
                choices=["json", "text"],
                default="text",
                help="Output format",
            )
            return parser
