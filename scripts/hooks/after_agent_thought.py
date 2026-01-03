#!/usr/bin/env python3
"""afterAgentThought hook - Processes agent thoughts for monitoring.

Allows monitoring of agent reasoning process for analytics.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase


class AfterAgentThoughtHook(HookBase):
    """Hook for processing agent thoughts after completion."""

    def __init__(self: AfterAgentThoughtHook) -> None:
        """Initialize after agent thought hook."""
        super().__init__("afterAgentThought")

    def run(self: AfterAgentThoughtHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract thought information
            text = input_data.get("text", "")
            duration_ms = input_data.get("duration_ms", 0)

            # Log thought for monitoring
            thought_length = len(text)
            self.logger.info(
                f"Agent thought processed: {thought_length} chars, {duration_ms}ms"
            )

            # No output expected for thought processing
            self.write_output({})

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                None,  # No user message for after hooks
                f"Agent thought hook error: {e}",
            )


if __name__ == "__main__":
    hook = AfterAgentThoughtHook()
    hook.run()
