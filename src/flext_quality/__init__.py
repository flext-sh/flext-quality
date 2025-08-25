"""Analysis backends for the code analyzer.

This module provides a pluggable architecture for different code analysis
backends. Each backend can provide different analysis capabilities and we
re-export the primary types for convenient imports in examples and tests.
"""

from __future__ import annotations

# Core backend classes
from flext_quality.ast_backend import ASTBackend
from flext_quality.backend_type import BackendType
from flext_quality.base import BaseAnalyzer
from flext_quality.external_backend import ExternalBackend

# Main analyzer classes
from flext_quality.analyzer import CodeAnalyzer

# Analysis types and results
from flext_quality.analysis_types import (
    AnalysisResults,
    ComplexityIssue,
    DeadCodeIssue,
    DuplicationIssue,
    FileAnalysisResult,
    OverallMetrics,
    SecurityIssue,
)

# Utilities
from flext_quality.utilities import FlextTestUtilities

# Grade calculator
from flext_quality.grade_calculator import FlextQualityGradeCalculator

# Create alias for backward compatibility
QualityGradeCalculator = FlextQualityGradeCalculator

# Registry of available backends
AVAILABLE_BACKENDS: dict[str, type[BaseAnalyzer]] = {
    "ast": ASTBackend,
    "external": ExternalBackend,
}

# Default backend configuration
DEFAULT_BACKENDS = ["ast", "external"]


def get_backend(name: str) -> type[BaseAnalyzer]:
    """Get a backend by name."""
    if name not in AVAILABLE_BACKENDS:
        msg = (
            f"Backend '{name}' not found. Available: {list(AVAILABLE_BACKENDS.keys())}"
        )
        raise ValueError(msg)
    return AVAILABLE_BACKENDS[name]


def get_all_backends() -> list[type[BaseAnalyzer]]:
    """Get all available backends."""
    return list(AVAILABLE_BACKENDS.values())


def get_default_backends() -> list[type[BaseAnalyzer]]:
    """Get the default backends."""
    return [AVAILABLE_BACKENDS[name] for name in DEFAULT_BACKENDS]


__all__: list[str] = [
    # Backend system
    "AVAILABLE_BACKENDS",
    "ASTBackend",
    "BackendType",
    "BaseAnalyzer",
    "ExternalBackend",
    "get_all_backends",
    "get_backend",
    "get_default_backends",
    # Main analyzer
    "CodeAnalyzer",
    # Analysis types
    "AnalysisResults",
    "ComplexityIssue",
    "DeadCodeIssue",
    "DuplicationIssue",
    "FileAnalysisResult",
    "OverallMetrics",
    "SecurityIssue",
    # Utilities
    "FlextTestUtilities",
    # Grade calculator
    "FlextQualityGradeCalculator",
    "QualityGradeCalculator",  # Legacy alias
]
