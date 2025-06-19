# 🔍 DC Code Analyzer - Enterprise Python Code Analysis Platform

> **Function**: Advanced Django-based code analysis platform for quality assessment, complexity analysis, and codebase insights | **Audience**: Development Teams, DevOps Engineers, Quality Assurance | **Status**: Beta

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Beta](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/codeanalyzer/dc_code_analyzer)

## 📋 **Overview**

Enterprise-grade Python code analysis platform that provides comprehensive static analysis, quality assessment, complexity measurement, and automated reporting capabilities through a modern Django web interface.

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../README.md) → **📂 Current**: DC Code Analyzer

---

## 🎯 **Core Purpose**

DC Code Analyzer delivers enterprise-level static code analysis for Python projects, combining multiple analysis backends (AST, external tools, quality metrics) into a unified platform. It provides automated code quality assessment, complexity analysis, security scanning, and comprehensive reporting capabilities.

### **Key Capabilities**

- **Multi-Backend Analysis**: AST parsing, external tool integration, quality metrics
- **Security Scanning**: Bandit integration for security vulnerability detection
- **Complexity Analysis**: Radon integration for cyclomatic complexity measurement
- **Dead Code Detection**: Vulture integration for unused code identification
- **Quality Metrics**: Comprehensive code quality scoring and trend analysis

### **Production Features**

- **Web Dashboard**: Modern Django-based interface with interactive reports
- **REST API**: Complete RESTful API for programmatic access
- **Batch Processing**: Celery-based asynchronous analysis processing
- **Report Generation**: PDF, HTML, and JSON report formats
- **Project Management**: Multi-project workspace with version tracking

---

## 🚀 **Quick Start**

### **Installation**

```bash
# Install via Poetry (recommended)
cd dc-code-analyzer
poetry install

# Install with optional dependencies
poetry install --extras "ai viz perf"

# Install from PyAuto workspace
cd /path/to/pyauto
poetry install --extras "analyzer"
```

### **Basic Configuration**

```bash
# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Database setup
python manage.py migrate
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

### **Running the Platform**

```bash
# Development server
python manage.py runserver

# Production deployment
./start_all.sh

# Background workers
./start_celery.sh

# Redis cache
./start_redis.sh
```

---

## 🏗️ **Architecture**

### **Django Application Structure**

```
┌─────────────────────────────────────────┐
│          Web Interface Layer           │
│      (Django Admin + Dashboard)        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         REST API Layer                  │
│    (Django REST Framework)             │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Analysis Engine                  │
│    (Multi-Backend Analyzer)            │
├─────────────────────────────────────────┤
│ • AST Backend                          │
│ • External Tools Backend               │
│ • Quality Metrics Backend              │
│ • Security Analysis Backend            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Task Queue & Workers              │
│         (Celery + Redis)                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Database & Storage               │
│    (PostgreSQL + File Storage)         │
└─────────────────────────────────────────┘
```

### **Component Structure**

```
dc-code-analyzer/
├── analyzer/                   # Core analysis engine
│   ├── backends/              # Analysis backends
│   │   ├── ast_backend.py     # AST parsing and analysis
│   │   ├── external_backend.py # External tool integration
│   │   ├── quality_backend.py  # Quality metrics calculation
│   │   └── base.py            # Base backend interface
│   ├── analysis_engine.py     # Main analysis orchestrator
│   ├── multi_backend_analyzer.py # Multi-backend coordinator
│   ├── report_generator.py    # Report generation engine
│   └── cli.py                 # Command-line interface
├── dashboard/                  # Web dashboard
│   ├── views.py               # Dashboard views
│   ├── charts.py              # Visualization components
│   └── templatetags/          # Custom template tags
├── code_analyzer_web/         # Django project settings
├── templates/                 # HTML templates
├── staticfiles/              # Static assets
└── tests/                    # Comprehensive test suite
```

---

## 🔧 **Core Features**

### **1. Analysis Backends**

#### **AST Backend**

```python
from analyzer.backends.ast_backend import ASTBackend

backend = ASTBackend()
results = backend.analyze_file("path/to/file.py")
print(f"Functions: {results['functions_count']}")
print(f"Classes: {results['classes_count']}")
print(f"Complexity: {results['complexity_score']}")
```

#### **External Tools Integration**

```python
from analyzer.backends.external_backend import ExternalBackend

backend = ExternalBackend()
# Integrates: bandit, vulture, radon, mypy, flake8
results = backend.run_analysis("project_path")
```

#### **Quality Metrics**

```python
from analyzer.backends.quality_backend import QualityBackend

backend = QualityBackend()
metrics = backend.calculate_metrics("project_path")
print(f"Quality Score: {metrics['overall_score']}")
```

### **2. Web Dashboard**

Access comprehensive analysis reports through the web interface:

- **Project Overview**: High-level metrics and trends
- **Detailed Reports**: File-by-file analysis results
- **Security Issues**: Vulnerability reports with remediation
- **Complexity Analysis**: Hotspot identification and recommendations
- **Quality Trends**: Historical quality tracking

### **3. REST API**

```python
import requests

# Create analysis session
response = requests.post('/api/analysis/', {
    'project_name': 'my-project',
    'source_path': '/path/to/code'
})

# Get results
session_id = response.json()['session_id']
results = requests.get(f'/api/analysis/{session_id}/')
```

### **4. CLI Interface**

```bash
# Analyze single file
dc-analyzer analyze --file path/to/file.py

# Analyze project
dc-analyzer analyze --project /path/to/project

# Generate report
dc-analyzer report --session-id 123 --format pdf

# List available backends
dc-analyzer backends --list
```

### **5. Batch Processing**

```bash
# Start Celery workers
celery -A code_analyzer_web worker --loglevel=info

# Schedule batch analysis
dc-analyzer batch --projects-file projects.json

# Monitor task status
celery -A code_analyzer_web flower
```

---

## 📊 **Analysis Capabilities**

### **Code Quality Metrics**

- **Maintainability Index**: Overall code maintainability score
- **Cyclomatic Complexity**: Function and class complexity analysis
- **Lines of Code**: Physical and logical line counting
- **Code Duplication**: Duplicate code block detection
- **Documentation Coverage**: Docstring and comment analysis

### **Security Analysis**

- **Vulnerability Detection**: Common security patterns
- **Dependency Scanning**: Known vulnerable dependencies
- **Code Injection Risks**: SQL injection, XSS, command injection
- **Cryptographic Issues**: Weak crypto implementations
- **File System Risks**: Path traversal, file permissions

### **Performance Analysis**

- **Algorithmic Complexity**: Big-O analysis
- **Memory Usage Patterns**: Memory leak detection
- **Database Query Analysis**: N+1 queries, inefficient patterns
- **Import Analysis**: Circular imports, unused imports
- **Resource Usage**: File handles, network connections

### **Documentation Quality**

- **Docstring Coverage**: Function and class documentation
- **Comment Quality**: Inline comment analysis
- **API Documentation**: Public interface documentation
- **README Assessment**: Project documentation quality
- **Type Hints**: Type annotation coverage

---

## 🔐 **Security & Compliance**

### **Security Features**

- **HTTPS Only**: Secure communication in production
- **Authentication**: Django built-in authentication system
- **Authorization**: Role-based access control
- **CSRF Protection**: Cross-site request forgery protection
- **SQL Injection Protection**: Django ORM protection

### **Compliance Support**

- **GDPR**: Data privacy and user consent
- **SOC 2**: Security and availability controls
- **ISO 27001**: Information security management
- **PCI DSS**: Payment card industry standards
- **HIPAA**: Healthcare data protection

---

## 🧪 **Testing**

### **Test Coverage**

- Unit Tests: 85%+ coverage requirement
- Integration Tests: Cross-component testing
- End-to-End Tests: Full workflow validation
- API Tests: REST endpoint validation

### **Running Tests**

```bash
# Unit tests
pytest tests/unit

# Integration tests
pytest tests/integration

# E2E tests
pytest tests/e2e

# All tests with coverage
pytest --cov=analyzer --cov-report=html
```

---

## 📚 **Usage Examples**

### **Basic Project Analysis**

```python
# examples/basic_analysis.py
from analyzer.analysis_engine import AnalysisEngine

engine = AnalysisEngine()
results = engine.analyze_project("/path/to/project")

print(f"Total Files: {results.total_files}")
print(f"Quality Score: {results.quality_score}")
print(f"Security Issues: {len(results.security_issues)}")
```

### **Custom Backend Integration**

```python
# examples/custom_backend.py
from analyzer.backends.base import BaseBackend

class CustomBackend(BaseBackend):
    def analyze_file(self, file_path):
        # Custom analysis logic
        return {
            'custom_metric': self.calculate_custom_metric(file_path)
        }

# Register custom backend
engine.register_backend('custom', CustomBackend())
```

### **Report Generation**

```python
# examples/report_generation.py
from analyzer.report_generator import ReportGenerator

generator = ReportGenerator()
report = generator.generate_report(
    session_id=123,
    format='pdf',
    template='comprehensive'
)
```

---

## 🔗 **Integration Ecosystem**

### **PyAuto Integration**

| Component                            | Integration       | Purpose            |
| ------------------------------------ | ----------------- | ------------------ |
| [FLX Core](../flx/)                  | Analysis plugins  | Code quality gates |
| [DC Scripts](../scripts/)            | Automation tools  | Batch analysis     |
| [Quality Tools](../scripts/quality/) | CI/CD integration | Automated checks   |

### **External Tools**

| Tool    | Purpose             | Integration      |
| ------- | ------------------- | ---------------- |
| Bandit  | Security analysis   | Security backend |
| Vulture | Dead code detection | Quality backend  |
| Radon   | Complexity analysis | Metrics backend  |
| MyPy    | Type checking       | External backend |
| Flake8  | Style checking      | External backend |

### **CI/CD Integration**

```yaml
# .github/workflows/code-analysis.yml
- name: Code Analysis
  run: |
    dc-analyzer analyze --project . --format json > analysis.json
    dc-analyzer quality-gate --threshold 8.0 analysis.json
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Analysis Timeouts**

   - **Symptom**: Long-running analysis sessions
   - **Solution**: Increase Celery task timeout, optimize backend configurations

2. **Database Connection Errors**

   - **Symptom**: Django database errors
   - **Solution**: Check PostgreSQL connection, verify credentials

3. **Static Files Not Loading**
   - **Symptom**: Missing CSS/JS in dashboard
   - **Solution**: Run `python manage.py collectstatic`

### **Debug Mode**

```bash
# Enable debug logging
export DJANGO_DEBUG=True
export DJANGO_LOG_LEVEL=DEBUG

# Start with verbose output
python manage.py runserver --verbosity=2
```

---

## 🛠️ **CLI Reference**

```bash
# Project analysis
dc-analyzer analyze --project /path/to/code --output report.json

# File analysis
dc-analyzer analyze --file script.py --backends ast,quality

# Report generation
dc-analyzer report --session-id 123 --format pdf --output report.pdf

# Backend management
dc-analyzer backends --list
dc-analyzer backends --configure bandit --config bandit.yaml

# Project management
dc-analyzer projects --create "New Project"
dc-analyzer projects --list
```

---

## 📖 **API Reference**

### **Core Endpoints**

- `POST /api/analysis/` - Create analysis session
- `GET /api/analysis/{id}/` - Get analysis results
- `GET /api/projects/` - List projects
- `POST /api/reports/` - Generate report
- `GET /api/backends/` - List available backends

### **WebSocket API**

```javascript
// Real-time analysis updates
const ws = new WebSocket("ws://localhost:8000/ws/analysis/123/");
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log("Analysis progress:", data.progress);
};
```

---

## 🔗 **Cross-References**

### **Prerequisites**

- [Django Documentation](https://docs.djangoproject.com/) - Django framework reference
- [Django REST Framework](https://www.django-rest-framework.org/) - API framework
- [Celery Documentation](https://docs.celeryproject.org/) - Task queue system

### **Next Steps**

- [Analysis Guide](./docs/analysis-guide.md) - Comprehensive analysis setup
- [API Integration](./docs/api-integration.md) - REST API usage
- [Custom Backends](./docs/custom-backends.md) - Backend development

### **Related Topics**

- [Code Quality Patterns](../docs/patterns/quality.md) - Quality assurance patterns
- [CI/CD Integration](../docs/patterns/cicd.md) - Continuous integration
- [Security Analysis](../docs/patterns/security.md) - Security assessment

---

**📂 Component**: DC Code Analyzer | **🏠 Root**: [PyAuto Home](../README.md) | **Framework**: Django 4.2+ | **Updated**: 2025-06-19
