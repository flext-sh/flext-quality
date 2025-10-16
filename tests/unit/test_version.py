"""Version metadata tests for flext-quality."""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextProjectMetadata, FlextProjectPerson

from flext_quality import __version__, __version_info__
from flext_quality.version import VERSION, FlextQualityVersion


def test_dunder_alignment() -> None:
    """__version__ mirrors the canonical VERSION object."""
    assert __version__ == VERSION.version
    assert __version_info__ == VERSION.version_info


def test_version_metadata() -> None:
    """VERSION exposes the normalized project metadata."""
    assert isinstance(VERSION, FlextQualityVersion)
    assert isinstance(VERSION.metadata, FlextProjectMetadata)
    assert VERSION.project
    assert isinstance(VERSION.urls, Mapping)
    assert VERSION.version_tuple == VERSION.version_info


def test_contact_information() -> None:
    """Primary author and maintainer are available as person objects."""
    assert isinstance(VERSION.author, FlextProjectPerson)
    assert isinstance(VERSION.maintainer, FlextProjectPerson)
    assert VERSION.author_name
    assert VERSION.maintainer_name


def test_author_and_maintainer_lists() -> None:
    """Tuple accessors mirror the underlying metadata dataclass."""
    assert VERSION.authors == VERSION.metadata.authors
    assert VERSION.maintainers == VERSION.metadata.maintainers
