# FLEXT Quality Quick Start Guide

Get up and running with FLEXT Quality in minutes. This guide covers installation, basic configuration, and your first quality analysis.

## Prerequisites

- **Python 3.13+** installed on your system
- **Poetry** for Python dependency management
- **Docker & Docker Compose** (optional, for full service stack)
- **Git** for version control

## Installation Options

### Option 1: Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality

# Complete setup with one command
make setup

# Start all services
./start_all.sh
```

### Option 2: Docker Setup

```bash
# Clone and start with Docker
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality

# Start all services with Docker
docker-compose up -d

# Check service status
docker-compose ps
```

### Option 3: Manual Setup

```bash
# Clone repository
git clone https://github.com/flext-sh/flext-quality.git
cd flext-quality

# Install dependencies
poetry install --with dev,test

# Setup database
make web-migrate

# Start web server
make web-start
```

## Verify Installation

Check that all services are running:

```bash
# Check web interface
curl http://localhost:8000/health

# Check API
curl http://localhost:8000/api/v1/health

# Check database connection
make diagnose
```

Expected output:

```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "redis": "connected",
    "celery": "running"
  },
  "version": "0.9.0"
}
```

## Your First Quality Analysis

### 1. Access the Web Dashboard

Open your browser and navigate to:

```
http://localhost:8000
```

You should see the FLEXT Quality dashboard.

### 2. Create Your First Project

Using the web interface:

1. Click "New Project"
2. Fill in project details:
   - **Name**: `my-first-project`
   - **Path**: `/path/to/your/python/project`
   - **Repository URL**: (optional) `https://github.com/user/repo`

Or use the command line:

```bash
# Create project via CLI
make create-project NAME=my-first-project PATH=/path/to/project
```

### 3. Run Quality Analysis

Via web interface:

1. Go to your project page
2. Click "Start Analysis"
3. Wait for analysis to complete (usually 2-5 minutes)

Via command line:

```bash
# Analyze project
make analyze PROJECT=my-first-project

# Or analyze any directory
make analyze-path PATH=/path/to/project
```

### 4. View Results

The analysis will provide:

- **Quality Score** (0-100)
- **Quality Grade** (A+ to F)
- **Issue Breakdown** by severity
- **Detailed Report** with recommendations

## Example: Analyzing FLEXT Core

Let's analyze the FLEXT core library as an example:

```bash
# If you have access to flext-core
git clone https://github.com/flext-sh/flext-core.git /tmp/flext-core

# Create project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "flext-core-example",
    "project_path": "/tmp/flext-core",
    "repository_url": "https://github.com/flext-sh/flext-core",
    "language": "python"
  }'

# Start analysis (replace PROJECT_ID with actual ID from previous response)
curl -X POST http://localhost:8000/api/v1/projects/PROJECT_ID/analyze

# Check results
curl http://localhost:8000/api/v1/projects/PROJECT_ID
```

Expected quality metrics for a well-maintained project:

```json
{
  "quality_score": 92.5,
  "quality_grade": "A",
  "metrics": {
    "coverage_percentage": 94.2,
    "complexity_score": 8.1,
    "security_score": 98.5,
    "maintainability_score": 89.3
  },
  "issue_counts": {
    "critical": 0,
    "high": 2,
    "medium": 8,
    "low": 15
  }
}
```

## Understanding Quality Scores

### Quality Grade Scale

- **A+ (95-100)**: Exceptional quality, minimal issues
- **A (90-94)**: High quality, few minor issues
- **A- (85-89)**: Good quality, some improvements needed
- **B+ (80-84)**: Acceptable quality, moderate issues
- **B (75-79)**: Below standard, significant issues
- **C (60-74)**: Poor quality, major refactoring needed
- **D (40-59)**: Very poor quality, extensive work required
- **F (0-39)**: Failing quality, complete overhaul needed

### Key Metrics Explained

- **Coverage Score**: Percentage of code covered by tests
- **Complexity Score**: Average cyclomatic complexity (lower is better)
- **Security Score**: Security vulnerability assessment
- **Maintainability Score**: Code maintainability assessment

## Common Configuration

### Environment Variables

Create a `.env` file for local development:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/flext_quality

# Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Quality thresholds
QUALITY_MIN_COVERAGE=90.0
QUALITY_MAX_COMPLEXITY=10
QUALITY_MIN_SECURITY_SCORE=90.0

# FLEXT integration
FLEXT_OBSERVABILITY_ENABLED=true
```

### Quality Standards

Customize quality standards in `pyproject.toml`:

```toml
[tool.flext-quality]
min_coverage = 90.0
max_complexity = 10
max_duplication = 5.0
enabled_analyzers = ["ruff", "mypy", "bandit", "semgrep"]
report_formats = ["html", "json", "executive"]

# Custom thresholds per project type
[tool.flext-quality.thresholds]
core_library = { min_coverage = 95.0, max_complexity = 8 }
application = { min_coverage = 85.0, max_complexity = 12 }
test_code = { min_coverage = 70.0, max_complexity = 15 }
```

## Basic API Usage

### Using Python SDK

```python
from flext_quality import FlextQualityClient

# Initialize client
client = FlextQualityClient(base_url="http://localhost:8000")

# Create project
project = await client.projects.create(
    name="api-example",
    project_path="/path/to/project"
)

# Start analysis
analysis = await client.analyses.start(project.id)

# Wait for completion
result = await client.analyses.wait_for_completion(analysis.id)

print(f"Quality Score: {result.quality_score}")
print(f"Grade: {result.quality_grade}")
```

### Using REST API

```bash
# Create project
PROJECT_ID=$(curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "rest-example", "project_path": "/path/to/project"}' \
  | jq -r '.data.id')

# Start analysis
ANALYSIS_ID=$(curl -X POST http://localhost:8000/api/v1/projects/$PROJECT_ID/analyze \
  | jq -r '.data.analysis_id')

# Check status
curl http://localhost:8000/api/v1/analyses/$ANALYSIS_ID

# Get results when complete
curl http://localhost:8000/api/v1/analyses/$ANALYSIS_ID/results
```

## Troubleshooting

### Common Issues

**Service won't start:**

```bash
# Check port conflicts
sudo netstat -tulpn | grep -E "(8000|5432|6379)"

# Restart services
docker-compose restart
# or
./start_all.sh
```

**Database connection error:**

```bash
# Check PostgreSQL
docker-compose exec db pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up -d db
make web-migrate
```

**Analysis fails:**

```bash
# Check logs
docker-compose logs -f celery

# Verify project path exists
ls -la /path/to/your/project

# Check disk space
df -h
```

### Getting Help

- **Documentation**: [docs/README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext-quality/issues)
- **Troubleshooting**: [docs/operations/troubleshooting.md](operations/troubleshooting.md)

## Next Steps

Now that you have FLEXT Quality running:

1. **Explore the Web Interface** - Browse projects, analyses, and reports
2. **Integrate with CI/CD** - Set up quality gates in your development workflow
3. **Customize Rules** - Configure quality standards for your organization
4. **Set up Monitoring** - Connect to your observability stack
5. **Scale Deployment** - Move to production with Kubernetes or Docker Swarm

### Recommended Reading

- **[Development Guide](development/README.md)** - Set up development environment
- **[Architecture Overview](architecture/README.md)** - Understand system design
- **[API Documentation](api/README.md)** - Integrate with external systems
- **[Deployment Guide](deployment/README.md)** - Production deployment

### Integration Examples

- **[CI/CD Integration](integration/cicd.md)** - GitHub Actions, GitLab CI
- **[IDE Integration](integration/ide.md)** - VS Code, PyCharm
- **[Monitoring Setup](integration/monitoring.md)** - Prometheus, Grafana

Welcome to FLEXT Quality! 🚀
