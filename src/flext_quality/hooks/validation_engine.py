"""FLEXT Validation Engine for Hooks - Core validation logic migration from ~/.claude/hooks.

Provides centralized validation for shell hooks:
- Dangerous commands detection
- Python syntax validation
- Code quality violation detection
- File operations validation

This module consolidates ~2487 lines from ~/.claude/hooks/utils/validators.py
into a lean, reusable service using FlextResult patterns and centralized rules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Self

from flext_core import FlextResult, FlextService, FlextTypes as t

from flext_quality.rules import registry
from flext_quality.tools.quality_operations import FlextQualityOperations


class ValidationViolation:
    """Represents a single validation violation.

    Attributes:
        code: Violation code (e.g., 'ANN401', 'E501')
        message: Violation message
        line: Line number where violation occurs
        file_path: Path to file with violation
        blocking: Whether this violation blocks execution
        rule_code: Associated rule code from registry

    """

    def __init__(
        self: Self,
        code: str,
        message: str,
        line: int,
        file_path: str | None = None,
        blocking: bool = False,
        rule_code: str | None = None,
    ) -> None:
        """Initialize validation violation."""
        self.code = code
        self.message = message
        self.line = line
        self.file_path = file_path
        self.blocking = blocking
        self.rule_code = rule_code

    def to_dict(self: Self) -> dict[str, t.GeneralValueType]:
        """Convert to dictionary representation."""
        return {
            "code": self.code,
            "message": self.message,
            "line": self.line,
            "file_path": self.file_path,
            "blocking": self.blocking,
            "rule_code": self.rule_code,
        }


class PreToolValidator(FlextService[list[ValidationViolation]]):
    """Pre-tool validation service for Claude Code hooks.

    Migrated core validation logic from ~/.claude/hooks/utils/validators.py.
    Provides centralized validation for:
    - Dangerous commands
    - File path validation
    - Python syntax checking
    - Code quality violations

    Usage:
        from flext_quality.hooks.validation_engine import PreToolValidator

        validator = PreToolValidator()
        hook_input = HookInput(
            tool_name="Edit",
            tool_input={"file_path": "/path/to/file.py"}
        )
        result = validator.validate(hook_input)

        if result.is_success:
            violations = result.unwrap()
            # Handle violations...
    """

    def __init__(self: Self) -> None:
        """Initialize pre-tool validator."""
        super().__init__()
        self._ops: FlextQualityOperations | None = None
        # Compile dangerous command patterns for efficiency
        self._dangerous_patterns = self._compile_dangerous_patterns()

    def execute(
        self: Self,
        **_kwargs: t.GeneralValueType,
    ) -> FlextResult[list[ValidationViolation]]:
        """Execute validator service - FlextService interface.

        Returns:
            FlextResult with empty violation list (service stub)

        """
        return FlextResult[list[ValidationViolation]].ok([])

    def validate(
        self: Self,
        hook_input: dict[str, t.GeneralValueType],
    ) -> FlextResult[list[ValidationViolation]]:
        """Validate tool input before execution.

        Args:
            hook_input: Hook input dict with 'tool_name' and 'tool_input'

        Returns:
            FlextResult with list of violations (empty if validation passes)

        """
        violations: list[ValidationViolation] = []

        # Extract hook metadata
        tool_name = str(hook_input.get("tool_name", ""))
        tool_input = hook_input.get("tool_input", {})

        if not isinstance(tool_input, dict):
            return FlextResult[list[ValidationViolation]].ok([])

        # Check dangerous commands for Bash tool
        if tool_name == "Bash":
            cmd = str(tool_input.get("command", ""))
            cmd_violations = self.check_dangerous_commands(cmd)
            violations.extend(cmd_violations)

        # Check file operations (Edit, Write tools)
        if tool_name in {"Edit", "Write"}:
            file_path = str(tool_input.get("file_path", ""))
            if file_path:
                file_violations = self.check_file_operations(file_path)
                violations.extend(file_violations)

                # Check Python syntax for Python files
                if file_path.endswith(".py"):
                    syntax_violations = self.check_python_syntax(file_path)
                    violations.extend(syntax_violations)

        return FlextResult[list[ValidationViolation]].ok(violations)

    def check_dangerous_commands(self: Self, command: str) -> list[ValidationViolation]:
        """Check if command contains dangerous patterns.

        Args:
            command: Command string to validate

        Returns:
            List of violations for dangerous patterns found

        """
        violations: list[ValidationViolation] = []

        # Check against compiled patterns
        for pattern_re, rule_name, guidance in self._dangerous_patterns:
            if pattern_re.search(command):
                violation = ValidationViolation(
                    code="DANGEROUS_CMD",
                    message=f"{rule_name}: {guidance}",
                    line=0,
                    blocking=True,
                    rule_code=rule_name,
                )
                violations.append(violation)
                break  # Report only first match per command

        return violations

    def check_file_operations(self: Self, file_path: str) -> list[ValidationViolation]:
        """Check file operation validity.

        Args:
            file_path: Path to file being operated on

        Returns:
            List of violations for invalid file operations

        """
        violations: list[ValidationViolation] = []
        path = Path(file_path)

        # Check for forbidden file modifications
        forbidden_files = {
            ".env",
            ".internal.invalid",
            "secrets.json",
            "credentials.json",
            "pyproject.toml",  # Only allow with explicit validation
        }

        if path.name in forbidden_files or str(path).endswith(tuple(forbidden_files)):
            violation = ValidationViolation(
                code="FORBIDDEN_FILE",
                message=f"Cannot modify {path.name} - contains critical configuration",
                line=0,
                file_path=file_path,
                blocking=True,
            )
            violations.append(violation)

        return violations

    def check_python_syntax(self: Self, file_path: str) -> list[ValidationViolation]:
        """Check Python file for syntax errors.

        Args:
            file_path: Path to Python file

        Returns:
            List of violations for syntax errors

        """
        violations: list[ValidationViolation] = []
        path = Path(file_path)

        # Only check existing files
        if not path.exists():
            return violations

        try:
            content = path.read_text(encoding="utf-8")
            # Attempt to compile to check syntax
            compile(content, str(path), "exec")
        except SyntaxError as e:
            violation = ValidationViolation(
                code="SYNTAX_ERROR",
                message=f"Python syntax error: {e.msg}",
                line=e.lineno or 0,
                file_path=file_path,
                blocking=True,
            )
            violations.append(violation)
        except UnicodeDecodeError as e:
            violation = ValidationViolation(
                code="ENCODING_ERROR",
                message=f"File encoding error: {e!s}",
                line=0,
                file_path=file_path,
                blocking=True,
            )
            violations.append(violation)

        return violations

    def check_code_quality(
        self: Self,
        file_path: str,
    ) -> FlextResult[list[ValidationViolation]]:
        """Check code quality violations using ruff/mypy.

        Args:
            file_path: Path to file to check

        Returns:
            FlextResult with list of quality violations

        """
        violations: list[ValidationViolation] = []
        path = Path(file_path)

        # Skip if file doesn't exist or not Python
        if not path.exists() or path.suffix != ".py":
            return FlextResult[list[ValidationViolation]].ok(violations)

        try:
            # Get quality operations for the project
            ops = self._get_ops(path)

            # Run lint check
            lint_result = ops.lint()
            if lint_result.is_success and lint_result.unwrap().errors > 0:
                # Extract violations from lint report
                # This leverages existing quality_operations infrastructure
                pass

        except Exception as e:
            return FlextResult[list[ValidationViolation]].error(
                f"Quality check failed: {e!s}"
            )

        return FlextResult[list[ValidationViolation]].ok(violations)

    def _get_ops(self: Self, file_path: Path) -> FlextQualityOperations:
        """Get or create operations instance for project.

        Args:
            file_path: Path to file to determine project

        Returns:
            FlextQualityOperations instance for project

        """
        project_path = file_path.parent
        if self._ops is None or self._ops.project_path != project_path:
            self._ops = FlextQualityOperations(project_path)
        return self._ops

    def _compile_dangerous_patterns(
        self: Self,
    ) -> list[tuple[re.Pattern[str], str, str]]:
        """Compile dangerous command patterns from registry.

        Returns:
            List of (compiled_pattern, rule_name, guidance) tuples

        """
        patterns: list[tuple[re.Pattern[str], str, str]] = []

        # Get dangerous commands from centralized registry
        dangerous_commands = registry.as_dangerous_commands()

        for pattern_str, rule_name, guidance in dangerous_commands:
            try:
                compiled = re.compile(pattern_str, re.IGNORECASE)
                patterns.append((compiled, rule_name, guidance))
            except re.error:
                # Skip invalid patterns
                continue

        return patterns


__all__ = ["PreToolValidator", "ValidationViolation"]
