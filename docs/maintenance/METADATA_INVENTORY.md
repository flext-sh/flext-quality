# Documentation Maintenance Metadata Inventory

| Repository | Maintenance Directory | Config Files | Markdown Assets | Automation Scripts | Notes |
|------------|-----------------------|--------------|------------------|--------------------|-------|
| flext-grpc | `flext-grpc/docs/maintenance` | `config.json` | `README.md`, `user-guide.md`, `troubleshooting.md`, `api-reference.md` | `audit.py`, `validation.py`, `optimization.py`, `reporting.py`, `sync.py`, `Makefile`, `requirements.txt` | Full standalone toolkit; JSON configuration diverges from shared YAML schema. |
| flext-ldap | `flext-ldap/docs/maintenance` | `config.yaml` | `README.md`, `user-guide.md`, `troubleshooting.md` | Wrappers (`audit.py`, `maintain.py`, `optimize.py`, `sync.py`, `validate_links.py`, `validate_style.py`, `report.py`), legacy `run_maintenance.sh` | Uses shared `flext-quality` profile API; includes `.link_cache.json`. |
| flext-observability | `flext-observability/docs/maintenance` | *(inline defaults in `audit/content-audit.py`)* | `README.md`, `dead_code_analysis.md`, `dead_code_cleanup_summary.md` | `audit/content-audit.py` | Audit-only workflow; no explicit validation/optimize/report scripts or configs. |
| client-b-meltano-native | `client-b-meltano-native/docs/maintenance` | *(none)* | `README.md` | *(none)* | Documentation guidance only; no automation currently implemented. |
| flext-quality | `flext-quality/docs/maintenance` | `config/audit_rules.yaml`, `config/style_guide.yaml`, `config/validation_config.yaml`, `config/schedule_config.yaml`, `config/notification_config.yaml`, `config/lychee.toml` | `README.md`, `MAINTENANCE_PROCEDURES.md`, `REFACTORING_PLAN.md` | Shared core (`scripts/*.py`, `dashboard.py`, `scheduled_maintenance.py`) | Source of shared tooling; serves as target schema for alignment. |

## Normalization Checklist

1. Convert JSON-based configs (`flext-grpc`) to shared YAML schema or generate adapters.
2. Extract inline/implicit configs (`flext-observability`) into explicit YAML files.
3. Define minimum capability set (audit, validation, optimization, reporting, sync) and plan for filling gaps per repository.
4. Document required Markdown deliverables and ensure consistent naming/location (`docs/maintenance/reports/*.md`).
5. Catalog existing automation entry points (CLI commands, cron jobs) and map them to `flext-quality` profiles.
