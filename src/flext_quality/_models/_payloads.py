"""Canonical quality payload models for flext-quality.

Declaration-only payload defaults reused by the composed models in
``flext_quality.models`` — the single public owner of the Quality model
surface. Split out of ``models.py`` to honor the per-module LOC SUPREME
LAW; ownership and public re-export remain on the ``models`` facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import FlextWebModels as _WebModels

from flext_quality import FlextQualityTypes as t


class _GithubLinkConfig(_WebModels.ManagedModel):
    """GitHub link checks declared in validation YAML."""

    validate_existence: bool = _WebModels.Field(
        default=True,
        description="Whether to verify that linked GitHub resources (repos, issues, files) actually exist.",
    )
    check_rate_limits: bool = _WebModels.Field(
        default=False,
        description="Whether to respect and check GitHub API rate limits while validating links.",
    )


class _DocumentationLinkConfig(_WebModels.ManagedModel):
    """Documentation link checks declared in validation YAML."""

    validate_structure: bool = _WebModels.Field(
        default=False,
        description="Whether to verify that internal documentation links point to a valid document structure.",
    )
    check_anchors: bool = _WebModels.Field(
        default=False,
        description="Whether to verify that heading anchors referenced by internal links actually exist.",
    )


class FlextQualityModelDefaults:
    """Canonical quality payload defaults reused by composed models."""

    class AuditMetrics(_WebModels.ManagedModel):
        """Typed metrics for documentation audit results."""

        total_issues: int = _WebModels.Field(
            default=0,
            description="Total number of documentation issues found by the audit.",
        )
        severity_breakdown: t.MutableIntMapping = _WebModels.Field(
            default_factory=dict,
            description="Count of issues found for each severity level (e.g. critical, high, medium, low).",
        )
        quality_score: int = _WebModels.Field(
            default=0,
            description="Overall documentation quality score from 0 to 100, higher is better.",
        )
        files_analyzed: int = _WebModels.Field(
            default=0, description="Number of documentation files the audit inspected."
        )
        issues_per_file: float = _WebModels.Field(
            default=0.0, description="Average number of issues found per analyzed file."
        )

    class QualityThresholdsConfig(_WebModels.ManagedModel):
        """Configuration for quality threshold limits."""

        max_age_days: int = _WebModels.Field(
            default=90,
            description="Maximum age in days before a documentation file is flagged as stale.",
        )
        min_word_count: int = _WebModels.Field(
            default=100,
            description="Minimum number of words a documentation file must contain to pass.",
        )
        max_broken_links: int = _WebModels.Field(
            default=0,
            description="Maximum number of broken links tolerated before a file fails the audit.",
        )
        min_completeness_score: float = _WebModels.Field(
            default=0.8,
            description="Minimum acceptable completeness score, from 0.0 to 1.0, for a document.",
        )
        max_file_size_mb: int = _WebModels.Field(
            default=10,
            description="Maximum documentation file size, in megabytes, before it is flagged.",
        )

    class ContentChecksConfig(_WebModels.ManagedModel):
        """Configuration for content validation checks."""

        check_freshness: bool = _WebModels.Field(
            default=True,
            description="Whether to check that documentation content is not stale.",
        )
        check_completeness: bool = _WebModels.Field(
            default=True,
            description="Whether to check that documentation content meets completeness requirements.",
        )
        check_consistency: bool = _WebModels.Field(
            default=True,
            description="Whether to check documentation content for internal consistency.",
        )
        check_links: bool = _WebModels.Field(
            default=True,
            description="Whether to check documentation content for broken or invalid links.",
        )
        check_structure: bool = _WebModels.Field(
            default=True,
            description="Whether to check documentation content for correct structural organization.",
        )
        check_accessibility: bool = _WebModels.Field(
            default=True,
            description="Whether to check documentation content against accessibility requirements.",
        )

    class SeverityLevelsConfig(_WebModels.ManagedModel):
        """Configuration for severity level categorization."""

        critical: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Issue type identifiers classified as critical severity.",
        )
        high: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Issue type identifiers classified as high severity.",
        )
        medium: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Issue type identifiers classified as medium severity.",
        )
        low: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Issue type identifiers classified as low severity.",
        )

    class MarkdownStyleConfig(_WebModels.ManagedModel):
        """Configuration for Markdown style preferences."""

        heading_style: str = _WebModels.Field(
            default="atx",
            description="Preferred Markdown heading style (e.g. ATX '#' or Setext underline).",
        )
        list_style: str = _WebModels.Field(
            default="dash",
            description="Preferred Markdown list marker style (e.g. '-', '*', or '+').",
        )
        emphasis_style: str = _WebModels.Field(
            default="*",
            description="Preferred Markdown emphasis marker style (e.g. asterisk or underscore).",
        )
        code_block_style: str = _WebModels.Field(
            default="fenced",
            description="Preferred Markdown code block style (e.g. fenced or indented).",
        )
        link_style: str = _WebModels.Field(
            default="inline",
            description="Preferred Markdown link style (e.g. inline or reference-style).",
        )

    class AccessibilityConfig(_WebModels.ManagedModel):
        """Configuration for accessibility requirements."""

        require_alt_text: bool = _WebModels.Field(
            default=True,
            description="Whether every image must carry descriptive alt text.",
        )
        descriptive_link_text: bool = _WebModels.Field(
            default=True,
            description="Whether link text must be descriptive rather than generic (e.g. not 'click here').",
        )
        proper_heading_hierarchy: bool = _WebModels.Field(
            default=True,
            description="Whether heading levels must form a proper, non-skipping hierarchy.",
        )
        min_alt_text_length: int = _WebModels.Field(
            default=5,
            description="Minimum character length required for image alt text.",
        )
        max_alt_text_length: int = _WebModels.Field(
            default=100,
            description="Maximum character length allowed for image alt text.",
        )
        check_color_contrast: bool = _WebModels.Field(
            default=False,
            description="Whether to check that documented color combinations meet contrast requirements.",
        )
        minimum_contrast_ratio: float = _WebModels.Field(
            default=4.5,
            description="Minimum acceptable color contrast ratio for documented color combinations.",
        )

    class FormattingConfig(_WebModels.ManagedModel):
        """Configuration for formatting standards."""

        max_line_length: int = _WebModels.Field(
            default=88,
            description="Maximum allowed line length, in characters, before a hard violation.",
        )
        soft_line_limit: int = _WebModels.Field(
            default=80,
            description="Preferred line length, in characters, used as a soft warning threshold below the hard maximum.",
        )
        consistent_indentation: bool = _WebModels.Field(
            default=True,
            description="Whether indentation must be consistent throughout the document.",
        )
        trailing_spaces: bool = _WebModels.Field(
            default=False,
            description="Whether trailing whitespace at the end of lines is flagged.",
        )
        trailing_newlines: bool = _WebModels.Field(
            default=True,
            description="Whether trailing blank lines at the end of the file are flagged.",
        )
        indentation_type: str = _WebModels.Field(
            default="spaces",
            description="Preferred indentation character type (e.g. 'spaces' or 'tabs').",
        )
        indentation_size: int = _WebModels.Field(
            default=4,
            description="Preferred number of indentation characters per nesting level.",
        )
        blank_lines_before_headings: bool = _WebModels.Field(
            default=True,
            description="Whether a blank line is required immediately before a heading.",
        )
        blank_lines_after_headings: bool = _WebModels.Field(
            default=False,
            description="Whether a blank line is required immediately after a heading.",
        )
        blank_lines_around_lists: bool = _WebModels.Field(
            default=True,
            description="Whether blank lines are required around list blocks.",
        )
        blank_lines_around_code_blocks: bool = _WebModels.Field(
            default=True,
            description="Whether blank lines are required around fenced code blocks.",
        )

    class HeadingsConfig(_WebModels.ManagedModel):
        """Documentation heading hierarchy policy."""

        enforce_hierarchy: bool = _WebModels.Field(
            default=True,
            description="Whether heading levels must strictly follow hierarchical order without skipping.",
        )
        max_heading_level: int = _WebModels.Field(
            default=4,
            description="Deepest heading level (e.g. 6 for H6) permitted in a document.",
        )
        require_space_after_hash: bool = _WebModels.Field(
            default=True,
            description="Whether ATX heading markers ('#') must be followed by a space.",
        )
        allow_closing_hashes: bool = _WebModels.Field(
            default=False,
            description="Whether trailing '#' closing markers on ATX headings are permitted.",
        )
        first_heading_level: int = _WebModels.Field(
            default=1,
            description="Heading level a document must start with (e.g. 1 for H1).",
        )
        toc_heading_level: int = _WebModels.Field(
            default=2,
            description="Deepest heading level included when generating a table of contents.",
        )

    class CodeStyleConfig(_WebModels.ManagedModel):
        """Documentation code block policy."""

        require_language_specifier: bool = _WebModels.Field(
            default=False,
            description="Whether fenced code blocks must declare a language specifier.",
        )
        preferred_languages: t.StrSequence = _WebModels.Field(
            default_factory=lambda: (
                "python",
                "bash",
                "json",
                "yaml",
                "sql",
                "javascript",
                "html",
            ),
            description="Language specifiers accepted for fenced code blocks.",
        )
        inline_code_style: str = _WebModels.Field(
            default="backticks",
            description="Preferred style for inline code spans (e.g. backtick delimiting).",
        )
        consistent_fencing: bool = _WebModels.Field(
            default=True,
            description="Whether fenced code blocks must use a consistent fence character throughout.",
        )
        fence_style: str = _WebModels.Field(
            default="backticks",
            description="Preferred fence character for code blocks (e.g. backtick or tilde).",
        )

    GithubLinkConfig = _GithubLinkConfig
    DocumentationLinkConfig = _DocumentationLinkConfig

    class LinkValidationConfig(_WebModels.ManagedModel):
        """Configuration for link validation settings."""

        timeout: int = _WebModels.Field(
            default=10,
            description="Timeout, in seconds, allowed for a single link check request.",
        )
        user_agent: str = _WebModels.Field(
            default="FLEXT-Quality-Doc-Auditor/1.0",
            description="User-Agent header string sent with outbound link check requests.",
        )
        check_external: bool = _WebModels.Field(
            default=True,
            description="Whether to validate links pointing outside the documentation repository.",
        )
        check_internal: bool = _WebModels.Field(
            default=True,
            description="Whether to validate links pointing to other files within the documentation repository.",
        )
        check_images: bool = _WebModels.Field(
            default=True, description="Whether to validate image references as links."
        )
        follow_redirects: bool = _WebModels.Field(
            default=True,
            description="Whether to follow HTTP redirects when validating a link.",
        )
        max_redirects: int = _WebModels.Field(
            default=5,
            description="Maximum number of HTTP redirects to follow before treating a link as broken.",
        )
        acceptable_status_codes: t.SequenceOf[int] = _WebModels.Field(
            default_factory=lambda: (200, 201, 202, 206, 301, 302, 303, 307, 308),
            description="HTTP status codes treated as a successful link check response.",
        )
        validate_content_type: bool = _WebModels.Field(
            default=False,
            description="Whether to verify the response Content-Type header of a checked link.",
        )
        expected_content_types: t.StrSequence = _WebModels.Field(
            default_factory=lambda: ("text/html", "text/plain", "application/json"),
            description="Content-Type values accepted when validate_content_type is enabled.",
        )
        allowed_domains: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Domains explicitly permitted for external links; empty means no allowlist restriction.",
        )
        blocked_domains: t.StrSequence = _WebModels.Field(
            default_factory=tuple,
            description="Domains explicitly forbidden for external links.",
        )
        github_links: _GithubLinkConfig = _WebModels.Field(
            default_factory=_GithubLinkConfig,
            description="Validation settings specific to links pointing at GitHub resources.",
        )
        documentation_links: _DocumentationLinkConfig = _WebModels.Field(
            default_factory=_DocumentationLinkConfig,
            description="Validation settings specific to internal documentation links.",
        )

    class ValidationRunConfig(_WebModels.ManagedModel):
        """Execution limits for validation operations."""

        enabled: bool = _WebModels.Field(
            default=True, description="Whether the validation run is enabled."
        )
        fail_on_errors: bool = _WebModels.Field(
            default=False,
            description="Whether the validation run should exit with failure when errors are found.",
        )
        verbose_output: bool = _WebModels.Field(
            default=False,
            description="Whether the validation run should emit verbose diagnostic output.",
        )
        save_results: bool = _WebModels.Field(
            default=True,
            description="Whether validation results should be persisted to disk.",
        )
        max_concurrent_requests: t.PositiveInt = _WebModels.Field(
            default=5,
            description="Maximum number of concurrent requests the validation run may issue.",
        )
        request_timeout: t.PositiveInt = _WebModels.Field(
            default=10,
            description="Timeout, in seconds, applied to each individual validation request.",
        )
        requests_per_second: t.PositiveInt = _WebModels.Field(
            default=10,
            description="Maximum sustained rate of requests, per second, the validation run may issue.",
        )
        burst_limit: t.PositiveInt = _WebModels.Field(
            default=20,
            description="Maximum number of requests permitted in a short burst above the sustained rate.",
        )

    class ContentAnalysisConfig(_WebModels.ManagedModel):
        """Configuration for content analysis parameters."""

        check_structure: bool = _WebModels.Field(
            default=True,
            description="Whether to analyze document structure (sections, headings) during content analysis.",
        )
        min_section_depth: int = _WebModels.Field(
            default=2,
            description="Minimum number of nested section levels a document must contain.",
        )
        required_sections: t.StrSequence = _WebModels.Field(
            default_factory=lambda: ("Overview", "Installation", "Usage"),
            description="Section headings that must be present in every analyzed document.",
        )
        min_word_count: int = _WebModels.Field(
            default=100,
            description="Minimum number of words required for a document to pass content analysis.",
        )
        check_readability: bool = _WebModels.Field(
            default=False,
            description="Whether to compute and check a document's readability score.",
        )
        readability_target_score: int = _WebModels.Field(
            default=60,
            description="Target readability score a document should meet or exceed.",
        )
        check_todos: bool = _WebModels.Field(
            default=True,
            description="Whether to flag unresolved TODO markers found in document content.",
        )
        check_fixmes: bool = _WebModels.Field(
            default=True,
            description="Whether to flag unresolved FIXME markers found in document content.",
        )
