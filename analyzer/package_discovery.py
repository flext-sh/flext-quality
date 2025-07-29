"""Python package discovery and analysis system."""

from __future__ import annotations

import importlib.metadata
import json
import site
from pathlib import Path
from typing import Any

# Use centralized logging
from flext_observability.structured_logging import get_logger

logger = get_logger(__name__)


class PackageDiscovery:
    """Discover and analyze Python packages for code analysis."""

    def __init__(self) -> None:
        """Initialize package discovery system."""
        self.packages_cache: dict[str, dict[str, Any]] = {}
        self._cached_packages: list[dict[str, Any]] | None = None

    def clear_cache(self) -> None:
        """Clear cached package information."""
        self._cached_packages = None
        self.packages_cache.clear()

    def get_installed_packages(self) -> list[dict[str, Any]]:
        """Get list of all installed packages."""
        if self._cached_packages is not None:
            return self._cached_packages

        packages: list[dict[str, Any]] = []

        # Use importlib.metadata for Python 3.8+
        for dist in importlib.metadata.distributions():
            package_info = self._analyze_package_fast(dist)
            if package_info:
                packages.append(package_info)

        # Sort by package type priority and name
        packages.sort(
            key=lambda x: (
                (
                    0
                    if x["package_type"] == "source"
                    else 1
                    if x["package_type"] == "wheel"
                    else 2
                ),
                x["name"].lower(),
            ),
        )

        # Cache the results
        self._cached_packages = packages
        return packages

    def _analyze_package_fast(
        self,
        dist: importlib.metadata.Distribution,
    ) -> dict[str, Any] | None:
        """Fast package analysis with minimal file system operations."""
        try:
            name = dist.metadata["Name"]
            version = dist.metadata["Version"]

            # Skip common system packages early
            if not self._is_interesting_package(name):
                return None

            # Get location with minimal file system operations
            location = self._get_package_location_fast(dist)

            # Determine package type
            package_type = self._determine_package_type_fast(dist, location)

            return {
                "name": name,
                "version": version,
                "location": location,
                "source_path": location,  # Use location as source_path for now
                "package_type": package_type,
                "description": dist.metadata.get("Summary", ""),
                "has_python_files": True,  # Assume true to avoid file system checks
                "estimated_size": 0,  # Skip size estimation for performance
            }
        except (RuntimeError, ValueError, TypeError):
            return None

    def _analyze_package(
        self,
        dist: importlib.metadata.Distribution,
    ) -> dict[str, Any] | None:
        """Detailed package analysis with file system checks."""
        try:
            name = dist.metadata["Name"]
            version = dist.metadata["Version"]

            # Get package location
            location = None
            if dist.files:
                # Get the first file to determine location
                first_file = next(iter(dist.files))
                location = str(Path(first_file.locate()).parent) if first_file else None

            # Determine package type
            package_type = self._determine_package_type(dist, location)

            # Skip system packages unless they're interesting for analysis
            if package_type == "system" and not self._is_interesting_package(name):
                return None

            # Get source path for analysis
            source_path = self._get_package_source_path(name, location)
            if not source_path or not Path(source_path).exists():
                return None

            return {
                "name": name,
                "version": version,
                "location": location,
                "source_path": source_path,
                "package_type": package_type,
                "description": dist.metadata.get("Summary", ""),
                "has_python_files": self._has_python_files(source_path),
                "estimated_size": self._estimate_package_size(source_path),
            }
        except (RuntimeError, ValueError, TypeError):
            return None

    def _determine_package_type(
        self,
        dist: importlib.metadata.Distribution,
        location: str | None,
    ) -> str:
        """Determine package type (source, wheel, system)."""
        if not location:
            return "system"

        location_path = Path(location)

        # Check if it's in site-packages
        site_packages = [Path(p) for p in site.getsitepackages()]
        if any(location_path.is_relative_to(sp) for sp in site_packages):
            # Check if it's a development installation
            if dist.files and any(".egg-link" in str(f) for f in dist.files):
                return "source"
            return "wheel"

        # Check if it's in user site-packages
        user_site = site.getusersitepackages()
        if user_site and location_path.is_relative_to(Path(user_site)):
            return "wheel"

        # Check for development installations
        if "site-packages" not in str(location_path):
            return "source"

        return "system"

    def _get_package_location_fast(
        self,
        dist: importlib.metadata.Distribution,
    ) -> str | None:
        """Get package location quickly."""
        try:
            # Check for editable installation first (development packages)
            if hasattr(dist, "read_text"):
                try:
                    direct_url = dist.read_text("direct_url.json")
                    if direct_url and "editable" in direct_url:
                        url_data = json.loads(direct_url)
                        if "url" in url_data and url_data["url"].startswith(
                            "file://",
                        ):
                            return str(url_data["url"][7:])  # Remove file://
                except (RuntimeError, ValueError, TypeError) as e:
                    logger.debug(
                        f"Failed to parse direct_url.json for {dist.metadata['name']}: {e}",
                    )

            # Try to get location from files
            if dist.files:
                first_file = next(iter(dist.files))
                return (
                    str(Path(first_file.locate()).parent.parent) if first_file else None
                )

            return None
        except (RuntimeError, ValueError, TypeError):
            return None

    def _determine_package_type_fast(
        self,
        dist: importlib.metadata.Distribution,
        location: str | None,
    ) -> str:
        """Fast package type determination."""
        if not location:
            return "system"

        # Check for development installation indicators
        try:
            # Check if it's outside site-packages (likely development)
            if location and "site-packages" not in str(location):
                return "source"

            # Check for .egg-link files (development installation)
            if dist.files and any(".egg-link" in str(f) for f in dist.files):
                return "source"

            # Check for editable installation
            if hasattr(dist, "read_text"):
                try:
                    direct_url = dist.read_text("direct_url.json")
                    if direct_url and "editable" in direct_url:
                        return "source"
                except (RuntimeError, ValueError, TypeError) as e:
                    logger.debug(
                        f"Failed to read direct_url.json for package type detection: {e}",
                    )

            return "wheel"
        except (RuntimeError, ValueError, TypeError):
            return "system"

    def _is_interesting_package(self, name: str) -> bool:
        """Check if package is interesting for analysis."""
        # Always include custom/local packages (those with flx, gruponos, etc.)
        if any(prefix in name.lower() for prefix in ["flx", "gruponos"]):
            return True

        # Skip common system packages and utilities that are not interesting for analysis
        skip_packages = {
            "pip",
            "setuptools",
            "wheel",
            "pkg-resources",
            "distribute",
            "certifi",
            "urllib3",
            "chardet",
            "idna",
            "requests",
            "six",
            "python-dateutil",
            "pytz",
            "packaging",
            "attrs",
            "cffi",
            "cryptography",
            "pycparser",
            "pyparsing",
            "markupsafe",
            "jinja2",
            "click",
            "blinker",
            "itsdangerous",
            "werkzeug",
            "pbr",
            "stevedore",
            "platformdirs",
            "tomli",
            "typing-extensions",
            "distlib",
            "filelock",
            "virtualenv",
            "pyproject-hooks",
            "build",
            "installer",
            "flit-core",
            "hatchling",
        }

        return name.lower() not in skip_packages

    def _get_package_source_path(
        self,
        package_name: str,
        location: str | None,
    ) -> str | None:
        """Get source path for package analysis."""
        if not location:
            return None

        location_path = Path(location)

        # Try different possible paths
        possible_paths = [
            location_path / package_name,
            location_path / package_name.replace("-", "_"),
            location_path / package_name.replace("_", "-"),
        ]

        for path in possible_paths:
            if path.exists() and path.is_dir():
                return str(path)

        # If location itself contains Python files, use it
        if self._has_python_files(str(location_path)):
            return str(location_path)

        return None

    def _has_python_files(self, path: str) -> bool:
        """Check if directory contains Python files."""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return False

            # Check for Python files in the directory
            for py_file in path_obj.rglob("*.py"):
                if not any(part.startswith(".") for part in py_file.parts):
                    return True

            return False
        except (RuntimeError, ValueError, TypeError):
            return False

    def _estimate_package_size(self, path: str) -> int:
        """Estimate package size by counting Python files."""
        try:
            path_obj = Path(path)
            return len(list(path_obj.rglob("*.py")))
        except (RuntimeError, ValueError, TypeError):
            return 0

    def get_package_by_name(self, package_name: str) -> dict[str, Any] | None:
        """Get package by name."""
        packages = self.get_installed_packages()
        for package in packages:
            if package["name"].lower() == package_name.lower():
                return package
        return None

    def search_packages(self, query: str) -> list[dict[str, Any]]:
        """Search packages by name or description."""
        packages = self.get_installed_packages()
        query_lower = query.lower()

        return [
            package
            for package in packages
            if query_lower in package["name"].lower()
            or query_lower in package.get("description", "").lower()
        ]

    def get_development_packages(self) -> list[dict[str, Any]]:
        """Get packages installed in development mode."""
        packages = self.get_installed_packages()
        return [p for p in packages if p["package_type"] == "source"]

    def get_analyzable_packages(self) -> list[dict[str, Any]]:
        """Get packages that can be analyzed."""
        packages = self.get_installed_packages()
        return [
            p for p in packages if p["has_python_files"] and p["estimated_size"] > 0
        ]
