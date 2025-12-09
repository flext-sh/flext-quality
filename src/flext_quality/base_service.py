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
    2. Use self.quality_config, self.quality_container, self.logger directly
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
        # Store quality-specific instances with unique names (avoid overriding parent attributes)
        object.__setattr__(self, "_quality_logger", FlextLogger(__name__))
        object.__setattr__(
            self,
            "_quality_config",
            config if config is not None else FlextQualityConfig(),
        )
        object.__setattr__(self, "_quality_container", FlextContainer.get_global())

    @property
    def quality_logger(self) -> FlextLogger:
        """Access quality logger (read-only)."""
        return self._quality_logger  # type: ignore[attr-defined]

    @property
    def quality_config(self) -> FlextQualityConfig:
        """Access quality configuration (read-only)."""
        return self._quality_config  # type: ignore[attr-defined]

    @property
    def quality_container(self) -> FlextContainer:
        """Access quality container (read-only)."""
        return self._quality_container  # type: ignore[attr-defined]
