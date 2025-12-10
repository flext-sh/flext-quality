"""FLEXT Quality Analyzer - Main analysis orchestrator with SOLID delegation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import uuid
from pathlib import Path
from typing import ClassVar, TypedDict
from uuid import UUID, uuid4

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)
from pydantic import BaseModel, Field, PrivateAttr

from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .external_backend import FlextQualityExternalBackend
from .models import FlextQualityModels

# =====================================================================
# Type Definitions - Replace Any/object with proper types
# =====================================================================


# =====================================================================
# Backend Issue Models - Validação Pydantic para dados externos
# =====================================================================


class BanditIssueModel(BaseModel):
    """Validado issue do Bandit (security analysis)."""

    line_number: int = Field(default=1, ge=1)
    severity: str = Field(default="MEDIUM")
    message: str = Field(default="Security issue detected")
    test_id: str = Field(default="")


class VultureIssueModel(BaseModel):
    """Validado issue do Vulture (dead code analysis)."""

    line_number: int = Field(default=1, ge=1)
    type: str = Field(default="unused variable")
    message: str = Field(default="Dead code detected")


class DuplicationIssueModel(BaseModel):
    """Validated duplication issue."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    analysis_id: str = Field(default_factory=lambda: str(uuid4()))
    file_path: str = Field(description="File path with duplication")
    line_number: int | None = Field(default=None, ge=1)
    issue_type: str = Field(default="duplication")
    severity: str = Field(default="medium")
    message: str = Field(
        default="Duplicate code detected",
        description="Issue description",
    )
    rule_id: str | None = Field(default=None)


class FileMetricsModel(BaseModel):
    """Validated file-level metrics model."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    file_path: str = Field(default="")
    lines_of_code: int = Field(default=0, ge=0)
    complexity_score: float = Field(default=0.0, ge=0)
    functions_count: int = Field(default=0, ge=0)
    classes_count: int = Field(default=0, ge=0)
    issues: list[FlextQualityModels.CodeIssue] = Field(default_factory=list)


# Legacy TypedDict aliases for backward compatibility (remove in v1.0)
class FileMetricsDict(TypedDict, total=False):
    """DEPRECATED: Use FileMetricsModel instead."""

    id: str
    file_path: str
    lines_of_code: int
    complexity_score: float
    functions_count: int
    classes_count: int
    issues: list[FlextQualityModels.CodeIssue]


class DuplicationIssueDict(TypedDict, total=False):
    """DEPRECATED: Use DuplicationIssueModel instead."""

    id: str
    analysis_id: str
    file_path: str
    line_number: int
    issue_type: str
    severity: str
    message: str
    rule_id: str


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
    file_metrics: list[FileMetricsModel] = Field(default_factory=list)
    analysis_errors: int = Field(default=0, ge=0)


# =====================================================================
# Main Analyzer - Orchestrator Pattern with SOLID Delegation
# =====================================================================


class FlextQualityAnalyzer(FlextService[FlextQualityModels.AnalysisResults]):
    """Main quality analyzer orchestrating focused analysis utilities."""

    auto_execute: ClassVar[bool] = False
    project_path: Path = Path()
    _analyzer_config: FlextQualityConfig = PrivateAttr()
    _analyzer_logger: FlextLogger = PrivateAttr()
    _current_results: FlextQualityModels.AnalysisResults | None = PrivateAttr(
        default=None,
    )

    def __init__(
        self,
        project_path: str | Path | None = None,
        config: FlextQualityConfig | None = None,
        **_data: object,
    ) -> None:
        """Initialize analyzer.

        Args:
            project_path: Path to analyze. If None, uses current directory.
            config: Optional quality configuration.
            **_data: Additional keyword arguments (ignored, for FlextService compatibility).

        """
        super().__init__()
        self.project_path = Path(project_path) if project_path is not None else Path()
        self._analyzer_config = config if config is not None else FlextQualityConfig()
        self._analyzer_logger = FlextLogger(__name__)
        self._current_results = None

    @property
    def analyzer_config(self) -> FlextQualityConfig:
        """Access analyzer configuration (read-only)."""
        return self._analyzer_config

    @property
    def analyzer_logger(self) -> FlextLogger:
        """Access analyzer logger (read-only)."""
        return self._analyzer_logger

    def execute(
        self,
        **_kwargs: object,
    ) -> FlextResult[FlextQualityModels.AnalysisResults]:
        """Execute analyzer service - override from FlextService."""
        _ = _kwargs
        return self.analyze_project()

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
            python_files,
            options,
            self.analyzer_logger,
        )
        if metrics_result.is_failure:
            return FlextResult.fail(f"File analysis failed: {metrics_result.error}")

        metrics_data = metrics_result.value

        # Analyze duplications
        duplication_issues: list[DuplicationIssueModel] = []
        if options.include_duplicates and len(python_files) > 1:
            dup_result = self._DuplicationAnalyzer.analyze(python_files)
            if dup_result.is_success:
                duplication_issues = dup_result.value

        # Create final results
        results_result = self._ResultsBuilder.create_analysis_results(
            metrics_data,
            duplication_issues,
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
                    file_path,
                    options,
                )
                if result.is_success:
                    metrics = result.value
                    file_metrics.append(metrics)
                    total_lines += metrics.lines_of_code
                else:
                    analysis_errors += 1
                    logger.warning(f"Failed to analyze {file_path}: {result.error}")

            return FlextResult.ok(
                FileMetricsData(
                    total_files=len(file_metrics),
                    total_lines=total_lines,
                    file_metrics=file_metrics,
                    analysis_errors=analysis_errors,
                ),
            )

        @staticmethod
        def analyze_single_file(
            file_path: Path,
            options: AnalysisOptions,
        ) -> FlextResult[FileMetricsModel]:
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
                        file_path,
                        complexity_score,
                    )
                    if options.include_complexity
                    else [],
                )
                issues.extend(
                    FlextQualityAnalyzer._DeadCodeAnalyzer.analyze(tree, file_path)
                    if options.include_dead_code
                    else [],
                )

                # Create validated FileMetricsModel - NO DICT CONVERSION
                metrics = FileMetricsModel(
                    id=str(uuid.uuid4()),
                    file_path=str(file_path),
                    lines_of_code=len(content.splitlines()),
                    complexity_score=complexity_score,
                    functions_count=len([
                        n
                        for n in ast.walk(tree)
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ]),
                    classes_count=len([
                        n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)
                    ]),
                    issues=issues,
                )
                return FlextResult.ok(metrics)
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
            file_path: Path,
            complexity_score: float,
        ) -> list[FlextQualityModels.CodeIssue]:
            """Find complexity issues."""
            if (
                complexity_score
                > FlextQualityConstants.Quality.Complexity.MAX_COMPLEXITY
            ):
                return [
                    FlextQualityModels.CodeIssue(
                        id=uuid4(),  # complexity issue{file_path.name}",
                        analysis_id=uuid4(),
                        file_path=str(file_path),
                        line_number=1,
                        issue_type=FlextQualityModels.IssueType.HIGH_COMPLEXITY,
                        severity=FlextQualityModels.IssueSeverity.MEDIUM,
                        message=f"High complexity: {complexity_score:.1f}",
                        rule_id="complexity_check",
                    ),
                ]
            return []

    class _SecurityAnalyzer:
        """Single responsibility: Analyze security issues."""

        backend = FlextQualityExternalBackend()

        @staticmethod
        def analyze(
            tree: ast.AST,
            file_path: Path,
        ) -> list[FlextQualityModels.CodeIssue]:
            r"""Analyze security issues using Bandit backend."""
            # Reserved for future AST-based analysis
            _ = tree  # Reserved for future use
            try:
                result = (
                    FlextQualityAnalyzer._SecurityAnalyzer.backend.analyze_with_tool(
                        "",
                        tool="bandit",
                    )
                )
                if not result.is_success or "issues" not in result.value:
                    return []

                # Validate each issue with BanditIssueModel - fail-fast on invalid data
                validated_issues = []
                issues = result.value["issues"]
                if not isinstance(issues, list):
                    return []
                for data in issues:
                    validated = BanditIssueModel.model_validate(data)
                    # Convert validated Bandit issue to CodeIssue
                    validated_issues.append(
                        FlextQualityModels.CodeIssue(
                            id=uuid4(),
                            analysis_id=uuid4(),
                            file_path=str(file_path),
                            line_number=validated.line_number,
                            issue_type=FlextQualityModels.IssueType.SECURITY_VULNERABILITY,
                            severity=validated.severity,
                            message=validated.message,
                            rule_id=validated.test_id,
                        ),
                    )
                return validated_issues
            except Exception as e:
                # Log the error and allow graceful degradation
                logger = FlextLogger(__name__)
                logger.warning("Security analysis with Bandit failed: %s", e)
                # Return empty list - security analysis is best-effort
                return []

    class _DeadCodeAnalyzer:
        """Single responsibility: Analyze dead code."""

        backend = FlextQualityExternalBackend()

        @staticmethod
        def analyze(
            tree: ast.AST,
            file_path: Path,
        ) -> list[FlextQualityModels.CodeIssue]:
            """Analyze dead code - external backend only."""
            # AST-based analysis not implemented - use external backend
            _ = tree  # Reserved for future AST-based analysis
            try:
                result = (
                    FlextQualityAnalyzer._DeadCodeAnalyzer.backend.analyze_with_tool(
                        "",
                        tool="vulture",
                    )
                )
                if not result.is_success or "issues" not in result.value:
                    return []

                # Validate each issue with VultureIssueModel - fail-fast on invalid data
                validated_issues = []
                issues = result.value["issues"]
                if not isinstance(issues, list):
                    return []
                for data in issues:
                    validated = VultureIssueModel.model_validate(data)
                    # Convert validated Vulture issue to CodeIssue
                    validated_issues.append(
                        FlextQualityModels.CodeIssue(
                            id=uuid4(),
                            analysis_id=uuid4(),
                            file_path=str(file_path),
                            line_number=validated.line_number,
                            issue_type=FlextQualityModels.IssueType.UNUSED_CODE,
                            severity=FlextQualityModels.IssueSeverity.LOW,
                            message=f"Unused {validated.type}",
                            rule_id="dead_code",
                        ),
                    )
                return validated_issues
            except Exception as e:
                logger = FlextLogger(__name__)
                logger.debug("Dead code analysis with Vulture failed: %s", e)
                # Return empty list - dead code analysis is best-effort
                return []

    class _DuplicationAnalyzer:
        """Single responsibility: Analyze code duplications."""

        @staticmethod
        def analyze(
            python_files: list[Path],
        ) -> FlextResult[list[DuplicationIssueModel]]:
            """Analyze duplications across files."""
            try:
                min_size = FlextQualityConstants.Quality.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK
                file_contents = {
                    pf: pf.read_text(encoding="utf-8")
                    for pf in python_files
                    if pf.is_file()
                    and (c := pf.read_text(encoding="utf-8"))
                    and len(c.strip()) > min_size
                }

                file_list = list(file_contents.keys())
                # Create validated DuplicationIssueModel instances - NO DICT CONVERSION
                issues: list[DuplicationIssueModel] = [
                    DuplicationIssueModel(
                        id=f"dup_{f1.name}_{f2.name}",
                        analysis_id=str(uuid.uuid4()),
                        file_path=str(f1),
                        line_number=None,
                        issue_type="duplicate_code",
                        severity="medium",
                        message=f"Duplication: {f1.name} ↔ {f2.name}",
                        rule_id="duplication_check",
                    )
                    for i, f1 in enumerate(file_list)
                    for f2 in file_list[i + 1 :]
                    if FlextQualityAnalyzer._DuplicationAnalyzer.has_duplication(
                        file_contents[f1],
                        file_contents[f2],
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
                return (
                    similarity
                    > FlextQualityConstants.Quality.Analysis.SIMILARITY_THRESHOLD
                )
            return False

    class _ResultsBuilder:
        """Single responsibility: Build final analysis results."""

        @staticmethod
        def create_analysis_results(
            metrics_data: FileMetricsData,
            duplication_issues: list[DuplicationIssueModel],
        ) -> FlextResult[FlextQualityModels.AnalysisResults]:
            """Create final analysis results."""
            try:
                # Aggregate all issues
                all_issues: list[FlextQualityModels.CodeIssue] = []
                for metrics in metrics_data.file_metrics:
                    if metrics.issues:
                        all_issues.extend(metrics.issues)

                # Convert duplication issues to CodeIssue objects
                all_issues.extend([
                    FlextQualityModels.CodeIssue(
                        id=UUID(str(dup.id)),
                        analysis_id=UUID(str(dup.analysis_id)),
                        file_path=dup.file_path,
                        line_number=dup.line_number,
                        issue_type=(FlextQualityModels.IssueType.DUPLICATE_CODE),
                        severity=(FlextQualityModels.IssueSeverity.MEDIUM),
                        message=dup.message,
                        rule_id=dup.rule_id,
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

                # Calculate scores from actual metrics
                complexity_scores: list[float] = [
                    metric.complexity_score for metric in metrics_data.file_metrics
                ]

                avg_complexity = (
                    sum(complexity_scores) / len(complexity_scores)
                    if complexity_scores
                    else 0.0
                )
                overall_score = max(
                    0.0,
                    100.0 - (security_count * 10 + complexity_count * 5),
                )

                # Build recommendations based on actual issues found
                recommendations: list[str] = []
                if security_count > 0:
                    recommendations.append("Address security vulnerabilities")
                if complexity_count > 0:
                    recommendations.append("Refactor complex functions")
                if dead_code_count > 0:
                    recommendations.append("Remove unused code")
                if dup_count > 0:
                    recommendations.append("Eliminate duplications")

                return FlextResult.ok(
                    FlextQualityModels.AnalysisResults(
                        issues=[
                            {"type": str(i.issue_type), "message": i.message}
                            for i in all_issues
                        ],
                        metrics={
                            "total_issues": len(all_issues),
                            "security_issues": security_count,
                            "complexity_issues": complexity_count,
                            "dead_code_issues": dead_code_count,
                            "duplication_issues": dup_count,
                        },
                        recommendations=recommendations,
                        overall_score=overall_score,
                        complexity_score=max(0.0, 100.0 - (avg_complexity * 5)),
                        security_score=max(0.0, 100.0 - (security_count * 10)),
                        coverage_score=max(0.0, 100.0 - (dead_code_count * 8)),
                        quality_grade="B",
                    ),
                )
            except Exception as e:
                return FlextResult.fail(f"Results creation error: {e}")
