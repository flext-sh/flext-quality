# FLEXT-Quality Development Commands

## Essential Commands (From Makefile)

### Setup & Installation

```bash
make setup              # Complete development environment setup
make install            # Install dependencies only
make install-dev        # Install dev dependencies
```

### Quality Gates (MANDATORY - Zero Tolerance)

```bash
make validate           # Complete validation pipeline (lint + type + security + test + quality)
make check             # Quick validation (lint + type-check)
make lint              # Ruff linting
make type-check        # MyPy type checking (strict mode)
make security          # Security scanning with Bandit + pip-audit
make fix               # Auto-fix issues with ruff
```

### Testing Commands

```bash
make test              # Run tests with coverage (90% minimum)
make test-unit         # Unit tests only
make test-integration  # Integration tests
make test-quality      # Quality analysis tests
make test-django       # Django-specific tests
make test-analysis     # Analysis engine tests
make test-e2e          # End-to-end tests
make test-fast         # Tests without coverage
make coverage-html     # Generate HTML coverage report
```

### Quality Analysis Operations

```bash
make analyze           # Run comprehensive quality analysis
make quality-check     # Check quality thresholds
make metrics           # Collect quality metrics
make report           # Generate quality reports
make workspace-analyze # Analyze FLEXT workspace
make detect-issues     # Detect quality issues
make calculate-scores  # Calculate quality scores
make quality-grade     # Calculate overall quality grade
make coverage-score    # Calculate coverage score
```

### Build & Distribution

```bash
make build             # Build package
make build-clean       # Clean and build
```

### Development Utilities

```bash
make format           # Auto-format code
make clean            # Clean build artifacts
make diagnose         # System diagnostics
make doctor           # Health check (diagnose + check)
```

### Django Web Interface

```bash
make web-start        # Start Django web interface (port 8000)
make web-migrate      # Run Django migrations
make web-shell        # Open Django shell
make web-collectstatic # Collect static files
make web-createsuperuser # Create Django superuser
```

## CLI Commands (via flext-quality)

```bash
flext-quality analyze --project /path/to/project --output report.html
flext-quality check-thresholds --min-coverage 90.0 --max-complexity 10
flext-quality collect-metrics --workspace /workspace --format json
flext-quality generate-report --analysis-id 123 --format pdf
flext-quality analyze-workspace --parallel --security-scan
```

## Short Aliases

```bash
make t    # test
make l    # lint
make f    # format
make tc   # type-check
make c    # clean
make i    # install
make v    # validate
```
