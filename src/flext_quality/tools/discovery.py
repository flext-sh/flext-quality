"""Dependency discovery helpers migrated from flext_tools.discovery_base."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Self

from flext import FlextResult, FlextService


class DependencyDiscovery(FlextService[list[dict[str, object]]]):
    """Inspect Python files to extract import information."""

    def __init__(self: Self) -> None:
        """Initialize discovery service with default FlextService setup."""
        super().__init__()

    def execute(self: Self) -> FlextResult[list[dict[str, object]]]:
        """Return empty discovery results by default."""
        return FlextResult[list[dict[str, object]]].ok([])

    def discover_dependencies(
        self,
        project_path: str | Path,
    ) -> FlextResult[list[dict[str, object]]]:
        """Collect import statements for Python files in *project_path*."""
        root = Path(project_path).expanduser()
        if not root.exists():
            return FlextResult[list[dict[str, object]]].ok([])

        python_files = list(root.rglob("*.py"))
        discovery_results: list[dict[str, object]] = []
        for file_path in python_files:
            imports = self.analyze_imports(str(file_path))
            if imports.is_success:
                discovery_results.append({
                    "file": str(file_path.relative_to(root)),
                    "imports": imports.value,
                })

        return FlextResult[list[dict[str, object]]].ok(discovery_results)

    def analyze_imports(self, file_path: str) -> FlextResult[list[str]]:
        """Parse a Python file and return imported module names."""
        path = Path(file_path).expanduser()
        if not path.exists():
            return FlextResult[list[str]].fail(f"File path does not exist: {path}")

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, SyntaxError) as error:
            return FlextResult[list[str]].fail(f"Failed to analyse imports: {error}")

        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(
                    alias.name.split(".", maxsplit=1)[0] for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".", maxsplit=1)[0])

        return FlextResult[list[str]].ok(sorted(modules))


__all__ = ["DependencyDiscovery"]
