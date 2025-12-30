"""Hook validation patterns - danger commands and rules.

All patterns are loaded from the centralized rules system via RuleRegistry.
Pattern tuple format: (regex_pattern, command_name, guidance_message)
"""

from __future__ import annotations

from flext_quality.rules import registry
from flext_quality.rules.models import RuleCategory

# Export in backward-compatible tuple format
DANGEROUS_COMMANDS: list[tuple[str, str, str]] = registry.as_dangerous_commands()

# Categorized patterns from registry
_bash_rules = registry.by_category(RuleCategory.BASH_COMMAND)

DANGEROUS_FILE_DELETION: list[tuple[str, str, str]] = [
    (r.pattern, r.name, r.guidance) for r in _bash_rules if "file-deletion" in r.tags
]

DANGEROUS_INPLACE_EDIT: list[tuple[str, str, str]] = [
    (r.pattern, r.name, r.guidance) for r in _bash_rules if "inplace" in r.name.lower()
]

DANGEROUS_GIT_REVIEW: list[tuple[str, str, str]] = [
    (r.pattern, r.name, r.guidance)
    for r in _bash_rules
    if "git" in r.tags and "reset" not in r.name.lower()
]

DANGEROUS_GIT_RESET: list[tuple[str, str, str]] = [
    (r.pattern, r.name, r.guidance)
    for r in _bash_rules
    if "git" in r.tags and "reset" in r.name.lower()
]

__all__ = [
    "DANGEROUS_COMMANDS",
    "DANGEROUS_FILE_DELETION",
    "DANGEROUS_GIT_RESET",
    "DANGEROUS_GIT_REVIEW",
    "DANGEROUS_INPLACE_EDIT",
]
