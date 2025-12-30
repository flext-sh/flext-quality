"""Validation rule models for centralized rule system.

This module defines Pydantic models for validation rules that can be loaded
from YAML files and used by all validators in the FLEXT ecosystem.

Models:
    - ValidationRule: Immutable rule definition with pattern, severity, guidance
    - RuleViolation: Detected violation with line number and context
    - RuleCategory: Enum for rule categories (bash, python, architecture, etc.)
    - RuleSeverity: Enum for violation severity (critical, high, medium, low)
"""

from __future__ import annotations

import re
from enum import StrEnum
from fnmatch import fnmatch
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RuleCategory(StrEnum):
    """Category of validation rule.

    Categories are organized by:
    - Language-specific: PYTHON_CODE, TYPESCRIPT_CODE, JAVASCRIPT_CODE, GO_CODE, RUST_CODE
    - Domain-specific: BASH_COMMAND, TYPE_SYSTEM, ARCHITECTURE, FILE_PROTECTION
    - Configuration: YAML_QUALITY, JSON_QUALITY
    """

    # Language-specific categories
    BASH_COMMAND = "bash_command"
    PYTHON_CODE = "python_code"
    TYPESCRIPT_CODE = "typescript_code"
    JAVASCRIPT_CODE = "javascript_code"
    GO_CODE = "go_code"
    RUST_CODE = "rust_code"

    # Domain-specific categories
    TYPE_SYSTEM = "type_system"
    ARCHITECTURE = "architecture"
    FILE_PROTECTION = "file_protection"

    # Configuration file categories
    YAML_QUALITY = "yaml_quality"
    JSON_QUALITY = "json_quality"


class RuleSeverity(StrEnum):
    """Severity level of rule violation."""

    CRITICAL = "critical"  # Always blocks execution
    HIGH = "high"  # Blocks in hooks, warns elsewhere
    MEDIUM = "medium"  # Warning only
    LOW = "low"  # Informational


class ValidationRule(BaseModel):
    r"""Immutable validation rule definition with multi-language support.

    Attributes:
        code: Unique rule identifier (e.g., DC001, TV003)
        name: Short human-readable name
        pattern: Default regex pattern to match violations
        patterns: Language-specific patterns (language → pattern mapping)
        language: Target programming language (python, typescript, go, etc.)
        file_types: File extensions this rule applies to (e.g., ".py", ".ts")
        category: Rule category for filtering
        severity: Violation severity level
        guidance: Educational message for fixing the violation
        applies_to: File patterns where rule applies (empty = all files)
        exceptions: File patterns to exclude from matching
        blocking: Whether violation blocks execution
        context_required: Required context for rule to apply (e.g., FLEXT_PROJECT)
        tags: Tags for filtering and grouping

    Example:
        >>> rule = ValidationRule(
        ...     code="DC001",
        ...     name="rm -rf",
        ...     pattern=r"rm\s+-rf?\s+",
        ...     category=RuleCategory.BASH_COMMAND,
        ...     severity=RuleSeverity.CRITICAL,
        ...     guidance="Use 'mv file file.bak' instead",
        ...     blocking=True,
        ...     tags=frozenset({"destructive", "file-deletion"}),
        ... )

        >>> # Multi-language rule example
        >>> rule = ValidationRule(
        ...     code="TS001",
        ...     name="missing-return-type",
        ...     pattern=r"function\s+\w+\s*\([^)]*\)\s*\{",
        ...     language="typescript",
        ...     file_types=(".ts", ".tsx"),
        ...     category=RuleCategory.TYPESCRIPT_CODE,
        ...     severity=RuleSeverity.HIGH,
        ...     guidance="Add explicit return type annotation",
        ... )

    """

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    # Identity
    code: str = Field(..., pattern=r"^[A-Z]{2}\d{3}$")
    name: str = Field(..., min_length=1, max_length=100)

    # Pattern (backward compatible - single pattern or language-specific patterns)
    pattern: str = Field(..., min_length=1)
    patterns: dict[str, str] = Field(default_factory=dict)  # language → pattern

    # Multi-language support
    language: str | None = Field(default=None)  # Target language (python, typescript, etc.)
    file_types: tuple[str, ...] = Field(default=())  # File extensions (.py, .ts, etc.)

    # Classification
    category: RuleCategory
    severity: RuleSeverity

    # Context
    guidance: str = Field(..., min_length=10)
    applies_to: tuple[str, ...] = Field(default=())
    exceptions: tuple[str, ...] = Field(default=())

    # Behavior
    blocking: bool = True
    context_required: tuple[str, ...] = Field(default=())

    # Tags for filtering
    tags: frozenset[str] = Field(default_factory=frozenset)

    @field_validator("pattern")
    @classmethod
    def validate_regex(cls, v: str) -> str:
        """Validate that pattern is a valid regex."""
        try:
            re.compile(v)
        except re.error as e:
            msg = f"Invalid regex pattern: {e}"
            raise ValueError(msg) from e
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def convert_tags(cls, v: frozenset[str] | list[str] | set[str]) -> frozenset[str]:
        """Convert tags from list/set to frozenset."""
        if isinstance(v, (list, set)):
            return frozenset(v)
        return v

    @field_validator("applies_to", "exceptions", "context_required", "file_types", mode="before")
    @classmethod
    def convert_to_tuple(cls, v: tuple[str, ...] | list[str]) -> tuple[str, ...]:
        """Convert lists to tuples for immutability."""
        if isinstance(v, list):
            return tuple(v)
        return v

    def get_pattern_for_language(self, language: str | None = None) -> str:
        """Get the appropriate pattern for a specific language.

        Args:
            language: Target language (e.g., "python", "typescript").
                     If None, uses the rule's default language or falls back to pattern.

        Returns:
            The pattern string for the specified language.

        """
        target = language or self.language or "default"
        if self.patterns and target in self.patterns:
            return self.patterns[target]
        return self.pattern

    def applies_to_file(self, file_path: str) -> bool:
        """Check if this rule applies to a given file.

        Args:
            file_path: Path to the file to check.

        Returns:
            True if the rule applies to this file.

        """
        # Check file extension (combined condition for SIM102)
        if self.file_types and not any(file_path.endswith(ext) for ext in self.file_types):
            return False

        # Check applies_to patterns (combined condition for SIM102)
        if self.applies_to and not any(fnmatch(file_path, pat) for pat in self.applies_to):
            return False

        # Check exception patterns (combined condition for SIM102)
        return not (self.exceptions and any(fnmatch(file_path, pat) for pat in self.exceptions))


class RuleViolation(BaseModel):
    """Detected rule violation.

    Attributes:
        rule: The validation rule that was violated
        line: Line number where violation was found
        column: Column number (if available)
        snippet: Code snippet showing the violation
        file_path: Path to the file containing the violation

    """

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    rule: ValidationRule
    line: int | None = None
    column: int | None = None
    snippet: str | None = None
    file_path: str | None = None

    def format_message(self) -> str:
        """Format violation as user-friendly message."""
        parts = [f"[{self.rule.code}]"]

        if self.line is not None:
            parts.append(f"L{self.line}")

        parts.extend([f"{self.rule.name}:", self.rule.guidance.strip().split("\n")[0]])

        return " ".join(parts)

    def format_detailed(self) -> str:
        """Format violation with full details."""
        lines = [
            f"[{self.rule.code}] {self.rule.name}",
            f"  Severity: {self.rule.severity.value}",
        ]

        if self.file_path:
            lines.append(f"  File: {self.file_path}")

        if self.line is not None:
            lines.append(f"  Line: {self.line}")

        if self.snippet:
            lines.append(f"  Code: {self.snippet[:80]}")

        lines.append(f"  Fix: {self.rule.guidance.strip()}")

        return "\n".join(lines)


__all__ = [
    "RuleCategory",
    "RuleSeverity",
    "RuleViolation",
    "ValidationRule",
]
