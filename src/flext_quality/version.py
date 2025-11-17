"""Project metadata for flext quality."""

from __future__ import annotations

from typing import Final

from .__version__ import __version__, __version_info__


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

    @property
    def version_tuple(self) -> tuple[int | str, ...]:
        """Return the version info tuple (alias for compatibility)."""
        return self._version_info

    @property
    def metadata(self) -> dict[str, object]:
        """Return project metadata."""
        return {
            "name": "flext-quality",
            "version": self._version,
            "description": "Code quality analysis and metrics for FLEXT ecosystem",
            "authors": ["FLEXT Team"],
            "maintainers": ["FLEXT Team"],
            "license": "MIT",
            "url": "https://github.com/flext/flext-quality",
            "project_urls": {
                "Documentation": "https://flext-quality.readthedocs.io/",
                "Source": "https://github.com/flext/flext-quality",
                "Tracker": "https://github.com/flext/flext-quality/issues",
            },
        }

    @property
    def project(self) -> str:
        """Return project name."""
        return "flext-quality"

    @property
    def urls(self) -> dict[str, object]:
        """Return project URLs."""
        urls = self.metadata["project_urls"]
        if isinstance(urls, dict):
            return urls
        return {}

    @property
    def author(self) -> str:
        """Return primary author."""
        return "FLEXT Team"

    @property
    def maintainer(self) -> str:
        """Return primary maintainer."""
        return "FLEXT Team"

    @property
    def author_name(self) -> str:
        """Return author name."""
        return self.author

    @property
    def maintainer_name(self) -> str:
        """Return maintainer name."""
        return self.maintainer

    @property
    def authors(self) -> list[str]:
        """Return list of authors."""
        authors = self.metadata["authors"]
        if isinstance(authors, list):
            return authors
        return ["FLEXT Team"]

    @property
    def maintainers(self) -> list[str]:
        """Return list of maintainers."""
        maintainers = self.metadata["maintainers"]
        if isinstance(maintainers, list):
            return maintainers
        return ["FLEXT Team"]

    @classmethod
    def current(cls) -> FlextQualityVersion:
        """Return canonical metadata loaded from package."""
        return cls(__version__, __version_info__)


VERSION: Final[FlextQualityVersion] = FlextQualityVersion.current()

__all__ = ["VERSION", "FlextQualityVersion", "__version__", "__version_info__"]
