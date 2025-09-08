"""AST function information model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


from flext_core import FlextModels


class FunctionInfo(FlextModels):
    """Strongly-typed function information from AST analysis."""


from flext_core import FlextModels


class FunctionInfo(FlextModels):
    """Strongly-typed function information from AST analysis."""

    name: str
    full_name: str
    file_path: str
    package_name: str
    line_number: int
    end_line_number: int
    decorators: FlextTypes.Core.StringList
    is_async: bool
    is_generator: bool
    is_method: bool
    is_property: bool
    is_class_method: bool
    is_static_method: bool
    parameter_count: int
    returns_annotation: str | None
    complexity: int
    docstring: str | None
