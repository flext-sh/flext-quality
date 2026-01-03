#!/usr/bin/env python3
"""beforeMCPExecution hook - Validates MCP tool calls before execution.

Checks for dangerous MCP tool usage and security violations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase
from flext_quality.hooks.validation_engine import PreToolValidator


class BeforeMCPHook(HookBase):
    """Hook for validating MCP tool calls before execution."""

    def __init__(self: BeforeMCPHook) -> None:
        """Initialize before MCP hook."""
        super().__init__("beforeMCPExecution")
        self.validator = PreToolValidator()

    def run(self: BeforeMCPHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract MCP information
            tool_name = input_data.get("tool_name", "")
            tool_input = input_data.get("tool_input", {})

            # Extract server information if available
            server_url = input_data.get("url")
            server_command = input_data.get("command")

            if not tool_name:
                self.handle_error("No tool_name provided in MCP hook")
                return

            # Log MCP call attempt
            self.logger.info(f"MCP tool call: {tool_name} with input: {tool_input}")

            # Create hook input for validation
            hook_input = {
                "tool_name": tool_name,
                "tool_input": tool_input,
            }

            # Add server information if available
            if server_url:
                hook_input["url"] = server_url
            if server_command:
                hook_input["command"] = server_command

            # Validate MCP call
            validation_result = self.validator.validate(hook_input)

            if validation_result.is_error():
                self.handle_error(
                    f"MCP validation error: {validation_result.unwrap_error()}",
                    "Erro interno na validação da ferramenta MCP",
                    "MCP tool validation failed due to internal error",
                )
                return

            violations = validation_result.unwrap()

            if violations:
                # Found violations - deny execution
                violation = violations[0]  # Report first violation
                output = {
                    "permission": "deny",
                    "user_message": violation.message,
                    "agent_message": f"MCP tool blocked: {violation.message}",
                }
                self.write_output(output)
                self.logger.warning(
                    f"Blocked MCP tool: {tool_name} - {violation.message}"
                )
            else:
                # No violations - allow execution
                self.write_output({"permission": "allow"})
                self.logger.info(f"Allowed MCP tool: {tool_name}")

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                "Erro interno no sistema de validação MCP",
                f"MCP hook error: {e}",
            )


if __name__ == "__main__":
    hook = BeforeMCPHook()
    hook.run()
