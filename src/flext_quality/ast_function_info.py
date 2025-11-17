"""AST function information model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FlextQualityASTFunctionInfo(BaseModel):
    """Unified AST function information class following FLEXT pattern.

    Single responsibility: AST function information management
    Contains all function-related models as nested classes.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    class FunctionInfo(BaseModel):
        """Strongly-typed function information from AST analysis."""

        name: str
        full_name: str
        file_path: str
        package_name: str
        line_number: int
        end_line_number: int
        decorators: list[str]
        is_generator: bool
        is_method: bool
        is_property: bool
        is_class_method: bool
        is_static_method: bool
        parameter_count: int
        returns_annotation: str | None
        complexity: int
        docstring: str | None
