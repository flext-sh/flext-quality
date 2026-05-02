"""FLEXT Quality Constants.

Centralized, immutable constants for the flext-quality project providing
hook events, rule types, validation thresholds, and runtime enumerations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_infra import c
from flext_web import c as web_c


class FlextQualityConstants(c, web_c):
    """Centralized constants for flext-quality (Layer 0).

    Provides immutable, namespace-organized constants for hook processing,
    rule engines, validation, and quality enforcement.

    Usage:
        from flext_core import c

        event = c.Quality.HookEvent.PRE_TOOL_USE
        threshold = c.Quality.THRESHOLD_DEFAULT_LINES
    """

    class Quality:
        """Quality-specific constants namespace."""

        @unique
        class HookEvent(StrEnum):
            """Claude Code hook events."""

            PRE_TOOL_USE = "PreToolUse"
            POST_TOOL_USE = "PostToolUse"
            USER_PROMPT_SUBMIT = "UserPromptSubmit"
            PRE_COMPACT = "PreCompact"
            SESSION_START = "SessionStart"
            STOP = "Stop"

        @unique
        class ToolName(StrEnum):
            """Tool names for hook filtering."""

            EDIT = "Edit"
            WRITE = "Write"
            BASH = "Bash"
            READ = "Read"
            GLOB = "Glob"
            GREP = "Grep"

        @unique
        class RuleType(StrEnum):
            """Rule types for validation."""

            BLOCKING = "blocking"
            WARNING = "warning"
            INFO = "info"

        @unique
        class RuleCategory(StrEnum):
            """Rule categories for organization."""

            LINT = "lint"
            TYPE = "type"
            PATTERN = "pattern"
            ARCHITECTURE = "architecture"
            SECURITY = "security"
            DOCUMENTATION = "documentation"

        @unique
        class Severity(StrEnum):
            """Rule severity levels."""

            ERROR = "error"
            WARNING = "warning"
            INFO = "info"

        @unique
        class RuleResult(StrEnum):
            """Rule evaluation results."""

            PASS = "pass"
            FAIL = "fail"
            SKIP = "skip"

        @unique
        class IntegrationStatus(StrEnum):
            """External integration status."""

            CONNECTED = "connected"
            DISCONNECTED = "disconnected"
            ERROR = "error"

        @unique
        class HookAction(StrEnum):
            """Hook response actions."""

            CONTINUE = "continue"
            BLOCK = "block"
            MODIFY = "modify"

        @unique
        class NotificationPriority(StrEnum):
            """Notification priority levels for quality alerts."""

            CRITICAL = "critical"
            WARNING = "warning"
            INFO = "info"

        @unique
        class ArgumentAction(StrEnum):
            """Supported argparse actions for quality tooling."""

            STORE_TRUE = "store_true"
            STORE_FALSE = "store_false"

        @unique
        class ArgumentValueType(StrEnum):
            """Supported argparse value coercions for quality tooling."""

            STRING = "str"
            INTEGER = "int"

        # ===== Quality Thresholds =====
        THRESHOLD_DEFAULT_LINES: Final[int] = 500
        "Default lines threshold."
        THRESHOLD_MAX_LINES: Final[int] = 1000
        "Maximum lines threshold."
        THRESHOLD_MIN_LINES: Final[int] = 1
        "Minimum lines threshold."
        THRESHOLD_MAX_CYCLOMATIC_COMPLEXITY: Final[int] = 10
        "Maximum cyclomatic complexity."
        THRESHOLD_MAX_COGNITIVE_COMPLEXITY: Final[int] = 15
        "Maximum cognitive complexity."
        THRESHOLD_MAX_FUNCTION_LENGTH: Final[int] = 50
        "Maximum function length."
        THRESHOLD_MAX_CLASS_LENGTH: Final[int] = 300
        "Maximum class length."
        THRESHOLD_MIN_TEST_COVERAGE: Final[float] = 80.0
        "Minimum test coverage percentage."
        THRESHOLD_MIN_DOCSTRING_COVERAGE: Final[float] = 80.0
        "Minimum docstring coverage percentage."
        THRESHOLD_MAX_LINE_LENGTH: Final[int] = 88
        "Maximum line length."
        THRESHOLD_FLEXT_CORE_LINE_LENGTH: Final[int] = 79
        "FLEXT core maximum line length."
        THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW: Final[int] = 10
        "Maximum broken links to show."
        THRESHOLD_MIN_HEADINGS_FOR_TOC: Final[int] = 5
        "Minimum headings for table of contents."

        HOOK_TIMEOUT_MS: Final[int] = 5000
        MCP_TIMEOUT_MS: Final[int] = 30000
        INTEGRATION_TIMEOUT_MS: Final[int] = 10000
        RULE_TIMEOUT_SECONDS: Final[int] = c.DEFAULT_TIMEOUT_SECONDS
        BATCH_SIZE: Final[int] = 100
        MAX_PARALLEL_RULES: Final[int] = 4
        MAX_CACHE_ENTRIES: Final[int] = 1000
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

        # ===== Standard Paths =====
        PATHS_RULES_DIR: Final[str] = "rules"
        "Rules directory path."
        PATHS_CONFIG_FILE: Final[str] = "quality.yaml"
        "Configuration file path."
        PATHS_CACHE_DIR: Final[str] = ".quality_cache"
        "Cache directory path."
        PATHS_REPORTS_DIR: Final[str] = "reports"
        "Reports directory path."
        PATHS_DOCS_MAINTENANCE_REPORTS_DIR: Final[str] = "docs/maintenance/reports/"
        "Documentation maintenance reports directory path."
        PATHS_DOCS_MAINTENANCE_SETTINGS_DIR: Final[str] = "docs/maintenance/settings/"
        "Documentation maintenance settings directory path."

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


c = FlextQualityConstants
__all__: tuple[str, ...] = ("FlextQualityConstants", "c")
