# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_infra import docs_main, infra
    from flext_tests import (
        active_rules,
        api,
        config,
        discover_repository_root,
        install_local_packages,
        load_infra_report,
        settings,
        split_csv,
        td,
        tf,
        tk,
        tm,
        tv,
    )
    from flext_web import web

    from flext_core import core, d, e, h, lazy_attribute, r, x
    from flext_quality import main, quality

    from . import helpers, unit
    from .base import TestsFlextQualityServiceBase, TestsFlextQualityServiceBase as s
    from .constants import TestsFlextQualityConstants, TestsFlextQualityConstants as c
    from .models import TestsFlextQualityModels, TestsFlextQualityModels as m
    from .protocols import TestsFlextQualityProtocols, TestsFlextQualityProtocols as p
    from .settings import TestsFlextQualitySettings
    from .typings import TestsFlextQualityTypes, TestsFlextQualityTypes as t
    from .utilities import TestsFlextQualityUtilities, TestsFlextQualityUtilities as u


__all__: tuple[str, ...] = (
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "active_rules",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "discover_repository_root",
    "docs_main",
    "e",
    "h",
    "helpers",
    "infra",
    "install_local_packages",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "quality",
    "r",
    "s",
    "settings",
    "split_csv",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "unit",
    "web",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextQualityServiceBase", "s"),
            ".constants": ("TestsFlextQualityConstants", "c"),
            ".helpers": ("helpers",),
            ".models": ("TestsFlextQualityModels", "m"),
            ".protocols": ("TestsFlextQualityProtocols", "p"),
            ".settings": ("TestsFlextQualitySettings",),
            ".typings": ("TestsFlextQualityTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextQualityUtilities", "u"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "flext_infra": ("docs_main", "infra"),
            "flext_quality": ("main", "quality"),
            "flext_tests": (
                "active_rules",
                "api",
                "config",
                "discover_repository_root",
                "install_local_packages",
                "load_infra_report",
                "settings",
                "split_csv",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
            "flext_web": ("web",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
