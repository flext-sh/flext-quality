"""Quality configuration management using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
import warnings
from typing import ClassVar

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextConstants


class FlextQualityConfig(FlextConfig):
    """Quality service configuration using flext-core patterns."""

    # Singleton pattern attributes
    _global_instance: ClassVar[FlextQualityConfig | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    # Analysis settings
    min_coverage: float = 90.0
    max_complexity: int = 10
    max_duplication: float = 5.0
    min_security_score: float = 90.0
    min_maintainability: float = 80.0

    # Service settings - using FlextConstants as SOURCE OF TRUTH
    analysis_timeout: int = FlextConstants.Defaults.TIMEOUT * 10  # 300 seconds
    parallel_workers: int = FlextConstants.Container.MAX_WORKERS  # 4 workers

    # Observability settings for quality analysis
    observability_quiet: bool = Field(
        default=False,
        description="Enable quiet mode for observability (useful for JSON/HTML output)",
    )

    observability_log_level: str = Field(
        default=INFO, description="Log level for observability components"
    )

    model_config: dict[str, object] = SettingsConfigDict(env_prefix="QUALITY_")

    # Singleton pattern override for proper typing
    @classmethod
    def get_global_instance(cls) -> FlextQualityConfig:
        """Get the global singleton instance of FlextQualityConfig."""
        if cls._global_instance is None:
            with cls._lock:
                if cls._global_instance is None:
                    cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextQualityConfig instance (mainly for testing)."""
        cls._global_instance = None


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
