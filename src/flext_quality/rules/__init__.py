# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Rules package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_quality.rules.engine as _flext_quality_rules_engine

    engine = _flext_quality_rules_engine
    import flext_quality.rules.loader as _flext_quality_rules_loader
    from flext_quality.rules.engine import FlextQualityRulesEngine

    loader = _flext_quality_rules_loader
    import flext_quality.rules.validators as _flext_quality_rules_validators
    from flext_quality.rules.loader import FlextQualityRulesLoader

    validators = _flext_quality_rules_validators
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_quality.rules.validators import FlextQualityValidators
_LAZY_IMPORTS = {
    "FlextQualityRulesEngine": "flext_quality.rules.engine",
    "FlextQualityRulesLoader": "flext_quality.rules.loader",
    "FlextQualityValidators": "flext_quality.rules.validators",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "engine": "flext_quality.rules.engine",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "loader": "flext_quality.rules.loader",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validators": "flext_quality.rules.validators",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextQualityRulesEngine",
    "FlextQualityRulesLoader",
    "FlextQualityValidators",
    "c",
    "d",
    "e",
    "engine",
    "h",
    "loader",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "validators",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
