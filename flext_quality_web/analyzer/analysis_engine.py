"""Integrated code analysis engine for Django Code Analyzer."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import TYPE_CHECKING, cast

from django.utils import timezone
from flext_core import get_logger

if TYPE_CHECKING:
    from flext_core import TAnyDict
else:
    # Runtime type alias using flext-core patterns
    TAnyDict = dict[str, object]

from analyzer.models import (
    DeadCodeIssue,
    DuplicateCodeBlock,
    FileAnalysis,
    QualityMetrics,
    SecurityIssue,
)

if TYPE_CHECKING:
    from analyzer.models import AnalysisSession

logger = get_logger(__name__)


class CodeAnalysisEngine:
    """Comprehensive code analysis engine."""

    def __init__(self, session: AnalysisSession) -> None:
        """Initialize analysis engine with session context."""
        self.session = session
        self.flx_project = session.flx_project
        self.project_path = Path(self.flx_project.path)
        self.results: TAnyDict = {
            "files_analyzed": 0,
            "total_lines": 0,
            "security_issues": [],
            "dead_code_issues": [],
            "duplicate_blocks": [],
            "quality_metrics": {},
        }

    def run_analysis(self) -> bool:
        """Run comprehensive analysis on the project."""
        try:
            logger.info("Starting analysis for project %s", self.flx_project.name)

            # Update session status
            self.session.status = "running"
            self.session.started_at = timezone.now()
            self.session.save()

            # Find and analyze Python files
            python_files = self._find_python_files()
            if not python_files:
                return self._handle_no_files_error()

            # Analyze individual files
            for file_path in python_files:
                self._analyze_file(file_path)

            # Run additional analyses
            if self.session.include_security:
                self._run_security_analysis()

            if self.session.include_dead_code:
                self._run_dead_code_analysis()

            if self.session.include_duplicates:
                self._run_duplicate_analysis()

            # Calculate quality metrics
            self._calculate_quality_metrics()

            # Update session completion
            self.session.status = "completed"
            self.session.completed_at = timezone.now()
            quality_metrics = self.results.get("quality_metrics", {})
            if quality_metrics and isinstance(quality_metrics, dict):
                self.session.overall_score = quality_metrics.get("overall_score", 0.0)
            else:
                self.session.overall_score = 0.0
            self.session.quality_grade = self._calculate_grade(
                self.session.overall_score or 0.0,
            )
            self.session.save()

            logger.info(
                "Analysis completed successfully for: %s",
                self.flx_project.name,
            )
            return True

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Analysis failed for project %s", self.flx_project.name)
            self.session.status = "failed"
            self.session.error_message = str(e)
            self.session.completed_at = timezone.now()
            self.session.save()
            return False

    def _find_python_files(self) -> list[Path]:
        """Find all Python files in the project."""
        if not self.project_path.exists():
            msg: str = f"Project path does not exist: {self.project_path}"
            raise FileNotFoundError(msg)

        # Skip hidden files and directories
        python_files = [
            py_file
            for py_file in self.project_path.rglob("*.py")
            if not any(part.startswith(".") for part in py_file.parts)
        ]

        logger.info("Found %s Python files", len(python_files))
        return python_files

    def _analyze_file(self, file_path: Path) -> FileAnalysis | None:
        """Analyze a single Python file."""
        try:
            with file_path.open(encoding="utf-8") as f:
                content = f.read()

            # Basic file metrics
            lines = content.splitlines()
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

            # Parse AST for complexity analysis
            try:
                tree = ast.parse(content)
                function_count = len(
                    [
                        node
                        for node in ast.walk(tree)
                        if isinstance(node, ast.FunctionDef)
                    ],
                )
                class_count = len(
                    [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
                )

                # Simple complexity calculation
                complexity = 1
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.While, ast.For, ast.FunctionDef)):
                        complexity += 1
                avg_complexity = complexity / max(function_count, 1)

            except SyntaxError:
                avg_complexity = 0
                function_count = 0
                class_count = 0

            # Create FileAnalysis record
            relative_path = str(file_path.relative_to(self.project_path))

            file_analysis = FileAnalysis.objects.create(
                session=self.session,
                file_path=relative_path,
                file_name=file_path.name,
                lines_of_code=lines_of_code,
                comment_lines=comment_lines,
                blank_lines=blank_lines,
                complexity_score=float(avg_complexity),
                maintainability_score=75.0,  # Placeholder
                function_count=function_count,
                class_count=class_count,
            )

            # Type-safe operations using flext-core patterns with cast
            current_files = cast("int", self.results.get("files_analyzed", 0))
            self.results["files_analyzed"] = current_files + 1
            current_lines = cast("int", self.results.get("total_lines", 0))
            self.results["total_lines"] = current_lines + len(lines)
            return file_analysis

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Error analyzing file %s", file_path)
        return None

    def _run_security_analysis(self) -> None:
        """Run basic security analysis."""
        try:
            logger.info("Running security analysis")

            # Simple security checks
            for py_file in self._find_python_files():
                try:
                    with py_file.open(encoding="utf-8") as f:
                        content = f.read()

                    lines = content.splitlines()
                    for i, line in enumerate(lines, 1):
                        # Check for potential security issues
                        if "password" in line.lower() and "=" in line:
                            SecurityIssue.objects.create(
                                session=self.session,
                                severity="HIGH",
                                confidence="MEDIUM",
                                issue_type="hardcoded_password",
                                test_id="B105",
                                file_path=str(py_file.relative_to(self.project_path)),
                                line_number=i,
                                description="Potential hardcoded password",
                                recommendation=(
                                    "Use environment variables or secure storage"
                                ),
                                code_snippet=line.strip(),
                            )

                except (OSError, UnicodeDecodeError) as e:
                    logger.warning("Could not scan %s: %s", py_file, e)

            count = SecurityIssue.objects.filter(session=self.session).count()
            logger.info("Found %s security issues", count)

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Security analysis failed")

    def _run_dead_code_analysis(self) -> None:
        """Run basic dead code analysis."""
        try:
            logger.info("Running dead code analysis")

            # Simple dead code detection
            for py_file in self._find_python_files():
                try:
                    with py_file.open(encoding="utf-8") as f:
                        content = f.read()

                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and (
                            node.name.startswith("_unused_")
                            or node.name.endswith("_old")
                        ):
                            DeadCodeIssue.objects.create(
                                session=self.session,
                                dead_type="function",
                                name=node.name,
                                file_path=str(py_file.relative_to(self.project_path)),
                                line_number=node.lineno,
                                confidence=0.7,
                                size_estimate=10,
                            )

                except (OSError, UnicodeDecodeError, SyntaxError) as e:
                    logger.warning("Could not analyze %s: %s", py_file, e)

            count = DeadCodeIssue.objects.filter(session=self.session).count()
            logger.info("Found %s dead code issues", count)

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Dead code analysis failed")

    def _run_duplicate_analysis(self) -> None:
        """Run basic duplicate code analysis."""
        try:
            logger.info("Running duplicate code analysis")

            # This is a placeholder for duplicate detection
            # In a real implementation, you would compare code blocks
            count = DuplicateCodeBlock.objects.filter(session=self.session).count()
            logger.info("Found %s duplicate blocks", count)

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Duplicate analysis failed")

    def _calculate_quality_metrics(self) -> None:
        """Calculate overall quality metrics."""
        try:
            # Get file analyses
            file_analyses = FileAnalysis.objects.filter(session=self.session)

            if not file_analyses.exists():
                return

            # Basic metrics
            total_files = file_analyses.count()
            total_lines = sum(fa.lines_of_code for fa in file_analyses)
            total_functions = sum(fa.function_count for fa in file_analyses)
            total_classes = sum(fa.class_count for fa in file_analyses)

            # Complexity metrics
            avg_complexity = (
                sum(fa.complexity_score for fa in file_analyses) / total_files
            )
            max_complexity = max(fa.complexity_score for fa in file_analyses)
            complex_functions_count = sum(
                1
                for fa in file_analyses
                if fa.complexity_score > self.session.complexity_threshold
            )

            # Issue counts
            security_issues_count = SecurityIssue.objects.filter(
                session=self.session,
            ).count()
            dead_code_items_count = DeadCodeIssue.objects.filter(
                session=self.session,
            ).count()
            duplicate_blocks_count = DuplicateCodeBlock.objects.filter(
                session=self.session,
            ).count()

            # Calculate component scores (0-100)
            complexity_score = max(0, 100 - (avg_complexity * 10))
            security_score = max(0, 100 - (security_issues_count * 5))
            maintainability_score = max(0, 100 - (complex_functions_count * 10))
            duplication_score = max(0, 100 - (duplicate_blocks_count * 10))
            documentation_score = 75  # Placeholder

            # Overall score (weighted average)
            overall_score = (
                complexity_score * 0.25
                + security_score * 0.25
                + maintainability_score * 0.2
                + duplication_score * 0.15
                + documentation_score * 0.15
            )

            # Create QualityMetrics record
            QualityMetrics.objects.create(
                session=self.session,
                overall_score=overall_score,
                complexity_score=complexity_score,
                maintainability_score=maintainability_score,
                security_score=security_score,
                documentation_score=documentation_score,
                duplication_score=duplication_score,
                total_files=total_files,
                total_lines=total_lines,
                total_functions=total_functions,
                total_classes=total_classes,
                avg_complexity=avg_complexity,
                max_complexity=max_complexity,
                complex_functions_count=complex_functions_count,
                docstring_coverage=0.5,
                documented_functions=int(total_functions * 0.5),
                security_issues_count=security_issues_count,
                dead_code_items_count=dead_code_items_count,
                duplicate_blocks_count=duplicate_blocks_count,
                duplicate_lines_ratio=0.1,
                technical_debt_ratio=max_complexity / 10 if max_complexity > 0 else 0,
                estimated_debt_hours=complex_functions_count * 2,
            )

            self.results["quality_metrics"] = {
                "overall_score": overall_score,
                "complexity_score": complexity_score,
                "security_score": security_score,
                "maintainability_score": maintainability_score,
                "duplication_score": duplication_score,
                "documentation_score": documentation_score,
            }

            logger.info(
                "Quality metrics calculated. Overall score: %.1f",
                overall_score,
            )

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Quality metrics calculation failed")

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        grade_thresholds = [
            (90, "A+"),
            (85, "A"),
            (80, "A-"),
            (75, "B+"),
            (70, "B"),
            (65, "B-"),
            (60, "C+"),
            (55, "C"),
            (50, "C-"),
            (45, "D+"),
            (40, "D"),
        ]

        for threshold, grade in grade_thresholds:
            if score >= threshold:
                return grade
        return "F"

    def _handle_no_files_error(self) -> bool:
        """Handle the error case when no Python files are found."""
        msg = "No Python files found in project path"
        raise ValueError(msg)
