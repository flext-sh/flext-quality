# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_quality/_protocols/base
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_web import FlextWebProtocols

if TYPE_CHECKING:
    from flext_quality import t


class FlextQualityProtocolsBase:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class QualityThresholdsConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        max_age_days: int
        min_word_count: int
        max_broken_links: int
        min_completeness_score: float
        max_file_size_mb: int

    @runtime_checkable
    class ContentChecksConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        check_freshness: bool
        check_completeness: bool
        check_consistency: bool
        check_links: bool
        check_structure: bool
        check_accessibility: bool

    @runtime_checkable
    class SeverityLevelsConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        critical: Sequence[str]
        high: Sequence[str]
        medium: Sequence[str]
        low: Sequence[str]

    @runtime_checkable
    class MarkdownStyleConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        heading_style: str
        list_style: str
        emphasis_style: str
        code_block_style: str
        link_style: str

    @runtime_checkable
    class AccessibilityConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        require_alt_text: bool
        descriptive_link_text: bool
        proper_heading_hierarchy: bool
        min_alt_text_length: int
        max_alt_text_length: int
        check_color_contrast: bool
        minimum_contrast_ratio: float

    @runtime_checkable
    class FormattingConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        max_line_length: int
        soft_line_limit: int
        consistent_indentation: bool
        trailing_spaces: bool
        trailing_newlines: bool
        indentation_type: str
        indentation_size: int
        blank_lines_before_headings: bool
        blank_lines_after_headings: bool
        blank_lines_around_lists: bool
        blank_lines_around_code_blocks: bool

    @runtime_checkable
    class HeadingsConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        enforce_hierarchy: bool
        max_heading_level: int
        require_space_after_hash: bool
        allow_closing_hashes: bool
        first_heading_level: int
        toc_heading_level: int

    @runtime_checkable
    class CodeStyleConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        require_language_specifier: bool
        preferred_languages: Sequence[str]
        inline_code_style: str
        consistent_fencing: bool
        fence_style: str

    @runtime_checkable
    class GithubLinkConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        validate_existence: bool
        check_rate_limits: bool

    @runtime_checkable
    class DocumentationLinkConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        validate_structure: bool
        check_anchors: bool

    @runtime_checkable
    class LinkValidationConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        timeout: int
        user_agent: str
        check_external: bool
        check_internal: bool
        check_images: bool
        follow_redirects: bool
        max_redirects: int
        acceptable_status_codes: Sequence[int]
        validate_content_type: bool
        expected_content_types: Sequence[str]
        allowed_domains: Sequence[str]
        blocked_domains: Sequence[str]

        @property
        def github_links(self) -> FlextQualityProtocolsBase.GithubLinkConfig:
            """Structural member projected from the owning model.

            Validation settings specific to links pointing at GitHub resources.
            """
            ...

        @property
        def documentation_links(
            self,
        ) -> FlextQualityProtocolsBase.DocumentationLinkConfig:
            """Validation settings specific to internal documentation links."""
            ...

    @runtime_checkable
    class ValidationRunConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        enabled: bool
        fail_on_errors: bool
        verbose_output: bool
        save_results: bool
        max_concurrent_requests: t.PositiveInt
        request_timeout: t.PositiveInt
        requests_per_second: t.PositiveInt
        burst_limit: t.PositiveInt

    @runtime_checkable
    class ContentAnalysisConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        check_structure: bool
        min_section_depth: int
        required_sections: Sequence[str]
        min_word_count: int
        check_readability: bool
        readability_target_score: int
        check_todos: bool
        check_fixmes: bool

    @runtime_checkable
    class AuditRulesConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def quality_thresholds(
            self,
        ) -> FlextQualityProtocolsBase.QualityThresholdsConfig:
            """Threshold limits applied when auditing documentation quality."""
            ...

        @property
        def content_checks(self) -> FlextQualityProtocolsBase.ContentChecksConfig:
            """Structural member projected from the owning model.

            Toggles controlling which content checks are performed during the audit.
            """
            ...

        @property
        def severity_levels(self) -> FlextQualityProtocolsBase.SeverityLevelsConfig:
            """Structural member projected from the owning model.

            Mapping of issue type identifiers to severity level categorization.
            """
            ...

    @runtime_checkable
    class StyleGuideConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def markdown(self) -> FlextQualityProtocolsBase.MarkdownStyleConfig:
            """Preferred Markdown style conventions."""
            ...

        @property
        def accessibility(self) -> FlextQualityProtocolsBase.AccessibilityConfig:
            """Accessibility requirements applied by the style guide."""
            ...

        @property
        def formatting(self) -> FlextQualityProtocolsBase.FormattingConfig:
            """Formatting standards applied by the style guide."""
            ...

        @property
        def headings(self) -> FlextQualityProtocolsBase.HeadingsConfig:
            """Heading hierarchy policy applied by the style guide."""
            ...

        @property
        def code(self) -> FlextQualityProtocolsBase.CodeStyleConfig:
            """Code block style policy applied by the style guide."""
            ...

    @runtime_checkable
    class ValidationConfig(FlextWebProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def validation(self) -> FlextQualityProtocolsBase.ValidationRunConfig:
            """Execution limits applied to validation runs."""
            ...

        @property
        def link_validation(self) -> FlextQualityProtocolsBase.LinkValidationConfig:
            """Settings controlling how links are validated."""
            ...

        @property
        def content_analysis(self) -> FlextQualityProtocolsBase.ContentAnalysisConfig:
            """Settings controlling how document content is analyzed."""
            ...


__all__: list[str] = [
    "FlextQualityProtocolsBase",
]
