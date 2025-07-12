"""FLEXT Quality - Enterprise Code Quality Analysis and Monitoring.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

__version__ = "0.7.0"
__author__ = "FLEXT Team"
__email__ = "dev@flext.sh"
__license__ = "MIT"

# Core analysis components
from flext_quality.analyzer import CodeAnalyzer
from flext_quality.cli import main as cli_main
from flext_quality.metrics import QualityMetrics
from flext_quality.reports import QualityReport

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
    return __version__


def get_info() -> dict[str, str]:
    return {
        "name": "flext-quality",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "description": "Enterprise Code Quality Analysis and Monitoring for FLEXT Framework",
    }
