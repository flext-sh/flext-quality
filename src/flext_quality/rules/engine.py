"""YAML Rules Engine for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_quality import FlextQualityRulesLoader, c, m, p, r, t, u

if TYPE_CHECKING:
    from collections.abc import MutableSequence


class FlextQualityRulesEngine:
    """Engine for YAML-based declarative rules validation."""

    def __init__(self, rules_path: Path | None = None) -> None:
        """Initialize rules engine."""
        self._rules_path: Path | None = rules_path
        self._rules: MutableSequence[m.Quality.RuleDefinition] = []
        self._loaded: bool = False

    def list_rules(self) -> MutableSequence[m.Quality.RuleDefinition]:
        """Get loaded rules.

        Returns:
            The resulting ``MutableSequence[m.Quality.RuleDefinition]``.
        """
        return list(self._rules)

    def load_rules(self, rules_path: Path | None = None) -> p.Result[int]:
        """Load rules from YAML file.

        Returns:
            The resulting ``p.Result[int]``.
        """
        path = rules_path or self._rules_path
        if path is None:
            path = Path(__file__).parent.parent.parent.parent / "rules" / "default.yaml"
        loader = FlextQualityRulesLoader()
        result = loader.load(path)
        if result.failure:
            return r[int].fail(result.error)
        self._rules = list(result.value)
        self._loaded = True
        return r[int].ok(len(self._rules))

    def validate(
        self, path: str, context: t.JsonMapping | None = None
    ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
        """Validate code against loaded rules.

        Returns:
            The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
        """
        if not self._loaded:
            load_result = self.load_rules()
            if load_result.failure:
                return r[t.SequenceOf[t.JsonMapping]].fail(load_result.error)
        target_path = Path(path)
        if not target_path.exists():
            return r[t.SequenceOf[t.JsonMapping]].fail(f"Path does not exist: {path}")
        files = self._get_files(target_path)
        if files.failure:
            return r[t.SequenceOf[t.JsonMapping]].fail(files.error)
        violations: MutableSequence[t.JsonMapping] = []
        for file_path in files.value:
            file_violations = self._validate_file(file_path, context or {})
            violations.extend(file_violations)
        return r[t.SequenceOf[t.JsonMapping]].ok(violations)

    def validate_content(
        self, content: str, filename: str = "<string>"
    ) -> p.Result[t.SequenceOf[t.JsonMapping]]:
        """Validate content string against loaded rules.

        Returns:
            The resulting ``p.Result[t.SequenceOf[t.JsonMapping]]``.
        """
        if not self._loaded:
            load_result = self.load_rules()
            if load_result.failure:
                return r[t.SequenceOf[t.JsonMapping]].fail(load_result.error)
        violations: MutableSequence[t.JsonMapping] = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            rule_violations = self._check_rule(rule, content, filename)
            violations.extend(rule_violations)
        return r[t.SequenceOf[t.JsonMapping]].ok(violations)

    def _check_rule(
        self, rule: m.Quality.RuleDefinition, content: str, filename: str
    ) -> t.SequenceOf[t.JsonMapping]:
        """Check a single rule against content.

        Returns:
            The resulting ``t.SequenceOf[t.JsonMapping]``.
        """
        violations: MutableSequence[t.JsonMapping] = []
        if rule.pattern is None:
            return violations
        try:
            pattern = u.Quality.compile_pattern(rule.pattern)
        except c.EXC_VALIDATION_VALUE:
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

    @staticmethod
    def _get_files(path: Path) -> p.Result[t.SequenceOf[Path]]:
        """Select the Python files under ``path`` through the CLI file owner.

        Returns:
            The resulting ``p.Result[t.SequenceOf[Path]]``.
        """
        if path.is_file():
            return [path] if path.suffix == ".py" else []
        return list(u.Cli.files_matching(path, includes=["*.py"]).value)

    @staticmethod
    def _rule_type_to_severity(rule_type: c.Quality.RuleType) -> str:
        """Convert rule type to severity.

        Returns:
            The resulting ``str``.
        """
        mapping = {
            c.Quality.RuleType.BLOCKING: c.Quality.Severity.ERROR,
            c.Quality.RuleType.WARNING: c.Quality.Severity.WARNING,
            c.Quality.RuleType.INFO: c.Quality.Severity.INFO,
        }
        return str(mapping.get(rule_type, c.Quality.Severity.INFO))

    def _validate_file(
        self, file_path: Path, context: t.JsonMapping
    ) -> t.SequenceOf[t.JsonMapping]:
        """Validate a single file against rules.

        Returns:
            The resulting ``t.SequenceOf[t.JsonMapping]``.
        """
        validation_context = t.json_dict_adapter().validate_python(context or {})
        read = u.Cli.files_read_text(file_path)
        if read.failure:
            return [
                {
                    "rule": "file-read-error",
                    "file": str(file_path),
                    "message": f"Failed to read file: {read.error}",
                    "severity": c.Quality.Severity.ERROR,
                    "context": validation_context,
                }
            ]
        content = read.value
        violations: MutableSequence[t.JsonMapping] = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            rule_violations = self._check_rule(rule, content, str(file_path))
            if validation_context:
                rule_violations = [
                    {**violation, "context": validation_context}
                    for violation in rule_violations
                ]
            violations.extend(rule_violations)
        return violations


# Why: declare public ABI so the flext-infra lazy-init generator can derive
# this submodule's package __init__.py exports (flext-1wjg1.16.32).
__all__: list[str] = ["FlextQualityRulesEngine"]
