# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import d, e, h, r, s, td, tf, tk, tm, tv, x

    from tests.constants import TestsFlextQualityConstants, c
    from tests.helpers.constants import TestsConstants
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.typings import TestsFlextQualityTypes, t
    from tests.utilities import TestsFlextQualityUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".helpers",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextQualityConstants",
                "c",
            ),
            ".models": (
                "TestsFlextQualityModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextQualityProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextQualityTypes",
                "t",
            ),
            ".utilities": (
                "TestsFlextQualityUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestsConstants",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
