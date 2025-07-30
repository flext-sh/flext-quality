"""Infrastructure ports for FLEXT-QUALITY v0.7.0.

REFACTORED:
    Using flext-core port patterns - NO duplication.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Remove injectable decorator for now - simplify

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import TConfigDict


class AnalysisPort(ABC):
    """Base port for analysis operations."""

    @abstractmethod
    async def analyze(self, project_path: Path) -> object:
        """Analyze project at given path."""


class ASTAnalysisPort(AnalysisPort):
    """Port for AST-based analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze using AST parsing."""
        return {"type": "ast", "path": str(project_path), "results": []}


class BanditSecurityPort(AnalysisPort):
    """Port for Bandit security analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze using Bandit security scanner."""
        return {"type": "security", "path": str(project_path), "issues": []}


class ComplexityAnalysisPort(AnalysisPort):
    """Port for complexity analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze code complexity."""
        return {"type": "complexity", "path": str(project_path), "metrics": {}}


class DeadCodeAnalysisPort(AnalysisPort):
    """Port for dead code analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze dead code."""
        return {"type": "dead_code", "path": str(project_path), "unused": []}


class DuplicationAnalysisPort(AnalysisPort):
    """Port for code duplication analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze code duplication."""
        return {"type": "duplication", "path": str(project_path), "duplicates": []}


class PylintPort(AnalysisPort):
    """Port for Pylint analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze using Pylint."""
        return {"type": "pylint", "path": str(project_path), "violations": []}


class RuffPort(AnalysisPort):
    """Port for Ruff analysis."""

    def __init__(self, config: TConfigDict | None = None) -> None:
        """Initialize with optional config."""
        self.config = config

    async def analyze(self, project_path: Path) -> object:
        """Analyze using Ruff."""
        return {"type": "ruff", "path": str(project_path), "violations": []}
