"""FLEXT Quality Constants - Centralized constants following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from enum import StrEnum
from typing import ClassVar, Literal

from flext_core import FlextConstants


class FlextQualityConstants(FlextConstants):
    """Central container for quality assessment constants following FLEXT patterns.

    Usage:
    ```python
    from flext_quality.constants import FlextQualityConstants

    threshold = FlextQualityConstants.Quality.Thresholds.OUTSTANDING_THRESHOLD
    coverage = FlextQualityConstants.Quality.Coverage.MINIMUM_COVERAGE
    ```
    """

    class Quality:
        """Quality domain constants namespace.

        All quality-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        # =========================================================================
        # COMPOSITION REFERENCES (Standardization Pattern) - Real Inheritance
        # =========================================================================

        # Core composition - real inheritance classes
        class CoreErrors(FlextConstants.Errors):
            """Core errors constants - real inheritance."""

        class CoreNetwork(FlextConstants.Network):
            """Core network constants - real inheritance."""

        class CoreSecurity(FlextConstants.Security):
            """Core security constants - real inheritance."""

        class CorePlatform(FlextConstants.Platform):
            """Core platform constants - real inheritance."""

        class CoreValidation(FlextConstants.Validation):
            """Core validation constants - real inheritance."""

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
            # SUPPORTED_FORMATS will be set after ReportFormat StrEnum is defined
            SUPPORTED_FORMATS: ClassVar[tuple[str, ...]]
            DEFAULT_FORMAT: str = "HTML"

        class Project:
            """Project lifecycle constants."""

            RECENT_UPDATE_DAYS: int = 7
            # SUPPORTED_LANGUAGES will be set after Language StrEnum is defined
            SUPPORTED_LANGUAGES: ClassVar[tuple[str, ...]]

        # =============================================================================
        # ANALYSIS BACKENDS - Backend configuration constants
        # =============================================================================

        class Backends:
            """Analysis backend constants."""

            # SUPPORTED_BACKENDS will be set after BackendType StrEnum is defined
            SUPPORTED_BACKENDS: ClassVar[tuple[str, ...]]
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
        # STRENUM CLASSES - Single source of truth for string enumerations
        # =============================================================================

        class AnalysisStatus(StrEnum):
            """Analysis status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use AnalysisStatus.QUEUED.value
                or AnalysisStatus.QUEUED directly - no base strings needed.
            """

            QUEUED = "queued"
            ANALYZING = "analyzing"
            COMPLETED = "completed"
            FAILED = "failed"

        class IssueSeverity(StrEnum):
            """Issue severity enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use IssueSeverity.CRITICAL.value
                or IssueSeverity.CRITICAL directly - no base strings needed.
            """

            CRITICAL = "CRITICAL"
            HIGH = "HIGH"
            MEDIUM = "MEDIUM"
            LOW = "LOW"
            INFO = "INFO"

        class IssueType(StrEnum):
            """Issue type enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use IssueType.SECURITY.value
                or IssueType.SECURITY directly - no base strings needed.
            """

            SECURITY = "SECURITY"
            COMPLEXITY = "COMPLEXITY"
            DUPLICATION = "DUPLICATION"
            COVERAGE = "COVERAGE"
            STYLE = "STYLE"
            BUG = "BUG"
            PERFORMANCE = "PERFORMANCE"
            MAINTAINABILITY = "MAINTAINABILITY"

        class ReportFormat(StrEnum):
            """Report format enumeration - matches Reporting.SUPPORTED_FORMATS.

            DRY Pattern:
                StrEnum is the single source of truth. Use ReportFormat.HTML.value
                or ReportFormat.HTML directly - no base strings needed.
            """

            HTML = "HTML"
            JSON = "JSON"
            PDF = "PDF"
            CSV = "CSV"
            XML = "XML"
            MARKDOWN = "MARKDOWN"

        class BackendType(StrEnum):
            """Backend type enumeration - matches Backends.SUPPORTED_BACKENDS.

            DRY Pattern:
                StrEnum is the single source of truth. Use BackendType.AST.value
                or BackendType.AST directly - no base strings needed.
            """

            AST = "AST"
            EXTERNAL = "EXTERNAL"
            HYBRID = "HYBRID"

        class Language(StrEnum):
            """Language enumeration - matches Project.SUPPORTED_LANGUAGES.

            DRY Pattern:
                StrEnum is the single source of truth. Use Language.PYTHON.value
                or Language.PYTHON directly - no base strings needed.
            """

            PYTHON = "python"
            JAVASCRIPT = "javascript"
            TYPESCRIPT = "typescript"
            JAVA = "java"
            GO = "go"
            RUST = "rust"

        class CheckStatus(StrEnum):
            """Check status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use CheckStatus.PASSED.value
                or CheckStatus.PASSED directly - no base strings needed.
            """

            PASSED = "passed"
            FAILED = "failed"
            WARNING = "warning"

        # Generated tuples from StrEnum members (DRY principle)
        # These replace the hardcoded tuples to avoid duplication
        # Access via: FlextQualityConstants.Quality.Reporting.SUPPORTED_FORMATS
        #            FlextQualityConstants.Quality.Project.SUPPORTED_LANGUAGES
        #            FlextQualityConstants.Quality.Backends.SUPPORTED_BACKENDS
        Reporting.SUPPORTED_FORMATS = tuple(
            member.value for member in ReportFormat.__members__.values()
        )
        """Supported report formats - generated from ReportFormat StrEnum."""

        Project.SUPPORTED_LANGUAGES = tuple(
            member.value for member in Language.__members__.values()
        )
        """Supported languages - generated from Language StrEnum."""

        Backends.SUPPORTED_BACKENDS = tuple(
            member.value for member in BackendType.__members__.values()
        )
        """Supported backends - generated from BackendType StrEnum."""

        # =============================================================================
        # LITERAL TYPES - Type-safe string literals (PEP 695)
        # =============================================================================
        # All Literal types reference StrEnum members - NO string duplication!

        class Literals:
            """Type-safe string literals for quality analysis (Python 3.13+ best practices).

            These type aliases provide strict type checking for common string values
            used throughout the flext-quality codebase.
            All Literal types reference StrEnum members to avoid string duplication (DRY principle).
            Using PEP 695 type statement for better type checking and IDE support.
            """

            # Analysis status literal - references AnalysisStatus StrEnum members
            type AnalysisStatusLiteral = Literal[
                FlextQualityConstants.Quality.AnalysisStatus.QUEUED,
                FlextQualityConstants.Quality.AnalysisStatus.ANALYZING,
                FlextQualityConstants.Quality.AnalysisStatus.COMPLETED,
                FlextQualityConstants.Quality.AnalysisStatus.FAILED,
            ]

            # Issue severity literal - references IssueSeverity StrEnum members
            type IssueSeverityLiteral = Literal[
                FlextQualityConstants.Quality.IssueSeverity.CRITICAL,
                FlextQualityConstants.Quality.IssueSeverity.HIGH,
                FlextQualityConstants.Quality.IssueSeverity.MEDIUM,
                FlextQualityConstants.Quality.IssueSeverity.LOW,
                FlextQualityConstants.Quality.IssueSeverity.INFO,
            ]

            # Issue type literal - references IssueType StrEnum members
            type IssueTypeLiteral = Literal[
                FlextQualityConstants.Quality.IssueType.SECURITY,
                FlextQualityConstants.Quality.IssueType.COMPLEXITY,
                FlextQualityConstants.Quality.IssueType.DUPLICATION,
                FlextQualityConstants.Quality.IssueType.COVERAGE,
                FlextQualityConstants.Quality.IssueType.STYLE,
                FlextQualityConstants.Quality.IssueType.BUG,
                FlextQualityConstants.Quality.IssueType.PERFORMANCE,
                FlextQualityConstants.Quality.IssueType.MAINTAINABILITY,
            ]

            # Report format literal - references ReportFormat StrEnum members
            type ReportFormatLiteral = Literal[
                FlextQualityConstants.Quality.ReportFormat.HTML,
                FlextQualityConstants.Quality.ReportFormat.JSON,
                FlextQualityConstants.Quality.ReportFormat.PDF,
                FlextQualityConstants.Quality.ReportFormat.CSV,
                FlextQualityConstants.Quality.ReportFormat.XML,
                FlextQualityConstants.Quality.ReportFormat.MARKDOWN,
            ]

            # Backend type literal - references BackendType StrEnum members
            type BackendTypeLiteral = Literal[
                FlextQualityConstants.Quality.BackendType.AST,
                FlextQualityConstants.Quality.BackendType.EXTERNAL,
                FlextQualityConstants.Quality.BackendType.HYBRID,
            ]

            # Language literal - references Language StrEnum members
            type LanguageLiteral = Literal[
                FlextQualityConstants.Quality.Language.PYTHON,
                FlextQualityConstants.Quality.Language.JAVASCRIPT,
                FlextQualityConstants.Quality.Language.TYPESCRIPT,
                FlextQualityConstants.Quality.Language.JAVA,
                FlextQualityConstants.Quality.Language.GO,
                FlextQualityConstants.Quality.Language.RUST,
            ]

            # Check status literal - references CheckStatus StrEnum members
            type CheckStatusLiteral = Literal[
                FlextQualityConstants.Quality.CheckStatus.PASSED,
                FlextQualityConstants.Quality.CheckStatus.FAILED,
                FlextQualityConstants.Quality.CheckStatus.WARNING,
            ]

            # Log level literal (reusing from flext-core)
            type LogLevelLiteral = FlextConstants.Literals.LogLevelLiteral

        # =============================================================================
        # QUALITY TOOLS - Internal tools constants
        # =============================================================================

        class Tools:
            """Quality tools constants."""

            LINT_TOOLS: tuple[str, ...] = ("ruff", "black")
            TYPE_TOOLS: tuple[str, ...] = ("mypy", "pyrefly")
            MIN_COVERAGE: int = 75
            MAX_LINE_LENGTH: int = 79
            REQUIRED_FILES: tuple[str, ...] = (
                "pyproject.toml",
                "Makefile",
                "README.md",
            )
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


c = FlextQualityConstants

__all__ = ["FlextQualityConstants", "c"]
