"""Dependency discovery helpers migrated from flext_tools.discovery_base."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes


class DependencyDiscovery(FlextService[list[FlextTypes.StringDict]]):
    """Inspect Python files to extract import information."""

    def __init__(self: Self) -> None:
        super().__init__()

    def execute(self: Self) -> FlextResult[list[FlextTypes.StringDict]]:
        """Return empty discovery results by default."""
        return FlextResult[list[FlextTypes.StringDict]].ok([])

    def discover_dependencies(
        self,
        project_path: str | Path,
    ) -> FlextResult[list[FlextTypes.StringDict]]:
        """Collect import statements for Python files in *project_path*."""
        root = Path(project_path).expanduser()
        if not root.exists():
            return FlextResult[list[FlextTypes.StringDict]].fail(
                f"Project path does not exist: {root}"
            )

        python_files = list(root.rglob("*.py"))
        discovery_results: list[FlextTypes.StringDict] = []
        for file_path in python_files:
            imports = self.analyze_imports(str(file_path))
            if imports.is_success:
                discovery_results.append(
                    {
                        "file": str(file_path.relative_to(root)),
                        "imports": imports.value,
                    }
                )

        return FlextResult[list[FlextTypes.StringDict]].ok(discovery_results)

    def analyze_imports(self, file_path: str) -> FlextResult[FlextTypes.StringList]:
        """Parse a Python file and return imported module names."""
        path = Path(file_path).expanduser()
        if not path.exists():
            return FlextResult[FlextTypes.StringList].fail(
                f"File path does not exist: {path}"
            )

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, SyntaxError) as error:
            return FlextResult[FlextTypes.StringList].fail(
                f"Failed to analyse imports: {error}"
            )

        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split(".", maxsplit=1)[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".", maxsplit=1)[0])

        return FlextResult[FlextTypes.StringList].ok(sorted(modules))


__all__ = ["DependencyDiscovery"]
