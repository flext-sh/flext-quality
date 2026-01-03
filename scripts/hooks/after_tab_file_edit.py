#!/usr/bin/env python3
"""afterTabFileEdit hook - Processes Tab file edits after completion.

Allows monitoring and processing of Tab (inline completion) file edits.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.hooks.base_hook import HookBase


class AfterTabFileEditHook(HookBase):
    """Hook for processing Tab file edits after completion."""

    def __init__(self: AfterTabFileEditHook) -> None:
        """Initialize after tab file edit hook."""
        super().__init__("afterTabFileEdit")

    def run(self: AfterTabFileEditHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract Tab edit information
            file_path = input_data.get("file_path", "")
            edits = input_data.get("edits", [])

            # Log Tab edit for monitoring
            edit_count = len(edits)
            self.logger.info(
                f"Tab file edit processed: {file_path} ({edit_count} edits)"
            )

            # For now, just allow - can add edit processing here
            self.write_output({})

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                None,  # No user message for after hooks
                f"Tab file edit hook error: {e}",
            )


if __name__ == "__main__":
    hook = AfterTabFileEditHook()
    hook.run()
