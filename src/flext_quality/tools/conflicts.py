"""Dependency conflict analysis helpers for flext-quality tools."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Self

from flext import FlextLogger, FlextResult, FlextService


class ConflictAnalyzer(FlextService[list[dict[str, str]]]):
    """Analyze conflicts in code quality tools."""

    def __init__(self: Self) -> None:
        """Initialize the ConflictAnalyzer service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[list[dict[str, str]]]:
        """Return an empty conflict list for the base service contract."""
        return FlextResult[list[dict[str, str]]].ok([])

    def analyze_dependencies(
        self,
        project_path: str | Path,
    ) -> FlextResult[list[dict[str, str]]]:
        """Analyse dependency declarations for duplicates with different pins."""
        # Validate project path is not empty
        if not project_path or (
            isinstance(project_path, str) and not project_path.strip()
        ):
            return FlextResult[list[dict[str, str]]].fail(
                "Project path cannot be empty",
                error_code="VALIDATION_ERROR",
            )

        project = Path(project_path).expanduser()
        if not project.exists():
            return FlextResult[list[dict[str, str]]].ok([])

        pyproject = project / "pyproject.toml"
        if not pyproject.exists():
            return FlextResult[list[dict[str, str]]].ok([])

        try:
            with pyproject.open("rb") as handle:
                raw = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError):
            self._logger.debug("Unable to load pyproject.toml for %s", project)
            return FlextResult[list[dict[str, str]]].ok([])

        deps: dict[str, str] = {}
        conflicts: list[dict[str, str]] = []
        poetry_data = raw.get("tool", {}).get("poetry", {})
        for section in ("dependencies", "group"):
            section_data = poetry_data.get(section, {})
            if section == "group":
                for group_data in section_data.values():
                    group_deps = group_data.get("dependencies", {})
                    conflicts.extend(self._collect_conflicts(group_deps, deps))
            else:
                conflicts.extend(self._collect_conflicts(section_data, deps))

        return FlextResult[list[dict[str, str]]].ok(conflicts)

    @staticmethod
    def _collect_conflicts(
        new_deps: dict[str, object],
        known: dict[str, str],
    ) -> list[dict[str, str]]:
        conflicts: list[dict[str, str]] = []
        for name, spec in new_deps.items():
            if not isinstance(spec, str):
                continue
            previous = known.get(name)
            if previous and previous != spec:
                conflicts.append({
                    "dependency": name,
                    "current": previous,
                    "requested": spec,
                })
            known[name] = spec
        return conflicts

    def detect_version_conflicts(self: Self) -> FlextResult[list[str]]:
        """Compat method retained for script expectations."""
        return FlextResult[list[str]].ok([])

    def resolve_conflicts(self: Self) -> FlextResult[bool]:
        """Placeholder resolution hook."""
        return FlextResult[bool].ok(True)

    def get_conflicts(self: Self) -> FlextResult[list[dict[str, str]]]:
        """Get conflicts for the current working directory."""
        return self.analyze_dependencies(Path.cwd())


__all__ = ["ConflictAnalyzer"]
