"""Dependency conflict analysis helpers for flext-quality tools."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService, FlextTypes


class ConflictAnalyzer(FlextService[list[FlextTypes.StringDict]]):
    """Perform lightweight dependency conflict inspections."""

    def __init__(self: Self) -> None:
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[list[FlextTypes.StringDict]]:
        """Return an empty conflict list for the base service contract."""
        return FlextResult[list[FlextTypes.StringDict]].ok([])

    def analyze_dependencies(
        self,
        project_path: str | Path,
    ) -> FlextResult[list[FlextTypes.StringDict]]:
        """Analyse dependency declarations for duplicates with different pins."""
        project = Path(project_path).expanduser()
        if not project.exists():
            return FlextResult[list[FlextTypes.StringDict]].fail(
                f"Project path does not exist: {project}"
            )

        pyproject = project / "pyproject.toml"
        if not pyproject.exists():
            return FlextResult[list[FlextTypes.StringDict]].ok([])

        try:
            with pyproject.open("rb") as handle:
                raw = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as error:
            self._logger.exception("Failed to load pyproject.toml")
            return FlextResult[list[FlextTypes.StringDict]].fail(
                f"Failed to read pyproject.toml: {error}"
            )

        deps: dict[str, str] = {}
        conflicts: list[FlextTypes.StringDict] = []
        poetry_data = raw.get("tool", {}).get("poetry", {})
        for section in ("dependencies", "group"):
            section_data = poetry_data.get(section, {})
            if section == "group":
                for group_data in section_data.values():
                    group_deps = group_data.get("dependencies", {})
                    conflicts.extend(self._collect_conflicts(group_deps, deps))
            else:
                conflicts.extend(self._collect_conflicts(section_data, deps))

        return FlextResult[list[FlextTypes.StringDict]].ok(conflicts)

    @staticmethod
    def _collect_conflicts(
        new_deps: dict[str, object],
        known: dict[str, str],
    ) -> list[FlextTypes.StringDict]:
        conflicts: list[FlextTypes.StringDict] = []
        for name, spec in new_deps.items():
            if not isinstance(spec, str):
                continue
            previous = known.get(name)
            if previous and previous != spec:
                conflicts.append(
                    {
                        "dependency": name,
                        "current": previous,
                        "requested": spec,
                    }
                )
            known[name] = spec
        return conflicts

    def detect_version_conflicts(self: Self) -> FlextResult[FlextTypes.StringList]:
        """Compat method retained for script expectations."""
        return FlextResult[FlextTypes.StringList].ok([])

    def resolve_conflicts(self: Self) -> FlextResult[None]:
        """Placeholder resolution hook."""
        return FlextResult[None].ok(None)


__all__ = ["ConflictAnalyzer"]
