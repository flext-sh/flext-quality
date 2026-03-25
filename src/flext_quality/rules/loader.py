"""Rules loader for YAML rule definitions."""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence
from pathlib import Path

import yaml
from flext_core import r
from pydantic import TypeAdapter

from flext_quality import c, m, t


class FlextQualityRulesLoader:
    """Loads rules from YAML files."""

    def load(self, path: Path) -> r[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from YAML file."""
        if not path.exists():
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Rules file not found: {path}",
            )
        try:
            with path.open(encoding="utf-8") as f:
                parsed = yaml.safe_load(f)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                f"Failed to parse YAML: {e}",
            )
        if not isinstance(parsed, dict):
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                "Invalid YAML: expected dict at root",
            )
        adapter: TypeAdapter[Mapping[str, t.NormalizedValue]] = TypeAdapter(
            Mapping[str, t.NormalizedValue],
        )
        parsed_dict: Mapping[str, t.NormalizedValue] = adapter.validate_python(parsed)
        rules_data_val = parsed_dict.get("rules", [])
        if not isinstance(rules_data_val, list):
            return r[Sequence[m.Quality.RuleDefinition]].fail(
                "Invalid YAML: 'rules' must be a list",
            )
        rules: MutableSequence[m.Quality.RuleDefinition] = []
        for idx, rule_data in enumerate(rules_data_val):
            if not isinstance(rule_data, dict):
                return r[Sequence[m.Quality.RuleDefinition]].fail(
                    f"Rule {idx}: expected dict",
                )
            rule_dict: Mapping[str, t.NormalizedValue] = adapter.validate_python(
                rule_data,
            )
            result = self._parse_rule(rule_dict, idx)
            if result.is_failure:
                return r[Sequence[m.Quality.RuleDefinition]].fail(result.error)
            rules.append(result.value)
        return r[Sequence[m.Quality.RuleDefinition]].ok(rules)

    def load_multiple(
        self,
        paths: Sequence[Path],
    ) -> r[Sequence[m.Quality.RuleDefinition]]:
        """Load rules from multiple YAML files."""
        all_rules: MutableSequence[m.Quality.RuleDefinition] = []
        for path in paths:
            result = self.load(path)
            if result.is_failure:
                return r[Sequence[m.Quality.RuleDefinition]].fail(
                    f"Error loading {path}: {result.error}",
                )
            all_rules.extend(result.value)
        return r[Sequence[m.Quality.RuleDefinition]].ok(all_rules)

    def _parse_rule(
        self,
        data: t.ContainerMapping,
        index: int,
    ) -> r[m.Quality.RuleDefinition]:
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
