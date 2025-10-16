"""Path helpers for quality tooling."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService


class FlextPathService(FlextService[None]):
    """Expose convenience helpers mirroring the historical flext_tools API."""

    def __init__(self: Self) -> None:
        super().__init__()
        self.logger = FlextLogger(__name__)

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
