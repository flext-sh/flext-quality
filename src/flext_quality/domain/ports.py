"""Domain service interfaces for FLEXT-QUALITY.

REFACTORED:
Defines service interfaces following clean architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import FlextResult, TAnyDict


# Using flext-core and ABC directly - no duplicate aliases


class AnalysisService(ABC):
    """Service interface for code analysis operations."""

    @abstractmethod
    async def analyze_project(
        self,
        project_path: Path,
        include_security: bool = True,
        include_complexity: bool = True,
        include_dead_code: bool = True,
        include_duplicates: bool = True,
    ) -> FlextResult[TAnyDict]:
        """Analyze a complete project with configurable analysis types."""
        ...

    @abstractmethod
    async def analyze_file(
        self,
        file_path: Path,
        analysis_types: list[str] | None = None,
    ) -> FlextResult[TAnyDict]:
        """Analyze a single file with specified analysis types."""
        ...

    @abstractmethod
    async def calculate_quality_score(
        self,
        analysis_results: TAnyDict,
    ) -> FlextResult[TAnyDict]:
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
    ) -> FlextResult[TAnyDict]:
        """Analyze project for security vulnerabilities."""
        ...

    @abstractmethod
    async def scan_file(
        self,
        file_path: Path,
        severity_threshold: str = "medium",
    ) -> FlextResult[TAnyDict]:
        """Scan a single file for security issues."""
        ...

    @abstractmethod
    async def validate_dependencies(
        self,
        project_path: Path,
    ) -> FlextResult[TAnyDict]:
        """Validate project dependencies for known vulnerabilities."""
        ...


class LintingService(ABC):
    """Service interface for code linting."""

    @abstractmethod
    async def lint_project(
        self,
        project_path: Path,
        fix: bool = False,
    ) -> FlextResult[TAnyDict]:
        """Lint entire project with optional auto-fix."""
        ...

    @abstractmethod
    async def lint_file(
        self,
        file_path: Path,
        fix: bool = False,
    ) -> FlextResult[TAnyDict]:
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
        analysis_results: TAnyDict,
        output_format: str = "html",
        output_path: Path | None = None,
    ) -> FlextResult[str]: ...

    @abstractmethod
    async def generate_summary(
        self,
        analysis_results: TAnyDict,
    ) -> FlextResult[TAnyDict]: ...

    @abstractmethod
    async def export_metrics(
        self,
        analysis_results: TAnyDict,
        output_format: str = "json",
    ) -> FlextResult[str]: ...


class ComplexityAnalyzerService(ABC):
    """Service interface for code complexity analysis."""

    @abstractmethod
    async def analyze_complexity(
        self,
        project_path: Path,
        threshold: int = 10,
    ) -> FlextResult[list[TAnyDict]]: ...

    @abstractmethod
    async def calculate_cyclomatic_complexity(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, int]]: ...

    @abstractmethod
    async def calculate_cognitive_complexity(
        self,
        file_path: Path,
    ) -> FlextResult[dict[str, int]]: ...


class DeadCodeDetectorService(ABC):
    """Service interface for dead code detection."""

    @abstractmethod
    async def detect_dead_code(
        self,
        project_path: Path,
    ) -> FlextResult[list[TAnyDict]]: ...

    @abstractmethod
    async def find_unused_imports(
        self,
        file_path: Path,
    ) -> FlextResult[list[str]]: ...

    @abstractmethod
    async def find_unused_variables(
        self,
        file_path: Path,
    ) -> FlextResult[list[TAnyDict]]: ...


class DuplicateDetectorService(ABC):
    """Service interface for duplicate code detection."""

    @abstractmethod
    async def detect_duplicates(
        self,
        project_path: Path,
        min_lines: int = 5,
        similarity_threshold: float = 0.8,
    ) -> FlextResult[list[TAnyDict]]: ...

    @abstractmethod
    async def find_similar_functions(
        self,
        project_path: Path,
        similarity_threshold: float = 0.8,
    ) -> FlextResult[list[TAnyDict]]: ...

    @abstractmethod
    async def calculate_duplication_ratio(
        self,
        project_path: Path,
    ) -> FlextResult[float]: ...


class MetricsCollectorService(ABC):
    """Service interface for quality metrics collection."""

    @abstractmethod
    async def collect_metrics(
        self,
        project_path: Path,
    ) -> FlextResult[TAnyDict]: ...

    @abstractmethod
    async def calculate_maintainability_index(
        self,
        project_path: Path,
    ) -> FlextResult[float]: ...

    @abstractmethod
    async def calculate_technical_debt(
        self,
        project_path: Path,
    ) -> FlextResult[TAnyDict]: ...
