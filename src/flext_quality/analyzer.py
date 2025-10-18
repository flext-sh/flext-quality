"""FLEXT Quality Analyzer - Main analysis engine following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import uuid
from pathlib import Path

from flext_core import (
    FlextBus,
    FlextContainer,
    FlextContext,
    FlextLogger,
    FlextResult,
    FlextService,
)
from pydantic import Field

from .config import FlextQualityConfig
from .constants import FlextQualityConstants
from .external_backend import FlextQualityExternalBackend
from .models import FlextQualityModels


class FlextQualityAnalyzer(FlextService[None]):
    """Main quality analyzer following FLEXT patterns with SOLID principles.

    Single responsibility: Orchestrate quality analysis using composition.
    Delegates specific analysis tasks to focused helper methods and external libraries.
    """

    project_path: Path = Field(..., description="Path to the project to analyze")

    def __init__(
        self, project_path: str | Path, config: FlextQualityConfig | None = None
    ) -> None:
        """Initialize analyzer with project path and configuration.

        Args:
            project_path: Path to the project to analyze
            config: Optional FlextQualityConfig instance. If None, creates default instance.

        """
        # Initialize with project_path for flext-core service
        super().__init__(project_path=Path(project_path))

        # Complete flext-core integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._logger = FlextLogger(__name__)

        self._config = config or FlextQualityConfig()
        self._current_results: FlextQualityModels.AnalysisResults | None = None

        # Initialize external backends for delegation (SOLID: composition)
        self._external_backend = FlextQualityExternalBackend()

    @property
    def logger(self) -> FlextLogger:
        """Get the logger instance."""
        return self._logger

    @property
    def container(self) -> FlextContainer:
        """Get the container instance."""
        return self._container

    def execute(self) -> FlextResult[None]:
        """Execute the analyzer service."""
        return FlextResult.ok(None)

    def analyze_project(
        self,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> FlextResult[FlextQualityModels.AnalysisResults]:
        """Analyze entire project for quality metrics and issues.

        Delegates to specialized helper methods for each analysis type.
        Applies SOLID principles through focused, single-responsibility methods.

        Args:
            include_security: Whether to include security analysis.
            include_complexity: Whether to include complexity analysis.
            include_dead_code: Whether to include dead code detection.
            include_duplicates: Whether to include duplicate code detection.

        Returns:
            AnalysisResults containing analysis results including metrics and issues.

        """
        self.logger.info("Starting project analysis: %s", self.project_path)

        # Emit analysis start event
        if self._bus is not None and hasattr(self._bus, "publish"):
            self._bus.publish(
                "quality.analysis.started",
                {
                    "project_path": str(self.project_path),
                    "config": self._config.get_analysis_config(),
                },
            )

        # Delegate file discovery to focused helper method
        python_files_result = self._discover_python_files()
        if python_files_result.is_failure:
            return FlextResult.fail(f"File discovery failed: {python_files_result.error}")

        python_files = python_files_result.value

        # Analyze each file using specialized analysis methods
        file_metrics: list[FlextQualityModels.FileAnalysisResult] = []
        total_lines = 0
        analysis_errors = 0

        for file_path in python_files:
            metrics_result = self._analyze_single_file(
                file_path,
                include_security=include_security,
                include_complexity=include_complexity,
                include_dead_code=include_dead_code,
            )
            if metrics_result.is_success:
                metrics = metrics_result.value
                file_metrics.append(metrics)
                total_lines += metrics.lines_of_code or 0
            else:
                analysis_errors += 1
                self.logger.warning(f"Failed to analyze {file_path}: {metrics_result.error}")

        # Delegate duplication analysis to specialized method
        duplication_issues = []
        if include_duplicates and len(python_files) > 1:
            duplication_result = self._analyze_duplications(python_files)
            if duplication_result.is_success:
                duplication_issues = duplication_result.value

        # Delegate metrics calculation to specialized method
        overall_metrics_result = self._calculate_overall_metrics(file_metrics, total_lines)
        if overall_metrics_result.is_failure:
            return FlextResult.fail(f"Metrics calculation failed: {overall_metrics_result.error}")

        # Collect all issues from different analysis types
        all_issues = []
        for metrics in file_metrics:
            if hasattr(metrics, 'issues') and metrics.issues:
                all_issues.extend(metrics.issues)

        # Convert duplication issues to standardized format
        for dup_issue in duplication_issues:
            issue = FlextQualityModels.CodeIssue(
                id=dup_issue["id"],
                analysis_id=dup_issue["analysis_id"],
                file_path=dup_issue["file_path"],
                line_number=dup_issue.get("line_number", 1),
                issue_type=dup_issue["issue_type"],
                severity=dup_issue["severity"],
                message=dup_issue["message"],
                rule_id=dup_issue["rule_id"],
            )
            all_issues.append(issue)

        # Delegate results creation to specialized method
        analysis_results_result = self._create_analysis_results(
            overall_metrics_result.value, all_issues
        )
        if analysis_results_result.is_failure:
            return FlextResult.fail(f"Results creation failed: {analysis_results_result.error}")

        self._current_results = analysis_results_result.value

        # Emit analysis completion event
        if self._bus is not None and hasattr(self._bus, "publish"):
            self._bus.publish(
                "quality.analysis.completed",
                {
                    "project_path": str(self.project_path),
                    "files_analyzed": len(file_metrics),
                    "total_issues": len(all_issues),
                    "overall_score": self._current_results.overall_score,
                },
            )

        return FlextResult.ok(self._current_results)

    def _discover_python_files(self) -> FlextResult[list[Path]]:
        """Discover all Python files in the project.

        Single responsibility: File discovery with proper filtering.
        """
        try:
            if not self.project_path.exists():
                return FlextResult.fail(f"Project path does not exist: {self.project_path}")

            if not self.project_path.is_dir():
                return FlextResult.fail(f"Project path is not a directory: {self.project_path}")

            # Use pathlib for efficient file discovery
            python_files = [
                py_file for py_file in self.project_path.rglob("*.py")
                if not any(part in py_file.parts for part in ["__pycache__", ".git", "node_modules", ".venv"])
            ]

            return FlextResult.ok(python_files)

        except Exception as e:
            return FlextResult.fail(f"File discovery failed: {e}")

    def _analyze_single_file(
        self,
        file_path: Path,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
    ) -> FlextResult[FlextQualityModels.FileAnalysisResult]:
        """Analyze a single Python file.

        Delegates to specialized analysis methods for each concern.
        """
        try:
            with Path(file_path).open("r", encoding="utf-8") as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=str(file_path))

            # Delegate complexity analysis
            complexity_score = self._calculate_file_complexity(tree)

            # Collect issues from different analysis types
            issues = []

            # Security analysis via external backend delegation
            if include_security:
                security_issues = self._analyze_security_issues(tree, file_path)
                issues.extend(security_issues)

            # Complexity issues
            if include_complexity:
                complexity_issues = self._analyze_complexity_issues(file_path, complexity_score)
                issues.extend(complexity_issues)

            # Dead code analysis
            if include_dead_code:
                dead_code_issues = self._analyze_dead_code(tree, file_path)
                issues.extend(dead_code_issues)

            # Create file analysis result
            result = FlextQualityModels.FileAnalysisResult(
                id=f"file_{uuid.uuid4()}",
                analysis_id="current",  # Would be set by caller
                file_path=str(file_path),
                lines_of_code=len(source_code.splitlines()),
                complexity_score=complexity_score,
                security_score=100.0 if not include_security or not issues else 80.0,  # Simplified
                maintainability_score=100.0 - (complexity_score * 0.5),  # Simplified
                coverage_score=85.0,  # Would be calculated from actual coverage
                functions_count=len([n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
                classes_count=len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                issues=[{
                    "type": issue.issue_type,
                    "message": issue.message,
                    "severity": issue.severity,
                    "line": issue.line_number
                } for issue in issues],
            )

            return FlextResult.ok(result)

        except SyntaxError as e:
            return FlextResult.fail(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            return FlextResult.fail(f"Failed to analyze {file_path}: {e}")

    def _calculate_file_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity for a file.

        Delegates to AST analysis with focused complexity calculation.
        """
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers) + len(node.orelse)

        return min(100.0, complexity * 2.0)  # Scale and cap

    def _analyze_security_issues(self, tree: ast.AST, file_path: Path) -> list[FlextQualityModels.CodeIssue]:
        """Analyze security issues using external backend delegation.

        Delegates security analysis to FlextQualityExternalBackend.
        """
        issues = []

        # Use external backend for comprehensive security analysis
        try:
            analysis_result = self._external_backend.analyze(
                "", file_path=file_path, tool="bandit"
            )

            if analysis_result.is_success:
                security_data = analysis_result.value
                for issue_data in security_data.get("issues", []):
                    issue = FlextQualityModels.CodeIssue(
                        id=f"security_{len(issues)}",
                        analysis_id="current",
                        file_path=str(file_path),
                        line_number=issue_data.get("line_number"),
                        issue_type="security",
                        severity=self._map_security_severity(issue_data.get("severity", "medium")),
                        message=issue_data.get("message", ""),
                        rule_id=issue_data.get("test_id"),
                    )
                    issues.append(issue)
        except Exception:
            # Fallback to basic AST-based security check
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in {"eval", "exec"}
                ):
                    issue = FlextQualityModels.CodeIssue(
                        id=f"security_basic_{len(issues)}",
                        analysis_id="current",
                        file_path=str(file_path),
                        line_number=getattr(node, 'lineno', 1),
                        issue_type="security",
                        severity="high",
                        message=f"Dangerous function call: {node.func.id}",
                        rule_id="dangerous_call",
                    )
                    issues.append(issue)

        return issues

    def _map_security_severity(self, severity: str) -> str:
        """Map security tool severity to standardized severity."""
        return {"high": "high", "medium": "medium", "low": "low"}.get(severity.lower(), "medium")

    def _analyze_complexity_issues(self, file_path: Path, complexity_score: float) -> list[FlextQualityModels.CodeIssue]:
        """Analyze complexity-related issues."""
        issues = []

        if complexity_score > FlextQualityConstants.Complexity.MAX_COMPLEXITY:
            issue = FlextQualityModels.CodeIssue(
                id=f"complexity_{file_path.name}_{complexity_score}",
                analysis_id="current",
                file_path=str(file_path),
                line_number=1,
                issue_type="complexity",
                severity="medium",
                message=f"High complexity score: {complexity_score:.1f}",
                rule_id="complexity_check",
            )
            issues.append(issue)

        return issues

    def _analyze_dead_code(self, tree: ast.AST, file_path: Path) -> list[FlextQualityModels.CodeIssue]:
        """Analyze dead code using external backend delegation."""
        issues = []

        # Use external backend for comprehensive dead code detection
        try:
            analysis_result = self._external_backend.analyze(
                "", file_path=file_path, tool="vulture"
            )

            if analysis_result.is_success:
                dead_code_data = analysis_result.value
                for issue_data in dead_code_data.get("issues", []):
                    issue = FlextQualityModels.CodeIssue(
                        id=f"dead_code_{len(issues)}",
                        analysis_id="current",
                        file_path=str(file_path),
                        line_number=issue_data.get("line_number"),
                        issue_type="dead_code",
                        severity="low",
                        message=f"Unused {issue_data.get('type', 'code')}: {issue_data.get('name', '')}",
                        rule_id="dead_code",
                    )
                    issues.append(issue)
        except Exception:
            # Fallback to basic dead code detection
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Simple check: function with no return statements
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                    if not has_return and len(node.body) > FlextQualityConstants.Analysis.MIN_FUNCTION_LENGTH_FOR_DEAD_CODE:  # Threshold for dead code detection
                        issue = FlextQualityModels.CodeIssue(
                            id=f"dead_code_basic_{len(issues)}",
                            analysis_id="current",
                            file_path=str(file_path),
                            line_number=getattr(node, 'lineno', 1),
                            issue_type="dead_code",
                            severity="low",
                            message=f"Function '{node.name}' appears to be unused",
                            rule_id="unused_function",
                        )
                        issues.append(issue)

        return issues

    def _analyze_duplications(self, python_files: list[Path]) -> FlextResult[list[dict[str, object]]]:
        """Analyze code duplications across files."""
        try:
            issues = []
            file_contents = {}

            # Read files with size filtering
            for py_file in python_files:
                try:
                    with py_file.open(encoding="utf-8") as f:
                        content = f.read()
                    if len(content.strip()) > FlextQualityConstants.Analysis.MIN_FILE_SIZE_FOR_DUPLICATION_CHECK:
                        file_contents[py_file] = content
                except Exception as e:
                    self.logger.warning(f"Failed to read file for duplication check: {py_file} - {e}")
                    continue

            # Compare files for duplications
            file_list = list(file_contents.keys())
            duplication_issues = [
                {
                    "id": f"duplication_{file1.name}_{file2.name}",
                    "analysis_id": str(uuid.uuid4()),
                    "file_path": str(file1),
                    "line_number": 1,
                    "issue_type": "duplicate_code",
                    "severity": "medium",
                    "message": f"Code duplication detected between {file1.name} and {file2.name}",
                    "rule_id": "duplication_check",
                }
                for i, file1 in enumerate(file_list)
                for file2 in file_list[i + 1:]
                if self._files_have_duplication(file_contents[file1], file_contents[file2])
            ]
            issues.extend(duplication_issues)

            return FlextResult.ok(issues)

        except Exception as e:
            return FlextResult.fail(f"Duplication analysis failed: {e}")

    def _files_have_duplication(self, content1: str, content2: str) -> bool:
        """Check if two files have significant code duplication."""
        lines1 = set(content1.splitlines())
        lines2 = set(content2.splitlines())

        if lines1 and lines2:
            similarity = len(lines1 & lines2) / max(len(lines1), len(lines2))
            return similarity > FlextQualityConstants.Analysis.SIMILARITY_THRESHOLD

        return False

    def _calculate_overall_metrics(
        self,
        file_metrics: list[FlextQualityModels.FileAnalysisResult],
        total_lines: int,
    ) -> FlextResult[FlextQualityModels.OverallMetrics]:
        """Calculate overall project metrics."""
        try:
            if not file_metrics:
                return FlextResult.ok(FlextQualityModels.OverallMetrics())

            # Aggregate metrics across all files
            avg_complexity = sum(m.complexity_score for m in file_metrics) / len(file_metrics)
            avg_coverage = sum(m.coverage_score for m in file_metrics) / len(file_metrics)
            avg_security = sum(m.security_score for m in file_metrics) / len(file_metrics)
            avg_maintainability = sum(m.maintainability_score for m in file_metrics) / len(file_metrics)

            total_functions = sum(m.functions_count for m in file_metrics)
            total_classes = sum(m.classes_count for m in file_metrics)

            overall_metrics = FlextQualityModels.OverallMetrics(
                files_analyzed=len(file_metrics),
                total_lines=total_lines,
                functions_count=total_functions,
                classes_count=total_classes,
                overall_score=(avg_complexity + avg_coverage + avg_security + avg_maintainability) / 4.0,
                coverage_score=avg_coverage,
                security_score=avg_security,
                maintainability_score=avg_maintainability,
                complexity_score=avg_complexity,
            )

            return FlextResult.ok(overall_metrics)

        except Exception as e:
            return FlextResult.fail(f"Metrics calculation failed: {e}")

    def _create_analysis_results(
        self,
        overall_metrics: FlextQualityModels.OverallMetrics,
        all_issues: list[FlextQualityModels.CodeIssue],
    ) -> FlextResult[FlextQualityModels.AnalysisResults]:
        """Create final analysis results."""
        try:
            # Group issues by type for metrics
            security_issues = [i for i in all_issues if i.issue_type == "security"]
            complexity_issues = [i for i in all_issues if i.issue_type == "complexity"]
            dead_code_issues = [i for i in all_issues if i.issue_type == "dead_code"]
            duplication_issues = [i for i in all_issues if i.issue_type == "duplicate_code"]

            # Create recommendations based on issues
            recommendations = []
            if security_issues:
                recommendations.append("Address security vulnerabilities")
            if complexity_issues:
                recommendations.append("Refactor complex functions")
            if dead_code_issues:
                recommendations.append("Remove unused code")
            if duplication_issues:
                recommendations.append("Eliminate code duplications")

            analysis_results = FlextQualityModels.AnalysisResults(
                issues=[{"type": i.issue_type, "message": i.message} for i in all_issues],
                metrics={
                    "total_issues": len(all_issues),
                    "security_issues": len(security_issues),
                    "complexity_issues": len(complexity_issues),
                    "dead_code_issues": len(dead_code_issues),
                    "duplication_issues": len(duplication_issues),
                },
                recommendations=recommendations,
                overall_score=overall_metrics.overall_score,
                coverage_score=overall_metrics.coverage_score,
                security_score=overall_metrics.security_score,
                maintainability_score=overall_metrics.maintainability_score,
                complexity_score=overall_metrics.complexity_score,
            )

            return FlextResult.ok(analysis_results)

        except Exception as e:
            return FlextResult.fail(f"Analysis results creation failed: {e}")

    def get_quality_score(self) -> float:
        """Get the overall quality score from the last analysis."""
        return self._current_results.overall_score if self._current_results else 0.0

    def get_quality_grade(self) -> str:
        """Get the quality grade from the last analysis."""
        return self._current_results.quality_grade if self._current_results else "F"

    def get_last_analysis_result(self) -> FlextQualityModels.AnalysisResults | None:
        """Get the results from the last analysis."""
        return self._current_results
