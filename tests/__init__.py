# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_quality import d, e, h, r, s, x

    from . import helpers as helpers, unit as unit
    from .conftest import (
        MockQualityAnalyzer,
        MockReportGenerator,
        T,
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
    from .constants import TestsFlextQualityConstants, TestsFlextQualityConstants as c
    from .helpers.constants import TestsConstants
    from .helpers.models import TestsModels
    from .helpers.protocols import TestsProtocols
    from .helpers.typing_helpers import (
        assert_analysis_results_structure,
        assert_dict_structure,
        assert_is_dict,
        assert_is_list,
        assert_issues_structure,
        assert_metrics_structure,
        safe_dict_access,
        safe_list_access,
    )
    from .helpers.typings import TestsTypings
    from .models import TestsFlextQualityModels, TestsFlextQualityModels as m, tm
    from .protocols import TestsFlextQualityProtocols, TestsFlextQualityProtocols as p
    from .typings import TestsFlextQualityTypes, TestsFlextQualityTypes as t
    from .unit.test_api import (
        TestFlextQualityAPI,
        TestFlextQualityHookExecution,
        TestFlextQualityRulesConfig,
        TestFlextQualitySingleton,
        TestFlextQualityStdinProcessing,
        TestFlextQualityValidation,
    )
    from .unit.test_basic import test_basic
    from .unit.test_cli import TestFlextQualityCliService, TestMainFunction
    from .utilities import TestsFlextQualityUtilities, TestsFlextQualityUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "MockQualityAnalyzer": ("tests.conftest", "MockQualityAnalyzer"),
    "MockReportGenerator": ("tests.conftest", "MockReportGenerator"),
    "T": ("tests.conftest", "T"),
    "TestFlextQualityAPI": ("tests.unit.test_api", "TestFlextQualityAPI"),
    "TestFlextQualityCliService": ("tests.unit.test_cli", "TestFlextQualityCliService"),
    "TestFlextQualityHookExecution": (
        "tests.unit.test_api",
        "TestFlextQualityHookExecution",
    ),
    "TestFlextQualityRulesConfig": (
        "tests.unit.test_api",
        "TestFlextQualityRulesConfig",
    ),
    "TestFlextQualitySingleton": ("tests.unit.test_api", "TestFlextQualitySingleton"),
    "TestFlextQualityStdinProcessing": (
        "tests.unit.test_api",
        "TestFlextQualityStdinProcessing",
    ),
    "TestFlextQualityValidation": ("tests.unit.test_api", "TestFlextQualityValidation"),
    "TestMainFunction": ("tests.unit.test_cli", "TestMainFunction"),
    "TestsConstants": ("tests.helpers.constants", "TestsConstants"),
    "TestsFlextQualityConstants": ("tests.constants", "TestsFlextQualityConstants"),
    "TestsFlextQualityModels": ("tests.models", "TestsFlextQualityModels"),
    "TestsFlextQualityProtocols": ("tests.protocols", "TestsFlextQualityProtocols"),
    "TestsFlextQualityTypes": ("tests.typings", "TestsFlextQualityTypes"),
    "TestsFlextQualityUtilities": ("tests.utilities", "TestsFlextQualityUtilities"),
    "TestsModels": ("tests.helpers.models", "TestsModels"),
    "TestsProtocols": ("tests.helpers.protocols", "TestsProtocols"),
    "TestsTypings": ("tests.helpers.typings", "TestsTypings"),
    "analysis_results": ("tests.conftest", "analysis_results"),
    "analysis_task_data": ("tests.conftest", "analysis_task_data"),
    "assert_analysis_results_structure": (
        "tests.helpers.typing_helpers",
        "assert_analysis_results_structure",
    ),
    "assert_dict_structure": ("tests.helpers.typing_helpers", "assert_dict_structure"),
    "assert_is_dict": ("tests.helpers.typing_helpers", "assert_is_dict"),
    "assert_is_list": ("tests.helpers.typing_helpers", "assert_is_list"),
    "assert_issues_structure": (
        "tests.helpers.typing_helpers",
        "assert_issues_structure",
    ),
    "assert_metrics_structure": (
        "tests.helpers.typing_helpers",
        "assert_metrics_structure",
    ),
    "assert_result_failure_with_error": (
        "tests.conftest",
        "assert_result_failure_with_error",
    ),
    "assert_result_success_with_data": (
        "tests.conftest",
        "assert_result_success_with_data",
    ),
    "c": ("tests.constants", "TestsFlextQualityConstants"),
    "celery_config": ("tests.conftest", "celery_config"),
    "code_analysis_config": ("tests.conftest", "code_analysis_config"),
    "codeclimate_config": ("tests.conftest", "codeclimate_config"),
    "d": ("flext_quality", "d"),
    "dashboard_data": ("tests.conftest", "dashboard_data"),
    "e": ("flext_quality", "e"),
    "h": ("flext_quality", "h"),
    "helpers": ("tests.helpers", ""),
    "m": ("tests.models", "TestsFlextQualityModels"),
    "mock_quality_analyzer": ("tests.conftest", "mock_quality_analyzer"),
    "mock_report_generator": ("tests.conftest", "mock_report_generator"),
    "p": ("tests.protocols", "TestsFlextQualityProtocols"),
    "package_metadata": ("tests.conftest", "package_metadata"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "quality_metrics_data": ("tests.conftest", "quality_metrics_data"),
    "r": ("flext_quality", "r"),
    "report_config": ("tests.conftest", "report_config"),
    "s": ("flext_quality", "s"),
    "safe_dict_access": ("tests.helpers.typing_helpers", "safe_dict_access"),
    "safe_list_access": ("tests.helpers.typing_helpers", "safe_list_access"),
    "sample_code_repository": ("tests.conftest", "sample_code_repository"),
    "secure_temp_dir": ("tests.conftest", "secure_temp_dir"),
    "set_test_environment": ("tests.conftest", "set_test_environment"),
    "sonarqube_config": ("tests.conftest", "sonarqube_config"),
    "t": ("tests.typings", "TestsFlextQualityTypes"),
    "temporary_project_structure": ("tests.conftest", "temporary_project_structure"),
    "test_basic": ("tests.unit.test_basic", "test_basic"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextQualityUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_quality", "x"),
}

__all__ = [
    "MockQualityAnalyzer",
    "MockReportGenerator",
    "T",
    "TestFlextQualityAPI",
    "TestFlextQualityCliService",
    "TestFlextQualityHookExecution",
    "TestFlextQualityRulesConfig",
    "TestFlextQualitySingleton",
    "TestFlextQualityStdinProcessing",
    "TestFlextQualityValidation",
    "TestMainFunction",
    "TestsConstants",
    "TestsFlextQualityConstants",
    "TestsFlextQualityModels",
    "TestsFlextQualityProtocols",
    "TestsFlextQualityTypes",
    "TestsFlextQualityUtilities",
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
    "tm",
    "u",
    "unit",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
