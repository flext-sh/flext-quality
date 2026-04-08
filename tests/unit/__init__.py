# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "test_api": "tests.unit.test_api",
    "test_basic": "tests.unit.test_basic",
    "test_cli": "tests.unit.test_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
