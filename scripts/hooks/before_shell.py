#!/usr/bin/env python3
"""beforeShellExecution hook - Validates shell commands before execution.

Uses FLEXT Quality validation engine to check dangerous commands and patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase
from flext_quality.hooks.validation_engine import PreToolValidator


class BeforeShellHook(HookBase):
    """Hook for validating shell commands before execution."""

    def __init__(self: BeforeShellHook) -> None:
        """Initialize before shell hook."""
        super().__init__("beforeShellExecution")
        self.validator = PreToolValidator()

    def run(self: BeforeShellHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract command and context
            command = input_data.get("command", "")
            cwd = input_data.get("cwd", "")

            if not command:
                # Allow empty commands
                self.write_output({"permission": "allow"})
                return

            # Validate command using FLEXT Quality engine
            hook_input = {
                "tool_name": "Bash",
                "tool_input": {
                    "command": command,
                    "cwd": cwd,
                },
            }

            validation_result = self.validator.validate(hook_input)

            if validation_result.is_error():
                self.handle_error(
                    f"Validation error: {validation_result.unwrap_error()}",
                    "Erro interno na validação do comando",
                    "Command validation failed due to internal error",
                )
                return

            violations = validation_result.unwrap()

            if violations:
                # Found violations - deny execution
                violation = violations[0]  # Report first violation
                output = {
                    "permission": "deny",
                    "user_message": violation.message,
                    "agent_message": f"Command blocked: {violation.message}",
                }
                self.write_output(output)
                self.logger.warning(f"Blocked command: {command} - {violation.message}")
            else:
                # No violations - allow execution
                self.write_output({"permission": "allow"})
                self.logger.info(f"Allowed command: {command}")

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                "Erro interno no sistema de validação",
                f"Hook error: {e}",
            )


if __name__ == "__main__":
    hook = BeforeShellHook()
    hook.run()
