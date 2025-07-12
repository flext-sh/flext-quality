"""FLEXT Quality Configuration - Modern Python 3.13 + Clean Architecture + DI.

REFACTORED: Uses flext-core BaseSettings with mixins, types, and constants.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ConfigDict, Field

from flext_core.domain.pydantic_base import BaseSettings


class QualityConfig(BaseSettings):
    """Quality analysis configuration using flext-core BaseSettings."""

    # Project settings
    project_name: str = Field(
        default="flext-quality",
        description="Project name for quality analysis",
    )
    project_root: Path = Field(
        default=".",
        description="Project root directory",
    )

    # Analysis configuration
    enable_ast_analysis: bool = Field(
        default=True,
        description="Enable AST-based analysis",
    )
    enable_security_analysis: bool = Field(
        default=True,
        description="Enable security analysis",
    )
    enable_complexity_analysis: bool = Field(
        default=True,
        description="Enable complexity analysis",
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
        description="Maximum cyclomatic complexity",
        ge=1,
    )
    min_coverage: float = Field(
        default=80.0,
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
    )

    # Tool configuration
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

    # Reporting
    generate_html_report: bool = Field(
        default=True,
        description="Generate HTML report",
    )
    generate_json_report: bool = Field(
        default=True,
        description="Generate JSON report",
    )
    generate_markdown_report: bool = Field(
        default=False,
        description="Generate Markdown report",
    )
    report_output_dir: Path = Field(
        default="reports",
        description="Output directory for reports",
    )

    # Linting configuration
    linting_enabled: bool = Field(
        default=True,
        description="Enable linting analysis",
    )

    # Custom rules
    enable_custom_rules: bool = Field(
        default=False,
        description="Enable custom quality rules",
    )

    def get_analysis_config(self) -> dict[str, Any]:
        """Get analysis configuration as dictionary."""
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
        """Get report configuration as dictionary."""
        return {
            "html": self.generate_html_report,
            "json": self.generate_json_report,
            "markdown": self.generate_markdown_report,
            "output_dir": self.report_output_dir,
        }

    def get_linting_config(self) -> dict[str, Any]:
        """Get linting configuration as dictionary."""
        return {
            "enabled": self.linting_enabled,
            "ruff": self.ruff_config_path,
            "mypy": self.mypy_config_path,
            "black": self.black_config_path,
        }

    model_config = ConfigDict(
        env_prefix="QUALITY_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
