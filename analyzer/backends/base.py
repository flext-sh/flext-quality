"""Base class for analysis backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from flext_core import get_logger

if TYPE_CHECKING:
    from pathlib import Path

    from analyzer.models import AnalysisSession

logger = get_logger(__name__)


class AnalysisResult:
    """Container for analysis results from a backend."""

    def __init__(self) -> None:
        """Initialize analysis result container."""
        self.packages: list[dict[str, Any]] = []
        self.files: list[dict[str, Any]] = []
        self.classes: list[dict[str, Any]] = []
        self.functions: list[dict[str, Any]] = []
        self.variables: list[dict[str, Any]] = []
        self.imports: list[dict[str, Any]] = []
        self.security_issues: list[dict[str, Any]] = []
        self.quality_metrics: dict[str, Any] = {}
        self.errors: list[dict[str, Any]] = []

    def merge(self, other: AnalysisResult) -> None:
        """Merge another AnalysisResult into this one."""
        self.packages.extend(other.packages)
        self.files.extend(other.files)
        self.classes.extend(other.classes)
        self.functions.extend(other.functions)
        self.variables.extend(other.variables)
        self.imports.extend(other.imports)
        self.security_issues.extend(other.security_issues)
        self.quality_metrics.update(other.quality_metrics)
        self.errors.extend(other.errors)


class AnalysisBackend(ABC):
    """Abstract base class for analysis backends."""

    def __init__(self, session: AnalysisSession, project_path: Path) -> None:
        """Initialize analysis backend with session and project path."""
        self.session = session
        self.project_path = project_path
        self.logger = FlextLoggerFactory.get_logger(__name__ + "." + self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this backend."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of this backend."""
        ...

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """Return the capabilities of this backend."""
        ...

    @abstractmethod
    def analyze(self, python_files: list[Path]) -> AnalysisResult:
        """Analyze the given Python files."""
        ...

    def is_available(self) -> bool:
        """Check if this backend is available."""
        return True

    def get_configuration(self) -> dict[str, Any]:
        """Get the configuration for this backend."""
        return {}

    def validate_configuration(self, _config: dict[str, Any]) -> bool:
        """Validate the configuration for this backend."""
        return True

    def _find_python_files(self, path: Path) -> list[Path]:
        """Find Python files in the given path."""
        python_files: list[Path] = []
        try:
            # Skip hidden files and directories
            python_files.extend(
                py_file
                for py_file in path.rglob("*.py")
                if not any(part.startswith(".") for part in py_file.parts)
            )
        except Exception:
            self.logger.exception("Error finding Python files in %s", path)

        return python_files

    def _get_relative_path(self, file_path: Path) -> str:
        """Get the relative path from the project root."""
        try:
            return str(file_path.relative_to(self.project_path))
        except ValueError:
            return str(file_path)

    def _get_package_name(self, file_path: Path) -> str:
        """Get the package name for a file path."""
        try:
            relative_path = file_path.relative_to(self.project_path)
            parts = list(relative_path.parts[:-1])  # Remove filename
            if parts and parts[-1] == "__pycache__":
                parts = parts[:-1]
            return ".".join(parts) if parts else "__main__"
        except ValueError:
            return "__main__"
