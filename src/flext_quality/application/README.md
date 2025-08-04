# Application Layer - Business Workflows and Service Orchestration

The application layer orchestrates business workflows for quality analysis operations, coordinating between domain entities and infrastructure services while maintaining clean separation of concerns.

## Architecture Principles

This layer implements the application service pattern with:

- **Workflow Orchestration**: Coordinates complex multi-step business processes
- **Transaction Management**: Ensures consistency across domain operations
- **Cross-Cutting Concerns**: Handles logging, validation, and error management
- **Interface Adaptation**: Bridges domain and infrastructure layers
- **Command/Query Separation**: Implements CQRS patterns for scalability

## Core Responsibilities

### Business Workflow Management

- **Analysis Pipeline Orchestration**: Manages end-to-end quality analysis workflows
- **Multi-Step Process Coordination**: Coordinates complex operations across services
- **Dependency Management**: Handles service dependencies and execution ordering
- **Error Recovery**: Implements rollback and compensation patterns

### Service Coordination

- **Domain Service Integration**: Coordinates multiple domain services
- **Infrastructure Service Management**: Manages external tool integration
- **Resource Allocation**: Handles concurrent analysis execution
- **Performance Optimization**: Implements caching and optimization strategies

### Transaction Boundaries

- **Consistency Guarantees**: Ensures data consistency across operations
- **Atomic Operations**: Groups related changes into single transactions
- **Rollback Mechanisms**: Handles failure scenarios gracefully
- **Event Publishing**: Publishes domain events within transaction boundaries

## Service Classes

### QualityProjectService

Manages project lifecycle and configuration workflows.

**Core Operations:**

```python
async def create_project(
    self,
    project_data: ProjectCreationData
) -> FlextResult[QualityProject]:
    """Create new quality project with validation and setup."""

async def configure_quality_thresholds(
    self,
    project_id: str,
    thresholds: QualityThresholds
) -> FlextResult[QualityProject]:
    """Update project quality thresholds with validation."""

async def get_project_history(
    self,
    project_id: str,
    limit: int = 50
) -> FlextResult[list[QualityAnalysis]]:
    """Retrieve project analysis history with pagination."""
```

**Business Workflows:**

- **Project Setup**: Creates project with default configurations
- **Threshold Management**: Updates quality standards with validation
- **History Tracking**: Maintains chronological analysis records
- **Configuration Validation**: Ensures settings are compatible and achievable

### QualityAnalysisService

Orchestrates analysis execution and result processing workflows.

**Core Operations:**

```python
async def execute_comprehensive_analysis(
    self,
    project_id: str,
    configuration: AnalysisConfiguration
) -> FlextResult[QualityAnalysis]:
    """Execute complete quality analysis with all backends."""

async def execute_targeted_analysis(
    self,
    project_id: str,
    target_files: list[str],
    analysis_types: list[AnalysisType]
) -> FlextResult[QualityAnalysis]:
    """Execute focused analysis on specific files and types."""

async def monitor_analysis_progress(
    self,
    analysis_id: str
) -> FlextResult[AnalysisProgress]:
    """Track real-time analysis execution progress."""
```

**Business Workflows:**

- **Analysis Orchestration**: Coordinates multi-backend analysis execution
- **Progress Monitoring**: Tracks and reports analysis execution status
- **Result Aggregation**: Combines results from multiple analysis backends
- **Quality Assessment**: Calculates scores and generates quality grades

### QualityReportService

Manages report generation and distribution workflows.

**Core Operations:**

```python
async def generate_executive_report(
    self,
    analysis_id: str,
    format: ReportFormat = ReportFormat.HTML
) -> FlextResult[QualityReport]:
    """Generate high-level executive quality summary."""

async def generate_technical_report(
    self,
    analysis_id: str,
    include_details: bool = True
) -> FlextResult[QualityReport]:
    """Generate detailed technical analysis report."""

async def generate_comparative_report(
    self,
    project_id: str,
    baseline_analysis_id: str,
    current_analysis_id: str
) -> FlextResult[QualityReport]:
    """Generate trend analysis comparing two analysis results."""
```

**Business Workflows:**

- **Multi-Format Generation**: Creates reports in HTML, JSON, and PDF formats
- **Stakeholder Customization**: Tailors content for different audiences
- **Historical Comparison**: Generates trend analysis and progress tracking
- **Distribution Management**: Handles report delivery and notification

### QualityMetricsService

Handles metrics collection and aggregation processes.

**Core Operations:**

```python
async def collect_project_metrics(
    self,
    project_id: str,
    analysis_configuration: MetricsConfiguration
) -> FlextResult[QualityMetrics]:
    """Collect comprehensive project-wide quality metrics."""

async def aggregate_ecosystem_metrics(
    self,
    project_ids: list[str],
    time_range: TimeRange
) -> FlextResult[EcosystemMetrics]:
    """Aggregate metrics across multiple FLEXT projects."""

async def calculate_trend_metrics(
    self,
    project_id: str,
    time_range: TimeRange
) -> FlextResult[TrendMetrics]:
    """Calculate quality trends over specified time period."""
```

**Business Workflows:**

- **Metrics Aggregation**: Combines file-level metrics into project summaries
- **Trend Calculation**: Analyzes quality changes over time
- **Ecosystem Analysis**: Provides cross-project quality insights
- **Threshold Monitoring**: Tracks compliance with quality standards

## CQRS Implementation

### Command Handlers

Handle state-changing operations with validation and event publishing.

```python
class CreateQualityProjectCommand:
    project_name: str
    project_path: str
    quality_thresholds: dict[str, float]

class CreateQualityProjectHandler:
    async def handle(
        self,
        command: CreateQualityProjectCommand
    ) -> FlextResult[QualityProject]:
        # Validation, creation, and event publishing
        pass
```

**Command Types:**

- **CreateQualityProject**: Initialize new project for analysis
- **ExecuteQualityAnalysis**: Start comprehensive quality analysis
- **UpdateQualityThresholds**: Modify project quality standards
- **GenerateQualityReport**: Create analysis reports

### Query Handlers

Handle read operations with optimized data retrieval.

```python
class GetProjectQualityHistoryQuery:
    project_id: str
    limit: int
    offset: int

class GetProjectQualityHistoryHandler:
    async def handle(
        self,
        query: GetProjectQualityHistoryQuery
    ) -> FlextResult[list[QualityAnalysis]]:
        # Optimized data retrieval
        pass
```

**Query Types:**

- **GetProjectQualityHistory**: Retrieve analysis history
- **GetQualityMetrics**: Fetch current quality metrics
- **GetEcosystemOverview**: Cross-project quality dashboard
- **GetTrendAnalysis**: Historical quality trend data

## Event-Driven Architecture

### Domain Event Publishing

Application services publish domain events for observability and integration.

**Event Types:**

```python
class QualityAnalysisStartedEvent(DomainEvent):
    project_id: str
    analysis_id: str
    analysis_type: str
    started_at: datetime

class QualityIssueDetectedEvent(DomainEvent):
    project_id: str
    analysis_id: str
    issue: QualityIssue
    detected_at: datetime

class QualityThresholdViolatedEvent(DomainEvent):
    project_id: str
    analysis_id: str
    threshold_type: str
    actual_value: float
    threshold_value: float
```

### Event Handlers

Process domain events for cross-cutting concerns and integration.

**Handler Examples:**

- **NotificationHandler**: Sends alerts for quality threshold violations
- **MetricsHandler**: Updates monitoring dashboards with analysis results
- **AuditHandler**: Records analysis activities for compliance tracking
- **IntegrationHandler**: Publishes events to external systems

## Error Handling and Resilience

### FlextResult Pattern

All operations return FlextResult for consistent error handling.

```python
async def execute_analysis(
    self,
    project: QualityProject
) -> FlextResult[QualityAnalysis]:
    try:
        # Business logic implementation
        analysis = await self._orchestrate_analysis(project)

        # Validation
        validation_result = analysis.validate_domain_rules()
        if not validation_result.success:
            return validation_result.cast()

        # Success path
        await self._publish_analysis_completed_event(analysis)
        return FlextResult.ok(analysis)

    except AnalysisTimeoutError as e:
        return FlextResult.fail(f"Analysis timeout: {e}")
    except InsufficientResourcesError as e:
        return FlextResult.fail(f"Resource limitation: {e}")
    except Exception as e:
        logger.exception("Unexpected error during analysis")
        return FlextResult.fail(f"Analysis failed: {e}")
```

### Retry and Circuit Breaker Patterns

Handle transient failures and external service unavailability.

```python
@retry(max_attempts=3, backoff_strategy=ExponentialBackoff())
@circuit_breaker(failure_threshold=5, timeout=60)
async def execute_external_tool_analysis(
    self,
    tool: ExternalAnalysisTool,
    project_path: str
) -> FlextResult[AnalysisResult]:
    # External tool integration with resilience
    pass
```

## Performance Optimization

### Async Processing

Long-running operations use async patterns for scalability.

```python
async def execute_parallel_analysis(
    self,
    project: QualityProject,
    analysis_backends: list[AnalysisBackend]
) -> FlextResult[QualityAnalysis]:
    # Execute multiple analysis backends concurrently
    tasks = [
        backend.analyze_project(project)
        for backend in analysis_backends
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Aggregate results and handle partial failures
    return self._aggregate_analysis_results(results)
```

### Caching Strategy

Intelligent caching reduces repeated analysis overhead.

```python
@cached(
    key_builder=lambda project_id, config: f"analysis:{project_id}:{hash(config)}",
    ttl=timedelta(hours=1)
)
async def get_cached_analysis_results(
    self,
    project_id: str,
    configuration: AnalysisConfiguration
) -> FlextResult[QualityAnalysis]:
    # Cached analysis results for repeated requests
    pass
```

### Resource Management

Intelligent resource allocation for concurrent analyses.

```python
class AnalysisResourceManager:
    def __init__(self, max_concurrent_analyses: int = 3):
        self._semaphore = asyncio.Semaphore(max_concurrent_analyses)

    async def execute_with_resource_limit(
        self,
        analysis_func: Callable[[], Awaitable[T]]
    ) -> T:
        async with self._semaphore:
            return await analysis_func()
```

## Integration Patterns

### FLEXT Core Integration

Built on flext-core application patterns:

```python
from flext_core import FlextService, FlextContainer

class QualityAnalysisService(FlextService):
    def __init__(self, container: FlextContainer):
        super().__init__(container)
        self._analysis_repository = container.get(AnalysisRepository)
        self._metrics_collector = container.get(MetricsCollectorService)
        self._report_generator = container.get(ReportGeneratorService)
```

### Observability Integration

Comprehensive monitoring through flext-observability:

```python
from flext_observability import (
    flext_create_trace,
    flext_create_metric,
    flext_create_log_entry
)

async def execute_analysis(self, project: QualityProject) -> FlextResult[QualityAnalysis]:
    trace_id = f"analysis_{project.id}_{uuid4()}"

    flext_create_trace(
        trace_id=trace_id,
        operation="QualityAnalysisService.execute_analysis",
        context={"project_id": project.id}
    )

    start_time = time.time()

    try:
        result = await self._perform_analysis(project)

        # Record success metrics
        flext_create_metric(
            name="quality_analysis_duration",
            value=time.time() - start_time,
            tags={"project_id": project.id, "status": "success"}
        )

        return result
    except Exception as e:
        # Record failure metrics
        flext_create_metric(
            name="quality_analysis_failures",
            value=1,
            tags={"project_id": project.id, "error_type": type(e).__name__}
        )
        raise
```

## Testing Strategy

### Service Testing

Comprehensive testing of application service workflows:

```python
@pytest.mark.asyncio
async def test_quality_analysis_service_comprehensive_workflow():
    # Given
    project = create_test_project()
    service = QualityAnalysisService(test_container)

    # When
    result = await service.execute_comprehensive_analysis(
        project.id,
        AnalysisConfiguration(include_all=True)
    )

    # Then
    assert result.success
    analysis = result.data
    assert analysis.status == AnalysisStatus.COMPLETED
    assert analysis.overall_score >= 0.0
    assert len(analysis.issues) >= 0
```

### Integration Testing

End-to-end workflow validation:

```python
@pytest.mark.integration
async def test_full_analysis_workflow():
    # Test complete workflow from project creation to report generation
    project_service = QualityProjectService(container)
    analysis_service = QualityAnalysisService(container)
    report_service = QualityReportService(container)

    # Create project
    project_result = await project_service.create_project(test_data)
    project = project_result.data

    # Execute analysis
    analysis_result = await analysis_service.execute_comprehensive_analysis(
        project.id, default_config
    )
    analysis = analysis_result.data

    # Generate report
    report_result = await report_service.generate_executive_report(
        analysis.id, ReportFormat.HTML
    )
    report = report_result.data

    # Validate end-to-end workflow
    assert report.analysis_id == analysis.id
    assert report.project_id == project.id
```

## Usage Examples

### Basic Service Usage

```python
from flext_quality.application import QualityAnalysisService

# Initialize service with dependency injection
service = QualityAnalysisService(container)

# Execute comprehensive analysis
result = await service.execute_comprehensive_analysis(
    project_id="flext-core-project",
    configuration=AnalysisConfiguration(
        include_security=True,
        include_complexity=True,
        include_duplicates=True,
        max_analysis_time=timedelta(minutes=30)
    )
)

if result.success:
    analysis = result.data
    print(f"Quality Score: {analysis.overall_score}")
    print(f"Issues Found: {len(analysis.issues)}")
else:
    print(f"Analysis failed: {result.error}")
```

### Workflow Orchestration

```python
# Multi-step workflow with error handling
async def complete_quality_assessment_workflow(project_path: str):
    project_service = container.get(QualityProjectService)
    analysis_service = container.get(QualityAnalysisService)
    report_service = container.get(QualityReportService)

    # Step 1: Create project
    project_result = await project_service.create_project(
        ProjectCreationData(path=project_path)
    )
    if not project_result.success:
        return project_result.cast()

    # Step 2: Execute analysis
    analysis_result = await analysis_service.execute_comprehensive_analysis(
        project_result.data.id,
        AnalysisConfiguration.default()
    )
    if not analysis_result.success:
        return analysis_result.cast()

    # Step 3: Generate reports
    report_result = await report_service.generate_executive_report(
        analysis_result.data.id
    )

    return report_result
```

## Related Documentation

- **[Domain Layer](../domain/README.md)** - Core business entities and rules
- **[Infrastructure Layer](../infrastructure/README.md)** - External dependencies
- **[CQRS Implementation](../../docs/architecture/cqrs-patterns.md)** - Command/Query patterns
- **[Event-Driven Architecture](../../docs/architecture/event-driven-design.md)** - Event handling patterns
