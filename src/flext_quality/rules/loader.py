"""Rules loader for YAML rule definitions."""

from __future__ import annotations

from pathlib import Path
from typing import TypeGuard

import yaml
from flext_core import FlextResult as r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.models import RuleDefinition


def _is_dict(value: object) -> TypeGuard[dict[str, object]]:
    """Type guard for dict validation."""
    return isinstance(value, dict)


def _is_list(value: object) -> TypeGuard[list[object]]:
    """Type guard for list validation."""
    return isinstance(value, list)


class FlextQualityRulesLoader:
    """Loads rules from YAML files."""

    def load(self, path: Path) -> r[list[RuleDefinition]]:
        """Load rules from YAML file."""
        if not path.exists():
            return r[list[RuleDefinition]].fail(f"Rules file not found: {path}")

        try:
            with path.open(encoding="utf-8") as f:
                parsed: object = yaml.safe_load(f)
        except Exception as e:
            return r[list[RuleDefinition]].fail(f"Failed to parse YAML: {e}")

        if not _is_dict(parsed):
            return r[list[RuleDefinition]].fail("Invalid YAML: expected dict at root")

        rules_data = parsed.get("rules", [])
        if not _is_list(rules_data):
            return r[list[RuleDefinition]].fail("Invalid YAML: 'rules' must be a list")

        rules: list[RuleDefinition] = []

        for idx, rule_data in enumerate(rules_data):
            if not _is_dict(rule_data):
                return r[list[RuleDefinition]].fail(f"Rule {idx}: expected dict")
            result = self._parse_rule(rule_data, idx)
            if result.is_failure:
                return r[list[RuleDefinition]].fail(result.error)
            rules.append(result.value)

        return r[list[RuleDefinition]].ok(rules)

    def _parse_rule(
        self,
        data: dict[str, object],
        index: int,
    ) -> r[RuleDefinition]:
        """Parse a single rule from dict."""
        name = data.get("name")
        if not name:
            return r[RuleDefinition].fail(f"Rule {index}: missing 'name'")

        rule_type_str = data.get("type")
        if not rule_type_str:
            return r[RuleDefinition].fail(f"Rule {index}: missing 'type'")

        try:
            rule_type = c.Quality.RuleType(str(rule_type_str))
        except ValueError:
            # Show VALUES not keys - users need lowercase: "blocking", "warning", "info"
            valid_types = [m.value for m in c.Quality.RuleType.__members__.values()]
            return r[RuleDefinition].fail(
                f"Rule {index}: invalid type '{rule_type_str}'. Valid: {valid_types}"
            )

        description = data.get("description", "")
        action = data.get("action", "warn")
        pattern = data.get("pattern")
        enabled = data.get("enabled", True)

        rule = RuleDefinition(
            name=str(name),
            type=rule_type,
            description=str(description),
            pattern=str(pattern) if pattern else None,
            action=str(action),
            enabled=bool(enabled),
        )

        return r[RuleDefinition].ok(rule)

    def load_multiple(self, paths: list[Path]) -> r[list[RuleDefinition]]:
        """Load rules from multiple YAML files."""
        all_rules: list[RuleDefinition] = []

        for path in paths:
            result = self.load(path)
            if result.is_failure:
                return r[list[RuleDefinition]].fail(
                    f"Error loading {path}: {result.error}"
                )
            all_rules.extend(result.value)

        return r[list[RuleDefinition]].ok(all_rules)
