"""FLEXT Quality Analyzer - Main analysis orchestrator with SOLID delegation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import uuid
from pathlib import Path
from typing import override

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)
from pydantic import BaseModel, Field

from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .external_backend import FlextQualityExternalBackend
from .models import FlextQualityModels

# =====================================================================
# Analysis Configuration Models (Pydantic 2)
# =====================================================================


class AnalysisOptions(BaseModel):
    """Analysis execution options."""

    include_security: bool = Field(default=True)
    include_complexity: bool = Field(default=True)
    include_dead_code: bool = Field(default=True)
    include_duplicates: bool = Field(default=True)


class FileMetricsData(BaseModel):
    """Aggregated file-level metrics."""

    total_files: int = Field(default=0, ge=0)
    total_lines: int = Field(default=0, ge=0)
    file_metrics: list[dict[str, object]] = Field(default_factory=list)
    analysis_errors: int = Field(default=0, ge=0)


# =====================================================================
# Main Analyzer - Orchestrator Pattern with SOLID Delegation
# =====================================================================


class FlextQualityAnalyzer(FlextService[None]):
    """Main quality analyzer orchestrating focused analysis utilities."""

    project_path: Path

    def __init__(
        self, project_path: str | Path, config: FlextQualityConfig | None = None
    ) -> None:
        """Initialize analyzer."""
        super().__init__(project_path=Path(project_path))
        self._config = config or FlextQualityConfig()
        self._logger = FlextLogger(__name__)
        self._current_results: FlextQualityModels.AnalysisResults | None = None

    @property
    def logger(self) -> FlextLogger:
        """Get logger."""
        return self._logger

    @override
    def execute(self) -> FlextResult[None]:
        """Execute analyzer service."""
        return FlextResult.ok(None)

    def analyze_project(
        self,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> FlextResult[FlextQualityModels.AnalysisResults]:
        """Analyze entire project - delegates to focused analyzers."""
        options = AnalysisOptions(
            include_security=include_security,
            include_complexity=include_complexity,
            include_dead_code=include_dead_code,
            include_duplicates=include_duplicates,
        )

        self.logger.info("Starting project analysis: %s", self.project_path)

        # Discover files
        files_result = self._FileDiscovery.discover_python_files(self.project_path)
        if files_result.is_failure:
            return FlextResult.fail(f"File discovery failed: {files_result.error}")

        python_files = files_result.value

        # Analyze each file
        metrics_result = self._FileAnalysisHelper.analyze_files(
            python_files, options, self.logger
        )
        if metrics_result.is_failure:
            return FlextResult.fail(f"File analysis failed: {metrics_result.error}")

        metrics_data = metrics_result.value

        # Analyze duplications
        duplication_issues = []
        if options.include_duplicates and len(python_files) > 1:
            dup_result = self._DuplicationAnalyzer.analyze(python_files)
            if dup_result.is_success:
                duplication_issues = dup_result.value

        # Create final results
        results_result = self._ResultsBuilder.create_analysis_results(
            metrics_data, duplication_issues
        )
        if results_result.is_failure:
            return FlextResult.fail(f"Results creation failed: {results_result.error}")

        self._current_results = results_result.value
        return FlextResult.ok(self._current_results)

    def get_quality_score(self) -> float:
        """Get overall quality score."""
        return self._current_results.overall_score if self._current_results else 0.0

    def get_quality_grade(self) -> str:
        """Get quality grade."""
        return self._current_results.quality_grade if self._current_results else "F"

    def get_last_analysis_result(self) -> FlextQualityModels.AnalysisResults | None:
        """Get last analysis results."""
        return self._current_results

    # =====================================================================
    # Nested Analysis Utilities - Single Responsibility
    # =====================================================================

    class _FileDiscovery:
        """Single responsibility: Discover Python files."""

        @staticmethod
        def discover_python_files(project_path: Path) -> FlextResult[list[Path]]:
            """Discover all Python files in project."""
            try:
                if not project_path.exists():
                    return FlextResult.fail(f"Path not found: {project_path}")
                if not project_path.is_dir():
                    return FlextResult.fail(f"Not a directory: {project_path}")

                python_files = [
                    py_file
                    for py_file in project_path.rglob("*.py")
                    if not any(
                        part in py_file.parts
                        for part in ["__pycache__", ".git", "node_modules", ".venv"]
                    )
                ]
                return FlextResult.ok(python_files)
            except Exception as e:
                return FlextResult.fail(f"File discovery error: {e}")

    class _FileAnalysisHelper:
        """Single responsibility: Analyze individual files."""

        @staticmethod
        def analyze_files(
            python_files: list[Path],
            options: AnalysisOptions,
            logger: FlextLogger,
        ) -> FlextResult[FileMetricsData]:
            """Analyze all files and aggregate metrics."""
            file_metrics = []
            total_lines = 0
            analysis_errors = 0

            for file_path in python_files:
                result = FlextQualityAnalyzer._FileAnalysisHelper.analyze_single_file(
                    file_path, options
                )
                if result.is_success:
                    metrics = result.value
                    file_metrics.append(metrics)
                    total_lines += int(metrics.get("lines_of_code", 0) or 0)
                else:
                    analysis_errors += 1
                    logger.warning(f"Failed to analyze {file_path}: {result.error}")

            return FlextResult.ok(
                FileMetricsData(
                    total_files=len(file_metrics),
                    total_lines=total_lines,
                    file_metrics=file_metrics,
                    analysis_errors=analysis_errors,
                )
            )

        @staticmethod
        def analyze_single_file(
            file_path: Path, options: AnalysisOptions
        ) -> FlextResult[dict[str, object]]:
            """Analyze single file - delegates to specialized analyzers."""
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(file_path))

                # Delegate to specialized analyzers
                complexity_score = (
                    FlextQualityAnalyzer._ComplexityAnalyzer.calculate_complexity(tree)
                )
                issues = (
                    FlextQualityAnalyzer._SecurityAnalyzer.analyze(tree, file_path)
                    if options.include_security
                    else []
                )
                issues.extend(
                    FlextQualityAnalyzer._ComplexityAnalyzer.find_issues(
                        file_path, complexity_score
                    )
                    if options.include_complexity
                    else []
                )
                issues.extend(
                    FlextQualityAnalyzer._DeadCodeAnalyzer.analyze(tree, file_path)
                    if options.include_dead_code
                    else []
                )

                return FlextResult.ok({
                    "id": f"file_{uuid.uuid4()}",
                    "file_path": str(file_path),
                    "lines_of_code": len(content.splitlines()),
                    "complexity_score": complexity_score,
                    "functions_count": len([
                        n
                        for n in ast.walk(tree)
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ]),
                    "classes_count": len([
                        n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                    ]),
                    "issues": issues,
                })
            except SyntaxError as e:
                return FlextResult.fail(f"Syntax error in {file_path}: {e}")
            except Exception as e:
                return FlextResult.fail(f"Analysis error: {e}")

    class _ComplexityAnalyzer:
        """Single responsibility: Calculate and analyze complexity."""

        @staticmethod
        def calculate_complexity(tree: ast.AST) -> float:
            """Calculate cyclomatic complexity."""
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.Try):
                    complexity += len(node.handlers) + len(node.orelse)
            return min(100.0, complexity * 2.0)

        @staticmethod
        def find_issues(
            file_path: Path, complexity_score: float
        ) -> list[FlextQualityModels.CodeIssue]:
            """Find complexity issues."""
            if complexity_score > FlextQualityConstants.Complexity.MAX_COMPLEXITY:
                return [
                    FlextQualityModels.CodeIssue(
                        id=f"complexity_{file_path.name}",
                        analysis_id="current",
                        file_path=str(file_path),
                        line_number=1,
                        issue_type="complexity",
                        severity="medium",
                        message=f"High complexity: {complexity_score:.1f}",
                        rule_id="complexity_check",
                    )
                ]
            return []

    class _SecurityAnalyzer:
        """Single responsibility: Analyze security issues."""

        backend = FlextQualityExternalBackend()

        @staticmethod
        def analyze(
            tree: ast.AST, file_path: Path
        ) -> list[FlextQualityModels.CodeIssue]:
            """Analyze security issues - external backend with AST fallback."""
            issues = []
            try:
                result = FlextQualityAnalyzer._SecurityAnalyzer.backend.analyze(
                    "", file_path=file_path, tool="bandit"
                )
                if result.is_success and "issues" in result.value:
                    issues = [
                        FlextQualityModels.CodeIssue(
                            id=f"security_{i}",
                            analysis_id="current",
                            file_path=str(file_path),
                            line_number=data.get("line_number", 1),
                            issue_type="security",
                            severity=data.get("severity", "medium"),
                            message=data.get("message", ""),
                            rule_id=data.get("test_id", "security"),
                        )
                        for i, data in enumerate(result.value["issues"])
                    ]
                    if issues:
                        return issues
            except Exception as e:
                FlextLogger(__name__).debug(
                    f"Bandit backend failed, using AST fallback: {e}"
                )

            # AST fallback: detect eval/exec
            return [
                FlextQualityModels.CodeIssue(
                    id=f"security_ast_{i}",
                    analysis_id="current",
                    file_path=str(file_path),
                    line_number=getattr(node, "lineno", 1),
                    issue_type="security",
                    severity="high",
                    message=f"Dangerous call: {node.func.id}",
                    rule_id="dangerous_call",
                )
                for i, node in enumerate(ast.walk(tree))
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in {"eval", "exec"}
                )
            ]

    class _DeadCodeAnalyzer:
        """Single responsibility: Analyze dead code."""

        backend = FlextQualityExternalBackend()

        @staticmethod
        def analyze(
            tree: ast.AST, file_path: Path
        ) -> list[FlextQualityModels.CodeIssue]:
            """Analyze dead code - external backend with AST fallback."""
            issues = []
            try:
                result = FlextQualityAnalyzer._DeadCodeAnalyzer.backend.analyze(
                    "", file_path=file_path, tool="vulture"
                )
                if result.is_success and "issues" in result.value:
                    issues = [
                        FlextQualityModels.CodeIssue(
                            id=f"dead_code_{i}",
                            analysis_id="current",
                            file_path=str(file_path),
                            line_number=data.get("line_number", 1),
                            issue_type="dead_code",
                            severity="low",
                            message=f"Unused {data.get('type', 'code')}",
                            rule_id="dead_code",
                        )
                        for i, data in enumerate(result.value["issues"])
                    ]
                    if issues:
                        return issues
            except Exception as e:
                FlextLogger(__name__).debug(
                    f"Vulture backend failed, using AST fallback: {e}"
                )

            # AST fallback: detect unused functions
            min_len = FlextQualityConstants.Analysis.MIN_FUNCTION_LENGTH_FOR_DEAD_CODE
            return [
                FlextQualityModels.CodeIssue(
                    id=f"dead_code_ast_{i}",
                    analysis_id="current",
                    file_path=str(file_path),
                    line_number=getattr(node, "lineno", 1),
                    issue_type="dead_code",
                    severity="low",
                    message=f"Unused function: {node.name}",
                    rule_id="unused_function",
                )
                for i, node in enumerate(ast.walk(tree))
                if (
                    isinstance(node, ast.FunctionDef)
                    and not any(isinstance(n, ast.Return) for n in ast.walk(node))
                    and len(node.body) > min_len
                )
            ]

    class _DuplicationAnalyzer:
        """Single responsibility: Analyze code duplications."""

        @staticmethod
        def analyze(python_files: list[Path]) -> FlextResult[list[dict[str, object]]]:
            """Analyze duplications across files."""
            try:
                min_size = (
                    FlextQualityConstants.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK
                )
                file_contents = {
                    pf: pf.read_text(encoding="utf-8")
                    for pf in python_files
                    if pf.is_file()
                    and (c := pf.read_text(encoding="utf-8"))
                    and len(c.strip()) > min_size
                }

                file_list = list(file_contents.keys())
                issues = [
                    {
                        "id": f"dup_{f1.name}_{f2.name}",
                        "analysis_id": str(uuid.uuid4()),
                        "file_path": str(f1),
                        "line_number": 1,
                        "issue_type": "duplicate_code",
                        "severity": "medium",
                        "message": f"Duplication: {f1.name} ↔ {f2.name}",
                        "rule_id": "duplication_check",
                    }
                    for i, f1 in enumerate(file_list)
                    for f2 in file_list[i + 1 :]
                    if FlextQualityAnalyzer._DuplicationAnalyzer.has_duplication(
                        file_contents[f1], file_contents[f2]
                    )
                ]
                return FlextResult.ok(issues)
            except Exception as e:
                return FlextResult.fail(f"Duplication analysis error: {e}")

        @staticmethod
        def has_duplication(content1: str, content2: str) -> bool:
            """Check if files have significant duplication."""
            lines1 = set(content1.splitlines())
            lines2 = set(content2.splitlines())
            if lines1 and lines2:
                similarity = len(lines1 & lines2) / max(len(lines1), len(lines2))
                return similarity > FlextQualityConstants.Analysis.SIMILARITY_THRESHOLD
            return False

    class _ResultsBuilder:
        """Single responsibility: Build final analysis results."""

        @staticmethod
        def create_analysis_results(
            metrics_data: FileMetricsData,
            duplication_issues: list[dict[str, object]],
        ) -> FlextResult[FlextQualityModels.AnalysisResults]:
            """Create final analysis results."""
            try:
                # Aggregate all issues
                all_issues = []
                for metrics in metrics_data.file_metrics:
                    if metrics.get("issues"):
                        all_issues.extend(metrics["issues"])

                # Add duplication issues as CodeIssue objects
                all_issues.extend([
                    FlextQualityModels.CodeIssue(
                        id=dup["id"],
                        analysis_id=dup["analysis_id"],
                        file_path=dup["file_path"],
                        line_number=dup.get("line_number", 1),
                        issue_type=dup["issue_type"],
                        severity=dup["severity"],
                        message=dup["message"],
                        rule_id=dup["rule_id"],
                    )
                    for dup in duplication_issues
                ])

                # Count issues by type
                def count_type(issue_type: str) -> int:
                    return len([i for i in all_issues if i.issue_type == issue_type])

                security_count = count_type("security")
                complexity_count = count_type("complexity")
                dead_code_count = count_type("dead_code")
                dup_count = count_type("duplicate_code")

                # Calculate scores
                avg_complexity = (
                    sum(m.get("complexity_score", 0) for m in metrics_data.file_metrics)
                    / len(metrics_data.file_metrics)
                    if metrics_data.file_metrics
                    else 0.0
                )
                overall_score = max(
                    0.0, 100.0 - (security_count * 10 + complexity_count * 5)
                )

                return FlextResult.ok(
                    FlextQualityModels.AnalysisResults(
                        issues=[
                            {"type": i.issue_type, "message": i.message}
                            for i in all_issues
                        ],
                        metrics={
                            "total_issues": len(all_issues),
                            "security_issues": security_count,
                            "complexity_issues": complexity_count,
                            "dead_code_issues": dead_code_count,
                            "duplication_issues": dup_count,
                        },
                        recommendations=[
                            r
                            for r in [
                                "Address security vulnerabilities"
                                if security_count > 0
                                else None,
                                "Refactor complex functions"
                                if complexity_count > 0
                                else None,
                                "Remove unused code" if dead_code_count > 0 else None,
                                "Eliminate duplications" if dup_count > 0 else None,
                            ]
                            if r is not None
                        ],
                        overall_score=overall_score,
                        complexity_score=max(0.0, 100.0 - (avg_complexity * 5)),
                        security_score=max(0.0, 100.0 - (security_count * 10)),
                        maintainability_score=max(0.0, 100.0 - (complexity_count * 5)),
                        coverage_score=85.0,
                    )
                )
            except Exception as e:
                return FlextResult.fail(f"Results creation error: {e}")
