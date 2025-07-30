"""Test DI container functionality."""

from __future__ import annotations

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

    def test_configure_dependencies_success_logging(self) -> None:
        """Test successful dependency configuration - DRY approach without mocks."""
        # Real test: dependency configuration should work without exceptions
        try:
            configure_flext_quality_dependencies()
            # If we get here, configuration succeeded
            assert True
        except Exception as e:
            msg = f"Dependency configuration failed: {e}"
            raise AssertionError(msg) from e

    def test_configure_dependencies_idempotent(self) -> None:
        """Test multiple calls to configure dependencies are safe."""
        # DRY approach: test actual behavior instead of mocking
        configure_flext_quality_dependencies()
        configure_flext_quality_dependencies()  # Should not fail on second call

        # Verify container is still functional
        container = get_flext_quality_container()
        assert isinstance(container, FlextContainer)

    def test_get_flext_quality_service_not_found(self) -> None:
        """Test getting non-existent service returns None - DRY approach."""
        result = get_flext_quality_service("non_existent_service")
        assert result is None

    def test_get_service_real_behavior(self) -> None:
        """Test real service retrieval behavior without mocking."""
        # DRY approach: test actual behavior
        configure_flext_quality_dependencies()

        # Test that container exists
        container = get_flext_quality_container()
        assert isinstance(container, FlextContainer)

        # Test non-existent service returns None
        result = get_flext_quality_service("definitely_does_not_exist")
        assert result is None

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
