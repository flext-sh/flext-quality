"""Observability helpers migrated from flext_tools.observability."""

from __future__ import annotations

import logging
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService


class FlextObservabilityService(FlextService[None]):
    """Provide lightweight observability utilities."""

    class DetailedLogger:
        """Simple wrapper returning a structured logger."""

        def __init__(self, name: str) -> None:
            """Initialize detailed logger with name."""
            self._logger = logging.getLogger(name)

        def info(self, message: str, **extra: object) -> None:
            """Log info message with extra context."""
            self._logger.info(message, extra=extra)

        def warning(self, message: str, **extra: object) -> None:
            """Log warning message with extra context."""
            self._logger.warning(message, extra=extra)

        def error(self, message: str, **extra: object) -> None:
            """Log error message with extra context."""
            self._logger.error(message, extra=extra)

    def __init__(self: Self) -> None:
        """Initialize observability service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[None]:
        """Execute observability service."""
        return FlextResult[None].ok(None)
