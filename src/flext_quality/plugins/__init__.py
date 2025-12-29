"""Quality Plugins - Tool integrations for quality checking.

Provides unified interfaces for quality validation tools.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Usage:
    from flext_quality.plugins import FlextRuffPlugin
    from flext_quality.plugins import FlextMyPyPlugin
    from flext_quality.plugins import FlextDuplicationPlugin
    from flext_quality.plugins import FlextCodeQualityPlugin
"""

from __future__ import annotations

from .code_quality_plugin import FlextCodeQualityPlugin
from .duplication_plugin import FlextDuplicationPlugin
from .mypy_plugin import FlextMyPyPlugin
from .ruff_plugin import FlextRuffPlugin

__all__ = [
    "FlextCodeQualityPlugin",
    "FlextDuplicationPlugin",
    "FlextMyPyPlugin",
    "FlextRuffPlugin",
]
