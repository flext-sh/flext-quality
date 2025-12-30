"""Centralized validation rule registry.

This module provides the RuleRegistry singleton that manages all validation
rules and provides efficient querying by category, severity, tag, and file type.

The registry loads rules from YAML files and maintains multiple indices
for fast filtering and lookup.
"""

from __future__ import annotations

from fnmatch import fnmatch

from .loader import RuleLoader
from .models import RuleCategory, RuleSeverity, ValidationRule


class RuleRegistry:
    """Centralized registry for validation rules.

    This singleton manages all validation rules and provides efficient
    querying by category, severity, tag, and file applicability.

    Attributes:
        _instance: Singleton instance
        _rules: Dict mapping rule code to rule
        _by_category: Dict mapping category to list of rules
        _by_severity: Dict mapping severity to list of rules
        _by_tag: Dict mapping tag to list of rules

    Example:
        >>> registry = RuleRegistry()
        >>> critical_rules = registry.by_severity(RuleSeverity.CRITICAL)
        >>> bash_rules = registry.by_category(RuleCategory.BASH_COMMAND)
        >>> git_rules = registry.by_tag("git")

    """

    _instance: RuleRegistry | None = None
    _initialized: bool = False
    _rules: dict[str, ValidationRule] = {}
    _by_category: dict[RuleCategory, list[ValidationRule]] = {}
    _by_severity: dict[RuleSeverity, list[ValidationRule]] = {}
    _by_tag: dict[str, list[ValidationRule]] = {}

    def __new__(cls) -> RuleRegistry:
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize registry by loading all rules from YAML files."""
        if self._initialized:
            return

        self._rules = {}
        self._by_category = {cat: [] for cat in RuleCategory}
        self._by_severity = {sev: [] for sev in RuleSeverity}
        self._by_tag = {}

        try:
            rules = RuleLoader.load_all()
            for rule in rules:
                self._register(rule)
        except (ValueError, OSError, ImportError):
            # Silently continue if rules cannot be loaded
            pass

        self._initialized = True

    def _register(self, rule: ValidationRule) -> None:
        """Register a rule in all indices."""
        self._rules[rule.code] = rule
        self._by_category[rule.category].append(rule)
        self._by_severity[rule.severity].append(rule)

        for tag in rule.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = []
            self._by_tag[tag].append(rule)

    # === Query Methods ===

    def get(self, code: str) -> ValidationRule | None:
        """Get a rule by its code.

        Args:
            code: Rule code (e.g., DC001, TV003)

        Returns:
            ValidationRule if found, None otherwise

        """
        return self._rules.get(code)

    def all(self) -> list[ValidationRule]:
        """Get all registered rules.

        Returns:
            List of all validation rules

        """
        return list(self._rules.values())

    def by_category(self, category: RuleCategory) -> list[ValidationRule]:
        """Get rules in a specific category.

        Args:
            category: Rule category to filter by

        Returns:
            List of rules in that category

        """
        return self._by_category.get(category, [])

    def by_severity(self, severity: RuleSeverity) -> list[ValidationRule]:
        """Get rules with a specific severity level.

        Args:
            severity: Severity level to filter by

        Returns:
            List of rules with that severity

        """
        return self._by_severity.get(severity, [])

    def by_tag(self, tag: str) -> list[ValidationRule]:
        """Get rules with a specific tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of rules with that tag

        """
        return self._by_tag.get(tag, [])

    def blocking_rules(self) -> list[ValidationRule]:
        """Get all rules that block execution.

        Returns:
            List of blocking rules

        """
        return [r for r in self._rules.values() if r.blocking]

    def for_file(self, file_path: str) -> list[ValidationRule]:
        """Get rules applicable to a specific file.

        Rules are applicable if:
        1. They have no applies_to patterns (apply to all), OR
        2. The file path matches at least one applies_to pattern

        Args:
            file_path: Path to the file to check

        Returns:
            List of applicable rules

        """
        result = []
        for rule in self._rules.values():
            if self._rule_applies_to_file(rule, file_path):
                result.append(rule)
        return result

    def _rule_applies_to_file(self, rule: ValidationRule, file_path: str) -> bool:
        """Check if a rule applies to a specific file.

        Args:
            rule: The rule to check
            file_path: The file path to check against

        Returns:
            True if rule applies to this file

        """
        if not rule.applies_to:
            return True

        return any(fnmatch(file_path, pat) for pat in rule.applies_to)

    def filter(
        self,
        *,
        category: RuleCategory | None = None,
        severity: RuleSeverity | None = None,
        blocking: bool | None = None,
        tags: set[str] | None = None,
        file_path: str | None = None,
    ) -> list[ValidationRule]:
        """Filter rules by multiple criteria.

        All criteria are combined with AND logic. If a criterion is None,
        it is not applied.

        Args:
            category: Filter by category
            severity: Filter by severity
            blocking: Filter by blocking status
            tags: Filter by tags (all must be present)
            file_path: Filter by file applicability

        Returns:
            List of matching rules

        """
        rules = list(self._rules.values())

        if category is not None:
            rules = [r for r in rules if r.category == category]

        if severity is not None:
            rules = [r for r in rules if r.severity == severity]

        if blocking is not None:
            rules = [r for r in rules if r.blocking == blocking]

        if tags is not None:
            rules = [r for r in rules if tags.issubset(r.tags)]

        if file_path is not None:
            rules = [r for r in rules if self._rule_applies_to_file(r, file_path)]

        return rules

    # === Backward Compatibility Methods ===

    def as_dangerous_commands(self) -> list[tuple[str, str, str]]:
        """Export bash command rules in legacy tuple format.

        Returns:
            List of (pattern, name, guidance) tuples for DANGEROUS_COMMANDS

        """
        return [
            (rule.pattern, rule.name, rule.guidance)
            for rule in self.by_category(RuleCategory.BASH_COMMAND)
        ]

    def as_type_verification_patterns(self) -> list[tuple[str, str, str]]:
        """Export type system rules in legacy tuple format.

        Returns:
            List of (pattern, code, guidance) tuples for TYPE_VERIFICATION_PATTERNS

        """
        return [
            (rule.pattern, rule.code, rule.guidance)
            for rule in self.by_category(RuleCategory.TYPE_SYSTEM)
        ]

    def as_code_quality_violations(self) -> list[tuple[str, str, str]]:
        """Export Python code quality rules in legacy tuple format.

        Returns:
            List of (pattern, name, guidance) tuples for CODE_QUALITY_VIOLATIONS

        """
        return [
            (rule.pattern, rule.name, rule.guidance)
            for rule in self.by_category(RuleCategory.PYTHON_CODE)
        ]

    # === Statistics ===

    def stats(self) -> dict[str, int]:
        """Get statistics about registered rules.

        Returns:
            Dict with counts by category and severity

        """
        return {
            "total": len(self._rules),
            "bash_command": len(self._by_category[RuleCategory.BASH_COMMAND]),
            "python_code": len(self._by_category[RuleCategory.PYTHON_CODE]),
            "type_system": len(self._by_category[RuleCategory.TYPE_SYSTEM]),
            "architecture": len(self._by_category[RuleCategory.ARCHITECTURE]),
            "file_protection": len(self._by_category[RuleCategory.FILE_PROTECTION]),
            "critical": len(self._by_severity[RuleSeverity.CRITICAL]),
            "high": len(self._by_severity[RuleSeverity.HIGH]),
            "medium": len(self._by_severity[RuleSeverity.MEDIUM]),
            "low": len(self._by_severity[RuleSeverity.LOW]),
            "blocking": len(self.blocking_rules()),
            "tags": len(self._by_tag),
        }


# Global singleton instance
registry = RuleRegistry()

__all__ = ["RuleRegistry", "registry"]
