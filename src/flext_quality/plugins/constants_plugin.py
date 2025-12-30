# VERIFIED_NEW_MODULE
"""Constants Compliance Plugin - FLEXT Constants Validation.

Validates constants compliance across FLEXT projects:
- Hardcoded value detection and replacement suggestions
- Duplicate constant declarations
- FLEXT architectural pattern violations
- Import compliance validation
- Usage pattern validation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from flext_core import FlextLogger, FlextResult, FlextService


class FlextConstantsPlugin(FlextService[int]):
    """FLEXT Constants Compliance Validation Plugin.

    Validates constants usage patterns, detects hardcoded values,
    and ensures architectural compliance across FLEXT projects.

    Usage::

        from flext_quality.plugins.constants_plugin import FlextConstantsPlugin

        plugin = FlextConstantsPlugin()
        result = plugin.check_project(Path("flext-core"))
        if result.is_success:
            for violation in result.value.violations:
                print(f"{violation.severity}: {violation.message}")
    """

    __slots__ = ("_constant_mappings", "_logger", "_pattern_mappings")

    # Hardcoded patterns to detect
    HARDCODED_PATTERNS: ClassVar[dict[str, str]] = {
        "localhost": "FlextConstants.Network.LOCALHOST",
        "127.0.0.1": "FlextConstants.Network.LOOPBACK_IP",
        "8000": "FlextConstants.Platform.FLEXT_API_PORT",
        "8080": "FlextConstants.Platform.DEFAULT_HTTP_PORT",
        "30": "FlextConstants.Network.DEFAULT_TIMEOUT",
    }

    # FLEXT architectural violation patterns
    ARCHITECTURAL_PATTERNS: ClassVar[dict[str, str]] = {
        r"from\s+click\s+import": "Direct CLI library import (use flext-cli)",
        r"from\s+rich\s+import": "Direct rich import (use flext-cli)",
        r"from\s+sqlalchemy\s+import": "Direct ORM import (use flext-db-*)",
        r"from\s+oracledb\s+import": "Direct Oracle import (use flext-db-oracle)",
        r"from\s+ldap3\s+import": "Direct LDAP import (use flext-ldap)",
        r"import\s+requests": "Direct HTTP import (use flext-core)",
        r"import\s+httpx": "Direct HTTP import (use flext-core)",
    }

    # ============================================
    # Result Dataclasses
    # ============================================

    @dataclass(frozen=True, slots=True)
    class Violation:
        """Single constants compliance violation."""

        type: str  # HARDCODED, DUPLICATE, ARCHITECTURE, USAGE, IMPORT
        severity: str  # ERROR, WARNING, INFO
        file_path: Path
        line_number: int | None
        message: str
        suggestion: str
        rule_id: str | None = None

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Aggregated constants check result."""

        total_violations: int
        files_checked: int
        violations_by_type: dict[str, int] = field(default_factory=dict)
        violations_by_severity: dict[str, int] = field(default_factory=dict)
        violations: tuple[FlextConstantsPlugin.Violation, ...] = field(
            default_factory=tuple
        )
        constants_found: int = 0
        duplicates_found: int = 0

    def __init__(self) -> None:
        """Initialize constants plugin."""
        super().__init__()
        self._logger = FlextLogger.get_logger(__name__)

        # Pre-compile regex patterns for performance
        self._hardcoded_regexes = {
            pattern: re.compile(rf"\b{re.escape(pattern)}\b")
            for pattern in self.HARDCODED_PATTERNS
        }

        self._architectural_regexes = {
            re.compile(pattern): message
            for pattern, message in self.ARCHITECTURAL_PATTERNS.items()
        }

    def check_project(
        self, project_path: Path, include_tests: bool = True
    ) -> FlextResult[CheckResult]:
        """Check constants compliance for entire project.

        Args:
            project_path: Path to project root
            include_tests: Whether to include test directories

        Returns:
            CheckResult with violations and statistics

        """
        try:
            if not project_path.exists():
                return FlextResult.failure(
                    f"Project path does not exist: {project_path}"
                )

            violations = []
            files_checked = 0
            constants_found = 0
            duplicates_found = 0

            # Check source code
            src_path = project_path / "src"
            if src_path.exists():
                src_result = self._check_directory(src_path, "src")
                if src_result.is_success:
                    violations.extend(src_result.value.violations)
                    files_checked += src_result.value.files_checked
                    constants_found += src_result.value.constants_found
                    duplicates_found += src_result.value.duplicates_found

            # Check examples
            examples_path = project_path / "examples"
            if examples_path.exists():
                examples_result = self._check_directory(examples_path, "examples")
                if examples_result.is_success:
                    violations.extend(examples_result.value.violations)
                    files_checked += examples_result.value.files_checked

            # Check tests (optional)
            if include_tests:
                tests_path = project_path / "tests"
                if tests_path.exists():
                    tests_result = self._check_directory(tests_path, "tests")
                    if tests_result.is_success:
                        violations.extend(tests_result.value.violations)
                        files_checked += tests_result.value.files_checked

            # Check scripts
            scripts_path = project_path / "scripts"
            if scripts_path.exists():
                scripts_result = self._check_directory(scripts_path, "scripts")
                if scripts_result.is_success:
                    violations.extend(scripts_result.value.violations)
                    files_checked += scripts_result.value.files_checked

            # Aggregate results
            violations_by_type = {}
            violations_by_severity = {}

            for violation in violations:
                violations_by_type[violation.type] = (
                    violations_by_type.get(violation.type, 0) + 1
                )
                violations_by_severity[violation.severity] = (
                    violations_by_severity.get(violation.severity, 0) + 1
                )

            result = self.CheckResult(
                total_violations=len(violations),
                files_checked=files_checked,
                violations_by_type=violations_by_type,
                violations_by_severity=violations_by_severity,
                violations=tuple(violations),
                constants_found=constants_found,
                duplicates_found=duplicates_found,
            )

            return FlextResult.success(result)

        except Exception as e:
            self._logger.exception(f"Constants check failed for {project_path}")
            return FlextResult.failure(f"Constants check failed: {e}")

    def _check_directory(
        self, directory: Path, context: str
    ) -> FlextResult[CheckResult]:
        """Check constants in directory."""
        violations = []
        files_checked = 0
        constants_found = 0
        duplicates_found = 0

        try:
            for py_file in directory.rglob("*.py"):
                if self._should_check_file(py_file):
                    file_result = self._check_file(py_file, context)
                    violations.extend(file_result.violations)
                    constants_found += file_result.constants_found
                    duplicates_found += file_result.duplicates_found
                    files_checked += 1

            result = self.CheckResult(
                total_violations=len(violations),
                files_checked=files_checked,
                violations=tuple(violations),
                constants_found=constants_found,
                duplicates_found=duplicates_found,
            )

            return FlextResult.success(result)

        except Exception as e:
            return FlextResult.failure(f"Directory check failed: {e}")

    def _check_file(self, file_path: Path, context: str) -> CheckResult:
        """Check constants in single file."""
        violations = []
        constants_found = 0
        duplicates_found = 0

        try:
            content = Path(file_path).read_text(encoding="utf-8")

            lines = content.split("\n")

            # Check for hardcoded values
            hardcoded_violations = self._check_hardcoded_values(
                file_path, content, lines, context
            )
            violations.extend(hardcoded_violations)

            # Check for architectural violations
            arch_violations = self._check_architectural_patterns(
                file_path, content
            )
            violations.extend(arch_violations)

            # Check for duplicate constants (only in constants.py files)
            if file_path.name == "constants.py":
                duplicate_violations, const_count, dup_count = (
                    self._check_duplicate_constants(file_path, content)
                )
                violations.extend(duplicate_violations)
                constants_found = const_count
                duplicates_found = dup_count

            # Check import patterns
            import_violations = self._check_import_patterns(file_path, content, lines)
            violations.extend(import_violations)

        except Exception as e:
            self._logger.warning(f"Failed to check file {file_path}: {e}")

        return self.CheckResult(
            total_violations=len(violations),
            files_checked=1,
            violations=tuple(violations),
            constants_found=constants_found,
            duplicates_found=duplicates_found,
        )

    def _check_hardcoded_values(
        self, file_path: Path, content: str, lines: list[str], context: str
    ) -> list[Violation]:
        """Check for hardcoded values that should use constants."""
        violations = []

        # Skip certain contexts where hardcoded values are acceptable
        if context in {"tests", "examples"} or "test" in str(file_path).lower():
            return violations

        for pattern, regex in self._hardcoded_regexes.items():
            for match in regex.finditer(content):
                line_num = content[: match.start()].count("\n") + 1
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                # Skip if it's in a comment or docstring
                if self._is_in_comment_or_docstring(
                    line_content,
                    match.start() - content[: match.start()].rfind("\n") - 1,
                ):
                    continue

                # Skip if it's defining the constant itself
                if (
                    "constants.py" in str(file_path)
                    and pattern in line_content
                    and "=" in line_content
                ):
                    continue

                suggestion = self.HARDCODED_PATTERNS[pattern]
                violation = self.Violation(
                    type="HARDCODED",
                    severity="WARNING",
                    file_path=file_path,
                    line_number=line_num,
                    message=f"Hardcoded value '{pattern}' found",
                    suggestion=f"Replace with {suggestion}",
                    rule_id=f"HARDCODED_{pattern.upper()}",
                )
                violations.append(violation)

        return violations

    def _check_architectural_patterns(
        self, file_path: Path, content: str
    ) -> list[Violation]:
        """Check for architectural pattern violations."""
        violations = []

        for regex, message in self._architectural_regexes.items():
            for match in regex.finditer(content):
                line_num = content[: match.start()].count("\n") + 1

                violation = self.Violation(
                    type="ARCHITECTURE",
                    severity="ERROR",
                    file_path=file_path,
                    line_number=line_num,
                    message=message,
                    suggestion="Use appropriate FLEXT abstraction layer",
                    rule_id="ARCHITECTURAL_VIOLATION",
                )
                violations.append(violation)

        return violations

    def _check_duplicate_constants(
        self, file_path: Path, content: str
    ) -> tuple[list[Violation], int, int]:
        """Check for duplicate constant declarations."""
        violations = []
        constants_found = 0
        duplicates_found = 0

        try:
            tree = ast.parse(content)
            constants = {}

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            const_name = target.id
                            if const_name in constants:
                                duplicates_found += 1
                                violation = self.Violation(
                                    type="DUPLICATE",
                                    severity="ERROR",
                                    file_path=file_path,
                                    line_number=getattr(node, "lineno", None),
                                    message=f"Duplicate constant declaration: {const_name}",
                                    suggestion="Remove duplicate or rename constant",
                                    rule_id="DUPLICATE_CONSTANT",
                                )
                                violations.append(violation)
                            else:
                                constants[const_name] = node
                                constants_found += 1

        except SyntaxError:
            # Skip files with syntax errors
            pass

        return violations, constants_found, duplicates_found

    def _check_import_patterns(
        self, file_path: Path, content: str, lines: list[str]
    ) -> list[Violation]:
        """Check import patterns for compliance."""
        violations = []

        # Check for incorrect alias usage
        if re.search(r"from\s+flext_core\s+import.*\bc\b", content):
            line_num = None
            for i, line in enumerate(lines, 1):
                if (
                    "from flext_core import" in line
                    and "c" in line
                    and " as c" not in line
                ):
                    line_num = i
                    break

            violation = self.Violation(
                type="USAGE",
                severity="WARNING",
                file_path=file_path,
                line_number=line_num,
                message="Incorrect import alias 'c' found",
                suggestion="Use 'from flext_core import FlextConstants' instead",
                rule_id="INCORRECT_ALIAS",
            )
            violations.append(violation)

        return violations

    def _should_check_file(self, file_path: Path) -> bool:
        """Determine if file should be checked."""
        # Skip certain directories and files
        skip_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "build",
            "dist",
            "*.pyc",
            ".bak",
            ".tmp",
        ]

        for pattern in skip_patterns:
            if pattern in str(file_path):
                return False

        return file_path.suffix == ".py"

    def _is_in_comment_or_docstring(self, line: str, char_pos: int) -> bool:
        """Check if position is within comment or docstring."""
        # Check for comments
        if "#" in line and line.find("#") < char_pos:
            return True

        # Basic docstring detection (would need more sophisticated parsing for multi-line)
        return bool('"""' in line or "'''" in line)
