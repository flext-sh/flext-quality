"""FlextQuality tools utilities for path operations, colors, and stdlib detection.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Migrated from flext_tools.utilities and adapted for flext-quality.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import ClassVar, Self

from flext_cli import FlextCli
from flext_core import FlextLogger, FlextResult, FlextService


class FlextQualityToolsUtilities(FlextService[None]):
    """Unified utilities with complete flext-core integration.

    Consolidates:
    - Terminal colors (ANSI codes and colored output)
    - Path operations (navigation, normalization, file finding)
    - Standard library detection (module identification)

    MANDATORY: Uses flext-cli for ALL terminal output (NO direct rich/click).
    """

    class Colors:
        """Terminal colors using flext-cli (MANDATORY - NO direct rich)."""

        # ANSI color codes
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        WHITE = "\033[97m"
        GRAY = "\033[90m"
        ORANGE = "\033[38;5;208m"

        # Formatting
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RESET = "\033[0m"

        # Semantic aliases
        WARNING = YELLOW
        FAIL = RED
        HEADER = MAGENTA
        ENDC = RESET

        @staticmethod
        def colorize(message: str, color: str) -> str:
            """Colorize text with ANSI color codes.

            Args:
                message: Text to colorize
                color: ANSI color code

            Returns:
                Colorized text with reset at end

            """
            if not color:
                return message
            return f"{color}{message}{FlextQualityToolsUtilities.Colors.RESET}"

        @staticmethod
        def print_colored(
            message: str,
            color: str = "",
            logger: FlextLogger | None = None,
        ) -> FlextResult[None]:
            """Print text with color formatting using flext-cli.

            MANDATORY: Uses FlextCli for output (NO direct rich/click).

            Args:
                message: Text to print
                color: ANSI color code (optional)
                logger: Optional logger for parallel logging

            Returns:
                FlextResult indicating success/failure of print operation

            """
            if logger:
                logger.info(message)

            try:
                cli = FlextCli()
                if color:
                    colored_msg = FlextQualityToolsUtilities.Colors.colorize(
                        message, color
                    )
                    cli.console.print(colored_msg)
                else:
                    cli.console.print(message)
                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"CLI output failed: {e}")

    class Paths:
        """Path utilities for workspace navigation and file operations."""

        # Ignore patterns (common directories/files to skip)
        IGNORE_PATTERNS: ClassVar[list[str]] = [
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
        ]

        @staticmethod
        def should_ignore_path(path: str | Path) -> bool:
            """Check if path should be ignored based on common patterns.

            Args:
                path: Path to check

            Returns:
                True if path matches ignore patterns

            """
            path_str = str(path)
            return any(
                pattern in path_str
                for pattern in FlextQualityToolsUtilities.Paths.IGNORE_PATTERNS
            )

        @staticmethod
        def get_project_root() -> Path:
            """Get project root directory (current working directory).

            Returns:
                Path to project root

            """
            return Path.cwd()

        @staticmethod
        def normalize_path(path: str | Path) -> Path:
            """Normalize path to absolute resolved path.

            Args:
                path: Path to normalize

            Returns:
                Absolute resolved Path

            """
            return Path(path).resolve()

        @staticmethod
        def resolve_path(path: str | Path) -> Path:
            """Resolve path to absolute path (alias for normalize_path).

            Args:
                path: Path to resolve

            Returns:
                Absolute resolved Path

            """
            return Path(path).resolve()

        @staticmethod
        def find_python_files(
            root: str | Path,
            exclude_patterns: list[str] | None = None,
        ) -> list[Path]:
            """Find all Python files in directory tree.

            Args:
                root: Root directory to search
                exclude_patterns: Optional list of patterns to exclude

            Returns:
                Sorted list of Python file paths

            """
            root_path = Path(root)
            exclude = (
                exclude_patterns or FlextQualityToolsUtilities.Paths.IGNORE_PATTERNS
            )

            python_files: list[Path] = [
                py_file
                for py_file in root_path.rglob("*.py")
                if not any(pattern in str(py_file) for pattern in exclude)
            ]

            return sorted(python_files)

    class Stdlib:
        """Standard library module detection."""

        @staticmethod
        def get_stdlib_modules() -> list[str]:
            """Get list of Python standard library modules.

            Returns:
                Sorted list of stdlib module names

            """
            stdlib_modules = [
                "os",
                "sys",
                "re",
                "json",
                "urllib",
                "http",
                "pathlib",
                "collections",
                "itertools",
                "functools",
                "typing",
                "datetime",
                "argparse",
                "subprocess",
                "shutil",
                "glob",
                "tempfile",
                "ast",
                "asyncio",
                "contextlib",
                "dataclasses",
                "enum",
                "importlib",
                "logging",
                "pickle",
                "socket",
                "threading",
                "time",
                "uuid",
            ]

            # Add Python 3.13+ stdlib modules
            if hasattr(sys, "stdlib_module_names"):
                stdlib_modules.extend(list(sys.stdlib_module_names))

            return sorted(set(stdlib_modules))

        @staticmethod
        def is_stdlib_module(module_name: str) -> bool:
            """Check if module is from standard library.

            Args:
                module_name: Module name to check (e.g., 'os.path')

            Returns:
                True if module is from stdlib

            """
            # Extract base module name (before first dot)
            base_module = module_name.split(".", maxsplit=1)[0]
            return base_module in FlextQualityToolsUtilities.Stdlib.get_stdlib_modules()

    def __init__(self: Self) -> None:
        """Initialize utilities service."""
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._cli = FlextCli()  # MANDATORY: Use flext-cli

    def execute(self: Self) -> FlextResult[None]:
        """Execute utilities service - FlextService interface.

        Returns:
            FlextResult indicating service execution success

        """
        return FlextResult[None].ok(None)


# Backward compatibility aliases (for existing code)
Colors = FlextQualityToolsUtilities.Colors


def colorize(message: str, color: str) -> str:
    """Convenience function for colorize.

    Args:
        message: Text to colorize
        color: ANSI color code

    Returns:
        Colorized text

    """
    return FlextQualityToolsUtilities.Colors.colorize(message, color)


def print_colored(message: str, color: str = "") -> None:
    """Convenience function for print_colored.

    Args:
        message: Text to print
        color: ANSI color code (optional)

    """
    FlextQualityToolsUtilities.Colors.print_colored(message, color)


def get_project_root() -> Path:
    """Convenience function for get_project_root.

    Returns:
        Path to project root

    """
    return FlextQualityToolsUtilities.Paths.get_project_root()


def normalize_path(path: str | Path) -> Path:
    """Convenience function for normalize_path.

    Args:
        path: Path to normalize

    Returns:
        Absolute resolved Path

    """
    return FlextQualityToolsUtilities.Paths.normalize_path(path)


def should_ignore_path(path: str | Path) -> bool:
    """Convenience function for should_ignore_path.

    Args:
        path: Path to check

    Returns:
        True if path should be ignored

    """
    return FlextQualityToolsUtilities.Paths.should_ignore_path(path)


def get_stdlib_modules() -> list[str]:
    """Convenience function for get_stdlib_modules.

    Returns:
        List of stdlib module names

    """
    return FlextQualityToolsUtilities.Stdlib.get_stdlib_modules()


def is_stdlib_module(module_name: str) -> bool:
    """Convenience function for is_stdlib_module.

    Args:
        module_name: Module name to check

    Returns:
        True if module is from stdlib

    """
    return FlextQualityToolsUtilities.Stdlib.is_stdlib_module(module_name)


__all__ = [
    "Colors",
    "FlextQualityToolsUtilities",
    "colorize",
    "get_project_root",
    "get_stdlib_modules",
    "is_stdlib_module",
    "normalize_path",
    "print_colored",
    "should_ignore_path",
]
