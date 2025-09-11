# =============================================================================
# FLEXT-QUALITY - Code Quality Analysis & Metrics Service Makefile
# =============================================================================
# Python 3.13+ Quality Framework - Clean Architecture + DDD + Django + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-quality
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_quality

# Quality Standards
MIN_COVERAGE := 90
QUALITY_MIN_COVERAGE := 90.0
QUALITY_MAX_COMPLEXITY := 10
QUALITY_MAX_DUPLICATION := 5.0

# Django Configuration
DJANGO_PORT := 8000
DATABASE_URL := postgresql://postgres:postgres@localhost:5432/dc_analyzer
REDIS_URL := redis://localhost:6379/0

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE QUALITY_MIN_COVERAGE QUALITY_MAX_COMPLEXITY QUALITY_MAX_DUPLICATION DJANGO_PORT DATABASE_URL REDIS_URL

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-QUALITY - Code Quality Analysis & Metrics Service"
	@echo "======================================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum"
	@echo "Django Port: $(DJANGO_PORT)"
	@echo "Quality Thresholds: Coverage $(QUALITY_MIN_COVERAGE)%, Complexity $(QUALITY_MAX_COMPLEXITY), Duplication $(QUALITY_MAX_DUPLICATION)%"
	@echo "Architecture: Clean Architecture + DDD + Django + Quality Analysis"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY)
# =============================================================================

.PHONY: validate
validate: lint type-check security test quality-check ## Run all quality gates
	@echo "✅ Quality validation complete"

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

.PHONY: type-check
type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# =============================================================================
# TESTING
# =============================================================================

.PHONY: test
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(COV_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

.PHONY: test-quality
test-quality: ## Run quality analysis tests
	$(POETRY) run pytest $(TESTS_DIR) -m quality -v

.PHONY: test-django
test-django: ## Run Django-specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m django -v

.PHONY: test-analysis
test-analysis: ## Run analysis engine tests
	$(POETRY) run pytest $(TESTS_DIR) -k analysis -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	$(POETRY) run pytest $(TESTS_DIR) -m e2e -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(COV_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

# =============================================================================
# QUALITY ANALYSIS OPERATIONS
# =============================================================================

.PHONY: analyze
analyze: ## Run comprehensive quality analysis
	$(POETRY) run python -m flext_quality.cli analyze

.PHONY: quality-check
quality-check: ## Check quality thresholds
	$(POETRY) run python -m flext_quality.cli check-thresholds

.PHONY: metrics
metrics: ## Collect quality metrics
	$(POETRY) run python -m flext_quality.cli collect-metrics

.PHONY: report
report: ## Generate quality reports
	$(POETRY) run python -m flext_quality.cli generate-report

.PHONY: workspace-analyze
workspace-analyze: ## Analyze FLEXT workspace
	$(POETRY) run python -m flext_quality.cli analyze-workspace

.PHONY: detect-issues
detect-issues: ## Detect quality issues
	$(POETRY) run python -m flext_quality.cli detect-issues

.PHONY: calculate-scores
calculate-scores: ## Calculate quality scores
	$(POETRY) run python -m flext_quality.cli calculate-scores

.PHONY: quality-grade
quality-grade: ## Calculate overall quality grade
	$(POETRY) run python -m flext_quality.cli quality-grade

.PHONY: coverage-score
coverage-score: ## Calculate coverage score
	$(POETRY) run python -m flext_quality.cli coverage-score

# =============================================================================
# DJANGO OPERATIONS
# =============================================================================

.PHONY: web-start
web-start: ## Start Django web interface
	$(POETRY) run python manage.py runserver $(DJANGO_PORT)

.PHONY: web-migrate
web-migrate: ## Run Django migrations
	$(POETRY) run python manage.py migrate

.PHONY: web-shell
web-shell: ## Open Django shell
	$(POETRY) run python manage.py shell

.PHONY: web-collectstatic
web-collectstatic: ## Collect static files
	$(POETRY) run python manage.py collectstatic --noinput

.PHONY: web-createsuperuser
web-createsuperuser: ## Create Django superuser
	$(POETRY) run python manage.py createsuperuser

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	$(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	rm -rf reports/ quality_reports/ analysis_results/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Quality Service: $$($(POETRY) run python -c 'import flext_quality; print(getattr(flext_quality, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================

# =============================================================================

.PHONY: t l f tc c i v
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-quality test-django test-analysis test-e2e test-fast coverage-html build build-clean analyze quality-check metrics report workspace-analyze detect-issues calculate-scores quality-grade coverage-score web-start web-migrate web-shell web-collectstatic web-createsuperuser docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v
