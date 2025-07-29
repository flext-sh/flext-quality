"""Test dependency injection container functionality."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from flext_quality.application.handlers import (
    AnalyzeProjectHandler,
    RunLintingHandler,
    RunSecurityCheckHandler,
)
from flext_quality.application.services import (
    AnalysisServiceImpl,
    LintingServiceImpl,
    SecurityAnalyzerServiceImpl,
)
from flext_quality.infrastructure.config import QualityConfig
from flext_quality.infrastructure.container import (
    QualityContainer,
    _create_analysis_result_repository,
    _create_analysis_service,
    _create_analyze_project_handler,
    _create_ast_analysis_port,
    _create_complexity_analysis_port,
    _create_dead_code_analysis_port,
    _create_duplicate_analysis_port,
    _create_linting_service,
    _create_quality_metrics_repository,
    _create_quality_rule_repository,
    _create_ruff_port,
    _create_run_linting_handler,
    _create_run_security_check_handler,
    _create_security_analyzer_port,
    _create_security_analyzer_service,
    configure_quality_dependencies,
    get_quality_container,
)
from flext_quality.infrastructure.persistence.repositories import (
    AnalysisResultRepository,
    QualityMetricsRepository,
    QualityRuleRepository,
)
from flext_quality.infrastructure.ports import (
    ASTAnalysisPort,
    BanditSecurityPort,
    ComplexityAnalysisPort,
    DeadCodeAnalysisPort,
    DuplicationAnalysisPort,
    RuffPort,
)


class TestFactoryFunctions:
    """Test factory functions for dependency creation."""

    def test_create_analysis_result_repository(self) -> None:
        """Test creating analysis result repository."""
        repo = _create_analysis_result_repository()
        assert isinstance(repo, AnalysisResultRepository)

    def test_create_quality_metrics_repository(self) -> None:
        """Test creating quality metrics repository."""
        repo = _create_quality_metrics_repository()
        assert isinstance(repo, QualityMetricsRepository)

    def test_create_quality_rule_repository(self) -> None:
        """Test creating quality rule repository."""
        repo = _create_quality_rule_repository()
        assert isinstance(repo, QualityRuleRepository)

    def test_create_ast_analysis_port(self) -> None:
        """Test creating AST analysis port."""
        config = QualityConfig()
        port = _create_ast_analysis_port(config)
        assert isinstance(port, ASTAnalysisPort)

    def test_create_security_analyzer_port(self) -> None:
        """Test creating security analyzer port."""
        config = QualityConfig()
        port = _create_security_analyzer_port(config)
        assert isinstance(port, BanditSecurityPort)

    def test_create_complexity_analysis_port(self) -> None:
        """Test creating complexity analysis port."""
        config = QualityConfig()
        port = _create_complexity_analysis_port(config)
        assert isinstance(port, ComplexityAnalysisPort)

    def test_create_dead_code_analysis_port(self) -> None:
        """Test creating dead code analysis port."""
        config = QualityConfig()
        port = _create_dead_code_analysis_port(config)
        assert isinstance(port, DeadCodeAnalysisPort)

    def test_create_duplicate_analysis_port(self) -> None:
        """Test creating duplicate analysis port."""
        config = QualityConfig()
        port = _create_duplicate_analysis_port(config)
        assert isinstance(port, DuplicationAnalysisPort)

    def test_create_ruff_port(self) -> None:
        """Test creating ruff port."""
        config = QualityConfig()
        port = _create_ruff_port(config)
        assert isinstance(port, RuffPort)

    def test_create_analysis_service(self) -> None:
        """Test creating analysis service."""
        config = QualityConfig()

        # Create all required dependencies
        ast_port = _create_ast_analysis_port(config)
        security_port = _create_security_analyzer_port(config)
        complexity_port = _create_complexity_analysis_port(config)
        dead_code_port = _create_dead_code_analysis_port(config)
        duplicate_port = _create_duplicate_analysis_port(config)
        repo = _create_analysis_result_repository()

        # Create service
        service = _create_analysis_service(
            ast_port=ast_port,
            security_port=security_port,
            complexity_port=complexity_port,
            dead_code_port=dead_code_port,
            duplicate_port=duplicate_port,
            repo=repo,
        )
        assert isinstance(service, AnalysisServiceImpl)

    def test_create_security_analyzer_service(self) -> None:
        """Test creating security analyzer service."""
        config = QualityConfig()
        port = _create_security_analyzer_port(config)
        repo = _create_analysis_result_repository()

        service = _create_security_analyzer_service(port=port, repo=repo)
        assert isinstance(service, SecurityAnalyzerServiceImpl)

    def test_create_linting_service(self) -> None:
        """Test creating linting service."""
        config = QualityConfig()
        port = _create_ruff_port(config)
        repo = _create_analysis_result_repository()

        service = _create_linting_service(port=port, repo=repo)
        assert isinstance(service, LintingServiceImpl)

    def test_create_analyze_project_handler(self) -> None:
        """Test creating analyze project handler."""
        service = AnalysisServiceImpl()
        handler = _create_analyze_project_handler(service)
        assert isinstance(handler, AnalyzeProjectHandler)

    def test_create_run_security_check_handler(self) -> None:
        """Test creating run security check handler."""
        service = SecurityAnalyzerServiceImpl()
        handler = _create_run_security_check_handler(service)
        assert isinstance(handler, RunSecurityCheckHandler)

    def test_create_run_linting_handler(self) -> None:
        """Test creating run linting handler."""
        service = LintingServiceImpl()
        handler = _create_run_linting_handler(service)
        assert isinstance(handler, RunLintingHandler)


class TestQualityContainer:
    """Test QualityContainer class."""

    def test_container_initialization(self) -> None:
        """Test container initialization."""
        container = QualityContainer()
        assert container is not None
        assert hasattr(container, "_instances")
        assert isinstance(container._instances, dict)
        assert len(container._instances) == 0

    def test_resolve_quality_config(self) -> None:
        """Test resolving QualityConfig."""
        container = QualityContainer()
        config = container.resolve(QualityConfig)

        assert isinstance(config, QualityConfig)
        # Should cache the instance
        config2 = container.resolve(QualityConfig)
        assert config is config2

    def test_resolve_analysis_result_repository(self) -> None:
        """Test resolving AnalysisResultRepository."""
        container = QualityContainer()
        repo = container.resolve(AnalysisResultRepository)

        assert isinstance(repo, AnalysisResultRepository)
        # Should cache the instance
        repo2 = container.resolve(AnalysisResultRepository)
        assert repo is repo2

    def test_resolve_quality_metrics_repository(self) -> None:
        """Test resolving QualityMetricsRepository."""
        container = QualityContainer()
        repo = container.resolve(QualityMetricsRepository)

        assert isinstance(repo, QualityMetricsRepository)
        # Should cache the instance
        repo2 = container.resolve(QualityMetricsRepository)
        assert repo is repo2

    def test_resolve_quality_rule_repository(self) -> None:
        """Test resolving QualityRuleRepository."""
        container = QualityContainer()
        repo = container.resolve(QualityRuleRepository)

        assert isinstance(repo, QualityRuleRepository)
        # Should cache the instance
        repo2 = container.resolve(QualityRuleRepository)
        assert repo is repo2

    def test_resolve_unknown_service_fallback(self) -> None:
        """Test resolving unknown service with fallback instantiation."""
        container = QualityContainer()

        # Create a simple test class
        class TestService:
            def __init__(self) -> None:
                self.initialized = True

        service = container.resolve(TestService)
        assert isinstance(service, TestService)
        assert service.initialized is True

        # Should cache the instance
        service2 = container.resolve(TestService)
        assert service is service2

    def test_resolve_unknown_service_with_args_fails(self) -> None:
        """Test resolving unknown service that requires args fails gracefully."""
        container = QualityContainer()

        # Create a test class that requires arguments
        class TestServiceWithArgs:
            def __init__(self, required_arg: str) -> None:
                self.required_arg = required_arg

        # Should raise TypeError when trying to instantiate without args
        with pytest.raises(TypeError):
            container.resolve(TestServiceWithArgs)

    def test_container_instances_isolation(self) -> None:
        """Test that different containers maintain separate instances."""
        container1 = QualityContainer()
        container2 = QualityContainer()

        config1 = container1.resolve(QualityConfig)
        config2 = container2.resolve(QualityConfig)

        # Different containers should have different instances
        assert config1 is not config2
        assert isinstance(config1, QualityConfig)
        assert isinstance(config2, QualityConfig)


class TestContainerGlobalFunctions:
    """Test global container management functions."""

    def teardown_method(self) -> None:
        """Clean up global container state after each test."""
        # Reset global container to clean state
        import flext_quality.infrastructure.container
        flext_quality.infrastructure.container._container = None

    def test_configure_quality_dependencies(self) -> None:
        """Test configuring quality dependencies."""
        configure_quality_dependencies()

        # Should create global container
        import flext_quality.infrastructure.container
        assert flext_quality.infrastructure.container._container is not None
        assert isinstance(
            flext_quality.infrastructure.container._container,
            QualityContainer
        )

    def test_get_quality_container_creates_if_not_exists(self) -> None:
        """Test get_quality_container creates container if it doesn't exist."""
        # Ensure container is None initially
        import flext_quality.infrastructure.container
        flext_quality.infrastructure.container._container = None

        container = get_quality_container()
        assert isinstance(container, QualityContainer)

        # Should return same instance on subsequent calls
        container2 = get_quality_container()
        assert container is container2

    def test_get_quality_container_returns_existing(self) -> None:
        """Test get_quality_container returns existing container."""
        # First call should create container
        container1 = get_quality_container()

        # Second call should return same instance
        container2 = get_quality_container()
        assert container1 is container2
        assert isinstance(container1, QualityContainer)

    @patch("flext_quality.infrastructure.container.QualityContainer")
    def test_get_quality_container_initialization_failure(
        self,
        mock_container_class: MagicMock
    ) -> None:
        """Test get_quality_container handles initialization failure."""
        # Mock container creation to return None (simulating failure)
        mock_container_class.return_value = None

        # Reset global container to trigger initialization
        import flext_quality.infrastructure.container
        flext_quality.infrastructure.container._container = None

        # Should raise RuntimeError when container fails to initialize
        with pytest.raises(RuntimeError, match="Container initialization failed"):
            get_quality_container()

    def test_container_singleton_behavior(self) -> None:
        """Test that global container maintains singleton behavior."""
        # Reset to clean state
        import flext_quality.infrastructure.container
        flext_quality.infrastructure.container._container = None

        # Multiple calls should return same instance
        container1 = get_quality_container()
        container2 = get_quality_container()
        container3 = get_quality_container()

        assert container1 is container2
        assert container2 is container3
        assert isinstance(container1, QualityContainer)


class TestContainerIntegration:
    """Test container integration scenarios."""

    def test_full_dependency_resolution_workflow(self) -> None:
        """Test complete dependency resolution workflow."""
        container = QualityContainer()

        # Resolve configuration
        config = container.resolve(QualityConfig)
        assert isinstance(config, QualityConfig)

        # Resolve repositories
        analysis_repo = container.resolve(AnalysisResultRepository)
        metrics_repo = container.resolve(QualityMetricsRepository)
        rules_repo = container.resolve(QualityRuleRepository)

        assert isinstance(analysis_repo, AnalysisResultRepository)
        assert isinstance(metrics_repo, QualityMetricsRepository)
        assert isinstance(rules_repo, QualityRuleRepository)

        # Verify caching works
        config2 = container.resolve(QualityConfig)
        assert config is config2

    def test_container_state_persistence(self) -> None:
        """Test that container maintains state across resolutions."""
        container = QualityContainer()

        # Resolve several services
        services = [
            container.resolve(QualityConfig),
            container.resolve(AnalysisResultRepository),
            container.resolve(QualityMetricsRepository),
            container.resolve(QualityRuleRepository),
        ]

        # All should be properly instantiated
        for service in services:
            assert service is not None

        # Container should have 4 cached instances
        assert len(container._instances) == 4

        # Re-resolving should return same instances
        for service_type in [QualityConfig, AnalysisResultRepository,
                            QualityMetricsRepository, QualityRuleRepository]:
            cached_service = container.resolve(service_type)
            assert cached_service in services

    def test_factory_functions_integration(self) -> None:
        """Test that factory functions work correctly with dependencies."""
        config = QualityConfig()

        # Test port creation with config
        ports = [
            _create_ast_analysis_port(config),
            _create_security_analyzer_port(config),
            _create_complexity_analysis_port(config),
            _create_dead_code_analysis_port(config),
            _create_duplicate_analysis_port(config),
            _create_ruff_port(config),
        ]

        # All ports should be properly created
        for port in ports:
            assert port is not None

        # Test repository creation
        repos = [
            _create_analysis_result_repository(),
            _create_quality_metrics_repository(),
            _create_quality_rule_repository(),
        ]

        # All repositories should be properly created
        for repo in repos:
            assert repo is not None

        # Test service creation with dependencies
        analysis_service = _create_analysis_service(
            ast_port=ports[0],
            security_port=ports[1],
            complexity_port=ports[2],
            dead_code_port=ports[3],
            duplicate_port=ports[4],
            repo=repos[0],
        )
        assert isinstance(analysis_service, AnalysisServiceImpl)
