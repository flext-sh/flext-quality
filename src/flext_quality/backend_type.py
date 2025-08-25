"""Backend type enumeration for FLEXT Quality."""

from __future__ import annotations

from enum import Enum


class BackendType(Enum):
    """Enumeration of backend types."""

    AST = "ast"
    EXTERNAL = "external"
    HYBRID = "hybrid"
