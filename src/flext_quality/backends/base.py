"""Base class for analysis backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


class BackendType(Enum):
    """Enumeration of backend types."""

    AST = "ast"
    EXTERNAL = "external"
    HYBRID = "hybrid"


class BaseAnalyzer(ABC):
    """Abstract base class for code analyzers."""

    @abstractmethod
    def analyze(self, code: str, file_path: Path | None = None) -> dict[str, Any]:
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
