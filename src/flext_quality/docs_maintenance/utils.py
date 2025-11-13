"""Utility helpers shared by the documentation maintenance modules."""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT_ENV = "FLEXT_DOC_PROJECT_ROOT"


def get_project_root(default: Path | None = None) -> Path:
    """Return the project root for documentation maintenance.

    The value is resolved using the ``FLEXT_DOC_PROJECT_ROOT`` environment variable,
    falling back to ``default`` or the current working directory.
    """
    env_value = os.environ.get(_PROJECT_ROOT_ENV)
    if env_value:
        return Path(env_value).resolve()
    if default is not None:
        return default.resolve()
    return Path.cwd().resolve()


def get_maintenance_dir(project_root: Path | None = None) -> Path:
    """Return the docs maintenance directory for the selected project."""
    root = get_project_root(project_root)
    return root / "docs" / "maintenance"


def get_docs_dir(project_root: Path | None = None) -> Path:
    """Return the project documentation directory."""
    return get_project_root(project_root) / "docs"


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_reports_dir(project_root: Path | None = None, *, create: bool = True) -> Path:
    """Return the reports directory, creating it if requested."""
    path = get_maintenance_dir(project_root) / "reports"
    return ensure_directory(path) if create else path


def get_backups_dir(project_root: Path | None = None, *, create: bool = True) -> Path:
    """Return the backups directory, creating it if requested."""
    path = get_maintenance_dir(project_root) / "backups"
    return ensure_directory(path) if create else path


def get_cache_dir(project_root: Path | None = None, *, create: bool = True) -> Path:
    """Return the cache directory, creating it if requested."""
    path = get_maintenance_dir(project_root) / ".cache"
    return ensure_directory(path) if create else path


def get_cache_file(
    filename: str, project_root: Path | None = None, *, create_dir: bool = True
) -> Path:
    """Return a cache file path within the maintenance cache directory."""
    directory = get_cache_dir(project_root, create=create_dir)
    return directory / filename


def get_config_path(
    filename: str, project_root: Path | None = None, *, ensure_exists: bool = False
) -> Path:
    """Return the path to a configuration file."""
    path = get_maintenance_dir(project_root) / "config" / filename
    if ensure_exists and not path.exists():
        msg = f"Configuration file not found: {path}"
        raise FileNotFoundError(msg)
    return path
