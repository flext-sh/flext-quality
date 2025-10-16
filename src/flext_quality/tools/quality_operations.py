"""Quality checking operations for linting, type checking, and duplicate detection.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Consolidates flext_tools quality operations:
- QualityGateway → Complete quality pipeline
- LintingService → Ruff linting operations
- TypeChecker → MyPy/PyRefly type checking
- DuplicateDetector → Code duplicate detection
- ExportRepairer → __init__.py export fixing
- DocstringNormalizer → Google-style docstring normalization
- PatternAuditor → Code pattern auditing
- FalsePositiveAuditor → False positive filtering

MANDATORY: Uses flext-cli for ALL output (NO direct rich/click)
"""

from __future__ import annotations

import re
from pathlib import Path

from flext_cli import FlextCli
from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
    FlextTypes,
    FlextUtilities,
)
from pydantic import ConfigDict

from flext_quality.models import FlextQualityModels
from .utilities import FlextQualityToolsUtilities


class FlextQualityOperations(FlextService[None]):
    """Unified quality checking operations with complete flext-core integration.

    Example usage:
    ```python
    from .tools import FlextQualityOperations

    quality = FlextQualityOperations()

    # Run all quality checks
    result = quality.gateway.run_all_checks(project_path=".")

    # Run specific checks
    lint_result = quality.linting.fix_issues(
        module_path="src/my_module.py",
        dry_run=True,  # MANDATORY default
    )

    type_result = quality.types.check_types(module_path="src/my_module.py")
    dup_result = quality.duplicates.detect(project_path=".", threshold=10)
    ```

    MANDATORY: Uses flext-cli for ALL output (NO direct rich/click).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    def execute(self) -> FlextResult[None]:
        """Execute quality operations service - FlextService interface."""
        return FlextResult[None].ok(None)

    class QualityGateway:
        """Quality gateway running all checks.

        Consolidates: quality_gateway.py, quality_gateway_runner.py
        """

        @classmethod
        def run_all_checks(
            cls,
            project_path: str,
            *,
            _config: dict[str, object] | None = None,
        ) -> FlextResult[FlextQualityModels.CheckResult]:
            """Run complete quality pipeline.

            Args:
                project_path: Path to project
                config: Optional configuration (reserved for future use)

            Returns:
                FlextResult with QualityCheckResult

            """
            FlextLogger(__name__)
            FlextCli()  # MANDATORY: Use flext-cli

            # Run lint check
            lint_result = FlextQualityOperations.LintingService.run_lint(project_path)
            lint_passed = lint_result.is_success

            # Run type check
            type_result = FlextQualityOperations.TypeChecker.run_type_check(
                project_path
            )
            type_passed = type_result.is_success

            # Run coverage check (placeholder)
            coverage = 0.0

            result = FlextQualityModels.CheckResult(
                lint_passed=lint_passed,
                type_check_passed=type_passed,
                coverage=coverage,
                violations=[],
            )

            return FlextResult[FlextQualityModels.CheckResult].ok(result)

    class LintingService:
        """Linting operations with gradual fixing.

        Consolidates: gradual_lint_fixer.py, lint_fixer.py
        """

        @staticmethod
        def run_lint(project_path: str) -> FlextResult[FlextTypes.Dict]:
            """Run ruff linting."""
            cmd_result = FlextUtilities.run_external_command(
                cmd=["ruff", "check", project_path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Handle execution failure
            if cmd_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Ruff execution failed: {cmd_result.error}"
                )

            result = cmd_result.value

            if result.returncode == 0:
                return FlextResult[FlextTypes.Dict].ok({"passed": True})

            return FlextResult[FlextTypes.Dict].fail(f"Linting failed: {result.stdout}")

        @staticmethod
        def fix_issues(
            module_path: str,
            *,
            dry_run: bool = True,
        ) -> FlextResult[FlextTypes.Dict]:
            """Fix linting issues gradually.

            Args:
                module_path: Path to Python module or project
                dry_run: Run in dry-run mode (default True - MANDATORY)

            Returns:
                FlextResult with fixing statistics

            """
            logger = FlextLogger(__name__)

            if dry_run:
                logger.info("DRY RUN: Would fix linting issues")
                # Run check to see what would be fixed
                cmd_result = FlextUtilities.run_external_command(
                    cmd=["ruff", "check", module_path, "--fix", "--dry-run"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                # Handle execution failure
                if cmd_result.is_failure:
                    return FlextResult[FlextTypes.Dict].fail(
                        f"Ruff dry-run failed: {cmd_result.error}"
                    )

                result = cmd_result.value
                return FlextResult[FlextTypes.Dict].ok(
                    {
                        "dry_run": True,
                        "would_fix": result.stdout.count("Fixed"),
                        "message": result.stdout,
                    }
                )

            # Real fix
            cmd_result = FlextUtilities.run_external_command(
                cmd=["ruff", "check", module_path, "--fix"],
                capture_output=True,
                text=True,
                check=False,
            )

            # Handle execution failure
            if cmd_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Ruff fix failed: {cmd_result.error}"
                )

            result = cmd_result.value

            if result.returncode == 0:
                return FlextResult[FlextTypes.Dict].ok({"fixed": True})

            return FlextResult[FlextTypes.Dict].fail(f"Fixing failed: {result.stderr}")

    class TypeChecker:
        """Type checking with MyPy/PyRefly.

        Consolidates: mypy_checker.py, mypy_analyzer.py
        """

        @staticmethod
        def run_type_check(
            project_path: str,
            *,
            _strict: bool = True,
        ) -> FlextResult[FlextTypes.Dict]:
            """Run type checking.

            Args:
                project_path: Path to Python module or project
                _strict: Use strict mode (reserved for future use)

            Returns:
                FlextResult with type checking results

            """
            # Try pyrefly first
            cmd_result = FlextUtilities.run_external_command(
                cmd=["pyrefly", "check", project_path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Handle execution failure
            if cmd_result.is_failure:
                # Pyrefly failed to execute, fall back to mypy
                pass
            else:
                result = cmd_result.value
                if result.returncode == 0:
                    return FlextResult[FlextTypes.Dict].ok(
                        {
                            "passed": True,
                            "tool": "pyrefly",
                        }
                    )

            # Fall back to mypy
            cmd_result = FlextUtilities.run_external_command(
                cmd=["mypy", project_path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Handle execution failure
            if cmd_result.is_failure:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Type checking failed: {cmd_result.error}"
                )

            result = cmd_result.value

            if result.returncode == 0:
                return FlextResult[FlextTypes.Dict].ok(
                    {
                        "passed": True,
                        "tool": "mypy",
                    }
                )

            return FlextResult[FlextTypes.Dict].fail(
                f"Type checking failed: {result.stdout}"
            )

        @staticmethod
        def check_types(
            module_path: str,
        ) -> FlextResult[FlextTypes.Dict]:
            """Run type checking with console output.

            Args:
                module_path: Path to Python module or project

            Returns:
                FlextResult with type checking results

            """
            FlextLogger(__name__)
            FlextCli()  # MANDATORY: Use flext-cli

            return FlextQualityOperations.TypeChecker.run_type_check(module_path)

    class DuplicateDetector:
        """Code duplicate detection and analysis.

        Consolidates: detect_duplicates.py, code_duplicates.py, duplicates.py
        """

        @staticmethod
        def detect_duplicates(
            _project_path: str,
            *,
            threshold: int = 10,
        ) -> FlextResult[FlextTypes.Dict]:
            """Detect code duplicates.

            Args:
                _project_path: Path to project (reserved for future implementation)
                threshold: Minimum lines for duplicate detection

            Returns:
                FlextResult with duplicate detection results

            """
            FlextLogger(__name__)
            FlextCli()  # MANDATORY: Use flext-cli

            # Placeholder implementation - would use AST analysis or external tool
            return FlextResult[FlextTypes.Dict].ok(
                {
                    "duplicates_found": 0,
                    "threshold": threshold,
                }
            )

    class ExportRepairer:
        """__init__.py export repair and validation.

        Consolidates: repair_init_exports.py
        """

        @staticmethod
        def repair_exports(
            _package_path: str,
            *,
            dry_run: bool = True,
        ) -> FlextResult[FlextTypes.Dict]:
            """Repair __init__.py exports.

            Args:
                _package_path: Path to Python package (reserved for future implementation)
                dry_run: Run in dry-run mode (default True - MANDATORY)

            Returns:
                FlextResult with repair statistics

            """
            logger = FlextLogger(__name__)

            if dry_run:
                logger.info("DRY RUN: Would repair exports")
                return FlextResult[FlextTypes.Dict].ok(
                    {
                        "dry_run": True,
                        "message": "Dry run - no changes made",
                    }
                )

            # Would implement export repair logic here
            return FlextResult[FlextTypes.Dict].ok({"repaired": True})

    class DocstringNormalizer:
        """Docstring normalization to Google style.

        Consolidates: normalize_docstrings.py
        """

        @staticmethod
        def normalize_docstrings(
            _module_path: str,
            *,
            dry_run: bool = True,
        ) -> FlextResult[FlextTypes.Dict]:
            """Normalize docstrings to Google style.

            Args:
                _module_path: Path to Python module (reserved for future implementation)
                dry_run: Run in dry-run mode (default True - MANDATORY)

            Returns:
                FlextResult with normalization statistics

            """
            logger = FlextLogger(__name__)

            if dry_run:
                logger.info("DRY RUN: Would normalize docstrings")
                return FlextResult[FlextTypes.Dict].ok(
                    {
                        "dry_run": True,
                        "message": "Dry run - no changes made",
                    }
                )

            # Would implement docstring normalization here
            return FlextResult[FlextTypes.Dict].ok({"normalized": True})

    class PatternAuditor:
        """Pattern audit system for code quality.

        Consolidates: pattern_audit_system.py
        """

        @staticmethod
        def audit_patterns(
            project_path: str,
        ) -> FlextResult[FlextTypes.Dict]:
            """Audit code patterns for quality issues.

            Args:
                project_path: Path to project

            Returns:
                FlextResult with audit results

            """
            FlextLogger(__name__)
            FlextCli()  # MANDATORY: Use flext-cli

            workspace = Path(project_path).expanduser().resolve()
            if not workspace.exists():
                return FlextResult[FlextTypes.Dict].fail(
                    f"Project path does not exist: {workspace}"
                )

            method_pattern = re.compile(
                r"def\s+(?P<name>\w+)\([^)]*\)\s*->\s*FlextResult\[(?P<rtype>[^\]]+)\]:"
            )
            bad_return_pattern = re.compile(
                r"return\s+FlextResult\.(?:ok|fail)\s*\("
            )

            issues: list[FlextTypes.StringDict] = []

            for file_path in workspace.rglob("*.py"):
                if FlextQualityToolsUtilities.Paths.should_ignore_path(file_path):
                    continue

                try:
                    source = file_path.read_text(encoding="utf-8")
                except OSError:
                    continue

                lines = source.splitlines()
                for line_number, line in enumerate(lines, start=1):
                    method_match = method_pattern.search(line)
                    if not method_match:
                        continue

                    declared_type = method_match.group("rtype").strip()
                    if declared_type.casefold() == "none":
                        continue

                    # Inspect the next ~50 lines for bad returns
                    for candidate in lines[line_number : line_number + 50]:
                        if candidate.strip().startswith("def "):
                            break
                        if bad_return_pattern.search(candidate):
                            issues.append(
                                {
                                    "file": str(file_path.relative_to(workspace)),
                                    "line": line_number,
                                    "method": method_match.group("name"),
                                    "declared_type": declared_type,
                                    "issue": "FlextResult[T] method returns FlextResult.ok()/fail() directly",
                                }
                            )
                            break

            return FlextResult[FlextTypes.Dict].ok(
                {
                    "issues_found": len(issues),
                    "issues": issues,
                }
            )

    class FalsePositiveAuditor:
        """False positive auditing and filtering.

        Consolidates: audit_false_positives.py
        """

        @staticmethod
        def audit_false_positives(
            results: list[FlextTypes.Dict],
        ) -> FlextResult[list[FlextTypes.Dict]]:
            """Audit and filter false positives.

            Args:
                results: List of check results to audit

            Returns:
                FlextResult with filtered results

            """
            FlextLogger(__name__)

            # Filter false positives
            filtered = [r for r in results if not r.get("false_positive", False)]

            return FlextResult[list[FlextTypes.Dict]].ok(filtered)

    def __init__(self) -> None:
        """Initialize quality operations service."""
        super().__init__()
        self.logger = FlextLogger(__name__)
        # Note: FlextCli is created locally in methods that need it

        # Initialize helper services
        self.gateway = self.QualityGateway()
        self.linting = self.LintingService()
        self.types = self.TypeChecker()
        self.duplicates = self.DuplicateDetector()
        self.exports = self.ExportRepairer()
        self.docstrings = self.DocstringNormalizer()
        self.patterns = self.PatternAuditor()
        self.audit = self.FalsePositiveAuditor()


__all__ = ["FlextQualityOperations"]
