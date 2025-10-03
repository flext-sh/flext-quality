"""Project metadata for flext quality."""

from __future__ import annotations

from typing import Final

from flext_quality.__version__ import __version__, __version_info__


class FlextQualityVersion:
    """Structured metadata for the flext quality distribution."""

    def __init__(self, version: str, version_info: tuple[int | str, ...]) -> None:
        """Initialize version metadata.

        Args:
            version: Version string (e.g., "1.0.0")
            version_info: Version info tuple

        """
        self._version = version
        self._version_info = version_info

    @property
    def version(self) -> str:
        """Return the version string."""
        return self._version

    @property
    def version_info(self) -> tuple[int | str, ...]:
        """Return the version info tuple."""
        return self._version_info

    @classmethod
    def current(cls) -> FlextQualityVersion:
        """Return canonical metadata loaded from package."""
        return cls(__version__, __version_info__)


VERSION: Final[FlextQualityVersion] = FlextQualityVersion.current()

__all__ = ["VERSION", "FlextQualityVersion", "__version__", "__version_info__"]
