"""CLI service for flext-quality.

Provides FLEXT-integrated CLI service for quality operations.
Uses flext-cli for consistent output formatting.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from pathlib import Path
from typing import NoReturn, final

from flext_cli import FlextCliOutput
from flext_core import r

from flext_quality import FlextQuality, c
from flext_quality.integrations.code_execution import FlextQualityCodeExecutionBridge


@final
class FlextQualityCliService:
    """CLI service for flext-quality operations."""

    def __init__(self) -> None:
        """Initialize the CLI service."""
        self._output = FlextCliOutput()
        self._quality = FlextQuality.get_instance()
        self._executor = FlextQualityCodeExecutionBridge()

    def display_status(self) -> r[Mapping[str, object]]:
        """Display quality service status."""
        status = self._quality.get_status()
        return r[Mapping[str, object]].ok(status)

    def build_check_commands(self, target_path: Path) -> r[list[list[str]]]:
        """Build commands for quick check (lint + type)."""
        commands: list[list[str]] = []

        lint_result = self._executor.build_ruff_command(target_path)
        if lint_result.is_failure:
            return r[list[list[str]]].fail(lint_result.error)
        commands.append(lint_result.value)

        type_result = self._executor.build_basedpyright_command(target_path)
        if type_result.is_failure:
            return r[list[list[str]]].fail(type_result.error)
        commands.append(type_result.value)

        return r[list[list[str]]].ok(commands)

    def build_validate_commands(
        self,
        target_path: Path,
    ) -> r[list[list[str]]]:
        """Build commands for full validation."""
        commands: list[list[str]] = []

        lint_result = self._executor.build_ruff_command(target_path)
        if lint_result.is_failure:
            return r[list[list[str]]].fail(lint_result.error)
        commands.append(lint_result.value)

        type_result = self._executor.build_basedpyright_command(target_path)
        if type_result.is_failure:
            return r[list[list[str]]].fail(type_result.error)
        commands.append(type_result.value)

        src_path = (
            target_path / "src" if (target_path / "src").exists() else target_path
        )
        commands.append(["bandit", "-r", str(src_path), "-c", "pyproject.toml"])

        test_path = target_path / "tests"
        src_for_cov = target_path / "src"
        commands.extend([
            [
                "pytest",
                str(test_path),
                f"--cov={src_for_cov}",
                "--cov-report=term-missing",
            ],
            ["python", "-m", "coverage", "report"],
        ])

        return r[list[list[str]]].ok(commands)


class _CommandHandlers:
    """Command handlers for CLI operations."""

    @staticmethod
    def handle_status(service: FlextQualityCliService) -> r[int]:
        """Handle status command."""
        result = service.display_status()
        if result.is_failure:
            service._output.display_message(
                f"Status failed: {result.error}",
                message_type="error",
            )
            return r[int].ok(1)

        service._output.display_message("flext-quality status", message_type="success")
        service._output.display_message(
            f"Version: {c.Quality.Mcp.SERVER_VERSION}",
            message_type="info",
        )
        service._output.print_message(f"Version: {c.Quality.Mcp.SERVER_VERSION}")
        return r[int].ok(0)

    @staticmethod
    def handle_check(service: FlextQualityCliService, target_path: Path) -> r[int]:
        """Handle check command."""
        result = service.build_check_commands(target_path)
        if result.is_failure:
            service._output.display_message(
                f"Failed: {result.error}",
                message_type="error",
            )
            return r[int].ok(1)

        service._output.display_message(
            f"Running check on {target_path}...",
            message_type="info",
        )
        for cmd in result.value:
            service._output.display_message(f"  {' '.join(cmd)}", message_type="info")
        return r[int].ok(0)

    @staticmethod
    def handle_validate(
        service: FlextQualityCliService,
        target_path: Path,
    ) -> r[int]:
        """Handle validate command."""
        result = service.build_validate_commands(target_path)
        if result.is_failure:
            service._output.display_message(
                f"Failed: {result.error}",
                message_type="error",
            )
            return r[int].ok(1)

        service._output.display_message(
            f"Running validation on {target_path}...",
            message_type="info",
        )
        for cmd in result.value:
            service._output.display_message(f"  {' '.join(cmd)}", message_type="info")
        return r[int].ok(0)


def _dispatch(service: FlextQualityCliService, command: str, args: list[str]) -> int:
    """Dispatch command to handler."""
    if command == "status":
        result = _CommandHandlers.handle_status(service)
        return result.value if result.is_success else 1

    if command == "check":
        target_path = Path(args[0]) if args else Path.cwd()
        result = _CommandHandlers.handle_check(service, target_path)
        return result.value if result.is_success else 1

    if command == "validate":
        target_path = Path(args[0]) if args else Path.cwd()
        result = _CommandHandlers.handle_validate(service, target_path)
        return result.value if result.is_success else 1

    service._output.display_message(f"Unknown command: {command}", message_type="error")
    service._output.display_message(
        "Commands: status, check, validate",
        message_type="info",
    )
    service._output.print_message("Commands: status, check, validate")
    return 1


def main() -> NoReturn:
    """Main CLI entry point."""
    service = FlextQualityCliService()
    args = sys.argv[1:]

    if not args:
        result = _CommandHandlers.handle_status(service)
        sys.exit(result.value if result.is_success else 1)

    exit_code = _dispatch(service, args[0], args[1:])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
