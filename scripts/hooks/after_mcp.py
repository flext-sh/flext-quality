#!/usr/bin/env python3
"""afterMCPExecution hook - Processes MCP tool results after completion.

Allows monitoring and processing of MCP tool execution results.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase


class AfterMCPHook(HookBase):
    """Hook for processing MCP tool results after completion."""

    def __init__(self: AfterMCPHook) -> None:
        """Initialize after MCP hook."""
        super().__init__("afterMCPExecution")

    def run(self: AfterMCPHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract MCP result information
            tool_name = input_data.get("tool_name", "")
            duration = input_data.get("duration", 0)

            # Log MCP execution for monitoring
            self.logger.info(f"MCP tool {tool_name} completed in {duration}ms")

            # For now, just allow - can add result processing here
            self.write_output({})

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                None,  # No user message for after hooks
                f"MCP execution hook error: {e}",
            )


if __name__ == "__main__":
    hook = AfterMCPHook()
    hook.run()
