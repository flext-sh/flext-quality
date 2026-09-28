"""Canonical quality payloads reused by composed model defaults."""

from __future__ import annotations

from flext_infra import FlextInfraModels as m, FlextInfraUtilities as u

from flext_quality import t


class FlextQualityModelDefaults:
    """Quality payload classes reused directly by composed models."""

    class AuditMetrics(m.BaseModel):
        """Typed metrics for documentation audit results."""

        total_issues: int = 0
        severity_breakdown: t.MutableIntMapping = u.Field(default_factory=dict)
        quality_score: int = 0
        files_analyzed: int = 0
        issues_per_file: float = 0.0

    class QualityThresholdsConfig(m.BaseModel):
        """Configuration for quality threshold limits."""

        max_age_days: int = 90
        min_word_count: int = 100
        max_broken_links: int = 0
        min_completeness_score: float = 0.8
        max_file_size_mb: int = 10

    class ContentChecksConfig(m.BaseModel):
        """Configuration for content validation checks."""

        check_freshness: bool = True
        check_completeness: bool = True
        check_consistency: bool = True
        check_links: bool = True
        check_structure: bool = True
        check_accessibility: bool = True

    class SeverityLevelsConfig(m.BaseModel):
        """Configuration for severity level categorization."""

        critical: t.StrSequence = u.Field(default_factory=list)
        high: t.StrSequence = u.Field(default_factory=list)
        medium: t.StrSequence = u.Field(default_factory=list)
        low: t.StrSequence = u.Field(default_factory=list)

    class MarkdownStyleConfig(m.BaseModel):
        """Configuration for Markdown style preferences."""

        heading_style: str = "atx"
        list_style: str = "dash"
        emphasis_style: str = "*"
        code_block_style: str = "fenced"
        link_style: str = "inline"

    class AccessibilityConfig(m.BaseModel):
        """Configuration for accessibility requirements."""

        require_alt_text: bool = True
        descriptive_links: bool = True
        heading_structure: bool = True
        descriptive_link_text: bool = True
        proper_heading_hierarchy: bool = True
        min_alt_text_length: int = 5
        max_alt_text_length: int = 100
        check_color_contrast: bool = False
        minimum_contrast_ratio: float = 4.5

    class FormattingConfig(m.BaseModel):
        """Configuration for formatting standards."""

        max_line_length: int = 88
        soft_line_limit: int = 80
        consistent_indentation: bool = True
        trailing_spaces: bool = False
        trailing_newlines: bool = True
        indentation_type: str = "spaces"
        indentation_size: int = 4
        blank_lines_before_headings: bool = True
        blank_lines_after_headings: bool = False
        blank_lines_around_lists: bool = True
        blank_lines_around_code_blocks: bool = True

    class LinkValidationConfig(m.BaseModel):
        """Configuration for link validation settings."""

        timeout: int = 10
        retry_attempts: int = 3
        user_agent: str = "FLEXT-Quality-Doc-Auditor/1.0"
        check_external: bool = True
        check_internal: bool = True
        check_images: bool = True
        follow_redirects: bool = True
        max_redirects: int = 5
        acceptable_status_codes: t.SequenceOf[int] = u.Field(
            default_factory=lambda: [200, 201, 202, 206, 301, 302, 303, 307, 308]
        )
        validate_content_type: bool = False
        expected_content_types: t.StrSequence = u.Field(
            default_factory=lambda: ["text/html", "text/plain", "application/json"]
        )
        allowed_domains: t.StrSequence = u.Field(default_factory=list)
        blocked_domains: t.StrSequence = u.Field(default_factory=list)

    class ContentAnalysisConfig(m.BaseModel):
        """Configuration for content analysis parameters."""

        min_section_depth: int = 2
        required_sections: t.StrSequence = u.Field(
            default_factory=lambda: ["Overview", "Installation", "Usage"]
        )
        min_word_count: int = 100
        check_readability: bool = False
        readability_target_score: int = 60
        check_todos: bool = True
        check_fixmes: bool = True


__all__ = ["FlextQualityModelDefaults"]
