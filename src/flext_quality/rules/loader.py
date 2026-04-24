"""Rules loader for YAML rule definitions."""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)
from pathlib import Path

from flext_quality import c, m, p, r, t, u


class FlextQualityRulesLoader:
    """Loads rules from YAML files."""

    def load(self, path: Path) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from YAML file."""
        if not path.exists():
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Rules file not found: {path}",
            )
        yaml_result = u.Cli.yaml_safe_load(path)
        if yaml_result.failure:
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Failed to parse YAML: {yaml_result.error}",
            )
        parsed = yaml_result.value
        if not isinstance(parsed, dict):
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                "Invalid YAML: expected dict at root",
            )
        parsed_dict: t.JsonMapping = (
            t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(parsed)
        )
        rules_data_val = parsed_dict.get("rules", [])
        if not isinstance(rules_data_val, list):
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                "Invalid YAML: 'rules' must be a list",
            )
        rules_data: Sequence[t.JsonMapping] = (
            t.Quality.RELAXED_CONTAINER_MAPPING_SEQUENCE_ADAPTER.validate_python(
                rules_data_val,
            )
        )
        rules: MutableSequence[m.Quality.RuleDefinition] = []
        for idx, rule_data in enumerate(rules_data):
            rule_dict: t.JsonMapping = (
                t.Quality.CONTAINER_MAPPING_ADAPTER.validate_python(
                    dict(rule_data),
                )
            )
            result = self._parse_rule(rule_dict, idx)
            if result.failure:
                return r[Sequence[m.Quality.RuleDefinition]].fail(result.error)
            rules.append(result.value)
        return r[Sequence[m.Quality.RuleDefinition]].ok(rules)

    def load_multiple(
        self,
        paths: Sequence[Path],
    ) -> p.Result[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from multiple YAML files."""
        all_rules: MutableSequence[m.Quality.RuleDefinition] = []
        for path in paths:
            result = self.load(path)
            if result.failure:
                return r[Sequence[m.Quality.RuleDefinition]].fail(
                    f"Error loading {path}: {result.error}",
                )
            all_rules.extend(result.value)
        return r[Sequence[m.Quality.RuleDefinition]].ok(all_rules)

    def _parse_rule(
        self,
        data: t.JsonMapping,
        index: int,
    ) -> p.Result[m.Quality.RuleDefinition]:
        """Parse a single rule from dict."""
        name = data.get("name")
        if not name:
            return r[m.Quality.RuleDefinition].fail(f"Rule {index}: missing 'name'")
        rule_type_str = data.get("type")
        if not rule_type_str:
            return r[m.Quality.RuleDefinition].fail(f"Rule {index}: missing 'type'")
        try:
            rule_type = c.Quality.RuleType(str(rule_type_str))
        except ValueError:
            valid_types = [m.value for m in c.Quality.RuleType.__members__.values()]
            return r[m.Quality.RuleDefinition].fail(
                f"Rule {index}: invalid type '{rule_type_str}'. Valid: {valid_types}",
            )
        description = data.get("description", "")
        action = data.get("action", "warn")
        pattern = data.get("pattern")
        enabled = data.get("enabled", True)
        rule = m.Quality.RuleDefinition(
            name=str(name),
            type=rule_type,
            description=str(description),
            pattern=str(pattern) if pattern else None,
            action=str(action),
            enabled=bool(enabled),
        )
        return r[m.Quality.RuleDefinition].ok(rule)
