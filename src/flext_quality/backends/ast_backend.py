"""AST-based analysis backend for detailed code structure analysis."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from flext_quality.backends.base import (
    BackendType,
    BaseAnalyzer,
)

if TYPE_CHECKING:
    from pathlib import Path


class ASTVisitor(ast.NodeVisitor):
    """AST visitor to extract detailed code structure information."""

    def __init__(self, file_path: Path, package_name: str) -> None:
        """Initialize AST visitor with file path and package name."""
        self.file_path = file_path
        self.package_name = package_name
        self.current_class: dict[str, object] | None = None
        self.current_function: dict[str, object] | None = None
        self.scope_stack: list[str] = []

        # Results
        self.classes: list[dict[str, object]] = []
        self.functions: list[dict[str, object]] = []
        self.variables: list[dict[str, object]] = []
        self.imports: list[dict[str, object]] = []
        self.constants: list[dict[str, object]] = []

        # Context tracking
        self.class_stack: list[dict[str, object]] = []
        self.function_stack: list[dict[str, object]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition."""
        # Extract class analysis into smaller helper methods
        full_name = self._calculate_class_full_name(node)
        base_classes = self._extract_base_classes(node)
        decorators, is_dataclass, is_abstract = self._analyze_class_decorators(node)
        method_counts = self._count_class_methods(node)

        class_info = {
            "name": node.name,
            "full_name": full_name,
            "file_path": str(self.file_path),
            "package_name": self.package_name,
            "line_number": node.lineno,
            "end_line_number": getattr(node, "end_lineno", node.lineno),
            "base_classes": base_classes,
            "decorators": decorators,
            "is_dataclass": is_dataclass,
            "is_abstract": is_abstract,
            "has_docstring": ast.get_docstring(node) is not None,
            **method_counts,
        }

        self.classes.append(class_info)
        self.class_stack.append(class_info)
        self.current_class = class_info

        # Visit child nodes
        self.generic_visit(node)

        # Pop class from stack
        self.class_stack.pop()
        self.current_class = self.class_stack[-1] if self.class_stack else None

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        """Visit a function or method definition."""
        function_info = {
            "name": node.name,
            "full_name": self._calculate_function_full_name(node),
            "file_path": str(self.file_path),
            "package_name": self.package_name,
            "line_number": node.lineno,
            "end_line_number": getattr(node, "end_lineno", node.lineno),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "is_method": self.current_class is not None,
            "class_name": self.current_class["name"] if self.current_class else None,
            "has_docstring": ast.get_docstring(node) is not None,
            "argument_count": len(node.args.args),
            "has_type_hints": self._check_type_hints(node),
            "cyclomatic_complexity": self._calculate_complexity(node),
        }

        self.functions.append(function_info)
        self.function_stack.append(function_info)
        self.current_function = function_info

        # Visit child nodes
        self.generic_visit(node)

        # Pop function from stack
        self.function_stack.pop()
        self.current_function = self.function_stack[-1] if self.function_stack else None

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit an async function definition."""
        self.visit_FunctionDef(node)

    def _calculate_class_full_name(self, node: ast.ClassDef) -> str:
        """Calculate the full name of a class."""
        if self.current_class:
            return f"{self.current_class['full_name']}.{node.name}"
        return f"{self.package_name}.{node.name}" if self.package_name else node.name

    def _extract_base_classes(self, node: ast.ClassDef) -> list[str]:
        """Extract base class names."""
        return [self._get_name_from_node(base) for base in node.bases]

    def _analyze_class_decorators(
        self,
        node: ast.ClassDef,
    ) -> tuple[list[str], bool, bool]:
        """Analyze class decorators."""
        decorators = [self._get_name_from_node(dec) for dec in node.decorator_list]
        is_dataclass = any("dataclass" in dec for dec in decorators)
        is_abstract = any("abstractmethod" in dec for dec in decorators)
        return decorators, is_dataclass, is_abstract

    def _count_class_methods(self, node: ast.ClassDef) -> dict[str, int]:
        """Count different types of methods in a class."""
        methods = [
            n
            for n in node.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        return {
            "method_count": len(methods),
            "public_methods": len([m for m in methods if not m.name.startswith("_")]),
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
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> str:
        """Calculate the full name of a function."""
        if self.current_class:
            return f"{self.current_class['full_name']}.{node.name}"
        return f"{self.package_name}.{node.name}" if self.package_name else node.name

    def _check_type_hints(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function has type hints."""
        return node.returns is not None or any(arg.annotation for arg in node.args.args)

    def _calculate_complexity(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(
                child,
                (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler),
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


class ASTBackend(BaseAnalyzer):
    """AST-based analysis backend."""

    def get_backend_type(self) -> BackendType:
        """Return the backend type."""
        return BackendType.AST

    def get_capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        return ["complexity", "functions", "classes", "imports", "docstrings"]

    def analyze(self, code: str, file_path: Path | None = None) -> dict[str, object]:
        """Analyze Python code using AST.

        Args:
            code: Python source code to analyze
            file_path: Optional file path for context

        Returns:
            Dictionary with analysis results

        """
        result: dict[str, object] = {}

        if file_path:
            result["file_path"] = str(file_path)

        try:
            tree = ast.parse(code)

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
            result["error"] = f"Syntax error: {e}"

        return result

    def _extract_functions(self, tree: ast.AST) -> list[dict[str, object]]:
        """Extract function information from AST."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_info = {
                    "name": node.name,
                    "args": len(node.args.args),
                    "lineno": node.lineno,
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                }
                functions.append(func_info)
        return functions

    def _extract_classes(self, tree: ast.AST) -> list[dict[str, object]]:
        """Extract class information from AST."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count methods
                methods = sum(
                    1
                    for item in node.body
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
                class_info = {
                    "name": node.name,
                    "methods": methods,
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
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not ast.get_docstring(node)
        ]
