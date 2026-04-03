# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Helpers package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_quality.utilities import FlextQualityUtilities as u
from tests.helpers.constants import TestsConstants, TestsConstants as c
from tests.helpers.models import TestsModels, TestsModels as m
from tests.helpers.protocols import TestsProtocols, TestsProtocols as p
from tests.helpers.typing_helpers import (
    assert_analysis_results_structure,
    assert_dict_structure,
    assert_is_dict,
    assert_is_list,
    assert_issues_structure,
    assert_metrics_structure,
    safe_dict_access,
    safe_list_access,
)
from tests.helpers.typings import TestsTypings, t

if _t.TYPE_CHECKING:
    import tests.helpers.assertions as _tests_helpers_assertions

    assertions = _tests_helpers_assertions
    import tests.helpers.constants as _tests_helpers_constants

    constants = _tests_helpers_constants
    import tests.helpers.models as _tests_helpers_models

    models = _tests_helpers_models
    import tests.helpers.protocols as _tests_helpers_protocols

    protocols = _tests_helpers_protocols
    import tests.helpers.typing_helpers as _tests_helpers_typing_helpers

    typing_helpers = _tests_helpers_typing_helpers
    import tests.helpers.typings as _tests_helpers_typings

    typings = _tests_helpers_typings

    _ = (
        TestsConstants,
        TestsModels,
        TestsProtocols,
        TestsTypings,
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        assertions,
        c,
        constants,
        d,
        e,
        h,
        m,
        models,
        p,
        protocols,
        r,
        s,
        safe_dict_access,
        safe_list_access,
        t,
        typing_helpers,
        typings,
        u,
        x,
    )
_LAZY_IMPORTS = {
    "TestsConstants": "tests.helpers.constants",
    "TestsModels": "tests.helpers.models",
    "TestsProtocols": "tests.helpers.protocols",
    "TestsTypings": "tests.helpers.typings",
    "assert_analysis_results_structure": "tests.helpers.typing_helpers",
    "assert_dict_structure": "tests.helpers.typing_helpers",
    "assert_is_dict": "tests.helpers.typing_helpers",
    "assert_is_list": "tests.helpers.typing_helpers",
    "assert_issues_structure": "tests.helpers.typing_helpers",
    "assert_metrics_structure": "tests.helpers.typing_helpers",
    "assertions": "tests.helpers.assertions",
    "c": ("tests.helpers.constants", "TestsConstants"),
    "constants": "tests.helpers.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.helpers.models", "TestsModels"),
    "models": "tests.helpers.models",
    "p": ("tests.helpers.protocols", "TestsProtocols"),
    "protocols": "tests.helpers.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "safe_dict_access": "tests.helpers.typing_helpers",
    "safe_list_access": "tests.helpers.typing_helpers",
    "t": "tests.helpers.typings",
    "typing_helpers": "tests.helpers.typing_helpers",
    "typings": "tests.helpers.typings",
    "u": ("flext_quality.utilities", "FlextQualityUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsConstants",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "assertions",
    "c",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "safe_dict_access",
    "safe_list_access",
    "t",
    "typing_helpers",
    "typings",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
