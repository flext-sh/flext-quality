"""Scalar constants for flext-quality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Final


class FlextQualityConstantsValues:
    """Scalar constants mixed into ``c.Quality`` and ``c.Quality.LinkCheckerDemo``."""

    class Quality:
        """Quality scalar constants."""

        DEFAULT_CONFIG: Final[str] = str(
            Path(__file__).resolve().parent.parent
            / "docs"
            / "settings"
            / "schedule_config.yaml"
        )

        THRESHOLD_MAX_BROKEN_LINKS_TO_SHOW: Final[int] = 10
        "Maximum broken links to show."

    class LinkCheckerDemo:
        """Demo link fixtures for the documentation link checker."""

        VSCODE_URL: Final[str] = "https://github.com/microsoft/vscode"
        HTTPBIN_OK_URL: Final[str] = "https://httpbin.org/status/200"
        HTTPBIN_BROKEN_URL: Final[str] = "https://httpbin.org/status/404"


__all__: list[str] = ["FlextQualityConstantsValues"]
