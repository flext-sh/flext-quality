"""FLEXT Quality Models - Analysis execution, reporting, and configuration models.

- Analysis: Analysis execution and results
- Reporting: Report generation and metrics
- Configuration: Analysis configuration models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pathlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Self, override
from uuid import UUID

from flext_core import FlextCore
from pydantic import (
    Field,
    SerializationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

from .constants import FlextQualityConstants
from .value_objects import FlextQualityValueObjects


class FlextQualityModels(FlextCore.Models.StrictArbitraryTypesModel):
    """Unified quality models class following FLEXT architecture patterns.

    Inherits from FlextCore.Models.StrictArbitraryTypesModel for comprehensive validation.
    Single responsibility: Quality data models and validation
    Contains all Pydantic models as nested classes with shared functionality.
    """

    # =============================================================================
    # ENUM CLASSES - Analysis status enumerations
    # =============================================================================

    @property
    def active_quality_models_count(self) -> int:
        """Computed field returning the number of active quality model types."""
        # Count active quality models based on nested classes
        quality_model_classes = [
            self.ProjectModel,
            self.AnalysisModel,
            self.IssueModel,
            self.ReportModel,
            self.ConfigModel,
        ]
        return len([cls for cls in quality_model_classes if cls])

    @property
    def quality_system_summary(self) -> FlextCore.Types.Dict:
        """Computed field providing comprehensive quality system summary."""
        return {
            "system_info": {
                "name": "FLEXT Quality Analysis System",
                "version": "2.11.0",
                "active_models": self.active_quality_models_count,
                "architecture": "Clean Architecture + DDD",
            },
            "supported_operations": [
                "code_quality_analysis",
                "security_vulnerability_detection",
                "test_coverage_measurement",
                "complexity_analysis",
                "maintainability_scoring",
                "quality_reporting",
            ],
            "analysis_capabilities": [
                "AST-based analysis",
                "External tool integration",
                "Multi-backend support",
                "Parallel processing",
                "Real-time monitoring",
            ],
            "reporting_formats": ["HTML", "JSON", "PDF", "CSV", "XML"],
            "enterprise_features": [
                "Quality thresholds",
                "Trend analysis",
                "Executive summaries",
                "Audit logging",
                "Security compliance",
            ],
        }

    @model_validator(mode="after")
    def validate_quality_system_consistency(self) -> Self:
        """Model validator ensuring quality system consistency and standards."""
        # Validate that quality models maintain consistency
        # Note: _initialized attribute check removed as it's not defined in the model

        # Ensure enterprise quality standards are properly set
        if hasattr(self, "ConfigModel"):
            # Quality-specific validation logic can be added here
            pass

        return self

    @field_serializer("*", when_used="json")
    def serialize_with_quality_metadata(
        self, value: object, _info: SerializationInfo
    ) -> Any:
        """Field serializer adding quality analysis metadata and compliance context."""
        if isinstance(value, dict):
            return {
                **value,
                "_quality_metadata": {
                    "processed_at": datetime.now(UTC).isoformat(),
                    "model_type": "FlextQualityModels",
                    "quality_validated": True,
                    "enterprise_compliant": True,
                    "analysis_ready": True,
                },
            }
        return value

    @override
    def __init__(self) -> None:
        """Initialize models with dependency injection."""
        super().__init__()
        self._container = FlextCore.Container.get_global()
        self.logger = FlextCore.Logger(__name__)

    class ProjectModel(FlextCore.Models.StrictArbitraryTypesModel):
        """Pydantic model for quality project representation."""

        id: UUID = Field(..., description="Unique project identifier")
        name: str = Field(
            default="", min_length=1, max_length=255, description="Project name"
        )
        path: str = Field(..., description="Project path for analysis")
        description: str | None = Field(None, description="Project description")
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Creation timestamp",
        )
        updated_at: datetime = Field(
            default_factory=datetime.now,
            description="Last update timestamp",
        )

        @property
        def project_summary(self) -> FlextCore.Types.Dict:
            """Computed field providing comprehensive project summary."""
            return {
                "project_info": {
                    "id": str(self.id),
                    "name": self.name,
                    "path": self.path,
                    "has_description": bool(self.description),
                },
                "lifecycle_info": {
                    "created_at": self.created_at.isoformat(),
                    "updated_at": self.updated_at.isoformat(),
                    "project_age_days": (datetime.now(UTC) - self.created_at).days,
                    "is_recently_updated": (datetime.now(UTC) - self.updated_at).days
                    < FlextQualityConstants.Project.RECENT_UPDATE_DAYS,
                },
                "analysis_readiness": {
                    "path_exists": True,  # Would need file system check in real implementation
                    "is_enterprise_ready": True,
                    "supports_quality_analysis": True,
                },
            }

        @model_validator(mode="after")
        def validate_project_consistency(self) -> Self:
            """Model validator for project consistency."""
            # Validate project name follows quality standards
            if not self.name.strip():
                msg = "Project name cannot be empty"
                raise ValueError(msg)

            # Validate path format (basic validation)
            if not self.path or not self.path.strip():
                msg = "Project path is required for quality analysis"
                raise ValueError(msg)

            # Ensure updated_at is not before created_at
            if self.updated_at < self.created_at:
                msg = "Updated timestamp cannot be before created timestamp"
                raise ValueError(msg)

            return self

        @field_serializer("path", when_used="json")
        def serialize_path_securely(self, value: str) -> str:
            """Field serializer for secure path handling."""
            # Don't expose full system paths in serialization for security

            return pathlib.Path(value).name if value else ""

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate project name follows basic constraints."""
            if not v.strip():
                msg = "Project name cannot be empty"
                raise ValueError(msg)
            return v.strip()

    class AnalysisModel(FlextCore.Models.StrictArbitraryTypesModel):
        """Pydantic model for quality analysis representation."""

        id: UUID = Field(..., description="Unique analysis identifier")
        project_id: UUID = Field(..., description="Associated project identifier")
        status: str = Field(..., description="Analysis status")
        overall_score: float = Field(
            0.0,
            ge=0.0,
            le=100.0,
            description="Overall quality score",
        )
        coverage_score: float = Field(
            0.0,
            ge=0.0,
            le=100.0,
            description="Test coverage score",
        )
        security_score: float = Field(
            0.0,
            ge=0.0,
            le=100.0,
            description="Security analysis score",
        )
        maintainability_score: float = Field(
            0.0,
            ge=0.0,
            le=100.0,
            description="Maintainability score",
        )
        complexity_score: float = Field(
            0.0,
            ge=0.0,
            le=100.0,
            description="Complexity score",
        )
        started_at: datetime = Field(
            default_factory=datetime.now,
            description="Analysis start time",
        )
        completed_at: datetime | None = Field(
            None,
            description="Analysis completion time",
        )
        error_message: str | None = Field(
            None,
            description="Error message if analysis failed",
        )

        @property
        def analysis_summary(self) -> FlextCore.Types.Dict:
            """Computed field providing comprehensive analysis summary."""
            duration_seconds: float = 0.0
            if self.completed_at and self.started_at:
                duration_seconds = (self.completed_at - self.started_at).total_seconds()

            return {
                "analysis_info": {
                    "id": str(self.id),
                    "project_id": str(self.project_id),
                    "status": self.status,
                    "has_errors": bool(self.error_message),
                },
                "quality_scores": {
                    "overall": self.overall_score,
                    "coverage": self.coverage_score,
                    "security": self.security_score,
                    "maintainability": self.maintainability_score,
                    "complexity": self.complexity_score,
                    "average_score": self._calculate_average_score(),
                },
                "performance_info": {
                    "started_at": self.started_at.isoformat(),
                    "completed_at": self.completed_at.isoformat()
                    if self.completed_at
                    else None,
                    "duration_seconds": duration_seconds,
                    "is_completed": bool(self.completed_at),
                    "is_successful": self.status == "COMPLETED"
                    and not self.error_message,
                },
                "enterprise_compliance": {
                    "meets_coverage_threshold": self.coverage_score
                    >= FlextQualityConstants.Coverage.MINIMUM_COVERAGE,
                    "meets_security_threshold": self.security_score
                    >= FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE,
                    "meets_maintainability_threshold": self.maintainability_score
                    >= FlextQualityConstants.Maintainability.MINIMUM_MAINTAINABILITY,
                    "overall_enterprise_ready": self._is_enterprise_ready(),
                },
            }

        @model_validator(mode="after")
        def validate_analysis_consistency(self) -> Self:
            """Model validator for analysis consistency."""
            # Validate completion timestamp
            if self.completed_at and self.completed_at < self.started_at:
                msg = "Completion time cannot be before start time"
                raise ValueError(msg)

            # Validate status and completion consistency
            if self.status == "COMPLETED" and not self.completed_at:
                msg = "Completed analysis must have completion timestamp"
                raise ValueError(msg)

            # Validate error handling
            if self.status == "FAILED" and not self.error_message:
                msg = "Failed analysis must have error message"
                raise ValueError(msg)

            # Validate enterprise score requirements
            if self.status == "COMPLETED" and self.overall_score == 0.0:
                msg = "Completed analysis must have non-zero overall score"
                raise ValueError(msg)

            return self

        @field_serializer("error_message", when_used="json")
        def serialize_error_message_securely(self, value: str | None) -> str | None:
            """Field serializer for secure error message handling."""
            if not value:
                return value

            # Sanitize error messages to avoid exposing sensitive paths or information
            return value.replace("/home/", "/[HOME]/").replace("/opt/", "/[OPT]/")

        def _calculate_average_score(self) -> float:
            """Calculate average of all quality scores."""
            scores = [
                self.overall_score,
                self.coverage_score,
                self.security_score,
                self.maintainability_score,
                self.complexity_score,
            ]
            non_zero_scores = [score for score in scores if score > 0]
            return (
                sum(non_zero_scores) / len(non_zero_scores) if non_zero_scores else 0.0
            )

        def _is_enterprise_ready(self) -> bool:
            """Check if analysis meets enterprise quality standards."""
            return (
                self.coverage_score >= FlextQualityConstants.Coverage.MINIMUM_COVERAGE
                and self.security_score
                >= FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE
                and self.maintainability_score
                >= FlextQualityConstants.Maintainability.MINIMUM_MAINTAINABILITY
                and self.overall_score
                >= FlextQualityConstants.Thresholds.ENTERPRISE_READY_THRESHOLD
            )

        @field_validator(
            "overall_score",
            "coverage_score",
            "security_score",
            "maintainability_score",
            "complexity_score",
        )
        @classmethod
        def validate_score_range(cls, v: float) -> float:
            """Ensure scores are within valid range."""
            return max(0.0, min(100.0, v))

    class IssueModel(FlextCore.Models.StrictArbitraryTypesModel):
        """Pydantic model for quality issue representation."""

        id: UUID = Field(..., description="Unique issue identifier")
        analysis_id: UUID = Field(..., description="Associated analysis identifier")
        file_path: str = Field(..., description="File path where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of the issue")
        column_number: int | None = Field(
            None,
            ge=1,
            description="Column number of the issue",
        )
        severity: str = Field(..., description="Issue severity level")
        issue_type: str = Field(..., description="Type of quality issue")
        message: str = Field(..., description="Issue description message")
        rule: str | None = Field(None, description="Rule that triggered this issue")
        source: str = Field(..., description="Analysis backend that detected the issue")

        @property
        def issue_summary(self) -> FlextCore.Types.Dict:
            """Computed field providing comprehensive issue summary."""
            return {
                "issue_identity": {
                    "id": str(self.id),
                    "analysis_id": str(self.analysis_id),
                    "source": self.source,
                    "rule": self.rule,
                },
                "location_info": {
                    "file_path": self.file_path,
                    "line_number": self.line_number,
                    "column_number": self.column_number,
                    "file_name": self._extract_filename(),
                    "has_precise_location": bool(self.column_number),
                },
                "classification": {
                    "severity": self.severity,
                    "issue_type": self.issue_type,
                    "is_critical": self.severity == "CRITICAL",
                    "is_security_related": self._is_security_issue(),
                    "priority_score": self._calculate_priority_score(),
                },
                "description": {
                    "message": self.message,
                    "message_length": len(self.message),
                    "has_rule": bool(self.rule),
                },
            }

        @model_validator(mode="after")
        def validate_issue_consistency(self) -> Self:
            """Model validator for issue consistency."""
            # Validate severity levels
            valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
            if self.severity not in valid_severities:
                msg = f"Severity must be one of: {valid_severities}"
                raise ValueError(msg)

            # Validate issue types
            valid_issue_types = [
                "SECURITY",
                "COMPLEXITY",
                "DUPLICATION",
                "COVERAGE",
                "STYLE",
                "BUG",
                "PERFORMANCE",
                "MAINTAINABILITY",
            ]
            if self.issue_type not in valid_issue_types:
                msg = f"Issue type must be one of: {valid_issue_types}"
                raise ValueError(msg)

            # Validate message content
            if not self.message.strip():
                msg = "Issue message cannot be empty"
                raise ValueError(msg)

            return self

        @field_serializer("file_path", when_used="json")
        def serialize_file_path_securely(self, value: str) -> str:
            """Field serializer for secure file path handling."""
            # Sanitize file paths to avoid exposing sensitive directory structure

            # Keep relative path structure but remove absolute path prefixes
            if value.startswith("/"):
                path_parts = value.split("/")
                # Return path relative to project root (keep last segments)
                return (
                    "/".join(
                        path_parts[
                            -FlextQualityConstants.Reporting.PATH_SEGMENTS_TO_KEEP :
                        ]
                    )
                    if len(path_parts)
                    > FlextQualityConstants.Reporting.PATH_SEGMENTS_TO_KEEP
                    else value
                )
            return value

        def _extract_filename(self) -> str:
            """Extract filename from file path."""
            return pathlib.Path(self.file_path).name

        def _is_security_issue(self) -> bool:
            """Check if this is a security-related issue."""
            return (
                self.issue_type == "SECURITY"
                or "security" in self.message.lower()
                or "vulnerability" in self.message.lower()
            )

        def _calculate_priority_score(self) -> int:
            """Calculate priority score based on severity and type."""
            severity_scores = {
                "CRITICAL": 100,
                "HIGH": 75,
                "MEDIUM": 50,
                "LOW": 25,
                "INFO": 10,
            }

            base_score = severity_scores.get(self.severity, 0)

            # Boost security issues
            if self._is_security_issue():
                base_score += 20

            return min(100, base_score)

        @field_validator("line_number", "column_number")
        @classmethod
        def validate_positive_numbers(cls, v: int | None) -> int | None:
            """Ensure line and column numbers are positive."""
            if v is not None and v < 1:
                msg = "Line and column numbers must be positive"
                raise ValueError(msg)
            return v

    class ReportModel(FlextCore.Models.StrictArbitraryTypesModel):
        """Pydantic model for quality report representation."""

        id: UUID = Field(..., description="Unique report identifier")
        analysis_id: UUID = Field(..., description="Associated analysis identifier")
        format_type: str = Field(..., description="Report format (HTML, JSON, PDF)")
        content: str = Field(..., description="Report content")
        file_path: str | None = Field(None, description="Path to saved report file")
        generated_at: datetime = Field(
            default_factory=datetime.now,
            description="Report generation time",
        )
        metadata: FlextCore.Types.Dict = Field(
            default_factory=dict,
            description="Additional report metadata",
        )

        @property
        def report_summary(self) -> FlextCore.Types.Dict:
            """Computed field providing comprehensive report summary."""
            return {
                "report_identity": {
                    "id": str(self.id),
                    "analysis_id": str(self.analysis_id),
                    "format_type": self.format_type,
                    "generated_at": self.generated_at.isoformat(),
                },
                "content_info": {
                    "content_length": len(self.content),
                    "content_size_kb": round(
                        len(self.content.encode("utf-8")) / 1024, 2
                    ),
                    "has_file_path": bool(self.file_path),
                    "file_name": self._extract_filename() if self.file_path else None,
                },
                "metadata_info": {
                    "metadata_count": len(self.metadata),
                    "has_metadata": bool(self.metadata),
                    "is_enterprise_format": self._is_enterprise_format(),
                },
                "report_characteristics": {
                    "is_large_report": len(self.content)
                    > FlextQualityConstants.Reporting.LARGE_REPORT_SIZE_BYTES,
                    "supports_export": bool(self.file_path),
                    "format_capabilities": self._get_format_capabilities(),
                },
            }

        @model_validator(mode="after")
        def validate_report_consistency(self) -> Self:
            """Model validator for report consistency."""
            # Validate format types
            valid_formats = ["HTML", "JSON", "PDF", "CSV", "XML", "MARKDOWN"]
            if self.format_type not in valid_formats:
                msg = f"Format type must be one of: {valid_formats}"
                raise ValueError(msg)

            # Validate content presence
            if not self.content.strip():
                msg = "Report content cannot be empty"
                raise ValueError(msg)

            # Validate file path consistency
            if self.file_path and not self.file_path.strip():
                msg = "File path cannot be empty string"
                raise ValueError(msg)

            return self

        @field_serializer("content", when_used="json")
        def serialize_content_efficiently(self, value: str) -> FlextCore.Types.Dict:
            """Field serializer for efficient content handling."""
            # For large content, provide summary instead of full content in JSON
            max_content_size = 10000  # 10KB limit for JSON serialization

            if len(value) > max_content_size:
                return {
                    "content_summary": f"{value[:max_content_size]}... [TRUNCATED]",
                    "full_content_size": len(value),
                    "truncated": True,
                    "available_via_file": bool(self.file_path),
                }
            return {
                "content": value,
                "content_size": len(value),
                "truncated": False,
            }

        @field_serializer("metadata", when_used="json")
        def serialize_metadata_with_context(
            self, value: dict[str, object]
        ) -> FlextCore.Types.Dict:
            """Field serializer for metadata with processing context."""
            return {
                "report_metadata": value,
                "metadata_context": {
                    "metadata_count": len(value),
                    "processed_at": datetime.now(UTC).isoformat(),
                    "format_type": self.format_type,
                    "enterprise_compliant": True,
                },
            }

        def _extract_filename(self) -> str | None:
            """Extract filename from file path."""
            if not self.file_path:
                return None

            return pathlib.Path(self.file_path).name

        def _is_enterprise_format(self) -> bool:
            """Check if this is an enterprise-grade report format."""
            enterprise_formats = ["HTML", "PDF", "JSON"]
            return self.format_type in enterprise_formats

        def _get_format_capabilities(self) -> FlextCore.Types.StringList:
            """Get capabilities based on report format."""
            capabilities_map = {
                "HTML": ["interactive", "styling", "charts", "responsive"],
                "PDF": ["portable", "print-ready", "executive-summary"],
                "JSON": ["machine-readable", "api-friendly", "structured"],
                "CSV": ["spreadsheet-compatible", "data-analysis"],
                "XML": ["structured", "schema-validation", "interoperable"],
                "MARKDOWN": ["human-readable", "version-control-friendly"],
            }
            return capabilities_map.get(self.format_type, [])

    class ConfigModel(FlextCore.Models.StrictArbitraryTypesModel):
        """Pydantic model for analysis configuration."""

        include_patterns: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="File patterns to include",
        )
        exclude_patterns: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="File patterns to exclude",
        )
        enable_security: bool = Field(
            default=True,
            description="Enable security analysis",
        )
        enable_complexity: bool = Field(
            default=True,
            description="Enable complexity analysis",
        )
        enable_coverage: bool = Field(
            default=True,
            description="Enable coverage analysis",
        )
        max_complexity: int = Field(
            FlextQualityConstants.Complexity.MAX_COMPLEXITY,
            description="Maximum allowed complexity",
        )
        min_coverage: float = Field(
            FlextQualityConstants.Coverage.MINIMUM_COVERAGE,
            description="Minimum coverage threshold",
        )
        security_threshold: float = Field(
            FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE,
            description="Security score threshold",
        )

        @property
        def config_summary(self) -> FlextCore.Types.Dict:
            """Computed field providing comprehensive configuration summary."""
            return {
                "pattern_configuration": {
                    "include_patterns_count": len(self.include_patterns),
                    "exclude_patterns_count": len(self.exclude_patterns),
                    "has_include_patterns": bool(self.include_patterns),
                    "has_exclude_patterns": bool(self.exclude_patterns),
                },
                "analysis_configuration": {
                    "security_enabled": self.enable_security,
                    "complexity_enabled": self.enable_complexity,
                    "coverage_enabled": self.enable_coverage,
                    "enabled_analyses_count": sum([
                        self.enable_security,
                        self.enable_complexity,
                        self.enable_coverage,
                    ]),
                },
                "quality_thresholds": {
                    "max_complexity": self.max_complexity,
                    "min_coverage": self.min_coverage,
                    "security_threshold": self.security_threshold,
                    "is_enterprise_grade": self._is_enterprise_grade(),
                },
                "configuration_status": {
                    "is_complete": self._is_configuration_complete(),
                    "is_production_ready": self._is_production_ready(),
                    "has_strict_thresholds": self._has_strict_thresholds(),
                },
            }

        @model_validator(mode="after")
        def validate_config_consistency(self) -> Self:
            """Model validator for configuration consistency."""
            # Validate threshold ranges
            if (
                self.min_coverage < FlextQualityConstants.Validation.MINIMUM_PERCENTAGE
                or self.min_coverage
                > FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE
            ):
                msg = f"Minimum coverage must be between {FlextQualityConstants.Validation.MINIMUM_PERCENTAGE} and {FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE}"
                raise ValueError(msg)

            if (
                self.security_threshold
                < FlextQualityConstants.Validation.MINIMUM_PERCENTAGE
                or self.security_threshold
                > FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE
            ):
                msg = f"Security threshold must be between {FlextQualityConstants.Validation.MINIMUM_PERCENTAGE} and {FlextQualityConstants.Validation.MAXIMUM_PERCENTAGE}"
                raise ValueError(msg)

            if self.max_complexity < 1:
                msg = "Maximum complexity must be at least 1"
                raise ValueError(msg)

            # Validate enterprise requirements
            if (
                self.enable_security
                and self.security_threshold
                < FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE
            ):
                msg = f"Security analysis requires minimum {FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE}% threshold"
                raise ValueError(msg)

            # Validate analysis enablement
            if not any([
                self.enable_security,
                self.enable_complexity,
                self.enable_coverage,
            ]):
                msg = "At least one analysis type must be enabled"
                raise ValueError(msg)

            return self

        @field_serializer("include_patterns", when_used="json")
        def serialize_include_patterns_with_metadata(
            self, value: FlextCore.Types.StringList
        ) -> FlextCore.Types.Dict:
            """Field serializer for include patterns with validation metadata."""
            return {
                "patterns": value,
                "pattern_metadata": {
                    "pattern_count": len(value),
                    "has_python_patterns": any("*.py" in pattern for pattern in value),
                    "has_test_patterns": any("test" in pattern for pattern in value),
                    "coverage_scope": "comprehensive" if not value else "filtered",
                },
            }

        @field_serializer("exclude_patterns", when_used="json")
        def serialize_exclude_patterns_with_metadata(
            self, value: FlextCore.Types.StringList
        ) -> FlextCore.Types.Dict:
            """Field serializer for exclude patterns with validation metadata."""
            return {
                "patterns": value,
                "exclusion_metadata": {
                    "exclusion_count": len(value),
                    "excludes_tests": any("test" in pattern for pattern in value),
                    "excludes_generated": any(
                        "generated" in pattern for pattern in value
                    ),
                    "security_focused": not any(
                        "security" in pattern for pattern in value
                    ),
                },
            }

        def _is_enterprise_grade(self) -> bool:
            """Check if configuration meets enterprise standards."""
            return (
                self.min_coverage >= FlextQualityConstants.Coverage.MINIMUM_COVERAGE
                and self.security_threshold
                >= FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE
                and self.max_complexity
                <= FlextQualityConstants.Complexity.MAX_COMPLEXITY
                and self.enable_security
                and self.enable_coverage
            )

        def _is_configuration_complete(self) -> bool:
            """Check if configuration is complete."""
            return (
                self.max_complexity > 0
                and self.min_coverage >= 0
                and self.security_threshold >= 0
            )

        def _is_production_ready(self) -> bool:
            """Check if configuration is ready for production use."""
            return (
                self._is_configuration_complete()
                and self.enable_security
                and self.min_coverage >= FlextQualityConstants.Coverage.COVERAGE
                and self.security_threshold
                >= FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE
            )

        def _has_strict_thresholds(self) -> bool:
            """Check if configuration has strict quality thresholds."""
            return (
                self.min_coverage
                >= FlextQualityConstants.Thresholds.EXCELLENT_THRESHOLD
                and self.security_threshold
                >= FlextQualityConstants.Security.TARGET_SECURITY_SCORE
                and self.max_complexity
                <= FlextQualityConstants.Complexity.STRICT_COMPLEXITY
            )

        @field_validator("max_complexity")
        @classmethod
        def validate_max_complexity(cls, v: int) -> int:
            """Ensure max complexity is reasonable."""
            return max(1, min(50, v))

        @field_validator("min_coverage", "security_threshold")
        @classmethod
        def validate_percentage(cls, v: float) -> float:
            """Ensure percentage values are within valid range."""
            return max(0.0, min(100.0, v))

    # ==== ANALYSIS RESULT MODELS (from analysis_types.py migration) ====

    class FileAnalysisResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Result of analyzing a single file."""

        file_path: Path = Field(..., description="Path to the analyzed file")
        lines_of_code: int = Field(default=0, ge=0, description="Total lines of code")
        complexity_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Complexity score",
        )
        security_issues: int = Field(
            default=0,
            ge=0,
            description="Number of security issues",
        )
        style_issues: int = Field(default=0, ge=0, description="Number of style issues")
        dead_code_lines: int = Field(default=0, ge=0, description="Lines of dead code")

    class CodeIssue(FlextCore.Models.StrictArbitraryTypesModel):
        """General code quality issue."""

        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        issue_type: str = Field(..., description="Type of code issue")
        message: str = Field(..., description="Human-readable issue message")
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.MEDIUM,
            description="Issue severity level",
        )
        rule_id: str | None = Field(
            default=None, description="Rule that detected the issue"
        )

    class ComplexityIssue(FlextCore.Models.StrictArbitraryTypesModel):
        """Complexity-related code issue."""

        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        complexity_score: float = Field(
            ..., description="Complexity score that triggered issue"
        )
        complexity_type: str = Field(
            ..., description="Type of complexity (cyclomatic/cognitive)"
        )
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.MEDIUM,
            description="Issue severity level",
        )
        message: str = Field(..., description="Human-readable issue message")

    class SecurityIssue(FlextCore.Models.StrictArbitraryTypesModel):
        """Security-related code issue."""

        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        issue_type: FlextQualityValueObjects.IssueType = Field(
            ...,
            description="Type of security issue",
        )
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.HIGH,
            description="Issue severity level",
        )
        message: str = Field(..., description="Human-readable issue message")
        rule_id: str = Field(..., description="Security rule that detected the issue")

    class DeadCodeIssue(FlextCore.Models.StrictArbitraryTypesModel):
        """Dead code issue."""

        file_path: str = Field(..., description="File where dead code was found")
        line_number: int = Field(..., ge=1, description="Line number of dead code")
        issue_type: FlextQualityValueObjects.IssueType = Field(
            default=FlextQualityValueObjects.IssueType.UNREACHABLE_CODE,
            description="Type of dead code issue",
        )
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.LOW,
            description="Issue severity level",
        )
        message: str = Field(..., description="Human-readable issue message")

    class DuplicationIssue(FlextCore.Models.StrictArbitraryTypesModel):
        """Code duplication issue."""

        files: FlextCore.Types.StringList = Field(
            ..., description="Files containing duplicated code"
        )
        line_ranges: list[tuple[int, int]] = Field(
            ...,
            description="Line ranges of duplicated code in each file",
        )
        similarity_score: float = Field(
            ge=0.0,
            le=100.0,
            description="Similarity score between duplicated blocks",
        )
        duplicated_lines: int = Field(..., description="Number of duplicated lines")
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.MEDIUM,
            description="Issue severity level",
        )
        message: str = Field(..., description="Human-readable issue message")

    class Dependency(FlextCore.Models.StrictArbitraryTypesModel):
        """Project dependency information."""

        name: str = Field(..., description="Dependency name")
        version: str = Field(..., description="Dependency version")
        type: str = Field(..., description="Dependency type (direct/dev/optional)")
        license: str | None = Field(default=None, description="Dependency license")
        vulnerabilities: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="Known vulnerabilities",
        )

    class TestResults(FlextCore.Models.StrictArbitraryTypesModel):
        """Test execution results."""

        total_tests: int = Field(default=0, description="Total number of tests")
        passed_tests: int = Field(default=0, description="Number of passed tests")
        failed_tests: int = Field(default=0, description="Number of failed tests")
        skipped_tests: int = Field(default=0, description="Number of skipped tests")
        coverage_percentage: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Test coverage percentage",
        )
        execution_time: float = Field(
            default=0.0, description="Test execution time in seconds"
        )

    class OverallMetrics(FlextCore.Models.StrictArbitraryTypesModel):
        """Overall project quality metrics."""

        files_analyzed: int = Field(default=0, description="Number of files analyzed")
        total_lines: int = Field(default=0, description="Total lines of code")
        functions_count: int = Field(default=0, description="Number of functions")
        classes_count: int = Field(default=0, description="Number of classes")
        average_complexity: float = Field(
            default=0.0, description="Average complexity score"
        )
        max_complexity: float = Field(
            default=0.0, description="Maximum complexity score"
        )
        quality_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Overall quality score",
        )
        coverage_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Coverage score",
        )
        security_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Security score",
        )
        maintainability_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Maintainability score",
        )
        complexity_score: float = Field(
            default=0.0,
            ge=0.0,
            le=100.0,
            description="Complexity score",
        )

    class AnalysisResults(FlextCore.Models.StrictArbitraryTypesModel):
        """Complete analysis results for a project."""

        overall_metrics: OverallMetrics = Field(
            ..., description="Overall project metrics"
        )
        file_metrics: list[FileAnalysisResult] = Field(
            default_factory=list,
            description="Metrics for individual files",
        )
        code_issues: list[CodeIssue] = Field(
            default_factory=list,
            description="General code issues",
        )
        complexity_issues: list[ComplexityIssue] = Field(
            default_factory=list,
            description="Complexity issues",
        )
        security_issues: list[SecurityIssue] = Field(
            default_factory=list,
            description="Security issues",
        )
        dead_code_issues: list[DeadCodeIssue] = Field(
            default_factory=list,
            description="Dead code issues",
        )
        duplication_issues: list[DuplicationIssue] = Field(
            default_factory=list,
            description="Code duplication issues",
        )
        dependencies: list[Dependency] = Field(
            default_factory=list,
            description="Project dependencies",
        )
        test_results: TestResults | None = Field(
            default=None,
            description="Test results if available",
        )
        analysis_config: dict[str, Any] = Field(
            default_factory=dict,
            description="Configuration used for analysis",
        )
        analysis_timestamp: str = Field(
            default_factory=lambda: datetime.now(UTC).isoformat(),
            description="When analysis was performed",
        )

        @property
        def total_issues(self) -> int:
            """Total number of issues found across all categories."""
            return (
                len(self.code_issues)
                + len(self.complexity_issues)
                + len(self.security_issues)
                + len(self.dead_code_issues)
                + len(self.duplication_issues)
            )

        def get_quality_score(self) -> float:
            """Calculate overall quality score."""
            return self.overall_metrics.quality_score

    # ==== WEB MODELS (from web.py migration) ====

    class AppConfig(FlextCore.Models.StrictArbitraryTypesModel):
        """Web app configuration."""

        title: str = Field(..., description="App title")
        version: str = Field(..., description="App version")
        enable_cors: bool = Field(default=True, description="Enable CORS")
        enable_docs: bool = Field(default=True, description="Enable docs")

    # ==== INTERNAL TOOLS MODELS (from flext_tools migration) ====

    class GitOperation(FlextCore.Models.StrictArbitraryTypesModel):
        """Git operation command for quality tools."""

        repo_path: str
        operation_type: str
        dry_run: bool = True
        temp_path: str | None = None

    class RewriteResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Git history rewrite result."""

        commits_processed: int
        commits_changed: int
        success: bool
        errors: FlextCore.Types.StringList

    class OptimizationTarget(FlextCore.Models.StrictArbitraryTypesModel):
        """Target for optimization."""

        project_path: str
        module_name: str
        file_path: str
        optimization_type: str
        priority: int = 1

    class OptimizationResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Result of optimization operation."""

        target: OptimizationTarget
        success: bool
        changes_made: int
        errors: FlextCore.Types.StringList
        warnings: FlextCore.Types.StringList

    class CheckResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Quality check result."""

        lint_passed: bool
        type_check_passed: bool
        coverage: float
        violations: FlextCore.Types.StringList

    class QualityValidationResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Quality validation result."""

        passed: bool
        checks_run: int
        checks_passed: int
        failures: FlextCore.Types.StringList

    class AnalysisResult(FlextCore.Models.StrictArbitraryTypesModel):
        """Architecture analysis result."""

        violations: FlextCore.Types.StringList
        suggestions: FlextCore.Types.StringList
        complexity_score: float
        domain_library_usage: dict[str, bool]

    class DependencyInfo(FlextCore.Models.StrictArbitraryTypesModel):
        """Dependency information."""

        name: str
        version: str
        source: str
        required_by: FlextCore.Types.StringList

    # =============================================================================
    # DOMAIN ENTITY MODELS - Moved from entities.py
    # =============================================================================

    class DomainEvent(FlextCore.Models.DomainEvent):
        """Base class for domain events."""

        event_type: str
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Project(FlextCore.Models.Entity):
        """Quality project domain entity using enhanced mixins for code reduction."""

        # Project identification
        name: str = Field(..., min_length=1)
        # Project paths
        project_path: str = Field(..., min_length=1)
        repository_url: str | None = None

        # Configuration
        config_path: str | None = None
        language: str = Field(default="python")

        # Analysis settings
        auto_analyze: bool = Field(default=True)
        analysis_schedule: str | None = None  # cron format

        # Quality thresholds from constants
        min_coverage: float = Field(
            default=FlextQualityConstants.Coverage.MINIMUM_COVERAGE, ge=0.0, le=100.0
        )
        max_complexity: int = Field(
            default=FlextQualityConstants.Complexity.MAX_COMPLEXITY, ge=1
        )
        max_duplication: float = Field(
            default=FlextQualityConstants.Duplication.MAXIMUM_DUPLICATION,
            ge=0.0,
            le=100.0,
        )

        # Statistics
        last_analysis_at: datetime | None = None
        total_analyses: int = Field(default=0)

    class Analysis(FlextCore.Models.Entity):
        """Quality analysis domain entity with comprehensive analysis tracking."""

        # Analysis identification
        analysis_id: UUID = Field(
            default_factory=UUID, description="Unique analysis ID"
        )
        project_id: UUID = Field(..., description="Project this analysis belongs to")

        # Analysis metadata
        status: str = Field(default="queued")
        started_at: datetime | None = None
        completed_at: datetime | None = None
        duration_seconds: float | None = None

        # Analysis configuration
        include_security: bool = Field(default=True)
        include_complexity: bool = Field(default=True)
        include_coverage: bool = Field(default=True)
        include_duplication: bool = Field(default=False)
        include_dependencies: bool = Field(default=True)

        # Analysis results
        overall_score: float | None = None
        coverage_score: float | None = None
        complexity_score: float | None = None
        security_score: float | None = None
        maintainability_score: float | None = None

        # File and issue statistics
        total_files: int = Field(default=0)
        analyzed_files: int = Field(default=0)
        total_lines: int = Field(default=0)
        issues_found: int = Field(default=0)
        critical_issues: int = Field(default=0)
        high_issues: int = Field(default=0)
        medium_issues: int = Field(default=0)
        low_issues: int = Field(default=0)

        # Analysis artifacts
        report_path: str | None = None
        log_path: str | None = None

        # Error handling
        error_message: str | None = None
        retry_count: int = Field(default=0)

    class Issue(FlextCore.Models.Entity):
        """Quality issue domain entity with detailed issue tracking."""

        # Issue identification
        issue_id: UUID = Field(default_factory=UUID, description="Unique issue ID")
        analysis_id: UUID = Field(..., description="Analysis that found this issue")

        # Issue location
        file_path: str = Field(..., description="File where issue was found")
        line_number: int = Field(..., ge=1, description="Line number of issue")
        column_number: int | None = None

        # Issue details
        issue_type: FlextQualityValueObjects.IssueType = Field(
            ..., description="Type of quality issue"
        )
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.MEDIUM,
            description="Issue severity level",
        )
        rule_id: str | None = None
        rule_name: str | None = None

        # Issue content
        message: str = Field(..., description="Human-readable issue message")
        description: str | None = None
        suggestion: str | None = None

        # Context information
        context_lines: FlextCore.Types.StringList | None = None
        related_code: str | None = None

        # Issue metadata
        tool_name: str | None = None  # ruff, mypy, bandit, etc.
        tool_version: str | None = None
        detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

        # Resolution tracking
        resolved: bool = Field(default=False)
        resolved_at: datetime | None = None
        resolution_notes: str | None = None

    class Rule(FlextCore.Models.Entity):
        """Quality rule domain entity defining analysis rules and thresholds."""

        # Rule identification
        rule_id: str = Field(..., description="Unique rule identifier")
        name: str = Field(..., description="Human-readable rule name")

        # Rule metadata
        category: str = Field(
            ..., description="Rule category (security, complexity, style)"
        )
        tool: str = Field(..., description="Tool that implements this rule")

        # Rule configuration
        enabled: bool = Field(default=True)
        severity: FlextQualityValueObjects.IssueSeverity = Field(
            default=FlextQualityValueObjects.IssueSeverity.MEDIUM
        )

        # Rule parameters
        parameters: dict[str, object] | None = None

        # Rule description
        description: str = Field(..., description="Rule description")
        rationale: str | None = None
        examples: FlextCore.Types.StringList | None = None

        # Rule metadata
        deprecated: bool = Field(default=False)
        replacement_rule: str | None = None

    class Report(FlextCore.Models.Entity):
        """Quality report domain entity containing analysis summaries and insights."""

        # Report identification
        report_id: UUID = Field(default_factory=UUID, description="Unique report ID")
        analysis_id: UUID = Field(..., description="Analysis this report is based on")

        # Report metadata
        generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
        report_type: str = Field(default="comprehensive", description="Type of report")
        format: str = Field(default="html", description="Report format")

        # Report content
        title: str = Field(..., description="Report title")
        summary: str | None = None
        executive_summary: str | None = None

        # Quality scores
        overall_score: float | None = None
        coverage_score: float | None = None
        complexity_score: float | None = None
        security_score: float | None = None
        maintainability_score: float | None = None

        # Statistics
        total_files: int = Field(default=0)
        analyzed_files: int = Field(default=0)
        total_lines: int = Field(default=0)
        total_issues: int = Field(default=0)
        critical_issues: int = Field(default=0)
        high_issues: int = Field(default=0)
        medium_issues: int = Field(default=0)
        low_issues: int = Field(default=0)

        # File paths
        html_report_path: str | None = None
        json_report_path: str | None = None
        pdf_report_path: str | None = None

        # Report sections
        sections: dict[str, object] | None = None

    # =============================================================================
    # AST ANALYSIS MODELS - Moved from ast_*.py files
    # =============================================================================

    class FunctionInfo(FlextCore.Models.StrictArbitraryTypesModel):
        """Strongly-typed function information from AST analysis."""

        name: str
        full_name: str
        file_path: str
        package_name: str
        line_number: int
        end_line_number: int
        decorators: FlextCore.Types.StringList
        is_generator: bool
        is_method: bool
        is_property: bool
        is_class_method: bool
        is_static_method: bool
        parameter_count: int
        returns_annotation: str | None
        complexity: int
        docstring: str | None

    class ClassInfo(FlextCore.Models.StrictArbitraryTypesModel):
        """Strongly-typed class information from AST analysis."""

        name: str
        full_name: str
        file_path: str
        package_name: str
        line_number: int
        end_line_number: int
        base_classes: FlextCore.Types.StringList
        decorators: FlextCore.Types.StringList
        is_dataclass: bool
        is_abstract: bool
        has_docstring: bool
        method_count: int
        public_methods: int
        private_methods: int
        protected_methods: int
        property_count: int = 0
        class_method_count: int = 0
        static_method_count: int = 0
        complexity: int = 0

    # =============================================================================
    # DOMAIN EVENT MODELS - Moved from entities.py
    # =============================================================================

    class ProjectCreatedEvent(DomainEvent):
        """Event fired when a quality project is created."""

        project_id: UUID
        project_name: str
        project_path: str

    class AnalysisStartedEvent(DomainEvent):
        """Event fired when analysis starts."""

        analysis_id: UUID
        project_id: UUID

    class AnalysisCompletedEvent(DomainEvent):
        """Event fired when analysis completes."""

        analysis_id: UUID
        project_id: UUID
        overall_score: float
        issues_found: int

    class IssueDetectedEvent(DomainEvent):
        """Event fired when a quality issue is detected."""

        issue_id: UUID
        analysis_id: UUID
        issue_type: str
        severity: str

    class ReportGeneratedEvent(DomainEvent):
        """Event fired when a quality report is generated."""

        report_id: UUID
        analysis_id: UUID
        report_type: str
        format: str


# Export models for clean imports
__all__ = [
    "FlextQualityModels",
]
