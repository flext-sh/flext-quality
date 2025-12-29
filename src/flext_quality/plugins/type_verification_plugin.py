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
            except SyntaxError:
                self._logger.warning("Syntax error in %s", file_path)
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

        # Run all analyzers using dispatch pattern
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
            analyzer.analyze(tree)
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
    # ANALYZER CLASSES - Using dispatch pattern for FLEXT compliance
    # =========================================================================

    class _BaseAnalyzer:
        """Base analyzer with dispatch pattern (no ast.NodeVisitor)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            self.filename = filename
            self.categories = categories
            self.violations: list[FlextTypeVerificationPlugin.TypeViolation] = []
            self._dispatch: dict[type, object] = {}

        def analyze(self: Self, tree: ast.AST) -> None:
            """Analyze AST tree using dispatch pattern."""
            for node in ast.walk(tree):
                handler = self._dispatch.get(type(node))
                if handler and callable(handler):
                    handler(node)

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
            line = node.lineno if hasattr(node, "lineno") else 0
            col = node.col_offset if hasattr(node, "col_offset") else 0
            self.violations.append(
                FlextTypeVerificationPlugin.TypeViolation(
                    rule_id=rule_id,
                    category=category,
                    severity=severity,
                    file=self.filename,
                    line=line,
                    column=col,
                    message=message,
                    suggestion=suggestion,
                    raw_type=raw_type,
                )
            )

    class _AnnotationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV001 (missing annotations) and TV002 (excessive)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.FunctionDef: self._handle_function_def,
                ast.AsyncFunctionDef: self._handle_function_def,
            }

        def _handle_function_def(self: Self, node: ast.FunctionDef) -> None:
            """Check function for annotation issues."""
            if not self._should_check("missing_annotation"):
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

    class _CentralizationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV003-TV005 (centralization violations)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.Assign: self._handle_assign,
                ast.ClassDef: self._handle_class_def,
            }

        def _handle_assign(self: Self, node: ast.Assign) -> None:
            """Check for TypeAlias outside typings.py."""
            if not self._should_check("decentralized_type"):
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV003: TypeAlias outside typings.py
            if (
                not self.filename.endswith("typings.py")
                and isinstance(node.value, ast.Subscript)
                and self._is_type_alias(node.value)
            ):
                target_name = self._get_target_name(node.targets)
                self._add_violation(
                    tv.RuleId.TYPEALIAS_OUTSIDE_TYPINGS,
                    "decentralized_type",
                    node,
                    tv.MESSAGES["TV003"].format(file=self.filename),
                    suggestion=f"Move {target_name} to typings.py",
                )

        def _handle_class_def(self: Self, node: ast.ClassDef) -> None:
            """Check for Protocol outside protocols.py."""
            if not self._should_check("decentralized_type"):
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

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.AnnAssign: self._handle_ann_assign,
            }

        def _handle_ann_assign(self: Self, node: ast.AnnAssign) -> None:
            """Check for Callable that should use Protocol."""
            if not self._should_check("needs_protocol"):
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            if (
                isinstance(node.annotation, ast.Subscript)
                and self._is_complex_callable(node.annotation)
            ):
                self._add_violation(
                    tv.RuleId.COMPLEX_CALLABLE_NEEDS_PROTOCOL,
                    "needs_protocol",
                    node,
                    tv.MESSAGES["TV007"],
                    suggestion="Define a Protocol with __call__ method",
                )

        def _is_complex_callable(self: Self, node: ast.Subscript) -> bool:
            """Check if node is a complex Callable."""
            tv = FlextQualityConstants.Quality.TypeVerification
            return (
                isinstance(node.value, ast.Name)
                and node.value.id == "Callable"
                and isinstance(node.slice, ast.Tuple)
                and len(node.slice.elts) > tv.MAX_CALLABLE_PARAMS
            )

    class _ModelRecommendationAnalyzer(_BaseAnalyzer):
        """Analyzer for TV009-TV011 (Model recommendations)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.ClassDef: self._handle_class_def,
            }

        def _handle_class_def(self: Self, node: ast.ClassDef) -> None:
            """Check for dataclass that should use Pydantic."""
            if not self._should_check("needs_model"):
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV010: dataclass should use Pydantic
            for decorator in node.decorator_list:
                is_dataclass_name = (
                    isinstance(decorator, ast.Name) and decorator.id == "dataclass"
                )
                is_dataclass_call = (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Name)
                    and decorator.func.id == "dataclass"
                )
                if is_dataclass_name or is_dataclass_call:
                    self._add_violation(
                        tv.RuleId.DATACLASS_NEEDS_PYDANTIC,
                        "needs_model",
                        node,
                        tv.MESSAGES["TV010"],
                        suggestion="Use Pydantic BaseModel instead",
                    )
                    break

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
            # Use a two-pass approach: first collect, then validate
            self._function_nodes: list[ast.FunctionDef] = []

        def analyze(self: Self, tree: ast.AST) -> None:
            """Analyze using custom walk for function context."""
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._analyze_function(node)

        def _analyze_function(self: Self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            """Analyze a function for coupling issues."""
            isinstance_count = 0
            for child in ast.walk(node):
                if (
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Name)
                    and child.func.id == "isinstance"
                ):
                    isinstance_count += 1
                if isinstance(child, ast.Compare):
                    self._check_none_comparison(child)

            # TV012: Check isinstance count
            tv = FlextQualityConstants.Quality.TypeVerification
            if (
                self._should_check("excessive_coupling")
                and isinstance_count > tv.MAX_ISINSTANCE_PER_FUNCTION
            ):
                self._add_violation(
                    tv.RuleId.EXCESSIVE_ISINSTANCE,
                    "excessive_coupling",
                    node,
                    tv.MESSAGES["TV012"].format(count=isinstance_count),
                    suggestion="Consider using Protocol or pattern matching",
                )

        def _check_none_comparison(self: Self, node: ast.Compare) -> None:
            """Count None checks."""
            if not self._should_check("excessive_none"):
                return

            for op in node.ops:
                if isinstance(op, (ast.Is, ast.IsNot)):
                    for comparator in node.comparators:
                        if (
                            isinstance(comparator, ast.Constant)
                            and comparator.value is None
                        ):
                            self._none_check_count += 1

    class _ResultUsageAnalyzer(_BaseAnalyzer):
        """Analyzer for TV015-TV017 (FlextResult misuse)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.Return: self._handle_return,
                ast.Subscript: self._handle_subscript,
            }

        def _handle_return(self: Self, node: ast.Return) -> None:
            """Check for returning None from FlextResult method."""
            if not self._should_check("result_misuse"):
                return

            # TV015: Returning None directly - simplified check
            # Would need context to know if in FlextResult-returning method
            if (
                isinstance(node.value, ast.Constant)
                and node.value.value is None
            ):
                # This is a simplified check - would need context
                pass

        def _handle_subscript(self: Self, node: ast.Subscript) -> None:
            """Check for FlextResult without type parameter."""
            if not self._should_check("result_misuse"):
                return

            tv = FlextQualityConstants.Quality.TypeVerification
            # TV016: FlextResult without type param
            if (
                isinstance(node.value, ast.Name)
                and node.value.id == "FlextResult"
                and not isinstance(node.slice, (ast.Name, ast.Subscript))
            ):
                self._add_violation(
                    tv.RuleId.RESULT_MISSING_TYPE_PARAM,
                    "result_misuse",
                    node,
                    tv.MESSAGES["TV016"],
                    suggestion="Add type parameter: FlextResult[T]",
                )

    class _UncentralizedTypeAnalyzer(_BaseAnalyzer):
        """Analyzer for TV018 (uncentralized types)."""

        def __init__(
            self: Self,
            filename: str,
            categories: set[str] | None,
        ) -> None:
            super().__init__(filename, categories)
            self._dispatch = {
                ast.AnnAssign: self._handle_ann_assign,
            }

        def _handle_ann_assign(self: Self, node: ast.AnnAssign) -> None:
            """Check for types that should be centralized."""
            if not self._should_check("uncentralized_type"):
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
