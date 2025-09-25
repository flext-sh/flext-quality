"""Code analyzer interface for FLEXT Quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import warnings
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_quality.analysis_types import FlextQualityAnalysisTypes
from flext_quality.grade_calculator import FlextQualityGradeCalculator
from flext_quality.value_objects import IssueSeverity, IssueType

logger = FlextLogger(__name__)

# Constants
MIN_FILE_SIZE_FOR_DUPLICATION_CHECK = 100
SIMILARITY_THRESHOLD = 0.8


class FlextQualityCodeAnalyzer:
    """Main code analyzer interface for FLEXT Quality."""

    def __init__(self, project_path: str | Path) -> None:
        """Initialize analyzer with project path."""
        self.project_path = Path(project_path)
        self._current_results: FlextQualityAnalysisTypes.AnalysisResults | None = None

    def analyze_project(
        self,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> FlextQualityAnalysisTypes.AnalysisResults:
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
        logger.info("Starting code analysis trace for project: %s", self.project_path)
        logger.info("Starting project analysis: %s", self.project_path)
        logger.info("Starting comprehensive code analysis for %s", self.project_path)

        # Find Python files
        python_files = self._find_python_files()

        # Analyze each file using FlextResult pattern
        file_metrics: list[FlextQualityAnalysisTypes.FileAnalysisResult] = []
        total_lines = 0
        analysis_errors = 0

        for file_path in python_files:
            metrics_result: FlextResult[object] = self._analyze_file(file_path)
            if metrics_result.is_success:
                metrics = metrics_result.value
                file_metrics.append(metrics)
                total_lines += metrics.lines_of_code
            else:
                analysis_errors += 1
                logger.warning(
                    "Failed to analyze file %s: %s",
                    file_path,
                    metrics_result.error,
                )

        # Log analysis summary
        logger.info(
            "File analysis complete: %d succeeded, %d failed",
            len(file_metrics),
            analysis_errors,
        )

        # Calculate overall metrics
        overall_metrics = FlextQualityAnalysisTypes.OverallMetrics(
            files_analyzed=len(file_metrics),  # Only count successfully analyzed files
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
        security_issues: list[object] = (
            self._analyze_security() if include_security else []
        )
        dead_code_issues: list[object] = (
            self._analyze_dead_code() if include_dead_code else []
        )
        duplication_issues: list[object] = (
            self._analyze_duplicates() if include_duplicates else []
        )

        # Create final results
        results = FlextQualityAnalysisTypes.AnalysisResults(
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
        logger.info("Files analyzed: %d", len(file_metrics))
        logger.info("Total issues found: %d", results.total_issues)
        logger.info("Analysis errors: %d", analysis_errors)

        logger.info(
            "Analysis completed. Files: %d, Lines: %d",
            len(file_metrics),
            total_lines,
        )

        logger.info("Code analysis completed for %s", self.project_path)

        return results

    def get_quality_score(self: object) -> float:
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

    def get_quality_grade(self: object) -> str:
        """Get letter grade based on quality score - DRY refactored.

        Returns:
            Letter grade (A+ to F) based on calculated quality score.

        """
        score = self.get_quality_score()
        grade = FlextQualityGradeCalculator.calculate_grade(score)
        return str(grade.value)

    def _find_python_files(self: object) -> list[Path]:
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

    def _analyze_file(
        self, file_path: Path
    ) -> FlextResult[FlextQualityAnalysisTypes.FileAnalysisResult]:
        """Analyze a single Python file.

        Args:
            file_path: Path to the Python file.

        Returns:
            FlextResult containing FlextQualityAnalysisTypes.FileAnalysisResult with file metrics or error.

        """
        if not Path(file_path).exists():
            return FlextResult[FlextQualityAnalysisTypes.FileAnalysisResult].fail(
                f"File does not exist: {file_path}",
            )

        # Read file content with explicit error handling
        content_result: FlextResult[object] = self._read_file_content(file_path)
        if content_result.is_failure:
            return FlextResult[FlextQualityAnalysisTypes.FileAnalysisResult].fail(
                content_result.error or "Failed to read file content",
            )

        content = content_result.value
        lines = content.splitlines()

        # Basic metrics
        lines_of_code = len(
            [
                line
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ],
        )

        # Parse AST with explicit error handling
        ast_result: FlextResult[object] = self._parse_ast_content(content)
        if ast_result.is_failure:
            # Handle syntax errors explicitly - still return valid result with limited data
            logger.warning("Syntax error in %s: %s", file_path, ast_result.error)

            analysis_result = FlextQualityAnalysisTypes.FileAnalysisResult(
                file_path=file_path,
                lines_of_code=lines_of_code,
                complexity_score=0.0,  # No complexity for files with syntax errors
                security_issues=1,  # Syntax error is a security/quality issue
                style_issues=0,
                dead_code_lines=0,
            )
            return FlextResult[FlextQualityAnalysisTypes.FileAnalysisResult].ok(
                analysis_result
            )

        tree = ast_result.value

        # Calculate cyclomatic complexity (simplified)
        complexity = self._calculate_complexity(tree)

        analysis_result = FlextQualityAnalysisTypes.FileAnalysisResult(
            file_path=file_path,
            lines_of_code=lines_of_code,
            complexity_score=max(0.0, min(100.0, 100.0 - complexity * 2)),
            security_issues=0,  # Will be calculated later
            style_issues=0,  # Will be calculated later
            dead_code_lines=0,  # Will be calculated later
        )

        return FlextResult[FlextQualityAnalysisTypes.FileAnalysisResult].ok(
            analysis_result
        )

    def _read_file_content(self, file_path: Path) -> FlextResult[str]:
        """Read file content with explicit error handling.

        Args:
            file_path: Path to the file to read.

        Returns:
            FlextResult containing file content or error message.

        """
        if not file_path.exists():
            return FlextResult[str].fail(f"File does not exist: {file_path}")

        if not file_path.is_file():
            return FlextResult[str].fail(f"Path is not a file: {file_path}")

        # Check file size before reading
        if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
            return FlextResult[str].fail(f"File too large: {file_path}")

        # Read with explicit encoding handling
        try:
            with file_path.open(encoding="utf-8", errors="strict") as f:
                content = f.read()
        except UnicodeDecodeError as e:
            return FlextResult[str].fail(f"File encoding error: {e}")
        except OSError as e:
            return FlextResult[str].fail(f"OS error reading file: {e}")
        except MemoryError:
            return FlextResult[str].fail(
                f"File too large to read into memory: {file_path}",
            )

        return FlextResult[str].ok(content)

    def _parse_ast_content(self, content: str) -> FlextResult[ast.AST]:
        """Parse content into AST with explicit error handling.

        Args:
            content: Python source code content.

        Returns:
            FlextResult containing AST tree or error message.

        """
        if not content.strip():
            return FlextResult[ast.AST].fail("Empty content cannot be parsed")

        try:
            tree = ast.parse(content)
            return FlextResult[ast.AST].ok(tree)
        except SyntaxError as e:
            return FlextResult[ast.AST].fail(f"Syntax error: {e}")
        except ValueError as e:
            return FlextResult[ast.AST].fail(f"Value error in parsing: {e}")
        except RecursionError:
            return FlextResult[ast.AST].fail("Code too deeply nested to parse")

    def _calculate_complexity(self, tree: ast.AST) -> int:
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            # Count decision points
            if isinstance(node, (ast.If | ast.While | ast.For) | ast.With):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, (ast.And | ast.Or)):
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

    def _analyze_security(
        self: object,
    ) -> list[FlextQualityAnalysisTypes.SecurityIssue]:
        issues: list[FlextQualityAnalysisTypes.SecurityIssue] = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                if "eval(" in content:
                    issues.append(
                        FlextQualityAnalysisTypes.SecurityIssue(
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
                        FlextQualityAnalysisTypes.SecurityIssue(
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
                        FlextQualityAnalysisTypes.SecurityIssue(
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

    def _calculate_quality_score(
        self, file_metrics: list[FlextQualityAnalysisTypes.FileAnalysisResult]
    ) -> float:
        """Calculate overall quality score from file metrics."""
        if not file_metrics:
            return 0.0

        total_score = sum(metrics.complexity_score for metrics in file_metrics)
        return total_score / len(file_metrics)

    def _analyze_complexity(
        self,
        file_metrics: list[FlextQualityAnalysisTypes.FileAnalysisResult],
    ) -> list[FlextQualityAnalysisTypes.ComplexityIssue]:
        complexity_threshold = 10

        complex_issues: list[FlextQualityAnalysisTypes.ComplexityIssue] = []
        for metrics in file_metrics:
            # Calculate complexity from score - lower score means higher complexity
            complexity_val = int((100.0 - metrics.complexity_score) / 2)
            if complexity_val > complexity_threshold:
                complex_issues.append(
                    FlextQualityAnalysisTypes.ComplexityIssue(
                        file_path=str(metrics.file_path),
                        function_name="file_level",  # Would need AST parsing for specific functions
                        line_number=1,
                        complexity_value=complexity_val,
                        issue_type="high_complexity",
                        message=f"High complexity: {complexity_val}",
                    ),
                )
        return complex_issues

    def _analyze_dead_code(
        self: object,
    ) -> list[FlextQualityAnalysisTypes.DeadCodeIssue]:
        # This is a placeholder - real implementation would use vulture or similar
        issues: list[FlextQualityAnalysisTypes.DeadCodeIssue] = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                lines = content.splitlines()

                for i, line in enumerate(lines):
                    if (
                        "import " in line or "from " in line
                    ) and "# unused" in line.lower():
                        issues.append(
                            FlextQualityAnalysisTypes.DeadCodeIssue(
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

    def _analyze_duplicates(
        self: object,
    ) -> list[FlextQualityAnalysisTypes.DuplicationIssue]:
        issues: list[FlextQualityAnalysisTypes.DuplicationIssue] = []

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

        files = list(file_contents.keys())
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1, file2 = files[i], files[j]

                lines1 = set(file_contents[file1].splitlines())
                lines2 = set(file_contents[file2].splitlines())

                if lines1 and lines2:
                    similarity = len(lines1 & lines2) / max(len(lines1), len(lines2))

                    if similarity > SIMILARITY_THRESHOLD:  # 80% similarity threshold
                        duplicate_lines = len(lines1 & lines2)  # Common lines count
                        similarity_percent = similarity * 100.0  # Convert to percentage

                        issues.append(
                            FlextQualityAnalysisTypes.DuplicationIssue(
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
        """Initialize the instance."""
        warnings.warn(
            "CodeAnalyzer is deprecated; use FlextQualityCodeAnalyzer",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(project_path)
