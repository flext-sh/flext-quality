"""FLEXT Quality Constants - Centralized constants following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from typing import ClassVar, Literal

from flext_core import FlextConstants


class FlextQualityConstants(FlextConstants):
    """Central container for quality assessment constants following FLEXT patterns.

    Extends FlextConstants with quality-specific constants organized into
    logical categories with complete type safety and enterprise standards.
    """

    # =========================================================================
    # COMPOSITION REFERENCES (Standardization Pattern)
    # =========================================================================

    # Core composition - reference core constants for easy access
    CoreErrors = FlextConstants.Errors
    CoreNetwork = FlextConstants.Network
    CoreSecurity = FlextConstants.Security
    CorePlatform = FlextConstants.Platform
    CoreValidation = FlextConstants.Validation

    # =============================================================================
    # QUALITY THRESHOLDS - Enterprise quality standards
    # =============================================================================

    class Thresholds:
        """Quality score thresholds for assessment levels."""

        # Industry-leading quality
        OUTSTANDING_THRESHOLD: float = 95.0
        EXCELLENT_THRESHOLD: float = 90.0
        GOOD_THRESHOLD: float = 80.0
        ACCEPTABLE_THRESHOLD: float = 70.0
        BELOW_AVERAGE_THRESHOLD: float = 60.0
        ENTERPRISE_READY_THRESHOLD: float = 85.0

    class Coverage:
        """Coverage thresholds and limits."""

        MINIMUM_COVERAGE: float = 90.0
        COVERAGE: float = 75.0
        TARGET_COVERAGE: float = 95.0
        EXCELLENT_COVERAGE: float = 98.0
        MAXIMUM_COVERAGE: float = 100.0

    class Complexity:
        """Complexity thresholds."""

        MAX_COMPLEXITY: int = 10
        WARNING_COMPLEXITY: int = 7
        IDEAL_COMPLEXITY: int = 5
        STRICT_COMPLEXITY: int = 8
        HIGH_COMPLEXITY_WARNING_THRESHOLD: int = 50

    class QualitySecurity:
        """Security scoring thresholds for quality analysis."""

        MINIMUM_SECURITY_SCORE: float = 90.0
        TARGET_SECURITY_SCORE: float = 95.0
        HIGH_SECURITY_SCORE_THRESHOLD: float = 95.0

    class Maintainability:
        """Maintainability scoring thresholds."""

        MINIMUM_MAINTAINABILITY: float = 80.0
        TARGET_MAINTAINABILITY: float = 90.0

    class Duplication:
        """Code duplication thresholds."""

        MAXIMUM_DUPLICATION: float = 5.0
        TARGET_DUPLICATION: float = 3.0
        EXCELLENT_DUPLICATION: float = 1.0

    # =============================================================================
    # PERFORMANCE AND TIMEOUTS - Analysis performance limits
    # =============================================================================

    class QualityPerformance:
        """Performance and timeout limits for quality analysis."""

        MINIMUM_ANALYSIS_TIMEOUT: int = 30
        MAXIMUM_ANALYSIS_TIMEOUT: int = 3600
        DEFAULT_ANALYSIS_TIMEOUT: int = 300
        MINIMUM_WORKERS: int = 1
        MAXIMUM_WORKERS: int = 16
        DEFAULT_WORKERS: int = 4

    class QualityNetwork:
        """Network-related constants."""

        MAX_CONNECTIONS: int = 100
        DEFAULT_TIMEOUT: int = 30
        RETRY_ATTEMPTS: int = 3

    class QualityValidation:
        """Validation ranges and limits for quality analysis."""

        MINIMUM_PERCENTAGE: float = 0.0
        MAXIMUM_PERCENTAGE: float = 100.0
        COVERAGE_EXTERNAL_TOOLS_THRESHOLD: float = 100.0
        SECURITY_BANDIT_THRESHOLD: float = 90.0
        SECURITY_DEPENDENCY_SCAN_THRESHOLD: float = 95.0

    # =============================================================================
    # REPORTING AND OUTPUT - Report generation constants
    # =============================================================================

    class Reporting:
        """Reporting constants and limits."""

        LARGE_REPORT_SIZE_BYTES: int = 100000
        PATH_SEGMENTS_TO_KEEP: int = 4
        SUPPORTED_FORMATS: tuple[str, ...] = (
            "HTML",
            "JSON",
            "PDF",
            "CSV",
            "XML",
            "MARKDOWN",
        )
        DEFAULT_FORMAT: str = "HTML"

    class Project:
        """Project lifecycle constants."""

        RECENT_UPDATE_DAYS: int = 7
        SUPPORTED_LANGUAGES: tuple[str, ...] = (
            "python",
            "javascript",
            "typescript",
            "java",
            "go",
            "rust",
        )

    # =============================================================================
    # ANALYSIS BACKENDS - Backend configuration constants
    # =============================================================================

    class Backends:
        """Analysis backend constants."""

        SUPPORTED_BACKENDS: tuple[str, ...] = ("AST", "EXTERNAL", "HYBRID")
        DEFAULT_BACKEND: str = "AST"
        EXTERNAL_TOOLS: tuple[str, ...] = (
            "ruff",
            "mypy",
            "bandit",
            "coverage",
            "pytest",
        )

    class Analysis:
        """Analysis configuration constants."""

        DEFAULT_INCLUDE_PATTERNS: tuple[str, ...] = ("*.py", "*.pyi")
        DEFAULT_EXCLUDE_PATTERNS: tuple[str, ...] = (
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
        )
        MAX_FUNCTION_NAME_LENGTH: int = 50
        MIN_FILE_SIZE_FOR_DUPLICATION_CHECK: int = 100
        SIMILARITY_THRESHOLD: float = 0.8
        MIN_FUNCTION_LENGTH_FOR_DEAD_CODE: int = 5
        GRADE_A_THRESHOLD: float = 90.0
        GRADE_B_THRESHOLD: float = 80.0
        GRADE_C_THRESHOLD: float = 70.0
        GRADE_D_THRESHOLD: float = 60.0
        HIGH_ISSUE_THRESHOLD: int = 50
        HTML_ISSUE_LIMIT: int = 100
        ISSUE_PREVIEW_LIMIT: int = 10
        MIN_COVERAGE_THRESHOLD: float = 75.0
        MIN_SCORE_THRESHOLD: float = 60.0

    # =============================================================================
    # LITERAL TYPES - Type-safe string literals
    # =============================================================================

    class Literals:
        """Type-safe string literals for quality analysis (Python 3.13+ best practices).

        These type aliases provide strict type checking for common string values
        used throughout the flext-quality codebase.
        """

        # Analysis status literal
        AnalysisStatusLiteral: type = Literal[
            "queued", "analyzing", "completed", "failed"
        ]

        # Issue severity literal
        IssueSeverityLiteral: type = Literal[
            "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"
        ]

        # Issue type literal
        IssueTypeLiteral: type = Literal[
            "SECURITY",
            "COMPLEXITY",
            "DUPLICATION",
            "COVERAGE",
            "STYLE",
            "BUG",
            "PERFORMANCE",
            "MAINTAINABILITY",
        ]

        # Report format literal
        ReportFormatLiteral: type = Literal[
            "HTML", "JSON", "PDF", "CSV", "XML", "MARKDOWN"
        ]

        # Backend type literal
        BackendTypeLiteral: type = Literal["AST", "EXTERNAL", "HYBRID"]

        # Language literal
        LanguageLiteral: type = Literal[
            "python", "javascript", "typescript", "java", "go", "rust"
        ]

        # Check status literal
        CheckStatusLiteral: type = Literal["passed", "failed", "warning"]

        # Log level literal (reusing from flext-core)
        LogLevelLiteral: type = Literal["debug", "info", "warning", "error", "critical"]

    # =============================================================================
    # QUALITY TOOLS - Internal tools constants
    # =============================================================================

    class Tools:
        """Quality tools constants."""

        LINT_TOOLS: tuple[str, ...] = ("ruff", "black")
        TYPE_TOOLS: tuple[str, ...] = ("mypy", "pyrefly")
        MIN_COVERAGE: int = 75
        MAX_LINE_LENGTH: int = 79
        REQUIRED_FILES: tuple[str, ...] = ("pyproject.toml", "Makefile", "README.md")
        REQUIRED_DIRS: tuple[str, ...] = ("src", "tests")

    class Git:
        """Git tool constants for quality operations."""

        DEFAULT_AUTHOR_NAME: str = "Marlon Costa"
        DEFAULT_AUTHOR_EMAIL: str = "marlonsc@gmail.com"
        DEFAULT_BACKUP_DIR: str = "~/flext-backup"
        AI_PATTERNS: tuple[str, ...] = (
            r"🤖 Generated with \[Claude Code\].*",
            r"Co-Authored-By: Claude.*",
            r"Co-Authored-By: Codex.*",
            r"Co-Authored-By: Cursor.*",
            r"Generated by Claude.*",
            r"Generated by Codex.*",
            r"Generated by Cursor.*",
            r"Claude Code.*",
            r"\[Claude Code\].*",
            r"\[Codex\].*",
            r"\[Cursor\].*",
            r"With assistance from.*",
            r"AI-assisted.*",
            r"noreply@anthropic\.com",
        )

    class Optimization:
        """Module optimization constants."""

        DEFAULT_BATCH_SIZE: int = 5
        MAX_FILE_SIZE: int = 512 * 1024 * 1024  # 512MB
        SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".py", ".pyi"})
        EXCLUDE_PATTERNS: tuple[str, ...] = (
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
        )

    class Patterns:
        """Pattern matching constants for quality analysis enforcement."""

        FORBIDDEN_DIRECT_IMPORTS: ClassVar[dict[str, str]] = {
            "import ldap3": "flext-ldap",
            "from ldap3": "flext-ldap",
            "import click": "flext-cli",
            "from click": "flext-cli",
            "import rich": "flext-cli",
            "from rich": "flext-cli",
            "import httpx": "flext-api",
            "from httpx": "flext-api",
            "import requests": "flext-api",
            "from requests": "flext-api",
            "import oracledb": "flext-db-oracle",
            "from oracledb": "flext-db-oracle",
            "import meltano": "flext-meltano",
            "from meltano": "flext-meltano",
            "import fastapi": "flext-web",
            "from fastapi": "flext-web",
        }

        FORBIDDEN_PATTERNS: tuple[str, ...] = (
            r"# type: ignore.*$",
            r"def .*\).*-> object:",
            r"except.*pass",
            r"from flext_core\.[^.]+\.import",
        )

    class DryRun:
        """Dry-run mode constants for safe testing."""

        DEFAULT_TEMP_PREFIX: str = f"{tempfile.gettempdir()}/flext-tools-"
        BACKUP_SUFFIX: str = ".backup"
        DRY_RUN_DEFAULT: bool = True

    # =============================================================================
    # SCORING AND PENALTIES - Quality score calculation constants
    # =============================================================================

    class Scoring:
        """Score calculation and penalty constants."""

        MAX_QUALITY_SCORE: float = 100.0
        MIN_QUALITY_SCORE: float = 0.0
        BASE_SCORE: float = 100.0
        CRITICAL_ISSUE_PENALTY: int = 10
        HIGH_ISSUE_PENALTY: int = 5
        NORMAL_ISSUE_PENALTY: int = 2
        LOW_ISSUE_PENALTY: int = 1
