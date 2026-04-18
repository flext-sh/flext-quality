# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-quality.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion


class FlextQualityVersion(FlextVersion):
    """flext-quality version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata = metadata("flext-quality")


__version__ = FlextQualityVersion.__version__
__version_info__ = FlextQualityVersion.__version_info__
__title__ = FlextQualityVersion.__title__
__description__ = FlextQualityVersion.__description__
__author__ = FlextQualityVersion.__author__
__author_email__ = FlextQualityVersion.__author_email__
__license__ = FlextQualityVersion.__license__
__url__ = FlextQualityVersion.__url__
__all__: list[str] = [
    "FlextQualityVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
