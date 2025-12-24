"""Color utilities mirroring the legacy flext_tools.colors API."""

from __future__ import annotations

from typing import Self

from flext import FlextLogger, FlextResult, FlextService


class FlextColorService(FlextService[str]):
    """Provide ANSI color helpers with FlextResult wrapping."""

    class Colors:
        """ANSI color codes used across the workspace."""

        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        WHITE = "\033[97m"
        GRAY = "\033[90m"
        ORANGE = "\033[38;5;208m"

        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"

        WARNING = YELLOW
        FAIL = RED
        HEADER = MAGENTA
        ENDC = RESET

    class _FormattingHelper:
        """Internal helper replicating the legacy interface."""

        @staticmethod
        def colorize(message: str, color: str) -> str:
            if not color:
                return message
            return f"{color}{message}{FlextColorService.Colors.RESET}"

    class _OutputHelper:
        """Simple print helper keeping compatibility with prior API."""

        @staticmethod
        def print_colored(message: str, color: str = "") -> None:
            # Reserved for future colored output implementation
            _ = message  # Reserved for future use
            if color:
                pass

    def __init__(self: Self) -> None:
        """Initialize color service."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[str]:
        """Return basic status message."""
        return FlextResult[str].ok("Color service ready")

    def colorize(self, message: str, color: str) -> FlextResult[str]:
        """Colorize text and wrap the result in FlextResult."""
        colored = self._FormattingHelper.colorize(message, color)
        return FlextResult[str].ok(colored)

    def print_colored(self, message: str, color: str = "") -> FlextResult[bool]:
        """Print a colored message."""
        self._OutputHelper.print_colored(message, color)
        return FlextResult[bool].ok(True)


Colors = FlextColorService.Colors


def colorize(message: str, color: str) -> str:
    """Convenience wrapper using FlextColorService."""
    service = FlextColorService()
    result = service.colorize(message, color)
    return result.value if result.is_success else message


def print_colored(message: str, color: str = "") -> None:
    """Convenience wrapper for colored printing."""
    FlextColorService().print_colored(message, color)


__all__ = ["Colors", "FlextColorService", "colorize", "print_colored"]
