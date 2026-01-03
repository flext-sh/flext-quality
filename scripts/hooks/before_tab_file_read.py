#!/usr/bin/env python3
"""beforeTabFileRead hook - Controls file access for Tab completions.

Validates file access before Tab (inline completions) reads files.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_quality.hooks.base_hook import HookBase


class BeforeTabFileReadHook(HookBase):
    """Hook for controlling file access before Tab reads."""

    def __init__(self: BeforeTabFileReadHook) -> None:
        """Initialize before tab file read hook."""
        super().__init__("beforeTabFileRead")

        # Sensitive files that should be protected
        self.sensitive_files = {
            ".env",
            ".internal.invalid",
            ".env.production",
            ".env.development",
            "secrets.json",
            "credentials.json",
            "private.key",
            "id_rsa",
            ".git/config",
            ".ssh/config",
        }

    def run(self: BeforeTabFileReadHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract file information
            file_path = input_data.get("file_path", "")

            if not file_path:
                self.handle_error("No file_path provided in beforeTabFileRead hook")
                return

            path = Path(file_path)

            # Check for sensitive files
            if self._is_sensitive_file(path):
                output = {
                    "permission": "deny",
                    "user_message": f"Access denied: {path.name} contains sensitive information",
                    "agent_message": f"File access blocked: {file_path} contains sensitive data",
                }
                self.write_output(output)
                self.logger.warning(
                    f"Blocked Tab access to sensitive file: {file_path}"
                )
                return

            # Check if file exists
            if not path.exists():
                output = {
                    "permission": "deny",
                    "user_message": f"File not found: {file_path}",
                    "agent_message": f"Cannot read non-existent file: {file_path}",
                }
                self.write_output(output)
                self.logger.warning(
                    f"Tab attempted to read non-existent file: {file_path}"
                )
                return

            # Allow reading
            self.write_output({"permission": "allow"})
            self.logger.info(f"Allowed Tab read access to: {file_path}")

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                "Erro interno na validação de acesso a arquivos",
                f"Tab file access hook error: {e}",
            )

    def _is_sensitive_file(self: BeforeTabFileReadHook, path: Path) -> bool:
        """Check if file path contains sensitive information.

        Args:
            path: Path to check

        Returns:
            True if file should be protected

        """
        # Check exact filename matches
        if path.name in self.sensitive_files:
            return True

        # Check for patterns in path
        path_str = str(path)
        sensitive_patterns = [
            "/.git/",
            "/.ssh/",
            "/node_modules/",
            "/__pycache__/",
            "/.pytest_cache/",
            "/.mypy_cache/",
            "/dist/",
            "/build/",
        ]

        return any(pattern in path_str for pattern in sensitive_patterns)


if __name__ == "__main__":
    hook = BeforeTabFileReadHook()
    hook.run()
