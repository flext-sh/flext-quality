"""Analysis backends for the code analyzer.

This module provides a pluggable architecture for different code analysis backends.
Each backend can provide different analysis capabilities.
"""

from __future__ import annotations

from flext_quality.backends.ast_backend import ASTBackend
from flext_quality.backends.base import (
    BackendType,
    BaseAnalyzer,
)
from flext_quality.backends.external_backend import (
    ExternalBackend,
)

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
    "AVAILABLE_BACKENDS",
    "ASTBackend",
    "BackendType",
    "BaseAnalyzer",
    "ExternalBackend",
    "get_all_backends",
    "get_backend",
    "get_default_backends",
]
