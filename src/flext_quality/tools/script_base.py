"""Base script service used by migrated quality scripts."""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes as t


@dataclass(slots=True)
class ScriptMetadata:
    """Simple metadata holder for script definitions."""

    name: str
    description: str
    category: str
    version: str = "1.0.0"


class FlextScriptService(FlextService[object], ABC):
    """Provide a consistent execution harness for CLI-style scripts."""

    def __init__(self: Self) -> None:
        """Initialize script service."""
        super().__init__()

    @property
    @abstractmethod
    def metadata(self: Self) -> ScriptMetadata:
        """Return metadata describing the script."""

    def execute(self: Self, **_kwargs: object) -> FlextResult[object]:
        """Alias for :meth:`run` to satisfy FlextService contract."""
        return self.run({})

    def create_parser(self: Self) -> argparse.ArgumentParser:
        """Return a pre-configured argument parser using metadata."""
        meta = self.metadata
        parser = argparse.ArgumentParser(
            prog=meta.name,
            description=meta.description,
        )
        parser.add_argument("--version", action="version", version=meta.version)
        return parser

    def validate_preconditions(self: Self) -> FlextResult[bool]:
        """Hook used by subclasses to ensure prerequisites are satisfied."""
        return FlextResult[bool].ok(True)

    def run(
        self: Self, args: dict[str, t.GeneralValueType] | None = None
    ) -> FlextResult[object]:
        """Execute the script with validation and error handling."""
        validation = self.validate_preconditions()
        if validation.is_failure:
            return FlextResult[object].fail(
                validation.error or "Preconditions validation failed",
            )

        try:
            return self.execute_implementation(args or {})
        except Exception as error:
            self.logger.exception("Script execution failed")
            return FlextResult[object].fail(str(error))

    def main(self: Self) -> int:
        """CLI entrypoint used by standalone scripts."""
        parser = self.create_parser()
        namespace = parser.parse_args()
        result = self.run(vars(namespace))
        return 0 if result.is_success else 1

    @abstractmethod
    def execute_implementation(
        self,
        args: dict[str, t.GeneralValueType],
    ) -> FlextResult[object]:
        """Execute the script logic."""


__all__ = ["FlextScriptService", "ScriptMetadata"]
