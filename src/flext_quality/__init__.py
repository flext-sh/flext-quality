# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext quality package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import *

    from flext_quality import (
        api,
        constants,
        docs,
        hooks,
        integrations,
        models,
        protocols,
        rules,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_quality.api import *
    from flext_quality.constants import *
    from flext_quality.docs import (
        core,
        dashboard,
        notifications,
        scheduled_maintenance,
        scripts,
        tools,
    )
    from flext_quality.docs.core import base_classes, config_manager, file_discovery
    from flext_quality.docs.core.base_classes import *
    from flext_quality.docs.core.config_manager import *
    from flext_quality.docs.core.file_discovery import *
    from flext_quality.docs.dashboard import *
    from flext_quality.docs.notifications import *
    from flext_quality.docs.scheduled_maintenance import *
    from flext_quality.docs.scripts import audit, optimize, report, validate
    from flext_quality.docs.scripts.audit import *
    from flext_quality.docs.scripts.optimize import *
    from flext_quality.docs.scripts.report import *
    from flext_quality.docs.scripts.validate import *
    from flext_quality.docs.tools import content_analyzer, link_checker, style_validator
    from flext_quality.docs.tools.content_analyzer import *
    from flext_quality.docs.tools.link_checker import *
    from flext_quality.docs.tools.style_validator import *
    from flext_quality.hooks import base, manager
    from flext_quality.hooks.base import *
    from flext_quality.hooks.manager import *
    from flext_quality.integrations import (
        claude_context,
        claude_mem,
        code_execution,
        mcp_client,
    )
    from flext_quality.integrations._health import *
    from flext_quality.integrations.claude_context import *
    from flext_quality.integrations.claude_mem import *
    from flext_quality.integrations.code_execution import *
    from flext_quality.integrations.mcp_client import *
    from flext_quality.mcp import resources, server
    from flext_quality.mcp.resources import *
    from flext_quality.mcp.server import *
    from flext_quality.mcp.tools import *
    from flext_quality.models import *
    from flext_quality.protocols import *
    from flext_quality.rules import engine, loader, validators
    from flext_quality.rules.engine import *
    from flext_quality.rules.loader import *
    from flext_quality.rules.validators import *
    from flext_quality.services import cli
    from flext_quality.services.cli import *
    from flext_quality.settings import *
    from flext_quality.typings import *
    from flext_quality.utilities import *

from flext_quality.docs import _LAZY_IMPORTS as _DOCS_LAZY
from flext_quality.hooks import _LAZY_IMPORTS as _HOOKS_LAZY
from flext_quality.integrations import _LAZY_IMPORTS as _INTEGRATIONS_LAZY
from flext_quality.mcp import _LAZY_IMPORTS as _MCP_LAZY
from flext_quality.rules import _LAZY_IMPORTS as _RULES_LAZY
from flext_quality.services import _LAZY_IMPORTS as _SERVICES_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_DOCS_LAZY,
    **_HOOKS_LAZY,
    **_INTEGRATIONS_LAZY,
    **_MCP_LAZY,
    **_RULES_LAZY,
    **_SERVICES_LAZY,
    "FlextQuality": "flext_quality.api",
    "FlextQualityConstants": "flext_quality.constants",
    "FlextQualityModels": "flext_quality.models",
    "FlextQualityProtocols": "flext_quality.protocols",
    "FlextQualitySettings": "flext_quality.settings",
    "FlextQualityTypes": "flext_quality.typings",
    "FlextQualityUtilities": "flext_quality.utilities",
    "api": "flext_quality.api",
    "c": ["flext_quality.constants", "FlextQualityConstants"],
    "constants": "flext_quality.constants",
    "d": "flext_cli",
    "docs": "flext_quality.docs",
    "e": "flext_cli",
    "h": "flext_cli",
    "hooks": "flext_quality.hooks",
    "integrations": "flext_quality.integrations",
    "m": ["flext_quality.models", "FlextQualityModels"],
    "models": "flext_quality.models",
    "p": ["flext_quality.protocols", "FlextQualityProtocols"],
    "protocols": "flext_quality.protocols",
    "r": "flext_cli",
    "rules": "flext_quality.rules",
    "s": "flext_cli",
    "services": "flext_quality.services",
    "settings": "flext_quality.settings",
    "t": ["flext_quality.typings", "FlextQualityTypes"],
    "typings": "flext_quality.typings",
    "u": ["flext_quality.utilities", "FlextQualityUtilities"],
    "utilities": "flext_quality.utilities",
    "x": "flext_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
