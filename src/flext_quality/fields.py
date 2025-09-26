"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from flext_core import FlextContainer, FlextLogger


class FlextQualityFields:
    """Unified quality fields class following FLEXT architecture patterns.

    Single responsibility: Quality Pydantic field definitions
    Contains all field factory functions as static methods with shared functionality.
    """

    @override
    def __init__(self: object) -> None:
        """Initialize fields with dependency injection."""
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    @staticmethod
    def entity_id_field(description: str = "Unique entity identifier") -> FieldInfo:
        """Standard UUID field for entity identifiers."""
        return cast("FieldInfo", Field(..., description=description))

    @staticmethod
    def optional_entity_id_field(
        description: str = "Optional entity identifier",
    ) -> FieldInfo:
        """Optional UUID field for entity identifiers."""
        return cast("FieldInfo", Field(None, description=description))

    @staticmethod
    def created_at_field() -> FieldInfo:
        """Standard created_at timestamp field."""
        return cast(
            "FieldInfo",
            Field(
                default_factory=datetime.now,
                description="Creation timestamp",
            ),
        )

    @staticmethod
    def updated_at_field() -> FieldInfo:
        """Standard updated_at timestamp field."""
        return cast(
            "FieldInfo",
            Field(
                default_factory=datetime.now,
                description="Last update timestamp",
            ),
        )

    @staticmethod
    def optional_completed_at_field() -> FieldInfo:
        """Optional completion timestamp field."""
        return cast("FieldInfo", Field(None, description="Completion timestamp"))

    @staticmethod
    def started_at_field() -> FieldInfo:
        """Analysis start timestamp field."""
        return cast(
            "FieldInfo",
            Field(
                default_factory=datetime.now,
                description="Analysis start time",
            ),
        )

    @staticmethod
    def quality_score_field(description: str = "Quality score") -> FieldInfo:
        """Standard quality score field (0-100)."""
        return cast(
            "FieldInfo",
            Field(
                0.0,
                ge=0.0,
                le=100.0,
                description=description,
            ),
        )

    @staticmethod
    def overall_score_field() -> FieldInfo:
        """Overall quality score field."""
        return FlextQualityFields.quality_score_field("Overall quality score")

    @staticmethod
    def coverage_score_field() -> FieldInfo:
        """Test coverage score field."""
        return FlextQualityFields.quality_score_field("Test coverage score")

    @staticmethod
    def security_score_field() -> FieldInfo:
        """Security analysis score field."""
        return FlextQualityFields.quality_score_field("Security analysis score")

    @staticmethod
    def maintainability_score_field() -> FieldInfo:
        """Maintainability score field."""
        return FlextQualityFields.quality_score_field("Maintainability score")

    @staticmethod
    def complexity_score_field() -> FieldInfo:
        """Complexity score field."""
        return FlextQualityFields.quality_score_field("Complexity score")

    @staticmethod
    def file_path_field(description: str = "File path") -> FieldInfo:
        """Standard file path field."""
        return cast("FieldInfo", Field(..., description=description))

    @staticmethod
    def optional_file_path_field(description: str = "Optional file path") -> FieldInfo:
        """Optional file path field."""
        return cast("FieldInfo", Field(None, description=description))

    @staticmethod
    def project_path_field() -> FieldInfo:
        """Project path field for analysis."""
        return cast("FieldInfo", Field(..., description="Project path for analysis"))

    @staticmethod
    def name_field(max_length: int = 255, description: str = "Name") -> FieldInfo:
        """Standard name field with length validation."""
        return cast(
            "FieldInfo",
            Field(
                ...,
                min_length=1,
                max_length=max_length,
                description=description,
            ),
        )

    @staticmethod
    def project_name_field() -> FieldInfo:
        """Project name field."""
        return FlextQualityFields.name_field(255, "Project name")

    @staticmethod
    def optional_description_field() -> FieldInfo:
        """Optional description field."""
        return cast("FieldInfo", Field(None, description="Description"))

    @staticmethod
    def message_field(description: str = "Message") -> FieldInfo:
        """Standard message field."""
        return cast("FieldInfo", Field(..., description=description))

    @staticmethod
    def issue_message_field() -> FieldInfo:
        """Issue description message field."""
        return FlextQualityFields.message_field("Issue description message")

    @staticmethod
    def optional_error_message_field() -> FieldInfo:
        """Optional error message field."""
        return cast(
            "FieldInfo",
            Field(None, description="Error message if operation failed"),
        )

    @staticmethod
    def content_field(description: str = "Content") -> FieldInfo:
        """Standard content field."""
        return cast("FieldInfo", Field(..., description=description))

    @staticmethod
    def report_content_field() -> FieldInfo:
        """Report content field."""
        return FlextQualityFields.content_field("Report content")

    @staticmethod
    def line_number_field() -> FieldInfo:
        """Line number field (must be positive)."""
        return cast("FieldInfo", Field(..., ge=1, description="Line number"))

    @staticmethod
    def optional_column_number_field() -> FieldInfo:
        """Optional column number field (must be positive)."""
        return cast("FieldInfo", Field(None, ge=1, description="Column number"))

    @staticmethod
    def max_complexity_field(default: int = 10) -> FieldInfo:
        """Maximum complexity threshold field."""
        return cast(
            "FieldInfo",
            Field(default, ge=1, le=50, description="Maximum allowed complexity"),
        )

    @staticmethod
    def percentage_field(
        default: float = 0.0,
        description: str = "Percentage value",
    ) -> FieldInfo:
        """Percentage field (0-100)."""
        return cast(
            "FieldInfo",
            Field(default, ge=0.0, le=100.0, description=description),
        )

    @staticmethod
    def min_coverage_field(default: float = 90.0) -> FieldInfo:
        """Minimum coverage threshold field."""
        return FlextQualityFields.percentage_field(
            default,
            "Minimum coverage threshold",
        )

    @staticmethod
    def security_threshold_field(default: float = 90.0) -> FieldInfo:
        """Security score threshold field."""
        return FlextQualityFields.percentage_field(default, "Security score threshold")

    @staticmethod
    def string_list_field(description: str = "List of strings") -> FieldInfo:
        """Standard list of strings field."""
        return cast("FieldInfo", Field(default_factory=list, description=description))

    @staticmethod
    def include_patterns_field() -> FieldInfo:
        """File patterns to include field."""
        return FlextQualityFields.string_list_field("File patterns to include")

    @staticmethod
    def exclude_patterns_field() -> FieldInfo:
        """File patterns to exclude field."""
        return FlextQualityFields.string_list_field("File patterns to exclude")

    @staticmethod
    def metadata_field() -> FieldInfo:
        """Standard metadata dictionary field."""
        return cast(
            "FieldInfo",
            Field(
                default_factory=dict,
                description="Additional metadata",
            ),
        )

    @staticmethod
    def report_metadata_field() -> FieldInfo:
        """Report metadata field."""
        return cast(
            "FieldInfo",
            Field(
                default_factory=dict,
                description="Additional report metadata",
            ),
        )

    @staticmethod
    def feature_flag_field(
        *,
        default: bool = True,
        description: str = "Feature flag",
    ) -> FieldInfo:
        """Standard feature flag field."""
        return cast("FieldInfo", Field(default, description=description))

    @staticmethod
    def enable_security_field() -> FieldInfo:
        """Enable security analysis flag."""
        return FlextQualityFields.feature_flag_field(
            default=True,
            description="Enable security analysis",
        )

    @staticmethod
    def enable_complexity_field() -> FieldInfo:
        """Enable complexity analysis flag."""
        return FlextQualityFields.feature_flag_field(
            default=True,
            description="Enable complexity analysis",
        )

    @staticmethod
    def enable_coverage_field() -> FieldInfo:
        """Enable coverage analysis flag."""
        return FlextQualityFields.feature_flag_field(
            default=True,
            description="Enable coverage analysis",
        )

    @staticmethod
    def status_field(description: str = "Status") -> FieldInfo:
        """Standard status field."""
        return cast("FieldInfo", Field(..., description=description))

    @staticmethod
    def analysis_status_field() -> FieldInfo:
        """Analysis status field."""
        return FlextQualityFields.status_field("Analysis status")

    @staticmethod
    def severity_field() -> FieldInfo:
        """Issue severity field."""
        return cast("FieldInfo", Field(..., description="Issue severity level"))

    @staticmethod
    def issue_type_field() -> FieldInfo:
        """Issue type field."""
        return cast("FieldInfo", Field(..., description="Type of quality issue"))

    @staticmethod
    def format_type_field() -> FieldInfo:
        """Report format type field."""
        return cast(
            "FieldInfo",
            Field(..., description="Report format (HTML, JSON, PDF)"),
        )

    @staticmethod
    def rule_field() -> FieldInfo:
        """Optional rule field."""
        return cast(
            "FieldInfo",
            Field(None, description="Rule that triggered this issue"),
        )

    @staticmethod
    def source_field() -> FieldInfo:
        """Analysis source field."""
        return cast(
            "FieldInfo",
            Field(..., description="Analysis backend that detected the issue"),
        )


# Backward compatibility aliases for existing code
entity_id_field = FlextQualityFields.entity_id_field
optional_entity_id_field = FlextQualityFields.optional_entity_id_field
created_at_field = FlextQualityFields.created_at_field
updated_at_field = FlextQualityFields.updated_at_field
optional_completed_at_field = FlextQualityFields.optional_completed_at_field
started_at_field = FlextQualityFields.started_at_field
quality_score_field = FlextQualityFields.quality_score_field
overall_score_field = FlextQualityFields.overall_score_field
coverage_score_field = FlextQualityFields.coverage_score_field
security_score_field = FlextQualityFields.security_score_field
maintainability_score_field = FlextQualityFields.maintainability_score_field
complexity_score_field = FlextQualityFields.complexity_score_field
file_path_field = FlextQualityFields.file_path_field
optional_file_path_field = FlextQualityFields.optional_file_path_field
project_path_field = FlextQualityFields.project_path_field
name_field = FlextQualityFields.name_field
project_name_field = FlextQualityFields.project_name_field
optional_description_field = FlextQualityFields.optional_description_field
message_field = FlextQualityFields.message_field
issue_message_field = FlextQualityFields.issue_message_field
optional_error_message_field = FlextQualityFields.optional_error_message_field
content_field = FlextQualityFields.content_field
report_content_field = FlextQualityFields.report_content_field
line_number_field = FlextQualityFields.line_number_field
optional_column_number_field = FlextQualityFields.optional_column_number_field
max_complexity_field = FlextQualityFields.max_complexity_field
percentage_field = FlextQualityFields.percentage_field
min_coverage_field = FlextQualityFields.min_coverage_field
security_threshold_field = FlextQualityFields.security_threshold_field
string_list_field = FlextQualityFields.string_list_field
include_patterns_field = FlextQualityFields.include_patterns_field
exclude_patterns_field = FlextQualityFields.exclude_patterns_field
metadata_field = FlextQualityFields.metadata_field
report_metadata_field = FlextQualityFields.report_metadata_field
feature_flag_field = FlextQualityFields.feature_flag_field
enable_security_field = FlextQualityFields.enable_security_field
enable_complexity_field = FlextQualityFields.enable_complexity_field
enable_coverage_field = FlextQualityFields.enable_coverage_field
status_field = FlextQualityFields.status_field
analysis_status_field = FlextQualityFields.analysis_status_field
severity_field = FlextQualityFields.severity_field
issue_type_field = FlextQualityFields.issue_type_field
format_type_field = FlextQualityFields.format_type_field
rule_field = FlextQualityFields.rule_field
source_field = FlextQualityFields.source_field

# Export all field functions
__all__ = [
    "FlextQualityFields",
    "analysis_status_field",
    "complexity_score_field",
    "content_field",
    "coverage_score_field",
    "created_at_field",
    "enable_complexity_field",
    "enable_coverage_field",
    "enable_security_field",
    "entity_id_field",
    "exclude_patterns_field",
    "feature_flag_field",
    "file_path_field",
    "format_type_field",
    "include_patterns_field",
    "issue_message_field",
    "issue_type_field",
    "line_number_field",
    "maintainability_score_field",
    "max_complexity_field",
    "message_field",
    "metadata_field",
    "min_coverage_field",
    "name_field",
    "optional_column_number_field",
    "optional_completed_at_field",
    "optional_description_field",
    "optional_entity_id_field",
    "optional_error_message_field",
    "optional_file_path_field",
    "overall_score_field",
    "percentage_field",
    "project_name_field",
    "project_path_field",
    "quality_score_field",
    "report_content_field",
    "report_metadata_field",
    "rule_field",
    "security_score_field",
    "security_threshold_field",
    "severity_field",
    "source_field",
    "started_at_field",
    "status_field",
    "string_list_field",
    "updated_at_field",
]
