"""Quality configuration management using flext-core patterns."""

from __future__ import annotations

import warnings

from flext_core import FlextModels
from pydantic_settings import SettingsConfigDict


class FlextQualityConfig(FlextModels.BaseModel):
    """Quality service configuration using flext-core patterns."""

    # Analysis settings
    min_coverage: float = 90.0
    max_complexity: int = 10
    max_duplication: float = 5.0
    min_security_score: float = 90.0
    min_maintainability: float = 80.0

    # Service settings
    analysis_timeout: int = 300
    parallel_workers: int = 4

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
