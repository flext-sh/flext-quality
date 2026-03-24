"""FLEXT Quality Documentation Maintenance - File Discovery.

Documentation file discovery and filtering system.
Finds, categorizes, and filters documentation files in a project.
"""

from __future__ import annotations

import fnmatch
import logging
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import ClassVar, NotRequired, TypedDict

from flext_quality import m, t


class FlextQualityFileStatistics(TypedDict):
    """Statistics payload for discovered documentation files."""

    total_files: int
    total_size: NotRequired[int]
    total_lines: NotRequired[int]
    total_words: NotRequired[int]
    markdown_files: NotRequired[int]
    other_files: NotRequired[int]
    size_distribution: NotRequired[Mapping[str, int]]
    categories: NotRequired[Mapping[str, int]]
    avg_file_size: NotRequired[float]
    avg_lines_per_file: NotRequired[float]
    avg_words_per_file: NotRequired[float]


class FlextQualityDocumentationFinder:
    """Documentation file discovery and filtering system."""

    # Common documentation file patterns
    DEFAULT_PATTERNS: ClassVar[MutableSequence[str]] = [
        "**/*.md",
        "**/*.mdx",
        "**/*.rst",
        "**/*.txt",
        "**/README*",
        "**/CHANGELOG*",
        "**/CONTRIBUTING*",
        "**/docs/**/*.md",
        "**/docs/**/*.mdx",
        "**/docs/**/*.rst",
        "**/documentation/**/*.md",
        "**/documentation/**/*.mdx",
        "**/wiki/**/*.md",
    ]

    # File size constants (in bytes)
    SIZE_SMALL: int = 1024  # 1KB
    SIZE_MEDIUM: int = 10240  # 10KB
    SIZE_LARGE: int = 102400  # 100KB

    # Path depth constants
    DOCS_ROOT_DEPTH: int = 2

    # Default ignore patterns
    DEFAULT_IGNORE_PATTERNS: ClassVar[MutableSequence[str]] = [
        "**/node_modules/**",
        "**/build/**",
        "**/dist/**",
        "**/.git/**",
        "**/__pycache__/**",
        "**/.*",
        "**/cache/**",
        "**/tmp/**",
        "**/temp/**",
        "**/*.min.*",
        "**/vendor/**",
        "**/env/**",
        "**/venv/**",
        "**/.env/**",
        "**/coverage/**",
        "**/reports/**",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache/**",
        "**/.mypy_cache/**",
        "**/.tox/**",
    ]

    def __init__(
        self,
        project_root: Path,
        patterns: t.StrSequence | None = None,
        ignore_patterns: t.StrSequence | None = None,
        ignore_file: str | None = None,
    ) -> None:
        """Initialize the documentation finder.

        Args:
            project_root: Root directory of the project
            patterns: Custom file patterns to search for
            ignore_patterns: Custom patterns to ignore
            ignore_file: Path to .ignore file (like .gitignore)

        """
        self.project_root = project_root.resolve()
        self.patterns: MutableSequence[str] = (
            list(patterns) if patterns else list(self.DEFAULT_PATTERNS)
        )
        self.ignore_patterns: MutableSequence[str] = (
            list(ignore_patterns)
            if ignore_patterns
            else list(self.DEFAULT_IGNORE_PATTERNS)
        )
        self.ignore_file = ignore_file or ".gitignore"

        # Load ignore patterns from file if it exists
        self._load_ignore_file()

        # Cache for found files
        self._file_cache: MutableSequence[Path] | None = None
        self._metadata_cache: MutableMapping[str, m.Quality.FileMetadata] = {}

    def _load_ignore_file(self) -> None:
        """Load ignore patterns from .gitignore or similar file."""
        ignore_path = self.project_root / self.ignore_file
        if not ignore_path.exists():
            return

        try:
            self._load_ignore_patterns_from_file(ignore_path)
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
            # If we can't read the ignore file, just continue silently
            # This is acceptable as ignore files are optional
            logger = logging.getLogger(__name__)
            logger.debug(f"Could not read ignore file {self.ignore_file}: {e}")

    def _load_ignore_patterns_from_file(self, ignore_path: Path) -> None:
        """Load and process ignore patterns from file.

        Args:
            ignore_path: Path to ignore file

        """
        with ignore_path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if line and not line.startswith("#"):
                    processed_line = self._process_ignore_line(line)
                    if processed_line:
                        self.ignore_patterns.append(processed_line)

    def _process_ignore_line(self, line: str) -> str:
        """Process a single ignore line into a glob pattern.

        Args:
            line: Raw ignore line from file

        Returns:
            Processed glob pattern

        """
        # Convert gitignore patterns to glob patterns
        line = line.removeprefix("/")
        if not line.startswith("**/"):
            line = f"**/{line}"
        if (
            not line.endswith("/**")
            and "." not in Path(line).name
            and "/" in line
            and not line.endswith("**")
        ):
            # Add /** for directory patterns
            line = f"{line}/**"
        return line

    def find_files(self, *, use_cache: bool = True) -> Sequence[Path]:
        """Find all documentation files in the project.

        Args:
            use_cache: Whether to use cached results

        Returns:
            List of Path objects for found documentation files

        """
        if use_cache and self._file_cache is not None:
            return list(self._file_cache)

        found_files: MutableSequence[Path] = []

        for pattern in self.patterns:
            try:
                # Use pathlib for pattern matching
                matches = list(self.project_root.glob(pattern))
                found_files.extend(
                    match
                    for match in matches
                    if match.is_file() and not self._is_ignored(match)
                )
            except (OSError, ValueError) as e:
                # Skip patterns that cause errors during glob matching
                # This prevents crashes from malformed glob patterns
                logger = logging.getLogger(__name__)
                logger.debug(
                    "Error during glob matching for pattern '%s': %s",
                    pattern,
                    e,
                )

        # Remove duplicates while preserving order
        seen: set[str] = set()
        unique_files: MutableSequence[Path] = []
        for file_path in found_files:
            file_str = str(file_path)
            if file_str not in seen:
                seen.add(file_str)
                unique_files.append(file_path)

        # Sort by path for consistent ordering
        unique_files = sorted(unique_files, key=str)

        if use_cache:
            self._file_cache = list(unique_files)

        return unique_files

    def _is_ignored(self, file_path: Path) -> bool:
        """Check if a file should be ignored based on patterns."""
        try:
            # Get relative path from project root
            relative_path = file_path.relative_to(self.project_root)
            path_str = str(relative_path)

            # Check against ignore patterns
            for pattern in self.ignore_patterns:
                if self._matches_pattern(path_str, pattern):
                    return True

            return False

        except ValueError:
            # If we can't make it relative, it's probably outside the project
            return True

    def _matches_pattern(self, path_str: str, pattern: str) -> bool:
        """Check if a path matches a glob pattern."""
        # Simple glob matching - could be enhanced with more sophisticated matching
        try:
            return fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(
                path_str,
                pattern.rstrip("/"),
            )
        except (OSError, ValueError):
            return False

    def find_markdown_files(self) -> Sequence[Path]:
        """Find specifically markdown files."""
        all_files = self.find_files()
        return [f for f in all_files if f.suffix.lower() in {".md", ".mdx"}]

    def find_readme_files(self) -> Sequence[Path]:
        """Find README files."""
        all_files = self.find_files()
        return [f for f in all_files if f.name.lower().startswith("readme")]

    def find_by_extension(self, extensions: t.StrSequence) -> Sequence[Path]:
        """Find files by their extensions."""
        all_files = self.find_files()
        extensions = [ext.lower().lstrip(".") for ext in extensions]
        return [f for f in all_files if f.suffix.lower().lstrip(".") in extensions]

    def get_file_metadata(self, file_path: Path) -> m.Quality.FileMetadata:
        """Get metadata for a specific file."""
        path_str = str(file_path)
        if path_str not in self._metadata_cache:
            self._metadata_cache[path_str] = m.Quality.FileMetadata.from_path(file_path)
        return self._metadata_cache[path_str]

    def get_files_metadata(
        self,
        files: Sequence[Path] | None = None,
    ) -> Sequence[m.Quality.FileMetadata]:
        """Get metadata for multiple files."""
        if files is None:
            files = self.find_files()

        return [self.get_file_metadata(f) for f in files]

    def _initialize_categories(self) -> MutableMapping[str, MutableSequence[Path]]:
        """Initialize empty category dictionaries."""
        return {
            "readme": [],
            "changelog": [],
            "contributing": [],
            "docs_root": [],
            "docs_subdir": [],
            "examples": [],
            "other": [],
        }

    def _categorize_by_filename(self, filename: str) -> str | None:
        """Categorize file by filename patterns."""
        filename_lower = filename.lower()
        if filename_lower.startswith("readme"):
            return "readme"
        if filename_lower.startswith("changelog"):
            return "changelog"
        if filename_lower.startswith("contributing"):
            return "contributing"
        return None

    def _categorize_by_directory(self, path_parts: tuple[str, ...]) -> str:
        """Categorize file by directory structure."""
        if len(path_parts) <= 1:
            return "other"

        first_dir = path_parts[0].lower()
        if first_dir == "docs":
            return (
                "docs_root"
                if len(path_parts) == self.DOCS_ROOT_DEPTH
                else "docs_subdir"
            )
        if first_dir in {"examples", "example", "samples", "demos"}:
            return "examples"
        return "other"

    def _safe_get_relative_path(self, file_path: Path) -> tuple[str, ...] | None:
        """Safely get relative path parts."""
        try:
            relative_path = file_path.relative_to(self.project_root)
            return relative_path.parts
        except (ValueError, OSError):
            return None

    def categorize_files(
        self,
        files: Sequence[Path] | None = None,
    ) -> MutableMapping[str, MutableSequence[Path]]:
        """Categorize files by type and location."""
        if files is None:
            files = self.find_files()

        categories = self._initialize_categories()

        for file_path in files:
            # Try filename-based categorization first
            filename_category = self._categorize_by_filename(file_path.name)
            if filename_category:
                categories[filename_category].append(file_path)
                continue

            # Fallback to directory-based categorization
            path_parts = self._safe_get_relative_path(file_path)
            if path_parts is not None:
                dir_category = self._categorize_by_directory(path_parts)
                categories[dir_category].append(file_path)
            else:
                categories["other"].append(file_path)

        return categories

    def get_statistics(
        self, files: Sequence[Path] | None = None
    ) -> FlextQualityFileStatistics:
        """Get statistics about found files."""
        if files is None:
            files = self.find_files()

        if not files:
            return {"total_files": 0}

        metadata_list = self.get_files_metadata(files)

        # Basic statistics
        stats: FlextQualityFileStatistics = {
            "total_files": len(files),
            "total_size": sum(meta.size for meta in metadata_list),
            "total_lines": sum(meta.lines for meta in metadata_list),
            "total_words": sum(meta.words for meta in metadata_list),
            "markdown_files": len([
                f for f in files if f.suffix.lower() in {".md", ".mdx"}
            ]),
            "other_files": len([
                f for f in files if f.suffix.lower() not in {".md", ".mdx"}
            ]),
        }

        # File size distribution
        size_ranges = {
            "small": len([
                m for m in metadata_list if m.size < self.SIZE_SMALL
            ]),  # < 1KB
            "medium": len([
                m for m in metadata_list if self.SIZE_SMALL <= m.size < self.SIZE_MEDIUM
            ]),  # 1-10KB
            "large": len([
                m for m in metadata_list if self.SIZE_MEDIUM <= m.size < self.SIZE_LARGE
            ]),  # 10-100KB
            "huge": len([
                m for m in metadata_list if m.size >= self.SIZE_LARGE
            ]),  # > 100KB
        }
        stats["size_distribution"] = size_ranges

        # Categories
        categories = self.categorize_files(files)
        stats["categories"] = {cat: len(files) for cat, files in categories.items()}

        # Average metrics
        if stats["total_files"] > 0:
            stats["avg_file_size"] = stats.get("total_size", 0) / stats["total_files"]
            stats["avg_lines_per_file"] = (
                stats.get("total_lines", 0) / stats["total_files"]
            )
            stats["avg_words_per_file"] = (
                stats.get("total_words", 0) / stats["total_files"]
            )

        return stats

    def invalidate_cache(self) -> None:
        """Invalidate the file cache."""
        self._file_cache = None
        self._metadata_cache = {}

    def add_pattern(self, pattern: str) -> None:
        """Add a custom search pattern."""
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            self.invalidate_cache()

    def add_ignore_pattern(self, pattern: str) -> None:
        """Add a custom ignore pattern."""
        if pattern not in self.ignore_patterns:
            self.ignore_patterns.append(pattern)
            self.invalidate_cache()

    def filter_by_age(self, files: Sequence[Path], max_age_days: int) -> Sequence[Path]:
        """Filter files by maximum age in days."""
        cutoff_time = (datetime.now(UTC) - timedelta(days=max_age_days)).timestamp()

        return [f for f in files if f.stat().st_mtime >= cutoff_time]

    def filter_by_size(
        self,
        files: Sequence[Path],
        min_size: int = 0,
        max_size: int | None = None,
    ) -> Sequence[Path]:
        """Filter files by size range."""
        filtered = [f for f in files if f.stat().st_size >= min_size]
        if max_size is not None:
            filtered = [f for f in filtered if f.stat().st_size <= max_size]
        return filtered

    def find_recently_modified(self, days: int = 7) -> Sequence[Path]:
        """Find files modified within the last N days."""
        return self.filter_by_age(self.find_files(), days)


# Module-level aliases for pyrefly compatibility
FileStatistics = FlextQualityFileStatistics
DocumentationFinder = FlextQualityDocumentationFinder
