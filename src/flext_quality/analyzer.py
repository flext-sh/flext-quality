"""Code analyzer interface for FLEXT Quality."""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Main code analyzer interface for FLEXT Quality."""

    def __init__(self, project_path: str | Path) -> None:
        """Initialize code analyzer.

        Args:
            project_path: Path to the project to analyze.

        """
        self.project_path = Path(project_path)
        self.analysis_results: dict[str, Any] = {}

    def analyze_project(
        self,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> dict[str, Any]:
        """Analyze the entire project.

        Args:
            include_security: Include security analysis.
            include_complexity: Include complexity analysis.
            include_dead_code: Include dead code detection.
            include_duplicates: Include duplicate code detection.

        Returns:
            Analysis results dictionary.

        """
        logger.info("Starting project analysis: %s", self.project_path)

        results = {
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

        # Analyze each file
        file_metrics = []
        for file_path in python_files:
            metrics = self._analyze_file(file_path)
            if metrics:
                file_metrics.append(metrics)
                results["total_lines"] += metrics.get("lines_of_code", 0)

        # Calculate overall metrics
        results["metrics"] = self._calculate_overall_metrics(file_metrics)

        # Run specialized analyses
        if include_security:
            results["issues"]["security"] = self._analyze_security()

        if include_complexity:
            results["issues"]["complexity"] = self._analyze_complexity(file_metrics)

        if include_dead_code:
            results["issues"]["dead_code"] = self._analyze_dead_code()

        if include_duplicates:
            results["issues"]["duplicates"] = self._analyze_duplicates()

        self.analysis_results = results

        logger.info(
            "Analysis completed. Files: %d, Lines: %d",
            results["files_analyzed"],
            results["total_lines"],
        )

        return results

    def get_quality_score(self) -> float:
        """Calculate overall quality score (0-100).

        Returns:
            Quality score from 0 to 100.

        """
        if not self.analysis_results:
            return 0.0

        self.analysis_results.get("metrics", {})
        issues = self.analysis_results.get("issues", {})

        # Base score
        score = 100.0

        # Deduct for complexity issues
        complexity_penalty = len(issues.get("complexity", [])) * 5
        score -= min(complexity_penalty, 30)

        # Deduct for security issues
        security_penalty = len(issues.get("security", [])) * 10
        score -= min(security_penalty, 40)

        # Deduct for dead code
        dead_code_penalty = len(issues.get("dead_code", [])) * 3
        score -= min(dead_code_penalty, 20)

        # Deduct for duplicates
        duplicate_penalty = len(issues.get("duplicates", [])) * 5
        score -= min(duplicate_penalty, 25)

        return max(0.0, score)

    def get_quality_grade(self) -> str:
        """Get letter grade for quality score.

        Returns:
            Letter grade (A+ to F).

        """
        score = self.get_quality_score()

        if score >= 95:
            return "A+"
        if score >= 90:
            return "A"
        if score >= 85:
            return "A-"
        if score >= 80:
            return "B+"
        if score >= 75:
            return "B"
        if score >= 70:
            return "B-"
        if score >= 65:
            return "C+"
        if score >= 60:
            return "C"
        if score >= 55:
            return "C-"
        if score >= 50:
            return "D+"
        if score >= 45:
            return "D"
        return "F"

    def _find_python_files(self) -> list[Path]:
        """Find all Python files in the project."""
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

    def _analyze_file(self, file_path: Path) -> dict[str, Any] | None:
        """Analyze a single Python file."""
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
                ]
            )
            comment_lines = len(
                [line for line in lines if line.strip().startswith("#")]
            )
            blank_lines = len([line for line in lines if not line.strip()])

            # AST analysis
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

        except Exception as e:
            logger.exception("Error analyzing file %s: %s", file_path, e)
            return None

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity (simplified version)."""
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
        self, file_metrics: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Calculate overall project metrics."""
        if not file_metrics:
            return {}

        total_files = len(file_metrics)
        total_loc = sum(m.get("lines_of_code", 0) for m in file_metrics)
        total_functions = sum(m.get("function_count", 0) for m in file_metrics)
        total_classes = sum(m.get("class_count", 0) for m in file_metrics)

        avg_complexity = sum(m.get("complexity", 0) for m in file_metrics) / total_files
        max_complexity = max(m.get("complexity", 0) for m in file_metrics)

        return {
            "total_files": total_files,
            "total_lines_of_code": total_loc,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": avg_complexity,
            "max_complexity": max_complexity,
            "avg_lines_per_file": total_loc / total_files if total_files > 0 else 0,
        }

    def _analyze_security(self) -> list[dict[str, Any]]:
        """Analyze security issues (simplified)."""
        # This is a simplified implementation
        # In production, this would integrate with bandit or similar tools
        issues = []

        for py_file in self._find_python_files():
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                # Simple security checks
                if "eval(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "dangerous_function",
                            "message": "Use of eval() detected",
                            "severity": "high",
                        }
                    )

                if "exec(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "dangerous_function",
                            "message": "Use of exec() detected",
                            "severity": "high",
                        }
                    )

                if "import os" in content and "os.system(" in content:
                    issues.append(
                        {
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "command_injection",
                            "message": "Potential command injection with os.system()",
                            "severity": "medium",
                        }
                    )

            except Exception as e:
                logger.warning("Error checking security in %s: %s", py_file, e)

        return issues

    def _analyze_complexity(
        self, file_metrics: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Analyze complexity issues."""
        complexity_threshold = 10

        return [{
                        "file": metrics["file_path"],
                        "type": "high_complexity",
                        "message": f"High complexity: {metrics['complexity']}",
                        "complexity": metrics["complexity"],
                        "threshold": complexity_threshold,
                    } for metrics in file_metrics if metrics.get("complexity", 0) > complexity_threshold]

    def _analyze_dead_code(self) -> list[dict[str, Any]]:
        """Analyze dead code (simplified)."""
        # This is a placeholder - real implementation would use vulture or similar
        issues = []

        # Simple check for unused imports
        for py_file in self._find_python_files():
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
                            }
                        )

            except Exception as e:
                logger.warning("Error checking dead code in %s: %s", py_file, e)

        return issues

    def _analyze_duplicates(self) -> list[dict[str, Any]]:
        """Analyze duplicate code (simplified)."""
        # This is a placeholder - real implementation would do more sophisticated analysis
        issues = []

        file_contents = {}
        for py_file in self._find_python_files():
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()
                    if len(content.strip()) > 100:  # Only check substantial files
                        file_contents[py_file] = content
            except Exception as e:
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
                            }
                        )

        return issues
