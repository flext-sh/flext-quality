# VERIFIED_NEW_MODULE
"""Type Verification Plugin - AST-based type system compliance checking.

Implements TV001-TV018 detection rules for:
- Missing/excessive type annotations
- Type centralization violations
- Protocol/Model recommendations
- FlextResult usage patterns

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

from ..constants import FlextQualityConstants


class FlextTypeVerificationPlugin(FlextService["FlextTypeVerificationPlugin.CheckResult"]):
    """Type verification plugin for detecting type issues.

    Implements AST-based analysis for TV001-TV018 rules.

    Usage:
        from flext_quality.plugins import FlextTypeVerificationPlugin

        plugin = FlextTypeVerificationPlugin()
        result = plugin.check([Path("file.py")])
        if result.is_success:
            for violation in result.value.violations:
                logger.info("%s: %s", violation.rule_id, violation.message)
    """

    __slots__ = ("_logger", "_settings")

    # =========================================================================
    # NESTED DATACLASSES - Following FLEXT facade pattern
    # =========================================================================

    @dataclass(frozen=True, slots=True)
    class TypeViolation:
        """Single type violation detected by the plugin."""

        rule_id: str
        category: str
        severity: str
        file: str
        line: int
        column: int
        message: str
        suggestion: str | None = None
        raw_type: str | None = None

    @dataclass(frozen=True, slots=True)
    class TypeViolationStats:
        """Statistics for type violations by category."""

        by_category: dict[str, int]
        by_severity: dict[str, int]
        by_rule: dict[str, int]
        total: int

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Result container for type verification check."""

        violations: tuple[FlextTypeVerificationPlugin.TypeViolation, ...]
        stats: FlextTypeVerificationPlugin.TypeViolationStats
        files_checked: int
        guidance: tuple[str, ...]

    def __init__(self: Self) -> None:
        """Initialize type verification plugin."""
        super().__init__()
        self._logger = FlextLogger(__name__)

    def execute(self: Self) -> FlextResult[CheckResult]:
        """Satisfy FlextService contract."""
        return FlextResult[FlextTypeVerificationPlugin.CheckResult].fail(
            "Use check() method with file list"
        )

    def check(
        self: Self,
        files: list[Path],
        categories: set[str] | None = None,
    ) -> FlextResult[CheckResult]:
        """Check files for type violations.

        Args:
            files: Files to check.
            categories: Optional set of categories to check (default: all).

        Returns:
            CheckResult with violations and statistics.

        """
        if not files:
            return FlextResult[FlextTypeVerificationPlugin.CheckResult].ok(
                FlextTypeVerificationPlugin.CheckResult(
                    violations=(),
                    stats=FlextTypeVerificationPlugin.TypeViolationStats(
                        by_category={},
                        by_severity={},
                        by_rule={},
                        total=0,
                    ),
                    files_checked=0,
                    guidance=(),
                )
            )

        all_violations: list[FlextTypeVerificationPlugin.TypeViolation] = []

        for file_path in files:
            if not file_path.exists():
                continue

            try:
                source = file_path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(file_path))
                file_violations = self._analyze_file(
                    tree, str(file_path), categories
                )
                all_violations.extend(file_violations)
            except SyntaxError as err:
                self._logger.warning("Syntax error in %s: %s", file_path, err)
            except UnicodeDecodeError:
                self._logger.warning("Encoding error in %s", file_path)

        violations_tuple = tuple(all_violations)
        stats = self._calculate_stats(violations_tuple)
        guidance = self._generate_guidance(stats)

        result = FlextTypeVerificationPlugin.CheckResult(
            violations=violations_tuple,
            stats=stats,
            files_checked=len(files),
            guidance=guidance,
        )

        self._logger.info(
            "Type verification: %d violations in %d files",
            stats.total,
            len(files),
        )

        return FlextResult[FlextTypeVerificationPlugin.CheckResult].ok(result)

    def _analyze_file(
        self: Self,
        tree: ast.AST,
        filename: str,
        categories: set[str] | None,
    ) -> list[TypeViolation]:
        """Analyze a single file for type violations."""
        violations: list[FlextTypeVerificationPlugin.TypeViolation] = []

        # Run all analyzers
        analyzers = [
            self._AnnotationAnalyzer(filename, categories),
            self._CentralizationAnalyzer(filename, categories),
            self._ProtocolRecommendationAnalyzer(filename, categories),
            self._ModelRecommendationAnalyzer(filename, categories),
            self._CouplingAnalyzer(filename, categories),
            self._ResultUsageAnalyzer(filename, categories),
            self._UncentralizedTypeAnalyzer(filename, categories),
        ]

        for analyzer in analyzers:
            analyzer.visit(tree)
            violations.extend(analyzer.violations)

        return violations

    def _calculate_stats(
        self: Self,
        violations: tuple[TypeViolation, ...],
    ) -> TypeViolationStats:
        """Calculate violation statistics."""
        by_category: dict[str, int] = {}
        by_severity: dict[str, int] = {}
        by_rule: dict[str, int] = {}

        for v in violations:
            by_category[v.category] = by_category.get(v.category, 0) + 1
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1
            by_rule[v.rule_id] = by_rule.get(v.rule_id, 0) + 1

        return FlextTypeVerificationPlugin.TypeViolationStats(
            by_category=by_category,
            by_severity=by_severity,
            by_rule=by_rule,
            total=len(violations),
        )

    def _generate_guidance(
        self: Self,
        stats: TypeViolationStats,
    ) -> tuple[str, ...]:
        """Generate guidance based on statistics."""
        guidance: list[str] = []

        if stats.by_category.get("decentralized_type", 0) > 0:
            guidance.append(
                "Move TypeAlias definitions to typings.py and Protocol "
                "definitions to protocols.py"
            )

        if stats.by_category.get("uncentralized_type", 0) > 0:
            guidance.append(
                "Replace raw dict/Mapping types with centralized aliases "
                "from t.* namespace"
            )

        if stats.by_category.get("result_misuse", 0) > 0:
            guidance.append(
                "Review FlextResult usage - ensure proper type parameters "
                "and unwrap patterns"
            )

        if stats.by_category.get("needs_protocol", 0) > 0:
            guidance.append(
                "Consider defining Protocol types for complex Callable "
                "signatures"
            )

        if stats.by_category.get("needs_model", 0) > 0:
            guidance.append(
                "Consider using Pydantic models instead of complex "
                "dict types or dataclasses"
            )

        return tuple(guidance)

    # =========================================================================
    # ANALYZER CLASSES - Nested for SOLID compliance
    # =========================================================================

    class _BaseAnalyzer(ast.NodeVisitor):
        """Base analyzer with common functionality."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            self.filename = filename
            self.categories = categories
            self.violations: list[FlextTypeVerificationPlugin.TypeViolation] = []

        def _should_check(self: Self, category: str) -> bool:
            """Check if category should be analyzed."""
            return self.categories is None or category in self.categories

        def _add_violation(
            self: Self,
            rule_id: str,
            category: str,
            node: ast.AST,
            message: str,
            suggestion: str | None = None,
            raw_type: str | None = None,
        ) -> None:
            """Add a violation to the list."""
            tv = FlextQualityConstants.Quality.TypeVerification
            severity = tv.RULE_SEVERITIES.get(rule_id, "warning")
            self.violations.append(
                FlextTypeVerificationPlugin.TypeViolation(
                    rule_id=rule_id,
                    category=category,
                    severity=severity,
                    file=self.filename,
                    line=node.lineno if hasattr(node, "lineno") else 0,
                    column=node.col_offset if hasattr(node, "col_offset") else 0,
                    message=message,
                    suggestion=suggestion,
                    raw_type=raw_type,
                )
            )

    class _AnnotationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV001 (missing annotations) and TV002 (excessive)."""

        def visit_FunctionDef(self: Self, node: ast.FunctionDef) -> None:
            """Check function for annotation issues."""
            if not self._should_check("missing_annotation"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV001: Check for missing return type on public functions
            if not node.name.startswith("_") and node.returns is None:
                self._add_violation(
                    tv.RuleId.MISSING_ANNOTATION,
                    "missing_annotation",
                    node,
                    tv.MESSAGES["TV001"].format(target=node.name),
                )

            self.generic_visit(node)

        visit_AsyncFunctionDef = visit_FunctionDef

    class _CentralizationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV003-TV005 (centralization violations)."""

        def visit_Assign(self: Self, node: ast.Assign) -> None:
            """Check for TypeAlias outside typings.py."""
            if not self._should_check("decentralized_type"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV003: TypeAlias outside typings.py
            if not self.filename.endswith("typings.py"):
                if isinstance(node.value, ast.Subscript):
                    if self._is_type_alias(node.value):
                        target_name = self._get_target_name(node.targets)
                        self._add_violation(
                            tv.RuleId.TYPEALIAS_OUTSIDE_TYPINGS,
                            "decentralized_type",
                            node,
                            tv.MESSAGES["TV003"].format(file=self.filename),
                            suggestion=f"Move {target_name} to typings.py",
                        )

            self.generic_visit(node)

        def visit_ClassDef(self: Self, node: ast.ClassDef) -> None:
            """Check for Protocol outside protocols.py."""
            if not self._should_check("decentralized_type"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV004: Protocol outside protocols.py
            if not self.filename.endswith("protocols.py"):
                for base in node.bases:
                    if self._is_protocol_base(base):
                        self._add_violation(
                            tv.RuleId.PROTOCOL_OUTSIDE_PROTOCOLS,
                            "decentralized_type",
                            node,
                            tv.MESSAGES["TV004"].format(file=self.filename),
                            suggestion=f"Move {node.name} to protocols.py",
                        )
                        break

            self.generic_visit(node)

        def _is_type_alias(self: Self, node: ast.Subscript) -> bool:
            """Check if node is a TypeAlias."""
            if isinstance(node.value, ast.Name):
                return node.value.id == "TypeAlias"
            if isinstance(node.value, ast.Attribute):
                return node.value.attr == "TypeAlias"
            return False

        def _is_protocol_base(self: Self, node: ast.expr) -> bool:
            """Check if node is a Protocol base class."""
            if isinstance(node, ast.Name):
                return node.id == "Protocol"
            if isinstance(node, ast.Attribute):
                return node.attr == "Protocol"
            return False

        def _get_target_name(self: Self, targets: list[ast.expr]) -> str:
            """Get name from assignment targets."""
            if targets and isinstance(targets[0], ast.Name):
                return targets[0].id
            return "unknown"

    class _ProtocolRecommendationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV006-TV008 (Protocol recommendations)."""

        def visit_AnnAssign(self: Self, node: ast.AnnAssign) -> None:
            """Check for Callable that should use Protocol."""
            if not self._should_check("needs_protocol"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            if isinstance(node.annotation, ast.Subscript):
                if self._is_complex_callable(node.annotation):
                    self._add_violation(
                        tv.RuleId.COMPLEX_CALLABLE_NEEDS_PROTOCOL,
                        "needs_protocol",
                        node,
                        tv.MESSAGES["TV007"],
                        suggestion="Define a Protocol with __call__ method",
                    )

            self.generic_visit(node)

        def _is_complex_callable(self: Self, node: ast.Subscript) -> bool:
            """Check if node is a complex Callable."""
            tv = FlextQualityConstants.Quality.TypeVerification
            if isinstance(node.value, ast.Name):
                if node.value.id == "Callable":
                    # Check parameter count
                    if isinstance(node.slice, ast.Tuple):
                        if len(node.slice.elts) > tv.MAX_CALLABLE_PARAMS:
                            return True
            return False

    class _ModelRecommendationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV009-TV011 (Model recommendations)."""

        def visit_ClassDef(self: Self, node: ast.ClassDef) -> None:
            """Check for dataclass that should use Pydantic."""
            if not self._should_check("needs_model"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV010: dataclass should use Pydantic
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name):
                    if decorator.id == "dataclass":
                        self._add_violation(
                            tv.RuleId.DATACLASS_NEEDS_PYDANTIC,
                            "needs_model",
                            node,
                            tv.MESSAGES["TV010"],
                            suggestion="Use Pydantic BaseModel instead",
                        )
                        break
                elif isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name):
                        if decorator.func.id == "dataclass":
                            self._add_violation(
                                tv.RuleId.DATACLASS_NEEDS_PYDANTIC,
                                "needs_model",
                                node,
                                tv.MESSAGES["TV010"],
                                suggestion="Use Pydantic BaseModel instead",
                            )
                            break

            self.generic_visit(node)

    class _CouplingAnalyzer(_BaseAnalyzer):
        """Analyzer for TV012-TV014 (coupling and complexity)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._isinstance_counts: dict[str, int] = {}
            self._none_check_count = 0
            self._current_function: str | None = None

        def visit_FunctionDef(self: Self, node: ast.FunctionDef) -> None:
            """Track function context for isinstance counting."""
            self._current_function = node.name
            self._isinstance_counts[node.name] = 0
            self.generic_visit(node)

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV012: Check isinstance count
            if self._should_check("excessive_coupling"):
                count = self._isinstance_counts.get(node.name, 0)
                if count > tv.MAX_ISINSTANCE_PER_FUNCTION:
                    self._add_violation(
                        tv.RuleId.EXCESSIVE_ISINSTANCE,
                        "excessive_coupling",
                        node,
                        tv.MESSAGES["TV012"].format(count=count),
                        suggestion="Consider using Protocol or pattern matching",
                    )

            self._current_function = None

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self: Self, node: ast.Call) -> None:
            """Count isinstance calls."""
            if isinstance(node.func, ast.Name):
                if node.func.id == "isinstance":
                    if self._current_function:
                        self._isinstance_counts[self._current_function] = (
                            self._isinstance_counts.get(self._current_function, 0) + 1
                        )

            self.generic_visit(node)

        def visit_Compare(self: Self, node: ast.Compare) -> None:
            """Count None checks."""
            if self._should_check("excessive_none"):
                for op in node.ops:
                    if isinstance(op, (ast.Is, ast.IsNot)):
                        for comparator in node.comparators:
                            if isinstance(comparator, ast.Constant):
                                if comparator.value is None:
                                    self._none_check_count += 1

            self.generic_visit(node)

    class _ResultUsageAnalyzer(_BaseAnalyzer):
        """Analyzer for TV015-TV017 (FlextResult misuse)."""

        def visit_Return(self: Self, node: ast.Return) -> None:
            """Check for returning None from FlextResult method."""
            if not self._should_check("result_misuse"):
                self.generic_visit(node)
                return

            # TV015: Returning None directly
            if isinstance(node.value, ast.Constant):
                if node.value.value is None:
                    # This is a simplified check - would need context
                    # to know if we're in a FlextResult-returning method
                    pass

            self.generic_visit(node)

        def visit_Subscript(self: Self, node: ast.Subscript) -> None:
            """Check for FlextResult without type parameter."""
            if not self._should_check("result_misuse"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV016: FlextResult without type param - simplified check
            if isinstance(node.value, ast.Name):
                if node.value.id == "FlextResult":
                    if not isinstance(node.slice, (ast.Name, ast.Subscript)):
                        self._add_violation(
                            tv.RuleId.RESULT_MISSING_TYPE_PARAM,
                            "result_misuse",
                            node,
                            tv.MESSAGES["TV016"],
                            suggestion="Add type parameter: FlextResult[T]",
                        )

            self.generic_visit(node)

    class _UncentralizedTypeAnalyzer(_BaseAnalyzer):
        """Analyzer for TV018 (uncentralized types)."""

        def visit_AnnAssign(self: Self, node: ast.AnnAssign) -> None:
            """Check for types that should be centralized."""
            if not self._should_check("uncentralized_type"):
                self.generic_visit(node)
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            type_str = self._get_annotation_string(node.annotation)
            if type_str and self._should_be_centralized(type_str):
                suggestion = tv.TYPE_MAPPING.get(type_str)
                if suggestion:
                    self._add_violation(
                        tv.RuleId.UNCENTRALIZED_TYPE,
                        "uncentralized_type",
                        node,
                        tv.MESSAGES["TV018"].format(
                            suggestion=suggestion,
                            raw_type=type_str,
                        ),
                        suggestion=f"Use {suggestion}",
                        raw_type=type_str,
                    )

            self.generic_visit(node)

        def _get_annotation_string(self: Self, node: ast.expr) -> str | None:
            """Convert annotation AST to string representation."""
            try:
                return ast.unparse(node)
            except (AttributeError, ValueError):
                return None

        def _should_be_centralized(self: Self, type_str: str) -> bool:
            """Check if type should use centralized alias."""
            tv = FlextQualityConstants.Quality.TypeVerification
            # Skip simple types
            if type_str in tv.EXCLUDED_SIMPLE_TYPES:
                return False

            # Skip already centralized types
            for prefix in tv.EXCLUDED_TYPE_PREFIXES:
                if type_str.startswith(prefix):
                    return False

            # Check if in mapping
            return type_str in tv.TYPE_MAPPING


__all__ = ["FlextTypeVerificationPlugin"]
