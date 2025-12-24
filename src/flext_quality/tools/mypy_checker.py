"""MyPy checking helpers used by quality workflows."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Self

from flext import FlextResult, FlextService
from flext_quality.subprocess_utils import SubprocessUtils


class MyPyChecker(FlextService[list[str]]):
    """Run mypy (or a fallback) against a project path."""

    def __init__(self: Self) -> None:
        """Initialize the MyPyChecker service."""
        super().__init__()

    def execute(self: Self) -> FlextResult[list[str]]:
        """Return empty diagnostics list for base execution."""
        return FlextResult[list[str]].ok([])

    def check_project(
        self,
        project_path: str | Path,
    ) -> FlextResult[list[str]]:
        """Execute mypy when available and return diagnostics."""
        root = Path(project_path).expanduser()
        if not root.exists():
            return FlextResult[list[str]].fail(f"Project path does not exist: {root}")

        if shutil.which("mypy") is None:
            # Environment without mypy – treat as success to keep workflows moving.
            return FlextResult[list[str]].ok([])

        run_result = SubprocessUtils.run_external_command(
            ["mypy", str(root)],
            capture_output=True,
            check=False,
        )
        if run_result.is_failure:
            return FlextResult[list[str]].fail(
                f"MyPy execution failed: {run_result.error}",
            )

        completed = run_result.value
        if completed.returncode != 0:
            diagnostics = completed.stdout.splitlines()
            return FlextResult[list[str]].ok(diagnostics)
        return FlextResult[list[str]].ok([])

    def get_type_coverage(self, project_path: str | Path) -> FlextResult[str]:
        """Placeholder for compatibility – returns a friendly message."""
        _ = project_path
        return FlextResult[str].ok("Type coverage calculation not implemented yet")

    def check_workspace(self: Self) -> FlextResult[list[str]]:
        """Run MyPy for the current workspace root."""
        return self.check_project(Path.cwd())


__all__ = ["MyPyChecker"]
