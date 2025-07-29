"""Quality system configuration using flext-core BaseSettings.

REFACTORED: Uses flext-core configuration patterns - NO duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextBaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class QualityConfig(FlextBaseSettings):
    """Quality analysis configuration using flext-core BaseSettings."""

    # Project settings
    project_name: str = Field(
        default="flext-infrastructure.monitoring.flext-quality",
        description="Quality analysis project name",
    )
    project_version: str = Field(
        default="0.7.0",
        description="Quality analysis version",
    )
    project_root: Path = Field(
        default_factory=Path.cwd,
        description="Project root directory",
    )

    # Analysis settings
    analysis_enabled: bool = Field(
        default=True,
        description="Enable quality analysis",
    )
    analysis_timeout: int = Field(
        default=300,
        description="Analysis timeout in seconds",
        ge=10,
        le=3600,
    )
    analysis_threads: int = Field(
        default=4,
        description="Number of analysis threads",
        ge=1,
        le=16,
    )

    # Code analysis backends
    enable_ast_analysis: bool = Field(
        default=True,
        description="Enable AST-based code analysis",
    )
    enable_security_analysis: bool = Field(
        default=True,
        description="Enable security vulnerability analysis",
    )
    enable_complexity_analysis: bool = Field(
        default=True,
        description="Enable cyclomatic complexity analysis",
    )
    enable_dead_code_analysis: bool = Field(
        default=True,
        description="Enable dead code detection",
    )
    enable_duplicate_analysis: bool = Field(
        default=True,
        description="Enable duplicate code detection",
    )

    # Quality thresholds
    max_complexity: int = Field(
        default=10,
        description="Maximum allowed cyclomatic complexity",
        ge=1,
        le=50,
    )
    min_coverage: float = Field(
        default=95.0,
        description="Minimum test coverage percentage",
        ge=0.0,
        le=100.0,
    )
    max_line_length: int = Field(
        default=88,
        description="Maximum line length",
        ge=50,
        le=200,
    )
    max_file_lines: int = Field(
        default=1000,
        description="Maximum lines per file",
        ge=100,
        le=5000,
    )

    # Linting configuration
    linting_enabled: bool = Field(
        default=True,
        description="Enable linting checks",
    )
    ruff_config_path: Path | None = Field(
        default=None,
        description="Path to ruff configuration file",
    )
    mypy_config_path: Path | None = Field(
        default=None,
        description="Path to mypy configuration file",
    )
    black_config_path: Path | None = Field(
        default=None,
        description="Path to black configuration file",
    )

    # Security analysis
    bandit_config_path: Path | None = Field(
        default=None,
        description="Path to bandit configuration file",
    )
    security_severity_threshold: str = Field(
        default="medium",
        description="Minimum security issue severity to report",
        pattern="^(low|medium|high|critical)$",
    )

    # Report generation
    generate_html_report: bool = Field(
        default=True,
        description="Generate HTML quality report",
    )
    generate_json_report: bool = Field(
        default=True,
        description="Generate JSON quality report",
    )
    generate_markdown_report: bool = Field(
        default=True,
        description="Generate Markdown quality report",
    )
    report_output_dir: Path = Field(
        default=Path("reports"),
        description="Directory for quality reports",
    )

    # Caching
    enable_cache: bool = Field(
        default=True,
        description="Enable analysis result caching",
    )
    cache_ttl_seconds: int = Field(
        default=3600,  # 1 hour default cache TTL
        description="Cache time-to-live in seconds",
        ge=60,
        le=86400,
    )
    cache_directory: str = Field(
        default=".quality_cache",
        description="Directory for analysis cache",
    )

    # Integration settings
    enable_git_integration: bool = Field(
        default=True,
        description="Enable git integration for change detection",
    )
    enable_ci_integration: bool = Field(
        default=True,
        description="Enable CI/CD integration features",
    )
    ci_fail_on_issues: bool = Field(
        default=True,
        description="Fail CI build on quality issues",
    )

    # File patterns
    include_patterns: list[str] = Field(
        default_factory=lambda: ["*.py"],
        description="File patterns to include in analysis",
    )
    exclude_patterns: list[str] = Field(
        default_factory=lambda: [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "node_modules",
            "*.pyc",
            "*.pyo",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ],
        description="File patterns to exclude from analysis",
    )

    # Performance settings
    enable_parallel_analysis: bool = Field(
        default=True,
        description="Enable parallel analysis for better performance",
    )
    max_parallel_workers: int = Field(
        default=4,
        description="Maximum parallel workers",
        ge=1,
        le=16,
    )
    memory_limit_mb: int = Field(
        default=1024,
        description="Memory limit for analysis in MB",
        ge=256,
        le=8192,
    )

    # Database settings for storing results
    enable_result_storage: bool = Field(
        default=True,
        description="Enable storing analysis results in database",
    )
    result_retention_days: int = Field(
        default=30,
        description="Days to retain analysis results",
        ge=1,
        le=365,
    )

    # Notification settings
    enable_notifications: bool = Field(
        default=False,
        description="Enable quality issue notifications",
    )
    notification_webhook_url: str | None = Field(
        default=None,
        description="Webhook URL for notifications",
    )
    notification_threshold: str = Field(
        default="high",
        description="Minimum severity for notifications",
        pattern="^(low|medium|high|critical)$",
    )

    # Custom rules
    custom_rules_path: str | None = Field(
        default=None,
        description="Path to custom quality rules",
    )
    enable_custom_rules: bool = Field(
        default=False,
        description="Enable custom quality rules",
    )

    def get_analysis_config(self) -> dict[str, Any]:
        """Get analysis configuration dictionary.

        Returns:
            Dictionary containing analysis settings and thresholds.

        """
        return {
            "ast": self.enable_ast_analysis,
            "security": self.enable_security_analysis,
            "complexity": self.enable_complexity_analysis,
            "dead_code": self.enable_dead_code_analysis,
            "duplicates": self.enable_duplicate_analysis,
            "thresholds": {
                "max_complexity": self.max_complexity,
                "min_coverage": self.min_coverage,
                "max_line_length": self.max_line_length,
                "max_file_lines": self.max_file_lines,
            },
        }

    def get_report_config(self) -> dict[str, Any]:
        """Get report generation configuration.

        Returns:
            Dictionary containing report generation settings.

        """
        return {
            "html": self.generate_html_report,
            "json": self.generate_json_report,
            "markdown": self.generate_markdown_report,
            "output_dir": self.report_output_dir,
        }

    def get_linting_config(self) -> dict[str, Any]:
        """Get linting configuration dictionary.

        Returns:
            Dictionary containing linting tool configurations.

        """
        return {
            "enabled": self.linting_enabled,
            "ruff": self.ruff_config_path,
            "mypy": self.mypy_config_path,
            "black": self.black_config_path,
        }

    model_config = SettingsConfigDict(
        # Remove invalid keys for flext-core SettingsConfigDict
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )
