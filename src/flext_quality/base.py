"""Shared service foundation for flext-quality components."""

from __future__ import annotations

from abc import ABC
from typing import override

from flext_core import FlextSettings, s
from flext_quality import FlextQualitySettings, t


class FlextQualityServiceBase(s[t.JsonMapping], ABC):
    """Base class for flext-quality services with typed settings access."""

    @property
    @override
    def settings(self) -> FlextQualitySettings:
        """Return the typed quality settings namespace."""
        return FlextSettings.fetch_global().fetch_namespace(
            "quality", FlextQualitySettings
        )


s = FlextQualityServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextQualityServiceBase", "s"]
