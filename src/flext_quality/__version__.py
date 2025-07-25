"""Version information for flext-quality package.

This module contains version information for the flext-quality package.
"""

from __future__ import annotations

import importlib.metadata

# Import from centralized version management system
# 🚨 ARCHITECTURAL COMPLIANCE: DI container
from flext_quality.infrastructure.di_container import get_service_result

FlextResult = get_service_result()

try:
    __version__ = importlib.metadata.version("flext-quality")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.8.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# FLEXT Enterprise - Unified Versioning System
# Version is managed centrally in flext_core.version
# This maintains backward compatibility while eliminating duplication.
