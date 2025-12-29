# VERIFIED_NEW_MODULE
"""Test quality operations for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Provides BatchOperation implementations for test quality.
"""

from __future__ import annotations

from .antipattern_remover import TestAntipatternOperation
from .fixture_consolidator import FixtureConsolidateOperation
from .inheritance_fixer import TestInheritanceOperation
from .structure_fixer import TestStructureOperation

__all__ = [
    "FixtureConsolidateOperation",
    "TestAntipatternOperation",
    "TestInheritanceOperation",
    "TestStructureOperation",
]
