#!/usr/bin/env python3
"""afterFileEdit hook - Validates files after editing.

Performs syntax checking, quality validation, and FLEXT standards compliance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_quality.hooks.base_hook import HookBase
from flext_quality.hooks.validation_engine import PreToolValidator


class AfterFileEditHook(HookBase):
    """Hook for validating files after editing."""

    def __init__(self: AfterFileEditHook) -> None:
        """Initialize after file edit hook."""
        super().__init__("afterFileEdit")
        self.validator = PreToolValidator()

    def run(self: AfterFileEditHook) -> None:
        """Execute hook logic."""
        try:
            # Read input from Cursor
            input_data = self.read_input()

            # Extract file information with proper type narrowing
            file_path_raw = input_data.get("file_path", "")
            file_path = str(file_path_raw) if file_path_raw else ""
            edits_raw = input_data.get("edits", [])
            edits = list(edits_raw) if isinstance(edits_raw, list) else []

            if not file_path:
                self.logger.warning("No file_path provided in afterFileEdit hook")
                return

            file_path_obj = Path(file_path)

            # Log edit information
            self.logger.info(f"File edited: {file_path} ({len(edits)} edits)")

            # Perform validations based on file type
            validation_errors: list[str] = []

            # Syntax validation for Python files
            if file_path.endswith(".py"):
                syntax_errors = self._validate_python_syntax(file_path_obj)
                validation_errors.extend(syntax_errors)

                # Code quality validation
                quality_errors = self._validate_code_quality(file_path_obj)
                validation_errors.extend(quality_errors)

            # File protection validation
            protection_errors = self._validate_file_protection(file_path_obj)
            validation_errors.extend(protection_errors)

            # Report any issues found
            if validation_errors:
                for error in validation_errors:
                    self.logger.warning(f"Validation issue in {file_path}: {error}")
            else:
                self.logger.info(f"All validations passed for {file_path}")

        except Exception as e:
            self.handle_error(f"Hook execution error: {e}")

    def _validate_python_syntax(self: AfterFileEditHook, file_path: Path) -> list[str]:
        """Validate Python file syntax.

        Args:
            file_path: Path to Python file

        Returns:
            List of syntax error messages

        """
        errors = []

        try:
            if not file_path.exists():
                return ["File does not exist"]

            content = file_path.read_text(encoding="utf-8")

            # Attempt to compile to check syntax
            _ = compile(content, str(file_path), "exec")

        except SyntaxError as e:
            error_msg = f"Syntax error: {e.msg} at line {e.lineno}"
            errors.append(error_msg)
            self.logger.exception("Python syntax error in %s: %s", file_path, error_msg)

        except UnicodeDecodeError as e:
            error_msg = f"Encoding error: {e}"
            errors.append(error_msg)
            self.logger.exception("Encoding error in %s: %s", file_path, error_msg)

        except Exception as e:
            error_msg = f"Error reading file: {e}"
            errors.append(error_msg)
            self.logger.exception("File read error for %s: %s", file_path, error_msg)

        return errors

    def _validate_code_quality(self: AfterFileEditHook, file_path: Path) -> list[str]:
        """Validate code quality using FLEXT Quality engine.

        Args:
            file_path: Path to file

        Returns:
            List of quality violation messages

        """
        errors = []

        try:
            # Use validation engine for file operations validation
            hook_input: dict[str, object] = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": str(file_path),
                },
            }

            validation_result = self.validator.validate(hook_input)
            if validation_result.is_success:
                violations = validation_result.unwrap()
                for violation in violations:
                    if violation.blocking:
                        error_msg = f"Quality: {violation.message}"
                        errors.append(error_msg)
                        self.logger.error(
                            f"Quality violation in {file_path}: {error_msg}"
                        )

        except Exception:
            self.logger.exception("Quality validation error for %s", file_path)

        return errors

    def _validate_file_protection(
        self: AfterFileEditHook, file_path: Path
    ) -> list[str]:
        """Validate file protection rules.

        Args:
            file_path: Path to file

        Returns:
            List of protection violation messages

        """
        errors = []

        # Check file operations validation
        hook_input: dict[str, object] = {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": str(file_path),
            },
        }

        validation_result = self.validator.validate(hook_input)

        if validation_result.is_success:
            violations = validation_result.unwrap()
            for violation in violations:
                if violation.blocking:
                    error_msg = f"Protection: {violation.message}"
                    errors.append(error_msg)
                    self.logger.warning(
                        f"File protection violation: {file_path} - {error_msg}"
                    )

        return errors


if __name__ == "__main__":
    hook = AfterFileEditHook()
    hook.run()
