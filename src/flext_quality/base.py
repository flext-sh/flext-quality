"""Base class for analysis backends using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from pathlib import Path

from flext_core import FlextResult

from .backend_type import BackendType


class FlextQualityAnalyzer(ABC):
    """Abstract base class for code analyzers using flext-core patterns."""

    @abstractmethod
    def analyze(
        self,
        _code: str,
        file_path: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Analyze code and return results.

        Args:
        _code: Source code to analyze
        file_path: Optional file path for context

        Returns:
        FlextResult containing analysis results dictionary

        """
        ...

    @abstractmethod
    def get_backend_type(self: object) -> BackendType:
        """Get the type of this backend.

        Returns:
        BackendType enum value

        """
        ...

    @abstractmethod
    def get_capabilities(self: object) -> list[str]:
        """Get list of capabilities this backend provides.

        Returns:
        List of capability strings

        """
        ...


# Legacy compatibility facade (temporary)
BaseAnalyzer = FlextQualityAnalyzer
warnings.warn(
    "BaseAnalyzer is deprecated; use FlextQualityAnalyzer",
    DeprecationWarning,
    stacklevel=2,
)
