# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Hooks system - Protocol-based hook lifecycle management."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_quality.hooks.base import *
    from flext_quality.hooks.manager import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityBaseHook": "flext_quality.hooks.base",
    "FlextQualityHookManager": "flext_quality.hooks.manager",
    "base": "flext_quality.hooks.base",
    "manager": "flext_quality.hooks.manager",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
