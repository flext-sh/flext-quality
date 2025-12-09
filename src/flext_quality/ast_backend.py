"""AST-based analysis backend for detailed code structure analysis.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import override

from flext_core import FlextContainer, FlextLogger, FlextResult

from .ast_class_info import FlextQualityASTClassInfo
from .ast_function_info import FlextQualityASTFunctionInfo
from .backend_type import BackendType
from .base import BaseAnalyzer


class FlextQualityASTBackend(BaseAnalyzer):
    """Unified AST backend class following FLEXT architecture patterns.

    Single responsibility: AST-based code analysis
    Contains all AST analysis functionality as nested classes with shared resources.
    """

    def __init__(self) -> None:
        """Initialize AST backend with dependency injection."""
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    class _ASTVisitor(ast.NodeVisitor):
        """Nested AST visitor to extract detailed code structure information."""

        def __init__(self, file_path: Path, package_name: str) -> None:
            """Initialize AST visitor with file path and package name."""
            super().__init__()
            self.file_path = file_path
            self.package_name = package_name
            self.current_class: FlextQualityASTClassInfo.ClassInfo | None = None
            self.current_function: FlextQualityASTFunctionInfo.FunctionInfo | None = (
                None
            )
            self.scope_stack: list[str] = []

            # Results - using strongly typed models
            self.classes: list[FlextQualityASTClassInfo.ClassInfo] = []
            self.functions: list[FlextQualityASTFunctionInfo.FunctionInfo] = []
            self.variables: list[
                dict[str, object]
            ] = []  # Keeping as generic dict[str, object] with object values
            self.imports: list[
                dict[str, object]
            ] = []  # Keeping as generic dict[str, object] with object values
            self.constants: list[
                dict[str, object]
            ] = []  # Keeping as generic dict[str, object] with object values

            # Context tracking
            self.class_stack: list[FlextQualityASTClassInfo.ClassInfo] = []
            self.function_stack: list[FlextQualityASTFunctionInfo.FunctionInfo] = []

        @override
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            """Visit a class definition."""
            # Extract class analysis into smaller helper methods
            full_name = self._calculate_class_full_name(node)
            base_classes = self._extract_base_classes(node)
            decorators, is_dataclass, is_abstract = self._analyze_class_decorators(node)
            method_counts = self._count_class_methods(node)

            class_info = FlextQualityASTClassInfo.ClassInfo(
                name=node.name,
                full_name=full_name,
                file_path=str(self.file_path),
                package_name=self.package_name,
                line_number=node.lineno,
                end_line_number=getattr(node, "end_lineno", node.lineno),
                base_classes=base_classes,
                decorators=decorators,
                is_dataclass=is_dataclass,
                is_abstract=is_abstract,
                has_docstring=ast.get_docstring(node) is not None,
                **method_counts,
            )

            self.classes.append(class_info)
            self.class_stack.append(class_info)
            self.current_class = class_info

            # Visit child nodes
            self.generic_visit(node)

            # Pop class from stack
            self.class_stack.pop()
            self.current_class = self.class_stack[-1] if self.class_stack else None

        @override
        def visit_FunctionDef(
            self,
            node: ast.FunctionDef,
        ) -> None:
            """Visit a function or method definition."""
            function_info = FlextQualityASTFunctionInfo.FunctionInfo(
                name=node.name,
                full_name=self._calculate_function_full_name(node),
                file_path=str(self.file_path),
                package_name=self.package_name,
                line_number=node.lineno,
                end_line_number=getattr(node, "end_lineno", node.lineno),
                decorators=[
                    self._get_name_from_node(dec) for dec in node.decorator_list
                ],
                is_generator=self._check_is_generator(node),
                is_method=self.current_class is not None,
                is_property=self._check_is_property(node),
                is_class_method=self._check_is_classmethod(node),
                is_static_method=self._check_is_staticmethod(node),
                parameter_count=len(node.args.args),
                returns_annotation=self._get_return_annotation(node),
                complexity=self._calculate_complexity(node),
                docstring=ast.get_docstring(node),
            )

            self.functions.append(function_info)
            self.function_stack.append(function_info)
            self.current_function = function_info

            # Visit child nodes
            self.generic_visit(node)

            # Pop function from stack
            self.function_stack.pop()
            self.current_function = (
                self.function_stack[-1] if self.function_stack else None
            )

        def _calculate_class_full_name(self, node: ast.ClassDef) -> str:
            """Calculate the full name of a class."""
            if self.current_class:
                return f"{self.current_class.full_name}.{node.name}"
            return (
                f"{self.package_name}.{node.name}" if self.package_name else node.name
            )

        def _extract_base_classes(
            self,
            node: ast.ClassDef,
        ) -> list[str]:
            """Extract base class names."""
            return [self._get_name_from_node(base) for base in node.bases]

        def _analyze_class_decorators(
            self,
            node: ast.ClassDef,
        ) -> tuple[list[str], bool, bool]:
            """Analyze class decorators."""
            decorators = [self._get_name_from_node(dec) for dec in node.decorator_list]
            is_dataclass: bool = any("dataclass" in dec for dec in decorators)
            is_abstract = any("abstractmethod" in dec for dec in decorators)
            return decorators, is_dataclass, is_abstract

        def _count_class_methods(self, node: ast.ClassDef) -> dict[str, int]:
            """Count different types of methods in a class."""
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            return {
                "method_count": len(methods),
                "public_methods": len(
                    [m for m in methods if not m.name.startswith("_")],
                ),
                "private_methods": len([m for m in methods if m.name.startswith("__")]),
                "protected_methods": len(
                    [
                        m
                        for m in methods
                        if m.name.startswith("_") and not m.name.startswith("__")
                    ],
                ),
            }

        def _calculate_function_full_name(
            self,
            node: ast.FunctionDef,
        ) -> str:
            """Calculate the full name of a function."""
            if self.current_class:
                return f"{self.current_class.full_name}.{node.name}"
            return (
                f"{self.package_name}.{node.name}" if self.package_name else node.name
            )

        def _check_type_hints(
            self,
            node: ast.FunctionDef,
        ) -> bool:
            """Check if function has type hints."""
            return node.returns is not None or any(
                arg.annotation for arg in node.args.args
            )

        def _calculate_complexity(
            self,
            node: ast.FunctionDef,
        ) -> int:
            """Calculate cyclomatic complexity of a function."""
            complexity = 1  # Base complexity
            for child in ast.walk(node):
                if isinstance(
                    child,
                    (ast.If, ast.While, ast.For, ast.ExceptHandler),
                ):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            return complexity

        def _get_name_from_node(self, node: ast.AST) -> str:
            """Get name from an AST node."""
            if isinstance(node, ast.Name):
                return node.id
            if isinstance(node, ast.Attribute):
                return f"{self._get_name_from_node(node.value)}.{node.attr}"
            return str(node)

        def _check_is_generator(
            self,
            node: ast.FunctionDef,
        ) -> bool:
            """Check if function is a generator (contains yield)."""
            for child in ast.walk(node):
                if isinstance(child, (ast.Yield, ast.YieldFrom)):
                    return True
            return False

        def _check_is_property(
            self,
            node: ast.FunctionDef,
        ) -> bool:
            """Check if function is a property."""
            return any(
                self._get_name_from_node(dec).endswith("property")
                for dec in node.decorator_list
            )

        def _check_is_classmethod(
            self,
            node: ast.FunctionDef,
        ) -> bool:
            """Check if function is a classmethod."""
            return any(
                self._get_name_from_node(dec) == "classmethod"
                for dec in node.decorator_list
            )

        def _check_is_staticmethod(
            self,
            node: ast.FunctionDef,
        ) -> bool:
            """Check if function is a staticmethod."""
            return any(
                self._get_name_from_node(dec) == "staticmethod"
                for dec in node.decorator_list
            )

        def _get_return_annotation(
            self,
            node: ast.FunctionDef,
        ) -> str | None:
            """Get return type annotation as string."""
            if node.returns:
                return ast.unparse(node.returns)
            return None

    @override
    def get_backend_type(self: object) -> BackendType:
        """Return the backend type."""
        return BackendType.AST

    @override
    def get_capabilities(self: object) -> list[str]:
        """Return the capabilities of this backend."""
        return ["complexity", "functions", "classes", "imports", "docstrings"]

    @override
    def analyze(
        self, _code: str, file_path: Path | None = None
    ) -> FlextResult[dict[str, object]]:
        """Analyze Python code using AST.

        Args:
            _code: Python source code to analyze
            file_path: Optional file path for context

        Returns:
            FlextResult containing analysis results dictionary

        """
        result: dict[str, object] = {}

        if file_path:
            result["file_path"] = str(file_path)

        try:
            tree = ast.parse(_code)

            # Extract various metrics
            result["functions"] = self._extract_functions(tree)
            result["classes"] = self._extract_classes(tree)
            result["complexity"] = self._calculate_complexity(tree)
            result["imports"] = self._extract_imports(tree)

            # Check for missing docstrings
            missing_docs = self._check_docstrings(tree)
            if missing_docs:
                result["missing_docstrings"] = missing_docs

        except SyntaxError as e:
            return FlextResult.fail(f"Syntax error: {e}")

        return FlextResult.ok(result)

    def _extract_functions(self, tree: ast.AST) -> list[dict[str, object]]:
        """Extract function information from AST."""
        functions: list[dict[str, object]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info: dict[str, object] = {
                    "name": node.name,
                    "args": len(node.args.args),
                    "lineno": node.lineno,
                    "is": isinstance(node, ast.FunctionDef),
                }
                functions.append(func_info)
        return functions

    def _extract_classes(self, tree: ast.AST) -> list[dict[str, object]]:
        """Extract class information from AST."""
        classes: list[dict[str, object]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count methods
                sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
                class_info: dict[str, object] = {
                    "name": node.name,
                    "methods": "methods",
                    "lineno": node.lineno,
                    "bases": [
                        base.id if isinstance(base, ast.Name) else str(base)
                        for base in node.bases
                    ],
                }
                classes.append(class_info)
        return classes

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
        return complexity

    def _extract_imports(self, tree: ast.AST) -> list[dict[str, object]]:
        """Extract import information."""
        imports: list[dict[str, object]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(
                    [{"module": alias.name, "names": []} for alias in node.names],
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(
                    {
                        "module": node.module,
                        "names": [alias.name for alias in node.names],
                    },
                )
        return imports

    def _check_docstrings(self, tree: ast.AST) -> list[str]:
        """Check for missing docstrings."""
        return [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and not ast.get_docstring(node)
        ]

    def create_visitor(self, file_path: Path, package_name: str) -> object:
        """Create an AST visitor instance.

        Public factory method for creating AST visitor instances.
        This provides a proper interface instead of accessing private members.

        Args:
        file_path: Path to the file being analyzed
        package_name: Name of the package containing the file

        Returns:
        AST visitor instance for code analysis.

        """
        return self._ASTVisitor(file_path, package_name)
