"""Refactoring cycle management for FLEXT projects.

This module provides tools for managing the massive refactoring cycle
across all FLEXT projects (1,811 files, 629K LOC).

Usage:
    from flext_quality.models import m
    status = m.Quality.Cycle.CycleStatus()

    from flext_quality.cycle import FlextQualityCycleServices
    manager = FlextQualityCycleServices.StatusManager()
"""

from __future__ import annotations

from .status_manager import FlextQualityCycleServices

__all__ = [
    "FlextQualityCycleServices",
]
