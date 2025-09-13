"""Test DI container functionality using FlextContainer directly.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextContainer, FlextTypes


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
        assert result.success

        # Retrieve service
        get_result = container.get("quality_service")
        service = get_result.unwrap_or(None)
        assert service == test_service

    def test_quality_service_registration(self) -> None:
        """Test registering quality-specific services."""
        container = FlextContainer()

        # Register a quality analysis service (mock)
        class MockQualityAnalyzer:
            def analyze(self, __code: str) -> FlextTypes.Core.Dict:
                return {"quality_score": 85, "issues": []}

        analyzer = MockQualityAnalyzer()
        result = container.register("quality_analyzer", analyzer)
        assert result.success

        # Retrieve and test
        get_result = container.get("quality_analyzer")
        retrieved_analyzer = get_result.unwrap_or(None)
        assert retrieved_analyzer is not None
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
        assert not result.success
        assert result.error is not None
