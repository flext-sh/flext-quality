# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services - Business logic layer (Tier 3)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality.services.cli import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityCliService": "flext_quality.services.cli",
    "cli": "flext_quality.services.cli",
    "main": "flext_quality.services.cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
