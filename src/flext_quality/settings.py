"""Quality configuration management using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import warnings
from typing import Literal, Self

from flext_core import FlextResult, FlextSettings, FlextTypes as t
from pydantic import Field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from .constants import FlextQualityConstants


@FlextSettings.auto_register("quality")
class FlextQualitySettings(FlextSettings):
    """Single Pydantic 2 Settings class for flext-quality extending FlextSettings.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration

    This class extends FlextSettings (BaseSettings) for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.quality)
    - Environment variable loading from FLEXT_QUALITY_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2

    Follows standardized pattern:
    - No nested classes within Config
    - All defaults from FlextQualityConstants
    - Uses Pydantic 2.11+ field_validator and model_validator
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_QUALITY_",
        case_sensitive=False,
        extra="allow",
        # Inherit enhanced Pydantic 2.11+ features from FlextSettings
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "title": "FLEXT Quality Configuration",
            "description": "Code quality analysis configuration extending FlextSettings",
        },
    )

    # Quality Analysis Configuration using FlextQualityConstants for defaults
    min_coverage: float = Field(
        default=FlextQualityConstants.Quality.Coverage.MINIMUM_COVERAGE,
        ge=FlextQualityConstants.Quality.QualityValidation.MINIMUM_PERCENTAGE,
        le=FlextQualityConstants.Quality.QualityValidation.MAXIMUM_PERCENTAGE,
        description="Minimum test coverage percentage required",
    )

    max_complexity: int = Field(
        default=FlextQualityConstants.Quality.Complexity.MAX_COMPLEXITY,
        ge=1,
        le=FlextQualityConstants.Quality.Complexity.HIGH_COMPLEXITY_WARNING_THRESHOLD,
        description="Maximum cyclomatic complexity allowed",
    )

    max_duplication: float = Field(
        default=FlextQualityConstants.Quality.Duplication.MAXIMUM_DUPLICATION,
        ge=FlextQualityConstants.Quality.QualityValidation.MINIMUM_PERCENTAGE,
        le=FlextQualityConstants.Quality.QualityValidation.MAXIMUM_PERCENTAGE,
        description="Maximum code duplication percentage allowed",
    )

    min_security_score: float = Field(
        default=FlextQualityConstants.Quality.QualitySecurity.MINIMUM_SECURITY_SCORE,
        ge=FlextQualityConstants.Quality.QualityValidation.MINIMUM_PERCENTAGE,
        le=FlextQualityConstants.Quality.QualityValidation.MAXIMUM_PERCENTAGE,
        description="Minimum security score required",
    )

    min_maintainability: float = Field(
        default=FlextQualityConstants.Quality.Maintainability.MINIMUM_MAINTAINABILITY,
        ge=FlextQualityConstants.Quality.QualityValidation.MINIMUM_PERCENTAGE,
        le=FlextQualityConstants.Quality.QualityValidation.MAXIMUM_PERCENTAGE,
        description="Minimum maintainability index required",
    )

    # Service Configuration using FlextQualityConstants for defaults
    analysis_timeout: int = Field(
        default=FlextQualityConstants.Quality.QualityPerformance.DEFAULT_ANALYSIS_TIMEOUT,
        gt=0,
        le=FlextQualityConstants.Quality.QualityPerformance.MAXIMUM_ANALYSIS_TIMEOUT,
        description="Quality analysis timeout in seconds",
    )

    parallel_workers: int = Field(
        default=FlextQualityConstants.Quality.QualityPerformance.DEFAULT_WORKERS,
        ge=1,
        le=FlextQualityConstants.Quality.QualityPerformance.MAXIMUM_WORKERS,
        description="Number of parallel workers for analysis",
    )

    memory_limit_mb: int = Field(
        default=FlextQualityConstants.Quality.Optimization.MAX_FILE_SIZE
        // (1024 * 1024),
        gt=0,
        le=2048,
        description="Memory limit per file in MB",
    )

    # Backend Configuration using FlextQualityConstants for defaults
    enable_ast_analysis: bool = Field(
        default=True,
        description="Enable AST-based code analysis",
    )

    enable_external_tools: bool = Field(
        default=True,
        description="Enable external tool integration",
    )

    enable_ruff: bool = Field(
        default=True,
        description="Enable Ruff linting analysis",
    )

    enable_mypy: bool = Field(
        default=True,
        description="Enable MyPy type checking analysis",
    )

    enable_bandit: bool = Field(
        default=True,
        description="Enable Bandit security analysis",
    )

    enable_dependency_scan: bool = Field(
        default=True,
        description="Enable dependency vulnerability scanning",
    )

    # Reporting Configuration using FlextQualityConstants for defaults
    enable_html_reports: bool = Field(
        default=True,
        description="Enable HTML report generation",
    )

    enable_json_reports: bool = Field(
        default=True,
        description="Enable JSON report generation",
    )

    enable_audit_logging: bool = Field(
        default=True,
        description="Enable audit logging for quality operations",
    )

    include_trend_analysis: bool = Field(
        default=True,
        description="Include trend analysis in reports",
    )

    include_executive_summary: bool = Field(
        default=True,
        description="Include executive summary in reports",
    )

    # Observability Configuration using FlextQualityConstants for defaults
    observability_quiet: bool = Field(
        default=False,
        description="Enable quiet mode for observability (useful for JSON/HTML output)",
    )

    observability_log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = Field(
        default="INFO",
        description="Log level for observability components",
    )

    # Project Identification
    project_name: str = Field(
        default="flext-quality",
        description="Project name",
    )

    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # Pydantic 2.11+ field validators (warnings only - validation via Field constraints)
    @field_validator("max_complexity")
    @classmethod
    def validate_complexity_threshold(cls, v: int) -> int:
        """Warn if complexity threshold is high (validation via Field constraint)."""
        if (
            v
            > FlextQualityConstants.Quality.Complexity.HIGH_COMPLEXITY_WARNING_THRESHOLD
        ):
            warnings.warn(
                f"High complexity threshold ({v}) may be too permissive",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("analysis_timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Warn if analysis timeout is very high (validation via Field constraint)."""
        if (
            v
            > FlextQualityConstants.Quality.QualityPerformance.MAXIMUM_ANALYSIS_TIMEOUT
        ):
            warnings.warn(
                f"Very long timeout ({v}s) may cause performance issues",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("parallel_workers")
    @classmethod
    def validate_workers(cls, v: int) -> int:
        """Warn if worker count is high (validation via Field constraint)."""
        if v > FlextQualityConstants.Quality.QualityPerformance.MAXIMUM_WORKERS:
            warnings.warn(
                f"High worker count ({v}) may impact system performance",
                UserWarning,
                stacklevel=2,
            )
        return v

    @model_validator(mode="after")
    def validate_quality_configuration_consistency(self) -> Self:
        """Validate quality configuration consistency."""
        # Validate threshold relationships
        if (
            self.min_coverage
            >= FlextQualityConstants.Quality.QualityValidation.COVERAGE_EXTERNAL_TOOLS_THRESHOLD
            and not self.enable_external_tools
        ):
            warnings.warn(
                "100% coverage target requires external tools for validation",
                UserWarning,
                stacklevel=2,
            )

        # Validate security configuration
        if (
            self.min_security_score
            >= FlextQualityConstants.Quality.QualityValidation.SECURITY_BANDIT_THRESHOLD
            and not self.enable_bandit
        ):
            msg = "High security score requires Bandit security analysis"
            raise ValueError(msg)

        # Validate analysis configuration
        if not any([
            self.enable_ast_analysis,
            self.enable_external_tools,
            self.enable_ruff,
            self.enable_mypy,
            self.enable_bandit,
        ]):
            msg = "At least one analysis method must be enabled"
            raise ValueError(msg)

        # Validate reporting configuration
        if not any([self.enable_html_reports, self.enable_json_reports]):
            warnings.warn(
                "No report formats enabled, analysis results may not be accessible",
                UserWarning,
                stacklevel=2,
            )

        return self

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate quality analysis business rules."""
        try:
            # Validate analysis requirements
            if self.min_coverage > 0.0 and not self.enable_external_tools:
                return FlextResult[bool].fail(
                    "Coverage analysis requires external tools",
                )

            # Validate performance requirements
            if (
                self.analysis_timeout
                < FlextQualityConstants.Quality.QualityPerformance.MINIMUM_ANALYSIS_TIMEOUT
            ):
                return FlextResult[bool].fail(
                    f"Analysis timeout too low (minimum {FlextQualityConstants.Quality.QualityPerformance.MINIMUM_ANALYSIS_TIMEOUT} seconds)",
                )

            # Validate threshold consistency
            if (
                self.min_security_score
                >= FlextQualityConstants.Quality.QualityValidation.SECURITY_DEPENDENCY_SCAN_THRESHOLD
                and not self.enable_dependency_scan
            ):
                return FlextResult[bool].fail(
                    "High security score requires dependency scanning",
                )

            # Validate reporting requirements
            if self.include_trend_analysis and not self.enable_audit_logging:
                return FlextResult[bool].fail("Trend analysis requires audit logging")

            return FlextResult[bool].ok(True)
        except Exception as e:
            error_msg = f"Business rules validation failed: {e}"
            return FlextResult[bool].fail(error_msg)

    def get_analysis_config(self) -> dict[str, t.GeneralValueType]:
        """Get quality analysis configuration context."""
        return {
            "min_coverage": self.min_coverage,
            "max_complexity": self.max_complexity,
            "max_duplication": self.max_duplication,
            "min_security_score": self.min_security_score,
            "min_maintainability": self.min_maintainability,
            "timeout": self.analysis_timeout,
            "workers": self.parallel_workers,
        }

    def get_backend_config(self) -> dict[str, t.GeneralValueType]:
        """Get analysis backend configuration context."""
        return {
            "enable_ast_analysis": self.enable_ast_analysis,
            "enable_external_tools": self.enable_external_tools,
            "enable_ruff": self.enable_ruff,
            "enable_mypy": self.enable_mypy,
            "enable_bandit": self.enable_bandit,
            "enable_dependency_scan": self.enable_dependency_scan,
        }

    def get_reporting_config(self) -> dict[str, t.GeneralValueType]:
        """Get quality reporting configuration context."""
        return {
            "enable_html_reports": self.enable_html_reports,
            "enable_json_reports": self.enable_json_reports,
            "enable_audit_logging": self.enable_audit_logging,
            "include_trend_analysis": self.include_trend_analysis,
            "include_executive_summary": self.include_executive_summary,
        }

    def get_observability_config(self) -> dict[str, t.GeneralValueType]:
        """Get observability configuration context."""
        return {
            "quiet": self.observability_quiet,
            "log_level": self.observability_log_level,
        }

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **overrides: object,
    ) -> FlextQualitySettings:
        """Create configuration for specific environment using direct instantiation."""
        # Note: environment parameter reserved for future use
        _ = environment  # Unused but maintains parent signature
        return cls.model_validate(overrides)

    @classmethod
    def create_default(cls) -> FlextQualitySettings:
        """Create default configuration instance using direct instantiation."""
        return cls()

    @classmethod
    def create_for_development(cls) -> FlextQualitySettings:
        """Create configuration optimized for development using model_validate."""
        return cls.model_validate({
            "min_coverage": 80.0,
            "max_complexity": 15,
            "analysis_timeout": 120,
            "parallel_workers": 2,
        })

    @classmethod
    def create_for_production(cls) -> FlextQualitySettings:
        """Create configuration optimized for production using model_validate."""
        return cls.model_validate({
            "min_coverage": FlextQualityConstants.Quality.Coverage.TARGET_COVERAGE,
            "max_complexity": 8,
            "min_security_score": FlextQualityConstants.Quality.QualitySecurity.TARGET_SECURITY_SCORE,
            "min_maintainability": 85.0,
            "analysis_timeout": 600,
            "parallel_workers": 8,
        })


__all__ = [
    "FlextQualitySettings",
]
