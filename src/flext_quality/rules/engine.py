"""YAML Rules Engine for flext-quality."""

from __future__ import annotations

import re
from pathlib import Path

from flext_core import FlextResult as r

from flext_quality.constants import FlextQualityConstants as c
from flext_quality.models import FlextQualityModels as m
from flext_quality.rules.loader import FlextQualityRulesLoader


class FlextQualityRulesEngine:
    """Engine for YAML-based declarative rules validation."""

    def __init__(self, rules_path: Path | None = None) -> None:
        """Initialize rules engine."""
        self._rules_path: Path | None = rules_path
        self._rules: list[m.Quality.RuleDefinition] = []
        self._loaded: bool = False

    def load_rules(self, rules_path: Path | None = None) -> r[int]:
        """Load rules from YAML file."""
        path = rules_path or self._rules_path
        if path is None:
            path = Path(__file__).parent.parent.parent.parent / "rules" / "default.yaml"

        loader = FlextQualityRulesLoader()
        result = loader.load(path)
        if result.is_failure:
            return r[int].fail(result.error)

        self._rules = result.value
        self._loaded = True
        return r[int].ok(len(self._rules))

    def validate(
        self,
        path: str,
        context: dict[str, object] | None = None,
    ) -> r[list[dict[str, object]]]:
        """Validate code against loaded rules."""
        if not self._loaded:
            load_result = self.load_rules()
            if load_result.is_failure:
                return r[list[dict[str, object]]].fail(load_result.error)

        target_path = Path(path)
        if not target_path.exists():
            return r[list[dict[str, object]]].fail(f"Path does not exist: {path}")

        violations: list[dict[str, object]] = []
        files = self._get_files(target_path)

        for file_path in files:
            file_violations = self._validate_file(file_path, context or {})
            violations.extend(file_violations)

        return r[list[dict[str, object]]].ok(violations)

    def validate_content(
        self,
        content: str,
        filename: str = "<string>",
    ) -> r[list[dict[str, object]]]:
        """Validate content string against loaded rules."""
        if not self._loaded:
            load_result = self.load_rules()
            if load_result.is_failure:
                return r[list[dict[str, object]]].fail(load_result.error)

        violations: list[dict[str, object]] = []

        for rule in self._rules:
            if not rule.enabled:
                continue

            rule_violations = self._check_rule(rule, content, filename)
            violations.extend(rule_violations)

        return r[list[dict[str, object]]].ok(violations)

    def get_rules(self) -> list[m.Quality.RuleDefinition]:
        """Get loaded rules."""
        return self._rules.copy()

    def _get_files(self, path: Path) -> list[Path]:
        """Get Python files from path."""
        if path.is_file():
            return [path] if path.suffix == ".py" else []
        return list(path.rglob("*.py"))

    def _validate_file(
        self,
        file_path: Path,
        _context: dict[str, object],
    ) -> list[dict[str, object]]:
        """Validate a single file against rules."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            return [
                {
                    "rule": "file-read-error",
                    "file": str(file_path),
                    "message": f"Failed to read file: {e}",
                    "severity": c.Quality.Severity.ERROR,
                }
            ]

        violations: list[dict[str, object]] = []

        for rule in self._rules:
            if not rule.enabled:
                continue

            rule_violations = self._check_rule(rule, content, str(file_path))
            violations.extend(rule_violations)

        return violations

    def _check_rule(
        self,
        rule: m.Quality.RuleDefinition,
        content: str,
        filename: str,
    ) -> list[dict[str, object]]:
        """Check a single rule against content."""
        violations: list[dict[str, object]] = []

        if rule.pattern is None:
            return violations

        try:
            pattern = re.compile(rule.pattern)
        except re.error:
            pattern = None

        lines = content.splitlines()
        for line_num, line in enumerate(lines, start=1):
            match_found = False

            if pattern is not None:
                match_found = bool(pattern.search(line))
            else:
                match_found = rule.pattern in line

            if match_found:
                severity = self._rule_type_to_severity(rule.type)
                violations.append({
                    "rule": rule.name,
                    "file": filename,
                    "line": line_num,
                    "message": rule.description,
                    "severity": severity,
                    "action": rule.action,
                    "type": rule.type,
                })

        return violations

    def _rule_type_to_severity(self, rule_type: c.Quality.RuleType) -> str:
        """Convert rule type to severity."""
        mapping = {
            c.Quality.RuleType.BLOCKING: c.Quality.Severity.ERROR,
            c.Quality.RuleType.WARNING: c.Quality.Severity.WARNING,
            c.Quality.RuleType.INFO: c.Quality.Severity.INFO,
        }
        return mapping.get(rule_type, c.Quality.Severity.INFO)
