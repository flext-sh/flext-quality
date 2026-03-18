# Documentation Maintenance Modernization Roadmap

<!-- TOC START -->

- [Table of Contents](#table-of-contents)
- [Guiding Principles](#guiding-principles)
- [Phase 1 – Foundation (Weeks 1-2)](#phase-1-foundation-weeks-1-2)
- [Phase 2 – Platform Upgrades (Weeks 3-5)](#phase-2-platform-upgrades-weeks-3-5)
- [Phase 3 – Pilot Migrations (Weeks 6-8)](#phase-3-pilot-migrations-weeks-6-8)
- [Phase 4 – Portfolio Rollout (Weeks 9-14)](#phase-4-portfolio-rollout-weeks-9-14)
- [Phase 5 – Optimization & Governance (Weeks 15+)](#phase-5-optimization-governance-weeks-15)
- [Cross-Cutting Workstreams](#cross-cutting-workstreams)
- [Progress Log](#progress-log)

<!-- TOC END -->

## Table of Contents

- [Documentation Maintenance Modernization Roadmap](#documentation-maintenance-modernization-roadmap)
  - [Guiding Principles](#guiding-principles)
  - [Phase 1 – Foundation (Weeks 1-2)](#phase-1--foundation-weeks-1-2)
  - [Phase 2 – Platform Upgrades (Weeks 3-5)](#phase-2--platform-upgrades-weeks-3-5)
  - [Phase 3 – Pilot Migrations (Weeks 6-8)](#phase-3--pilot-migrations-weeks-6-8)
  - [Phase 4 – Portfolio Rollout (Weeks 9-14)](#phase-4--portfolio-rollout-weeks-9-14)
  - [Phase 5 – Optimization & Governance (Weeks 15+)](#phase-5--optimization--governance-weeks-15)
  - [Cross-Cutting Workstreams](#cross-cutting-workstreams)
  - [Progress Log](#progress-log)

> Scope: Consolidate and enhance documentation maintenance across all FLEXT projects (32+ repos) using shared tooling provided by `flext-quality`.

## Guiding Principles

- **Centralize capabilities** in `flext-quality`, exposing profile-based APIs so individual projects remain thin wrappers.
- **Configuration over code**: project-specific behavior is driven entirely through metadata (`docs/maintenance/config.*`,
  schedules, notifications).
- **Automation first**: every task produce machine-readable output (JSON) and human-friendly Markdown; HTML and dashboards extend the same data.
- **Iterative rollout**: ship in slices (pilot repos → full portfolio) with validation gates at every stage.

## Phase 1 – Foundation (Weeks 1-2)

1. **Metadata Inventory**
   - Scan all repositories for existing `docs/maintenance/` assets.
   - Normalize config schemas (audit, style, validation, schedule).
   - Catalogue current artifacts (Markdown, HTML, JSON, dashboards) and consumers.
1. **Shared API Enhancements**
   - Extend profile orchestrator to accept `output_formats=["markdown"]` with future-proof hooks for HTML.
   - Ensure helper functions (`run_comprehensive`, `run_audit`, etc.) return structured results.
   - Document baseline expectations in `flext-quality/docs/README.md`.
1. **Tooling Audit**
   - Evaluate candidate libraries (Typer/Rich, httpx/aiohttp, markdown-it, pandas/polars) and draft recommendations.

## Phase 2 – Platform Upgrades (Weeks 3-5)

1. **CLI & UX Modernization**
   - Introduce Typer-based entry points for audit/validate/optimize/report with consistent flags.
   - Add Rich-based progress/logging for clarity.
1. **Async Validation Layer**
   - Replace ad-hoc concurrency with `httpx.AsyncClient` for link checking.
   - Implement rate limiting/backoff strategies configurable per profile.
1. **Markdown Report Generator**
   - Create templated Markdown summaries (`jinja2` templates).
   - Persist outputs in `docs/maintenance/reports/*.md` alongside JSON snapshots.
1. **Shared Scheduling Interface**
   - Convert schedule execution to a single `flext-quality` runner with pluggable backends (cron, systemd, GitHub Actions).

## Phase 3 – Pilot Migrations (Weeks 6-8)

1. **Select Pilot Repos**
   - Target `flext-ldap` (Advanced profile) and `flext-grpc` (gRPC profile).
   - Mirror existing functionality using new shared APIs.
1. **Validation & Sign-off**
   - Run parallel jobs comparing legacy vs. new outputs.
   - Capture diffs, regression-test Markdown generation, and collect stakeholder feedback.
1. **Documentation & Training**
   - Produce quick-start guides per profile (Advanced, gRPC, others as needed).
   - Host internal demos or recordings.

## Phase 4 – Portfolio Rollout (Weeks 9-14)

1. **Batch Migration**
   - Group remaining projects by similarity; migrate in waves of 5-6.
   - For each wave: update wrappers, align configs, update CI workflows, validate outputs.
1. **Central Monitoring**
   - Wire aggregated metrics into dashboards (Markdown summary + optional HTML).
   - Establish alerting thresholds using normalized metadata.
1. **Process Integration**
   - Update release playbooks to reference the shared tooling.
   - Ensure new projects adopt `flext-quality` profiles from inception.

## Phase 5 – Optimization & Governance (Weeks 15+)

1. **Performance & Scalability**
   - Benchmark large repos; optimize IO (async filesystem reads, caching).
   - Introduce optional distributed execution (e.g., via Celery/Arq) if required.
1. **Quality Gates**
   - Enforce documentation checks in CI/CD pipelines with configurable severity.
1. **Continuous Improvement**
   - Establish quarterly reviews of audit rules, templates, and library versions.
   - Maintain change logs and upgrade guides within `flext-quality`.

## Cross-Cutting Workstreams

- **Testing Strategy**: unit tests for shared modules, snapshot markdown comparisons, integration tests via pilot repos.
- **Versioning & Releases**: semantic versioning for `flext-quality`; changelog entries per release.
- **Security & Compliance**: evaluate link-validation timeouts, ensure no sensitive data leaks into reports.
- **Stakeholder Communication**: frequent updates through README, internal channels, or dashboards.

______________________________________________________________________

**Next Immediate Actions**

1. Approve this roadmap and adjust timelines/priorities as needed.
1. Kick off Phase 1 metadata inventory and tooling audit (ownership: Docs Platform team).
1. Schedule design review for Phase 2 architecture proposals (CLI, async validation, templating).

## Progress Log

- **2025-10-16** – Initiated Phase 1 metadata inventory. Current findings:

  - Detected active maintenance directories in `flext-grpc`, `flext-ldap`, `flext-observability`, `flext-quality`,
    and `flext-meltano-native`.
  - Collected configuration files for shared tooling:
    - `flext-grpc/docs/maintenance/config.json`
    - `flext-ldap/docs/maintenance/config.yaml`
    - `flext-quality/docs/maintenance/config/{audit_rules,style_guide,validation_config,schedule_config,notification_config}.yaml`
  - No additional maintenance metadata discovered in other repositories within current depth scan.
  - Next: expand search depth, document artifacts (Markdown/HTML/JSON) per repo, and align schema comparisons.

- **2025-10-16** – Completed high-level artifact inventory for detected projects:

  - `flext-grpc`: maintenance scripts (`audit.py`, `validation.py`, `optimization.py`, `reporting.py`, `sync.py`),
    user documentation (`README.md`, `user-guide.md`, `troubleshooting.md`, `api-reference.md`), `Makefile`,
    and `requirements.txt`.
  - `flext-ldap`: wrappers for shared tooling, configuration (`config.yaml`), legacy scripts (`run_maintenance.sh`),
    documentation (`README.md`, `user-guide.md`, `troubleshooting.md`), and cache artifacts (`.link_cache.json`).
  - `flext-observability`: standalone Audit script (`audit/content-audit.py`) with associated reports (`dead_code_analysis.md`,
    `dead_code_cleanup_summary.md`, `README.md`).
  - `flext-meltano-native`: single maintenance `README.md` identified; no automation scripts present yet.
  - Next: map each artifact to the shared capabilities matrix (audit/validation/optimization/reporting),
    evaluate gaps against target schema, and prepare normalization checklist.

- **2025-10-16** – Capability mapping against shared maintenance pillars:

  | Repository             | Audit                           | Validation               | Optimization                                            | Reporting                  | Sync                                                                           | Config Format                               | Notes                                                        |
  | ---------------------- | ------------------------------- | ------------------------ | ------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------ |
  | `flext-grpc`           | ✅ (`audit.py`)                 | ✅ (`validation.py`)     | ✅ (`optimization.py`)                                  | ✅ (`reporting.py`,        |                                                                                |                                             |                                                              |
  | HTML/CSV dashboards)   | ✅ (`sync.py`)                  | `config.json`            | Full standalone toolchain with Makefile + requirements. |                            |                                                                                |                                             |                                                              |
  | `flext-ldap`           | ✅ (wrappers to shared profile) | ✅ (`validate_links.py`, |                                                         |                            |                                                                                |                                             |                                                              |
  | `validate_style.py`)   | ✅ (`optimize.py`)              | ✅ (`report.py`)         | ✅ (`sync.py`)                                          | `config.yaml`              | Uses shared infrastructure plus legacy shell runner; includes cache artifacts. |                                             |                                                              |
  | `flext-observability`  | ✅ (`audit/content-audit.py`)   | ❌                       | ❌                                                      | ⚠️ Markdown summaries only | ❌                                                                             | config embedded in script (`yaml` optional) | Lightweight audit only; no automation scripts detected.      |
  | `flext-meltano-native` | ❌                              | ❌                       | ❌                                                      | ❌                         | ❌                                                                             | None                                        | Documentation guidance only; no executable maintenance code. |

  - Observed schema divergence: JSON-based config (`flext-grpc`) vs YAML (`flext-ldap`) vs inline defaults (`flext-observability`).
  - Next: draft normalization checklist (config schema conversion, capability gaps,
    wrapper migration plan) and define acceptance tests per capability pillar.

- **2025-10-16** – Published detailed metadata inventory (`docs/maintenance/metadata-inventory.md`) summarizing directories,
  config formats, markdown deliverables,
  and automation scripts per repository. Established normalization checklist covering schema conversion,
  capability gap closure, report naming, and automation mapping.

- **2025-10-16** – Completed initial tooling audit (`docs/maintenance/tooling-audit.md`) highlighting candidate libraries for CLI modernization (Typer,
  Rich), async validation (`httpx`), templated reporting (Jinja2), configuration validation (pydantic),
  and supporting utilities (pathspec, rapidfuzz).

- **2025-10-16** – Implemented shared reporting enhancements: default output format now Markdown,
  centralized export pipeline (`ReportGenerator.export_report`) produces timestamped Markdown/JSON/HTML artifacts with `latest_*` pointers,
  and `DocumentationMaintainer` records generated outputs plus quality metrics.

- **2025-10-16** – Completed Phase 1 standardization wave: introduced the shared Typer CLI (`src/flext_quality/docs_maintenance/cli.py`) and extended the orchestrator to support programmatic handlers; removed legacy project-side scripts in `flext-ldap`,
  `flext-grpc`, `flext-observability`,
  and `flext-meltano-native`; converted per-project configs to the normalized YAML schema; and wired new `docs-maintenance` Makefile targets that invoke the shared runner with Markdown-only output.

- **2025-10-16** – Unified profile layout: removed the dedicated `grpc` maintenance profile in favour of the shared advanced toolkit,
  mapped legacy profile slugs to the consolidated module,
  and confirmed all projects execute through the same Markdown-first workflow via their Makefile targets.
