"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_web import FlextWebProtocols

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


class FlextQualityProtocols(FlextWebProtocols):
    """Namespace for flext-quality protocols."""

    @runtime_checkable
    class Quality(Protocol):
        """Quality-specific protocols namespace."""

        ArgumentOptionSpec = FlextQualityProtocolsArgumentOptionSpec
        ArgumentParserSpec = FlextQualityProtocolsArgumentParserSpec
        ValidatorBase = FlextQualityProtocolsValidatorBase
        HookImpl = FlextQualityProtocolsHookImpl
        DocsConfig = FlextQualityProtocolsDocsConfig
        BaseHook = FlextQualityProtocolsBaseHook
        RuleValidator = FlextQualityProtocolsRuleValidator
        IntegrationClient = FlextQualityProtocolsIntegrationClient
        McpTool = FlextQualityProtocolsMcpTool


p = FlextQualityProtocols

__all__: list[str] = ["FlextQualityProtocols", "p"]
