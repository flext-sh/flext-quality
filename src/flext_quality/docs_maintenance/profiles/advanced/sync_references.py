# VERIFIED_NEW_MODULE
# LEGACY_PROFILE - docs_maintenance profile following existing patterns
"""Cross-Reference Synchronization Profile.

Synchronize and manage cross-references between documentation files.
Handles TOC updates, link fixes, and reference graph management.

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
    FlextQualityCrossReferenceManager,
    FlextQualityMarkdownParser,
)

logger = logging.getLogger(__name__)


class FlextQualityCrossReferenceSync:
    """Facade for cross-reference synchronization types and operations.

    Provides centralized access to all cross-reference sync
    components following FLEXT facade pattern.
    """

    class ReferenceUpdate(TypedDict):
        """Information about a reference update."""

        file: str
        old_ref: str
        new_ref: str
        line: int
        status: str

    class TocEntry(TypedDict):
        """Table of contents entry."""

        text: str
        anchor: str
        level: int
        line: int

    class SyncSummary(TypedDict):
        """Summary of synchronization operation."""

        total_files: int
        files_updated: int
        references_fixed: int
        toc_updates: int
        errors: int

    @dataclass
    class SyncResult:
        """Result of a single file synchronization."""

        file_path: str
        toc_updated: bool
        references_updated: int
        errors: list[str]
        synced_at: str

    @dataclass
    class SyncReport:
        """Complete synchronization report."""

        summary: FlextQualityCrossReferenceSync.SyncSummary
        results: list[FlextQualityCrossReferenceSync.SyncResult]
        reference_updates: list[FlextQualityCrossReferenceSync.ReferenceUpdate]
        generated_at: str
        docs_directory: str

    class Synchronizer:
        """Synchronize cross-references between documentation files.

        Features:
        - TOC synchronization with headers
        - Internal link validation and fixing
        - Reference graph management
        - Batch synchronization
        """

        def __init__(self, docs_dir: Path | None = None) -> None:
            """Initialize reference synchronizer.

            Args:
                docs_dir: Documentation directory (defaults to project docs/)

            """
            self._docs_dir = docs_dir or get_docs_dir()
            self._parser = FlextQualityMarkdownParser()
            self._ref_manager = FlextQualityCrossReferenceManager()

        def sync_toc(
            self,
            path: Path,
            *,
            dry_run: bool = False,
        ) -> FlextResult[FlextQualityCrossReferenceSync.SyncResult]:
            """Synchronize table of contents with actual headers.

            Args:
                path: Path to markdown file
                dry_run: If True, preview without modifying

            Returns:
                FlextResult with synchronization result

            """
            try:
                if not path.exists():
                    return FlextResult.fail(f"File not found: {path}")

                content = path.read_text(encoding="utf-8")
                errors: list[str] = []
                toc_updated = False

                # Extract headers
                headers_result = self._parser.extract_headers(content)
                if headers_result.is_failure:
                    return FlextResult.fail(headers_result.error)

                headers = headers_result.value

                # Generate TOC from headers
                toc_entries = self._generate_toc_entries(headers)

                # Find existing TOC section
                toc_start, toc_end = self._find_toc_section(content)

                if toc_start >= 0 and toc_end > toc_start:
                    # Generate new TOC content
                    new_toc = self._format_toc(toc_entries)

                    # Replace TOC section
                    lines = content.split("\n")
                    new_content = (
                        "\n".join(lines[:toc_start])
                        + "\n"
                        + new_toc
                        + "\n"
                        + "\n".join(lines[toc_end:])
                    )

                    if new_content != content:
                        toc_updated = True
                        if not dry_run:
                            path.write_text(new_content, encoding="utf-8")

                return FlextResult.ok(FlextQualityCrossReferenceSync.SyncResult(
                    file_path=str(path),
                    toc_updated=toc_updated,
                    references_updated=0,
                    errors=errors,
                    synced_at=datetime.now(UTC).isoformat(),
                ))

            except Exception as e:
                return FlextResult.fail(f"TOC sync failed: {e}")

        def sync_references(
            self,
            path: Path,
            *,
            dry_run: bool = False,
        ) -> FlextResult[FlextQualityCrossReferenceSync.SyncResult]:
            """Synchronize internal references in a markdown file.

            Args:
                path: Path to markdown file
                dry_run: If True, preview without modifying

            Returns:
                FlextResult with synchronization result

            """
            try:
                if not path.exists():
                    return FlextResult.fail(f"File not found: {path}")

                content = path.read_text(encoding="utf-8")
                errors: list[str] = []
                references_updated = 0

                # Extract links
                links_result = self._parser.extract_links(content)
                if links_result.is_failure:
                    return FlextResult.fail(links_result.error)

                # Check each internal link
                new_content = content
                for link in links_result.value:
                    if link["type"] == "internal":
                        target_url = str(link["url"]).split("#")[0]
                        if target_url:
                            target_path = (path.parent / target_url).resolve()
                            if not target_path.exists():
                                # Try to find the file
                                fixed_path = self._find_moved_file(
                                    target_url, path.parent,
                                )
                                if fixed_path:
                                    old_ref = str(link["url"])
                                    new_ref = str(
                                        fixed_path.relative_to(path.parent),
                                    )
                                    new_content = new_content.replace(
                                        f"]({old_ref})",
                                        f"]({new_ref})",
                                    )
                                    references_updated += 1
                                else:
                                    errors.append(
                                        f"Broken link: {link['url']} (line {link['line']})",
                                    )

                if new_content != content and not dry_run:
                    path.write_text(new_content, encoding="utf-8")

                return FlextResult.ok(FlextQualityCrossReferenceSync.SyncResult(
                    file_path=str(path),
                    toc_updated=False,
                    references_updated=references_updated,
                    errors=errors,
                    synced_at=datetime.now(UTC).isoformat(),
                ))

            except Exception as e:
                return FlextResult.fail(f"Reference sync failed: {e}")

        def sync_directory(
            self,
            directory: Path | None = None,
            *,
            dry_run: bool = False,
            pattern: str = c.Quality.Markdown.DEFAULT_GLOB_PATTERN,
        ) -> FlextResult[FlextQualityCrossReferenceSync.SyncReport]:
            """Synchronize all markdown files in a directory.

            Args:
                directory: Directory to sync (defaults to docs_dir)
                dry_run: If True, preview without modifying
                pattern: Glob pattern for markdown files

            Returns:
                FlextResult with complete sync report

            """
            try:
                target_dir = directory or self._docs_dir
                if not target_dir.exists():
                    return FlextResult.fail(f"Directory not found: {target_dir}")

                md_files = list(target_dir.glob(pattern))
                results: list[FlextQualityCrossReferenceSync.SyncResult] = []
                reference_updates: list[
                    FlextQualityCrossReferenceSync.ReferenceUpdate
                ] = []
                files_updated = 0
                total_refs_fixed = 0
                total_toc_updates = 0
                error_count = 0

                for md_file in md_files:
                    # Sync TOC
                    toc_result = self.sync_toc(md_file, dry_run=dry_run)
                    if toc_result.is_success and toc_result.value.toc_updated:
                        total_toc_updates += 1

                    # Sync references
                    ref_result = self.sync_references(md_file, dry_run=dry_run)
                    if ref_result.is_success:
                        file_result = ref_result.value
                        results.append(file_result)
                        total_refs_fixed += file_result.references_updated
                        if (
                            file_result.references_updated > 0
                            or (toc_result.is_success and toc_result.value.toc_updated)
                        ):
                            files_updated += 1
                        if file_result.errors:
                            error_count += len(file_result.errors)
                    else:
                        error_count += 1

                summary = FlextQualityCrossReferenceSync.SyncSummary(
                    total_files=len(md_files),
                    files_updated=files_updated,
                    references_fixed=total_refs_fixed,
                    toc_updates=total_toc_updates,
                    errors=error_count,
                )

                return FlextResult.ok(FlextQualityCrossReferenceSync.SyncReport(
                    summary=summary,
                    results=results,
                    reference_updates=reference_updates,
                    generated_at=datetime.now(UTC).isoformat(),
                    docs_directory=str(target_dir),
                ))

            except Exception as e:
                return FlextResult.fail(f"Directory sync failed: {e}")

        def _generate_toc_entries(
            self,
            headers: list[dict[str, str | int]],
        ) -> list[FlextQualityCrossReferenceSync.TocEntry]:
            """Generate TOC entries from headers.

            Args:
                headers: List of header dictionaries

            Returns:
                List of TOC entries

            """
            entries: list[FlextQualityCrossReferenceSync.TocEntry] = []
            for header in headers:
                level = int(header.get("level", 1))
                if level > 1:  # Skip H1 (document title)
                    text = str(header.get("text", ""))
                    anchor = self._text_to_anchor(text)
                    entries.append(FlextQualityCrossReferenceSync.TocEntry(
                        text=text,
                        anchor=anchor,
                        level=level,
                        line=int(header.get("line", 0)),
                    ))
            return entries

        def _text_to_anchor(self, text: str) -> str:
            """Convert header text to anchor link.

            Args:
                text: Header text

            Returns:
                Anchor-compatible string

            """
            anchor = text.lower().replace(" ", "-")
            return "".join(c for c in anchor if c.isalnum() or c == "-")

        def _find_toc_section(self, content: str) -> tuple[int, int]:
            """Find TOC section boundaries in content.

            Args:
                content: File content

            Returns:
                Tuple of (start_line, end_line) or (-1, -1) if not found

            """
            lines = content.split("\n")
            toc_start = -1
            toc_end = -1

            for i, line in enumerate(lines):
                lower_line = line.lower().strip()
                if toc_start < 0:
                    if lower_line in {
                        "## table of contents",
                        "## contents",
                        "## toc",
                        "<!-- toc -->",
                    }:
                        toc_start = i
                elif lower_line.startswith("## ") or lower_line == "<!-- /toc -->":
                    toc_end = i
                    break

            if toc_start >= 0 and toc_end < 0:
                # TOC goes to end of file or next section
                for i in range(toc_start + 1, len(lines)):
                    if lines[i].strip().startswith("## "):
                        toc_end = i
                        break
                if toc_end < 0:
                    toc_end = len(lines)

            return toc_start, toc_end

        def _format_toc(
            self,
            entries: list[FlextQualityCrossReferenceSync.TocEntry],
        ) -> str:
            """Format TOC entries as markdown.

            Args:
                entries: TOC entries

            Returns:
                Formatted TOC string

            """
            lines = ["## Table of Contents", ""]
            for entry in entries:
                indent = "  " * (entry["level"] - 2)  # H2 = no indent
                lines.append(f"{indent}- [{entry['text']}](#{entry['anchor']})")
            return "\n".join(lines)

        def _find_moved_file(
            self,
            original_ref: str,
            search_dir: Path,
        ) -> Path | None:
            """Try to find a file that may have been moved.

            Args:
                original_ref: Original reference path
                search_dir: Directory to search in

            Returns:
                New path if found, None otherwise

            """
            filename = Path(original_ref).name
            # Search in current directory and subdirectories
            matches = list(search_dir.glob(f"**/{filename}"))
            if len(matches) == 1:
                return matches[0]
            return None

    class CLI:
        """CLI operations for cross-reference synchronization."""

        @staticmethod
        def run(args: argparse.Namespace) -> int:
            """Run cross-reference sync from CLI args.

            Args:
                args: Parsed command line arguments

            Returns:
                Exit code (0 for success)

            """
            target = Path(args.path)
            synchronizer = FlextQualityCrossReferenceSync.Synchronizer()

            if target.is_file():
                if args.toc_only:
                    result = synchronizer.sync_toc(target, dry_run=args.dry_run)
                elif args.refs_only:
                    result = synchronizer.sync_references(
                        target, dry_run=args.dry_run,
                    )
                else:
                    # Sync both
                    toc_result = synchronizer.sync_toc(target, dry_run=args.dry_run)
                    ref_result = synchronizer.sync_references(
                        target, dry_run=args.dry_run,
                    )
                    if toc_result.is_success and ref_result.is_success:
                        result = ref_result
                    else:
                        result = toc_result if toc_result.is_failure else ref_result

                if result.is_success:
                    data = result.value
                    if args.format == "json":
                        logger.info(json.dumps(asdict(data), indent=2))  # DEBUG
                    else:
                        mode = "(dry-run)" if args.dry_run else ""
                        logger.info(f"{data.file_path}: synced {mode}")  # DEBUG
                        if data.toc_updated:
                            logger.info("  TOC: updated")  # DEBUG
                        if data.references_updated > 0:
                            logger.info(  # DEBUG
                                f"  References fixed: {data.references_updated}",
                            )
                        for error in data.errors:
                            logger.warning(f"  Warning: {error}")  # DEBUG
                    return 0
                logger.error(f"Error: {result.error}")  # DEBUG
                return 1

            result = synchronizer.sync_directory(target, dry_run=args.dry_run)
            if result.is_success:
                report = result.value
                if args.format == "json":
                    logger.info(json.dumps(asdict(report), indent=2))  # DEBUG
                else:
                    mode = "(DRY-RUN)" if args.dry_run else ""
                    logger.info(  # DEBUG
                        f"=== Cross-Reference Sync Report {mode} ===",
                    )
                    logger.info(f"Directory: {report.docs_directory}")  # DEBUG
                    logger.info(  # DEBUG
                        f"Total files: {report.summary['total_files']}",
                    )
                    logger.info(  # DEBUG
                        f"Files updated: {report.summary['files_updated']}",
                    )
                    logger.info(  # DEBUG
                        f"TOC updates: {report.summary['toc_updates']}",
                    )
                    logger.info(  # DEBUG
                        f"References fixed: {report.summary['references_fixed']}",
                    )
                    if report.summary["errors"] > 0:
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
                description="Synchronize cross-references in markdown files",
            )
            parser.add_argument(
                "path",
                nargs="?",
                default=".",
                help="File or directory to sync",
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
            parser.add_argument(
                "--toc-only",
                action="store_true",
                help="Only sync table of contents",
            )
            parser.add_argument(
                "--refs-only",
                action="store_true",
                help="Only sync cross-references",
            )
            return parser
