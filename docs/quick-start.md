# FLEXT Quality Quick Start Guide

**Version**: 0.9.9 RC | **Status**: Accessibility Improvements Needed · 1.0.0 Release Preparation | **Updated**: 2025-09-17

---

## Current Status Notice

**FLEXT Quality** has solid domain architecture with critical accessibility barriers requiring resolution.

### **Implementation Status:**

- ✅ **Domain Architecture** - Complete entity design with FlextResult patterns
- ✅ **Service Layer** - Functional async services with proper error handling
- ⚠️ **Core Analyzer** - FlextQualityCodeAnalyzer functional but not exported
- ❌ **Quality Gates** - 2 MyPy type errors, test execution blocked by imports
- ⚠️ **Modern Integration** - Limited 2025 Python quality ecosystem integration

**For developers**: See [TODO.md](../TODO.md) for accurate technical assessment and priorities.

---

## Prerequisites

- **Python 3.13+** with type annotation support
- **FLEXT ecosystem** dependencies (flext-core, flext-cli, etc.)
- **Modern quality tools**: Ruff, MyPy, Bandit (managed via project)
- **Poetry** for dependency management

## Current Setup (Development/Transformation)

### **Step 1: Clone and Install**

```bash
# Clone the repository
git clone <repository-url>
cd flext-quality

# Install dependencies
poetry install

# Activate environment
poetry shell
```

### **Step 2: Verify Current State**

```bash
# Check type errors (expect 45 errors currently)
mypy src/flext_quality/ --strict

# Check test status (expect import failures currently)
pytest tests/ -v

# Check available commands (limited functionality)
python -m flext_quality --help
```

### **Step 3: Review Architecture**

```bash
# Explore the excellent domain architecture
ls -la src/flext_quality/
# entities.py     - Core business entities ✅
# value_objects.py - Quality metrics and scores ✅
# services.py     - Domain services (needs consolidation)
# api.py          - API facade (90% not implemented)
# cli.py          - CLI interface (needs flext-cli conversion)
```

---

## Intended Usage (Post-Transformation)

### **Basic Quality Analysis** (WORKING)

```python
import asyncio
from flext_quality import FlextQualityService
from flext_quality.analyzer import FlextQualityCodeAnalyzer

# Option 1: Service Layer Approach
async def service_analysis():
    service = FlextQualityService()

    # Create project with quality thresholds
    project_result = await service.create_project(
        name="my_project",
        project_path="./src",
        _min_coverage=85.0,  # Note: internal parameter name
        _max_complexity=10
    )

    if project_result.success:
        project = project_result.value
        print(f"✅ Project: {project.name}")
        print(f"📁 Path: {project.project_path}")
        print(f"🎯 Min Coverage: {project.min_coverage}")

# Option 2: Direct Analysis Engine
def direct_analysis():
    # Analyze project directly
    analyzer = FlextQualityCodeAnalyzer("./src")

    # Run comprehensive analysis
    analysis_result = analyzer.analyze_project(
        include_security=True,
        include_complexity=True,
        include_dead_code=True,
        include_duplicates=True
    )

    # Get results
    score = analyzer.get_quality_score()
    grade = analyzer.get_quality_grade()

    print(f"📊 Quality Score: {score}")
    print(f"🏆 Quality Grade: {grade}")
    print(f"📄 Files Analyzed: {analysis_result.overall_metrics.files_analyzed}")
    print(f"📏 Total Lines: {analysis_result.overall_metrics.total_lines}")

# Run both approaches
asyncio.run(service_analysis())
direct_analysis()
```

### **CLI Usage** (PLANNED - Pure FLEXT-CLI)

```bash
# Comprehensive project analysis
flext-quality analyze --project ./src --format html --output quality-report.html

# Quality gate validation with thresholds
flext-quality validate --thresholds quality-config.toml

# Workspace-wide quality analysis (absorbing workspace scripts)
flext-quality workspace-analyze --parallel --security-scan

# Quality metrics collection
flext-quality metrics --project ./src --export json

# Code fixing automation (absorbing gradual_lint_fixer.py)
flext-quality fix --project ./src --auto-approve --backup
```

### **Enterprise Dashboard** (PLANNED - FLEXT-WEB)

```python
from flext_quality import FlextQualityWeb

# Create enterprise quality dashboard
quality_web = FlextQualityWeb()
dashboard = await quality_web.create_enterprise_dashboard()

# Dashboard features (planned):
# - Real-time quality metrics overview
# - Project health trends and analytics
# - Issue management and resolution tracking
# - Executive reporting with quality KPIs
# - Team collaboration and code review integration
```

### **Integration with FLEXT Ecosystem** (PLANNED)

```python
# FLEXT-API integration for programmatic access
from flext_api import FlextApiRouter
from flext_quality import FlextQualityApiRouter

api_router = FlextApiRouter()
api_router.include_router(FlextQualityApiRouter())

# FLEXT-AUTH integration for enterprise security
from flext_auth import FlextAuthMiddleware
from flext_quality import FlextQualityAuthenticatedService

quality_service = FlextQualityAuthenticatedService(
    auth_middleware=FlextAuthMiddleware()
)
```

---

## Enterprise Features (Post-Transformation)

### **Workspace Integration** (Research-Based 2025 Patterns)

FLEXT Quality will absorb and modernize all workspace quality functionality:

```python
# Absorbing workspace scripts into unified architecture:
WORKSPACE_INTEGRATION = {
    "quality_gateway.py": "FlextQualityGateway - Enterprise quality gates",
    "complete_quality_analysis.py": "FlextQualityAnalyzer - Multi-tool analysis",
    "gradual_lint_fixer.py": "FlextQualityFixer - Automated code remediation",
    "mypy_analyzer.py": "Type analysis integration with dual MyPy/PyRight",
    "pattern_audit_system.py": "FlextQualityValidator - Pattern detection",
    "flext_tools/quality_*": "Core quality bridge and gateway integration"
}
```

### **Modern Tool Stack** (Research-Based)

```python
# 2025 Enterprise Quality Stack Integration
ENTERPRISE_TOOLS = {
    "ruff": {
        "description": "Rust-based linting, 3453+ patterns, extremely fast",
        "features": "TOML config, hierarchical overrides, pre-commit integration"
    },
    "mypy": {
        "description": "Industry standard type checking with plugin system",
        "features": "Strict mode, incremental cache, enterprise reporting"
    },
    "bandit": {
        "description": "Security vulnerability scanning",
        "features": "CVE detection, custom rules, CI/CD integration"
    },
    "coverage.py": {
        "description": "Test coverage measurement and reporting",
        "features": "Branch coverage, HTML/XML reports, threshold enforcement"
    }
}
```

### **Configuration Management** (Modern Standards)

```toml
# quality-config.toml (PLANNED)
[tool.flext_quality]
project_name = "my-enterprise-project"
python_version = "3.13"

[tool.flext_quality.analysis]
min_coverage = 90.0
max_complexity = 10
security_level = "enterprise"
enable_parallel = true

[tool.flext_quality.tools.ruff]
extend = "enterprise-python.toml"
line_length = 88
target_version = "py313"

[tool.flext_quality.tools.mypy]
strict = true
disallow_untyped_defs = true
warn_return_any = true

[tool.flext_quality.reporting]
formats = ["html", "json", "pdf"]
include_executive_summary = true
include_trend_analysis = true
```

---

## Development Status & Roadmap

### **Phase 1: Critical Fixes (Week 1)**

- 🔥 Fix 45 MyPy type errors for production readiness
- 🔥 Restore test infrastructure (0% → 85% coverage target)
- 🔥 Complete API implementation (replace 90% placeholders)
- 🔥 Consolidate service architecture (unified class patterns)

### **Phase 2: Workspace Absorption (Week 2)**

- 📦 Absorb all `scripts/quality/*.py` functionality
- 📦 Integrate `flext_tools` quality components
- 🔧 Implement modern Python quality stack (Ruff, MyPy, etc.)

### **Phase 3: FLEXT Ecosystem Integration (Week 3)**

- 🖥️ Convert to pure FLEXT-CLI (remove argparse)
- 🌐 Implement FLEXT-WEB enterprise dashboard
- 🗄️ Add proper repository layer with database persistence
- 🔐 Integrate FLEXT-AUTH for enterprise security

### **Phase 4: Enterprise Features (Week 4)**

- 📊 Executive reporting and quality KPIs
- 🤝 Team collaboration and code review integration
- 📈 Quality trend analysis and predictive insights
- 🔄 CI/CD pipeline integration with quality gates

---

## Getting Involved in Transformation

### **For Developers**

1. Review [TODO.md](../TODO.md) for detailed transformation plan
2. Focus on Phase 1 critical fixes first
3. Follow FLEXT standards (unified classes, FlextResult patterns, etc.)
4. Contribute to fixing type errors and API implementations

### **For FLEXT Users**

1. Wait for transformation completion (2-3 weeks)
2. Prepare projects for integration with new quality platform
3. Review planned CLI and API interfaces
4. Provide feedback on enterprise requirements

### **For Enterprise Teams**

1. Plan integration with enterprise quality workflows
2. Review dashboard and reporting requirements
3. Prepare for migration from current quality tools
4. Consider pilot deployment after transformation

---

## Support During Transformation

- **Issues**: Report via GitHub Issues with "transformation" label
- **Questions**: Use GitHub Discussions for transformation-related questions
- **Updates**: Watch repository for transformation progress updates
- **Contributing**: See transformation roadmap in TODO.md for contribution opportunities

---

**NOTE**: This quick start guide describes the intended functionality. Current implementation has significant gaps requiring the transformation outlined in [TODO.md](../TODO.md). The excellent architectural foundations suggest 2-3 weeks focused development will achieve full functionality.

**VISION**: FLEXT Quality will become the premier enterprise code quality platform, absorbing workspace functionality and providing unified interfaces to Python's best quality tools while maintaining zero-tolerance quality enforcement.
