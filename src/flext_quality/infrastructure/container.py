"""Dependency injection container for FLEXT-QUALITY.
REFACTORED:
            Uses Lato DI framework with flext-core patterns.
"""
from __future__ import annotations

from flext_core.config import get_container

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


# Funções de fábrica
def _create_analysis_result_repository() -> AnalysisResultRepository:
    return AnalysisResultRepository()


def _create_quality_metrics_repository() -> QualityMetricsRepository:
    return QualityMetricsRepository()


def _create_quality_rule_repository() -> QualityRuleRepository:
    return QualityRuleRepository()


def _create_ast_analysis_port(config: QualityConfig) -> ASTAnalysisPort:
    return ASTAnalysisPort(config)


def _create_security_analyzer_port(config: QualityConfig) -> BanditSecurityPort:
    return BanditSecurityPort(config)


def _create_complexity_analysis_port(config: QualityConfig) -> ComplexityAnalysisPort:
    return ComplexityAnalysisPort(config)


def _create_dead_code_analysis_port(config: QualityConfig) -> DeadCodeAnalysisPort:
    return DeadCodeAnalysisPort(config)


def _create_duplicate_analysis_port(config: QualityConfig) -> DuplicationAnalysisPort:
    return DuplicationAnalysisPort(config)


def _create_ruff_port(config: QualityConfig) -> RuffPort:
    return RuffPort(config)


def _create_analysis_service(
    ast_port: ASTAnalysisPort,
    security_port: BanditSecurityPort,
    complexity_port: ComplexityAnalysisPort,
    dead_code_port: DeadCodeAnalysisPort,
    duplicate_port: DuplicationAnalysisPort,
    repo: AnalysisResultRepository,
) -> AnalysisServiceImpl:
    return AnalysisServiceImpl()


def _create_security_analyzer_service(
    port: BanditSecurityPort,
    repo: AnalysisResultRepository,
) -> SecurityAnalyzerServiceImpl:
    return SecurityAnalyzerServiceImpl(port=port, repository=repo)


def _create_linting_service(
    port: RuffPort,
    repo: AnalysisResultRepository,
) -> LintingServiceImpl:
    return LintingServiceImpl()


def _create_analyze_project_handler(
    service: AnalysisServiceImpl,
) -> AnalyzeProjectHandler:
    return AnalyzeProjectHandler()


def _create_run_security_check_handler(
    service: SecurityAnalyzerServiceImpl,
) -> RunSecurityCheckHandler:
    return RunSecurityCheckHandler()


def _create_run_linting_handler(service: LintingServiceImpl) -> RunLintingHandler:
    return RunLintingHandler()


# Classe do container DI
class QualityContainer:
    """Dependency injection container for FLEXT-QUALITY."""

    def __init__(self) -> None:
        """Initialize the quality container."""
        self._instances: dict[str, object] = {}

    def resolve(self, service_type: type[object]) -> object:
        """Resolve a service instance."""
        service_name = service_type.__name__
        # Simple service resolution - create if not exists
        if service_name not in self._instances:
            if service_type == QualityConfig:
                self._instances[service_name] = QualityConfig()
            elif service_type == AnalysisResultRepository:
                self._instances[service_name] = _create_analysis_result_repository()
            elif service_type == QualityMetricsRepository:
                self._instances[service_name] = _create_quality_metrics_repository()
            elif service_type == QualityRuleRepository:
                self._instances[service_name] = _create_quality_rule_repository()
            # Add more service types as needed
            else:
                # Fallback: try to instantiate
                self._instances[service_name] = service_type()
        return self._instances[service_name]


# Container instance
_container: QualityContainer | None = None


def configure_quality_dependencies() -> None:
    """Configure quality-specific dependencies."""
    # Get core container (but not used in simplified implementation)
    get_container()
    # Create quality container
    global _container
    _container = QualityContainer()


def get_quality_container() -> QualityContainer:
    global _container
    if _container is None:
        configure_quality_dependencies()
    # Ensure container is properly initialized
    if _container is None:
        msg = "Container initialization failed"
        raise RuntimeError(msg)
    return _container
