"""Code analyzer interface for FLEXT Quality."""

from __future__ import annotations

import ast
from pathlib import Path

from flext_core import get_logger
from flext_observability import (
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
)

from flext_quality.domain.quality_grade_calculator import QualityGradeCalculator

logger = get_logger(__name__)


class CodeAnalyzer:
    """Main code analyzer interface for FLEXT Quality."""

    def __init__(self, project_path: str | Path) -> None:
        self.project_path = Path(project_path)
        self.analysis_results: dict[str, object] = {}

    def analyze_project(
        self,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> dict[str, object]:
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
        flext_create_trace(
            trace_id=f"analyze_project_{self.project_path.name}",
            operation="CodeAnalyzer.analyze_project",
            config={"project_path": str(self.project_path)},
        )

        logger.info("Starting project analysis: %s", self.project_path)
        flext_create_log_entry(
            message=f"Starting comprehensive code analysis for {self.project_path}",
            level="info",
            context={
                "analyzer": "CodeAnalyzer",
                "project_path": str(self.project_path),
            },
        )

        results: dict[str, object] = {
            "project_path": str(self.project_path),
            "files_analyzed": 0,
            "total_lines": 0,
            "python_files": [],
            "metrics": {},
            "issues": {
                "security": [],
                "complexity": [],
                "dead_code": [],
                "duplicates": [],
            },
        }

        # Find Python files
        python_files = self._find_python_files()
        results["python_files"] = [str(f) for f in python_files]
        results["files_analyzed"] = len(python_files)

        # Analyze each file with proper type safety
        file_metrics = []
        total_lines = 0
        for file_path in python_files:
            metrics = self._analyze_file(file_path)
            if metrics:
                file_metrics.append(metrics)
                lines = metrics.get("lines_of_code", 0)
                if isinstance(lines, (int, float)):
                    total_lines += int(lines)

        results["total_lines"] = total_lines

        # Calculate overall metrics
        results["metrics"] = self._calculate_overall_metrics(file_metrics)

        # Run specialized analyses with proper type casting
        issues_dict = results["issues"]
        if isinstance(issues_dict, dict):
            if include_security:
                issues_dict["security"] = self._analyze_security()

            if include_complexity:
                issues_dict["complexity"] = self._analyze_complexity(file_metrics)

            if include_dead_code:
                issues_dict["dead_code"] = self._analyze_dead_code()

            if include_duplicates:
                issues_dict["duplicates"] = self._analyze_duplicates()

        self.analysis_results = results

        # Create metrics for observability using REAL flext-observability API with type safety
        files_analyzed = results["files_analyzed"]
        if isinstance(files_analyzed, (int, float)):
            flext_create_metric(
                name="code_analysis_files_analyzed",
                value=float(files_analyzed),
                tags={"project_path": str(self.project_path)},
            )

        total_lines_obj = results["total_lines"]
        if isinstance(total_lines_obj, (int, float)):
            flext_create_metric(
                name="code_analysis_total_lines",
                value=float(total_lines_obj),
                tags={"project_path": str(self.project_path)},
            )

        # Count total issues for metrics with proper type handling
        issues_dict = results["issues"]
        if isinstance(issues_dict, dict):
            total_issues = sum(
                len(issue_list)
                for issue_list in issues_dict.values()
                if isinstance(issue_list, list)
            )
        else:
            total_issues = 0

        flext_create_metric(
            name="code_analysis_total_issues",
            value=float(total_issues),
            tags={"project_path": str(self.project_path)},
        )

        logger.info(
            "Analysis completed. Files: %d, Lines: %d",
            results["files_analyzed"],
            results["total_lines"],
        )

        flext_create_log_entry(
            message=f"Code analysis completed for {self.project_path}",
            level="info",
            context={
                "analyzer": "CodeAnalyzer",
                "project_path": str(self.project_path),
                "files_analyzed": results["files_analyzed"],
                "total_lines": results["total_lines"],
                "total_issues": total_issues,
            },
        )

        return results

    def get_quality_score(self) -> float:
        """Calculate overall quality score based on analysis results.

        Returns:
            Quality score between 0.0 and 100.0 based on code quality metrics.

        """
        if not self.analysis_results:
            return 0.0

        self.analysis_results.get("metrics", {})
        issues_obj = self.analysis_results.get("issues", {})

        # Type safety for issues dictionary
        if not isinstance(issues_obj, dict):
            return 0.0

        issues = issues_obj

        # Base score
        score = 100.0

        # Deduct for complexity issues with type safety
        complexity_list = issues.get("complexity", [])
        if isinstance(complexity_list, list):
            complexity_penalty = len(complexity_list) * 5
            score -= min(complexity_penalty, 30)

        # Deduct for security issues with type safety
        security_list = issues.get("security", [])
        if isinstance(security_list, list):
            security_penalty = len(security_list) * 10
            score -= min(security_penalty, 40)

        # Deduct for dead code with type safety
        dead_code_list = issues.get("dead_code", [])
        if isinstance(dead_code_list, list):
            dead_code_penalty = len(dead_code_list) * 3
            score -= min(dead_code_penalty, 20)

        # Deduct for duplicates with type safety
        duplicates_list = issues.get("duplicates", [])
        if isinstance(duplicates_list, list):
            duplicate_penalty = len(duplicates_list) * 5
            score -= min(duplicate_penalty, 25)

        return max(0.0, score)

    def get_quality_grade(self) -> str:
        """Get letter grade based on quality score - DRY refactored.

        Returns:
            Letter grade (A+ to F) based on calculated quality score.

        """
        score = self.get_quality_score()
        grade = QualityGradeCalculator.calculate_grade(score)
        return grade.value

    def _find_python_files(self) -> list[Path]:
        if not self.project_path.exists():
            logger.warning("Project path does not exist: %s", self.project_path)
            return []

        python_files = []
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

    def _analyze_file(self, file_path: Path) -> dict[str, object] | None:
        """Analyze a single Python file.

        Args:
            file_path: Path to the Python file.

        Returns:
            Dictionary with file metrics or None if analysis fails.

        """
        try:
            with open(file_path, encoding="utf-8") as f:
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
            comment_lines = len(
                [line for line in lines if line.strip().startswith("#")],
            )
            blank_lines = len([line for line in lines if not line.strip()])

            try:
                tree = ast.parse(content)

                # Count functions and classes
                functions = [
                    node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
                ]
                classes = [
                    node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
                ]

                # Calculate cyclomatic complexity (simplified)
                complexity = self._calculate_complexity(tree)

                return {
                    "file_path": str(file_path.relative_to(self.project_path)),
                    "lines_of_code": lines_of_code,
                    "comment_lines": comment_lines,
                    "blank_lines": blank_lines,
                    "total_lines": len(lines),
                    "function_count": len(functions),
                    "class_count": len(classes),
                    "complexity": complexity,
                    "functions": [f.name for f in functions],
                    "classes": [c.name for c in classes],
                }

            except SyntaxError as e:
                logger.warning("Syntax error in %s: %s", file_path, e)
                return {
                    "file_path": str(file_path.relative_to(self.project_path)),
                    "lines_of_code": lines_of_code,
                    "comment_lines": comment_lines,
                    "blank_lines": blank_lines,
                    "total_lines": len(lines),
                    "function_count": 0,
                    "class_count": 0,
                    "complexity": 0,
                    "syntax_error": str(e),
                }
        except (RuntimeError, ValueError, TypeError, FileNotFoundError, OSError) as e:
            logger.exception("Error analyzing file %s: %s", file_path, e)
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
        file_metrics: list[dict[str, object]],
    ) -> dict[str, object]:
        if not file_metrics:
            return {}

        total_files = len(file_metrics)

        # DRY helper for safe metric extraction with type safety
        def safe_get_metric(
            metric_list: list[dict[str, object]], key: str, default: float = 0,
        ) -> list[int | float]:
            """Extract metric safely with type validation."""
            values = []
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

    def _analyze_security(self) -> list[dict[str, object]]:
        # This is a simplified implementation
        # In production, this would integrate with bandit or similar tools
        issues = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                # Simple security checks with proper type casting for consistency
                if "eval(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "dangerous_function",
                            "message": "Use of eval() detected",
                            "severity": "high",
                            "line": 0,  # Add line number for consistency with other dict structures
                        },
                    )

                if "exec(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "dangerous_function",
                            "message": "Use of exec() detected",
                            "severity": "high",
                        },
                    )

                if "import os" in content and "os.system(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "command_injection",
                            "message": "Potential command injection with os.system()",
                            "severity": "medium",
                        },
                    )
            except (RuntimeError, ValueError, TypeError) as e:
                logger.warning("Error checking security in %s: %s", py_file, e)

        return issues

    def _analyze_complexity(
        self,
        file_metrics: list[dict[str, object]],
    ) -> list[dict[str, object]]:
        complexity_threshold = 10

        # DRY pattern: extract complexity once with proper type safety
        complex_files = []
        for metrics in file_metrics:
            complexity_val = metrics.get("complexity", 0)
            if (
                isinstance(complexity_val, (int, float))
                and complexity_val > complexity_threshold
            ):
                complex_files.append(
                    {
                        "file": metrics["file_path"],
                        "type": "high_complexity",
                        "message": f"High complexity: {complexity_val}",
                        "complexity": complexity_val,
                        "threshold": complexity_threshold,
                    },
                )
        return complex_files

    def _analyze_dead_code(self) -> list[dict[str, object]]:
        # This is a placeholder - real implementation would use vulture or similar
        issues = []
        for py_file in self.project_path.rglob("*.py"):
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                lines = content.splitlines()
                [
                    line.strip()
                    for line in lines
                    if line.strip().startswith("import ")
                    or line.strip().startswith("from ")
                ]

                # Simple heuristic: if import line contains "unused" comment
                for i, line in enumerate(lines):
                    if (
                        "import " in line or "from " in line
                    ) and "# unused" in line.lower():
                        issues.append(
                            {
                                "file": str(py_file.relative_to(self.project_path)),
                                "line": i + 1,
                                "type": "unused_import",
                                "message": f"Potentially unused import: {line.strip()}",
                            },
                        )
            except (RuntimeError, ValueError, TypeError) as e:
                logger.warning("Error checking dead code in %s: %s", py_file, e)

        return issues

    def _analyze_duplicates(self) -> list[dict[str, object]]:
        # This is a placeholder - real implementation would do more sophisticated analysis
        issues = []

        file_contents = {}
        for py_file in self.project_path.rglob("*.py"):
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()
                    if len(content.strip()) > 100:
                        # Only check substantial files
                        file_contents[py_file] = content
            except (RuntimeError, ValueError, TypeError) as e:
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

                    if similarity > 0.8:  # 80% similarity threshold
                        issues.append(
                            {
                                "type": "duplicate_files",
                                "files": [
                                    str(file1.relative_to(self.project_path)),
                                    str(file2.relative_to(self.project_path)),
                                ],
                                "similarity": similarity,
                                "message": f"High similarity ({similarity:.1%}) between files",
                            },
                        )

        return issues
