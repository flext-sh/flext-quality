"""FLEXT Quality Tools - Internal utilities package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Internal tools for flext-quality operations. These utilities consume
flext-quality's domain API and provide supporting functionality.
"""

from __future__ import annotations

from .tools.architecture import FlextQualityArchitectureTools
from .tools.dependencies import FlextQualityDependencyTools
from .tools.git import FlextQualityGitTools
from .tools.optimizer_operations import FlextQualityOptimizerOperations
from .tools.quality_operations import FlextQualityOperations
from .tools.utilities import (
    Colors,
    FlextQualityToolsUtilities,
    colorize,
    get_project_root,
    get_stdlib_modules,
    is_stdlib_module,
    normalize_path,
    print_colored,
    should_ignore_path,
)
from .tools.validation import FlextQualityValidationTools

__all__ = [
    # Utility components
    "Colors",
    # Tool services
    "FlextQualityArchitectureTools",
    "FlextQualityDependencyTools",
    "FlextQualityGitTools",
    "FlextQualityOperations",
    "FlextQualityOptimizerOperations",
    "FlextQualityToolsUtilities",
    "FlextQualityValidationTools",
    # Convenience functions
    "colorize",
    "get_project_root",
    "get_stdlib_modules",
    "is_stdlib_module",
    "normalize_path",
    "print_colored",
    "should_ignore_path",
]
