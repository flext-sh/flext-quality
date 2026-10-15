"""Shared service foundation for flext-quality components.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC

from flext_core import FlextService

from flext_quality import t


class FlextQualityServiceBase[TResult = t.JsonDict](FlextService[TResult], ABC):
    """Base class for flext-quality services with typed settings access.

    Generic over the service result type so consumers can specialize:
    ``FlextQualityServiceBase[bool]`` for boolean-returning commands etc.
    """


s = FlextQualityServiceBase

__all__: t.MutableSequenceOf[str] = ["FlextQualityServiceBase", "s"]
