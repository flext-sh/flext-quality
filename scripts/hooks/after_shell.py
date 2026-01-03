#!/usr/bin/env python3
"""afterShellExecution hook - Processes shell command results after completion.

Allows monitoring and processing of shell command execution results.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase


class AfterShellHook(HookBase):
    """Hook for processing shell command results after completion."""

    def __init__(self: AfterShellHook) -> None:
        """Initialize after shell hook."""
        super().__init__("afterShellExecution")

    def run(self: AfterShellHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract shell result information
            command = input_data.get("command", "")
            output = input_data.get("output", "")
            duration = input_data.get("duration", 0)

            # Log shell execution for monitoring
            output_length = len(output)
            self.logger.info(
                f"Shell command completed: '{command[:50]}...' ({output_length} chars output, {duration}ms)"
            )

            # For now, just allow - can add result processing here
            self.write_output({})

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                None,  # No user message for after hooks
                f"Shell execution hook error: {e}",
            )


if __name__ == "__main__":
    hook = AfterShellHook()
    hook.run()
