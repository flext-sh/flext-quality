"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_web import FlextWebProtocols

from flext_quality._protocols.quality import FlextQualityProtocolsQuality


class FlextQualityProtocols(FlextWebProtocols):
    """Namespace for flext-quality protocols."""

    @runtime_checkable
    class Quality(Protocol):
        """Quality-specific protocols namespace."""

        ArgumentOptionSpec = FlextQualityProtocolsQuality.FlextQualityProtocolsArgumentOptionSpec
        ArgumentParserSpec = FlextQualityProtocolsQuality.FlextQualityProtocolsArgumentParserSpec
        ValidatorBase = FlextQualityProtocolsQuality.FlextQualityProtocolsValidatorBase
        HookImpl = FlextQualityProtocolsQuality.FlextQualityProtocolsHookImpl
        DocsConfig = FlextQualityProtocolsQuality.FlextQualityProtocolsDocsConfig
        BaseHook = FlextQualityProtocolsQuality.FlextQualityProtocolsBaseHook
        RuleValidator = FlextQualityProtocolsQuality.FlextQualityProtocolsRuleValidator
        IntegrationClient = FlextQualityProtocolsQuality.FlextQualityProtocolsIntegrationClient
        McpTool = FlextQualityProtocolsQuality.FlextQualityProtocolsMcpTool


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
