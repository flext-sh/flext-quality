"""FlextQualityBaseService - Consolidates FlextService initialization pattern.

Eliminates duplication of logger, config, and container initialization
across multiple FlextService subclasses.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeVar

from flext_core import FlextContainer, FlextLogger, FlextService

from .settings import FlextQualitySettings

T = TypeVar("T")


class FlextQualityBaseService(FlextService[T]):
    """Base class for all FLEXT Quality services.

    Consolidates repeated initialization patterns:
    - FlextLogger(__name__) instantiation
    - FlextQualitySettings initialization
    - FlextContainer.get_global() access

    Subclasses should:
    1. Call super().__init__() with optional config
    2. Use self.quality_config, self.quality_container, self.logger directly
    3. Implement execute() for FlextService contract
    """

    # Type hints for private attributes
    _quality_logger: FlextLogger
    _quality_config: FlextQualitySettings
    _quality_container: FlextContainer

    def __new__(
        cls,
        _config: FlextQualitySettings | None = None,
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
        config: FlextQualitySettings | None = None,
        **_data: object,
    ) -> None:
        """Initialize base service with standard pattern.

        Args:
            config: Optional quality configuration. Uses default if None.
            **_data: Additional keyword arguments (ignored).

        """
        super().__init__()
        # Store quality-specific instances with unique names (avoid overriding parent attributes)
        object.__setattr__(self, "_quality_logger", FlextLogger(__name__))
        object.__setattr__(
            self,
            "_quality_config",
            config if config is not None else FlextQualitySettings(),
        )
        object.__setattr__(self, "_quality_container", FlextContainer.get_global())

    @property
    def quality_logger(self) -> FlextLogger:
        """Access quality logger (read-only)."""
        return self._quality_logger

    @property
    def quality_config(self) -> FlextQualitySettings:
        """Access quality configuration (read-only)."""
        return self._quality_config

    @property
    def quality_container(self) -> FlextContainer:
        """Access quality container (read-only)."""
        return self._quality_container
