"""Base models for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebModels as _WebModels, m, t


class FlextQualityModelsBase:
    """Base models for flext-quality."""

    class ConfigNamespace(m.BaseModel):
        """Open, frozen namespace exposing every ``config/*.yaml`` domain."""

        model_config = m.ConfigDict(extra="allow", frozen=True)

    class QualityThresholdsConfig(_WebModels.ManagedModel):
        """Configuration for quality threshold limits."""

        max_age_days: int = _WebModels.Field(
            description=(
                "Maximum age in days before a documentation file is flagged as stale."
            ),
        )
        min_word_count: int = _WebModels.Field(
            description=(
                "Minimum number of words a documentation file must contain to pass."
            ),
        )
        max_broken_links: int = _WebModels.Field(
            description=(
                "Maximum number of broken links tolerated before a file fails the "
                "audit."
            ),
        )
        min_completeness_score: float = _WebModels.Field(
            description=(
                "Minimum acceptable completeness score, from 0.0 to 1.0, for a "
                "document."
            ),
        )
        max_file_size_mb: int = _WebModels.Field(
            description=(
                "Maximum documentation file size, in megabytes, before it is flagged."
            ),
        )

    class ContentChecksConfig(_WebModels.ManagedModel):
        """Configuration for content validation checks."""

        check_freshness: bool = _WebModels.Field(
            description="Whether to check that documentation content is not stale.",
        )
        check_completeness: bool = _WebModels.Field(
            description=(
                "Whether to check that documentation content meets completeness "
                "requirements."
            ),
        )
        check_consistency: bool = _WebModels.Field(
            description=(
                "Whether to check documentation content for internal consistency."
            ),
        )
        check_links: bool = _WebModels.Field(
            description=(
                "Whether to check documentation content for broken or invalid links."
            ),
        )
        check_structure: bool = _WebModels.Field(
            description=(
                "Whether to check documentation content for correct structural "
                "organization."
            ),
        )
        check_accessibility: bool = _WebModels.Field(
            description=(
                "Whether to check documentation content against accessibility "
                "requirements."
            ),
        )

    class SeverityLevelsConfig(_WebModels.ManagedModel):
        """Configuration for severity level categorization."""

        critical: t.StrSequence = _WebModels.Field(
            description="Issue type identifiers classified as critical severity.",
        )
        high: t.StrSequence = _WebModels.Field(
            description="Issue type identifiers classified as high severity.",
        )
        medium: t.StrSequence = _WebModels.Field(
            description="Issue type identifiers classified as medium severity.",
        )
        low: t.StrSequence = _WebModels.Field(
            description="Issue type identifiers classified as low severity.",
        )

    class MarkdownStyleConfig(_WebModels.ManagedModel):
        """Configuration for Markdown style preferences."""

        heading_style: str = _WebModels.Field(
            description=(
                "Preferred Markdown heading style (e.g. ATX '#' or Setext underline)."
            ),
        )
        list_style: str = _WebModels.Field(
            description=(
                "Preferred Markdown list marker style (e.g. '-', '*', or '+')."
            ),
        )
        emphasis_style: str = _WebModels.Field(
            description=(
                "Preferred Markdown emphasis marker style (e.g. asterisk or "
                "underscore)."
            ),
        )
        code_block_style: str = _WebModels.Field(
            description=(
                "Preferred Markdown code block style (e.g. fenced or indented)."
            ),
        )
        link_style: str = _WebModels.Field(
            description=(
                "Preferred Markdown link style (e.g. inline or reference-style)."
            ),
        )

    class AccessibilityConfig(_WebModels.ManagedModel):
        """Configuration for accessibility requirements."""

        require_alt_text: bool = _WebModels.Field(
            description="Whether every image must carry descriptive alt text.",
        )
        descriptive_link_text: bool = _WebModels.Field(
            description=(
                "Whether link text must be descriptive rather than generic (e.g. "
                "not 'click here')."
            ),
        )
        proper_heading_hierarchy: bool = _WebModels.Field(
            description=(
                "Whether heading levels must form a proper, non-skipping hierarchy."
            ),
        )
        min_alt_text_length: int = _WebModels.Field(
            description="Minimum character length required for image alt text.",
        )
        max_alt_text_length: int = _WebModels.Field(
            description="Maximum character length allowed for image alt text.",
        )
        check_color_contrast: bool = _WebModels.Field(
            description=(
                "Whether to check that documented color combinations meet "
                "contrast requirements."
            ),
        )
        minimum_contrast_ratio: float = _WebModels.Field(
            description=(
                "Minimum acceptable color contrast ratio for documented color "
                "combinations."
            ),
        )

    class FormattingConfig(_WebModels.ManagedModel):
        """Configuration for formatting standards."""

        max_line_length: int = _WebModels.Field(
            description=(
                "Maximum allowed line length, in characters, before a hard violation."
            ),
        )
        soft_line_limit: int = _WebModels.Field(
            description=(
                "Preferred line length, in characters, used as a soft warning "
                "threshold below the hard maximum."
            ),
        )
        consistent_indentation: bool = _WebModels.Field(
            description=(
                "Whether indentation must be consistent throughout the document."
            ),
        )
        trailing_spaces: bool = _WebModels.Field(
            description=("Whether trailing whitespace at the end of lines is flagged."),
        )
        trailing_newlines: bool = _WebModels.Field(
            description=(
                "Whether trailing blank lines at the end of the file are flagged."
            ),
        )
        indentation_type: str = _WebModels.Field(
            description=(
                "Preferred indentation character type (e.g. 'spaces' or 'tabs')."
            ),
        )
        indentation_size: int = _WebModels.Field(
            description=(
                "Preferred number of indentation characters per nesting level."
            ),
        )
        blank_lines_before_headings: bool = _WebModels.Field(
            description=(
                "Whether a blank line is required immediately before a heading."
            ),
        )
        blank_lines_after_headings: bool = _WebModels.Field(
            description=(
                "Whether a blank line is required immediately after a heading."
            ),
        )
        blank_lines_around_lists: bool = _WebModels.Field(
            description="Whether blank lines are required around list blocks.",
        )
        blank_lines_around_code_blocks: bool = _WebModels.Field(
            description=("Whether blank lines are required around fenced code blocks."),
        )

    class HeadingsConfig(_WebModels.ManagedModel):
        """Documentation heading hierarchy policy."""

        enforce_hierarchy: bool = _WebModels.Field(
            description=(
                "Whether heading levels must strictly follow hierarchical order "
                "without skipping."
            ),
        )
        max_heading_level: int = _WebModels.Field(
            description=(
                "Deepest heading level (e.g. 6 for H6) permitted in a document."
            ),
        )
        require_space_after_hash: bool = _WebModels.Field(
            description=(
                "Whether ATX heading markers ('#') must be followed by a space."
            ),
        )
        allow_closing_hashes: bool = _WebModels.Field(
            description=(
                "Whether trailing '#' closing markers on ATX headings are permitted."
            ),
        )
        first_heading_level: int = _WebModels.Field(
            description="Heading level a document must start with (e.g. 1 for H1).",
        )
        toc_heading_level: int = _WebModels.Field(
            description=(
                "Deepest heading level included when generating a table of contents."
            ),
        )

    class CodeStyleConfig(_WebModels.ManagedModel):
        """Documentation code block policy."""

        require_language_specifier: bool = _WebModels.Field(
            description=(
                "Whether fenced code blocks must declare a language specifier."
            ),
        )
        preferred_languages: t.StrSequence = _WebModels.Field(
            description="Language specifiers accepted for fenced code blocks.",
        )
        inline_code_style: str = _WebModels.Field(
            description=(
                "Preferred style for inline code spans (e.g. backtick delimiting)."
            ),
        )
        consistent_fencing: bool = _WebModels.Field(
            description=(
                "Whether fenced code blocks must use a consistent fence character "
                "throughout."
            ),
        )
        fence_style: str = _WebModels.Field(
            description=(
                "Preferred fence character for code blocks (e.g. backtick or tilde)."
            ),
        )

    class GithubLinkConfig(_WebModels.ManagedModel):
        """GitHub link checks declared in validation YAML."""

        validate_existence: bool = _WebModels.Field(
            description=(
                "Whether to verify that linked GitHub resources (repos, issues, "
                "files) actually exist."
            ),
        )
        check_rate_limits: bool = _WebModels.Field(
            description=(
                "Whether to respect and check GitHub API rate limits while "
                "validating links."
            ),
        )

    class DocumentationLinkConfig(_WebModels.ManagedModel):
        """Documentation link checks declared in validation YAML."""

        validate_structure: bool = _WebModels.Field(
            description=(
                "Whether to verify that internal documentation links point to a "
                "valid document structure."
            ),
        )
        check_anchors: bool = _WebModels.Field(
            description=(
                "Whether to verify that heading anchors referenced by internal "
                "links actually exist."
            ),
        )

    class LinkValidationConfig(_WebModels.ManagedModel):
        """Configuration for link validation settings."""

        timeout: int = _WebModels.Field(
            description=(
                "Timeout, in seconds, allowed for a single link check request."
            ),
        )
        user_agent: str = _WebModels.Field(
            description=(
                "User-Agent header string sent with outbound link check requests."
            ),
        )
        check_external: bool = _WebModels.Field(
            description=(
                "Whether to validate links pointing outside the documentation "
                "repository."
            ),
        )
        check_internal: bool = _WebModels.Field(
            description=(
                "Whether to validate links pointing to other files within the "
                "documentation repository."
            ),
        )
        check_images: bool = _WebModels.Field(
            description="Whether to validate image references as links.",
        )
        follow_redirects: bool = _WebModels.Field(
            description="Whether to follow HTTP redirects when validating a link.",
        )
        max_redirects: int = _WebModels.Field(
            description=(
                "Maximum number of HTTP redirects to follow before treating a "
                "link as broken."
            ),
        )
        acceptable_status_codes: t.SequenceOf[int] = _WebModels.Field(
            description=(
                "HTTP status codes treated as a successful link check response."
            ),
        )
        validate_content_type: bool = _WebModels.Field(
            description=(
                "Whether to verify the response Content-Type header of a checked link."
            ),
        )
        expected_content_types: t.StrSequence = _WebModels.Field(
            description=(
                "Content-Type values accepted when validate_content_type is enabled."
            ),
        )
        allowed_domains: t.StrSequence = _WebModels.Field(
            description=(
                "Domains explicitly permitted for external links; empty means no "
                "allowlist restriction."
            ),
        )
        blocked_domains: t.StrSequence = _WebModels.Field(
            description="Domains explicitly forbidden for external links.",
        )
        github_links: FlextQualityModelsBase.GithubLinkConfig = _WebModels.Field(
            description=(
                "Validation settings specific to links pointing at GitHub resources."
            ),
        )
        documentation_links: FlextQualityModelsBase.DocumentationLinkConfig = (
            _WebModels.Field(
                description=(
                    "Validation settings specific to internal documentation links."
                ),
            )
        )

    class ValidationRunConfig(_WebModels.ManagedModel):
        """Execution limits for validation operations."""

        enabled: bool = _WebModels.Field(
            description="Whether the validation run is enabled.",
        )
        fail_on_errors: bool = _WebModels.Field(
            description=(
                "Whether the validation run should exit with failure when errors "
                "are found."
            ),
        )
        verbose_output: bool = _WebModels.Field(
            description=(
                "Whether the validation run should emit verbose diagnostic output."
            ),
        )
        save_results: bool = _WebModels.Field(
            description="Whether validation results should be persisted to disk.",
        )
        max_concurrent_requests: t.PositiveInt = _WebModels.Field(
            description=(
                "Maximum number of concurrent requests the validation run may issue."
            ),
        )
        request_timeout: t.PositiveInt = _WebModels.Field(
            description=(
                "Timeout, in seconds, applied to each individual validation request."
            ),
        )
        requests_per_second: t.PositiveInt = _WebModels.Field(
            description=(
                "Maximum sustained rate of requests, per second, the validation "
                "run may issue."
            ),
        )
        burst_limit: t.PositiveInt = _WebModels.Field(
            description=(
                "Maximum number of requests permitted in a short burst above the "
                "sustained rate."
            ),
        )

    class ContentAnalysisConfig(_WebModels.ManagedModel):
        """Configuration for content analysis parameters."""

        check_structure: bool = _WebModels.Field(
            description=(
                "Whether to analyze document structure (sections, headings) "
                "during content analysis."
            ),
        )
        min_section_depth: int = _WebModels.Field(
            description=(
                "Minimum number of nested section levels a document must contain."
            ),
        )
        required_sections: t.StrSequence = _WebModels.Field(
            description=(
                "Section headings that must be present in every analyzed document."
            ),
        )
        min_word_count: int = _WebModels.Field(
            description=(
                "Minimum number of words required for a document to pass content "
                "analysis."
            ),
        )
        check_readability: bool = _WebModels.Field(
            description=(
                "Whether to compute and check a document's readability score."
            ),
        )
        readability_target_score: int = _WebModels.Field(
            description=("Target readability score a document should meet or exceed."),
        )
        check_todos: bool = _WebModels.Field(
            description=(
                "Whether to flag unresolved TODO markers found in document content."
            ),
        )
        check_fixmes: bool = _WebModels.Field(
            description=(
                "Whether to flag unresolved FIXME markers found in document content."
            ),
        )

    class AuditRulesConfig(_WebModels.FlexibleInternalModel):
        """Configuration for audit rules and thresholds."""

        quality_thresholds: FlextQualityModelsBase.QualityThresholdsConfig = (
            _WebModels.Field(
                description=(
                    "Threshold limits applied when auditing documentation quality."
                ),
            )
        )
        content_checks: FlextQualityModelsBase.ContentChecksConfig = _WebModels.Field(
            description=(
                "Toggles controlling which content checks are performed during "
                "the audit."
            ),
        )
        severity_levels: FlextQualityModelsBase.SeverityLevelsConfig = _WebModels.Field(
            description=(
                "Mapping of issue type identifiers to severity level categorization."
            ),
        )

    class StyleGuideConfig(_WebModels.FlexibleInternalModel):
        """Configuration for style guide rules."""

        markdown: FlextQualityModelsBase.MarkdownStyleConfig = _WebModels.Field(
            description="Preferred Markdown style conventions."
        )
        accessibility: FlextQualityModelsBase.AccessibilityConfig = _WebModels.Field(
            description=("Accessibility requirements applied by the style guide."),
        )
        formatting: FlextQualityModelsBase.FormattingConfig = _WebModels.Field(
            description="Formatting standards applied by the style guide.",
        )
        headings: FlextQualityModelsBase.HeadingsConfig = _WebModels.Field(
            description="Heading hierarchy policy applied by the style guide.",
        )
        code: FlextQualityModelsBase.CodeStyleConfig = _WebModels.Field(
            description="Code block style policy applied by the style guide.",
        )

    class ValidationConfig(_WebModels.FlexibleInternalModel):
        """Configuration for validation settings."""

        validation: FlextQualityModelsBase.ValidationRunConfig = _WebModels.Field(
            description="Execution limits applied to validation runs.",
        )
        link_validation: FlextQualityModelsBase.LinkValidationConfig = _WebModels.Field(
            description="Settings controlling how links are validated.",
        )
        content_analysis: FlextQualityModelsBase.ContentAnalysisConfig = (
            _WebModels.Field(
                description=("Settings controlling how document content is analyzed."),
            )
        )


__all__: list[str] = ["FlextQualityModelsBase"]
