# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality import d as d, e as e, h as h, r as r, s as s, x as x
    from tests import (
        conftest as conftest,
        constants as constants,
        helpers as helpers,
        models as models,
        protocols as protocols,
        typings as typings,
        unit as unit,
        utilities as utilities,
    )
    from tests.conftest import (
        MockQualityAnalyzer as MockQualityAnalyzer,
        MockReportGenerator as MockReportGenerator,
        analysis_results as analysis_results,
        analysis_task_data as analysis_task_data,
        assert_result_failure_with_error as assert_result_failure_with_error,
        assert_result_success_with_data as assert_result_success_with_data,
        celery_config as celery_config,
        code_analysis_config as code_analysis_config,
        codeclimate_config as codeclimate_config,
        dashboard_data as dashboard_data,
        mock_quality_analyzer as mock_quality_analyzer,
        mock_report_generator as mock_report_generator,
        package_metadata as package_metadata,
        pytest_configure as pytest_configure,
        quality_metrics_data as quality_metrics_data,
        report_config as report_config,
        sample_code_repository as sample_code_repository,
        secure_temp_dir as secure_temp_dir,
        set_test_environment as set_test_environment,
        sonarqube_config as sonarqube_config,
        temporary_project_structure as temporary_project_structure,
    )
    from tests.constants import (
        FlextQualityTestConstants as FlextQualityTestConstants,
        FlextQualityTestConstants as c,
    )
    from tests.helpers import assertions as assertions, typing_helpers as typing_helpers
    from tests.helpers.constants import TestsConstants as TestsConstants
    from tests.helpers.models import TestsModels as TestsModels
    from tests.helpers.protocols import TestsProtocols as TestsProtocols
    from tests.helpers.typing_helpers import (
        assert_analysis_results_structure as assert_analysis_results_structure,
        assert_dict_structure as assert_dict_structure,
        assert_is_dict as assert_is_dict,
        assert_is_list as assert_is_list,
        assert_issues_structure as assert_issues_structure,
        assert_metrics_structure as assert_metrics_structure,
        safe_dict_access as safe_dict_access,
        safe_list_access as safe_list_access,
    )
    from tests.helpers.typings import TestsTypings as TestsTypings
    from tests.models import (
        FlextQualityTestModels as FlextQualityTestModels,
        FlextQualityTestModels as m,
    )
    from tests.protocols import (
        FlextQualityTestProtocols as FlextQualityTestProtocols,
        FlextQualityTestProtocols as p,
    )
    from tests.typings import (
        FlextQualityTestTypes as FlextQualityTestTypes,
        FlextQualityTestTypes as t,
    )
    from tests.unit import test_api as test_api, test_cli as test_cli
    from tests.unit.test_api import (
        TestFlextQualityAPI as TestFlextQualityAPI,
        TestFlextQualityHookExecution as TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig as TestFlextQualityRulesConfig,
        TestFlextQualitySingleton as TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing as TestFlextQualityStdinProcessing,
        TestFlextQualityValidation as TestFlextQualityValidation,
    )
    from tests.unit.test_basic import test_basic as test_basic
    from tests.unit.test_cli import (
        TestFlextQualityCliService as TestFlextQualityCliService,
        TestMainFunction as TestMainFunction,
    )
    from tests.utilities import (
        FlextQualityTestUtilities as FlextQualityTestUtilities,
        FlextQualityTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextQualityTestConstants": ["tests.constants", "FlextQualityTestConstants"],
    "FlextQualityTestModels": ["tests.models", "FlextQualityTestModels"],
    "FlextQualityTestProtocols": ["tests.protocols", "FlextQualityTestProtocols"],
    "FlextQualityTestTypes": ["tests.typings", "FlextQualityTestTypes"],
    "FlextQualityTestUtilities": ["tests.utilities", "FlextQualityTestUtilities"],
    "MockQualityAnalyzer": ["tests.conftest", "MockQualityAnalyzer"],
    "MockReportGenerator": ["tests.conftest", "MockReportGenerator"],
    "TestFlextQualityAPI": ["tests.unit.test_api", "TestFlextQualityAPI"],
    "TestFlextQualityCliService": ["tests.unit.test_cli", "TestFlextQualityCliService"],
    "TestFlextQualityHookExecution": [
        "tests.unit.test_api",
        "TestFlextQualityHookExecution",
    ],
    "TestFlextQualityRulesConfig": [
        "tests.unit.test_api",
        "TestFlextQualityRulesConfig",
    ],
    "TestFlextQualitySingleton": ["tests.unit.test_api", "TestFlextQualitySingleton"],
    "TestFlextQualityStdinProcessing": [
        "tests.unit.test_api",
        "TestFlextQualityStdinProcessing",
    ],
    "TestFlextQualityValidation": ["tests.unit.test_api", "TestFlextQualityValidation"],
    "TestMainFunction": ["tests.unit.test_cli", "TestMainFunction"],
    "TestsConstants": ["tests.helpers.constants", "TestsConstants"],
    "TestsModels": ["tests.helpers.models", "TestsModels"],
    "TestsProtocols": ["tests.helpers.protocols", "TestsProtocols"],
    "TestsTypings": ["tests.helpers.typings", "TestsTypings"],
    "analysis_results": ["tests.conftest", "analysis_results"],
    "analysis_task_data": ["tests.conftest", "analysis_task_data"],
    "assert_analysis_results_structure": [
        "tests.helpers.typing_helpers",
        "assert_analysis_results_structure",
    ],
    "assert_dict_structure": ["tests.helpers.typing_helpers", "assert_dict_structure"],
    "assert_is_dict": ["tests.helpers.typing_helpers", "assert_is_dict"],
    "assert_is_list": ["tests.helpers.typing_helpers", "assert_is_list"],
    "assert_issues_structure": [
        "tests.helpers.typing_helpers",
        "assert_issues_structure",
    ],
    "assert_metrics_structure": [
        "tests.helpers.typing_helpers",
        "assert_metrics_structure",
    ],
    "assert_result_failure_with_error": [
        "tests.conftest",
        "assert_result_failure_with_error",
    ],
    "assert_result_success_with_data": [
        "tests.conftest",
        "assert_result_success_with_data",
    ],
    "assertions": ["tests.helpers.assertions", ""],
    "c": ["tests.constants", "FlextQualityTestConstants"],
    "celery_config": ["tests.conftest", "celery_config"],
    "code_analysis_config": ["tests.conftest", "code_analysis_config"],
    "codeclimate_config": ["tests.conftest", "codeclimate_config"],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_quality", "d"],
    "dashboard_data": ["tests.conftest", "dashboard_data"],
    "e": ["flext_quality", "e"],
    "h": ["flext_quality", "h"],
    "helpers": ["tests.helpers", ""],
    "m": ["tests.models", "FlextQualityTestModels"],
    "mock_quality_analyzer": ["tests.conftest", "mock_quality_analyzer"],
    "mock_report_generator": ["tests.conftest", "mock_report_generator"],
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextQualityTestProtocols"],
    "package_metadata": ["tests.conftest", "package_metadata"],
    "protocols": ["tests.protocols", ""],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "quality_metrics_data": ["tests.conftest", "quality_metrics_data"],
    "r": ["flext_quality", "r"],
    "report_config": ["tests.conftest", "report_config"],
    "s": ["flext_quality", "s"],
    "safe_dict_access": ["tests.helpers.typing_helpers", "safe_dict_access"],
    "safe_list_access": ["tests.helpers.typing_helpers", "safe_list_access"],
    "sample_code_repository": ["tests.conftest", "sample_code_repository"],
    "secure_temp_dir": ["tests.conftest", "secure_temp_dir"],
    "set_test_environment": ["tests.conftest", "set_test_environment"],
    "sonarqube_config": ["tests.conftest", "sonarqube_config"],
    "t": ["tests.typings", "FlextQualityTestTypes"],
    "temporary_project_structure": ["tests.conftest", "temporary_project_structure"],
    "test_api": ["tests.unit.test_api", ""],
    "test_basic": ["tests.unit.test_basic", "test_basic"],
    "test_cli": ["tests.unit.test_cli", ""],
    "typing_helpers": ["tests.helpers.typing_helpers", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextQualityTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_quality", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextQualityTestConstants",
    "FlextQualityTestModels",
    "FlextQualityTestProtocols",
    "FlextQualityTestTypes",
    "FlextQualityTestUtilities",
    "MockQualityAnalyzer",
    "MockReportGenerator",
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "TestsConstants",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "analysis_results",
    "analysis_task_data",
    "assert_analysis_results_structure",
    "assert_dict_structure",
    "assert_is_dict",
    "assert_is_list",
    "assert_issues_structure",
    "assert_metrics_structure",
    "assert_result_failure_with_error",
    "assert_result_success_with_data",
    "assertions",
    "c",
    "celery_config",
    "code_analysis_config",
    "codeclimate_config",
    "conftest",
    "constants",
    "d",
    "dashboard_data",
    "e",
    "h",
    "helpers",
    "m",
    "mock_quality_analyzer",
    "mock_report_generator",
    "models",
    "p",
    "package_metadata",
    "protocols",
    "pytest_configure",
    "quality_metrics_data",
    "r",
    "report_config",
    "s",
    "safe_dict_access",
    "safe_list_access",
    "sample_code_repository",
    "secure_temp_dir",
    "set_test_environment",
    "sonarqube_config",
    "t",
    "temporary_project_structure",
    "test_api",
    "test_basic",
    "test_cli",
    "typing_helpers",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
