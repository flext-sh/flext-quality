"""Rule validators implementing ValidatorSpec protocol.

This module provides validators that can check content against rules
and find violations with line numbers and snippets.

Classes:
    - RuleValidator: Single rule validator with pattern matching
    - CompositeValidator: Combines multiple validators with AND/OR logic
    - NegatedValidator: Negates a validator's result

Functions:
    - validate_content: Validate content against rules from registry
"""

from __future__ import annotations

import re

from flext_core import FlextResult as r

from .models import RuleCategory, RuleViolation, ValidationRule
from .registry import registry


class RuleValidator:
    """Validator that checks content against a single ValidationRule.

    This validator implements a subset of the ValidatorSpec protocol,
    allowing composition with AND, OR, and NOT operators.

    Attributes:
        rule: The validation rule to check
        pattern: Compiled regex pattern

    """

    def __init__(self, rule: ValidationRule) -> None:
        """Initialize validator with a rule.

        Args:
            rule: The ValidationRule to validate against

        """
        self._rule = rule
        self._compiled = re.compile(rule.pattern, re.MULTILINE)

    def __call__(self, content: str) -> bool:
        """Check if content violates the rule.

        Args:
            content: Content to validate

        Returns:
            True if content matches the pattern (violates the rule)

        """
        return bool(self._compiled.search(content))

    def __and__(self, other: RuleValidator | CompositeValidator) -> CompositeValidator:
        """Combine validators with AND logic.

        Both validators must match for the result to be True.

        Args:
            other: Another validator to combine with

        Returns:
            CompositeValidator with AND mode

        """
        validators = [self]
        if isinstance(other, CompositeValidator) and other._mode == "and":
            validators.extend(other._validators)
        else:
            validators.append(other)
        return CompositeValidator(validators, mode="and")

    def __or__(self, other: RuleValidator | CompositeValidator) -> CompositeValidator:
        """Combine validators with OR logic.

        At least one validator must match for the result to be True.

        Args:
            other: Another validator to combine with

        Returns:
            CompositeValidator with OR mode

        """
        validators = [self]
        if isinstance(other, CompositeValidator) and other._mode == "or":
            validators.extend(other._validators)
        else:
            validators.append(other)
        return CompositeValidator(validators, mode="or")

    def __invert__(self) -> NegatedValidator:
        """Negate the validator.

        Returns True when pattern does NOT match.

        Returns:
            NegatedValidator

        """
        return NegatedValidator(self)

    def find_violations(
        self,
        content: str,
        file_path: str | None = None,
    ) -> list[RuleViolation]:
        """Find all violations in content.

        Args:
            content: Content to check
            file_path: Optional file path for context

        Returns:
            List of RuleViolation objects found

        """
        violations = []

        for match in self._compiled.finditer(content):
            line_num = content[: match.start()].count("\n") + 1
            snippet = match.group(0)[:80]

            violations.append(
                RuleViolation(
                    rule=self._rule,
                    line=line_num,
                    snippet=snippet,
                    file_path=file_path,
                )
            )

        return violations

    @property
    def rule(self) -> ValidationRule:
        """Get the underlying rule."""
        return self._rule


class CompositeValidator:
    """Validator combining multiple validators with AND/OR logic.

    Attributes:
        validators: List of validators to combine
        mode: Either "and" or "or"

    """

    def __init__(
        self,
        validators: list[RuleValidator | CompositeValidator],
        mode: str,
    ) -> None:
        """Initialize composite validator.

        Args:
            validators: List of validators to combine
            mode: "and" or "or" logic

        """
        self._validators = validators
        self._mode = mode

    def __call__(self, content: str) -> bool:
        """Check if content matches the composite condition.

        Args:
            content: Content to validate

        Returns:
            True if condition is met (AND all match, OR any match)

        """
        if self._mode == "and":
            return all(v(content) for v in self._validators)
        return any(v(content) for v in self._validators)

    def __and__(
        self,
        other: RuleValidator | CompositeValidator,
    ) -> CompositeValidator:
        """Combine with AND logic."""
        validators = list(self._validators)
        if isinstance(other, CompositeValidator) and other._mode == "and":
            validators.extend(other._validators)
        else:
            validators.append(other)
        return CompositeValidator(validators, mode="and")

    def __or__(
        self,
        other: RuleValidator | CompositeValidator,
    ) -> CompositeValidator:
        """Combine with OR logic."""
        validators = list(self._validators)
        if isinstance(other, CompositeValidator) and other._mode == "or":
            validators.extend(other._validators)
        else:
            validators.append(other)
        return CompositeValidator(validators, mode="or")

    def __invert__(self) -> NegatedValidator:
        """Negate the composite validator."""
        return NegatedValidator(self)


class NegatedValidator:
    """Validator that negates another validator.

    Returns True when the wrapped validator returns False.
    """

    def __init__(self, validator: RuleValidator | CompositeValidator) -> None:
        """Initialize with validator to negate.

        Args:
            validator: Validator to negate

        """
        self._validator = validator

    def __call__(self, content: str) -> bool:
        """Check if content does NOT match the wrapped validator.

        Args:
            content: Content to validate

        Returns:
            Opposite of wrapped validator's result

        """
        return not self._validator(content)

    def __invert__(self) -> RuleValidator | CompositeValidator:
        """Double negation returns original validator."""
        if isinstance(self._validator, NegatedValidator):
            return self._validator.unwrap()
        return self._validator

    def unwrap(self) -> RuleValidator | CompositeValidator:
        """Get the wrapped validator.

        Returns:
            The wrapped validator

        """
        return self._validator


def validate_content(
    content: str,
    *,
    file_path: str | None = None,
    category: str | None = None,
    blocking_only: bool = False,
) -> r[list[RuleViolation]]:
    """Validate content against rules from registry.

    Args:
        content: Content to validate
        file_path: Optional file path for filtering applicable rules
        category: Optional category name to filter by
        blocking_only: If True, only check blocking rules

    Returns:
        FlextResult containing list of RuleViolation objects

    """
    violations: list[RuleViolation] = []

    # Get applicable rules
    rules = registry.for_file(file_path) if file_path else registry.all()

    # Filter by category if specified
    if category is not None:
        try:
            cat = RuleCategory(category)
            rules = [r for r in rules if r.category == cat]
        except ValueError:
            return r[list[RuleViolation]].fail(f"Unknown category: {category}")

    # Filter by blocking if specified
    if blocking_only:
        rules = [r for r in rules if r.blocking]

    # Validate each rule
    for rule in rules:
        validator = RuleValidator(rule)
        violations.extend(validator.find_violations(content, file_path))

    return r[list[RuleViolation]].ok(violations)


__all__ = [
    "CompositeValidator",
    "NegatedValidator",
    "RuleValidator",
    "validate_content",
]
