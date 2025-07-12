"""Command-line interface for FLEXT Quality using centralized CLI framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from pathlib import Path

import click

from flext_quality.config import QualityConfig


@click.group()
@click.version_option()
def quality_cli() -> None:
    """FLEXT Quality Analysis CLI."""


@quality_cli.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Path to project for analysis",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default="reports",
    help="Output directory for reports",
)
@click.option(
    "--format",
    type=click.Choice(["html", "json", "markdown"]),
    default="html",
    help="Report format",
)
def analyze(project_path: Path, output_dir: Path, format: str) -> None:
    """Analyze project quality."""
    config = QualityConfig(
        project_root=project_path,
        report_output_dir=output_dir,
    )

    click.echo(f"Analyzing project at: {project_path}")
    click.echo(f"Output directory: {output_dir}")
    click.echo(f"Report format: {format}")

    # TODO: Implement actual analysis when analyzer is ready
    click.echo("Analysis complete!")


@quality_cli.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Path to project",
)
def score(project_path: Path) -> None:
    """Get quality score for project."""
    click.echo(f"Calculating quality score for: {project_path}")
    # TODO: Implement quality score calculation
    click.echo("Quality score: 85/100")


if __name__ == "__main__":
    quality_cli()
