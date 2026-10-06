"""Scalar constants for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Final

from flext_web import c

if TYPE_CHECKING:
    from flext_quality import t


class FlextQualityConstantsValues:
    """Scalar constants mixed into ``c.Quality`` and ``c.Quality.LinkCheckerDemo``."""

    class Quality:
        """Quality scalar constants."""

        DEFAULT_CONFIG: Final[str] = str(
            Path(__file__).resolve().parent.parent
            / "docs"
            / "settings"
            / "schedule_config.yaml",
        )

        THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW: Final[int] = 10
        "Maximum broken links to show."

        THRESHOLD_MAX_CRITICAL_ISSUES_TO_SHOW: Final[int] = 5
        "Maximum critical issues to show in a notification."

        # ===== Quality Thresholds =====
        THRESHOLD_MIN_HEADINGS_FOR_TOC: Final[int] = 5
        "Minimum headings for table of contents."

        HOOK_TIMEOUT_MS: Final[int] = 5000
        MCP_TIMEOUT_MS: Final[int] = 30000
        INTEGRATION_TIMEOUT_MS: Final[int] = 10000
        RULE_TIMEOUT_SECONDS: Final[int] = c.DEFAULT_TIMEOUT_SECONDS
        BATCH_SIZE: Final[int] = 100
        DEFAULT_SEARCH_LIMIT: Final[int] = 20
        DEFAULT_MEMORY_SEARCH_LIMIT: Final[int] = 10
        DEFAULT_TIMELINE_DEPTH: Final[int] = 5
        JSON_INDENT: Final[int] = 2
        MS_TO_SECONDS_DIVISOR: Final[int] = 1000

        # ===== MCP Configuration =====
        MCP_SERVER_NAME: Final[str] = "flext-quality"
        "MCP server name."
        MCP_SERVER_VERSION: Final[str] = "1.0.0"
        "MCP server version."
        MCP_DEFAULT_PORT: Final[int] = 3100
        "MCP default port."
        CLAUDE_CONTEXT_SERVER_NAME: Final[str] = "claude-context"
        "MCP server name for claude-context integration."
        CLAUDE_MEM_SERVER_NAME: Final[str] = "claude-mem"
        "MCP server name for claude-mem integration."

        # ===== Standard Paths =====
        PATHS_RULES_DIR: Final[str] = "rules"
        "Rules directory path."
        PATHS_DOCS_MAINTENANCE_REPORTS_DIR: Final[str] = "docs/maintenance/reports/"
        "Documentation maintenance reports directory path."
        SCHEDULED_MAINTENANCE_MIN_PYTHON_ARGS: Final[int] = 2
        "Minimum command parts for a python -m invocation."
        SCHEDULED_MAINTENANCE_MIN_GIT_ARGS: Final[int] = 2
        "Minimum command parts for a git subcommand invocation."
        SCHEDULED_MAINTENANCE_PYTHON_MODULE_INDEX: Final[int] = 2
        "Index of the module name in a python -m command."
        LINK_CHECKER_MIN_PATH_PARTS_FOR_REPO: Final[int] = 2
        "Minimum GitHub path parts for a repository URL."
        LINK_CHECKER_MIN_PATH_PARTS_FOR_DETAILED_REPO: Final[int] = 3
        "Minimum GitHub path parts for a detailed repository URL."
        STYLE_VALIDATOR_MIN_INLINE_CODE_BACKTICKS: Final[int] = 2
        "Minimum inline-code backticks for detecting code-style lines."
        STYLE_VALIDATOR_MAX_LINE_PREVIEW_LENGTH: Final[int] = 50
        "Maximum line preview length in style validation diagnostics."
        STYLE_VALIDATOR_MAX_LINE_TOO_LONG_VIOLATIONS: Final[int] = 5
        "Maximum long-line violations before emitting a wrapping suggestion."
        STYLE_VALIDATOR_MIN_COMMAND_LINE_ARGS: Final[int] = 2
        "Minimum argv length for style validator CLI usage."
        STYLE_VALIDATOR_CONFIG_ARG_INDEX: Final[int] = 2
        "Index of optional config path in style validator CLI usage."

        # ===== Validation Patterns =====
        PATTERNS_TYPE_IGNORE: Final[str] = "#\\s*type:\\s*ignore"
        "Type ignore comment pattern."
        PATTERNS_CAST_USAGE: Final[str] = "cast\\s*\\("
        "Cast function usage pattern."
        PATTERNS_ANY_TYPE: Final[str] = ":\\s*Any\\b"
        "Any type annotation pattern."
        PATTERNS_TYPE_CHECKING: Final[str] = "if\\s+TYPE_CHECKING\\s*:"
        "TYPE_CHECKING guard pattern."
        PATTERNS_TIER_VIOLATION: Final[str] = "from flext_.*\\.(services|api) import"
        "Tier violation import pattern."
        PATTERNS_OPTIONAL_PATTERN: Final[str] = "Optional\\["
        "Optional type pattern."
        PATTERNS_UNION_PATTERN: Final[str] = "Union\\["
        "Union type pattern."

        # === Pre-compiled regex authorities ===
        PATTERNS_TYPE_IGNORE_RE: ClassVar[t.RegexPattern] = re.compile(
            PATTERNS_TYPE_IGNORE,
        )
        PATTERNS_CAST_USAGE_RE: ClassVar[t.RegexPattern] = re.compile(
            PATTERNS_CAST_USAGE,
        )
        PATTERNS_ANY_TYPE_RE: ClassVar[t.RegexPattern] = re.compile(PATTERNS_ANY_TYPE)
        PATTERNS_TYPE_CHECKING_RE: ClassVar[t.RegexPattern] = re.compile(
            PATTERNS_TYPE_CHECKING,
        )
        PATTERNS_TIER_VIOLATION_RE: ClassVar[t.RegexPattern] = re.compile(
            PATTERNS_TIER_VIOLATION,
        )
        PATTERNS_OPTIONAL_RE: ClassVar[t.RegexPattern] = re.compile(
            PATTERNS_OPTIONAL_PATTERN,
        )
        PATTERNS_UNION_RE: ClassVar[t.RegexPattern] = re.compile(PATTERNS_UNION_PATTERN)
        FORBIDDEN_PATTERN_RE_MAP: ClassVar[t.MappingKV[str, t.RegexPattern]] = (
            MappingProxyType({
                "type-ignore": PATTERNS_TYPE_IGNORE_RE,
                "cast-usage": PATTERNS_CAST_USAGE_RE,
                "any-type": PATTERNS_ANY_TYPE_RE,
                "type-checking": PATTERNS_TYPE_CHECKING_RE,
                "optional-pattern": PATTERNS_OPTIONAL_RE,
                "union-pattern": PATTERNS_UNION_RE,
            })
        )

    class LinkCheckerDemo:
        """Demo link fixtures for the documentation link checker."""

        VSCODE_URL: Final[str] = "https://github.com/microsoft/vscode"
        HTTPBIN_OK_URL: Final[str] = "https://httpbin.org/status/200"
        HTTPBIN_BROKEN_URL: Final[str] = "https://httpbin.org/status/404"


__all__: list[str] = ["FlextQualityConstantsValues"]
