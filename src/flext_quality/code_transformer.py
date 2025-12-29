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
from libcst.metadata import MetadataWrapper

from .tools.libcst_visitors import FlextQualityLibcstVisitors


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
        self.statements = self.StatementTransformer(self)
        self.classes = self.ClassTransformer(self)
        self.indentation = self.IndentationTransformer(self)

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
                if isinstance(node.value, (cst.Attribute, cst.Name)):
                    prefix = FlextQualityCodeTransformer.Helpers.get_dotted_name(
                        node.value
                    )
                    return f"{prefix}.{node.attr.value}"
                return node.attr.value
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

        def __init__(self: Self, transformer: FlextQualityCodeTransformer) -> None:
            """Initialize statement transformer."""
            self._transformer = transformer

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
                visitor = FlextQualityLibcstVisitors.RemoveStatementVisitor(
                    module_name, FlextQualityCodeTransformer.Helpers
                )
                new_module = module.visit(visitor)
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
                checker = FlextQualityLibcstVisitors.StatementCheckerVisitor(
                    module_name, FlextQualityCodeTransformer.Helpers
                )
                wrapper = MetadataWrapper(module)
                wrapper.visit(checker)
                return FlextResult[bool].ok(checker.found)

            except cst.ParserSyntaxError as e:
                return FlextResult[bool].fail(f"Parse error: {e}")
            except Exception as e:
                return FlextResult[bool].fail(f"Check error: {e}")

    class ClassTransformer:
        """Modify class definitions using CST."""

        def __init__(self: Self, transformer: FlextQualityCodeTransformer) -> None:
            """Initialize class transformer."""
            self._transformer = transformer

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
                visitor = FlextQualityLibcstVisitors.ChangeBaseClassVisitor(
                    class_name, old_base, new_base, FlextQualityCodeTransformer.Helpers
                )
                new_module = module.visit(visitor)
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
                visitor = FlextQualityLibcstVisitors.AddBaseClassVisitor(
                    class_name, new_base, FlextQualityCodeTransformer.Helpers
                )
                new_module = module.visit(visitor)
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
                finder = FlextQualityLibcstVisitors.ClassFinderVisitor(
                    FlextQualityCodeTransformer.Helpers
                )
                wrapper = MetadataWrapper(module)
                wrapper.visit(finder)
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

        def __init__(self: Self, transformer: FlextQualityCodeTransformer) -> None:
            """Initialize indentation transformer."""
            self._transformer = transformer

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
                visitor = FlextQualityLibcstVisitors.NestInClassVisitor(
                    class_name, function_names
                )
                new_module = module.visit(visitor)
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
                visitor = FlextQualityLibcstVisitors.ExtractFromClassVisitor(
                    class_name, method_names
                )
                new_module = module.visit(visitor)
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
