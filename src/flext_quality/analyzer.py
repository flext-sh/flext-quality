"""Code analyzer interface for FLEXT Quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


import ast
import warnings
from pathlib import Path

from flext_core import FlextLogger
from flext_observability import (
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

from flext_quality.analysis_types import (
    AnalysisResults,
    ComplexityIssue,
    DeadCodeIssue,
    DuplicationIssue,
    FileAnalysisResult,
    IssueSeverity,
    IssueType,
    OverallMetrics,
    SecurityIssue,
)
from flext_quality.grade_calculator import QualityGradeCalculator

logger = FlextLogger(__name__)

# Constants
MIN_FILE_SIZE_FOR_DUPLICATION_CHECK = 100
SIMILARITY_THRESHOLD = 0.8


class FlextQualityCodeAnalyzer:
    """Main code analyzer interface for FLEXT Quality."""


from flext_core import FlextLogger

logger = FlextLogger(__name__)

# Constants
MIN_FILE_SIZE_FOR_DUPLICATION_CHECK = 100
SIMILARITY_THRESHOLD = 0.8


class FlextQualityCodeAnalyzer:
    """Main code analyzer interface for FLEXT Quality."""

    def __init__(self, project_path: str | Path) -> None:
        """Initialize analyzer with project path."""
        self.project_path = Path(project_path)
        self._current_results: AnalysisResults | None = None

    def analyze_project(
        self,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> AnalysisResults:
        """Analyze entire project for quality metrics and issues.

        Args:
            include_security: Whether to include security analysis.
            include_complexity: Whether to include complexity analysis.
            include_dead_code: Whether to include dead code detection.
            include_duplicates: Whether to include duplicate code detection.

        Returns:
            Dictionary containing analysis results including metrics and issues.

        """
        # Create trace for the entire analysis
        # Emit trace via observability integration
        flext_create_trace(
            operation_name="CodeAnalyzer.analyze_project",
            service_name="flext-quality",
            config={"project_path": str(self.project_path)},
        )

        logger.info("Starting project analysis: %s", self.project_path)
        flext_create_log_entry(
            message=f"Starting comprehensive code analysis for {self.project_path}",
            service="flext-quality",
            level="info",
        )

        # Find Python files
        python_files = self._find_python_files()
        files_analyzed = len(python_files)

        # Analyze each file
        file_metrics: list[FileAnalysisResult] = []
        total_lines = 0
        for file_path in python_files:
            metrics = self._analyze_file(file_path)
            if metrics:
                file_metrics.append(metrics)
                total_lines += metrics.lines_of_code

        # Calculate overall metrics
        overall_metrics = OverallMetrics(
            files_analyzed=files_analyzed,
            total_lines=total_lines,
            quality_score=self._calculate_quality_score(file_metrics),
            coverage_score=85.0,  # Placeholder - would need real coverage integration
            security_score=90.0,  # Will be calculated from security issues
            maintainability_score=80.0,  # Will be calculated from complexity
            complexity_score=75.0,  # Will be calculated from complexity issues
        )

        # Run specialized analyses
        complexity_issues = (
            self._analyze_complexity(file_metrics) if include_complexity else []
        )
        security_issues = self._analyze_security() if include_security else []
        dead_code_issues = self._analyze_dead_code() if include_dead_code else []
        duplication_issues = self._analyze_duplicates() if include_duplicates else []

        # Create final results
        results = AnalysisResults(
            overall_metrics=overall_metrics,
            file_metrics=file_metrics,
            complexity_issues=complexity_issues,
            security_issues=security_issues,
            dead_code_issues=dead_code_issues,
            duplication_issues=duplication_issues,
        )

        # Store results for further analysis
        self._current_results = results

        # Create metrics for observability using REAL flext-observability API with type safety
        flext_create_metric(
            name="files_analyzed",
            value=float(files_analyzed),
            tags={"project": str(self.project_path)},
        )

        flext_create_metric(
            name="total_issues",
            value=float(results.total_issues),
            tags={"project": str(self.project_path)},
        )

        logger.info(
            "Analysis completed. Files: %d, Lines: %d",
            files_analyzed,
            total_lines,
        )

        flext_create_log_entry(
            message=f"Code analysis completed for {self.project_path}",
            service="flext-quality",
            level="info",
        )

        return results

    def get_quality_score(self) -> float:
        """Calculate overall quality score based on analysis results.

        Returns:
            Quality score between 0.0 and 100.0 based on code quality metrics.

        """
        if not self._current_results:
            return 0.0

        results = self._current_results

        # Base score
        score = 100.0

        # Deduct for complexity issues
        complexity_penalty = len(results.complexity_issues) * 5
        score -= min(complexity_penalty, 30)

        # Deduct for security issues
        security_penalty = len(results.security_issues) * 10
        score -= min(security_penalty, 40)

        # Deduct for dead code
        dead_code_penalty = len(results.dead_code_issues) * 3
        score -= min(dead_code_penalty, 20)

        # Deduct for duplicates
        duplicates_penalty = len(results.duplication_issues) * 8
        score -= min(duplicates_penalty, 25)

        return max(0.0, score)

    def get_quality_grade(self) -> str:
        """Get letter grade based on quality score - DRY refactored.

        Returns:
            Letter grade (A+ to F) based on calculated quality score.

        """
        score = self.get_quality_score()
        grade = QualityGradeCalculator.calculate_grade(score)
        return str(grade.value)

    def _find_python_files(self) -> list[Path]:
        if not self.project_path.exists():
            logger.warning("Project path does not exist: %s", self.project_path)
            return []

        python_files: list[Path] = []
        for py_file in self.project_path.rglob("*.py"):
            # Skip hidden files and common ignore patterns
            if any(part.startswith(".") for part in py_file.parts):
                continue
            if any(
                ignore in str(py_file)
                for ignore in ["__pycache__", ".git", "node_modules"]
            ):
                continue

            python_files.append(py_file)

        return python_files

    def _analyze_file(self, file_path: Path) -> FileAnalysisResult | None:
        """Analyze a single Python file.

        Args:
            file_path: Path to the Python file.

        Returns:
            FileAnalysisResult with file metrics or None if analysis fails.

        """
        try:
            with Path(file_path).open(encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()

            # Basic metrics
            lines_of_code = len(
                [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ],
            )

            try:
                tree = ast.parse(content)

                # Count functions and classes (including async functions) - for complexity calculation

                # Calculate cyclomatic complexity (simplified)
                complexity = self._calculate_complexity(tree)

                return FileAnalysisResult(
                    file_path=file_path,
                    lines_of_code=lines_of_code,
                    complexity_score=max(0.0, min(100.0, 100.0 - complexity * 2)),
                    security_issues=0,  # Will be calculated later
                    style_issues=0,  # Will be calculated later
                    dead_code_lines=0,  # Will be calculated later
                )

            except SyntaxError as e:
                # Reuse module-level logger
                logger.warning("Syntax error in %s: %s", file_path, e)

                return FileAnalysisResult(
                    file_path=file_path,
                    lines_of_code=lines_of_code,
                    complexity_score=0.0,  # No complexity for files with syntax errors
                    security_issues=1,  # Syntax error is a security/quality issue
                    style_issues=0,
                    dead_code_lines=0,
                )
        except (RuntimeError, ValueError, TypeError, FileNotFoundError, OSError):
            # Reuse module-level logger
            logger.exception("File analysis failed for %s", file_path)
            logger.exception("Error analyzing file %s", file_path)
            return None

    def _calculate_complexity(self, tree: ast.AST) -> int:
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            # Count decision points
            if isinstance(node, ast.If | ast.While | ast.For | ast.With):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, ast.And | ast.Or):
                complexity += 1

        return complexity

    def _calculate_overall_metrics(
        self,
        file_metrics: list[FlextTypes.Core.Dict],
    ) -> FlextTypes.Core.Dict:
        if not file_metrics:
            return {}

        total_files = len(file_metrics)

        # DRY helper for safe metric extraction with type safety
        def safe_get_metric(
            metric_list: list[FlextTypes.Core.Dict],
            key: str,
            default: float = 0,
        ) -> list[int | float]:
            """Extract metric values safely with type validation.

            Args:
                metric_list: List of metric dictionaries
                key: Metric key to extract
                default: Default value for missing/invalid entries

            Returns:
                List of numeric values with type safety guaranteed

            """
            values: list[int | float] = []
            for m in metric_list:
                value = m.get(key, default)
                if isinstance(value, (int, float)):
                    values.append(value)
                else:
                    values.append(default)
            return values

        # Extract metrics with type safety
        loc_values = safe_get_metric(file_metrics, "lines_of_code", 0)
        function_values = safe_get_metric(file_metrics, "function_count", 0)
        class_values = safe_get_metric(file_metrics, "class_count", 0)
        complexity_values = safe_get_metric(file_metrics, "complexity", 0.0)

        total_loc = sum(loc_values)
        total_functions = sum(function_values)
        total_classes = sum(class_values)

        avg_complexity = (
            sum(complexity_values) / total_files if total_files > 0 else 0.0
        )
        max_complexity = max(complexity_values) if complexity_values else 0.0

        return {
            "total_files": total_files,
            "total_lines_of_code": total_loc,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": avg_complexity,
            "max_complexity": max_complexity,
            "avg_lines_per_file": total_loc / total_files if total_files > 0 else 0,
        }

    def _analyze_security(self) -> list[SecurityIssue]:
        issues: list[SecurityIssue] = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                # Simple security checks
                if "eval(" in content:
                    issues.append(
                        SecurityIssue(
                            file_path=str(py_file.relative_to(self.project_path)),
                            line_number=1,  # Would need line-by-line analysis for exact position
                            issue_type=IssueType.SECURITY_VULNERABILITY,
                            description="Use of eval() function detected - potential code injection vulnerability",
                            severity=IssueSeverity.HIGH,
                            message="Use of eval() detected",
                            rule_id="B307",  # Bandit rule ID for eval usage
                        ),
                    )

                if "exec(" in content:
                    issues.append(
                        SecurityIssue(
                            file_path=str(py_file.relative_to(self.project_path)),
                            line_number=1,
                            issue_type=IssueType.SECURITY_VULNERABILITY,
                            description="Use of exec() function detected - potential code injection vulnerability",
                            severity=IssueSeverity.HIGH,
                            message="Use of exec() detected",
                            rule_id="B102",  # Bandit rule ID for exec usage
                        ),
                    )

                if "import os" in content and "os.system(" in content:
                    issues.append(
                        SecurityIssue(
                            file_path=str(py_file.relative_to(self.project_path)),
                            line_number=1,
                            issue_type=IssueType.SECURITY_VULNERABILITY,
                            description="Use of os.system() function detected - potential command injection vulnerability",
                            severity=IssueSeverity.MEDIUM,
                            message="Potential command injection with os.system()",
                            rule_id="B605",  # Bandit rule ID for os.system usage
                        ),
                    )
            except (RuntimeError, ValueError, TypeError) as e:
                logger.warning("Error checking security in %s: %s", py_file, e)

        return issues

    def _calculate_quality_score(self, file_metrics: list[FileAnalysisResult]) -> float:
        """Calculate overall quality score from file metrics."""
        if not file_metrics:
            return 0.0

        total_score = sum(metrics.complexity_score for metrics in file_metrics)
        return total_score / len(file_metrics)

    def _analyze_complexity(
        self,
        file_metrics: list[FileAnalysisResult],
    ) -> list[ComplexityIssue]:
        complexity_threshold = 10

        complex_issues: list[ComplexityIssue] = []
        for metrics in file_metrics:
            # Calculate complexity from score - lower score means higher complexity
            complexity_val = int((100.0 - metrics.complexity_score) / 2)
            if complexity_val > complexity_threshold:
                complex_issues.append(
                    ComplexityIssue(
                        file_path=str(metrics.file_path),
                        function_name="file_level",  # Would need AST parsing for specific functions
                        line_number=1,
                        complexity_value=complexity_val,
                        issue_type="high_complexity",
                        message=f"High complexity: {complexity_val}",
                    ),
                )
        return complex_issues

    def _analyze_dead_code(self) -> list[DeadCodeIssue]:
        # This is a placeholder - real implementation would use vulture or similar
        issues: list[DeadCodeIssue] = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                lines = content.splitlines()

                # Simple heuristic: if import line contains "unused" comment
                for i, line in enumerate(lines):
                    if (
                        "import " in line or "from " in line
                    ) and "# unused" in line.lower():
                        issues.append(
                            DeadCodeIssue(
                                file_path=str(py_file.relative_to(self.project_path)),
                                line_number=i + 1,
                                end_line_number=i + 1,
                                issue_type="unused_import",
                                code_type="import_statement",
                                code_snippet=line.strip(),
                                message=f"Potentially unused import: {line.strip()}",
                            ),
                        )
            except (RuntimeError, ValueError, TypeError) as e:
                logger.warning("Error checking dead code in %s: %s", py_file, e)

        return issues

    def _analyze_duplicates(self) -> list[DuplicationIssue]:
        issues: list[DuplicationIssue] = []

        file_contents: dict[Path, str] = {}
        for py_file in self.project_path.rglob("*.py"):
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()
                    if len(content.strip()) > MIN_FILE_SIZE_FOR_DUPLICATION_CHECK:
                        # Only check substantial files
                        file_contents[py_file] = content
            except (
                RuntimeError,
                ValueError,
                TypeError,
                OSError,
                UnicodeDecodeError,
            ) as e:
                logger.warning("Error reading %s: %s", py_file, e)

        # Simple duplicate detection based on file similarity
        files = list(file_contents.keys())
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1, file2 = files[i], files[j]

                # Simple line-based similarity check
                lines1 = set(file_contents[file1].splitlines())
                lines2 = set(file_contents[file2].splitlines())

                if lines1 and lines2:
                    similarity = len(lines1 & lines2) / max(len(lines1), len(lines2))

                    if similarity > SIMILARITY_THRESHOLD:  # 80% similarity threshold
                        duplicate_lines = len(lines1 & lines2)  # Common lines count
                        similarity_percent = similarity * 100.0  # Convert to percentage

                        issues.append(
                            DuplicationIssue(
                                files=[
                                    str(file1.relative_to(self.project_path)),
                                    str(file2.relative_to(self.project_path)),
                                ],
                                duplicate_lines=duplicate_lines,
                                similarity=similarity,
                                similarity_percent=similarity_percent,
                                line_ranges=[
                                    (1, len(lines1)),
                                    (1, len(lines2)),
                                ],  # Simplified
                                message=f"High similarity ({similarity:.1%}) between files",
                            ),
                        )

        return issues


# Legacy compatibility facade (TEMPORARY)
class CodeAnalyzer(FlextQualityCodeAnalyzer):
    """Legacy analyzer class - replaced by FlextQualityCodeAnalyzer.

    DEPRECATED: Use FlextQualityCodeAnalyzer directly.
    This facade provides compatibility during migration.
    """

    def __init__(self, project_path: str | Path) -> None:
        warnings.warn(
            "CodeAnalyzer is deprecated; use FlextQualityCodeAnalyzer",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(project_path)
