# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_quality import (
        assertions,
        conftest,
        constants,
        helpers,
        models,
        protocols,
        test_api,
        test_cli,
        typing_helpers,
        typings,
        unit,
        utilities,
    )
    from flext_quality.conftest import (
        analysis_results,
        analysis_task_data,
        assert_result_success_with_data,
        celery_config,
        code_analysis_config,
        codeclimate_config,
        dashboard_data,
        mock_quality_analyzer,
        mock_report_generator,
        package_metadata,
        quality_metrics_data,
        report_config,
        sample_code_repository,
        secure_temp_dir,
        set_test_environment,
        sonarqube_config,
        temporary_project_structure,
    )
    from flext_quality.constants import (
        FlextQualityTestConstants,
        FlextQualityTestConstants as c,
    )
    from flext_quality.helpers import (
        TestsConstants,
        TestsModels,
        TestsProtocols,
        TestsTypings,
        assert_analysis_results_structure,
        assert_is_dict,
        assert_is_list,
        assert_metrics_structure,
        missing,
        safe_list_access,
    )
    from flext_quality.models import FlextQualityTestModels, FlextQualityTestModels as m
    from flext_quality.protocols import (
        FlextQualityTestProtocols,
        FlextQualityTestProtocols as p,
    )
    from flext_quality.typings import FlextQualityTestTypes, FlextQualityTestTypes as t
    from flext_quality.unit import (
        TestFlextQualityAPI,
        TestFlextQualityCliService,
        test_basic,
    )
    from flext_quality.utilities import (
        FlextQualityTestUtilities,
        FlextQualityTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_quality.helpers",
        "flext_quality.unit",
    ),
    {
        "FlextQualityTestConstants": "flext_quality.constants",
        "FlextQualityTestModels": "flext_quality.models",
        "FlextQualityTestProtocols": "flext_quality.protocols",
        "FlextQualityTestTypes": "flext_quality.typings",
        "FlextQualityTestUtilities": "flext_quality.utilities",
        "analysis_results": "flext_quality.conftest",
        "analysis_task_data": "flext_quality.conftest",
        "assert_result_success_with_data": "flext_quality.conftest",
        "assertions": "flext_quality.assertions",
        "c": ("flext_quality.constants", "FlextQualityTestConstants"),
        "celery_config": "flext_quality.conftest",
        "code_analysis_config": "flext_quality.conftest",
        "codeclimate_config": "flext_quality.conftest",
        "conftest": "flext_quality.conftest",
        "constants": "flext_quality.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dashboard_data": "flext_quality.conftest",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "flext_quality.helpers",
        "m": ("flext_quality.models", "FlextQualityTestModels"),
        "mock_quality_analyzer": "flext_quality.conftest",
        "mock_report_generator": "flext_quality.conftest",
        "models": "flext_quality.models",
        "p": ("flext_quality.protocols", "FlextQualityTestProtocols"),
        "package_metadata": "flext_quality.conftest",
        "protocols": "flext_quality.protocols",
        "quality_metrics_data": "flext_quality.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "report_config": "flext_quality.conftest",
        "s": ("flext_core.service", "FlextService"),
        "sample_code_repository": "flext_quality.conftest",
        "secure_temp_dir": "flext_quality.conftest",
        "set_test_environment": "flext_quality.conftest",
        "sonarqube_config": "flext_quality.conftest",
        "t": ("flext_quality.typings", "FlextQualityTestTypes"),
        "temporary_project_structure": "flext_quality.conftest",
        "test_api": "flext_quality.test_api",
        "test_cli": "flext_quality.test_cli",
        "typing_helpers": "flext_quality.typing_helpers",
        "typings": "flext_quality.typings",
        "u": ("flext_quality.utilities", "FlextQualityTestUtilities"),
        "unit": "flext_quality.unit",
        "utilities": "flext_quality.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
