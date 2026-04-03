# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Helpers package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality import (
        assertions,
        constants,
        models,
        protocols,
        typing_helpers,
        typings,
    )
    from flext_quality.assertions import missing, safe_list_access
    from flext_quality.constants import TestsConstants, TestsConstants as c
    from flext_quality.models import TestsModels, TestsModels as m
    from flext_quality.protocols import TestsProtocols, TestsProtocols as p
    from flext_quality.typing_helpers import (
        assert_analysis_results_structure,
        assert_is_dict,
        assert_is_list,
        assert_metrics_structure,
    )
    from flext_quality.typings import TestsTypings, t
    from flext_quality.utilities import FlextQualityUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestsConstants": "flext_quality.constants",
    "TestsModels": "flext_quality.models",
    "TestsProtocols": "flext_quality.protocols",
    "TestsTypings": "flext_quality.typings",
    "assert_analysis_results_structure": "flext_quality.typing_helpers",
    "assert_is_dict": "flext_quality.typing_helpers",
    "assert_is_list": "flext_quality.typing_helpers",
    "assert_metrics_structure": "flext_quality.typing_helpers",
    "assertions": "flext_quality.assertions",
    "c": ("flext_quality.constants", "TestsConstants"),
    "constants": "flext_quality.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_quality.models", "TestsModels"),
    "missing": "flext_quality.assertions",
    "models": "flext_quality.models",
    "p": ("flext_quality.protocols", "TestsProtocols"),
    "protocols": "flext_quality.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "safe_list_access": "flext_quality.assertions",
    "t": "flext_quality.typings",
    "typing_helpers": "flext_quality.typing_helpers",
    "typings": "flext_quality.typings",
    "u": ("flext_quality.utilities", "FlextQualityUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
