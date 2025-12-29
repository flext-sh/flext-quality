# VERIFIED_NEW_MODULE
"""Code transformer using libcst for safe AST-based transformations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides libcst-based code transformations that preserve formatting.
Used for:
- Adding/removing imports
- Modifying class inheritance
- Nesting/unnesting code blocks
- Safe code refactoring

Usage:
    from flext_quality.code_transformer import FlextQualityCodeTransformer

    transformer = FlextQualityCodeTransformer()

    # Add statement to source
    result = transformer.statements.inject("from typing import Self", source)

    # Change class base
    result = transformer.classes.change_base(source, "MyClass", "OldBase", "NewBase")
"""

from __future__ import annotations

from pathlib import Path
from typing import Self

import libcst as cst
from flext_core import FlextLogger, FlextResult


class FlextQualityCodeTransformer:
    """Base class for libcst-based code transformations.

    Provides safe code manipulation that preserves:
    - Formatting and whitespace
    - Comments
    - Original structure

    All transformations use CST (Concrete Syntax Tree) instead of
    string manipulation to ensure correctness.
    """

    def __init__(self: Self) -> None:
        """Initialize transformer with logger."""
        self._logger = FlextLogger(__name__)
        self.statements = self.StatementTransformer(self._logger)
        self.classes = self.ClassTransformer(self._logger)
        self.indentation = self.IndentationTransformer(self._logger)

    # =========================================================================
    # Nested Helper Classes (CST Transformers)
    # =========================================================================

    class _RemoveStatementVisitor(cst.CSTTransformer):
        """Remove statements from a specific module."""

        def __init__(self: Self, module_name: str) -> None:
            """Initialize with module name to remove."""
            super().__init__()
            self.module_name = module_name

        def leave_ImportFrom(
            self: Self,
            original_node: cst.ImportFrom,
            updated_node: cst.ImportFrom,
        ) -> cst.ImportFrom | cst.RemovalSentinel:
            """Remove ImportFrom if it matches the target module."""
            if updated_node.module is not None:
                module_str = FlextQualityCodeTransformer.Helpers.get_dotted_name(
                    updated_node.module
                )
                if module_str == self.module_name or module_str.startswith(
                    f"{self.module_name}."
                ):
                    return cst.RemovalSentinel.REMOVE
            return updated_node

    class _StatementCheckerVisitor(cst.CSTVisitor):
        """Check if source has statement from specific module."""

        def __init__(self: Self, module_name: str) -> None:
            """Initialize with module name to find."""
            super().__init__()
            self.module_name = module_name
            self.found = False

        def visit_ImportFrom(self: Self, node: cst.ImportFrom) -> bool:
            """Check ImportFrom nodes."""
            if node.module is not None:
                module_str = FlextQualityCodeTransformer.Helpers.get_dotted_name(
                    node.module
                )
                if module_str == self.module_name or module_str.startswith(
                    f"{self.module_name}."
                ):
                    self.found = True
            return False

    class _ChangeBaseClassVisitor(cst.CSTTransformer):
        """Change a class's base class."""

        def __init__(
            self: Self, class_name: str, old_base: str, new_base: str
        ) -> None:
            """Initialize with class and base names."""
            super().__init__()
            self.class_name = class_name
            self.old_base = old_base
            self.new_base = new_base

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef:
            """Replace base class if it matches."""
            if updated_node.name.value != self.class_name:
                return updated_node

            new_bases: list[cst.Arg] = []
            for base in updated_node.bases:
                if (
                    isinstance(base.value, cst.Name)
                    and base.value.value == self.old_base
                ):
                    new_bases.append(base.with_changes(value=cst.Name(self.new_base)))
                elif isinstance(base.value, cst.Attribute):
                    base_str = FlextQualityCodeTransformer.Helpers.get_dotted_name(
                        base.value
                    )
                    if base_str == self.old_base:
                        new_bases.append(
                            base.with_changes(
                                value=FlextQualityCodeTransformer.Helpers.create_dotted_name(
                                    self.new_base
                                )
                            )
                        )
                    else:
                        new_bases.append(base)
                else:
                    new_bases.append(base)

            return updated_node.with_changes(bases=new_bases)

    class _AddBaseClassVisitor(cst.CSTTransformer):
        """Add a base class to an existing class."""

        def __init__(self: Self, class_name: str, new_base: str) -> None:
            """Initialize with class and new base names."""
            super().__init__()
            self.class_name = class_name
            self.new_base = new_base

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef:
            """Add base class if it matches the target class."""
            if updated_node.name.value != self.class_name:
                return updated_node

            new_base_arg = cst.Arg(
                value=FlextQualityCodeTransformer.Helpers.create_dotted_name(
                    self.new_base
                )
            )
            new_bases = [*updated_node.bases, new_base_arg]

            return updated_node.with_changes(bases=new_bases)

    class _ClassFinderVisitor(cst.CSTVisitor):
        """Find all classes in source code."""

        def __init__(self: Self) -> None:
            """Initialize class finder."""
            super().__init__()
            self.classes: list[dict[str, str | list[str] | int]] = []

        def visit_ClassDef(self: Self, node: cst.ClassDef) -> bool:
            """Record class information."""
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base.value, cst.Name):
                    bases.append(base.value.value)
                elif isinstance(base.value, cst.Attribute):
                    bases.append(
                        FlextQualityCodeTransformer.Helpers.get_dotted_name(base.value)
                    )

            self.classes.append({
                "name": node.name.value,
                "bases": bases,
            })
            return True

    class _NestInClassVisitor(cst.CSTTransformer):
        """Move top-level functions into a class as methods."""

        def __init__(self: Self, class_name: str, function_names: list[str]) -> None:
            """Initialize with class and function names."""
            super().__init__()
            self.class_name = class_name
            self.function_names = function_names
            self.functions_to_add: list[cst.FunctionDef] = []

        def leave_FunctionDef(
            self: Self,
            original_node: cst.FunctionDef,
            updated_node: cst.FunctionDef,
        ) -> cst.FunctionDef | cst.RemovalSentinel:
            """Remove function if it should be nested."""
            if updated_node.name.value in self.function_names:
                self.functions_to_add.append(updated_node)
                return cst.RemovalSentinel.REMOVE
            return updated_node

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef:
            """Add functions to target class."""
            if updated_node.name.value != self.class_name:
                return updated_node

            if not self.functions_to_add:
                return updated_node

            # Add self parameter to functions
            new_methods: list[cst.BaseStatement] = []
            for func in self.functions_to_add:
                self_param = cst.Param(name=cst.Name("self"))
                new_params = [self_param, *func.params.params]
                new_func = func.with_changes(
                    params=func.params.with_changes(params=new_params)
                )
                new_methods.append(new_func)

            new_body = updated_node.body.with_changes(
                body=[*updated_node.body.body, *new_methods]
            )
            return updated_node.with_changes(body=new_body)

    class _ExtractFromClassVisitor(cst.CSTTransformer):
        """Extract methods from a class to top-level functions."""

        def __init__(self: Self, class_name: str, method_names: list[str]) -> None:
            """Initialize with class and method names."""
            super().__init__()
            self.class_name = class_name
            self.method_names = method_names
            self.extracted_functions: list[cst.FunctionDef] = []

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef | cst.FlattenSentinel[cst.BaseStatement]:
            """Extract methods from target class."""
            if updated_node.name.value != self.class_name:
                return updated_node

            remaining_body: list[cst.BaseStatement] = []
            extracted: list[cst.FunctionDef] = []

            for stmt in updated_node.body.body:
                if (
                    isinstance(stmt, cst.FunctionDef)
                    and stmt.name.value in self.method_names
                ):
                    # Remove self parameter
                    params = [p for p in stmt.params.params if p.name.value != "self"]
                    extracted_func = stmt.with_changes(
                        params=stmt.params.with_changes(params=params)
                    )
                    extracted.append(extracted_func)
                else:
                    remaining_body.append(stmt)

            if not extracted:
                return updated_node

            new_class = updated_node.with_changes(
                body=updated_node.body.with_changes(body=remaining_body)
            )

            # Return class followed by extracted functions
            return cst.FlattenSentinel([new_class, *extracted])

    # =========================================================================
    # Helper Methods (nested class for static utilities)
    # =========================================================================

    class Helpers:
        """Static helper methods for CST manipulation."""

        @staticmethod
        def get_dotted_name(node: cst.Attribute | cst.Name) -> str:
            """Get dotted name string from CST node."""
            if isinstance(node, cst.Name):
                return node.value
            if isinstance(node, cst.Attribute):
                prefix = FlextQualityCodeTransformer.Helpers.get_dotted_name(node.value)
                return f"{prefix}.{node.attr.value}"
            return ""

        @staticmethod
        def create_dotted_name(name: str) -> cst.BaseExpression:
            """Create CST node from dotted name string."""
            parts = name.split(".")
            if len(parts) == 1:
                return cst.Name(parts[0])

            result: cst.BaseExpression = cst.Name(parts[0])
            for part in parts[1:]:
                result = cst.Attribute(value=result, attr=cst.Name(part))
            return result

    # =========================================================================
    # Public API Classes
    # =========================================================================

    class StatementTransformer:
        """Add, remove, and reorganize statements using CST."""

        def __init__(self: Self, logger: FlextLogger) -> None:
            """Initialize statement transformer."""
            self._logger = logger

        def inject(
            self: Self,
            stmt: str,
            source: str,
        ) -> FlextResult[str]:
            """Inject a statement to source code.

            Args:
                stmt: Statement to add (e.g., "from typing import Self").
                source: Source code to modify.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                new_stmt = cst.parse_statement(stmt)

                # Find position after existing statements of same type
                new_body: list[cst.BaseStatement | cst.SimpleStatementLine] = []
                stmt_section_ended = False

                for existing in module.body:
                    if not stmt_section_ended:
                        if isinstance(existing, cst.SimpleStatementLine):
                            # Check if it's a similar statement type
                            for item in existing.body:
                                if isinstance(item, cst.Import | cst.ImportFrom):
                                    new_body.append(existing)
                                    continue
                        stmt_section_ended = True
                        # Add new statement here
                        new_body.append(new_stmt)
                    new_body.append(existing)

                # If no similar statements found, add at beginning (after docstring)
                if not any(
                    isinstance(s, cst.SimpleStatementLine)
                    and any(isinstance(i, cst.Import | cst.ImportFrom) for i in s.body)
                    for s in module.body
                ):
                    has_docstring = (
                        len(module.body) > 0
                        and isinstance(module.body[0], cst.SimpleStatementLine)
                        and isinstance(module.body[0].body[0], cst.Expr)
                        and isinstance(module.body[0].body[0].value, cst.SimpleString)
                    )
                    if has_docstring:
                        new_body = [module.body[0], new_stmt, *module.body[1:]]
                    else:
                        new_body = [new_stmt, *module.body]

                new_module = module.with_changes(body=new_body)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

        def remove_from_module(
            self: Self,
            module_name: str,
            source: str,
        ) -> FlextResult[str]:
            """Remove statements from a specific module.

            Args:
                module_name: Module name to remove statements from.
                source: Source code to modify.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                transformer = FlextQualityCodeTransformer._RemoveStatementVisitor(
                    module_name
                )
                new_module = module.visit(transformer)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

        def has_module(
            self: Self,
            module_name: str,
            source: str,
        ) -> FlextResult[bool]:
            """Check if source has statement from specific module.

            Args:
                module_name: Module name to look for.
                source: Source code to check.

            Returns:
                FlextResult with True if statement exists.

            """
            try:
                module = cst.parse_module(source)
                checker = FlextQualityCodeTransformer._StatementCheckerVisitor(
                    module_name
                )
                module.walk(checker)
                return FlextResult[bool].ok(checker.found)

            except cst.ParserSyntaxError as e:
                return FlextResult[bool].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[bool].fail(f"Check error: {e}")

    class ClassTransformer:
        """Modify class definitions using CST."""

        def __init__(self: Self, logger: FlextLogger) -> None:
            """Initialize class transformer."""
            self._logger = logger

        def change_base(
            self: Self,
            source: str,
            class_name: str,
            old_base: str,
            new_base: str,
        ) -> FlextResult[str]:
            """Change a class's base class.

            Args:
                source: Source code to modify.
                class_name: Name of class to modify.
                old_base: Current base class name.
                new_base: New base class name.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                transformer = FlextQualityCodeTransformer._ChangeBaseClassVisitor(
                    class_name, old_base, new_base
                )
                new_module = module.visit(transformer)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

        def append_base(
            self: Self,
            source: str,
            class_name: str,
            new_base: str,
        ) -> FlextResult[str]:
            """Add a base class to an existing class.

            Args:
                source: Source code to modify.
                class_name: Name of class to modify.
                new_base: Base class to add.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                transformer = FlextQualityCodeTransformer._AddBaseClassVisitor(
                    class_name, new_base
                )
                new_module = module.visit(transformer)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

        def find_classes(
            self: Self,
            source: str,
        ) -> FlextResult[list[dict[str, str | list[str] | int]]]:
            """Find all classes in source code.

            Args:
                source: Source code to analyze.

            Returns:
                FlextResult with list of class info dicts.

            """
            try:
                module = cst.parse_module(source)
                finder = FlextQualityCodeTransformer._ClassFinderVisitor()
                module.walk(finder)
                return FlextResult[list[dict[str, str | list[str] | int]]].ok(
                    finder.classes
                )

            except cst.ParserSyntaxError as e:
                return FlextResult[list[dict[str, str | list[str] | int]]].fail(
                    f"Parse error: {e}"
                )
            except Exception as e:
                return FlextResult[list[dict[str, str | list[str] | int]]].fail(
                    f"Find error: {e}"
                )

    class IndentationTransformer:
        """Nest and unnest code blocks using CST."""

        def __init__(self: Self, logger: FlextLogger) -> None:
            """Initialize indentation transformer."""
            self._logger = logger

        def nest_in_class(
            self: Self,
            source: str,
            class_name: str,
            function_names: list[str],
        ) -> FlextResult[str]:
            """Move top-level functions into a class as methods.

            Args:
                source: Source code to modify.
                class_name: Target class name.
                function_names: Functions to move into the class.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                transformer = FlextQualityCodeTransformer._NestInClassVisitor(
                    class_name, function_names
                )
                new_module = module.visit(transformer)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

        def extract_from_class(
            self: Self,
            source: str,
            class_name: str,
            method_names: list[str],
        ) -> FlextResult[str]:
            """Extract methods from a class to top-level functions.

            Args:
                source: Source code to modify.
                class_name: Source class name.
                method_names: Methods to extract.

            Returns:
                FlextResult with modified source or error.

            """
            try:
                module = cst.parse_module(source)
                transformer = FlextQualityCodeTransformer._ExtractFromClassVisitor(
                    class_name, method_names
                )
                new_module = module.visit(transformer)
                return FlextResult[str].ok(new_module.code)

            except cst.ParserSyntaxError as e:
                return FlextResult[str].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[str].fail(f"Transform error: {e}")

    # =========================================================================
    # Top-Level Methods
    # =========================================================================

    def transform_file(
        self: Self,
        file_path: Path,
        transformer: cst.CSTTransformer,
    ) -> FlextResult[str]:
        """Apply a transformer to a file.

        Args:
            file_path: Path to file to transform.
            transformer: CST transformer to apply.

        Returns:
            FlextResult with transformed source.

        """
        try:
            source = file_path.read_text(encoding="utf-8")
            module = cst.parse_module(source)
            new_module = module.visit(transformer)
            return FlextResult[str].ok(new_module.code)

        except cst.ParserSyntaxError as e:
            return FlextResult[str].fail(f"Parse error in {file_path}: {e}")
        except FileNotFoundError:
            return FlextResult[str].fail(f"File not found: {file_path}")
        except Exception as e:
            return FlextResult[str].fail(f"Transform error: {e}")

    def parse_module(self: Self, source: str) -> FlextResult[cst.Module]:
        """Parse source code into CST module.

        Args:
            source: Source code to parse.

        Returns:
            FlextResult with parsed module.

        """
        try:
            return FlextResult[cst.Module].ok(cst.parse_module(source))
        except cst.ParserSyntaxError as e:
            return FlextResult[cst.Module].fail(f"Parse error: {e}")


__all__ = ["FlextQualityCodeTransformer"]
