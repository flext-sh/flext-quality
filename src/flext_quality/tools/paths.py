"""Path helpers for quality tooling."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Self

from flext import FlextLogger, FlextResult, FlextService


class FlextPathService(FlextService[bool]):
    """Expose convenience helpers mirroring the historical flext_tools API."""

    class _ValidationHelper:
        """Leverage legacy ignore pattern semantics."""

        IGNORE_PATTERNS: ClassVar[list[str]] = [
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "*.pyc",
            "*.pyo",
        ]

        @classmethod
        def should_ignore_path(cls, path: str | Path) -> bool:
            path_str = str(path)
            for pattern in cls.IGNORE_PATTERNS:
                if pattern.startswith("*."):
                    # Wildcard pattern like *.pyc
                    extension = pattern[1:]  # Remove * to get .pyc
                    if path_str.endswith(extension):
                        return True
                elif pattern in path_str:
                    # Direct substring match
                    return True
            return False

    class _UtilityHelper:
        """Utility helper for path operations."""

        @staticmethod
        def normalize_path(path: str | Path) -> Path:
            """Normalize a path by resolving it."""
            return FlextPathService.resolve(path)

        @staticmethod
        def resolve_path(path: str | Path) -> Path:
            """Resolve a path to an absolute Path."""
            return FlextPathService.resolve(path)

    class Paths(_ValidationHelper):
        """Alias matching the previous API surface."""

    def __init__(self: Self) -> None:
        """Initialize paths service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[bool]:
        """Return a simple success result."""
        return FlextResult[bool].ok(True)

    @staticmethod
    def resolve(path: str | Path) -> Path:
        """Resolve *path* to an absolute Path."""
        return Path(path).expanduser().resolve()

    @staticmethod
    def is_within(base: str | Path, candidate: str | Path) -> bool:
        """Return True if *candidate* is within *base*."""
        base_path = Path(base).expanduser().resolve()
        try:
            Path(candidate).expanduser().resolve().relative_to(base_path)
        except ValueError:
            return False
        return True


__all__ = ["FlextPathService"]
