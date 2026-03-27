# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_quality import d, e, h, r, s, x
    from tests import helpers, unit
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
    from tests.helpers.constants import TestsConstants
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typing_helpers import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        safe_dict_access,
        safe_list_access,
    )
    from tests.helpers.typings import TestsTypings
    from tests.models import FlextQualityTestModels, FlextQualityTestModels as m
    from tests.protocols import (
        FlextQualityTestProtocols,
        FlextQualityTestProtocols as p,
    )
    from tests.typings import FlextQualityTestTypes, FlextQualityTestTypes as t
    from tests.unit.test_api import (
        TestFlextQualityAPI,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
    )
    from tests.unit.test_basic import test_basic
    from tests.unit.test_cli import TestFlextQualityCliService, TestMainFunction
    from tests.utilities import (
        FlextQualityTestUtilities,
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
    "TestFlextQualityHookExecution": ["tests.unit.test_api", "TestFlextQualityHookExecution"],
    "TestFlextQualityRulesConfig": ["tests.unit.test_api", "TestFlextQualityRulesConfig"],
    "TestFlextQualitySingleton": ["tests.unit.test_api", "TestFlextQualitySingleton"],
    "TestFlextQualityStdinProcessing": ["tests.unit.test_api", "TestFlextQualityStdinProcessing"],
    "TestFlextQualityValidation": ["tests.unit.test_api", "TestFlextQualityValidation"],
    "TestMainFunction": ["tests.unit.test_cli", "TestMainFunction"],
    "TestsConstants": ["tests.helpers.constants", "TestsConstants"],
    "TestsModels": ["tests.helpers.models", "TestsModels"],
    "TestsProtocols": ["tests.helpers.protocols", "TestsProtocols"],
    "TestsTypings": ["tests.helpers.typings", "TestsTypings"],
    "analysis_results": ["tests.conftest", "analysis_results"],
    "analysis_task_data": ["tests.conftest", "analysis_task_data"],
    "assert_analysis_results_structure": ["tests.helpers.typing_helpers", "assert_analysis_results_structure"],
    "assert_dict_structure": ["tests.helpers.typing_helpers", "assert_dict_structure"],
    "assert_is_dict": ["tests.helpers.typing_helpers", "assert_is_dict"],
    "assert_is_list": ["tests.helpers.typing_helpers", "assert_is_list"],
    "assert_issues_structure": ["tests.helpers.typing_helpers", "assert_issues_structure"],
    "assert_metrics_structure": ["tests.helpers.typing_helpers", "assert_metrics_structure"],
    "assert_result_failure_with_error": ["tests.conftest", "assert_result_failure_with_error"],
    "assert_result_success_with_data": ["tests.conftest", "assert_result_success_with_data"],
    "c": ["tests.constants", "FlextQualityTestConstants"],
    "celery_config": ["tests.conftest", "celery_config"],
    "code_analysis_config": ["tests.conftest", "code_analysis_config"],
    "codeclimate_config": ["tests.conftest", "codeclimate_config"],
    "d": ["flext_quality", "d"],
    "dashboard_data": ["tests.conftest", "dashboard_data"],
    "e": ["flext_quality", "e"],
    "h": ["flext_quality", "h"],
    "helpers": ["tests.helpers", ""],
    "m": ["tests.models", "FlextQualityTestModels"],
    "mock_quality_analyzer": ["tests.conftest", "mock_quality_analyzer"],
    "mock_report_generator": ["tests.conftest", "mock_report_generator"],
    "p": ["tests.protocols", "FlextQualityTestProtocols"],
    "package_metadata": ["tests.conftest", "package_metadata"],
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
    "test_basic": ["tests.unit.test_basic", "test_basic"],
    "u": ["tests.utilities", "FlextQualityTestUtilities"],
    "unit": ["tests.unit", ""],
    "x": ["flext_quality", "x"],
}

__all__ = [
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
    "c",
    "celery_config",
    "code_analysis_config",
    "codeclimate_config",
    "d",
    "dashboard_data",
    "e",
    "h",
    "helpers",
    "m",
    "mock_quality_analyzer",
    "mock_report_generator",
    "p",
    "package_metadata",
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
    "test_basic",
    "u",
    "unit",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
