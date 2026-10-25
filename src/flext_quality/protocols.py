# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols for flext-quality.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeAlias

from flext_web import FlextWebProtocols

from flext_quality._protocols import FlextQualityProtocolsQuality


class FlextQualityProtocols(FlextWebProtocols):
    """Namespace for flext-quality protocols."""

    class Quality:
        """Quality-specific protocols namespace."""

        ArgumentOptionSpec: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsArgumentOptionSpec
        )
        ArgumentParserSpec: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsArgumentParserSpec
        )
        ValidatorBase: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsValidatorBase
        )
        HookImpl: TypeAlias = FlextQualityProtocolsQuality.FlextQualityProtocolsHookImpl
        DocsConfig: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsDocsConfig
        )
        BaseHook: TypeAlias = FlextQualityProtocolsQuality.FlextQualityProtocolsBaseHook
        RuleValidator: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsRuleValidator
        )
        IntegrationClient: TypeAlias = (
            FlextQualityProtocolsQuality.FlextQualityProtocolsIntegrationClient
        )
        McpTool: TypeAlias = FlextQualityProtocolsQuality.FlextQualityProtocolsMcpTool


p = FlextQualityProtocols
__all__: list[str] = ["FlextQualityProtocols", "p"]
