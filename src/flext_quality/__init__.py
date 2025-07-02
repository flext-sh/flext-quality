"""FLEXT Quality - Enterprise Code Quality Analysis and Monitoring."""

from __future__ import annotations

__version__ = "0.5.0"
__author__ = "FLEXT Team"
__email__ = "dev@flext.sh"
__license__ = "MIT"

# Core analysis components
from .analyzer import CodeAnalyzer
from .cli import main as cli_main
from .metrics import QualityMetrics
from .reports import QualityReport

__all__ = [
    # Core components
    "CodeAnalyzer",
    "QualityMetrics",
    "QualityReport",
    "__author__",
    "__email__",
    "__license__",
    # Version and metadata
    "__version__",
    # CLI
    "cli_main",
]


def get_version() -> str:
    """Get the library version.

    Returns:
        The current version string.

    """
    return __version__


def get_info() -> dict[str, str]:
    """Get library information.

    Returns:
        Dictionary containing library metadata.

    """
    return {
        "name": "flext-quality",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "description": "Enterprise Code Quality Analysis and Monitoring for FLEXT Framework",
    }
