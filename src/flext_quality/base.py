"""Base class for analysis backends using flext-core patterns."""

from __future__ import annotations

import warnings
from abc import abstractmethod
from pathlib import Path

from flext_core import FlextAbstractMixin

from flext_quality.backend_type import BackendType


class FlextQualityAnalyzer(FlextAbstractMixin):
    """Abstract base class for code analyzers using flext-core patterns."""

    @abstractmethod
    def analyze(self, code: str, file_path: Path | None = None) -> dict[str, object]:
        """Analyze code and return results.

        Args:
            code: Source code to analyze
            file_path: Optional file path for context

        Returns:
            Dictionary containing analysis results

        """
        ...

    @abstractmethod
    def get_backend_type(self) -> BackendType:
        """Get the type of this backend.

        Returns:
            BackendType enum value

        """
        ...

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get list of capabilities this backend provides.

        Returns:
            List of capability strings

        """
        ...


# Legacy compatibility facade (temporary)
BaseAnalyzer = FlextQualityAnalyzer
warnings.warn(
    "BaseAnalyzer is deprecated; use FlextQualityAnalyzer",
    DeprecationWarning,
    stacklevel=2,
)
