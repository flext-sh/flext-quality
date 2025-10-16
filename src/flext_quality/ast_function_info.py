"""AST function information model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextModels, FlextTypes


class FlextQualityASTFunctionInfo(FlextModels.StrictArbitraryTypesModel):
    """Unified AST function information class following FLEXT pattern.

    Single responsibility: AST function information management
    Contains all function-related models as nested classes.
    """

    class FunctionInfo(FlextModels.StrictArbitraryTypesModel):
        """Strongly-typed function information from AST analysis."""

        name: str
        full_name: str
        file_path: str
        package_name: str
        line_number: int
        end_line_number: int
        decorators: FlextTypes.StringList
        is_generator: bool
        is_method: bool
        is_property: bool
        is_class_method: bool
        is_static_method: bool
        parameter_count: int
        returns_annotation: str | None
        complexity: int
        docstring: str | None
