"""Path helpers for quality tooling."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Self

from flext_core import FlextLogger, FlextResult, FlextService


class FlextPathService(FlextService[Path]):
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
        ]

        @classmethod
        def should_ignore_path(cls, path: str | Path) -> bool:
            path_str = str(path)
            return any(pattern in path_str for pattern in cls.IGNORE_PATTERNS)

    class Paths(_ValidationHelper):
        """Alias matching the previous API surface."""

    def __init__(self: Self) -> None:
        """Initialize paths service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[None]:
        """Return a simple success result."""
        return FlextResult[None].ok(None)

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
