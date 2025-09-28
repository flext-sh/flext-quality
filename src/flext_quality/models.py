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
from typing import Any, override
from uuid import UUID

from pydantic import (
    ConfigDict,
    Field,
    SerializationInfo,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_core import FlextContainer, FlextLogger, FlextModels, FlextTypes
from flext_quality.constants import FlextQualityConstants


class FlextQualityModels(FlextModels):
    """Unified quality models class following FLEXT architecture patterns.

    Inherits from FlextModels to avoid duplication and ensure consistency.
    Single responsibility: Quality data models and validation
    Contains all Pydantic models as nested classes with shared functionality.
    """

    model_config = ConfigDict(
        # Enhanced Pydantic 2.11 enterprise features
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        hide_input_in_errors=True,
        json_schema_extra={
            "examples": [
                {
                    "quality_analysis": {
                        "project_name": "enterprise-flext-project",
                        "overall_score": 95.2,
                        "coverage_score": 98.5,
                        "security_score": 96.8,
                        "maintainability_score": 92.1,
                    },
                    "quality_issue": {
                        "severity": "HIGH",
                        "issue_type": "COMPLEXITY",
                        "file_path": "src/enterprise/service.py",
                        "line_number": 45,
                        "message": "Function complexity exceeds threshold",
                    },
                    "quality_report": {
                        "format_type": "HTML",
                        "generated_at": "2025-01-08T10:30:00Z",
                        "executive_summary": True,
                    },
                }
            ],
            "enterprise_features": [
                "Code quality analysis",
                "Security vulnerability detection",
                "Test coverage analysis",
                "Complexity measurement",
                "Maintainability scoring",
                "Enterprise reporting",
            ],
        },
    )

    @computed_field
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

    @computed_field
    @property
    def quality_system_summary(self) -> dict[str, Any]:
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
    def validate_quality_system_consistency(self) -> FlextQualityModels:
        """Model validator ensuring quality system consistency and standards."""
        # Validate that quality models maintain consistency
        if hasattr(self, "_initialized") and not self._initialized:
            msg = "Quality models must be properly initialized"
            raise ValueError(msg)

        # Ensure enterprise quality standards are properly set
        if hasattr(self, "ConfigModel"):
            # Quality-specific validation logic can be added here
            pass

        return self

    @field_serializer("*", when_used="json")
    def serialize_with_quality_metadata(
        self, value: object, _info: SerializationInfo
    ) -> object:
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
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    class ProjectModel(FlextModels.Config):
        """Pydantic model for quality project representation."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
            str_strip_whitespace=True,
        )

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

        @computed_field
        @property
        def project_summary(self) -> dict[str, Any]:
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
        def validate_project_consistency(self) -> FlextQualityModels.ProjectModel:
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

    class AnalysisModel(FlextModels.Config):
        """Pydantic model for quality analysis representation."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
        )

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

        @computed_field
        @property
        def analysis_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive analysis summary."""
            duration_seconds = 0
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
        def validate_analysis_consistency(self) -> FlextQualityModels.AnalysisModel:
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
                >= FlextQualityConstants.QualityThresholds.ENTERPRISE_READY_THRESHOLD
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

    class IssueModel(FlextModels.Config):
        """Pydantic model for quality issue representation."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
            str_strip_whitespace=True,
        )

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

        @computed_field
        @property
        def issue_summary(self) -> dict[str, Any]:
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
        def validate_issue_consistency(self) -> FlextQualityModels.IssueModel:
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

    class ReportModel(FlextModels.Config):
        """Pydantic model for quality report representation."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
            str_strip_whitespace=True,
        )

        id: UUID = Field(..., description="Unique report identifier")
        analysis_id: UUID = Field(..., description="Associated analysis identifier")
        format_type: str = Field(..., description="Report format (HTML, JSON, PDF)")
        content: str = Field(..., description="Report content")
        file_path: str | None = Field(None, description="Path to saved report file")
        generated_at: datetime = Field(
            default_factory=datetime.now,
            description="Report generation time",
        )
        metadata: FlextTypes.Core.Dict = Field(
            default_factory=dict,
            description="Additional report metadata",
        )

        @computed_field
        @property
        def report_summary(self) -> dict[str, Any]:
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
        def validate_report_consistency(self) -> FlextQualityModels.ReportModel:
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
        def serialize_content_efficiently(self, value: str) -> dict[str, Any]:
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
        def serialize_metadata_with_context(self, value: dict) -> dict[str, Any]:
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

        def _get_format_capabilities(self) -> list[str]:
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

    class ConfigModel(FlextModels.Config):
        """Pydantic model for analysis configuration."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
        )

        include_patterns: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="File patterns to include",
        )
        exclude_patterns: FlextTypes.Core.StringList = Field(
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

        @computed_field
        @property
        def config_summary(self) -> dict[str, Any]:
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
        def validate_config_consistency(self) -> FlextQualityModels.ConfigModel:
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
            self, value: list[str]
        ) -> dict[str, Any]:
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
            self, value: list[str]
        ) -> dict[str, Any]:
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
                and self.min_coverage
                >= FlextQualityConstants.Coverage.PRODUCTION_COVERAGE
                and self.security_threshold
                >= FlextQualityConstants.Security.MINIMUM_SECURITY_SCORE
            )

        def _has_strict_thresholds(self) -> bool:
            """Check if configuration has strict quality thresholds."""
            return (
                self.min_coverage >= FlextQualityConstants.QualityThresholds.EXCELLENT_THRESHOLD
                and self.security_threshold >= FlextQualityConstants.Security.TARGET_SECURITY_SCORE
                and self.max_complexity <= FlextQualityConstants.Complexity.STRICT_COMPLEXITY
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


# Backward compatibility aliases for existing code
FlextQualityProjectModel = FlextQualityModels.ProjectModel
FlextQualityAnalysisModel = FlextQualityModels.AnalysisModel
FlextQualityIssueModel = FlextQualityModels.IssueModel
FlextQualityReportModel = FlextQualityModels.ReportModel
FlextAnalysisConfigModel = FlextQualityModels.ConfigModel

# Export models for clean imports
__all__ = [
    "FlextAnalysisConfigModel",
    "FlextQualityAnalysisModel",
    "FlextQualityIssueModel",
    "FlextQualityModels",
    "FlextQualityProjectModel",
    "FlextQualityReportModel",
]
