"""Domain service interfaces for FLEXT-QUALITY.

REFACTORED:
Defines service interfaces following clean architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from flext_core import FlextResult


# Using flext-core and ABC directly - no duplicate aliases
class AnalysisService(ABC):
    """Service interface for code analysis operations."""

    @abstractmethod
    async def analyze_project(
        self,
        project_path: Path,
        *,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> FlextResult[dict[str, object]]:
        """Analyze a complete project with configurable analysis types."""
        ...

    @abstractmethod
    async def analyze_file(
        self,
        file_path: Path,
        analysis_types: list[str] | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Analyze a single file with specified analysis types."""
        ...

    @abstractmethod
    async def calculate_quality_score(
        self,
        analysis_results: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Calculate overall quality score from analysis results."""
        ...

    @abstractmethod
    async def get_quality_grade(self, quality_score: float) -> FlextResult[str]:
        """Convert quality score to letter grade (A, B, C, D, F)."""
        ...


class SecurityAnalyzerService(ABC):
    """Service interface for security analysis."""

    @abstractmethod
    async def analyze_security(
        self,
        project_path: Path,
        severity_threshold: str = "medium",
    ) -> FlextResult[dict[str, object]]:
        """Analyze project for security vulnerabilities."""
        ...

    @abstractmethod
    async def scan_file(
        self,
        file_path: Path,
        severity_threshold: str = "medium",
    ) -> FlextResult[dict[str, object]]:
        """Scan a single file for security issues."""
        ...

    @abstractmethod
    async def validate_dependencies(
        self,
        project_path: Path,
    ) -> FlextResult[dict[str, object]]:
        """Validate project dependencies for known vulnerabilities."""
        ...


class LintingService(ABC):
    """Service interface for code linting."""

    @abstractmethod
    async def lint_project(
        self,
        project_path: Path,
        *,
        fix: bool = False,
    ) -> FlextResult[dict[str, object]]:
        """Lint entire project with optional auto-fix."""
        ...

    @abstractmethod
    async def lint_file(
        self,
        file_path: Path,
        *,
        fix: bool = False,
    ) -> FlextResult[dict[str, object]]:
        """Lint a single file with optional auto-fix."""
        ...

    @abstractmethod
    async def format_code(self, file_path: Path) -> FlextResult[bool]:
        """Format code in a file according to style guidelines."""
        ...


class ReportGeneratorService(ABC):
    """Service interface for quality report generation."""

    @abstractmethod
    async def generate_report(
        self,
        analysis_results: dict[str, object],
        output_format: str = "html",
        output_path: Path | None = None,
    ) -> FlextResult[str]:
        """Generate quality report from analysis results.

        Args:
            analysis_results: Dictionary containing analysis results
            output_format: Format for the report (default: html)
            output_path: Optional path to save the report
        Returns:
            FlextResult containing the generated report content or error

        """
        ...

    @abstractmethod
    async def generate_summary(
        self,
        analysis_results: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Generate summary from analysis results.

        Args:
            analysis_results: Dictionary containing analysis results
        Returns:
            FlextResult containing the generated summary or error

        """
        ...

    @abstractmethod
    async def export_metrics(
        self,
        analysis_results: dict[str, object],
        output_format: str = "json",
    ) -> FlextResult[str]:
        """Export analysis metrics in specified format.

        Args:
            analysis_results: Dictionary containing analysis results
            output_format: Export format (default: json)

        Returns:
            FlextResult containing the exported metrics or error

        """
        ...


class ComplexityAnalyzerService(ABC):
    """Service interface for code complexity analysis."""

    @abstractmethod
    async def analyze_complexity(
        self,
        project_path: Path,
        threshold: int = 10,
    ) -> FlextResult[list[dict[str, object]]]:
        """Analyze code complexity in project.

        Args:
            project_path: Path to the project directory
            threshold: Complexity threshold for reporting (default: 10)

        Returns:
            FlextResult containing list of complexity issues or error

        """
        ...

    @abstractmethod
    async def calculate_cyclomatic_complexity(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, int]]:
        """Calculate cyclomatic complexity for file.

        Args:
            file_path: Path to the Python file
        Returns:
            FlextResult containing complexity metrics or error

        """
        ...

    @abstractmethod
    async def calculate_cognitive_complexity(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, int]]:
        """Calculate cognitive complexity for file.

        Args:
            file_path: Path to the Python file
        Returns:
            FlextResult containing cognitive complexity metrics or error

        """
        ...


class DeadCodeDetectorService(ABC):
    """Service interface for dead code detection."""

    @abstractmethod
    async def detect_dead_code(
        self,
        project_path: Path,
    ) -> FlextResult[list[dict[str, object]]]:
        """Detect dead code in project.

        Args:
            project_path: Path to the project directory
        Returns:
            FlextResult containing list of dead code instances or error

        """
        ...

    @abstractmethod
    async def find_unused_imports(
        self,
        file_path: Path,
    ) -> FlextResult[list[str]]:
        """Find unused imports in file.

        Args:
            file_path: Path to the Python file
        Returns:
            FlextResult containing list of unused import names or error

        """
        ...

    @abstractmethod
    async def find_unused_variables(
        self,
        file_path: Path,
    ) -> FlextResult[list[dict[str, object]]]:
        """Find unused variables in file.

        Args:
            file_path: Path to the Python file
        Returns:
            FlextResult containing list of unused variable information or error

        """
        ...


class DuplicateDetectorService(ABC):
    """Service interface for duplicate code detection."""

    @abstractmethod
    async def detect_duplicates(
        self,
        project_path: Path,
        min_lines: int = 5,
        similarity_threshold: float = 0.8,
    ) -> FlextResult[list[dict[str, object]]]:
        """Detect duplicate code blocks in project.

        Args:
            project_path: Path to the project directory
            min_lines: Minimum lines for duplication detection (default: 5)
            similarity_threshold: Similarity threshold for detection (default: 0.8)

        Returns:
            FlextResult containing list of duplicate code blocks or error

        """
        ...

    @abstractmethod
    async def find_similar_functions(
        self,
        project_path: Path,
        similarity_threshold: float = 0.8,
    ) -> FlextResult[list[dict[str, object]]]:
        """Find similar functions in project.

        Args:
            project_path: Path to the project directory
            similarity_threshold: Similarity threshold for detection (default: 0.8)

        Returns:
            FlextResult containing list of similar function pairs or error

        """
        ...

    @abstractmethod
    async def calculate_duplication_ratio(
        self,
        project_path: Path,
    ) -> FlextResult[float]:
        """Calculate code duplication ratio for project.

        Args:
            project_path: Path to the project directory
        Returns:
            FlextResult containing the duplication ratio or error

        """
        ...


class MetricsCollectorService(ABC):
    """Service interface for quality metrics collection."""

    @abstractmethod
    async def collect_metrics(
        self,
        project_path: Path,
    ) -> FlextResult[dict[str, object]]:
        """Collect comprehensive quality metrics for project.

        Args:
            project_path: Path to the project directory
        Returns:
            FlextResult containing metrics dictionary or error

        """
        ...

    @abstractmethod
    async def calculate_maintainability_index(
        self,
        project_path: Path,
    ) -> FlextResult[float]:
        """Calculate maintainability index for project.

        Args:
            project_path: Path to the project directory
        Returns:
            FlextResult containing the maintainability index or error

        """
        ...

    @abstractmethod
    async def calculate_technical_debt(
        self,
        project_path: Path,
    ) -> FlextResult[dict[str, object]]:
        """Calculate technical debt metrics for project.

        Args:
            project_path: Path to the project directory
        Returns:
            FlextResult containing technical debt metrics or error

        """
        ...
