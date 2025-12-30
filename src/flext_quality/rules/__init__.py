"""FLEXT Centralized Validation Rules System.

This package provides a centralized, extensible system for validation rules
used across all FLEXT projects and Claude Code hooks.

Architecture:
    - Models (Pydantic): ValidationRule, RuleViolation, RuleCategory, RuleSeverity
    - Loader: Loads rules from YAML files
    - Registry: Centralized rule registry with indexing
    - Validators: RuleValidator implementing ValidatorSpec protocol

Usage:
    from flext_quality.rules import registry
    from flext_quality.rules.validators import validate_content

    # Get all critical rules
    critical_rules = registry.by_severity(RuleSeverity.CRITICAL)

    # Get rules for a file
    file_rules = registry.for_file("src/example.py")

    # Validate content
    result = validate_content("import sys", "example.py", blocking_only=True)
    if result.is_success:
        violations = result.unwrap()

Example YAML format:
    metadata:
      category: bash_command
      version: "1.0.0"

    rules:
      - code: DC001
        name: rm -rf
        pattern: 'rm\\s+-rf?\\s+'
        severity: critical
        guidance: Use 'mv file file.bak' instead
        blocking: true
        tags: [destructive, file-deletion]
"""

from __future__ import annotations

from .loader import RuleLoader
from .models import RuleCategory, RuleSeverity, RuleViolation, ValidationRule
from .registry import RuleRegistry, registry
from .validators import (
    CompositeValidator,
    NegatedValidator,
    RuleValidator,
    validate_content,
)

__all__ = [
    "CompositeValidator",
    "NegatedValidator",
    "RuleCategory",
    "RuleLoader",
    "RuleRegistry",
    "RuleSeverity",
    "RuleValidator",
    "RuleViolation",
    "ValidationRule",
    "registry",
    "validate_content",
]
