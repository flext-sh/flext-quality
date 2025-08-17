"""Test version information."""

from __future__ import annotations

import re

from flext_quality import __version__, __version_info__


class TestVersion:
    """Test version information functionality."""

    def test_version_exists(self) -> None:
        """Test that version string exists."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_format(self) -> None:
        """Test version follows semantic versioning format."""
        # Semantic versioning pattern (X.Y.Z or X.Y.Z-suffix)
        pattern = r"^\d+\.\d+\.\d+(?:[-\w\.]+)?$"
        assert re.match(pattern, __version__), (
            f"Version '{__version__}' doesn't follow semantic versioning"
        )

    def test_version_info_exists(self) -> None:
        """Test that version info tuple exists."""
        assert __version_info__ is not None
        assert isinstance(__version_info__, tuple)
        assert len(__version_info__) >= 3

    def test_version_info_components(self) -> None:
        """Test version info tuple components are integers."""
        for component in __version_info__:
            assert isinstance(component, int)
            assert component >= 0

    def test_version_consistency(self) -> None:
        """Test version string and tuple consistency."""
        version_parts = __version__.split(".")
        major, minor, patch = version_parts[:3]

        # Extract numeric parts only
        major_num = int(major)
        minor_num = int(minor)
        patch_num = int(patch.split("-")[0])  # Handle pre-release versions

        assert __version_info__[0] == major_num
        assert __version_info__[1] == minor_num
        assert __version_info__[2] == patch_num

    def test_version_not_empty(self) -> None:
        """Test version is not empty or just dots."""
        assert __version__.strip()
        assert __version__ != "..."
        assert not __version__.startswith(".")
        assert not __version__.endswith(".")

    def test_fallback_version(self) -> None:
        """Test fallback version handling."""
        # This tests the fallback logic indirectly
        # If package is not installed, it should use "0.9.0"
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) >= 3, "Version must have at least major.minor.patch"
