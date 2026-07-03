# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.tests.unit.test_api import (
        TestsFlextQualityApi as TestsFlextQualityApi,
    )
    from flext_quality.tests.unit.test_basic import (
        TestsFlextQualityBasic as TestsFlextQualityBasic,
    )
    from flext_quality.tests.unit.test_cli import (
        TestsFlextQualityCli as TestsFlextQualityCli,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestsFlextQualityApi",),
        ".test_basic": ("TestsFlextQualityBasic",),
        ".test_cli": ("TestsFlextQualityCli",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
