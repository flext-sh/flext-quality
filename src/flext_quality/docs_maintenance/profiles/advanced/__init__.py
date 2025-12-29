"""Documentation maintenance and quality assurance tools.

This package contains tools for maintaining documentation quality,
including content auditing, link validation, and style checking.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .format_markdown import FlextQualityMarkdownFormatting
from .sync_references import FlextQualityCrossReferenceSync
from .validate_markdown import FlextQualityMarkdownValidation

__version__ = "0.1.0"

__all__ = [
    "FlextQualityCrossReferenceSync",
    "FlextQualityMarkdownFormatting",
    "FlextQualityMarkdownValidation",
]
