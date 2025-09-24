"""Quality configuration management using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextConstants


class FlextQualityConfig(FlextConfig):
    """Quality service configuration using flext-core patterns."""

    # Analysis settings
    min_coverage: float = 90.0
    max_complexity: int = 10
    max_duplication: float = 5.0
    min_security_score: float = 90.0
    min_maintainability: float = 80.0

    # Service settings - using FlextConstants as SOURCE OF TRUTH
    analysis_timeout: int = FlextConstants.Defaults.TIMEOUT * 10  # 300 seconds
    parallel_workers: int = FlextConstants.Container.MAX_WORKERS  # 4 workers

    model_config = SettingsConfigDict(env_prefix="QUALITY_")


# Legacy compatibility facade - DEPRECATED
QualityConfig = FlextQualityConfig
warnings.warn(
    "QualityConfig is deprecated; use FlextQualityConfig",
    DeprecationWarning,
    stacklevel=2,
)

# Export all classes
__all__ = [
    "FlextQualityConfig",
    "QualityConfig",  # Legacy compatibility
]
