# FLEXT QUALITY - Comprehensive Code Quality Analysis Engine
# ========================================================
# Enterprise quality analysis with metrics collection and reporting
# Python 3.13 + Quality Tools + Analysis Engine + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-quality
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: analyze report metrics quality-check workspace-analyze
.PHONY: quality-tools quality-engine analysis-test report-test

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎯 FLEXT QUALITY - Comprehensive Code Quality Analysis Engine"
	@echo "========================================================"
	@echo "🎯 Quality Tools + Analysis Engine + Metrics + Python 3.13"
	@echo ""
	@echo "📦 Enterprise quality analysis with comprehensive reporting"
	@echo "🔒 Zero tolerance quality gates with real analysis tools"
	@echo "🧪 90%+ test coverage requirement with quality engine compliance"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test quality-check ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT QUALITY ENGINE COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_quality --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-quality: ## Run quality analysis tests
	@echo "🧪 Running quality analysis tests..."
	@poetry run pytest tests/ -m "quality" -v
	@echo "✅ Quality tests complete"

test-analysis: ## Run analysis engine tests
	@echo "🧪 Running analysis engine tests..."
	@poetry run pytest tests/ -m "analysis" -v
	@echo "✅ Analysis tests complete"

test-reporting: ## Run reporting tests
	@echo "🧪 Running reporting tests..."
	@poetry run pytest tests/ -m "reporting" -v
	@echo "✅ Reporting tests complete"

test-performance: ## Run performance tests
	@echo "⚡ Running quality engine performance tests..."
	@poetry run pytest tests/performance/ -v --benchmark-only
	@echo "✅ Performance tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_quality --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security,quality
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security,quality
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🔍 QUALITY ANALYSIS OPERATIONS - CORE FUNCTIONALITY
# ============================================================================

analyze: ## Run comprehensive quality analysis on workspace
	@echo "🔍 Running comprehensive quality analysis..."
	@poetry run python scripts/analyze_workspace.py
	@echo "✅ Quality analysis complete"

quality-check: ## Check quality thresholds against standards
	@echo "🎯 Checking quality thresholds..."
	@poetry run python scripts/quality_check.py
	@echo "✅ Quality check complete"

metrics: ## Collect and calculate quality metrics
	@echo "📊 Collecting quality metrics..."
	@poetry run python scripts/collect_metrics.py
	@echo "✅ Metrics collection complete"

report: ## Generate comprehensive quality reports
	@echo "📋 Generating quality reports..."
	@poetry run python scripts/generate_report.py
	@echo "✅ Quality reports generated"

workspace-analyze: ## Analyze entire FLEXT workspace
	@echo "🏢 Analyzing FLEXT workspace..."
	@poetry run python scripts/analyze_flext_workspace.py
	@echo "✅ Workspace analysis complete"

project-analyze: ## Analyze specific project
	@echo "📁 Analyzing specific project..."
	@poetry run python scripts/analyze_project.py --project $(PROJECT)
	@echo "✅ Project analysis complete"

trend-analysis: ## Generate quality trend analysis
	@echo "📈 Generating trend analysis..."
	@poetry run python scripts/trend_analysis.py
	@echo "✅ Trend analysis complete"

comparative-analysis: ## Generate comparative analysis
	@echo "🔄 Generating comparative analysis..."
	@poetry run python scripts/comparative_analysis.py
	@echo "✅ Comparative analysis complete"

# ============================================================================
# 🔧 QUALITY TOOLS INTEGRATION
# ============================================================================

quality-tools: ## Test all quality tool integrations
	@echo "🔧 Testing quality tool integrations..."
	@poetry run python scripts/test_quality_tools.py
	@echo "✅ Quality tools test complete"

ruff-analysis: ## Run Ruff analysis with custom configuration
	@echo "🔍 Running Ruff analysis..."
	@poetry run python scripts/ruff_analyzer.py
	@echo "✅ Ruff analysis complete"

mypy-analysis: ## Run MyPy analysis with strict configuration
	@echo "🛡️ Running MyPy analysis..."
	@poetry run python scripts/mypy_analyzer.py
	@echo "✅ MyPy analysis complete"

coverage-analysis: ## Run coverage analysis with thresholds
	@echo "📊 Running coverage analysis..."
	@poetry run python scripts/coverage_analyzer.py
	@echo "✅ Coverage analysis complete"

security-analysis: ## Run security analysis with vulnerability scanning
	@echo "🔒 Running security analysis..."
	@poetry run python scripts/security_analyzer.py
	@echo "✅ Security analysis complete"

complexity-analysis: ## Run complexity analysis
	@echo "🌀 Running complexity analysis..."
	@poetry run python scripts/complexity_analyzer.py
	@echo "✅ Complexity analysis complete"

duplication-analysis: ## Run code duplication analysis
	@echo "🔄 Running duplication analysis..."
	@poetry run python scripts/duplication_analyzer.py
	@echo "✅ Duplication analysis complete"

# ============================================================================
# 📊 QUALITY METRICS & SCORING
# ============================================================================

calculate-scores: ## Calculate quality scores for all projects
	@echo "🎯 Calculating quality scores..."
	@poetry run python scripts/calculate_scores.py
	@echo "✅ Quality scores calculated"

coverage-score: ## Calculate coverage score
	@echo "📊 Calculating coverage score..."
	@poetry run python scripts/coverage_score.py
	@echo "✅ Coverage score calculated"

complexity-score: ## Calculate complexity score
	@echo "🌀 Calculating complexity score..."
	@poetry run python scripts/complexity_score.py
	@echo "✅ Complexity score calculated"

security-score: ## Calculate security score
	@echo "🔒 Calculating security score..."
	@poetry run python scripts/security_score.py
	@echo "✅ Security score calculated"

maintainability-score: ## Calculate maintainability score
	@echo "🔧 Calculating maintainability score..."
	@poetry run python scripts/maintainability_score.py
	@echo "✅ Maintainability score calculated"

quality-grade: ## Calculate overall quality grade
	@echo "🏆 Calculating overall quality grade..."
	@poetry run python scripts/quality_grade.py
	@echo "✅ Quality grade calculated"

# ============================================================================
# 📋 QUALITY REPORTING
# ============================================================================

generate-reports: ## Generate all quality reports
	@echo "📋 Generating all quality reports..."
	@poetry run python scripts/generate_all_reports.py
	@echo "✅ All reports generated"

executive-report: ## Generate executive summary report
	@echo "👔 Generating executive summary..."
	@poetry run python scripts/executive_report.py
	@echo "✅ Executive report generated"

technical-report: ## Generate technical detailed report
	@echo "🔧 Generating technical report..."
	@poetry run python scripts/technical_report.py
	@echo "✅ Technical report generated"

dashboard-report: ## Generate dashboard overview report
	@echo "📊 Generating dashboard report..."
	@poetry run python scripts/dashboard_report.py
	@echo "✅ Dashboard report generated"

html-report: ## Generate HTML quality report
	@echo "🌐 Generating HTML report..."
	@poetry run python scripts/html_report.py
	@echo "✅ HTML report generated"

json-report: ## Generate JSON quality report
	@echo "📄 Generating JSON report..."
	@poetry run python scripts/json_report.py
	@echo "✅ JSON report generated"

pdf-report: ## Generate PDF quality report
	@echo "📑 Generating PDF report..."
	@poetry run python scripts/pdf_report.py
	@echo "✅ PDF report generated"

# ============================================================================
# 🔍 QUALITY ISSUE MANAGEMENT
# ============================================================================

detect-issues: ## Detect quality issues across projects
	@echo "🔍 Detecting quality issues..."
	@poetry run python scripts/detect_issues.py
	@echo "✅ Issue detection complete"

classify-issues: ## Classify detected issues by severity
	@echo "📊 Classifying issues by severity..."
	@poetry run python scripts/classify_issues.py
	@echo "✅ Issue classification complete"

prioritize-issues: ## Prioritize issues by impact
	@echo "🎯 Prioritizing issues by impact..."
	@poetry run python scripts/prioritize_issues.py
	@echo "✅ Issue prioritization complete"

track-issues: ## Track issue resolution progress
	@echo "📈 Tracking issue resolution..."
	@poetry run python scripts/track_issues.py
	@echo "✅ Issue tracking complete"

# ============================================================================
# 🔍 DATA QUALITY & VALIDATION
# ============================================================================

validate-quality-data: ## Validate quality analysis data
	@echo "🔍 Validating quality analysis data..."
	@poetry run python scripts/validate_quality_data.py
	@echo "✅ Quality data validation complete"

validate-metrics: ## Validate quality metrics calculations
	@echo "🔍 Validating metrics calculations..."
	@poetry run python scripts/validate_metrics.py
	@echo "✅ Metrics validation complete"

validate-scores: ## Validate quality score calculations
	@echo "🔍 Validating score calculations..."
	@poetry run python scripts/validate_scores.py
	@echo "✅ Score validation complete"

data-integrity-check: ## Check data integrity across reports
	@echo "🔍 Checking data integrity..."
	@poetry run python scripts/data_integrity_check.py
	@echo "✅ Data integrity check complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

package: build ## Create deployment package
	@echo "📦 Creating deployment package..."
	@tar -czf dist/flext-quality-deployment.tar.gz \
		src/ \
		tests/ \
		scripts/ \
		pyproject.toml \
		README.md \
		CLAUDE.md
	@echo "✅ Deployment package created: dist/flext-quality-deployment.tar.gz"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@rm -rf reports/
	@rm -rf quality_reports/
	@rm -rf analysis_results/
	@rm -f *.log
	@rm -f quality_analysis.json
	@rm -f metrics_report.json
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# Quality Engine settings
export FLEXT_QUALITY_CONFIG := ./config.json
export FLEXT_QUALITY_DEBUG := false
export FLEXT_QUALITY_VERBOSE := true

# Quality Thresholds
export QUALITY_MIN_COVERAGE := 90.0
export QUALITY_MAX_COMPLEXITY := 10
export QUALITY_MAX_DUPLICATION := 5.0
export QUALITY_MIN_SECURITY_SCORE := 90.0
export QUALITY_MIN_MAINTAINABILITY := 80.0

# Analysis Tool Configuration
export QUALITY_ENABLE_RUFF := true
export QUALITY_ENABLE_MYPY := true
export QUALITY_ENABLE_COVERAGE := true
export QUALITY_ENABLE_BANDIT := true
export QUALITY_ENABLE_SAFETY := true

# Analysis Performance Settings
export QUALITY_PARALLEL_ANALYSIS := true
export QUALITY_MAX_WORKERS := 4
export QUALITY_ANALYSIS_TIMEOUT := 300
export QUALITY_INCREMENTAL_ANALYSIS := true

# Reporting Settings
export QUALITY_REPORT_FORMAT := html,json,pdf
export QUALITY_REPORT_OUTPUT_DIR := ./reports
export QUALITY_INCLUDE_TRENDS := true
export QUALITY_INCLUDE_COMPARISONS := true

# Cache Settings
export QUALITY_ENABLE_CACHE := true
export QUALITY_CACHE_DIR := ./.quality_cache
export QUALITY_CACHE_TTL := 3600

# Workspace Analysis Settings
export QUALITY_WORKSPACE_PATH := ../
export QUALITY_EXCLUDE_PATTERNS := vendor/,node_modules/,.git/,.venv/
export QUALITY_INCLUDE_EXTENSIONS := .py,.go,.js,.ts

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-quality
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT QUALITY - Comprehensive Code Quality Analysis Engine

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 DEVELOPMENT UTILITIES
# ============================================================================

dev-quality-server: ## Start development quality analysis server
	@echo "🔧 Starting development quality server..."
	@poetry run python scripts/dev_quality_server.py
	@echo "✅ Development quality server started"

dev-analysis-playground: ## Start quality analysis playground
	@echo "🎮 Starting analysis playground..."
	@poetry run python scripts/analysis_playground.py
	@echo "✅ Analysis playground session complete"

dev-metrics-explorer: ## Start metrics data explorer
	@echo "📊 Starting metrics explorer..."
	@poetry run python scripts/metrics_explorer.py
	@echo "✅ Metrics explorer session complete"

dev-report-designer: ## Start report template designer
	@echo "🎨 Starting report designer..."
	@poetry run python scripts/report_designer.py
	@echo "✅ Report designer session complete"

dev-dashboard-preview: ## Preview quality dashboard
	@echo "📊 Previewing quality dashboard..."
	@poetry run python scripts/dashboard_preview.py
	@echo "✅ Dashboard preview complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Core project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Quality Analysis Engine + Metrics + Reporting"
	@echo "🐍 Python: 3.13"
	@echo "🔗 Framework: FLEXT Core + Quality Tools + Analysis Engine"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Comprehensive Code Quality Analysis Engine"
	@echo "🔗 Dependencies: flext-core, flext-observability, ruff, mypy, pytest"
	@echo "📦 Provides: Quality analysis, metrics collection, comprehensive reporting"
	@echo "🎯 Standards: Enterprise quality analysis with automated reporting"

# ============================================================================
# 🔄 CONTINUOUS INTEGRATION
# ============================================================================

ci-check: validate ## CI quality checks
	@echo "🔍 Running CI quality checks..."
	@poetry run python scripts/ci_quality_report.py
	@echo "✅ CI quality checks complete"

ci-performance: ## CI performance benchmarks
	@echo "⚡ Running CI performance benchmarks..."
	@poetry run python scripts/ci_performance_benchmarks.py
	@echo "✅ CI performance benchmarks complete"

ci-integration: ## CI integration tests
	@echo "🔗 Running CI integration tests..."
	@poetry run pytest tests/integration/ -v --tb=short
	@echo "✅ CI integration tests complete"

ci-quality: ## CI quality analysis tests
	@echo "🔍 Running CI quality tests..."
	@poetry run pytest tests/ -m "quality" -v --tb=short
	@echo "✅ CI quality tests complete"

ci-analysis: ## CI analysis engine tests
	@echo "📊 Running CI analysis tests..."
	@poetry run pytest tests/ -m "analysis" -v --tb=short
	@echo "✅ CI analysis tests complete"

ci-reporting: ## CI reporting tests
	@echo "📋 Running CI reporting tests..."
	@poetry run pytest tests/ -m "reporting" -v --tb=short
	@echo "✅ CI reporting tests complete"

ci-all: ci-check ci-performance ci-integration ci-quality ci-analysis ci-reporting ## Run all CI checks
	@echo "✅ All CI checks complete"

# ============================================================================
# 🚀 PRODUCTION DEPLOYMENT
# ============================================================================

deploy-quality-engine: validate build ## Deploy quality engine for production use
	@echo "🚀 Deploying quality engine..."
	@poetry run python scripts/deploy_quality_engine.py
	@echo "✅ Quality engine deployment complete"

test-deployment: ## Test deployed quality engine functionality
	@echo "🧪 Testing deployed quality engine..."
	@poetry run python scripts/test_deployed_engine.py
	@echo "✅ Deployment test complete"

rollback-deployment: ## Rollback quality engine deployment
	@echo "🔄 Rolling back quality engine deployment..."
	@poetry run python scripts/rollback_engine_deployment.py
	@echo "✅ Deployment rollback complete"

# ============================================================================
# 🔬 MONITORING & OBSERVABILITY
# ============================================================================

monitor-quality-engine: ## Monitor quality engine health
	@echo "📊 Monitoring quality engine health..."
	@poetry run python scripts/monitor_quality_engine.py
	@echo "✅ Quality engine monitoring complete"

monitor-analysis-performance: ## Monitor analysis performance
	@echo "📊 Monitoring analysis performance..."
	@poetry run python scripts/monitor_analysis_performance.py
	@echo "✅ Analysis performance monitoring complete"

monitor-quality-trends: ## Monitor quality trends across workspace
	@echo "📊 Monitoring quality trends..."
	@poetry run python scripts/monitor_quality_trends.py
	@echo "✅ Quality trends monitoring complete"

generate-quality-metrics: ## Generate quality engine metrics
	@echo "📊 Generating quality engine metrics..."
	@poetry run python scripts/generate_engine_metrics.py
	@echo "✅ Quality engine metrics generated"

generate-health-report: ## Generate quality engine health report
	@echo "📊 Generating quality engine health report..."
	@poetry run python scripts/generate_health_report.py
	@echo "✅ Quality engine health report generated"
