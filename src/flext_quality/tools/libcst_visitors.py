# VERIFIED_NEW_MODULE
"""libcst visitor implementations for code transformation (infrastructure).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Private infrastructure module for libcst-based AST transformations.
The libcst library requires specific visitor method names (leave_*, visit_*)
that don't follow PEP 8 conventions - these are API contracts with libcst.

This module is part of internal tooling infrastructure.
"""

from __future__ import annotations

from typing import Self

import libcst as cst


class FlextQualityLibcstVisitors:
    """Centralized libcst visitor implementations for code transformation.

    Provides safe, reusable visitor classes for AST manipulation.
    All visitor methods follow libcst API contracts (leave_*, visit_*).
    """

    class RemoveStatementVisitor(cst.CSTTransformer):
        """Remove statements from a specific module."""

        def __init__(
            self: Self,
            module_name: str,
            helpers: type,
        ) -> None:
            """Initialize with module name to remove.

            Args:
                helpers: Helper class with get_dotted_name and create_dotted_name methods.

            """
            super().__init__()
            self.module_name = module_name
            self.helpers = helpers

        def leave_ImportFrom(
            self: Self,
            original_node: cst.ImportFrom,
            updated_node: cst.ImportFrom,
        ) -> cst.ImportFrom | cst.RemovalSentinel:
            """Remove ImportFrom if it matches the target module."""
            del original_node  # Required by libcst API
            if updated_node.module is not None:
                # type: ignore[attr-defined] - helpers class has get_dotted_name static method
                module_str = self.helpers.get_dotted_name(updated_node.module)  # type: ignore[attr-defined]
                if module_str == self.module_name or module_str.startswith(
                    f"{self.module_name}."
                ):
                    return cst.RemovalSentinel.REMOVE
            return updated_node

    class StatementCheckerVisitor(cst.CSTVisitor):
        """Check if source has statement from specific module."""

        def __init__(self: Self, module_name: str, helpers: type) -> None:
            """Initialize with module name to find."""
            super().__init__()
            self.module_name = module_name
            self.found = False
            self.helpers = helpers

        def visit_ImportFrom(self: Self, node: cst.ImportFrom) -> bool:
            """Check ImportFrom nodes."""
            if node.module is not None:
                # type: ignore[attr-defined] - helpers class has get_dotted_name static method
                module_str = self.helpers.get_dotted_name(node.module)  # type: ignore[attr-defined]
                if module_str == self.module_name or module_str.startswith(
                    f"{self.module_name}."
                ):
                    self.found = True
            return False

    class ChangeBaseClassVisitor(cst.CSTTransformer):
        """Change a class's base class."""

        def __init__(
            self: Self, class_name: str, old_base: str, new_base: str, helpers: type
        ) -> None:
            """Initialize with class and base names."""
            super().__init__()
            self.class_name = class_name
            self.old_base = old_base
            self.new_base = new_base
            self.helpers = helpers

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef:
            """Replace base class if it matches."""
            del original_node  # Required by libcst API
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
                    # type: ignore[attr-defined] - helpers class has get_dotted_name static method
                    base_str = self.helpers.get_dotted_name(base.value)  # type: ignore[attr-defined]
                    if base_str == self.old_base:
                        new_bases.append(
                            base.with_changes(
                                # type: ignore[attr-defined] - helpers class has create_dotted_name static method
                                value=self.helpers.create_dotted_name(self.new_base)  # type: ignore[attr-defined]
                            )
                        )
                    else:
                        new_bases.append(base)
                else:
                    new_bases.append(base)

            return updated_node.with_changes(bases=new_bases)

    class AddBaseClassVisitor(cst.CSTTransformer):
        """Add a base class to an existing class."""

        def __init__(
            self: Self, class_name: str, new_base: str, helpers: type
        ) -> None:
            """Initialize with class and new base names."""
            super().__init__()
            self.class_name = class_name
            self.new_base = new_base
            self.helpers = helpers

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,
            updated_node: cst.ClassDef,
        ) -> cst.ClassDef:
            """Add base class if it matches the target class."""
            del original_node  # Required by libcst API
            if updated_node.name.value != self.class_name:
                return updated_node

            # type: ignore[attr-defined] - helpers class has create_dotted_name static method
            new_base_arg = cst.Arg(
                value=self.helpers.create_dotted_name(self.new_base)  # type: ignore[attr-defined]
            )
            new_bases = [*updated_node.bases, new_base_arg]

            return updated_node.with_changes(bases=new_bases)

    class ClassFinderVisitor(cst.CSTVisitor):
        """Find all classes in source code."""

        def __init__(self: Self, helpers: type) -> None:
            """Initialize class finder."""
            super().__init__()
            self.classes: list[dict[str, str | list[str] | int]] = []
            self.helpers = helpers

        def visit_ClassDef(self: Self, node: cst.ClassDef) -> bool:
            """Record class information."""
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base.value, cst.Name):
                    bases.append(base.value.value)
                elif isinstance(base.value, cst.Attribute):
                    # type: ignore[attr-defined] - helpers class has get_dotted_name static method
                    bases.append(self.helpers.get_dotted_name(base.value))  # type: ignore[attr-defined]

            self.classes.append({
                "name": node.name.value,
                "bases": bases,
            })
            return True

    class NestInClassVisitor(cst.CSTTransformer):
        """Move top-level functions into a class as methods."""

        def __init__(
            self: Self, class_name: str, function_names: list[str]
        ) -> None:
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
            del original_node  # Required by libcst API
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
            del original_node  # Required by libcst API
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
                body=list(updated_node.body.body) + new_methods
            )
            return updated_node.with_changes(body=new_body)

    class ExtractFromClassVisitor(cst.CSTTransformer):
        """Extract methods from a class to top-level functions."""

        def __init__(self: Self, class_name: str, method_names: list[str]) -> None:
            """Initialize with class and method names."""
            super().__init__()
            self.class_name = class_name
            self.method_names = method_names
            self.extracted_functions: list[cst.FunctionDef] = []

        def leave_ClassDef(
            self: Self,
            original_node: cst.ClassDef,  # noqa: ARG002
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
                    params = [
                        p for p in stmt.params.params if p.name.value != "self"
                    ]
                    extracted_func = stmt.with_changes(
                        params=stmt.params.with_changes(params=params)
                    )
                    extracted.append(extracted_func)
                elif isinstance(stmt, cst.BaseStatement):
                    remaining_body.append(stmt)

            if not extracted:
                return updated_node

            new_class = updated_node.with_changes(
                body=updated_node.body.with_changes(body=remaining_body)
            )

            # Return class followed by extracted functions
            return cst.FlattenSentinel([new_class, *extracted])


__all__ = ["FlextQualityLibcstVisitors"]
