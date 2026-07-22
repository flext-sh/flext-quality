"""Runtime settings for flext-quality tests."""

from __future__ import annotations

from flext_quality import FlextQualitySettings
from flext_tests import FlextTestsSettings


class TestsFlextQualitySettings(FlextQualitySettings, FlextTestsSettings):
    """Quality settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextQualitySettings"]
