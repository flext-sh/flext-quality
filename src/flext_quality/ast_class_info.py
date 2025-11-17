"""AST class information model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FlextQualityASTClassInfo(BaseModel):
    """Unified AST class information class following FLEXT pattern.

    Single responsibility: AST class information management
    Contains all class-related models as nested classes.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    class ClassInfo(BaseModel):
        """Strongly-typed class information from AST analysis."""

        name: str
        full_name: str
        file_path: str
        package_name: str
        line_number: int
        end_line_number: int
        base_classes: list[str]
        decorators: list[str]
        is_dataclass: bool
        is_abstract: bool
        has_docstring: bool
        method_count: int
        public_methods: int
        private_methods: int
        protected_methods: int
        property_count: int = 0
        class_method_count: int = 0
        static_method_count: int = 0
        complexity: int = 0
