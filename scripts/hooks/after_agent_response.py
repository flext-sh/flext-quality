#!/usr/bin/env python3
"""afterAgentResponse hook - Processes agent responses after completion.

Allows monitoring and processing of agent responses for analytics and compliance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase


class AfterAgentResponseHook(HookBase):
    """Hook for processing agent responses after completion."""

    def __init__(self: AfterAgentResponseHook) -> None:
        """Initialize after agent response hook."""
        super().__init__("afterAgentResponse")

    def run(self: AfterAgentResponseHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract response information
            text = input_data.get("text", "")

            # Log response for monitoring
            response_length = len(text)
            self.logger.info(f"Agent response processed: {response_length} characters")

            # For now, just allow - can add compliance checks here
            self.write_output({})

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                None,  # No user message for after hooks
                f"Agent response hook error: {e}",
            )


if __name__ == "__main__":
    hook = AfterAgentResponseHook()
    hook.run()
