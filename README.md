# FLEXT-Quality

<!-- TOC START -->

- [🚀 Key Features](#-key-features)
- [📦 Installation](#-installation)
- [🛠️ Usage](#-usage)
  - [Running Validation](#running-validation)
  - [Checking Specific Rules](#checking-specific-rules)
  - [Integration with Pre-Commit](#integration-with-pre-commit)
- [🏗️ Architecture](#-architecture)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

<!-- TOC END -->

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Quality** is the centralized quality control library for the FLEXT ecosystem. It enforces rigorous architectural standards, checks for anti-patterns, and ensures code health across all projects.

**Reviewed**: 2026-02-17 | **Version**: 0.10.0-dev

Part of the [FLEXT](https://github.com/flext/flext) ecosystem.

## 🚀 Key Features

- **Rule Engine**: Extensible, YAML-based validation rules for Python, Bash, and Architecture.
- **Static Analysis**: Detects dangerous commands, strict typing violations, and `FlextResult` misuse.
- **Centralized Registry**: A single source of truth for linters, hooks, and CI gates.
- **Report Generation**: Detailed analysis reports in JSON, Markdown, and SARIF formats.
- **FLEXT Deep Integration**: Designed specifically to validate `flext-core` patterns (e.g., `FlextService`, `FlextContainer`).

## 📦 Installation

To use `flext-quality` in your project, install via Poetry:

```bash
poetry add flext-quality --group dev
```

## 🛠️ Usage

### Running Validation

Execute a full quality check on your project directory:

```bash
flext-quality validate ./src --report-format json
```

### Checking Specific Rules

Validate only specific rule categories (e.g., architecture):

```bash
flext-quality check --category architecture ./src
```

### Integration with Pre-Commit

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/flext-sh/flext-quality
  rev: v0.9.9
  hooks:
    - id: flext-validate
```

## 🏗️ Architecture

FLEXT-Quality operates as a separate domain service:

- **Domain**: Defines `Rule`, `Violation`, and `Report` entities.
- **Service**: Orchestrates validation logic against the `RuleRegistry`.
- **Adapters**: Outputs results to CLI, CI environment variables, or files.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on adding new validation rules.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
