"""FLEXT Quality Documentation Maintenance Package.

This package contains tools and utilities for maintaining documentation quality
across the FLEXT workspace, including auditing, validation, and reporting.
"""

from __future__ import annotations

from pathlib import Path

DOCS_PACKAGE_ROOT = Path(__file__).resolve().parent
DOCS_PROJECT_ROOT = DOCS_PACKAGE_ROOT.parents[2]
DOCS_CONFIG_DIR = DOCS_PACKAGE_ROOT / "config"
DOCS_REPORTS_DIR = DOCS_PACKAGE_ROOT / "reports"
DOCS_BACKUPS_DIR = DOCS_PACKAGE_ROOT / "backups"
DOCS_LOGS_DIR = DOCS_PACKAGE_ROOT / "logs"

__all__ = [
    "DOCS_BACKUPS_DIR",
    "DOCS_CONFIG_DIR",
    "DOCS_LOGS_DIR",
    "DOCS_PACKAGE_ROOT",
    "DOCS_PROJECT_ROOT",
    "DOCS_REPORTS_DIR",
]
