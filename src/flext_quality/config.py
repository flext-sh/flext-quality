"""FlextQuality configuration using FlextSettings pattern."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextSettings


class FlextQualitySettings(FlextSettings):
    """FlextQuality orchestrator configuration.

    Configuration sources (priority order):
    1. Environment variables (FLEXT_QUALITY_*)
    2. .env file
    3. Default values

    Example .env:
    ```
    FLEXT_QUALITY_MAX_PARALLEL_WORKERS=6
    FLEXT_QUALITY_PLUGIN_TIMEOUT=10
    FLEXT_QUALITY_RULE_DIRECTORIES=/home/user/flext/flext-quality/src/flext_quality/rules/data
    ```
    """

    # Parallel execution
    max_parallel_workers: int = 4  # Max concurrent processes
    plugin_timeout: int = 10  # Seconds per plugin

    # Rule directories
    rule_directories: list[Path] = [
        Path(__file__).parent / "rules" / "data",
    ]

    # Plugin configuration
    plugin_configs: dict[str, dict[str, Any]] = {
        "ruff": {
            "enabled": True,
            "config_path": None,  # Use project config
        },
        "mypy": {
            "enabled": True,
            "strict": True,
            "config_path": None,
        },
        "language-detector": {
            "enabled": True,
        },
        "rule-registry": {
            "enabled": True,
            "severity_threshold": "warning",
        },
    }

    # Logging
    log_level: str = "INFO"

    class Config:
        """Pydantic config for FlextSettings."""

        env_prefix = "FLEXT_QUALITY_"
        env_file = ".env"
        env_file_encoding = "utf-8"
