# Infrastructure Layer - External Dependencies and Adapters

The infrastructure layer contains all external dependencies, third-party integrations, and adapter implementations that connect the FLEXT Quality application to the outside world. This layer implements the interfaces defined in the domain layer, following Clean Architecture principles with proper dependency inversion.

## Architecture Principles

This layer follows the Dependency Inversion Principle by:

- **Interface Implementation**: All components implement domain-defined interfaces
- **External Dependency Isolation**: External services are isolated behind adapters
- **Configuration Management**: Centralized configuration for all external dependencies
- **Error Handling**: Consistent error handling and resilience patterns
- **Testability**: All adapters are mockable and testable in isolation

## Key Components

### Configuration Management (`config.py`)

Centralized configuration management for external dependencies:

**Responsibilities:**

- Environment variable management and validation
- External service configuration (databases, message queues, monitoring)
- Quality analysis tool configuration (Ruff, MyPy, Bandit)
- Security configuration and secrets management
- Feature flags and environment-specific settings

**Integration Points:**

- Environment-specific configuration files
- Secret management systems (HashiCorp Vault, Kubernetes secrets)
- Configuration validation with Pydantic models
- Hot reloading for development environments

### Dependency Injection Container (`container.py`)

Service registration and lifecycle management:

**Responsibilities:**

- Service registration and dependency resolution
- Singleton and transient service lifecycle management
- Interface binding to concrete implementations
- Configuration injection into services
- Health check registration and monitoring

**FLEXT Core Integration:**

```python
from flext_core import FlextContainer

def get_quality_container() -> FlextContainer:
    """Configure dependency injection container for quality services."""
    container = get_flext_container()

    # Register repository implementations
    container.register("quality_project_repository", QualityProjectRepository())
    container.register("quality_analysis_repository", QualityAnalysisRepository())

    # Register external tool adapters
    container.register("ruff_analyzer", RuffAnalyzerAdapter())
    container.register("mypy_analyzer", MyPyAnalyzerAdapter())
    container.register("bandit_analyzer", BanditAnalyzerAdapter())

    # Register application services
    container.register("quality_project_service", QualityProjectService())
    container.register("quality_analysis_service", QualityAnalysisService())

    return container
```

## Repository Implementations

### Data Persistence Patterns

Implementation of domain repository interfaces using various persistence technologies:

#### **QualityProjectRepository**

Manages project data persistence and retrieval:

- Project configuration and metadata storage
- Quality threshold management
- Analysis history tracking
- Integration with version control systems

#### **QualityAnalysisRepository**

Handles analysis result persistence:

- Analysis execution state management
- Quality metrics storage and aggregation
- Issue tracking and resolution status
- Historical analysis data archival

#### **QualityMetricsRepository**

Specialized metrics data management:

- Time-series metrics storage
- Aggregation and rollup operations
- Performance optimization for large datasets
- Integration with monitoring systems

### Persistence Technology Options

#### **Option 1: Django ORM Integration**

```python
class DjangoQualityProjectRepository(QualityProjectRepository):
    """Django ORM-based project repository implementation."""

    async def save(self, project: QualityProject) -> FlextResult[QualityProject]:
        try:
            django_model = await self._to_django_model(project)
            await django_model.asave()
            return FlextResult.ok(project)
        except Exception as e:
            return FlextResult.fail(f"Failed to save project: {e}")
```

#### **Option 2: Pure Repository Pattern**

```python
class PostgreSQLQualityProjectRepository(QualityProjectRepository):
    """PostgreSQL-based project repository using asyncpg."""

    def __init__(self, connection_pool: asyncpg.Pool):
        self._pool = connection_pool

    async def save(self, project: QualityProject) -> FlextResult[QualityProject]:
        async with self._pool.acquire() as conn:
            # Direct SQL operations with proper transaction handling
            pass
```

## External Tool Integrations

### Analysis Tool Adapters

Adapter implementations for external code analysis tools:

#### **RuffAnalyzerAdapter**

Python linting and code quality analysis:

```python
class RuffAnalyzerAdapter(SecurityAnalyzerService):
    """Adapter for Ruff Python linter integration."""

    async def analyze_project(self, project_path: str) -> FlextResult[list[QualityIssue]]:
        try:
            # Execute ruff with configured rules
            result = await self._execute_ruff(project_path)

            # Convert ruff output to domain QualityIssue entities
            issues = self._convert_to_quality_issues(result)

            return FlextResult.ok(issues)
        except Exception as e:
            return FlextResult.fail(f"Ruff analysis failed: {e}")

    async def _execute_ruff(self, project_path: str) -> dict:
        """Execute ruff analysis with timeout and error handling."""
        process = await asyncio.create_subprocess_exec(
            "ruff", "check", project_path, "--format", "json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=300  # 5 minute timeout
        )

        if process.returncode not in [0, 1]:  # 1 = issues found, still success
            raise AnalysisError(f"Ruff failed: {stderr.decode()}")

        return json.loads(stdout.decode())
```

#### **MyPyAnalyzerAdapter**

Static type checking and validation:

```python
class MyPyAnalyzerAdapter(LintingService):
    """Adapter for MyPy static type checker integration."""

    def __init__(self, config_path: str = "pyproject.toml"):
        self._config_path = config_path
        self._mypy_config = self._load_mypy_config()

    async def validate_types(self, project_path: str) -> FlextResult[list[QualityIssue]]:
        # MyPy analysis implementation with proper error handling
        pass
```

#### **BanditAnalyzerAdapter**

Security vulnerability scanning:

```python
class BanditAnalyzerAdapter(SecurityAnalyzerService):
    """Adapter for Bandit security scanner integration."""

    async def scan_vulnerabilities(self, project_path: str) -> FlextResult[list[QualityIssue]]:
        # Bandit security scanning with confidence and severity filtering
        pass
```

#### **CoverageAnalyzerAdapter**

Test coverage measurement and reporting:

```python
class CoverageAnalyzerAdapter(MetricsCollectorService):
    """Adapter for coverage.py test coverage analysis."""

    async def collect_coverage_metrics(self, project_path: str) -> FlextResult[CoverageMetric]:
        # Coverage analysis with line, branch, and function coverage
        pass
```

## External Service Integrations

### Monitoring and Observability

Integration with monitoring and observability platforms:

#### **FlextObservabilityAdapter**

```python
class FlextObservabilityAdapter:
    """Integration with flext-observability monitoring stack."""

    def __init__(self, observability_config: ObservabilityConfig):
        self._config = observability_config
        self._metrics_client = self._initialize_metrics_client()
        self._tracing_client = self._initialize_tracing_client()

    async def publish_quality_metrics(self, metrics: QualityMetrics) -> FlextResult[None]:
        """Publish quality metrics to observability platform."""
        try:
            await self._metrics_client.gauge(
                name="quality_overall_score",
                value=metrics.overall_score,
                tags={"project": metrics.project_id}
            )

            await self._metrics_client.counter(
                name="quality_issues_total",
                value=metrics.total_issues,
                tags={
                    "project": metrics.project_id,
                    "severity": "all"
                }
            )

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Failed to publish metrics: {e}")
```

#### **NotificationAdapter**

Alert and notification management:

```python
class NotificationAdapter:
    """Adapter for notification services (Slack, email, webhooks)."""

    async def send_quality_alert(
        self,
        alert: QualityAlert,
        channels: list[NotificationChannel]
    ) -> FlextResult[None]:
        """Send quality threshold violation alerts."""
        # Multi-channel notification implementation
        pass
```

### Event Publishing

Integration with event streaming and message queues:

#### **EventPublisherAdapter**

```python
class EventPublisherAdapter:
    """Adapter for publishing domain events to external systems."""

    def __init__(self, event_bus_config: EventBusConfig):
        self._config = event_bus_config
        self._publisher = self._initialize_publisher()

    async def publish_event(self, event: DomainEvent) -> FlextResult[None]:
        """Publish domain events to external event bus."""
        try:
            event_data = {
                "event_type": event.__class__.__name__,
                "event_data": event.model_dump(),
                "timestamp": event.occurred_at.isoformat(),
                "correlation_id": event.correlation_id
            }

            await self._publisher.publish(
                topic=f"quality.{event.aggregate_type}",
                message=event_data
            )

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Failed to publish event: {e}")
```

## File System Abstractions

### Project File Access

Abstracted file system operations for code analysis:

#### **ProjectFileSystemAdapter**

```python
class ProjectFileSystemAdapter:
    """Adapter for secure project file system access."""

    def __init__(self, security_config: FileSystemSecurityConfig):
        self._security_config = security_config
        self._allowed_paths = security_config.allowed_paths

    async def list_python_files(self, project_path: str) -> FlextResult[list[Path]]:
        """List Python files with security validation."""
        try:
            # Validate path is within allowed directories
            if not self._is_path_allowed(project_path):
                return FlextResult.fail(f"Path not allowed: {project_path}")

            python_files = []
            project_dir = Path(project_path)

            for py_file in project_dir.rglob("*.py"):
                # Skip hidden files and build artifacts
                if self._should_skip_file(py_file):
                    continue

                python_files.append(py_file)

            return FlextResult.ok(python_files)
        except Exception as e:
            return FlextResult.fail(f"Failed to list files: {e}")

    def _is_path_allowed(self, path: str) -> bool:
        """Validate path against security allowlist."""
        path_obj = Path(path).resolve()

        for allowed_path in self._allowed_paths:
            if path_obj.is_relative_to(allowed_path):
                return True

        return False
```

## Error Handling and Resilience

### Circuit Breaker Pattern

Fault tolerance for external service calls:

```python
class CircuitBreakerAdapter:
    """Circuit breaker implementation for external service calls."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self._failure_threshold = failure_threshold
        self._timeout = timeout
        self._failure_count = 0
        self._last_failure_time = None
        self._state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, operation: Callable[[], Awaitable[T]]) -> FlextResult[T]:
        """Execute operation with circuit breaker protection."""
        if self._state == "OPEN":
            if self._should_attempt_reset():
                self._state = "HALF_OPEN"
            else:
                return FlextResult.fail("Circuit breaker is open")

        try:
            result = await operation()
            self._on_success()
            return FlextResult.ok(result)
        except Exception as e:
            self._on_failure()
            return FlextResult.fail(f"Operation failed: {e}")
```

### Retry Logic

Configurable retry patterns for transient failures:

```python
@retry(
    max_attempts=3,
    backoff_strategy=ExponentialBackoff(base_delay=1.0, max_delay=30.0),
    retry_exceptions=(ConnectionError, TimeoutError)
)
async def execute_with_retry(self, operation: Callable[[], Awaitable[T]]) -> T:
    """Execute operation with exponential backoff retry logic."""
    return await operation()
```

## Testing Support

### Mock Implementations

Mock adapter implementations for testing:

```python
class MockRuffAnalyzerAdapter(SecurityAnalyzerService):
    """Mock Ruff analyzer for testing purposes."""

    def __init__(self):
        self.analyzed_projects: list[str] = []
        self.mock_issues: list[QualityIssue] = []

    async def analyze_project(self, project_path: str) -> FlextResult[list[QualityIssue]]:
        self.analyzed_projects.append(project_path)
        return FlextResult.ok(self.mock_issues.copy())

    def set_mock_issues(self, issues: list[QualityIssue]) -> None:
        """Configure mock issues for testing scenarios."""
        self.mock_issues = issues
```

### Test Utilities

Helper functions for infrastructure testing:

```python
class InfrastructureTestUtils:
    """Utilities for testing infrastructure layer components."""

    @staticmethod
    def create_test_container() -> FlextContainer:
        """Create test container with mock implementations."""
        container = FlextContainer()

        # Register mock implementations
        container.register("ruff_analyzer", MockRuffAnalyzerAdapter())
        container.register("mypy_analyzer", MockMyPyAnalyzerAdapter())

        return container

    @staticmethod
    async def wait_for_external_service(
        service_url: str,
        timeout: int = 30
    ) -> bool:
        """Wait for external service to become available in tests."""
        # Implementation for integration test setup
        pass
```

## Configuration Examples

### Environment Configuration

```yaml
# infrastructure/config/development.yml
database:
  url: postgresql://postgres:postgres@localhost:5432/flext_quality
  pool_size: 10
  max_overflow: 20

redis:
  url: redis://localhost:6379/0
  connection_pool_size: 10

external_tools:
  ruff:
    enabled: true
    timeout: 300
    config_file: pyproject.toml

  mypy:
    enabled: true
    strict_mode: true
    timeout: 600

  bandit:
    enabled: true
    confidence_level: medium
    severity_level: low

observability:
  metrics_endpoint: http://localhost:9090
  tracing_endpoint: http://localhost:14268
  service_name: flext-quality

notifications:
  slack:
    webhook_url: ${SLACK_WEBHOOK_URL}
    default_channel: "#quality-alerts"

  email:
    smtp_server: smtp.company.com
    smtp_port: 587
    from_email: quality@company.com
```

### Security Configuration

```python
class SecurityConfig:
    """Security configuration for infrastructure layer."""

    # File system access restrictions
    ALLOWED_PROJECT_PATHS = [
        Path("/workspace/projects"),
        Path("/tmp/analysis"),
    ]

    # External tool execution restrictions
    TOOL_EXECUTION_TIMEOUT = 600  # 10 minutes
    MAX_CONCURRENT_ANALYSES = 5

    # Network security
    ALLOWED_EXTERNAL_HOSTS = [
        "api.github.com",
        "pypi.org",
    ]

    # Secret management
    SECRET_ENCRYPTION_KEY = "${SECRET_ENCRYPTION_KEY}"
    VAULT_ENDPOINT = "${VAULT_ENDPOINT}"
```

## Integration Patterns

### FLEXT Ecosystem Integration

Standard patterns for integrating with other FLEXT services:

```python
class FlextEcosystemIntegration:
    """Integration patterns with FLEXT ecosystem services."""

    def __init__(self, ecosystem_config: EcosystemConfig):
        self._config = ecosystem_config
        self._service_registry = self._initialize_service_registry()

    async def register_quality_service(self) -> FlextResult[None]:
        """Register quality service with ecosystem service registry."""
        service_info = {
            "service_name": "flext-quality",
            "version": "0.9.0",
            "endpoints": {
                "health": "/health",
                "metrics": "/metrics",
                "analysis": "/api/v1/analysis"
            },
            "capabilities": [
                "code_quality_analysis",
                "security_scanning",
                "metrics_collection"
            ]
        }

        return await self._service_registry.register(service_info)
```

## Related Documentation

- **[Domain Layer](../domain/README.md)** - Core business entities and rules
- **[Application Layer](../application/README.md)** - Service orchestration and workflows
- **[FLEXT Core Integration](../../../docs/architecture/flext-core-integration.md)** - Foundation patterns
- **[External Tool Integration](../../../docs/integration/external-tools.md)** - Tool adapter patterns
