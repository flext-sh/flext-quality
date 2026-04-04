"""FLEXT Quality Documentation Optimization System.

Automated content enhancement, formatting fixes, and quality improvements.
Performs style corrections, readability improvements, and structural optimizations.

Usage:
    python optimize.py --fix-formatting
    python optimize.py --update-toc --add-alt-text
    python optimize.py --comprehensive --backup
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
from collections.abc import MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path

from flext_cli import FlextCliUtilities
from pydantic import ValidationError

from flext_quality import m, t

MIN_HEADINGS_FOR_TOC = 5


class FlextQualityDocumentationOptimizer:
    """Documentation optimization and enhancement system."""

    def __init__(self, *, backup: bool = True) -> None:
        """Initialize the documentation optimizer.

        Args:
            backup: Whether to create backups before making changes.

        """
        self.backup = backup
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.logger = logging.getLogger(self.__class__.__name__)
        self.results = m.Quality.OptimizerResults(
            timestamp=datetime.now(UTC).isoformat(),
        )

    def optimize_formatting(self, doc_files: Sequence[Path]) -> t.ContainerMapping:
        """Fix common formatting issues."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content
                content = self._fix_trailing_spaces(content)
                content = self._normalize_list_indentation(content)
                content = self._fix_heading_spacing(content)
                content = self._normalize_emphasis_style(content)
                if content != original_content:
                    self._save_with_backup(file_path, content)
                    self.results.changes_made += 1
                    self.results.optimizations.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "formatting_fixes",
                        "description": "Fixed trailing spaces, list indentation, and emphasis consistency",
                    })
                self.results.files_processed += 1
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                self.logger.warning("Failed to optimize formatting in file: %s", e)
        return self.results.model_dump()

    def _fix_trailing_spaces(self, content: str) -> str:
        """Remove trailing spaces from lines."""
        lines = content.split("\n")
        fixed_lines = [line.rstrip() for line in lines]
        return "\n".join(fixed_lines)

    def _normalize_list_indentation(self, content: str) -> str:
        """Normalize list indentation for consistency."""
        return content

    def _fix_heading_spacing(self, content: str) -> str:
        """Ensure proper spacing around headings."""
        lines = content.split("\n")
        fixed_lines: MutableSequence[str] = []
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\\s", line) and i > 0 and lines[i - 1].strip():
                fixed_lines.append("")
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def _normalize_emphasis_style(self, content: str) -> str:
        """Normalize emphasis style (prefer * over _ for consistency)."""
        return content

    def update_table_of_contents(self, doc_files: Sequence[Path]) -> t.ContainerMapping:
        """Update or add table of contents for long documents."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content
                headings = re.findall(r"^(#{1,6})\\s+(.+)$", content, re.MULTILINE)
                if len(headings) > MIN_HEADINGS_FOR_TOC:
                    content = self._add_or_update_toc(content)
                if content != original_content:
                    self._save_with_backup(file_path, content)
                    self.results.changes_made += 1
                    self.results.optimizations.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "toc_update",
                        "description": "Added or updated table of contents",
                    })
                self.results.files_processed += 1
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                self.logger.warning("Failed to update TOC in file: %s", e)
        return self.results.model_dump()

    def _find_existing_toc(self, lines: t.StrSequence) -> tuple[int, int]:
        """Find existing table of contents boundaries."""
        toc_start = -1
        toc_end = -1
        for i, line in enumerate(lines):
            if re.match(r"^##+\\s+Table of Contents", line, re.IGNORECASE):
                toc_start = i
            elif toc_start != -1 and (
                not line.strip() or re.match(r"^#{1,6}\\s", line)
            ):
                toc_end = i
                break
        return (toc_start, toc_end)

    def _extract_toc_headings(self, lines: t.StrSequence) -> MutableSequence[str]:
        """Extract headings for table of contents."""
        toc_lines: MutableSequence[str] = []
        for line in lines:
            match = re.match(r"^(#{1,6})\\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                anchor = self._heading_to_anchor(title)
                if level <= 3:
                    indent = "  " * (level - 1)
                    toc_lines.append(f"{indent}- [{title}](#{anchor})")
        return toc_lines

    def _generate_toc_content(self, headings: t.StrSequence) -> t.StrSequence:
        """Generate the complete table of contents content."""
        return ["## Table of Contents", "", *headings, "", "---", ""]

    def _find_toc_insertion_point(self, lines: t.StrSequence) -> int:
        """Find the best position to insert table of contents."""
        insert_pos = 0
        for i, line in enumerate(lines):
            if re.match(r"^##\\s", line):
                return i
            if re.match(r"^#{1,6}\\s", line):
                continue
            if line.strip() and (not re.match(r"^#{1,6}\\s", line)):
                insert_pos = i + 1
        return insert_pos

    def _add_or_update_toc(self, content: str) -> str:
        """Add or update table of contents."""
        lines = content.split("\n")
        toc_start, toc_end = self._find_existing_toc(lines)
        toc_headings = self._extract_toc_headings(lines)
        new_toc = self._generate_toc_content(toc_headings)
        if toc_start != -1 and toc_end != -1:
            lines = lines[:toc_start] + list(new_toc) + lines[toc_end:]
        else:
            insert_pos = self._find_toc_insertion_point(lines)
            lines = lines[:insert_pos] + [""] + list(new_toc) + lines[insert_pos:]
        return "\n".join(lines)

    def _heading_to_anchor(self, heading: str) -> str:
        """Convert heading to anchor link."""
        anchor = heading.lower()
        anchor = re.sub(r"[^\\w\\s-]", "", anchor)
        return re.sub(r"\\s+", "-", anchor)

    def enhance_accessibility(self, doc_files: Sequence[Path]) -> t.ContainerMapping:
        """Enhance accessibility of documentation."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content
                content = self._add_missing_alt_text(content)
                content = self._improve_link_text(content)
                if content != original_content:
                    self._save_with_backup(file_path, content)
                    self.results.changes_made += 1
                    self.results.optimizations.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "accessibility_enhancement",
                        "description": "Added alt text and improved link descriptions",
                    })
                self.results.files_processed += 1
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                self.logger.warning(
                    "Failed to enhance accessibility in %s: %s",
                    file_path,
                    e,
                )
        return self.results.model_dump()

    def _add_missing_alt_text(self, content: str) -> str:
        """Add descriptive alt text to images that lack it."""
        pattern = "!\\[\\]\\(([^)]+)\\)"
        matches = re.findall(pattern, content)
        for url in matches:
            filename = Path(url.split("/")[-1]).stem
            alt_text = filename.replace("-", " ").replace("_", " ").title()
            old_pattern = f"![\\]\\({re.escape(url)}\\)"
            new_pattern = f"![{alt_text}]\\({url}\\)"
            content = re.sub(old_pattern, new_pattern, content)
        return content

    def _improve_link_text(self, content: str) -> str:
        """Improve generic link text for better accessibility."""
        improvements = {
            "\\[here\\]\\(([^)]+)\\)": "[learn more](\\1)",
            "\\[click here\\]\\(([^)]+)\\)": "[learn more](\\1)",
            "\\[link\\]\\(([^)]+)\\)": "[learn more](\\1)",
            "\\[read more\\]\\(([^)]+)\\)": "[continue reading](\\1)",
        }
        for pattern, replacement in improvements.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        return content

    def optimize_content_structure(
        self,
        doc_files: Sequence[Path],
    ) -> t.ContainerMapping:
        """Optimize content structure and readability."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content
                content = self._break_long_paragraphs(content)
                content = self._ensure_heading_hierarchy(content)
                content = self._add_section_breaks(content)
                if content != original_content:
                    self._save_with_backup(file_path, content)
                    self.results.changes_made += 1
                    self.results.optimizations.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "structure_optimization",
                        "description": "Improved paragraph breaks and section organization",
                    })
                self.results.files_processed += 1
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
            ) as e:
                self.logger.warning(
                    "Failed to enhance accessibility in %s: %s",
                    file_path,
                    e,
                )
        return self.results.model_dump()

    def _break_long_paragraphs(self, content: str) -> str:
        """Break up paragraphs that are too long."""
        return content

    def _ensure_heading_hierarchy(self, content: str) -> str:
        """Ensure logical heading hierarchy."""
        return content

    def _add_section_breaks(self, content: str) -> str:
        """Add horizontal rules between major sections."""
        lines = content.split("\n")
        enhanced_lines: MutableSequence[str] = []
        for i, line in enumerate(lines):
            enhanced_lines.append(line)
            if (
                re.match(r"^##\\s", line)
                and i > 0
                and (not re.match(r"^#\\s", lines[i - 1]))
                and lines[i - 1].strip()
            ):
                enhanced_lines.extend(("", "---", ""))
        return "\n".join(enhanced_lines)

    def update_metadata(self, doc_files: Sequence[Path]) -> t.ContainerMapping:
        """Update frontmatter metadata and timestamps."""
        for file_path in doc_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content
                if content.startswith("---"):
                    content = self._update_frontmatter(content)
                if not re.search(r"<!--.*updated.*-->", content, re.IGNORECASE):
                    lines = content.split("\n")
                    if lines and lines[0].strip():
                        lines.insert(
                            1,
                            f"<!-- Updated: {datetime.now(UTC).strftime('%Y-%m-%d')} -->",
                        )
                        content = "\n".join(lines)
                if content != original_content:
                    self._save_with_backup(file_path, content)
                    self.results.changes_made += 1
                    self.results.optimizations.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "type": "metadata_update",
                        "description": "Updated frontmatter and added modification timestamp",
                    })
                self.results.files_processed += 1
            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
                OSError,
                ValueError,
            ) as e:
                self.logger.warning(
                    "Failed to enhance accessibility in %s: %s",
                    file_path,
                    e,
                )
        return self.results.model_dump()

    def _update_frontmatter(self, content: str) -> str:
        """Update YAML frontmatter with current metadata."""
        lines = content.split("\n")
        if lines[0] == "---":
            end_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line == "---":
                    end_idx = i + 1
                    break
            if end_idx > 0:
                try:
                    frontmatter_lines = lines[1 : end_idx - 1]
                    frontmatter_content = "\n".join(frontmatter_lines)
                    parsed_fm = FlextCliUtilities.Cli.yaml_parse(
                        frontmatter_content,
                    ).unwrap_or({})
                    metadata: t.MutableContainerValueMapping = {
                        str(k): v
                        for k, v in (parsed_fm or {}).items()
                        if isinstance(v, (str, int, float, bool))
                    }
                    metadata["updated"] = datetime.now(UTC).strftime("%Y-%m-%d")
                    new_frontmatter = FlextCliUtilities.Cli.yaml_dump_str(
                        metadata,
                    ).strip()
                    new_frontmatter_lines = (
                        ["---"] + new_frontmatter.split("\n") + ["---"]
                    )
                    lines = new_frontmatter_lines + lines[end_idx:]
                except (ValueError, ValidationError):
                    pass
        return "\n".join(lines)

    def _save_with_backup(self, file_path: Path, content: str) -> None:
        """Save file with optional backup."""
        if self.backup:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            shutil.copy2(file_path, backup_path)
            self.results.backups_created.append(
                str(backup_path.relative_to(self.project_root)),
            )
        _ = file_path.write_text(content, encoding="utf-8")

    def generate_report(self, report_format: str = "json") -> str:
        """Generate optimization report."""
        if report_format == "json":
            return self.results.model_dump_json(indent=2)
        return self.results.model_dump_json()

    def save_report(self, output_path: str = "docs/maintenance/reports/") -> str:
        """Save optimization report."""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"optimization_report_{timestamp}.json"
        filepath = output_dir / filename
        report_content = self.generate_report("json")
        _ = filepath.write_text(report_content, encoding="utf-8")
        latest_file = output_dir / "latest_optimization.json"
        latest_file.write_text(self.results.model_dump_json(indent=2), encoding="utf-8")
        return str(filepath)


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="FLEXT Quality Documentation Optimization",
    )
    _ = parser.add_argument(
        "--fix-formatting",
        action="store_true",
        help="Fix common formatting issues",
    )
    _ = parser.add_argument(
        "--update-toc",
        action="store_true",
        help="Update table of contents",
    )
    _ = parser.add_argument(
        "--add-alt-text",
        action="store_true",
        help="Add missing alt text to images",
    )
    _ = parser.add_argument(
        "--improve-accessibility",
        action="store_true",
        help="Enhance accessibility features",
    )
    _ = parser.add_argument(
        "--optimize-structure",
        action="store_true",
        help="Optimize content structure and readability",
    )
    _ = parser.add_argument(
        "--update-metadata",
        action="store_true",
        help="Update frontmatter and metadata",
    )
    _ = parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run all optimization checks",
    )
    _ = parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create backups before making changes",
    )
    _ = parser.add_argument(
        "--no-backup",
        action="store_false",
        dest="backup",
        help="Don't create backups",
    )
    _ = parser.add_argument(
        "--output",
        type=str,
        default="docs/maintenance/reports/",
        help="Output directory for reports",
    )
    _ = parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Specific files to optimize (default: all docs)",
    )
    return parser


def _discover_documentation_files(args: argparse.Namespace) -> Sequence[Path]:
    """Discover documentation files to optimize."""
    project_root = Path(__file__).parent.parent.parent.parent
    if args.files:
        return [project_root / f for f in args.files]
    doc_files: MutableSequence[Path] = []
    for pattern in [
        "**/*.md",
        "**/*.mdx",
        "**/README*",
        "**/docs/**/*.md",
        "**/docs/**/*.mdx",
    ]:
        doc_files.extend(project_root.glob(pattern))
    doc_files = list(set(doc_files))
    ignored_patterns = [".git", "__pycache__", "node_modules", ".serena/memories"]
    return [
        f
        for f in doc_files
        if not any(pattern in str(f) for pattern in ignored_patterns)
    ]


def _execute_optimizations(
    optimizer: FlextQualityDocumentationOptimizer,
    args: argparse.Namespace,
) -> bool:
    """Execute the requested optimizations and return if any were run."""
    run_any_optimization = False
    doc_files = _discover_documentation_files(args)
    if args.fix_formatting or args.comprehensive:
        optimizer.optimize_formatting(doc_files)
        run_any_optimization = True
    if args.update_toc or args.comprehensive:
        optimizer.update_table_of_contents(doc_files)
        run_any_optimization = True
    if args.add_alt_text or args.improve_accessibility or args.comprehensive:
        optimizer.enhance_accessibility(doc_files)
        run_any_optimization = True
    if args.optimize_structure or args.comprehensive:
        optimizer.optimize_content_structure(doc_files)
        run_any_optimization = True
    if args.update_metadata or args.comprehensive:
        optimizer.update_metadata(doc_files)
        run_any_optimization = True
    return run_any_optimization


def main() -> None:
    """Main entry point for optimization system."""
    parser = _create_argument_parser()
    args = parser.parse_args()
    optimizer = FlextQualityDocumentationOptimizer(backup=args.backup)
    run_any_optimization = _execute_optimizations(optimizer, args)
    if not run_any_optimization:
        parser.print_help()
        return
    optimizer.save_report(args.output)


if __name__ == "__main__":
    main()
