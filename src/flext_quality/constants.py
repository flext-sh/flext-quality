"""FLEXT Quality Constants.

Centralized, immutable constants for the flext-quality project providing
hook events, rule types, validation thresholds, and runtime enumerations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal, TypeAlias

from flext_cli import FlextCliConstants
from flext_core import FlextConstants
from flext_web import FlextWebConstants


class FlextQualityConstants(FlextWebConstants, FlextCliConstants):
    """Centralized constants for flext-quality (Layer 0).

    Provides immutable, namespace-organized constants for hook processing,
    rule engines, validation, and quality enforcement.

    Usage:
        from flext_quality import c

        event = c.Quality.HookEvent.PRE_TOOL_USE
        threshold = c.Quality.Threshold.DEFAULT_LINES
    """

    class Quality:
        """Quality-specific constants namespace."""

        class Literals:
            """Literal type aliases for quality domain values."""

            AnalysisStatusLiteral: TypeAlias = Literal[
                "pending",
                "running",
                "completed",
                "failed",
                "cancelled",
            ]
            IssueSeverityLiteral: TypeAlias = Literal[
                "critical",
                "error",
                "warning",
                "info",
                "hint",
            ]
            IssueTypeLiteral: TypeAlias = Literal[
                "lint",
                "type",
                "security",
                "complexity",
                "style",
                "documentation",
            ]
            ReportFormatLiteral: TypeAlias = Literal[
                "json",
                "html",
                "markdown",
                "text",
                "sarif",
            ]
            BackendTypeLiteral: TypeAlias = Literal[
                "ruff",
                "mypy",
                "pyrefly",
                "bandit",
                "vulture",
                "radon",
            ]
            LanguageLiteral: TypeAlias = Literal[
                "python",
                "typescript",
                "javascript",
                "go",
                "rust",
            ]
            CheckStatusLiteral: TypeAlias = Literal["pass", "fail", "skip", "error"]

        class HookEvent(StrEnum):
            """Claude Code hook events."""

            PRE_TOOL_USE = "PreToolUse"
            POST_TOOL_USE = "PostToolUse"
            USER_PROMPT_SUBMIT = "UserPromptSubmit"
            PRE_COMPACT = "PreCompact"
            SESSION_START = "SessionStart"
            STOP = "Stop"

        class ToolName(StrEnum):
            """Tool names for hook filtering."""

            EDIT = "Edit"
            WRITE = "Write"
            BASH = "Bash"
            READ = "Read"
            GLOB = "Glob"
            GREP = "Grep"

        class RuleType(StrEnum):
            """Rule types for validation."""

            BLOCKING = "blocking"
            WARNING = "warning"
            INFO = "info"

        class RuleCategory(StrEnum):
            """Rule categories for organization."""

            LINT = "lint"
            TYPE = "type"
            PATTERN = "pattern"
            ARCHITECTURE = "architecture"
            SECURITY = "security"
            DOCUMENTATION = "documentation"

        class Severity(StrEnum):
            """Rule severity levels."""

            ERROR = "error"
            WARNING = "warning"
            INFO = "info"

        class RuleResult(StrEnum):
            """Rule evaluation results."""

            PASS = "pass"
            FAIL = "fail"
            SKIP = "skip"

        class IntegrationStatus(StrEnum):
            """External integration status."""

            CONNECTED = "connected"
            DISCONNECTED = "disconnected"
            ERROR = "error"

        class HookAction(StrEnum):
            """Hook response actions."""

            CONTINUE = "continue"
            BLOCK = "block"
            MODIFY = "modify"

        class Threshold:
            """Quality thresholds for validation."""

            # File size limits
            DEFAULT_LINES: Final[int] = 500
            MAX_LINES: Final[int] = 1000
            MIN_LINES: Final[int] = 1

            # Complexity limits
            MAX_CYCLOMATIC_COMPLEXITY: Final[int] = 10
            MAX_COGNITIVE_COMPLEXITY: Final[int] = 15
            MAX_FUNCTION_LENGTH: Final[int] = 50
            MAX_CLASS_LENGTH: Final[int] = 300

            # Coverage limits
            MIN_TEST_COVERAGE: Final[float] = 80.0
            MIN_DOCSTRING_COVERAGE: Final[float] = 80.0

            # Line length
            MAX_LINE_LENGTH: Final[int] = 88
            FLEXT_CORE_LINE_LENGTH: Final[int] = 79

        class Errors:
            """Quality-specific error codes."""

            RULE_FAILED: Final[str] = "QUALITY_RULE_FAILED"
            THRESHOLD_EXCEEDED: Final[str] = "QUALITY_THRESHOLD_EXCEEDED"
            PATTERN_VIOLATION: Final[str] = "QUALITY_PATTERN_VIOLATION"
            ARCHITECTURE_VIOLATION: Final[str] = "QUALITY_ARCHITECTURE_VIOLATION"
            TYPE_ERROR: Final[str] = "QUALITY_TYPE_ERROR"
            LINT_ERROR: Final[str] = "QUALITY_LINT_ERROR"

        class Defaults:
            """Default configuration values."""

            # Timeouts (milliseconds for hooks)
            HOOK_TIMEOUT_MS: Final[int] = 5000
            MCP_TIMEOUT_MS: Final[int] = 30000
            INTEGRATION_TIMEOUT_MS: Final[int] = 10000
            RULE_TIMEOUT_SECONDS: Final[int] = 30

            # Batch processing
            BATCH_SIZE: Final[int] = 100
            MAX_PARALLEL_RULES: Final[int] = 4

            # Caching
            CACHE_TTL_SECONDS: Final[int] = 300
            MAX_CACHE_ENTRIES: Final[int] = 1000

            # Search/Query defaults
            DEFAULT_SEARCH_LIMIT: Final[int] = 20
            DEFAULT_MEMORY_SEARCH_LIMIT: Final[int] = 10
            DEFAULT_TIMELINE_DEPTH: Final[int] = 5

            # JSON formatting
            JSON_INDENT: Final[int] = 2

            # Subprocess timeout conversion
            MS_TO_SECONDS_DIVISOR: Final[int] = 1000

        class Mcp:
            """MCP Server configuration."""

            SERVER_NAME: Final[str] = "flext-quality"
            SERVER_VERSION: Final[str] = "1.0.0"
            DEFAULT_PORT: Final[int] = 3100

        class Paths:
            """Standard paths for quality artifacts."""

            RULES_DIR: Final[str] = "rules"
            CONFIG_FILE: Final[str] = "quality.yaml"
            CACHE_DIR: Final[str] = ".quality_cache"
            REPORTS_DIR: Final[str] = "reports"

        class Patterns:
            """Regex patterns for validation."""

            # Python patterns
            TYPE_IGNORE: Final[str] = r"#\s*type:\s*ignore"
            CAST_USAGE: Final[str] = r"cast\s*\("
            ANY_TYPE: Final[str] = r":\s*Any\b"
            TYPE_CHECKING: Final[str] = r"if\s+TYPE_CHECKING\s*:"

            # Import patterns
            TIER_VIOLATION: Final[str] = r"from flext_.*\.(services|api) import"
            OPTIONAL_PATTERN: Final[str] = r"Optional\["
            UNION_PATTERN: Final[str] = r"Union\["


# Short alias for runtime access
c = FlextQualityConstants

__all__ = ["FlextQualityConstants", "c"]
