"""Quality configuration management using flext-core patterns."""

from __future__ import annotations

from flext_core import FlextBaseConfigModel
from pydantic_settings import SettingsConfigDict


class QualityConfig(FlextBaseConfigModel):
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
