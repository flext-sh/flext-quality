"""Service base for flext-quality tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_quality import m
from tests.settings import TestsFlextQualitySettings


class TestsFlextQualityServiceBase(tests_s):
    """Quality test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextQualitySettings:
        """Return the typed Quality+Tests settings singleton."""

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextQualitySettings)


s = TestsFlextQualityServiceBase

__all__: list[str] = ["TestsFlextQualityServiceBase", "s"]
