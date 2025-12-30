"""FLEXT Hook Models - Pydantic models for hook input/output.

Provides type-safe data structures for hook communication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HookInput(BaseModel):
    """Input data from Claude Code hooks.

    Attributes:
        tool_name: Name of the tool being called (e.g., 'Edit', 'Bash')
        tool_input: Tool input parameters as dict
        cwd: Current working directory (optional)

    """

    tool_name: str
    tool_input: dict[str, Any]
    cwd: str | None = None

    class Config:
        """Pydantic config."""

        extra = "allow"  # Allow extra fields for flexibility


class ViolationInfo(BaseModel):
    """Information about a validation violation.

    Attributes:
        code: Violation code (e.g., 'ANN401', 'E501')
        line: Line number where violation occurs
        message: Human-readable violation message
        file_path: Path to file with violation (optional)
        blocking: Whether violation blocks execution
        rule_code: Associated rule code from registry

    """

    code: str
    line: int
    message: str
    file_path: str | None = None
    blocking: bool = False
    rule_code: str | None = None


class ValidationResult(BaseModel):
    """Result of hook validation.

    Attributes:
        decision: Validation decision ('allow', 'warn', 'block')
        reason: Explanation for the decision
        exit_code: Shell exit code (0=allow, 1=warn, 2=block)
        violations: List of violations found

    """

    decision: str
    reason: str
    exit_code: int
    violations: list[ViolationInfo] = Field(default_factory=list)

    def is_allowed(self: ValidationResult) -> bool:
        """Check if execution is allowed.

        Returns:
            True if exit_code is 0 or 1 (allow or warn)

        """
        return self.exit_code in {0, 1}

    def is_blocked(self: ValidationResult) -> bool:
        """Check if execution is blocked.

        Returns:
            True if exit_code is 2 (block)

        """
        return self.exit_code == 2  # noqa: PLR2004

    def to_dict(self: ValidationResult) -> dict[str, Any]:
        """Convert to dictionary for JSON output.

        Returns:
            Dictionary representation of result

        """
        return self.model_dump()

    def to_json(self: ValidationResult) -> str:
        """Convert to JSON string.

        Returns:
            JSON representation of result

        """
        return self.model_dump_json()


class WorkspaceContext(BaseModel):
    """Context information about the workspace.

    Attributes:
        project_name: Name of the project (e.g., 'flext')
        project_path: Path to project root
        workspace_type: Type of workspace ('flext', 'invest', 'global')
        has_claude_md: Whether CLAUDE.md exists
        has_pyproject: Whether pyproject.toml exists
        has_git_repo: Whether .git directory exists
        python_version: Python version used

    """

    project_name: str
    project_path: str
    workspace_type: str
    has_claude_md: bool = False
    has_pyproject: bool = False
    has_git_repo: bool = False
    python_version: str | None = None

    class Config:
        """Pydantic config."""

        extra = "allow"


class HookOutput(BaseModel):
    """Output from a hook operation.

    Attributes:
        success: Whether operation succeeded
        decision: Hook decision ('allow', 'warn', 'block')
        message: Output message for user
        exit_code: Shell exit code
        violations: Violations found (if any)
        context: Workspace context (if available)

    """

    success: bool = True
    decision: str = "allow"
    message: str = ""
    exit_code: int = 0
    violations: list[ViolationInfo] = Field(default_factory=list)
    context: WorkspaceContext | None = None

    def to_dict(self: HookOutput) -> dict[str, Any]:
        """Convert to dictionary for JSON output.

        Returns:
            Dictionary representation

        """
        return self.model_dump(exclude_none=True)

    def to_json(self: HookOutput) -> str:
        """Convert to JSON string.

        Returns:
            JSON representation

        """
        return self.model_dump_json(exclude_none=True)


__all__ = [
    "HookInput",
    "HookOutput",
    "ValidationResult",
    "ViolationInfo",
    "WorkspaceContext",
]
