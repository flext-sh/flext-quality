"""Command line interface for documentation maintenance."""

from __future__ import annotations

import importlib.util
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

if __package__ in {None, ""}:  # Support execution as a standalone script
    orchestrator_path = Path(__file__).resolve().with_name("orchestrator.py")
    spec = importlib.util.spec_from_file_location(
        "flext_quality.docs_maintenance.orchestrator", orchestrator_path
    )
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        msg = "Unable to load documentation orchestrator module"
        raise ImportError(msg)
    orchestrator_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = orchestrator_module
    spec.loader.exec_module(orchestrator_module)
    DEFAULT_PROFILE = orchestrator_module.DEFAULT_PROFILE
    DocumentationMaintenanceOrchestrator = (
        orchestrator_module.DocumentationMaintenanceOrchestrator
    )
else:
    from .orchestrator import DEFAULT_PROFILE, DocumentationMaintenanceOrchestrator


console = Console()
app = typer.Typer(help="Shared documentation maintenance commands")


@contextmanager
def _temporary_env(**variables: str | Path | None) -> Any:
    """Temporarily set environment variables for the maintenance run."""
    original: dict[str, str | None] = {}
    try:
        for name, value in variables.items():
            original[name] = os.environ.get(name)
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = str(value)
        yield
    finally:
        for name, value in original.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _render_summary(report: Any) -> None:
    """Render a high-level summary using rich tables."""
    summary = getattr(report, "summary", {}) or {}

    summary_table = Table(title="Maintenance Summary", box=None)
    summary_table.add_column("Metric", style="bold cyan")
    summary_table.add_column("Value", style="white")

    for key, value in summary.items():
        summary_table.add_row(key.replace("_", " ").title(), str(value))

    console.print(summary_table)

    operations = getattr(report, "operations_run", []) or []
    if not operations:
        return

    operations_table = Table(title="Operations", box=None)
    operations_table.add_column("Operation", style="bold green")
    operations_table.add_column("Status", style="bold")
    operations_table.add_column("Duration (s)", justify="right")

    for operation in operations:
        name = getattr(operation, "operation", "unknown")
        success = getattr(operation, "success", False)
        duration = getattr(operation, "duration", 0.0)
        status = "✅" if success else "❌"
        operations_table.add_row(name, status, f"{duration:.2f}")

    console.print(operations_table)


@app.command("comprehensive")
def run_comprehensive(
    project_root: Path = typer.Option(
        Path.cwd(),
        "--project-root",
        help="Path to the project root (defaults to current directory)",
        file_okay=False,
        resolve_path=True,
    ),
    profile: str = typer.Option(
        DEFAULT_PROFILE,
        "--profile",
        help="Maintenance profile slug to use",
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        help="Optional path to a maintenance configuration file",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Run without applying changes",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Show detailed logging in the terminal",
    ),
) -> None:
    """Execute the comprehensive maintenance workflow."""
    with _temporary_env(
        FLEXT_DOC_PROJECT_ROOT=project_root,
        FLEXT_DOC_PROFILE=profile,
    ):
        orchestrator = DocumentationMaintenanceOrchestrator(profile=profile)
        report = orchestrator.run(
            "comprehensive",
            config_path=str(config) if config else None,
            verbose=verbose,
            dry_run=dry_run,
        )

    console.print(
        f"[bold green]Documentation maintenance completed for[/] {project_root}"
    )
    _render_summary(report)


def main() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
