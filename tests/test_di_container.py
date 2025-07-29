"""Test DI container functionality."""

from __future__ import annotations

from unittest.mock import patch

from flext_core import FlextContainer

from flext_quality.infrastructure.di_container import (
    configure_flext_quality_dependencies,
    get_flext_quality_container,
    get_flext_quality_service,
)


class TestDIContainer:
    """Test dependency injection container functionality."""

    def test_get_flext_quality_container(self) -> None:
        """Test getting flext quality container instance."""
        container = get_flext_quality_container()
        assert isinstance(container, FlextContainer)

    def test_get_flext_quality_container_singleton(self) -> None:
        """Test container returns same instance (singleton pattern)."""
        container1 = get_flext_quality_container()
        container2 = get_flext_quality_container()
        assert container1 is container2

    def test_configure_flext_quality_dependencies(self) -> None:
        """Test configuring flext quality dependencies."""
        # This should not raise any exceptions
        configure_flext_quality_dependencies()

    @patch("flext_quality.infrastructure.di_container.logger")
    def test_configure_dependencies_success_logging(self, mock_logger: object) -> None:
        """Test successful dependency configuration logs info."""
        configure_flext_quality_dependencies()
        # Should log success message
        mock_logger.info.assert_called()

    @patch("flext_quality.infrastructure.di_container.logger")
    def test_configure_dependencies_exception_handling(self, mock_logger: object) -> None:
        """Test exception handling in dependency configuration."""
        # This method currently doesn't have complex logic that throws ImportError
        # So we'll test the basic functionality and logging
        configure_flext_quality_dependencies()
        # Should log info on successful configuration
        mock_logger.info.assert_called()

    def test_get_flext_quality_service_not_found(self) -> None:
        """Test getting non-existent service returns None."""
        result = get_flext_quality_service("non_existent_service")
        assert result is None

    @patch("flext_quality.infrastructure.di_container.logger")
    def test_get_service_not_found_logging(self, mock_logger: object) -> None:
        """Test service not found logs warning."""
        get_flext_quality_service("non_existent_service")
        mock_logger.warning.assert_called()

    def test_get_flext_quality_service_success(self) -> None:
        """Test getting existing service returns the service."""
        container = get_flext_quality_container()
        test_service = "test_service_instance"

        # Register a test service
        result = container.register("test_service", test_service)
        assert result.is_success

        # Retrieve the service
        retrieved = get_flext_quality_service("test_service")
        assert retrieved == test_service

    def test_container_integration(self) -> None:
        """Test full container integration workflow."""
        container = get_flext_quality_container()

        # Register service
        service_name = "integration_test_service"
        service_instance = {"data": "test"}

        result = container.register(service_name, service_instance)
        assert result.is_success

        # Retrieve via helper function
        retrieved = get_flext_quality_service(service_name)
        assert retrieved == service_instance

        # Clean up
        container.clear()

    def test_module_initialization(self) -> None:
        """Test module initializes dependencies on import."""
        # The module should have already called configure_flext_quality_dependencies
        # on import, so the container should exist
        container = get_flext_quality_container()
        assert container is not None
