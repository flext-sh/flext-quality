# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Rules engine - YAML-based declarative rules system."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.rules import (
        engine as engine,
        loader as loader,
        validators as validators,
    )
    from flext_quality.rules.engine import (
        FlextQualityRulesEngine as FlextQualityRulesEngine,
    )
    from flext_quality.rules.loader import (
        FlextQualityRulesLoader as FlextQualityRulesLoader,
    )
    from flext_quality.rules.validators import (
        FlextQualityValidators as FlextQualityValidators,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityRulesEngine": [
        "flext_quality.rules.engine",
        "FlextQualityRulesEngine",
    ],
    "FlextQualityRulesLoader": [
        "flext_quality.rules.loader",
        "FlextQualityRulesLoader",
    ],
    "FlextQualityValidators": [
        "flext_quality.rules.validators",
        "FlextQualityValidators",
    ],
    "engine": ["flext_quality.rules.engine", ""],
    "loader": ["flext_quality.rules.loader", ""],
    "validators": ["flext_quality.rules.validators", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
    "engine",
    "loader",
    "validators",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
