#!/usr/bin/env python3
"""FLEXT-gRPC Documentation Optimization System.

Automated content optimization and enhancement utilities for documentation maintenance.

Author: FLEXT-gRPC Documentation Maintenance System
Version: 1.0.0
"""

import argparse
import json
import operator
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import frontmatter
from flext_core import (
    FlextTypes,
)


class DocumentationOptimizer:
    """Main class for documentation optimization and enhancement."""

    def __init__(self, root_path: str = ".") -> None:
        """Initialize the documentation optimizer.

        Args:
            root_path: Root path for documentation optimization.

        """
        self.root_path = Path(root_path)
        self.config = self._load_config()

    def _load_config(self) -> dict[str, object]:
        """Load optimization configuration."""
        config_path = self.root_path / "docs" / "maintenance" / "config.json"
        if config_path.exists():
            with Path(config_path).open("r", encoding="utf-8") as f:
                return json.load(f)

        # Default configuration
        return {
            "optimization": {
                "auto_fix_formatting": True,
                "generate_toc": True,
                "update_metadata": True,
                "fix_common_issues": True,
                "max_toc_depth": 3,
                "toc_min_headings": 3,
            },
            "formatting": {
                "max_line_length": 88,
                "consistent_list_markers": True,
                "fix_heading_spacing": True,
                "normalize_emphasis": True,
            },
            "metadata": {
                "auto_update_dates": True,
                "add_missing_titles": True,
                "standardize_tags": True,
            },
        }

    def optimize_file(
        self, file_path: Path, dry_run: bool = False
    ) -> dict[str, object]:
        """Optimize a single documentation file."""
        # Read original content
        original_content = file_path.read_text(encoding="utf-8")

        # Parse frontmatter
        try:
            post = frontmatter.loads(original_content)
            metadata = dict[str, object](post.metadata)
            content = post.content
        except:
            metadata = {}
            content = original_content

        optimizations_applied = []
        issues_fixed = 0

        # Apply optimizations
        if self.config["optimization"]["auto_fix_formatting"]:
            content, formatting_fixes = self._fix_formatting(content)
            optimizations_applied.extend(formatting_fixes)
            issues_fixed += len(formatting_fixes)

        if self.config["optimization"]["generate_toc"]:
            content, toc_added = self._add_table_of_contents(content, file_path)
            if toc_added:
                optimizations_applied.append("Added table of contents")
                issues_fixed += 1

        if self.config["optimization"]["update_metadata"]:
            metadata, metadata_updates = self._update_metadata(metadata, file_path)
            optimizations_applied.extend(metadata_updates)
            issues_fixed += len(metadata_updates)

        if self.config["optimization"]["fix_common_issues"]:
            content, common_fixes = self._fix_common_issues(content)
            optimizations_applied.extend(common_fixes)
            issues_fixed += len(common_fixes)

        # Create optimized content
        if metadata:
            optimized_content = frontmatter.dumps(
                post.__class__(content, **metadata) if post else content
            )
        else:
            optimized_content = content

        # Save changes if not dry run
        if not dry_run and optimized_content != original_content:
            file_path.write_text(optimized_content, encoding="utf-8")

        return {
            "file_path": str(file_path.relative_to(self.root_path)),
            "optimizations_applied": optimizations_applied,
            "issues_fixed": issues_fixed,
            "changed": optimized_content != original_content,
            "original_size": len(original_content),
            "optimized_size": len(optimized_content),
        }

    def _fix_formatting(self, content: str) -> tuple[str, FlextTypes.StringList]:
        """Fix common formatting issues."""
        fixes_applied = []
        lines = content.split("\n")

        # Fix line length issues
        max_length = self.config["formatting"]["max_line_length"]
        for i, line in enumerate(lines):
            # Fix line length issues
            if (
                len(line) > max_length
                and not line.startswith("```")
                and not line.strip().startswith("|")
                and " " in line[max_length // 2 :]
            ):
                space_index = line.rfind(" ", 0, max_length)
                if space_index > max_length // 2:
                    lines[i] = line[:space_index] + "\n" + line[space_index + 1 :]
                    fixes_applied.append(f"Fixed long line at {i + 1}")

        # Fix heading spacing
        if self.config["formatting"]["fix_heading_spacing"]:
            for i, line in enumerate(lines):
                if re.match(r"^#{1,6}[^#\s]", line):
                    lines[i] = re.sub(r"^(#{1,6})([^#\s])", r"\1 \2", line)
                    fixes_applied.append(f"Fixed heading spacing at {i + 1}")

        # Consistent list markers
        if self.config["formatting"]["consistent_list_markers"]:
            list_markers = []
            for line in lines:
                match = re.match(r"^([-*+])\s", line)
                if match:
                    list_markers.append(match.group(1))

            if len(set(list_markers)) > 1:
                # Use most common marker
                primary_marker = max(set(list_markers), key=list_markers.count)

                for i, line in enumerate(lines):
                    if re.match(r"^[-*+]\s", line) and not line.startswith(
                        primary_marker
                    ):
                        lines[i] = re.sub(r"^[-*+]", primary_marker, line)
                        fixes_applied.append(f"Standardized list marker at {i + 1}")

        # Normalize emphasis
        if self.config["formatting"]["normalize_emphasis"]:
            # Convert mixed emphasis to consistent style
            # This is a simplified approach - prefer asterisks over underscores
            content_temp = "\n".join(lines)

            # Convert _text_ to *text* for italics
            italic_count = len(re.findall(r"_[^_]+_", content_temp))
            if italic_count > 0:
                content_temp = re.sub(r"_(.*?)_", r"*\1*", content_temp)
                if italic_count > 1:
                    fixes_applied.append(
                        f"Normalized {italic_count} italic emphasis styles"
                    )

            # Convert __text__ to **text** for bold
            bold_count = len(re.findall(r"__[^_]+__", content_temp))
            if bold_count > 0:
                content_temp = re.sub(r"__(.*?)__", r"**\1**", content_temp)
                if bold_count > 1:
                    fixes_applied.append(
                        f"Normalized {bold_count} bold emphasis styles"
                    )

            lines = content_temp.split("\n")

        return "\n".join(lines), fixes_applied

    def _add_table_of_contents(self, content: str, file_path: Path) -> tuple[str, bool]:
        """Add table of contents if appropriate."""
        lines = content.split("\n")

        # Find all headings
        headings = []
        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((i, level, title))

        # Check if TOC should be added
        min_headings = self.config["optimization"]["toc_min_headings"]
        max_depth = self.config["optimization"]["max_toc_depth"]

        if len(headings) < min_headings:
            return content, False

        # Check if TOC already exists
        toc_markers = ["## Table of Contents", "## TOC", "## Contents"]
        for line in lines[:20]:  # Check first 20 lines
            if any(marker.lower() in line.lower() for marker in toc_markers):
                return content, False

        # Generate TOC
        toc_lines = ["## Table of Contents", ""]
        for _line_num, level, title in headings:
            if level <= max_depth:
                indent = "  " * (level - 1)
                # Create anchor link
                anchor = re.sub(r"[^\w\s-]", "", title.lower().replace(" ", "-"))
                toc_lines.append(f"{indent}- [{title}](#{anchor})")

        toc_lines.append("")

        # Find where to insert TOC (after title/metadata, before first heading)
        insert_pos = 0
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\s+", line):
                insert_pos = i
                break

        # Insert TOC
        optimized_lines = lines[:insert_pos] + toc_lines + lines[insert_pos:]

        return "\n".join(optimized_lines), True

    def _update_metadata(
        self, metadata: dict[str, object], file_path: Path
    ) -> tuple[dict[str, object], FlextTypes.StringList]:
        """Update and enhance metadata."""
        updates = []

        # Auto-update dates
        if self.config["metadata"]["auto_update_dates"]:
            current_date = datetime.now(UTC).isoformat()

            if "updated" not in metadata and "last_updated" not in metadata:
                metadata["updated"] = current_date
                updates.append("Added update timestamp")
            elif "updated" in metadata:
                metadata["updated"] = current_date
                updates.append("Updated timestamp")
            elif "last_updated" in metadata:
                metadata["last_updated"] = current_date
                updates.append("Updated last_updated timestamp")

        # Add missing titles
        if self.config["metadata"]["add_missing_titles"] and "title" not in metadata:
            # Generate title from filename
            title = file_path.stem.replace("_", " ").replace("-", " ").title()
            metadata["title"] = title
            updates.append(f"Added title: {title}")

        # Standardize tags
        if (
            self.config["metadata"]["standardize_tags"]
            and "tags" in metadata
            and isinstance(metadata["tags"], str)
        ):
            metadata["tags"] = [tag.strip() for tag in metadata["tags"].split(",")]
            updates.append("Standardized tags format")

        return metadata, updates

    def _fix_common_issues(self, content: str) -> tuple[str, FlextTypes.StringList]:
        """Fix common documentation issues."""
        fixes = []

        # Fix trailing whitespace
        lines = content.split("\n")
        original_lines = len([line for line in lines if line.rstrip() != line])
        if original_lines > 0:
            lines = [line.rstrip() for line in lines]
            fixes.append(f"Removed trailing whitespace from {original_lines} lines")

        # Fix multiple consecutive blank lines (limit to 2)
        content_temp = "\n".join(lines)
        original_blank_lines = len(re.findall(r"\n\n\n+", content_temp))
        if original_blank_lines > 0:
            content_temp = re.sub(r"\n\n\n+", "\n\n", content_temp)
            fixes.append(
                f"Reduced consecutive blank lines in {original_blank_lines} places"
            )
            lines = content_temp.split("\n")

        # Fix missing alt text for images (basic check)
        image_matches = re.findall(r"!\[\]\([^)]+\)", content_temp)
        if image_matches:
            for match in image_matches:
                alt_text = f"![Image]({match[5:]}"  # Add generic alt text
                content_temp = content_temp.replace(match, alt_text, 1)
            fixes.append(f"Added alt text to {len(image_matches)} images")

        # Fix broken internal links (basic)
        # This would require more complex logic to be truly effective

        return "\n".join(lines), fixes

    def optimize_all_files(
        self, files: list[Path] | None = None, dry_run: bool = False
    ) -> dict[str, object]:
        """Optimize all documentation files."""
        if files is None:
            files = self._discover_files()

        results = []
        total_optimizations = 0
        total_issues_fixed = 0
        files_changed = 0

        for file_path in files:
            try:
                result = self.optimize_file(file_path, dry_run=dry_run)
                results.append(result)

                if result["changed"]:
                    files_changed += 1
                    total_optimizations += len(result["optimizations_applied"])
                    total_issues_fixed += result["issues_fixed"]

                    if result["optimizations_applied"]:
                        pass

            except Exception as e:
                results.append({
                    "file_path": str(file_path.relative_to(self.root_path)),
                    "error": str(e),
                    "changed": False,
                })

        return {
            "total_files_processed": len(results),
            "files_changed": files_changed,
            "total_optimizations_applied": total_optimizations,
            "total_issues_fixed": total_issues_fixed,
            "dry_run": dry_run,
            "results": results,
        }

    def _discover_files(self) -> list[Path]:
        """Discover documentation files to optimize."""
        files = []
        patterns = ["*.md", "*.mdx"]

        for pattern in patterns:
            files.extend(
                file_path
                for file_path in self.root_path.rglob(pattern)
                if not any(
                    excl in str(file_path)
                    for excl in [".git", "node_modules", "__pycache__", ".venv"]
                )
            )

        return sorted(files)

    def save_report(
        self, summary: dict[str, object], output_path: Path | None = None
    ) -> None:
        """Save optimization report."""
        if output_path is None:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            output_path = (
                self.root_path
                / "docs"
                / "maintenance"
                / "reports"
                / f"optimization_{timestamp}.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with Path(output_path).open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    def print_summary(self, summary: dict[str, object]) -> None:
        """Print optimization summary."""
        if summary.get("dry_run"):
            pass

        # Show top optimizations
        if summary["results"]:
            optimization_counts: dict[str, int] = {}
            for result in summary["results"]:
                for opt in result.get("optimizations_applied", []):
                    if opt not in optimization_counts:
                        optimization_counts[opt] = 0
                    optimization_counts[opt] += 1

            if optimization_counts:
                for opt, _count in sorted(
                    optimization_counts.items(),
                    key=operator.itemgetter(1),
                    reverse=True,
                ):
                    pass


class DocumentationEnhancer:
    """Advanced documentation enhancement utilities."""

    def __init__(self, root_path: str = ".") -> None:
        self.root_path = Path(root_path)

    def enhance_readability(self, content: str) -> tuple[str, FlextTypes.StringList]:
        """Enhance content readability."""
        enhancements = []

        # Add section breaks for long content
        lines = content.split("\n")

        # Suggest adding more headings for long sections
        heading_positions = []
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\s+", line):
                heading_positions.append(i)

        # Check for long sections without subheadings
        for i in range(len(heading_positions) - 1):
            start_line = heading_positions[i]
            end_line = heading_positions[i + 1]

            section_length = end_line - start_line
            if section_length > 100:  # Arbitrary threshold
                # This would require more sophisticated analysis
                pass

        # Basic enhancements that can be automated
        # (More advanced readability enhancements would require NLP)

        return content, enhancements

    def add_cross_references(
        self, content: str, all_files: list[Path]
    ) -> tuple[str, FlextTypes.StringList]:
        """Add intelligent cross-references between documents."""
        references_added = []

        # This would require sophisticated analysis of content relationships
        # For now, just a placeholder for future enhancement

        return content, references_added

    def generate_related_links(
        self, file_path: Path, all_files: list[Path]
    ) -> FlextTypes.StringList:
        """Generate suggestions for related documentation links."""
        suggestions = []

        # Analyze filename and content to suggest related docs
        filename = file_path.stem.lower()

        for other_file in all_files:
            if other_file != file_path:
                other_name = other_file.stem.lower()

                # Simple keyword matching
                if any(
                    keyword in filename and keyword in other_name
                    for keyword in ["api", "config", "install", "guide", "reference"]
                ):
                    suggestions.append(f"Consider linking to {other_file.name}")

        return suggestions

    def validate_content_completeness(
        self, content: str, file_path: Path
    ) -> dict[str, object]:
        """Validate content completeness and suggest improvements."""
        validation = {"score": 100, "missing_elements": [], "suggestions": []}

        # Check for common documentation elements
        checks = {
            "code_examples": bool(r"```" in content),
            "links": bool(re.findall(r"\[([^\]]+)\]\([^)]+\)", content)),
            "headings": bool(re.findall(r"^#{1,6}\s+", content, re.MULTILINE)),
            "lists": bool(re.findall(r"^[-*+]\s", content, re.MULTILINE)),
        }

        missing_count = sum(1 for check, present in checks.items() if not present)
        validation["score"] -= missing_count * 10

        if not checks["code_examples"]:
            validation["missing_elements"].append("code examples")
            validation["suggestions"].append("Add code examples to illustrate usage")

        if not checks["links"]:
            validation["missing_elements"].append("cross-references")
            validation["suggestions"].append("Add links to related documentation")

        return validation


def main() -> int:
    """Main entry point for documentation optimization."""
    parser = argparse.ArgumentParser(
        description="FLEXT-gRPC Documentation Optimization System"
    )
    parser.add_argument("--path", default=".", help="Root path to optimize")
    parser.add_argument("--output", help="Output path for report")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without applying them"
    )
    parser.add_argument("--file", help="Optimize only specific file")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args()

    # Create optimizer
    optimizer = DocumentationOptimizer(args.path)

    # Determine files to process
    files = [Path(args.file)] if args.file else optimizer._discover_files()

    if not files:
        return 1

    # Run optimization
    summary = optimizer.optimize_all_files(files, dry_run=args.dry_run)

    # Save report
    output_path = Path(args.output) if args.output else None

    optimizer.save_report(summary, output_path)

    # Print summary
    if not args.quiet:
        optimizer.print_summary(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
