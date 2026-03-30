# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_quality import *
    from tests import conftest, constants, models, protocols, typings, utilities
    from tests.conftest import *
    from tests.constants import *
    from tests.helpers import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextQualityTestConstants": "tests.constants",
    "FlextQualityTestModels": "tests.models",
    "FlextQualityTestProtocols": "tests.protocols",
    "FlextQualityTestTypes": "tests.typings",
    "FlextQualityTestUtilities": "tests.utilities",
    "MockQualityAnalyzer": "tests.conftest",
    "MockReportGenerator": "tests.conftest",
    "TestFlextQualityAPI": "tests.unit.test_api",
    "TestFlextQualityCliService": "tests.unit.test_cli",
    "TestFlextQualityHookExecution": "tests.unit.test_api",
    "TestFlextQualityRulesConfig": "tests.unit.test_api",
    "TestFlextQualitySingleton": "tests.unit.test_api",
    "TestFlextQualityStdinProcessing": "tests.unit.test_api",
    "TestFlextQualityValidation": "tests.unit.test_api",
    "TestMainFunction": "tests.unit.test_cli",
    "TestsConstants": "tests.helpers.constants",
    "TestsModels": "tests.helpers.models",
    "TestsProtocols": "tests.helpers.protocols",
    "TestsTypings": "tests.helpers.typings",
    "analysis_results": "tests.conftest",
    "analysis_task_data": "tests.conftest",
    "assert_analysis_results_structure": "tests.helpers.typing_helpers",
    "assert_dict_structure": "tests.helpers.typing_helpers",
    "assert_is_dict": "tests.helpers.typing_helpers",
    "assert_is_list": "tests.helpers.typing_helpers",
    "assert_issues_structure": "tests.helpers.typing_helpers",
    "assert_metrics_structure": "tests.helpers.typing_helpers",
    "assert_result_failure_with_error": "tests.conftest",
    "assert_result_success_with_data": "tests.conftest",
    "assertions": "tests.helpers.assertions",
    "c": ["tests.constants", "FlextQualityTestConstants"],
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
    "m": ["tests.models", "FlextQualityTestModels"],
    "mock_quality_analyzer": "tests.conftest",
    "mock_report_generator": "tests.conftest",
    "models": "tests.models",
    "p": ["tests.protocols", "FlextQualityTestProtocols"],
    "package_metadata": "tests.conftest",
    "protocols": "tests.protocols",
    "pytest_configure": "tests.conftest",
    "quality_metrics_data": "tests.conftest",
    "r": "flext_quality",
    "report_config": "tests.conftest",
    "s": "flext_quality",
    "safe_dict_access": "tests.helpers.typing_helpers",
    "safe_list_access": "tests.helpers.typing_helpers",
    "sample_code_repository": "tests.conftest",
    "secure_temp_dir": "tests.conftest",
    "set_test_environment": "tests.conftest",
    "sonarqube_config": "tests.conftest",
    "t": ["tests.typings", "FlextQualityTestTypes"],
    "temporary_project_structure": "tests.conftest",
    "test_api": "tests.unit.test_api",
    "test_basic": "tests.unit.test_basic",
    "test_cli": "tests.unit.test_cli",
    "typing_helpers": "tests.helpers.typing_helpers",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextQualityTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_quality",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
