# FLEXT Quality Development Guide

This guide provides comprehensive information for developers working on FLEXT Quality, including setup, patterns, standards, and workflows.

## Development Environment Setup

### Prerequisites

- **Python 3.13+** - Latest Python version with enhanced type system
- **Poetry** - Python dependency management and packaging
- **Docker & Docker Compose** - Containerization and service orchestration
- **Git** - Version control
- **Make** - Build automation
- **Node.js 18+** - For web UI development (if applicable)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality

# Complete development setup
make setup

# Verify installation
make diagnose
```

### Development Services

Start all required services for development:

```bash
# Option 1: All-in-one script
./start_all.sh

# Option 2: Docker Compose
docker-compose up -d

# Option 3: Manual setup
make install-dev
make web-migrate
make web-start
```

### Environment Configuration

Create a `.env` file for local development:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flext_quality_dev

# Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Django
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# FLEXT Integration
FLEXT_OBSERVABILITY_ENABLED=true
FLEXT_LOG_LEVEL=debug

# Quality Thresholds (Development)
QUALITY_MIN_COVERAGE=85.0  # Lower for development
QUALITY_MAX_COMPLEXITY=15  # Higher for development
```

## Project Structure

### Directory Organization

```
flext-quality/
├── src/flext_quality/           # Clean Architecture Implementation
│   ├── domain/                  # Domain Layer (Business Logic)
│   │   ├── entities.py         # Domain Entities
│   │   ├── value_objects.py    # Value Objects
│   │   ├── ports.py            # Interfaces/Ports
│   │   └── services.py         # Domain Services
│   ├── application/            # Application Layer (Use Cases)
│   │   ├── handlers.py         # Command/Query Handlers
│   │   ├── services.py         # Application Services
│   │   └── commands.py         # Commands & Queries
│   ├── infrastructure/         # Infrastructure Layer
│   │   ├── repositories.py     # Data Access
│   │   ├── services.py         # External Services
│   │   └── container.py        # Dependency Injection
│   └── presentation/           # Presentation Layer
│       ├── api/                # REST API
│       ├── web/                # Web Interface
│       └── cli/                # Command Line Interface
├── analyzer/                   # Django App (Legacy - Being Refactored)
├── dashboard/                  # Django Dashboard App
├── tests/                      # Test Suite
│   ├── unit/                   # Unit Tests
│   ├── integration/            # Integration Tests
│   └── e2e/                    # End-to-End Tests
├── docs/                       # Documentation
├── scripts/                    # Utility Scripts
└── docker/                     # Docker Configuration
```

### Key Architectural Files

- **`src/flext_quality/domain/entities.py`** - Core business entities
- **`src/flext_quality/application/services.py`** - Application services
- **`src/flext_quality/infrastructure/container.py`** - Dependency injection
- **`analyzer/models.py`** - Django models (being phased out)
- **`pyproject.toml`** - Project configuration and dependencies

## Development Patterns

### FLEXT Core Integration

All development must follow flext-core patterns:

```python
from flext_core import FlextEntity, FlextResult, FlextContainer
from flext_observability import flext_monitor_function

# Domain Entities
class QualityProject(FlextEntity):
    """Quality project domain entity following flext-core patterns."""
    name: str
    project_path: str

    def validate_standards(self) -> FlextResult[bool]:
        """Domain validation using FlextResult pattern."""
        if not self.project_path:
            return FlextResult[None].fail("Project path is required")
        return FlextResult[None].ok(True)

# Application Services
class QualityProjectService:
    """Application service with proper error handling."""

    @flext_monitor_function("create_project")
    async def create_project(self, name: str, path: str) -> FlextResult[QualityProject]:
        """Create project with monitoring and error handling."""
        try:
            project = QualityProject(name=name, project_path=path)
            validation = project.validate_standards()
            if not validation.success:
                return validation
            return FlextResult[None].ok(project)
        except Exception as e:
            return FlextResult[None].fail(f"Failed to create project: {e}")
```

### Clean Architecture Implementation

Follow strict Clean Architecture boundaries:

```python
# ✅ CORRECT: Domain → Application dependency
from flext_quality.domain.entities import QualityProject
from flext_quality.application.services import QualityProjectService

# ❌ INCORRECT: Domain → Infrastructure dependency
# from flext_quality.infrastructure.repositories import PostgreSQLRepository

# ✅ CORRECT: Use dependency injection for infrastructure
class QualityProjectService:
    def __init__(self, repository: QualityProjectRepository):
        self._repository = repository  # Injected dependency
```

### Error Handling Pattern

Always use FlextResult for error handling:

```python
# ✅ CORRECT: FlextResult pattern
async def analyze_project(project_id: str) -> FlextResult[QualityAnalysis]:
    try:
        project = await self._get_project(project_id)
        if not project.success:
            return project  # Propagate error

        analysis = await self._run_analysis(project.data)
        return analysis
    except Exception as e:
        return FlextResult[None].fail(f"Analysis failed: {e}")

# ❌ INCORRECT: Throwing exceptions
async def analyze_project_bad(project_id: str) -> QualityAnalysis:
    project = await self._get_project(project_id)
    if not project:
        raise ProjectNotFound(project_id)  # Don't do this
```

### Testing Patterns

Follow comprehensive testing strategy:

```python
import pytest
from flext_quality.application.services import QualityProjectService
from flext_quality.domain.entities import QualityProject

class TestQualityProjectService:
    """Test application service following patterns."""

    @pytest.fixture
    def service(self):
        """Service fixture with mocked dependencies."""
        return QualityProjectService()

    @pytest.mark.unit
    async def test_create_project_success(self, service):
        """Test successful project creation."""
        result = await service.create_project(
            name="test-project",
            project_path="/path/to/project"
        )

        assert result.success
        assert isinstance(result.data, QualityProject)
        assert result.data.name == "test-project"

    @pytest.mark.unit
    async def test_create_project_validation_failure(self, service):
        """Test project creation with validation failure."""
        result = await service.create_project(
            name="test-project",
            project_path=""  # Invalid empty path
        )

        assert not result.success
        assert "path is required" in result.error.lower()
```

## Quality Standards

### Code Quality Gates

All code must pass these quality gates:

```bash
# Run all quality checks
make validate

# Individual checks
make lint          # Ruff with ALL rules enabled
make type-check    # MyPy strict mode
make test          # 90% coverage minimum
make security      # Bandit + pip-audit
```

### Quality Thresholds

```toml
[tool.flext-quality]
min_coverage = 90.0
max_complexity = 10
max_duplication = 5.0
min_security_score = 90.0
enabled_analyzers = ["ruff", "mypy", "bandit", "semgrep"]
```

### Code Style Standards

Following FLEXT ecosystem standards:

```python
# Type hints are mandatory
def process_analysis(project: QualityProject) -> FlextResult[QualityAnalysis]:
    pass

# Use descriptive variable names
analysis_result = await analyzer.analyze_project(quality_project)

# Follow naming conventions
class QualityProjectService:  # PascalCase for classes
    def create_project(self):  # snake_case for methods
        pass

# Use proper docstrings
def calculate_quality_score(metrics: QualityMetrics) -> float:
    """Calculate composite quality score from analysis metrics.

    Args:
        metrics: Quality metrics from analysis

    Returns:
        Quality score between 0.0 and 100.0

    Raises:
        ValueError: If metrics are invalid
    """
    pass
```

## Development Workflows

### Feature Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/quality-dashboard-improvements

# 2. Make changes following patterns
# - Update domain entities if needed
# - Implement application services
# - Add infrastructure adapters
# - Update presentation layer

# 3. Run quality gates
make validate

# 4. Run tests
make test

# 5. Update documentation
# - Update relevant docs/ files
# - Update CLAUDE.md if needed

# 6. Commit and push
git add .
git commit -m "feat: improve quality dashboard with new metrics"
git push origin feature/quality-dashboard-improvements

# 7. Create pull request
gh pr create --title "Improve quality dashboard with new metrics"
```

### Bug Fix Workflow

```bash
# 1. Create bug fix branch
git checkout -b fix/analysis-memory-leak

# 2. Write failing test first
pytest tests/test_analyzer.py::test_memory_usage -v

# 3. Fix the issue
# - Identify root cause
# - Implement fix
# - Verify fix with test

# 4. Run quality gates
make validate

# 5. Commit fix
git commit -m "fix: resolve memory leak in analysis engine"
```

### Refactoring Workflow

```bash
# 1. Identify refactoring need
# - Check docs/TODO.md for architectural issues
# - Look for code smells and violations

# 2. Plan refactoring
# - Design new structure
# - Plan migration strategy
# - Consider backward compatibility

# 3. Implement incrementally
# - Small, focused changes
# - Maintain tests passing
# - Update documentation

# 4. Validate improvement
make validate
make test
```

## Debugging and Troubleshooting

### Local Debugging Setup

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

### Docker Debugging

```bash
# Debug Django service
docker-compose exec web python manage.py shell

# Debug Celery worker
docker-compose exec celery celery -A code_analyzer_web inspect active

# Check service logs
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db
```

### Common Issues and Solutions

**Issue: Database connection errors**

```bash
# Check PostgreSQL status
docker-compose ps
docker-compose exec db pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up -d db
make web-migrate
```

**Issue: Celery tasks not executing**

```bash
# Check Redis connection
redis-cli ping

# Check Celery worker status
celery -A code_analyzer_web inspect active

# Restart Celery worker
docker-compose restart celery
```

**Issue: Import errors in tests**

```bash
# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use poetry
poetry run pytest
```

## Integration Development

### FLEXT Ecosystem Integration

When developing integrations with other FLEXT services:

```python
from flext_observability import flext_create_metric, flext_create_trace

# Create quality metrics for ecosystem monitoring
def publish_quality_metrics(analysis: QualityAnalysis):
    """Publish quality metrics to FLEXT observability."""
    flext_create_metric(
        name="quality_score",
        value=analysis.overall_score,
        tags={
            "project": analysis.project_id,
            "ecosystem": "flext"
        }
    )

# Create traces for analysis operations
@flext_create_trace("quality_analysis")
async def analyze_project_with_tracing(project: QualityProject):
    """Analyze project with distributed tracing."""
    # Implementation with automatic tracing
    pass
```

### API Development

When developing API endpoints:

```python
from fastapi import APIRouter, Depends
from flext_quality.application.services import QualityProjectService

router = APIRouter(prefix="/api/v1/quality")

@router.post("/projects/{project_id}/analyze")
async def analyze_project(
    project_id: str,
    service: QualityProjectService = Depends()
) -> dict:
    """Analyze project quality following API patterns."""
    result = await service.analyze_project(project_id)

    if result.success:
        return {"status": "success", "data": result.data.dict()}
    else:
        return {"status": "error", "message": result.error}
```

## Performance Development

### Optimization Guidelines

```python
# Use async/await for I/O operations
async def analyze_large_project(project: QualityProject) -> FlextResult[QualityAnalysis]:
    """Analyze large project with async processing."""
    tasks = []
    for file_path in project.get_source_files():
        task = asyncio.create_task(analyze_file_async(file_path))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return combine_analysis_results(results)

# Use caching for expensive operations
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_complexity_score(file_content: str) -> float:
    """Calculate complexity with caching."""
    # Expensive computation cached
    return complex_analysis(file_content)
```

### Memory Management

```python
# Use generators for large datasets
def analyze_files_generator(file_paths: List[Path]):
    """Analyze files using generator to manage memory."""
    for file_path in file_paths:
        yield analyze_single_file(file_path)

# Process in batches
def analyze_large_codebase(project: QualityProject) -> QualityAnalysis:
    """Analyze large codebase in manageable batches."""
    batch_size = 100
    files = list(project.get_source_files())

    for batch_start in range(0, len(files), batch_size):
        batch = files[batch_start:batch_start + batch_size]
        process_file_batch(batch)
```

## Next Steps

- **[Coding Standards](coding-standards.md)** - Detailed coding standards and patterns
- **[Testing Strategy](testing.md)** - Comprehensive testing approach
- **[Contributing Guide](contributing.md)** - How to contribute to FLEXT Quality
- **[Architecture Guide](../architecture/README.md)** - System architecture details
