# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        api,
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        install_local_packages,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )

    from flext_quality import quality, web
    from tests.base import TestsFlextQualityServiceBase, s
    from tests.constants import TestsFlextQualityConstants, c
    from tests.models import TestsFlextQualityModels, m
    from tests.protocols import TestsFlextQualityProtocols, p
    from tests.settings import TestsFlextQualitySettings
    from tests.typings import TestsFlextQualityTypes, t
    from tests.utilities import TestsFlextQualityUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityServiceBase",
    "TestsFlextQualitySettings",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
    "api",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "quality",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "web",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextQualityConstants": ".constants",
        "TestsFlextQualityModels": ".models",
        "TestsFlextQualityProtocols": ".protocols",
        "TestsFlextQualityServiceBase": ".base",
        "TestsFlextQualitySettings": ".settings",
        "TestsFlextQualityTypes": ".typings",
        "TestsFlextQualityUtilities": ".utilities",
        "api": "flext_tests",
        "build_lazy_import_map": "flext_tests",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_tests",
        "cli": "flext_tests",
        "config": "flext_tests",
        "core": "flext_tests",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "install_lazy_exports": "flext_tests",
        "install_local_packages": "flext_tests",
        "lazy": "flext_tests",
        "lazy_getattr": "flext_tests",
        "lazy_member": "flext_tests",
        "m": ".models",
        "main": "flext_tests",
        "merge_lazy_imports": "flext_tests",
        "normalize_lazy_imports": "flext_tests",
        "p": ".protocols",
        "quality": "flext_quality",
        "r": "flext_tests",
        "resolve_lazy_members": "flext_tests",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "web": "flext_quality",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
