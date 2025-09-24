"""Quality service dependency injection container using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextLogger


class FlextQualityContainer:
    """Unified quality container class following FLEXT architecture patterns.

    Single responsibility: Quality dependency injection management
    Contains all container functionality as nested classes with shared resources.
    """

    def __init__(self: object) -> None:
        """Initialize container with dependency injection."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    @staticmethod
    def get_quality_container() -> FlextContainer:
        """Get quality service container using flext-core patterns."""
        return FlextContainer.get_global()


# Backward compatibility alias for existing code
get_quality_container = FlextQualityContainer.get_quality_container
