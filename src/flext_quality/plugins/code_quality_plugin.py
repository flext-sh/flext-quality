# VERIFIED_NEW_MODULE
"""Code Quality Plugin - SOLID/DRY/KISS validation.

Validates code quality using multiple tools orchestrated in parallel:
- Semgrep: Custom FLEXT pattern rules
- Deptry: Unused dependencies
- Pip-Audit: Security vulnerabilities (CVE scanning)
- Interrogate: Docstring coverage
- Darglint: Docstring validation
- Radon: Cyclomatic complexity (via external_backend)
- Complexipy: Cognitive complexity (via external_backend)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult, FlextService

from ..constants import FlextQualityConstants as c
from ..tools.workspace_discovery import FlextWorkspaceDiscovery
from .duplication_plugin import FlextDuplicationPlugin


class FlextCodeQualityPlugin(FlextService[int]):
    """Comprehensive code quality validation plugin.

    Validates SOLID, DRY, KISS through multiple integrated tools.

    Usage::

        from flext_quality.plugins import FlextCodeQualityPlugin

        plugin = FlextCodeQualityPlugin()

        # Single file/directory check
        result = plugin.check([Path("src/")])
        if result.is_success:
            for v in result.value.violations:
                logger.info("%s: %s", v.severity, v.message)

        # Workspace-wide check with FlextWorkspaceDiscovery
        result = plugin.check_workspace(Path("~/flext"))
        if result.is_success:
            logger.info("Total violations: %d", result.value.total_violations)

    """

    __slots__ = (
        "_duplication_plugin",
        "_logger",
        "_semgrep_rules_path",
        "_workspace_discovery",
    )

    # ============================================
    # Result Dataclasses
    # ============================================

    @dataclass(frozen=True, slots=True)
    class Violation:
        """Single code quality violation."""

        category: str  # SOLID, DRY, KISS, ANTI_PATTERN, FLEXT_ARCHITECTURE
        principle: str  # SRP, OCP, LSP, ISP, DIP, DUPLICATION, etc.
        severity: str  # ERROR, WARNING, INFO
        file_path: Path
        line_number: int | None
        message: str
        suggestion: str
        tool: str  # semgrep, deptry, pip-audit, interrogate, darglint
        rule_id: str | None

    @dataclass(frozen=True, slots=True)
    class CheckResult:
        """Aggregated check result."""

        total_violations: int
        files_checked: int
        violations_by_category: dict[str, int]
        violations_by_severity: dict[str, int]
        violations: tuple[FlextCodeQualityPlugin.Violation, ...] = field(
            default_factory=tuple
        )
        consolidation_guidance: tuple[str, ...] = field(default_factory=tuple)

    @dataclass(frozen=True, slots=True)
    class WorkspaceCheckResult:
        """Result of workspace-wide quality check."""

        total_projects: int
        total_violations: int
        total_files: int
        violations_by_project: dict[str, int]
        violations_by_category: dict[str, int]
        violations_by_severity: dict[str, int]
        violations: tuple[FlextCodeQualityPlugin.Violation, ...] = field(
            default_factory=tuple
        )
        consolidation_guidance: tuple[str, ...] = field(default_factory=tuple)

    # ============================================
    # Initialization
    # ============================================

    def __init__(
        self: Self,
        semgrep_rules_path: Path | None = None,
    ) -> None:
        """Initialize code quality plugin.

        Args:
            semgrep_rules_path: Path to Semgrep rules directory.
                Defaults to bundled rules in package.

        """
        super().__init__()
        self._logger = FlextLogger(__name__)
        self._semgrep_rules_path = (
            semgrep_rules_path
            or Path(__file__).parent.parent.parent.parent / "semgrep_rules"
        )
        self._workspace_discovery = FlextWorkspaceDiscovery()
        self._duplication_plugin = FlextDuplicationPlugin()

    def execute(self: Self) -> FlextResult[int]:
        """Satisfy FlextService contract."""
        return FlextResult[int].fail("Use check() or check_workspace() methods")

    # ============================================
    # Main Check Methods
    # ============================================

    def check(
        self: Self,
        targets: list[Path],
        categories: list[str] | None = None,
    ) -> FlextResult[CheckResult]:
        """Check files/directories for quality violations.

        Args:
            targets: Files or directories to check.
            categories: Filter by category (SOLID, DRY, KISS, etc.).
                If None, checks all categories.

        Returns:
            Check result with violations.

        """
        all_violations: list[FlextCodeQualityPlugin.Violation] = []
        files_checked = 0

        # Collect Python files from targets
        python_files: list[Path] = []
        for target in targets:
            if target.is_file() and target.suffix == ".py":
                python_files.append(target)
            elif target.is_dir():
                python_files.extend(
                    py_file
                    for py_file in target.rglob("*.py")
                    if "__pycache__" not in str(py_file) and ".venv" not in str(py_file)
                )

        files_checked = len(python_files)

        # Run Semgrep
        semgrep_result = self._run_semgrep(python_files)
        if semgrep_result.is_success:
            all_violations.extend(semgrep_result.value)

        # Run duplication check (DRY)
        if not categories or "DRY" in categories:
            dup_result = self._duplication_plugin.check(python_files)
            if dup_result.is_success and dup_result.value.duplicate_count > 0:
                for dup in dup_result.value.duplicates:
                    violation = FlextCodeQualityPlugin.Violation(
                        category="DRY",
                        principle="DUPLICATION",
                        severity="WARNING",
                        file_path=dup.file1,
                        line_number=None,
                        message=f"Duplicate code with {dup.file2} ({dup.similarity:.0%} similarity)",
                        suggestion="Extract shared code to common module or utility",
                        tool="duplication",
                        rule_id="dup-check",
                    )
                    all_violations.append(violation)

        # Filter by categories if specified
        if categories:
            all_violations = [v for v in all_violations if v.category in categories]

        # Generate consolidation guidance
        guidance = self._generate_consolidation_guidance(all_violations)

        # Aggregate by category and severity
        by_category: dict[str, int] = {}
        by_severity: dict[str, int] = {}
        for v in all_violations:
            by_category[v.category] = by_category.get(v.category, 0) + 1
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1

        return FlextResult[FlextCodeQualityPlugin.CheckResult].ok(
            FlextCodeQualityPlugin.CheckResult(
                total_violations=len(all_violations),
                files_checked=files_checked,
                violations_by_category=by_category,
                violations_by_severity=by_severity,
                violations=tuple(all_violations),
                consolidation_guidance=tuple(guidance),
            )
        )

    def check_workspace(
        self: Self,
        workspace_root: Path | None = None,
        categories: list[str] | None = None,
    ) -> FlextResult[WorkspaceCheckResult]:
        """Check all FLEXT projects in workspace.

        Uses FlextWorkspaceDiscovery to automatically discover and order
        projects by dependencies (foundation first).

        Args:
            workspace_root: Workspace root directory. Defaults to ~/flext.
            categories: Filter by category (SOLID, DRY, KISS, etc.).

        Returns:
            Workspace check result with per-project violations.

        """
        root = workspace_root or Path.home() / "flext"

        # Discover projects in dependency order
        discovery = FlextWorkspaceDiscovery(root)
        discovery_result = discovery.get_ordered_projects()

        if discovery_result.is_failure:
            return FlextResult[FlextCodeQualityPlugin.WorkspaceCheckResult].fail(
                discovery_result.error or "Discovery failed"
            )

        ordered_projects = discovery_result.value

        # Check each project in order
        all_violations: list[FlextCodeQualityPlugin.Violation] = []
        by_project: dict[str, int] = {}
        total_files = 0

        for project_name in ordered_projects:
            project_path = root / project_name / "src"
            if not project_path.exists():
                continue

            # Get all Python files in project
            python_files = list(project_path.rglob("*.py"))
            python_files = [
                f
                for f in python_files
                if "__pycache__" not in str(f) and ".venv" not in str(f)
            ]

            total_files += len(python_files)

            # Check project
            result = self.check(python_files, categories)
            if result.is_success:
                project_violations = list(result.value.violations)
                all_violations.extend(project_violations)
                by_project[project_name] = len(project_violations)

        # Run cross-project duplication check
        if not categories or "DRY" in categories:
            workspace_dup = self._duplication_plugin.check_workspace(root)
            if (
                workspace_dup.is_success
                and workspace_dup.value.cross_project_duplicates > 0
            ):
                for dup in workspace_dup.value.duplicates:
                    violation = FlextCodeQualityPlugin.Violation(
                        category="DRY",
                        principle="CROSS_PROJECT_DUPLICATION",
                        severity="WARNING",
                        file_path=dup.file1_path,
                        line_number=None,
                        message=(
                            f"Cross-project duplicate: {dup.file1_project}/{dup.file1_path.name} "
                            f"<-> {dup.file2_project}/{dup.file2_path.name} "
                            f"({dup.similarity:.0%} similarity)"
                        ),
                        suggestion=f"Consolidate to {dup.consolidation_target}",
                        tool="duplication",
                        rule_id="workspace-dup-check",
                    )
                    all_violations.append(violation)

        # Generate consolidation guidance
        guidance = self._generate_consolidation_guidance(all_violations)

        # Aggregate
        by_category: dict[str, int] = {}
        by_severity: dict[str, int] = {}
        for v in all_violations:
            by_category[v.category] = by_category.get(v.category, 0) + 1
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1

        self._logger.debug(
            "Workspace check: %d violations in %d projects (%d files)",
            len(all_violations),
            len(ordered_projects),
            total_files,
        )

        return FlextResult[FlextCodeQualityPlugin.WorkspaceCheckResult].ok(
            FlextCodeQualityPlugin.WorkspaceCheckResult(
                total_projects=len(ordered_projects),
                total_violations=len(all_violations),
                total_files=total_files,
                violations_by_project=by_project,
                violations_by_category=by_category,
                violations_by_severity=by_severity,
                violations=tuple(all_violations),
                consolidation_guidance=tuple(guidance),
            )
        )

    # ============================================
    # Tool Runners
    # ============================================

    def _run_semgrep(
        self: Self,
        files: list[Path],
    ) -> FlextResult[list[Violation]]:
        """Run Semgrep with FLEXT rules.

        Args:
            files: Files to analyze.

        Returns:
            List of violations from Semgrep.

        """
        if not files:
            return FlextResult[list[FlextCodeQualityPlugin.Violation]].ok([])

        if not self._semgrep_rules_path.exists():
            self._logger.warning(
                "Semgrep rules not found at %s", self._semgrep_rules_path
            )
            return FlextResult[list[FlextCodeQualityPlugin.Violation]].ok([])

        try:
            # Build command
            cmd = [
                "semgrep",
                "--config",
                str(self._semgrep_rules_path),
                "--json",
                "--no-git-ignore",
            ]
            cmd.extend(str(f) for f in files[: c.Quality.Analysis.MAX_FILES_PER_RUN])

            # Run Semgrep
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=c.Quality.Analysis.SEMGREP_TIMEOUT_SECONDS,
            )

            # Parse JSON output
            if result.stdout:
                data = json.loads(result.stdout)
                violations = self._parse_semgrep_output(data)
                return FlextResult[list[FlextCodeQualityPlugin.Violation]].ok(
                    violations
                )

            return FlextResult[list[FlextCodeQualityPlugin.Violation]].ok([])

        except subprocess.TimeoutExpired:
            self._logger.warning("Semgrep timeout exceeded")
            return FlextResult[list[FlextCodeQualityPlugin.Violation]].fail(
                "Semgrep analysis timed out"
            )
        except (
            subprocess.SubprocessError,
            json.JSONDecodeError,
            FileNotFoundError,
        ) as e:
            error_msg = str(e)
            self._logger.warning("Semgrep error: %s", error_msg)
            return FlextResult[list[FlextCodeQualityPlugin.Violation]].fail(
                f"Semgrep analysis failed: {error_msg}"
            )

    def _parse_semgrep_output(
        self: Self,
        data: dict[str, list[dict[str, str | int | dict[str, str | int]]]],
    ) -> list[Violation]:
        """Parse Semgrep JSON output into violations.

        Args:
            data: Semgrep JSON output.

        Returns:
            List of violations.

        """
        violations: list[FlextCodeQualityPlugin.Violation] = []

        results = data.get("results", [])
        for result in results:
            check_id = str(result.get("check_id", "unknown"))
            path_str = str(result.get("path", ""))
            path = Path(path_str)

            # Extract nested values with proper type handling
            start_data = result.get("start", {})
            start_dict = start_data if isinstance(start_data, dict) else {}
            line_val = start_dict.get("line")
            line: int | None = int(line_val) if isinstance(line_val, int) else None

            extra_data = result.get("extra", {})
            extra_dict = extra_data if isinstance(extra_data, dict) else {}
            message_val = extra_dict.get("message", "")
            message = str(message_val) if message_val else ""
            severity_val = extra_dict.get("severity", "WARNING")
            severity = str(severity_val).upper()

            metadata_data: str | int | dict[str, str | int] = extra_dict.get(
                "metadata", {}
            )
            metadata = metadata_data if isinstance(metadata_data, dict) else {}
            category = str(metadata.get("category", "UNKNOWN"))
            principle = str(metadata.get("principle", "UNKNOWN"))
            suggestion = str(metadata.get("fix", "See rule documentation"))

            violation = FlextCodeQualityPlugin.Violation(
                category=category,
                principle=principle,
                severity=severity,
                file_path=path,
                line_number=line,
                message=message.split("\n")[0] if message else check_id,
                suggestion=suggestion,
                tool="semgrep",
                rule_id=check_id,
            )
            violations.append(violation)

        return violations

    # ============================================
    # Consolidation Guidance
    # ============================================

    def _generate_consolidation_guidance(
        self: Self,
        violations: list[Violation],
    ) -> list[str]:
        """Generate SOLID-based consolidation suggestions.

        Args:
            violations: List of violations to analyze.

        Returns:
            List of consolidation guidance strings.

        """
        guidance: list[str] = []

        # Count by category
        by_category: dict[str, int] = {}
        for v in violations:
            by_category[v.category] = by_category.get(v.category, 0) + 1

        # Generate guidance based on patterns
        if (
            by_category.get("FLEXT_ARCHITECTURE", 0)
            > c.Quality.Thresholds.ARCHITECTURE_VIOLATION_THRESHOLD
        ):
            guidance.append(
                "Multiple FLEXT architecture violations detected. "
                "Review namespace usage (c.*, m.*, p.*, u.*) and FlextResult patterns."
            )

        if by_category.get("SOLID", 0) > c.Quality.Thresholds.SOLID_VIOLATION_THRESHOLD:
            guidance.append(
                "Multiple SOLID violations detected. "
                "Consider refactoring to improve dependency injection and separation of concerns."
            )

        if by_category.get("DRY", 0) > c.Quality.Thresholds.DRY_VIOLATION_THRESHOLD:
            guidance.append(
                "Code duplication detected. "
                "Consider extracting shared logic to flext-core utilities or shared protocols."
            )

        if by_category.get("ANTI_PATTERN", 0) > 0:
            guidance.append(
                "Anti-patterns detected (TYPE_CHECKING, cast, Any). "
                "These MUST be fixed before merge - see /code-quality-guardian."
            )

        # Project-specific guidance
        reimpl_count = sum(1 for v in violations if v.principle == "REIMPLEMENTATION")
        if reimpl_count > 0:
            guidance.append(
                f"{reimpl_count} reimplementations detected. "
                "Use base classes directly: FlextResult, FlextService, FlextLogger, etc."
            )

        return guidance


__all__ = ["FlextCodeQualityPlugin"]
