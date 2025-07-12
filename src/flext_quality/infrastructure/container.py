"""Dependency injection container for FLEXT-QUALITY.

REFACTORED:
            Uses Lato DI framework with flext-core patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from lato import Container, DependencyProvider, Scope

from flext_core.infrastructure.di import (
    configure_dependencies as configure_core_dependencies,
)
from flext_core.infrastructure.di import (
    get_container,
)
from flext_quality.application.handlers import (
    AnalyzeProjectHandler,
    GenerateReportHandler,
    RunLintingHandler,
    RunSecurityCheckHandler,
)
from flext_quality.application.services import (
    AnalysisServiceImpl,
    LintingServiceImpl,
    ReportGeneratorServiceImpl,
    SecurityAnalyzerServiceImpl,
)

if TYPE_CHECKING:
            from flext_quality.domain.ports import (
        AnalysisService,
        LintingService,
        ReportGeneratorService,
        SecurityAnalyzerService,
    )

from flext_quality.infrastructure.config import QualityConfig

# Importações necessárias para as funções de fábrica
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
    DuplicateAnalysisPort,
    HTMLReportGeneratorPort,
    JSONReportGeneratorPort,
    MarkdownReportGeneratorPort,
    RuffLintingPort,
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


def _create_duplicate_analysis_port(config: QualityConfig) -> DuplicateAnalysisPort:
        return DuplicateAnalysisPort(config)


def _create_html_report_generator(config: QualityConfig) -> HTMLReportGeneratorPort:
        return HTMLReportGeneratorPort(config)


def _create_json_report_generator(config: QualityConfig) -> JSONReportGeneratorPort:
        return JSONReportGeneratorPort(config)


def _create_markdown_report_generator( config: QualityConfig ) -> MarkdownReportGeneratorPort:
        return MarkdownReportGeneratorPort(config)


def _create_ruff_linting_port(config: QualityConfig) -> RuffLintingPort:
        return RuffLintingPort(config)


def _create_analysis_service( ast_port: ASTAnalysisPort, security_port: BanditSecurityPort, complexity_port: ComplexityAnalysisPort, dead_code_port: DeadCodeAnalysisPort, duplicate_port: DuplicateAnalysisPort, repo: AnalysisResultRepository ) -> AnalysisService:
        return AnalysisServiceImpl(
        ast_port=ast_port,
        security_port=security_port,
        complexity_port=complexity_port,
        dead_code_port=dead_code_port,
        duplicate_port=duplicate_port,
        repository=repo,
    )


def _create_security_analyzer_service( port: BanditSecurityPort, repo: AnalysisResultRepository ) -> SecurityAnalyzerService:
        return SecurityAnalyzerServiceImpl(port=port, repository=repo)


def _create_linting_service( port: RuffLintingPort, repo: AnalysisResultRepository ) -> LintingService:
        return LintingServiceImpl(port=port, repository=repo)


def _create_report_generator_service( html_generator: HTMLReportGeneratorPort, json_generator: JSONReportGeneratorPort, markdown_generator: MarkdownReportGeneratorPort, repo: AnalysisResultRepository ) -> ReportGeneratorService:
        return ReportGeneratorServiceImpl(
        html_generator=html_generator,
        json_generator=json_generator,
        markdown_generator=markdown_generator,
        repository=repo,
    )


def _create_analyze_project_handler(service: AnalysisService) -> AnalyzeProjectHandler:
        return AnalyzeProjectHandler(service=service)


def _create_run_security_check_handler( service: SecurityAnalyzerService ) -> RunSecurityCheckHandler:
        return RunSecurityCheckHandler(service=service)


def _create_run_linting_handler(service: LintingService) -> RunLintingHandler:
        return RunLintingHandler(service=service)


def _create_generate_report_handler( service: ReportGeneratorService ) -> GenerateReportHandler:
        return GenerateReportHandler(service=service)


# Classe do container DI
class QualityContainer(Container):
    """Dependency injection container for FLEXT-QUALITY."""

    # Configuration
    config: QualityConfig = DependencyProvider(QualityConfig, scope=Scope.SINGLETON)

    # Repositories
    analysis_result_repository: AnalysisResultRepository = DependencyProvider(
        _create_analysis_result_repository,
        scope=Scope.SINGLETON,
    )
    quality_metrics_repository: QualityMetricsRepository = DependencyProvider(
        _create_quality_metrics_repository,
        scope=Scope.SINGLETON,
    )
    quality_rule_repository: QualityRuleRepository = DependencyProvider(
        _create_quality_rule_repository,
        scope=Scope.SINGLETON,
    )

    # Infrastructure services (ports)
    ast_analysis_port: ASTAnalysisPort = DependencyProvider(
        _create_ast_analysis_port,
        scope=Scope.SINGLETON,
    )
    security_analyzer_port: BanditSecurityPort = DependencyProvider(
        _create_security_analyzer_port,
        scope=Scope.SINGLETON,
    )
    complexity_analysis_port: ComplexityAnalysisPort = DependencyProvider(
        _create_complexity_analysis_port,
        scope=Scope.SINGLETON,
    )
    dead_code_analysis_port: DeadCodeAnalysisPort = DependencyProvider(
        _create_dead_code_analysis_port,
        scope=Scope.SINGLETON,
    )
    duplicate_analysis_port: DuplicateAnalysisPort = DependencyProvider(
        _create_duplicate_analysis_port,
        scope=Scope.SINGLETON,
    )

    # Report generators
    html_report_generator: HTMLReportGeneratorPort = DependencyProvider(
        _create_html_report_generator,
        scope=Scope.SINGLETON,
    )
    json_report_generator: JSONReportGeneratorPort = DependencyProvider(
        _create_json_report_generator,
        scope=Scope.SINGLETON,
    )
    markdown_report_generator: MarkdownReportGeneratorPort = DependencyProvider(
        _create_markdown_report_generator,
        scope=Scope.SINGLETON,
    )

    # Linting services
    ruff_linting_port: RuffLintingPort = DependencyProvider(
        _create_ruff_linting_port,
        scope=Scope.SINGLETON,
    )

    # Domain services
    analysis_service: AnalysisService = DependencyProvider(
        _create_analysis_service,
        scope=Scope.REQUEST,
    )
    security_analyzer_service: SecurityAnalyzerService = DependencyProvider(
        _create_security_analyzer_service,
        scope=Scope.REQUEST,
    )
    linting_service: LintingService = DependencyProvider(
        _create_linting_service,
        scope=Scope.REQUEST,
    )
    report_generator_service: ReportGeneratorService = DependencyProvider(
        _create_report_generator_service,
        scope=Scope.REQUEST,
    )

    # Application handlers
    analyze_project_handler: AnalyzeProjectHandler = DependencyProvider(
        _create_analyze_project_handler,
        scope=Scope.REQUEST,
    )
    run_security_check_handler: RunSecurityCheckHandler = DependencyProvider(
        _create_run_security_check_handler,
        scope=Scope.REQUEST,
    )
    run_linting_handler: RunLintingHandler = DependencyProvider(
        _create_run_linting_handler,
        scope=Scope.REQUEST,
    )
    generate_report_handler: GenerateReportHandler = DependencyProvider(
        _create_generate_report_handler,
        scope=Scope.REQUEST,
    )


# Container instance
_container: QualityContainer | None = None


def configure_quality_dependencies() -> None:
        # First configure core dependencies
    configure_core_dependencies()

    # Get core container and extend it
    container = get_container()

    # Register quality-specific services
    global _container
    _container = QualityContainer()

    # Register with core container if needed:
    container.register("quality_config", _container.config)
    container.register("quality_container", _container)


def get_quality_container() -> QualityContainer:
    global _container
    if _container is None:
        configure_quality_dependencies()
    return _container  # type: ignore[return-value]
