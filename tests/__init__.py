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

    from flext_quality import d, e, h, r, s, x
    from tests import (
        conftest,
        constants,
        helpers,
        models,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.conftest import (
        MockQualityAnalyzer,
        MockReportGenerator,
        analysis_results,
        analysis_task_data,
        assert_result_failure_with_error,
        assert_result_success_with_data,
        celery_config,
        code_analysis_config,
        codeclimate_config,
        dashboard_data,
        mock_quality_analyzer,
        mock_report_generator,
        package_metadata,
        pytest_configure,
        quality_metrics_data,
        report_config,
        sample_code_repository,
        secure_temp_dir,
        set_test_environment,
        sonarqube_config,
        temporary_project_structure,
    )
    from tests.constants import (
        FlextQualityTestConstants,
        FlextQualityTestConstants as c,
    )
    from tests.helpers import (
        TestsConstants,
        TestsModels,
        TestsProtocols,
        TestsTypings,
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        assertions,
        safe_dict_access,
        safe_list_access,
        typing_helpers,
    )
    from tests.models import FlextQualityTestModels, FlextQualityTestModels as m
    from tests.protocols import (
        FlextQualityTestProtocols,
        FlextQualityTestProtocols as p,
    )
    from tests.typings import FlextQualityTestTypes, FlextQualityTestTypes as t
    from tests.unit import (
        TestFlextQualityAPI,
        TestFlextQualityCliService,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
        TestMainFunction,
        test_api,
        test_basic,
        test_cli,
    )
    from tests.utilities import (
        FlextQualityTestUtilities,
        FlextQualityTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "tests.helpers",
        "tests.unit",
    ),
    {
        "FlextQualityTestConstants": "tests.constants",
        "FlextQualityTestModels": "tests.models",
        "FlextQualityTestProtocols": "tests.protocols",
        "FlextQualityTestTypes": "tests.typings",
        "FlextQualityTestUtilities": "tests.utilities",
        "MockQualityAnalyzer": "tests.conftest",
        "MockReportGenerator": "tests.conftest",
        "analysis_results": "tests.conftest",
        "analysis_task_data": "tests.conftest",
        "assert_result_failure_with_error": "tests.conftest",
        "assert_result_success_with_data": "tests.conftest",
        "c": ("tests.constants", "FlextQualityTestConstants"),
        "celery_config": "tests.conftest",
        "code_analysis_config": "tests.conftest",
        "codeclimate_config": "tests.conftest",
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": "flext_quality",
        "dashboard_data": "tests.conftest",
        "e": "flext_quality",
        "h": "flext_quality",
        "helpers": "tests.helpers",
        "m": ("tests.models", "FlextQualityTestModels"),
        "mock_quality_analyzer": "tests.conftest",
        "mock_report_generator": "tests.conftest",
        "models": "tests.models",
        "p": ("tests.protocols", "FlextQualityTestProtocols"),
        "package_metadata": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "quality_metrics_data": "tests.conftest",
        "r": "flext_quality",
        "report_config": "tests.conftest",
        "s": "flext_quality",
        "sample_code_repository": "tests.conftest",
        "secure_temp_dir": "tests.conftest",
        "set_test_environment": "tests.conftest",
        "sonarqube_config": "tests.conftest",
        "t": ("tests.typings", "FlextQualityTestTypes"),
        "temporary_project_structure": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextQualityTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_quality",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
