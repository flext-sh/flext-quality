# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tools package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_quality.docs.tools.link_checker import (
        FlextQualityLinkChecker as FlextQualityLinkChecker,
    )
    from flext_quality.docs.tools.style_validator import (
        FlextQualityStyleValidator as FlextQualityStyleValidator,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".link_checker": ("FlextQualityLinkChecker",),
        ".style_validator": ("FlextQualityStyleValidator",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
