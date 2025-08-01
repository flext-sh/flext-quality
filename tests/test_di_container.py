"""Test DI container functionality using FlextContainer directly."""

from __future__ import annotations

from flext_core import FlextContainer


class TestDIContainer:
    """Test dependency injection using FlextContainer directly."""

    def test_flext_container_creation(self) -> None:
        """Test creating FlextContainer instance directly."""
        container = FlextContainer()
        assert isinstance(container, FlextContainer)

    def test_service_registration_and_retrieval(self) -> None:
        """Test registering and retrieving services from container."""
        container = FlextContainer()

        # Create a test service
        test_service = "test_quality_service"

        # Register service
        result = container.register("quality_service", test_service)
        assert result.is_success

        # Retrieve service
        get_result = container.get("quality_service")
        assert get_result.is_success
        assert get_result.data == test_service

    def test_quality_service_registration(self) -> None:
        """Test registering quality-specific services."""
        container = FlextContainer()

        # Register a quality analysis service (mock)
        class MockQualityAnalyzer:
            def analyze(self, code: str) -> dict:
                return {"quality_score": 85, "issues": []}

        analyzer = MockQualityAnalyzer()
        result = container.register("quality_analyzer", analyzer)
        assert result.is_success

        # Retrieve and test
        get_result = container.get("quality_analyzer")
        assert get_result.is_success
        retrieved_analyzer = get_result.data
        assert hasattr(retrieved_analyzer, "analyze")

        # Test functionality
        analysis = retrieved_analyzer.analyze("def hello(): pass")
        assert isinstance(analysis, dict)
        assert "quality_score" in analysis

    def test_container_error_handling(self) -> None:
        """Test container handles errors properly."""
        container = FlextContainer()

        # Test getting non-existent service
        result = container.get("non_existent_service")
        assert not result.is_success
        assert result.error is not None
