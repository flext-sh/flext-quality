# Documentation Maintenance Tooling Audit

<!-- TOC START -->

- [Table of Contents](#table-of-contents)
- [CLI & UX](#cli-ux)
- [HTTP & Concurrency](#http-concurrency)
- [Markdown & Reporting](#markdown-reporting)
- [Configuration & Validation](#configuration-validation)
- [Scheduling & Automation](#scheduling-automation)
- [File & Data Processing](#file-data-processing)
- [Observability](#observability)
  - [Immediate Recommendations (Phase 2+)](#immediate-recommendations-phase-2)

<!-- TOC END -->

## Table of Contents

- [Documentation Maintenance Tooling Audit](#documentation-maintenance-tooling-audit)
  - [CLI & UX](#cli--ux)
  - [HTTP & Concurrency](#http--concurrency)
  - [Markdown & Reporting](#markdown--reporting)
  - [Configuration & Validation](#configuration--validation)
  - [Scheduling & Automation](#scheduling--automation)
  - [File & Data Processing](#file--data-processing)
  - [Observability](#observability)
    - [Immediate Recommendations (Phase 2+)](#immediate-recommendations-phase-2)

**Goal:** Identify modern Python libraries to streamline documentation maintenance across FLEXT projects while reducing bespoke code.

## CLI & UX

- **[Typer](https://typer.tiangolo.com/)** → consistent CLI definitions with automatic help/validation (replacement for ad-hoc `argparse`).
- **[Rich](https://rich.readthedocs.io/)** → structured logging, progress bars, and tabular summaries for audits/validation runs.

## HTTP & Concurrency

- **[httpx](https://www.python-httpx.org/) + asyncio** → async link validation with built-in timeout/retry controls.
- **[AnyIO](https://anyio.readthedocs.io/)** → unified async primitives (optional) for background tasks.

## Markdown & Reporting

- **[Markdown-it-py](https://markdown-it-py.readthedocs.io/)** → parsing Markdown for headings/anchors when richer introspection is needed.
- **[Jinja2](https://jinja.palletsprojects.com/)** → templated Markdown/HTML outputs; integrates easily with our shared configs.
- **[tabulate](https://pypi.org/project/tabulate/)** or Rich tables for formatted metrics in CLI/Markdown.

## Configuration & Validation

- **[pydantic](https://docs.pydantic.dev/)** → schema validation for project-level configuration files (JSON/YAML) and shared defaults.
- **[PyYAML](https://pyyaml.org/)** → standard YAML loader/dumper with safe defaults (already in use).

## Scheduling & Automation

- **[APScheduler](https://apscheduler.readthedocs.io/)** → advanced scheduling beyond basic cron (optional future enhancement).

## File & Data Processing

- **[pathspec](https://pypi.org/project/pathspec/)** → consistent glob/ignore handling when crawling docs.
- **[rapidfuzz](https://maxbachmann.github.io/RapidFuzz/)** → fuzzy matching for suggested link repairs.

## Observability

- **[structlog](https://www.structlog.org/)** or Rich log handler for structured outputs that can be harvested by CI pipelines.

______________________________________________________________________

### Immediate Recommendations (Phase 2+)

1. Adopt Typer + Rich for all shared CLI entry points (`audit`, `validate`, `optimize`, `report`).
1. Migrate link validation to `httpx.AsyncClient` with backoff/retry helpers.
1. Use Jinja2 for Markdown templates (reports, dashboards) alongside Rich tables for CLI previews.
1. Validate project configs via pydantic models to enforce schema normalization.

This audit informs upcoming phases of the roadmap; selections can be revisited as requirements evolve.
