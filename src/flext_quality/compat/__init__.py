"""Backwards compatibility layer for flext-quality.

Provides stable API wrappers for external integrations, ensuring that
hooks, skills, and daemon processes continue working during internal
refactoring of the CLI and other components.

All classes in this module maintain exact API contracts with their
original implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from .hooks import FlextHookValidator
from .plugins import FlextCodeQualityPlugin, FlextDuplicationPlugin

__all__ = [
    "FlextCodeQualityPlugin",
    "FlextDuplicationPlugin",
    "FlextHookValidator",
]
