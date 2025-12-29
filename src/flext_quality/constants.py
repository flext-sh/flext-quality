"""FLEXT Quality Constants - Centralized constants following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from enum import StrEnum
from pathlib import Path
from typing import ClassVar

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

            # Code Quality Guardian thresholds
            ARCHITECTURE_VIOLATION_THRESHOLD: int = 5
            SOLID_VIOLATION_THRESHOLD: int = 10
            DRY_VIOLATION_THRESHOLD: int = 5
            KISS_VIOLATION_THRESHOLD: int = 5

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
            # Cognitive complexity (Complexipy)
            COGNITIVE_MAX_COMPLEXITY: int = 15
            COGNITIVE_LOW_THRESHOLD: int = 10
            COGNITIVE_MEDIUM_THRESHOLD: int = 15
            COGNITIVE_HIGH_THRESHOLD: int = 25

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
            # Tool-specific timeouts
            DEFAULT_TOOL_TIMEOUT: int = 30
            REFURB_TIMEOUT: int = 60
            COMPLEXIPY_TIMEOUT: int = 60
            ROPE_TIMEOUT: int = 60
            COVERAGE_TIMEOUT: int = 60
            RADON_TIMEOUT: int = 30
            # Validation tool timeouts
            RUFF_CHECK_TIMEOUT: int = 30
            MYPY_CHECK_TIMEOUT: int = 60

        class QualityNetwork:
            """Network-related constants."""

            MAX_CONNECTIONS: int = 100
            DEFAULT_TIMEOUT: int = 30
            RETRY_ATTEMPTS: int = 3
            DEFAULT_PORT: int = 8000
            MIN_PORT: int = 1
            MAX_PORT: int = 65535

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
            MAX_PROJECT_NAME_LENGTH: int = 255
            MIN_FILE_SIZE_FOR_DUPLICATION_CHECK: int = 100
            MIN_FILES_FOR_PAIR_COMPARISON: int = 2
            SIMILARITY_THRESHOLD: float = 0.65  # Aggressive: 65% detects more duplication to force refactoring
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

            # Code Quality Guardian analysis limits
            MAX_FILES_PER_RUN: int = 100
            SEMGREP_TIMEOUT_SECONDS: int = 120

        class Baseline:
            """Baseline file format constants."""

            PARTS_COUNT: int = 2
            DEFAULT_CONFIDENCE: int = 80
            EXCLUDED_DIRS: tuple[str, ...] = ("tests", "examples")

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

        class QualityGrade(StrEnum):
            """Quality grades with comprehensive scale (A+ through F).

            DRY Pattern:
                StrEnum is the single source of truth. Use QualityGrade.A_PLUS.value
                or QualityGrade.A_PLUS directly - no base strings needed.
            """

            A_PLUS = "A+"
            A = "A"
            A_MINUS = "A-"
            B_PLUS = "B+"
            B = "B"
            B_MINUS = "B-"
            C_PLUS = "C+"
            C = "C"
            C_MINUS = "C-"
            D_PLUS = "D+"
            D = "D"
            F = "F"

        class ModernizationCategory(StrEnum):
            """Categories for Refurb modernization suggestions.

            DRY Pattern:
                StrEnum is the single source of truth. Use ModernizationCategory.SYNTAX
                or ModernizationCategory.SYNTAX.value directly - no base strings needed.
            """

            SYNTAX = "syntax"
            PATTERN = "pattern"
            PERFORMANCE = "performance"
            READABILITY = "readability"

        class ComplexityLevel(StrEnum):
            """Cognitive complexity thresholds for Complexipy analysis.

            DRY Pattern:
                StrEnum is the single source of truth. Maps to Complexity class thresholds.
                LOW: <= COGNITIVE_LOW_THRESHOLD (10)
                MEDIUM: <= COGNITIVE_MEDIUM_THRESHOLD (15)
                HIGH: <= COGNITIVE_HIGH_THRESHOLD (25)
                CRITICAL: > COGNITIVE_HIGH_THRESHOLD
            """

            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
            CRITICAL = "critical"

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

        class Markdown:
            """Markdown documentation analysis constants."""

            # Header levels
            HEADER_H1_LEVEL: int = 1
            HEADER_H2_LEVEL: int = 2
            HEADER_H3_LEVEL: int = 3
            MAX_HEADER_HIERARCHY_JUMP: int = 1

            # Formatting defaults
            DEFAULT_WRAP_WIDTH: int = 88  # CONFIG

            # File patterns
            DEFAULT_GLOB_PATTERN: str = "**/*.md"

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
                r"def .*\).*->\s+object:",  # Regex pattern: function returning object
                r"except.*pass",
                r"from flext_core\.[^.]+\.import",
                r"class\s+\w+\s*\([^)]*\b[mptu]\b[^)]*\)",  # Runtime alias in class declaration/inheritance
            )

        class DryRun:
            """Dry-run mode constants for safe testing."""

            DEFAULT_TEMP_PREFIX: str = f"{tempfile.gettempdir()}/flext-tools-"
            BACKUP_SUFFIX: str = ".backup"
            DRY_RUN_DEFAULT: bool = True

        class Operations:
            """Quality operations constants for centralized validation."""

            # Coverage thresholds
            DEFAULT_MIN_COVERAGE: float = 80.0
            STRICT_MIN_COVERAGE: float = 90.0

            # Lint ratchet (errors must not increase)
            LINT_RATCHET_TOLERANCE: int = 0

            # Type checker selection
            DEFAULT_TYPE_CHECKER: str = "mypy"
            FALLBACK_TYPE_CHECKER: str = "pyrefly"

            # Batch operation settings
            MAX_FILES_PER_BATCH: int = 50
            AUTO_ROLLBACK_THRESHOLD: int = 0

        class Hooks:
            """Hook validation constants for shell integration.

            Provides patterns and module lists for FLEXT enforcement hooks.
            """

            # Foundation modules that cannot import from services/api
            FOUNDATION_MODULES: tuple[str, ...] = (
                "models",
                "protocols",
                "utilities",
                "constants",
                "typings",
            )

            # Directories where local constants are allowed (scripts, examples, etc.)
            LOCAL_CONSTANTS_ALLOWED: tuple[str, ...] = (
                "scripts/",
                "examples/",
            )

            # Tier violation patterns for foundation modules
            FORBIDDEN_IN_FOUNDATION: tuple[str, ...] = (
                r"from.*\.(services|api)\s",
                r"import.*\.(services|api)\s",
            )

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

        # =========================================================================
        # BATCH - Centralized batch operations constants
        # =========================================================================

        class Batch:
            """Batch operations constants for centralized fix scripts and hooks.

            Provides standardized modes, exit codes, and defaults for:
            - dry-run: Preview changes without modifying
            - backup: Create timestamped backups
            - execute: Apply changes with validation
            - rollback: Restore from backup on failure
            """

            class Mode(StrEnum):
                """Batch operation execution modes."""

                DRY_RUN = "dry-run"
                BACKUP = "backup"
                EXECUTE = "execute"
                ROLLBACK = "rollback"

            class ExitCode:
                """Standard exit codes for batch operations."""

                SUCCESS: int = 0
                VALIDATION_FAILED: int = 1
                BLOCKED: int = 2
                ROLLBACK_NEEDED: int = 3

            class Defaults:
                """Default configuration for batch operations."""

                BACKUP_DIR: str = tempfile.gettempdir()
                BACKUP_PREFIX: str = "flext_batch"
                BACKUP_EXTENSION: str = ".tar.gz"
                CLEANUP_HOURS: int = 24
                RATCHET_TOLERANCE: int = 0

        # =========================================================================
        # CYCLE - Refactoring cycle management constants
        # =========================================================================

        class Refactoring:
            """Refactoring scope and target constants for batch operations.

            Provides standardized scopes for:
            - Project-level: Single FLEXT project
            - Directory-level: src, tests, scripts, examples
            - Workspace-level: All FLEXT projects

            Usage:
                from flext_quality.constants import FlextQualityConstants

                scope = FlextQualityConstants.Quality.Refactoring.Scope.SRC
                projects = FlextQualityConstants.Quality.Refactoring.PROJECTS
            """

            class Scope(StrEnum):
                """Refactoring target scopes."""

                SRC = "src"
                TESTS = "tests"
                SCRIPTS = "scripts"
                EXAMPLES = "examples"
                ALL = "all"  # All directories

            class Target(StrEnum):
                """Refactoring operation targets."""

                PROJECT = "project"
                WORKSPACE = "workspace"

            # FLEXT projects in dependency order
            PROJECTS: tuple[str, ...] = (
                "flext-core",
                "flext-cli",
                "flext-ldif",
                "flext-ldap",
                "client-a-oud-mig",
            )

            # Workspace root path
            WORKSPACE_ROOT: str = "/home/marlonsc/flext"

            # Directories by scope
            SCOPE_DIRECTORIES: ClassVar[dict[str, tuple[str, ...]]] = {
                "src": ("src/",),
                "tests": ("tests/",),
                "scripts": ("scripts/",),
                "examples": ("examples/",),
                "all": ("src/", "tests/", "scripts/", "examples/"),
            }

            # Pattern replacements for namespace fixes
            class Patterns:
                """Common patterns for namespace refactoring."""

                # Nested namespace to flat namespace
                NESTED_TO_FLAT: ClassVar[dict[str, str]] = {
                    r"m\.Snapshot\.Configuration": "m.Configuration",
                    r"m\.Snapshot\.Service": "m.Service",
                    r"m\.Snapshot\.Health": "m.Health",
                    r"m\.Progress\.Operation": "m.Operation",
                }

                # Python 3.13+ syntax updates
                MODERN_SYNTAX: ClassVar[dict[str, str]] = {
                    r"Optional\[([^\]]+)\]": r"\1 | None",
                    r"Union\[([^,]+),\s*None\]": r"\1 | None",
                    r"Dict\[": "dict[",
                    r"List\[": "list[",
                    r"Tuple\[": "tuple[",
                    r"Set\[": "set[",
                }

        class Cycle:
            """Refactoring cycle management constants."""

            class Status(StrEnum):
                """Status values for files and projects in refactoring cycle."""

                PENDING = "pending"
                IN_PROGRESS = "in_progress"
                COMPLETED = "completed"
                MANUAL_REVIEW = "manual_review"
                SKIPPED = "skipped"

            class Severity(StrEnum):
                """Severity levels for discovered patterns."""

                BLOCK = "block"
                WARN = "warn"

            # Foundation projects always processed first
            FOUNDATION_PROJECTS: tuple[str, ...] = (
                "flext-core",
                "flext-cli",
            )

            # Fallback project order (used when discovery fails)
            _FALLBACK_PROJECT_ORDER: tuple[str, ...] = (
                "flext-core",
                "flext-cli",
                "flext-ldif",
                "flext-ldap",
                "flext-api",
                "flext-grpc",
                "flext-auth",
                "flext-plugin",
                "flext-quality",
                "flext-observability",
                "flext-web",
                "flext-db-oracle",
                "flext-oracle-oic",
                "flext-oracle-wms",
                "flext-dbt-ldap",
                "flext-dbt-ldif",
                "flext-dbt-oracle",
                "flext-dbt-oracle-wms",
                "flext-tap-ldap",
                "flext-tap-ldif",
                "flext-tap-oracle",
                "flext-tap-oracle-oic",
                "flext-tap-oracle-wms",
                "flext-target-ldap",
                "flext-target-ldif",
                "flext-target-oracle",
                "flext-target-oracle-oic",
                "flext-target-oracle-wms",
                "flext-meltano",
                "client-a-oud-mig",
                "flexcore",
            )

            # Backward compatibility alias
            PROJECT_ORDER = _FALLBACK_PROJECT_ORDER

            @classmethod
            def get_project_order(cls, _workspace_root: Path | None = None) -> tuple[str, ...]:
                """Retorna ordem de projetos descoberta dinamicamente.

                Usa FlextWorkspaceDiscovery para descobrir e ordenar.
                Fallback para lista hardcoded se discovery falhar.

                Args:
                    _workspace_root: Path to workspace root (default: ~/flext)

                Returns:
                    Tuple of project names in dependency order

                """
                # Discovery logic moved to cli.py to avoid circular imports
                return cls._FALLBACK_PROJECT_ORDER

            # Directory processing order
            DIRECTORY_ORDER: tuple[str, ...] = (
                "src/",
                "tests/",
                "scripts/",
                "examples/",
            )

        # =========================================================================
        # TYPE VERIFICATION - Type system compliance checking
        # =========================================================================

        class TypeVerification:
            """Type verification plugin constants for detecting type issues.

            Implements TV001-TV018 detection rules for:
            - Missing/excessive type annotations
            - Type centralization violations
            - Protocol/Model recommendations
            - FlextResult usage patterns
            """

            class RuleId:
                """Type verification rule identifiers (TV001-TV018)."""

                # Annotation issues
                MISSING_ANNOTATION = "TV001"
                EXCESSIVE_TYPING = "TV002"

                # Centralization violations
                TYPEALIAS_OUTSIDE_TYPINGS = "TV003"
                PROTOCOL_OUTSIDE_PROTOCOLS = "TV004"
                LOCAL_TYPEVAR = "TV005"

                # Protocol recommendations
                CALLABLE_NEEDS_PROTOCOL = "TV006"
                COMPLEX_CALLABLE_NEEDS_PROTOCOL = "TV007"
                UNION_CALLABLE_NEEDS_PROTOCOL = "TV008"

                # Model recommendations
                DICT_NEEDS_MODEL = "TV009"
                DATACLASS_NEEDS_PYDANTIC = "TV010"
                COMPLEX_UNION_NEEDS_MODEL = "TV011"

                # Coupling and complexity
                EXCESSIVE_ISINSTANCE = "TV012"
                TYPE_NARROWING_HINT = "TV013"
                EXCESSIVE_NONE_CHECKS = "TV014"

                # FlextResult misuse
                RESULT_RETURNING_NONE = "TV015"
                RESULT_MISSING_TYPE_PARAM = "TV016"
                RESULT_INCORRECT_UNWRAP = "TV017"

                # Uncentralized types
                UNCENTRALIZED_TYPE = "TV018"

            class Severity(StrEnum):
                """Type violation severity levels."""

                ERROR = "error"
                WARNING = "warning"
                INFO = "info"

            class Category(StrEnum):
                """Type violation categories."""

                MISSING_ANNOTATION = "missing_annotation"
                EXCESSIVE_TYPING = "excessive_typing"
                DECENTRALIZED_TYPE = "decentralized_type"
                NEEDS_PROTOCOL = "needs_protocol"
                NEEDS_MODEL = "needs_model"
                EXCESSIVE_COUPLING = "excessive_coupling"
                TYPE_NARROWING = "type_narrowing"
                EXCESSIVE_NONE = "excessive_none"
                RESULT_MISUSE = "result_misuse"
                UNCENTRALIZED_TYPE = "uncentralized_type"

            # Type mapping: raw type -> centralized type suggestion
            TYPE_MAPPING: ClassVar[dict[str, str]] = {
                # String dicts
                "dict[str, str]": "t.StringDict",
                "Mapping[str, str]": "t.StringMapping",
                # Int dicts
                "dict[str, int]": "t.StringIntDict",
                "Mapping[str, int]": "t.StringIntMapping",
                # Float/Bool/Numeric dicts
                "dict[str, float]": "t.StringFloatDict",
                "dict[str, bool]": "t.StringBoolDict",
                # Configuration dicts
                "dict[str, object]": "t.ConfigurationDict",
                "Mapping[str, object]": "t.ConfigurationMapping",
                # Nested dicts
                "dict[str, dict[str, int]]": "t.NestedStringIntDict",
                "dict[str, list[object]]": "t.StringListDict",
                # JSON/Scalar types
                "str | int | float | bool | None": "t.JsonPrimitive",
            }

            # Types that should NOT be flagged as uncentralized
            EXCLUDED_SIMPLE_TYPES: frozenset[str] = frozenset({
                "str", "int", "float", "bool", "None", "bytes",
                "list", "dict", "set", "tuple", "frozenset",
                "object", "type", "Self", "Never",
            })

            # Type prefixes to exclude from TV018
            EXCLUDED_TYPE_PREFIXES: tuple[str, ...] = (
                "t.",  # Already centralized
                "p.",  # Protocol usage
                "m.",  # Model usage
                "r[",  # FlextResult
                "FlextResult[",
                "list[str]", "list[int]", "list[float]", "list[bool]",
                "tuple[", "set[str]", "set[int]",
            )

            # Protocol namespace prefixes
            PROTOCOL_PREFIX: str = "p."
            FLEXT_PROTOCOLS_PREFIX: str = "Flext" + "Protocols."

            # Rule severity mapping
            RULE_SEVERITIES: ClassVar[dict[str, str]] = {
                "TV001": "warning",
                "TV002": "info",
                "TV003": "warning",
                "TV004": "warning",
                "TV005": "warning",
                "TV006": "info",
                "TV007": "warning",
                "TV008": "info",
                "TV009": "info",
                "TV010": "warning",
                "TV011": "info",
                "TV012": "warning",
                "TV013": "info",
                "TV014": "info",
                "TV015": "error",
                "TV016": "warning",
                "TV017": "warning",
                "TV018": "warning",
            }

            # Rules that should BLOCK in hooks
            BLOCKING_RULES: frozenset[str] = frozenset({
                "TV003",  # TypeAlias outside typings.py
                "TV004",  # Protocol outside protocols.py
                "TV015",  # FlextResult returning None
            })

            # Message templates
            MESSAGES: ClassVar[dict[str, str]] = {
                "TV001": "Missing type annotation for {target}",
                "TV002": "Excessive typing complexity in {target}",
                "TV003": "TypeAlias must be defined in typings.py, not {file}",
                "TV004": "Protocol must be defined in protocols.py, not {file}",
                "TV005": "TypeVar should be centralized in typings.py",
                "TV006": "Callable type should use Protocol for clarity",
                "TV007": "Complex Callable needs Protocol definition",
                "TV008": "Union with Callable should use Protocol",
                "TV009": "Complex dict type should use a Model",
                "TV010": "Consider using Pydantic model instead of dataclass",
                "TV011": "Complex Union type should use a Model",
                "TV012": "Excessive isinstance checks ({count} found)",
                "TV013": "Type narrowing opportunity detected",
                "TV014": "Excessive None checks ({count} found)",
                "TV015": "FlextResult method returning None directly",
                "TV016": "FlextResult missing type parameter",
                "TV017": "Incorrect FlextResult.unwrap() usage pattern",
                "TV018": "Use centralized type {suggestion} instead of {raw_type}",
            }

            # Thresholds
            MAX_ISINSTANCE_PER_FUNCTION: int = 5
            MAX_NONE_CHECKS_PER_FILE: int = 15
            MAX_CALLABLE_PARAMS: int = 3


c = FlextQualityConstants

__all__ = ["FlextQualityConstants", "c"]
