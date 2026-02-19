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
WORKSPACE_ROOT := $(shell cd .. && pwd)

# Quality Standards
QUALITY_MIN_COVERAGE := 100.0
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
	@echo "Coverage: $(MIN_COVERAGE)% minimum (MANDATORY)"
	@echo "Django Port: $(DJANGO_PORT)"
	@echo "Quality Thresholds: Coverage $(QUALITY_MIN_COVERAGE)%, Complexity $(QUALITY_MAX_COMPLEXITY), Duplication $(QUALITY_MAX_DUPLICATION)%"
	@echo "Architecture: Clean Architecture + DDD + Django + Quality Analysis"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install-workspace
install-workspace: ## Install workspace dependencies (flext-core, etc.)
	@echo "📦 Installing workspace dependencies from $(WORKSPACE_ROOT)..."
	cd $(WORKSPACE_ROOT) && $(POETRY) install
	@echo "✅ Workspace dependencies installed"

.PHONY: install
install: install-workspace ## Install all dependencies (workspace + local)
	$(POETRY) install

.PHONY: install-dev
install-dev: install-workspace ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install
	@echo "✅ Setup complete - flext-core and all dependencies available"

# =============================================================================
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates
	@echo "✅ Quality validation complete"

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format .

.PHONY: format-check
format-check: ## Check formatting
	$(POETRY) run ruff format --check .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check $(SRC_DIR)

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR) -c $(WORKSPACE_ROOT)/pyproject.toml
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# =============================================================================
# EXTENDED QUALITY CHECKS
# =============================================================================

.PHONY: dead-code
dead-code: ## Dead code detection (Vulture)
	cd $(WORKSPACE_ROOT) && $(POETRY) run vulture $(CURDIR)/$(SRC_DIR) --min-confidence 80 --exclude "tests,examples" || true

.PHONY: modernize
modernize: ## Modern patterns suggestions (via Ruff FURB rules)
	@echo "Note: Ruff already applies 36 FURB rules from refurb (see: ruff rule --all | grep FURB)"
	@echo "Refurb standalone disabled - incompatible with Python 3.13 TypeAliasStmt"
	@echo "Run 'make lint' to apply modernization suggestions via Ruff"

.PHONY: cognitive-complexity
cognitive-complexity: ## Cognitive complexity (Complexipy)
	cd $(WORKSPACE_ROOT) && $(POETRY) run complexipy $(CURDIR)/$(SRC_DIR) --max-complexity-allowed 15 || true

.PHONY: spell-check
spell-check: ## Spell checking (Codespell)
	cd $(WORKSPACE_ROOT) && $(POETRY) run codespell $(CURDIR)/$(SRC_DIR) --toml $(WORKSPACE_ROOT)/pyproject.toml --quiet-level 3 || true

.PHONY: deps
deps: ## Analyze dependencies with deptry (missing, unused, transitive)
	@echo "Analyzing dependencies in $(PROJECT_NAME)..."
	uvx deptry . --no-ansi 2>&1 | grep -E "(DEP00|Found)" || echo "No issues"

.PHONY: validate-full
validate-full: lint format-check type-check dead-code cognitive-complexity spell-check security test ## Full + extended checks

# =============================================================================
# TESTING (MANDATORY - 100% COVERAGE)
# =============================================================================

.PHONY: test
test: ## Run tests with 100% coverage (MANDATORY)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -q --maxfail=10000 --cov=$(COV_DIR) --cov-report=term-missing:skip-covered --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

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
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest --cov=$(COV_DIR) --cov-report=html

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
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli analyze

.PHONY: quality-check
quality-check: ## Check quality thresholds
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli check-thresholds

.PHONY: metrics
metrics: ## Collect quality metrics
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli collect-metrics

.PHONY: report
report: ## Generate quality reports
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli generate-report

.PHONY: workspace-analyze
workspace-analyze: ## Analyze FLEXT workspace
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli analyze-workspace

.PHONY: detect-issues
detect-issues: ## Detect quality issues
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli detect-issues

.PHONY: calculate-scores
calculate-scores: ## Calculate quality scores
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli calculate-scores

.PHONY: quality-grade
quality-grade: ## Calculate overall quality grade
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli quality-grade

.PHONY: coverage-score
coverage-score: ## Calculate coverage score
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli coverage-score

# =============================================================================
# DJANGO OPERATIONS
# =============================================================================

.PHONY: web-start
web-start: ## Start Django web interface
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py runserver $(DJANGO_PORT)

.PHONY: web-migrate
web-migrate: ## Run Django migrations
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py migrate

.PHONY: web-shell
web-shell: ## Open Django shell
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py shell

.PHONY: web-collectstatic
web-collectstatic: ## Collect static files
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py collectstatic --noinput

.PHONY: web-createsuperuser
web-createsuperuser: ## Create Django superuser
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py createsuperuser

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
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts and cruft
	@echo "🧹 Cleaning $(PROJECT_NAME) - removing build artifacts, cache files, and cruft..."

	# Build artifacts
	rm -rf build/ dist/ *.egg-info/

	# Test artifacts
	rm -rf .pytest_cache/ htmlcov/ .coverage .coverage.* coverage.xml

	# Python cache directories
	rm -rf .mypy_cache/ .pyrefly_cache/ .ruff_cache/

	# Python bytecode
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

	# Temporary files
	find . -type f -name "*.tmp" -delete 2>/dev/null || true
	find . -type f -name "*.temp" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true

	# Log files
	find . -type f -name "*.log" -delete 2>/dev/null || true

	# Editor files
	find . -type f -name ".vscode/settings.json" -delete 2>/dev/null || true
	find . -type f -name ".idea/" -type d -exec rm -rf {} + 2>/dev/null || true

	
	# Quality-specific files
	rm -rf reports/ quality-*.json
	rm -rf data/ output/ temp/

	@echo "✅ $(PROJECT_NAME) cleanup complete"

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
	@echo "Quality Service: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import flext_quality; print(getattr(flext_quality, \"__version__\", \"dev\"))' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================

# =============================================================================

.PHONY: t l f tc c i v vf dd cc sp dp
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate
vf: validate-full
dd: dead-code
cc: cognitive-complexity
sp: spell-check
dp: deps

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install-workspace install install-dev setup validate check lint format format-check type-check security fix dead-code modernize cognitive-complexity spell-check deps validate-full test test-unit test-integration test-quality test-django test-analysis test-e2e test-fast coverage-html build build-clean analyze quality-check metrics report workspace-analyze detect-issues calculate-scores quality-grade coverage-score web-start web-migrate web-shell web-collectstatic web-createsuperuser docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v vf dd cc sp dp
