"""Quality service dependency injection container using flext-core patterns."""

from __future__ import annotations

from flext_core import FlextContainer


def get_quality_container() -> FlextContainer:
    """Get quality service container using flext-core patterns."""
    return FlextContainer.get_global()

    # Register quality-specific services here if needed
    # container.register("quality_service", QualityService())
