"""Test dependency injection container functionality."""

from __future__ import annotations

from flext_quality.infrastructure.container import get_quality_container


class TestQualityContainer:
    """Test quality container functionality."""

    def test_get_quality_container(self) -> None:
        """Test getting quality container."""
        container = get_quality_container()
        assert container is not None
        # Should be a FlextContainer from flext-core
        assert hasattr(container, "register")
        assert hasattr(container, "get")
        assert hasattr(container, "get_typed")
