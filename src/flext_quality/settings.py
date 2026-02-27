"""FlextQualitySettings - Configuration for flext-quality.

Extends FlextSettings with quality-specific configuration for hooks,
rules, MCP integration, and quality thresholds.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextSettings, r
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_quality.constants import c


@FlextSettings.auto_register("quality")
class FlextQualitySettings(FlextSettings):
    """Settings for flext-quality project.

    Provides configuration for:
    - Hook processing (timeouts, events)
    - Rule engine (batch size, parallelism)
    - MCP server integration
    - Quality thresholds
    - Cache configuration

    Usage:
        from flext_quality.settings import FlextQualitySettings

        settings = FlextQualitySettings.get_global_instance()
        timeout = settings.hook_timeout_ms
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_",
        env_nested_delimiter="__",
        env_file=FlextSettings.resolve_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True,
    )

    # =========================================================================
    # Class Variables (not config fields)
    # =========================================================================
    _instance: ClassVar[FlextQualitySettings | None] = None

    # =========================================================================
    # Hook Configuration
    # =========================================================================
    hook_timeout_ms: int = Field(
        default=c.Quality.Defaults.HOOK_TIMEOUT_MS,
        ge=100,
        le=60000,
        description="Timeout for hook execution in milliseconds",
    )
    hook_enabled: bool = Field(
        default=True,
        description="Enable/disable hook processing",
    )

    # =========================================================================
    # Rule Engine Configuration
    # =========================================================================
    rule_timeout_seconds: int = Field(
        default=c.Quality.Defaults.RULE_TIMEOUT_SECONDS,
        ge=1,
        le=300,
        description="Timeout for rule evaluation in seconds",
    )
    rule_batch_size: int = Field(
        default=c.Quality.Defaults.BATCH_SIZE,
        ge=1,
        le=1000,
        description="Batch size for rule processing",
    )
    max_parallel_rules: int = Field(
        default=c.Quality.Defaults.MAX_PARALLEL_RULES,
        ge=1,
        le=32,
        description="Maximum parallel rule evaluations",
    )

    # =========================================================================
    # MCP Server Configuration
    # =========================================================================
    mcp_server_name: str = Field(
        default=c.Quality.Mcp.SERVER_NAME,
        description="MCP server name",
    )
    mcp_server_port: int = Field(
        default=c.Quality.Mcp.DEFAULT_PORT,
        ge=1024,
        le=65535,
        description="MCP server port",
    )
    mcp_timeout_ms: int = Field(
        default=c.Quality.Defaults.MCP_TIMEOUT_MS,
        ge=1000,
        le=300000,
        description="Timeout for MCP operations in milliseconds",
    )

    # =========================================================================
    # Integration Configuration
    # =========================================================================
    integration_timeout_ms: int = Field(
        default=c.Quality.Defaults.INTEGRATION_TIMEOUT_MS,
        ge=1000,
        le=60000,
        description="Timeout for external integrations in milliseconds",
    )

    # =========================================================================
    # Cache Configuration
    # =========================================================================
    cache_enabled: bool = Field(
        default=True,
        description="Enable/disable caching",
    )
    cache_ttl_seconds: int = Field(
        default=c.Quality.Defaults.CACHE_TTL_SECONDS,
        ge=0,
        le=86400,
        description="Cache time-to-live in seconds",
    )
    max_cache_entries: int = Field(
        default=c.Quality.Defaults.MAX_CACHE_ENTRIES,
        ge=0,
        le=100000,
        description="Maximum number of cache entries",
    )

    # =========================================================================
    # Quality Thresholds
    # =========================================================================
    max_cyclomatic_complexity: int = Field(
        default=c.Quality.Threshold.MAX_CYCLOMATIC_COMPLEXITY,
        ge=1,
        le=50,
        description="Maximum allowed cyclomatic complexity",
    )
    max_cognitive_complexity: int = Field(
        default=c.Quality.Threshold.MAX_COGNITIVE_COMPLEXITY,
        ge=1,
        le=50,
        description="Maximum allowed cognitive complexity",
    )
    max_function_length: int = Field(
        default=c.Quality.Threshold.MAX_FUNCTION_LENGTH,
        ge=1,
        le=500,
        description="Maximum function length in lines",
    )
    max_class_length: int = Field(
        default=c.Quality.Threshold.MAX_CLASS_LENGTH,
        ge=1,
        le=2000,
        description="Maximum class length in lines",
    )
    min_test_coverage: float = Field(
        default=c.Quality.Threshold.MIN_TEST_COVERAGE,
        ge=0.0,
        le=100.0,
        description="Minimum required test coverage percentage",
    )
    max_line_length: int = Field(
        default=c.Quality.Threshold.MAX_LINE_LENGTH,
        ge=40,
        le=200,
        description="Maximum line length",
    )

    # =========================================================================
    # Paths Configuration
    # =========================================================================
    rules_dir: str = Field(
        default=c.Quality.Paths.RULES_DIR,
        description="Directory for rule definitions",
    )
    config_file: str = Field(
        default=c.Quality.Paths.CONFIG_FILE,
        description="Quality configuration file name",
    )
    cache_dir: str = Field(
        default=c.Quality.Paths.CACHE_DIR,
        description="Cache directory name",
    )
    reports_dir: str = Field(
        default=c.Quality.Paths.REPORTS_DIR,
        description="Reports output directory",
    )

    # =========================================================================
    # Instance Management
    # =========================================================================
    @classmethod
    def get_instance(cls) -> FlextQualitySettings:
        """Get or create singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    @override
    def _reset_instance(cls) -> None:
        """Reset singleton instance (for testing)."""
        cls._instance = None

    # =========================================================================
    # Path Resolution
    # =========================================================================
    def get_rules_path(self, base_path: Path | None = None) -> Path:
        """Get the rules directory path."""
        base = base_path or Path.cwd()
        return base / self.rules_dir

    def get_cache_path(self, base_path: Path | None = None) -> Path:
        """Get the cache directory path."""
        base = base_path or Path.cwd()
        return base / self.cache_dir

    def get_reports_path(self, base_path: Path | None = None) -> Path:
        """Get the reports directory path."""
        base = base_path or Path.cwd()
        return base / self.reports_dir

    def get_config_path(self, base_path: Path | None = None) -> Path:
        """Get the config file path."""
        base = base_path or Path.cwd()
        return base / self.config_file

    # =========================================================================
    # Validation
    # =========================================================================
    def validate_thresholds(self) -> r[bool]:
        """Validate threshold configuration.

        Note: Range validation is handled by Pydantic Field constraints.
        This method validates logical constraints between fields.
        """
        if self.max_function_length > self.max_class_length:
            return r[bool].fail("max_function_length cannot exceed max_class_length")
        return r[bool].ok(value=True)

    def validate_paths(self, base_path: Path | None = None) -> r[bool]:
        """Validate that required paths exist or can be created."""
        base = base_path or Path.cwd()
        rules_path = base / self.rules_dir
        if not rules_path.exists():
            return r[bool].fail(f"Rules directory not found: {rules_path}")
        return r[bool].ok(value=True)


__all__ = ["FlextQualitySettings"]
