# flext-quality

**Type**: Application Service | **Status**: Active Development | **Dependencies**: flext-core

Code quality analysis and governance library for the FLEXT ecosystem.

> ⚠️ Development Status: Quality analysis engine functional; ecosystem integration in progress.

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_quality.domain.entities import QualityProject; project = QualityProject(name='test', path='.'); print('✅ Working')"

# Development setup
make setup
```

## Current Reality

**What Actually Works:**

- Quality analysis engine with multi-backend analyzers (AST, Ruff, MyPy, Bandit)
- Domain entities (QualityProject, QualityAnalysis, QualityIssue)
- Quality scoring and metrics calculation
- Report generation (HTML, JSON, PDF)

**What Needs Work:**

- Ecosystem-aware analysis (32-project structure understanding)
- Integration with flext-observability metrics
- CLI integration with flext-cli

## Architecture Role in FLEXT Ecosystem

### **Application Service Component**

FLEXT Quality provides code quality governance across the ecosystem:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | [FLEXT-QUALITY] | Observ │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | Plugin | WMS      │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Quality Governance**: Automated quality gates and standards enforcement
2. **Technical Debt Detection**: Proactive identification of maintainability issues
3. **Ecosystem Metrics**: Unified quality dashboards and reports

## Key Features

### **Current Capabilities**

- **Multi-Backend Analysis**: Pluggable analyzers (AST, Ruff, MyPy, Bandit, Semgrep)
- **Quality Scoring**: Composite quality scores with weighted metrics
- **Issue Detection**: Comprehensive quality issue identification and classification
- **Report Generation**: Multiple format reports (HTML, JSON, PDF)

### **FLEXT Core Integration**

- **FlextResult Pattern**: Type-safe error handling for all operations
- **FlextEntity**: Domain entities with business logic validation
- **Clean Architecture**: Domain/application/infrastructure separation

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-quality
poetry install

# Development setup
make setup
make web-migrate
```

### Basic Usage

```python
from flext_quality.domain.entities import QualityProject, QualityAnalysis
from flext_quality.application.services import QualityProjectService

# Create quality project
project = QualityProject(
    name="my-project",
    path="/path/to/project",
    language="python"
)

# Run analysis
service = QualityProjectService()
analysis_result = await service.create_analysis(project.id)
if analysis_result.success:
    analysis = analysis_result.data
    print(f"Overall score: {analysis.overall_score}")
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation (lint + type + security + test + quality-check)
make check                 # Quick lint + type check + test
make test                  # Run all tests (90% coverage requirement)
make lint                  # Code linting
make type-check            # Type checking
make security              # Security scanning
make format                # Code formatting
```

### Quality Analysis

```bash
# Analysis operations
make analyze               # Run comprehensive quality analysis
make workspace-analyze     # Analyze entire FLEXT workspace
make quality-check         # Check quality thresholds
make report                # Generate quality reports
```

### Django Web Interface

```bash
# Web development
make web-start             # Start Django web interface (port 8000)
make web-migrate           # Run Django migrations
make web-shell             # Open Django shell

# Full system with Docker
docker-compose up -d       # Start all services (web, db, redis, celery)
```

## Configuration

### Environment Variables

```bash
# Database configuration
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dc_analyzer

# Quality thresholds
export QUALITY_MIN_COVERAGE=90.0
export QUALITY_MAX_COMPLEXITY=10
export QUALITY_MIN_SECURITY_SCORE=90.0
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 90% target
- **Type Safety**: MyPy strict mode adoption
- **Linting**: Ruff with comprehensive rules
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
async def create_analysis(self, project_id: str) -> FlextResult[QualityAnalysis]:
    try:
        analysis = QualityAnalysis(project_id=project_id)
        return FlextResult.ok(analysis)
    except Exception as e:
        return FlextResult.fail(f"Analysis creation failed: {e}")
```

### **Service Integration**

- **flext-observability**: Quality metrics collection and monitoring
- **flext-web**: Dashboard integration for quality reports
- **flext-cli**: Quality analysis commands

## Current Status

**Version**: 0.9.0 (Development)

**Completed**:

- ✅ Multi-backend analysis engine
- ✅ Domain entities and quality scoring
- ✅ Report generation system

**In Progress**:

- 🔄 Django web interface integration with FLEXT patterns
- 🔄 Ecosystem-aware analysis (32-project structure)
- 🔄 Integration with flext-observability

**Planned**:

- 📋 flext-cli integration
- 📋 Real-time quality monitoring
- 📋 Executive quality dashboards

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain 90% coverage
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---

_Part of the FLEXT ecosystem - Enterprise data integration platform_
