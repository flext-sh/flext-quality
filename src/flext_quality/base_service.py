"""FlextQualityBaseService - Consolidates FlextService initialization pattern.

Eliminates duplication of logger, config, and container initialization
across multiple FlextService subclasses.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeVar

from flext_core import FlextContainer, FlextLogger, FlextService

from .config import FlextQualityConfig

T = TypeVar("T")


class FlextQualityBaseService(FlextService[T]):
    """Base class for all FLEXT Quality services.

    Consolidates repeated initialization patterns:
    - FlextLogger(__name__) instantiation
    - FlextQualityConfig initialization
    - FlextContainer.get_global() access

    Subclasses should:
    1. Call super().__init__() with optional config
    2. Use self._logger, self._config, self._container directly
    3. Implement execute() for FlextService contract
    """

    def __new__(
        cls,
        _config: FlextQualityConfig | None = None,
        **_data: object,
    ) -> FlextQualityBaseService[T]:
        """Create new service instance.

        Args:
            _config: Configuration (ignored in __new__, used in __init__).
            **_data: Additional keyword arguments.

        Returns:
            New service instance.

        """
        return super().__new__(cls)

    def __init__(
        self,
        config: FlextQualityConfig | None = None,
        **_data: object,
    ) -> None:
        """Initialize base service with standard pattern.

        Args:
            config: Optional quality configuration. Uses default if None.
            **_data: Additional keyword arguments (ignored).

        """
        super().__init__()
        self._logger = FlextLogger(__name__)
        # Use object.__setattr__ to bypass Pydantic's custom __setattr__ for private attributes
        object.__setattr__(
            self, "_config", config if config is not None else FlextQualityConfig()
        )
        object.__setattr__(self, "_container", FlextContainer.get_global())

    @property
    def logger(self) -> FlextLogger:
        """Access logger (read-only)."""
        return self._logger

    @property
    def config(self) -> FlextQualityConfig:
        """Access configuration (read-only)."""
        return self._config

    @property
    def container(self) -> FlextContainer:
        """Access container (read-only)."""
        return self._container
