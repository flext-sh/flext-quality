"""FLEXT Quality - Unified orchestration platform for Claude Code tooling.

Exposes `FlextQuality` as the main API facade, along with domain models,
settings, and utilities. Uses flext-core patterns: `FlextResult[T]`
railway pattern, `FlextSettings`.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_quality.api import FlextQuality
from flext_quality.constants import FlextQualityConstants
from flext_quality.models import FlextQualityModels
from flext_quality.protocols import FlextQualityProtocols
from flext_quality.settings import FlextQualitySettings
from flext_quality.typings import FlextQualityTypes
from flext_quality.utilities import FlextQualityUtilities

__version__ = "0.9.0"
__all__ = [
    "FlextQuality",
    "FlextQualityConstants",
    "FlextQualityModels",
    "FlextQualityProtocols",
    "FlextQualitySettings",
    "FlextQualityTypes",
    "FlextQualityUtilities",
    "__version__",
]
