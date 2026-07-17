"""Shared service foundation for flext-quality components."""

from __future__ import annotations

from abc import ABC

from flext_core import s
from flext_quality import p, t


class FlextQualityServiceBase[TResult: p.BaseModel = t.JsonDict](s[TResult], ABC):
    """Base class for flext-quality services with typed settings access.

    Generic over the service result type so consumers can specialize:
    ``FlextQualityServiceBase[bool]`` for boolean-returning commands etc.
    """


s = FlextQualityServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextQualityServiceBase", "s"]
