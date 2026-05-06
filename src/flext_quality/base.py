"""Shared service foundation for flext-quality components."""

from __future__ import annotations

from abc import ABC
from typing import override

from flext_core import s
from flext_quality import FlextQualitySettings, t


class FlextQualityServiceBase[TResult: t.JsonValue = t.JsonDict](s[TResult], ABC):
    """Base class for flext-quality services with typed settings access.

    Generic over the service result type so consumers can specialize:
    ``FlextQualityServiceBase[bool]`` for boolean-returning commands etc.
    """

    @property
    @override
    def settings(self) -> FlextQualitySettings:
        """Return the typed quality settings singleton (rule 1, propagating)."""
        return FlextQualitySettings.fetch_global()


s = FlextQualityServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextQualityServiceBase", "s"]
