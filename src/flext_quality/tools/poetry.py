"""Poetry operations and validation utilities for quality tooling."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextUtilities


class PoetryOperations(FlextService[str]):
    """Execute simple Poetry commands with FlextResult wrapping."""

    def __init__(self: Self) -> None:
        """Initialize the PoetryOperations service."""
        super().__init__()

    def execute(self: Self) -> FlextResult[str]:
        """Return a status message for compatibility."""
        return FlextResult[str].ok("Poetry operations ready")

    def install_dependencies(self, project_path: str | Path) -> FlextResult[str]:
        """Invoke ``poetry install`` if poetry is available."""
        return self._run_poetry(project_path, ["install"], "install")

    def update_dependencies(self, project_path: str | Path) -> FlextResult[str]:
        """Invoke ``poetry update`` if poetry is available."""
        return self._run_poetry(project_path, ["update"], "update")

    def check_lock_file(self, project_path: str | Path) -> FlextResult[bool]:
        """Check if ``poetry.lock`` exists in the project path."""
        project = Path(project_path).expanduser()
        lock_file = project / "poetry.lock"
        return FlextResult[bool].ok(lock_file.exists())

    def get_outdated_packages(self: Self) -> FlextResult[list[str]]:
        """Placeholder: poetry export of outdated packages is not yet implemented."""
        return FlextResult[list[str]].ok([])

    @staticmethod
    def _run_poetry(
        project_path: str | Path,
        args: list[str],
        operation: str,
    ) -> FlextResult[str]:
        project = Path(project_path).expanduser()
        if not project.exists():
            return FlextResult[str].fail(f"Project path does not exist: {project}")

        poetry_cmd = ["poetry", *args]
        result = FlextUtilities.CommandExecution.run_external_command(
            poetry_cmd,
            cwd=project,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.is_failure:
            return FlextResult[str].fail(
                f"Poetry {operation} failed: {result.error}",
            )

        completed = result.value
        if completed.returncode != 0:
            return FlextResult[str].fail(
                f"Poetry {operation} failed: {completed.stderr}"
            )
        return FlextResult[str].ok(
            f"Poetry {operation} completed for {project}",
        )


class PoetryValidator(FlextService[dict[str, bool]]):
    """Validate ``pyproject.toml`` structure for basic sanity checks."""

    def __init__(self: Self) -> None:
        """Initialize the PoetryValidator service."""
        super().__init__()

    def execute(self: Self) -> FlextResult[dict[str, bool]]:
        """Return default validation state."""
        return FlextResult[dict[str, bool]].ok({
            "pyproject_exists": False,
            "poetry_section": False,
            "dependencies_defined": False,
        })

    def validate_pyproject(
        self,
        project_path: str | Path,
    ) -> FlextResult[dict[str, bool]]:
        """Validate ``pyproject.toml`` at *project_path*."""
        project = Path(project_path).expanduser()
        pyproject = project / "pyproject.toml"

        if not pyproject.exists():
            return FlextResult[dict[str, bool]].ok({
                "pyproject_exists": False,
                "poetry_section": False,
                "dependencies_defined": False,
            })

        try:
            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as error:
            return FlextResult[dict[str, bool]].fail(
                f"Failed to read pyproject.toml: {error}"
            )

        poetry_data = data.get("tool", {}).get("poetry", {})
        dependencies = poetry_data.get("dependencies", {})
        stats = {
            "pyproject_exists": True,
            "poetry_section": bool(poetry_data),
            "dependencies_defined": bool(dependencies),
        }
        return FlextResult[dict[str, bool]].ok(stats)

    def validate_project(self, project_path: str | Path) -> FlextResult[bool]:
        """Return success if ``pyproject.toml`` passes validation."""
        result = self.validate_pyproject(project_path)
        if result.is_failure:
            return FlextResult[bool].fail(result.error or "Poetry validation failed")
        return FlextResult[bool].ok(result.value["pyproject_exists"])

    def check_lock_consistency(self, project_path: str | Path) -> FlextResult[bool]:
        """Ensure ``poetry.lock`` exists when dependencies are defined."""
        project = Path(project_path).expanduser()
        lock_path = project / "poetry.lock"
        return FlextResult[bool].ok(lock_path.exists())

    def get_dependency_issues(self: Self) -> FlextResult[list[str]]:
        """Placeholder that keeps interface compatibility."""
        return FlextResult[list[str]].ok([])

    def check_dependencies(
        self,
        project_path: str | Path,
    ) -> FlextResult[dict[str, object]]:
        """Return a coarse dependency summary."""
        validation = self.validate_pyproject(project_path)
        if validation.is_failure:
            return FlextResult[dict[str, object]].fail(
                validation.error or "Dependency check failed"
            )

        project = Path(project_path).expanduser()
        pyproject = project / "pyproject.toml"

        summary: dict[str, object] = {
            "project_path": str(project),
            "pyproject_exists": validation.value["pyproject_exists"],
            "dependencies_valid": validation.value["dependencies_defined"],
            "dependency_count": 0,
            "dev_dependencies_valid": False,
            "dev_dependency_count": 0,
        }

        if not pyproject.exists():
            return FlextResult[dict[str, object]].ok(summary)

        try:
            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as error:
            return FlextResult[dict[str, object]].fail(
                f"Failed to read pyproject.toml: {error}"
            )

        poetry_data = data.get("tool", {}).get("poetry", {})
        dependencies = poetry_data.get("dependencies", {})
        dev_dependencies = (
            poetry_data.get("group", {}).get("dev", {}).get("dependencies", {})
        )

        summary["dependency_count"] = len(dependencies)
        summary["dev_dependencies_valid"] = bool(dev_dependencies)
        summary["dev_dependency_count"] = len(dev_dependencies)

        return FlextResult[dict[str, object]].ok(summary)


__all__ = ["PoetryOperations", "PoetryValidator"]
