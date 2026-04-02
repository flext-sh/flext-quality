# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Rules engine - YAML-based declarative rules system."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_quality.rules import engine, loader, validators
    from flext_quality.rules.engine import FlextQualityRulesEngine
    from flext_quality.rules.loader import FlextQualityRulesLoader
    from flext_quality.rules.validators import FlextQualityValidators

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextQualityRulesEngine": "flext_quality.rules.engine",
    "FlextQualityRulesLoader": "flext_quality.rules.loader",
    "FlextQualityValidators": "flext_quality.rules.validators",
    "engine": "flext_quality.rules.engine",
    "loader": "flext_quality.rules.loader",
    "validators": "flext_quality.rules.validators",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
