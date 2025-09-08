"""Version information for flext-quality package.

This module contains version information for the flext-quality package.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


import importlib.metadata

try:
    __version__ = importlib.metadata.version("flext-quality")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# FLEXT Enterprise - Unified Versioning System
# Version is managed centrally in flext_core.version
# This maintains backward compatibility while eliminating duplication.
