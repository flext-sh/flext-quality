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
            self._logger = logging.getLogger(name)

        def info(self, message: str, **extra: object) -> None:
            self._logger.info(message, extra=extra)

        def warning(self, message: str, **extra: object) -> None:
            self._logger.warning(message, extra=extra)

        def error(self, message: str, **extra: object) -> None:
            self._logger.error(message, extra=extra)

    def __init__(self: Self) -> None:
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[None]:
        return FlextResult[None].ok(None)
