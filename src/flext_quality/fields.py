"""Centralized Pydantic field definitions for flext-quality.

This module provides reusable, validated field definitions following FLEXT patterns.
Fields are organized by domain and provide consistent validation across all models.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import cast

from pydantic import Field
from pydantic.fields import FieldInfo

# =============================================================================
# IDENTITY FIELDS - IDs and identifiers
# =============================================================================


def entity_id_field(description: str = "Unique entity identifier") -> FieldInfo:
    """Standard UUID field for entity identifiers."""
    return cast("FieldInfo", Field(..., description=description))


def optional_entity_id_field(
    description: str = "Optional entity identifier",
) -> FieldInfo:
    """Optional UUID field for entity identifiers."""
    return cast("FieldInfo", Field(None, description=description))


# =============================================================================
# TEMPORAL FIELDS - Date/time fields
# =============================================================================


def created_at_field() -> FieldInfo:
    """Standard created_at timestamp field."""
    return cast(
        "FieldInfo",
        Field(
            default_factory=datetime.now,
            description="Creation timestamp",
        ),
    )


def updated_at_field() -> FieldInfo:
    """Standard updated_at timestamp field."""
    return cast(
        "FieldInfo",
        Field(
            default_factory=datetime.now,
            description="Last update timestamp",
        ),
    )


def optional_completed_at_field() -> FieldInfo:
    """Optional completion timestamp field."""
    return cast("FieldInfo", Field(None, description="Completion timestamp"))


def started_at_field() -> FieldInfo:
    """Analysis start timestamp field."""
    return cast(
        "FieldInfo",
        Field(
            default_factory=datetime.now,
            description="Analysis start time",
        ),
    )


# =============================================================================
# SCORE FIELDS - Quality scores with validation
# =============================================================================


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


def overall_score_field() -> FieldInfo:
    """Overall quality score field."""
    return quality_score_field("Overall quality score")


def coverage_score_field() -> FieldInfo:
    """Test coverage score field."""
    return quality_score_field("Test coverage score")


def security_score_field() -> FieldInfo:
    """Security analysis score field."""
    return quality_score_field("Security analysis score")


def maintainability_score_field() -> FieldInfo:
    """Maintainability score field."""
    return quality_score_field("Maintainability score")


def complexity_score_field() -> FieldInfo:
    """Complexity score field."""
    return quality_score_field("Complexity score")


# =============================================================================
# PATH FIELDS - File and directory paths
# =============================================================================


def file_path_field(description: str = "File path") -> FieldInfo:
    """Standard file path field."""
    return cast("FieldInfo", Field(..., description=description))


def optional_file_path_field(description: str = "Optional file path") -> FieldInfo:
    """Optional file path field."""
    return cast("FieldInfo", Field(None, description=description))


def project_path_field() -> FieldInfo:
    """Project path field for analysis."""
    return cast("FieldInfo", Field(..., description="Project path for analysis"))


# =============================================================================
# CONTENT FIELDS - Text and message fields
# =============================================================================


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


def project_name_field() -> FieldInfo:
    """Project name field."""
    return name_field(255, "Project name")


def optional_description_field() -> FieldInfo:
    """Optional description field."""
    return cast("FieldInfo", Field(None, description="Description"))


def message_field(description: str = "Message") -> FieldInfo:
    """Standard message field."""
    return cast("FieldInfo", Field(..., description=description))


def issue_message_field() -> FieldInfo:
    """Issue description message field."""
    return message_field("Issue description message")


def optional_error_message_field() -> FieldInfo:
    """Optional error message field."""
    return cast(
        "FieldInfo", Field(None, description="Error message if operation failed")
    )


def content_field(description: str = "Content") -> FieldInfo:
    """Standard content field."""
    return cast("FieldInfo", Field(..., description=description))


def report_content_field() -> FieldInfo:
    """Report content field."""
    return content_field("Report content")


# =============================================================================
# NUMERIC FIELDS - Numbers with validation
# =============================================================================


def line_number_field() -> FieldInfo:
    """Line number field (must be positive)."""
    return cast("FieldInfo", Field(..., ge=1, description="Line number"))


def optional_column_number_field() -> FieldInfo:
    """Optional column number field (must be positive)."""
    return cast("FieldInfo", Field(None, ge=1, description="Column number"))


def max_complexity_field(default: int = 10) -> FieldInfo:
    """Maximum complexity threshold field."""
    return cast(
        "FieldInfo",
        Field(default, ge=1, le=50, description="Maximum allowed complexity"),
    )


def percentage_field(
    default: float = 0.0, description: str = "Percentage value"
) -> FieldInfo:
    """Percentage field (0-100)."""
    return cast("FieldInfo", Field(default, ge=0.0, le=100.0, description=description))


def min_coverage_field(default: float = 90.0) -> FieldInfo:
    """Minimum coverage threshold field."""
    return percentage_field(default, "Minimum coverage threshold")


def security_threshold_field(default: float = 90.0) -> FieldInfo:
    """Security score threshold field."""
    return percentage_field(default, "Security score threshold")


# =============================================================================
# COLLECTION FIELDS - Lists and dictionaries
# =============================================================================


def string_list_field(description: str = "List of strings") -> FieldInfo:
    """Standard list of strings field."""
    return cast("FieldInfo", Field(default_factory=list, description=description))


def include_patterns_field() -> FieldInfo:
    """File patterns to include field."""
    return string_list_field("File patterns to include")


def exclude_patterns_field() -> FieldInfo:
    """File patterns to exclude field."""
    return string_list_field("File patterns to exclude")


def metadata_field() -> FieldInfo:
    """Standard metadata dictionary field."""
    return cast(
        "FieldInfo",
        Field(
            default_factory=dict,
            description="Additional metadata",
        ),
    )


def report_metadata_field() -> FieldInfo:
    """Report metadata field."""
    return cast(
        "FieldInfo",
        Field(
            default_factory=dict,
            description="Additional report metadata",
        ),
    )


# =============================================================================
# BOOLEAN FIELDS - Feature flags and toggles
# =============================================================================


def feature_flag_field(
    *, default: bool = True, description: str = "Feature flag"
) -> FieldInfo:
    """Standard feature flag field."""
    return cast("FieldInfo", Field(default, description=description))


def enable_security_field() -> FieldInfo:
    """Enable security analysis flag."""
    return feature_flag_field(default=True, description="Enable security analysis")


def enable_complexity_field() -> FieldInfo:
    """Enable complexity analysis flag."""
    return feature_flag_field(default=True, description="Enable complexity analysis")


def enable_coverage_field() -> FieldInfo:
    """Enable coverage analysis flag."""
    return feature_flag_field(default=True, description="Enable coverage analysis")


# =============================================================================
# ENUMERATION FIELDS - Status and type fields
# =============================================================================


def status_field(description: str = "Status") -> FieldInfo:
    """Standard status field."""
    return cast("FieldInfo", Field(..., description=description))


def analysis_status_field() -> FieldInfo:
    """Analysis status field."""
    return status_field("Analysis status")


def severity_field() -> FieldInfo:
    """Issue severity field."""
    return cast("FieldInfo", Field(..., description="Issue severity level"))


def issue_type_field() -> FieldInfo:
    """Issue type field."""
    return cast("FieldInfo", Field(..., description="Type of quality issue"))


def format_type_field() -> FieldInfo:
    """Report format type field."""
    return cast("FieldInfo", Field(..., description="Report format (HTML, JSON, PDF)"))


def rule_field() -> FieldInfo:
    """Optional rule field."""
    return cast("FieldInfo", Field(None, description="Rule that triggered this issue"))


def source_field() -> FieldInfo:
    """Analysis source field."""
    return cast(
        "FieldInfo", Field(..., description="Analysis backend that detected the issue")
    )


# Export all field functions
__all__ = [
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
