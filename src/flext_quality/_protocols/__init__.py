# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Quality. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality._protocols.quality import (
        FlextQualityProtocolsArgumentOptionSpec,
        FlextQualityProtocolsArgumentParserSpec,
        FlextQualityProtocolsBaseHook,
        FlextQualityProtocolsDocsConfig,
        FlextQualityProtocolsHookImpl,
        FlextQualityProtocolsIntegrationClient,
        FlextQualityProtocolsMcpTool,
        FlextQualityProtocolsRuleValidator,
        FlextQualityProtocolsValidatorBase,
    )


__all__: tuple[str, ...] = (
    "FlextQualityProtocolsArgumentOptionSpec",
    "FlextQualityProtocolsArgumentParserSpec",
    "FlextQualityProtocolsBaseHook",
    "FlextQualityProtocolsDocsConfig",
    "FlextQualityProtocolsHookImpl",
    "FlextQualityProtocolsIntegrationClient",
    "FlextQualityProtocolsMcpTool",
    "FlextQualityProtocolsRuleValidator",
    "FlextQualityProtocolsValidatorBase",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextQualityProtocolsArgumentOptionSpec": ".quality",
        "FlextQualityProtocolsArgumentParserSpec": ".quality",
        "FlextQualityProtocolsBaseHook": ".quality",
        "FlextQualityProtocolsDocsConfig": ".quality",
        "FlextQualityProtocolsHookImpl": ".quality",
        "FlextQualityProtocolsIntegrationClient": ".quality",
        "FlextQualityProtocolsMcpTool": ".quality",
        "FlextQualityProtocolsRuleValidator": ".quality",
        "FlextQualityProtocolsValidatorBase": ".quality",
    }),
    public_exports=__all__,
)
