# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
    from flext_quality.api import *
    from flext_quality.constants import *
    from flext_quality.docs import *
    from flext_quality.docs.core import *
    from flext_quality.docs.scripts import *
    from flext_quality.docs.tools import *
    from flext_quality.hooks import *
    from flext_quality.integrations import *
    from flext_quality.mcp import *
    from flext_quality.models import *
    from flext_quality.protocols import *
    from flext_quality.rules import *
    from flext_quality.services import *
    from flext_quality.settings import *
    from flext_quality.typings import *
    from flext_quality.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_quality.docs",
        "flext_quality.hooks",
        "flext_quality.integrations",
        "flext_quality.mcp",
        "flext_quality.rules",
        "flext_quality.services",
    ),
    {
        "FlextQuality": "flext_quality.api",
        "FlextQualityConstants": "flext_quality.constants",
        "FlextQualityModels": "flext_quality.models",
        "FlextQualityProtocols": "flext_quality.protocols",
        "FlextQualitySettings": "flext_quality.settings",
        "FlextQualityTypes": "flext_quality.typings",
        "FlextQualityUtilities": "flext_quality.utilities",
        "api": "flext_quality.api",
        "c": ("flext_quality.constants", "FlextQualityConstants"),
        "constants": "flext_quality.constants",
        "d": "flext_cli",
        "docs": "flext_quality.docs",
        "e": "flext_cli",
        "h": "flext_cli",
        "hooks": "flext_quality.hooks",
        "integrations": "flext_quality.integrations",
        "m": ("flext_quality.models", "FlextQualityModels"),
        "models": "flext_quality.models",
        "p": ("flext_quality.protocols", "FlextQualityProtocols"),
        "protocols": "flext_quality.protocols",
        "r": "flext_cli",
        "rules": "flext_quality.rules",
        "s": "flext_cli",
        "services": "flext_quality.services",
        "settings": "flext_quality.settings",
        "t": ("flext_quality.typings", "FlextQualityTypes"),
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityUtilities"),
        "utilities": "flext_quality.utilities",
        "x": "flext_cli",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
