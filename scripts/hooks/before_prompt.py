#!/usr/bin/env python3
"""beforeSubmitPrompt hook - Validates prompts before submission.

Checks for dangerous content and security violations in user prompts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re

from flext_quality.hooks.base_hook import HookBase


class BeforePromptHook(HookBase):
    """Hook for validating prompts before submission."""

    def __init__(self: BeforePromptHook) -> None:
        """Initialize before prompt hook."""
        super().__init__("beforeSubmitPrompt")

        # Dangerous prompt patterns
        self.dangerous_patterns = [
            (
                re.compile(
                    r"\b(jailbreak|override.*instruction|ignore.*rule)\b", re.IGNORECASE
                ),
                "Jailbreak attempt detected",
            ),
            (
                re.compile(
                    r"\b(system.*prompt|internal.*instruction)\b", re.IGNORECASE
                ),
                "Attempt to access system prompts",
            ),
            (
                re.compile(r"\b(ignore.*safety|disable.*security)\b", re.IGNORECASE),
                "Attempt to disable safety measures",
            ),
            (
                re.compile(
                    r"\b(malicious|hack|exploit|attack)\b.*\b(system|network|server)\b",
                    re.IGNORECASE,
                ),
                "Potentially malicious intent detected",
            ),
        ]

    def run(self: BeforePromptHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract prompt and attachments
            prompt = input_data.get("prompt", "")
            attachments = input_data.get("attachments", [])

            if not prompt.strip():
                # Allow empty prompts
                self.write_output({"continue": True})
                return

            # Check for dangerous content
            violation = self._check_dangerous_content(prompt)

            if violation:
                # Block dangerous prompt
                output = {
                    "continue": False,
                    "user_message": f"🚫 Prompt bloqueado: {violation}",
                }
                self.write_output(output)
                self.logger.warning(f"Blocked dangerous prompt: {violation}")
            else:
                # Check attachments if any
                attachment_violation = self._check_attachments(attachments)
                if attachment_violation:
                    output = {
                        "continue": False,
                        "user_message": f"🚫 Anexo bloqueado: {attachment_violation}",
                    }
                    self.write_output(output)
                    self.logger.warning(
                        f"Blocked dangerous attachment: {attachment_violation}"
                    )
                else:
                    # Allow safe prompt
                    self.write_output({"continue": True})
                    self.logger.info("Prompt validation passed")

        except Exception as e:
            self.handle_error(
                f"Hook execution error: {e}",
                "Erro interno na validação do prompt",
                f"Prompt hook error: {e}",
            )

    def _check_dangerous_content(self: BeforePromptHook, prompt: str) -> str | None:
        """Check prompt for dangerous content.

        Args:
            prompt: User prompt text

        Returns:
            Violation message if dangerous content found, None otherwise

        """
        for pattern, message in self.dangerous_patterns:
            if pattern.search(prompt):
                return message

        return None

    def _check_attachments(
        self: BeforePromptHook, attachments: list[dict]
    ) -> str | None:
        """Check attachments for security issues.

        Args:
            attachments: List of attachment dictionaries

        Returns:
            Violation message if problematic attachment found, None otherwise

        """
        dangerous_extensions = {
            ".exe",
            ".bat",
            ".cmd",
            ".scr",
            ".pif",
            ".com",
            ".vbs",
            ".js",
            ".jar",
            ".msi",
            ".deb",
            ".rpm",
        }

        for attachment in attachments:
            file_path = attachment.get("filePath", "")
            if not file_path:
                continue

            # Check file extension
            file_path_lower = file_path.lower()
            for ext in dangerous_extensions:
                if file_path_lower.endswith(ext):
                    return f"Arquivos executáveis não são permitidos: {ext}"

        return None


if __name__ == "__main__":
    hook = BeforePromptHook()
    hook.run()
