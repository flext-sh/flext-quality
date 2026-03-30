# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
    from tests.conftest import *
    from tests.constants import *
    from tests.helpers import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

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
