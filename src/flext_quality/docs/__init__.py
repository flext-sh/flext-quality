# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Docs package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_quality.docs import (
        core,
        dashboard,
        notifications,
        scheduled_maintenance,
        scripts,
        tools,
    )
    from flext_quality.docs.core import (
        FlextQualityAuditRules,
        FlextQualityBaseAnalyzer,
        FlextQualityBaseAuditor,
        FlextQualityBaseReporter,
        FlextQualityBaseValidator,
        FlextQualityConfigManager,
        FlextQualityDocumentationFinder,
        FlextQualityFileStatistics,
        FlextQualityStyleGuide,
        FlextQualityValidationConfig,
        base_classes,
        config_manager,
        file_discovery,
    )
    from flext_quality.docs.dashboard import FlextQualityDocumentationDashboard
    from flext_quality.docs.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier,
    )
    from flext_quality.docs.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
        logger,
    )
    from flext_quality.docs.scripts import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityContentValidator,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
        audit,
        main,
        optimize,
        report,
        validate,
    )
    from flext_quality.docs.tools import (
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_file_content,
        analyze_files_content,
        content_analyzer,
        link_checker,
        style_validator,
        validate_file_style,
        validate_files_style,
        validate_links_sync,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_quality.docs.core",
        "flext_quality.docs.scripts",
        "flext_quality.docs.tools",
    ),
    {
        "FlextQualityDocumentationDashboard": "flext_quality.docs.dashboard",
        "FlextQualityDocumentationNotifier": "flext_quality.docs.notifications",
        "FlextQualityScheduledMaintenance": "flext_quality.docs.scheduled_maintenance",
        "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.docs.notifications",
        "c": ("flext_core.constants", "FlextConstants"),
        "core": "flext_quality.docs.core",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard": "flext_quality.docs.dashboard",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "logger": "flext_quality.docs.scheduled_maintenance",
        "m": ("flext_core.models", "FlextModels"),
        "notifications": "flext_quality.docs.notifications",
        "p": ("flext_core.protocols", "FlextProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "scheduled_maintenance": "flext_quality.docs.scheduled_maintenance",
        "scripts": "flext_quality.docs.scripts",
        "t": ("flext_core.typings", "FlextTypes"),
        "tools": "flext_quality.docs.tools",
        "u": ("flext_core.utilities", "FlextUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
