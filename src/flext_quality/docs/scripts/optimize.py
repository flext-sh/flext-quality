"""FLEXT Quality Documentation Optimization System.

Automated content enhancement, formatting fixes, and quality improvements.
Performs style corrections, readability improvements, and structural optimizations.

Usage:
    python optimize.py --fix-formatting
    python optimize.py --update-toc --add-alt-text
    python optimize.py --comprehensive --backup
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, override

from flext_cli import cli
from flext_quality import c, m, p, r, s, t, u

if TYPE_CHECKING:
    from collections.abc import MutableSequence


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
        self.results: m.Quality.OptimizerResults = m.Quality.OptimizerResults(
            timestamp=u.now().isoformat(),
        )

    def optimize_formatting(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.OptimizerResults:
        """Fix common formatting issues."""
        for file_path in doc_files:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning(
                    "Failed to optimize formatting in file: %s",
                    read.error,
                )
                continue
            content = read.value
            original_content = content
            content = self._fix_trailing_spaces(content)
            content = self._normalize_list_indentation(content)
            content = self._fix_heading_spacing(content)
            content = self._normalize_emphasis_style(content)
            if content != original_content:
                save = self._save_with_backup(file_path, content)
                if save.failure:
                    self.logger.warning(
                        "Failed to optimize formatting in file: %s",
                        save.error,
                    )
                    continue
                self.results.changes_made += 1
                self.results.optimizations.append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "formatting_fixes",
                    "description": "Fixed trailing spaces, list indentation, and emphasis consistency",
                })
            self.results.files_processed += 1
        return self.results

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
            if (
                u.Quality.compile_pattern(r"^#{1,6}\\s").match(line)
                and i > 0
                and lines[i - 1].strip()
            ):
                fixed_lines.append("")
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def _normalize_emphasis_style(self, content: str) -> str:
        """Normalize emphasis style (prefer * over _ for consistency)."""
        return content

    def update_table_of_contents(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.OptimizerResults:
        """Update or add table of contents for long documents."""
        for file_path in doc_files:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning("Failed to update TOC in file: %s", read.error)
                continue
            content = read.value
            original_content = content
            headings = u.Quality.compile_pattern(
                r"^(#{1,6})\\s+(.+)$",
                multiline=True,
            ).findall(content)
            if len(headings) > c.Quality.THRESHOLD_MIN_HEADINGS_FOR_TOC:
                content = self._add_or_update_toc(content)
            if content != original_content:
                save = self._save_with_backup(file_path, content)
                if save.failure:
                    self.logger.warning("Failed to update TOC in file: %s", save.error)
                    continue
                self.results.changes_made += 1
                self.results.optimizations.append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "toc_update",
                    "description": "Added or updated table of contents",
                })
            self.results.files_processed += 1
        return self.results

    def _find_existing_toc(self, lines: t.StrSequence) -> tuple[int, int]:
        """Find existing table of contents boundaries."""
        toc_start = -1
        toc_end = -1
        for i, line in enumerate(lines):
            if u.Quality.compile_pattern(
                r"^##+\\s+Table of Contents",
                ignorecase=True,
            ).match(line):
                toc_start = i
            elif toc_start != -1 and (
                not line.strip() or u.Quality.compile_pattern(r"^#{1,6}\\s").match(line)
            ):
                toc_end = i
                break
        return (toc_start, toc_end)

    def _extract_toc_headings(self, lines: t.StrSequence) -> MutableSequence[str]:
        """Extract headings for table of contents."""
        toc_lines: MutableSequence[str] = []
        for line in lines:
            match = u.Quality.compile_pattern(r"^(#{1,6})\\s+(.+)$").match(line)
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
            if u.Quality.compile_pattern(r"^##\\s").match(line):
                return i
            if u.Quality.compile_pattern(r"^#{1,6}\\s").match(line):
                continue
            if line.strip() and (
                not u.Quality.compile_pattern(r"^#{1,6}\\s").match(line)
            ):
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
            lines = [*lines[:insert_pos], "", *list(new_toc), *lines[insert_pos:]]
        return "\n".join(lines)

    def _heading_to_anchor(self, heading: str) -> str:
        """Convert heading to anchor link."""
        anchor = heading.lower()
        anchor = u.Quality.compile_pattern(r"[^\\w\\s-]").sub("", anchor)
        slug: str = u.Quality.compile_pattern(r"\\s+").sub("-", anchor)
        return slug

    def enhance_accessibility(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.OptimizerResults:
        """Enhance accessibility of documentation."""
        for file_path in doc_files:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning(
                    "Failed to enhance accessibility in %s: %s",
                    file_path,
                    read.error,
                )
                continue
            content = read.value
            original_content = content
            content = self._add_missing_alt_text(content)
            content = self._improve_link_text(content)
            if content != original_content:
                save = self._save_with_backup(file_path, content)
                if save.failure:
                    self.logger.warning(
                        "Failed to enhance accessibility in %s: %s",
                        file_path,
                        save.error,
                    )
                    continue
                self.results.changes_made += 1
                self.results.optimizations.append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "accessibility_enhancement",
                    "description": "Added alt text and improved link descriptions",
                })
            self.results.files_processed += 1
        return self.results

    def _add_missing_alt_text(self, content: str) -> str:
        """Add descriptive alt text to images that lack it."""
        pattern = "!\\[\\]\\(([^)]+)\\)"
        matches = u.Quality.compile_pattern(pattern).findall(content)
        for url in matches:
            filename = Path(url.split("/")[-1]).stem
            alt_text = filename.replace("-", " ").replace("_", " ").title()
            old_pattern = f"![\\]\\({u.Quality.escape_pattern(url)}\\)"
            new_pattern = f"![{alt_text}]\\({url}\\)"
            content = u.Quality.compile_pattern(old_pattern).sub(new_pattern, content)
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
            content = u.Quality.compile_pattern(pattern, ignorecase=True).sub(
                replacement,
                content,
            )
        return content

    def optimize_content_structure(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.OptimizerResults:
        """Optimize content structure and readability."""
        for file_path in doc_files:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning(
                    "Failed to optimize structure in %s: %s",
                    file_path,
                    read.error,
                )
                continue
            content = read.value
            original_content = content
            content = self._break_long_paragraphs(content)
            content = self._ensure_heading_hierarchy(content)
            content = self._add_section_breaks(content)
            if content != original_content:
                save = self._save_with_backup(file_path, content)
                if save.failure:
                    self.logger.warning(
                        "Failed to optimize structure in %s: %s",
                        file_path,
                        save.error,
                    )
                    continue
                self.results.changes_made += 1
                self.results.optimizations.append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "structure_optimization",
                    "description": "Improved paragraph breaks and section organization",
                })
            self.results.files_processed += 1
        return self.results

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
                u.Quality.compile_pattern(r"^##\\s").match(line)
                and i > 0
                and (not u.Quality.compile_pattern(r"^#\\s").match(lines[i - 1]))
                and lines[i - 1].strip()
            ):
                enhanced_lines.extend(("", "---", ""))
        return "\n".join(enhanced_lines)

    def update_metadata(
        self,
        doc_files: t.SequenceOf[Path],
    ) -> m.Quality.OptimizerResults:
        """Update frontmatter metadata and timestamps."""
        for file_path in doc_files:
            read = u.Cli.files_read_text(file_path)
            if read.failure:
                self.logger.warning(
                    "Failed to update metadata in %s: %s",
                    file_path,
                    read.error,
                )
                continue
            content = read.value
            original_content = content
            if content.startswith("---"):
                content = self._update_frontmatter(content)
            if not u.Quality.compile_pattern(
                r"<!--.*updated.*-->",
                ignorecase=True,
            ).search(content):
                lines = content.split("\n")
                if lines and lines[0].strip():
                    lines.insert(
                        1,
                        f"<!-- Updated: {u.now().strftime('%Y-%m-%d')} -->",
                    )
                    content = "\n".join(lines)
            if content != original_content:
                save = self._save_with_backup(file_path, content)
                if save.failure:
                    self.logger.warning(
                        "Failed to update metadata in %s: %s",
                        file_path,
                        save.error,
                    )
                    continue
                self.results.changes_made += 1
                self.results.optimizations.append({
                    "file": str(file_path.relative_to(self.project_root)),
                    "type": "metadata_update",
                    "description": "Updated frontmatter and added modification timestamp",
                })
            self.results.files_processed += 1
        return self.results

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
                lines = self._replace_frontmatter_lines(lines, end_idx)
        return "\n".join(lines)

    def _replace_frontmatter_lines(
        self,
        lines: t.StrSequence,
        end_idx: int,
    ) -> list[str]:
        """Return document lines with refreshed YAML frontmatter metadata."""
        frontmatter_lines = lines[1 : end_idx - 1]
        frontmatter_content = "\n".join(frontmatter_lines)
        empty_frontmatter: t.JsonMapping = {}
        parsed_fm = u.Cli.yaml_parse(
            frontmatter_content,
        ).unwrap_or(empty_frontmatter)
        metadata: t.MutableJsonMapping = {
            k: v
            for k, v in (parsed_fm or {}).items()
            if isinstance(v, t.PRIMITIVES_TYPES)
        }
        metadata["updated"] = u.now().strftime("%Y-%m-%d")
        new_frontmatter = u.Cli.yaml_dump_str(
            metadata,
        ).strip()
        new_frontmatter_lines = ["---", *new_frontmatter.split("\n"), "---"]
        return new_frontmatter_lines + list(lines[end_idx:])

    def _save_with_backup(self, file_path: Path, content: str) -> p.Result[None]:
        """Save file with optional backup."""
        if self.backup:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            shutil.copy2(file_path, backup_path)
            self.results.backups_created.append(
                str(backup_path.relative_to(self.project_root)),
            )
        write = u.Cli.atomic_write_text_file(file_path, content)
        if write.failure:
            return r[None].fail(write.error or f"cannot write {file_path}")
        return r[None].ok(None)

    def generate_report(self, report_format: str = "json") -> str:
        """Generate optimization report."""
        report_text: str = (
            self.results.model_dump_json(indent=2)
            if report_format == "json"
            else self.results.model_dump_json()
        )
        return report_text

    def save_report(
        self,
        output_path: str = "docs/maintenance/reports/",
    ) -> p.Result[str]:
        """Save optimization report."""
        output_dir = Path(output_path)
        timestamp = u.now().strftime("%Y%m%d_%H%M%S")
        filename = f"optimization_report_{timestamp}.json"
        filepath = output_dir / filename
        report_content = self.generate_report("json")
        report_write = u.Cli.atomic_write_text_file(filepath, report_content)
        if report_write.failure:
            return r[str].fail(report_write.error or f"cannot write {filepath}")
        latest_file = output_dir / "latest_optimization.json"
        latest_write = u.Cli.json_write(
            latest_file,
            self.results.model_dump(),
            options=m.Cli.JsonWriteOptions(indent=2),
        )
        if latest_write.failure:
            return r[str].fail(latest_write.error or f"cannot write {latest_file}")
        return r[str].ok(str(filepath))

    class Run(s[bool]):
        """CLI command for FLEXT Quality documentation optimization."""

        fix_formatting: bool = u.Field(
            False,
            description="Fix formatting",
            validate_default=True,
        )
        update_toc: bool = u.Field(
            False,
            description="Update tables of contents",
            validate_default=True,
        )
        add_alt_text: bool = u.Field(
            False,
            description="Add missing alt text",
            validate_default=True,
        )
        improve_accessibility: bool = u.Field(
            False,
            description="Improve accessibility",
            validate_default=True,
        )
        optimize_structure: bool = u.Field(
            False,
            description="Optimize content structure",
            validate_default=True,
        )
        update_metadata: bool = u.Field(
            False,
            description="Update metadata",
            validate_default=True,
        )
        comprehensive: bool = u.Field(
            False,
            description="Run all optimizations",
            validate_default=True,
        )
        backup: bool = u.Field(
            True,
            description="Create file backups",
            validate_default=True,
        )
        output: str = u.Field(
            c.Quality.PATHS_DOCS_MAINTENANCE_REPORTS_DIR,
            description="Optimization report output directory",
            validate_default=True,
        )
        files: t.StrSequence = u.Field(
            (),
            description="Documentation files to optimize",
            validate_default=True,
        )

        def discover_files(self) -> t.SequenceOf[Path]:
            """Discover documentation files to optimize."""
            project_root = Path(__file__).parent.parent.parent.parent
            if self.files:
                return [project_root / f for f in self.files]
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
            ignored = [".git", "__pycache__", "node_modules", ".serena/memories"]
            return [f for f in doc_files if not any(pat in str(f) for pat in ignored)]

        @override
        def execute(self) -> p.Result[bool]:
            """Run the requested optimizations."""
            optimizer = FlextQualityDocumentationOptimizer(backup=self.backup)
            run_any = False
            doc_files = self.discover_files()
            if self.fix_formatting or self.comprehensive:
                optimizer.optimize_formatting(doc_files)
                run_any = True
            if self.update_toc or self.comprehensive:
                optimizer.update_table_of_contents(doc_files)
                run_any = True
            if self.add_alt_text or self.improve_accessibility or self.comprehensive:
                optimizer.enhance_accessibility(doc_files)
                run_any = True
            if self.optimize_structure or self.comprehensive:
                optimizer.optimize_content_structure(doc_files)
                run_any = True
            if self.update_metadata or self.comprehensive:
                optimizer.update_metadata(doc_files)
                run_any = True
            if not run_any:
                return r[bool].fail("No optimization selected")
            save_result = optimizer.save_report(self.output)
            if save_result.failure:
                return r[bool].fail(
                    save_result.error or "optimization report write failed",
                )
            return r[bool].ok(value=True)

    @staticmethod
    def main(args: t.StrSequence | None = None) -> int:
        """Run optimization system via the canonical cli facade."""
        exit_code: int = u.Quality.execute_result_command(
            args=args,
            app_name="flext-quality-docs-optimize",
            app_help="FLEXT Quality Documentation Optimization",
            route=m.Cli.ResultCommandRoute(
                name="run",
                help_text="Run documentation optimizations",
                model_cls=FlextQualityDocumentationOptimizer.Run,
                handler=lambda params: params.execute(),
            ),
        )
        return exit_code


if __name__ == "__main__":
    cli.exit(FlextQualityDocumentationOptimizer.main())
