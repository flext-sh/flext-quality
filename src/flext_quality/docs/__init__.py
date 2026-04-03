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
    from flext_quality import (
        audit,
        base_classes,
        config_manager,
        content_analyzer,
        core,
        dashboard,
        file_discovery,
        link_checker,
        notifications,
        optimize,
        report,
        scheduled_maintenance,
        scripts,
        style_validator,
        tools,
        validate,
    )
    from flext_quality.core import (
        FlextQualityAuditRules,
        FlextQualityBaseAuditor,
        FlextQualityFileStatistics,
    )
    from flext_quality.dashboard import (
        FlextQualityDocumentationDashboard,
        issuesChart,
        qualityChart,
        run,
    )
    from flext_quality.notifications import (
        MAX_BROKEN_LINKS_TO_SHOW,
        FlextQualityDocumentationNotifier,
        desc_v,
        err_v,
        file_v,
        notify_broken_links,
        server,
        type_v,
        url_v,
    )
    from flext_quality.scheduled_maintenance import (
        FlextQualityScheduledMaintenance,
        logger,
    )
    from flext_quality.scripts import (
        MIN_HEADINGS_FOR_TOC,
        FlextQualityDocumentationAuditor,
        FlextQualityDocumentationOptimizer,
        FlextQualityDocumentationReporter,
        FlextQualityLinkValidator,
        critical,
        critical_high_issues,
        doc_files,
        high,
        project_root,
        quality_score,
        run_any_check,
        run_any_optimization,
        severity_breakdown,
        should_fail,
    )
    from flext_quality.tools import (
        MIN_ARGS,
        FlextQualityContentAnalyzer,
        FlextQualityLinkChecker,
        FlextQualityStyleValidator,
        analyze_files_content,
        analyzer,
        checker,
        config_path,
        context,
        error_msg,
        file,
        file_path,
        issue_types,
        issues,
        key,
        main,
        paths,
        recommendations,
        results,
        reverse,
        save_report,
        sorted_issues,
        status,
        suggestions,
        test_links,
        text,
        type,
        url,
        v_type,
        validate_files_style,
        validator,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_quality.core",
        "flext_quality.scripts",
        "flext_quality.tools",
    ),
    {
        "FlextQualityDocumentationDashboard": "flext_quality.dashboard",
        "FlextQualityDocumentationNotifier": "flext_quality.notifications",
        "FlextQualityScheduledMaintenance": "flext_quality.scheduled_maintenance",
        "MAX_BROKEN_LINKS_TO_SHOW": "flext_quality.notifications",
        "audit": "flext_quality.audit",
        "base_classes": "flext_quality.base_classes",
        "c": ("flext_core.constants", "FlextConstants"),
        "config_manager": "flext_quality.config_manager",
        "content_analyzer": "flext_quality.content_analyzer",
        "core": "flext_quality.core",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard": "flext_quality.dashboard",
        "desc_v": "flext_quality.notifications",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "err_v": "flext_quality.notifications",
        "file_discovery": "flext_quality.file_discovery",
        "file_v": "flext_quality.notifications",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "issuesChart": "flext_quality.dashboard",
        "link_checker": "flext_quality.link_checker",
        "logger": "flext_quality.scheduled_maintenance",
        "m": ("flext_core.models", "FlextModels"),
        "notifications": "flext_quality.notifications",
        "notify_broken_links": "flext_quality.notifications",
        "optimize": "flext_quality.optimize",
        "p": ("flext_core.protocols", "FlextProtocols"),
        "qualityChart": "flext_quality.dashboard",
        "r": ("flext_core.result", "FlextResult"),
        "report": "flext_quality.report",
        "run": "flext_quality.dashboard",
        "s": ("flext_core.service", "FlextService"),
        "scheduled_maintenance": "flext_quality.scheduled_maintenance",
        "scripts": "flext_quality.scripts",
        "server": "flext_quality.notifications",
        "style_validator": "flext_quality.style_validator",
        "t": ("flext_core.typings", "FlextTypes"),
        "tools": "flext_quality.tools",
        "type_v": "flext_quality.notifications",
        "u": ("flext_core.utilities", "FlextUtilities"),
        "url_v": "flext_quality.notifications",
        "validate": "flext_quality.validate",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
