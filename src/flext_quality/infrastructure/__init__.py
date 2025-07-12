"""Infrastructure layer for FLEXT-QUALITY.

Using flext-core patterns - NO duplication, clean architecture.
"""

from __future__ import annotations

# Import infrastructure components
from flext_quality.infrastructure.config import QualityConfig
from flext_quality.infrastructure.container import (
    QualityContainer,
    configure_quality_dependencies,
    get_quality_container,
)

__all__ = [
    "QualityConfig",
    "QualityContainer",
    "configure_quality_dependencies",
    "get_quality_container",
]
