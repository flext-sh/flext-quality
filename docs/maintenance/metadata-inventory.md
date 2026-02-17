# Documentation Maintenance Metadata Inventory

| Repository | Maintenance Directory         | Config Files  | Markdown Assets                                                        | Automation Scripts                     | Notes                                                           |
| ---------- | ----------------------------- | ------------- | ---------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------- |
| flext-grpc | `flext-grpc/docs/maintenance` | `config.yaml` | `README.md`, `user-guide.md`, `troubleshooting.md`, `api-reference.md` | _(shared runner invoked via Makefile)_ | Migrated to shared `flext-quality` CLI; legacy scripts removed. |

| flext-ldap | `flext-ldap/docs/maintenance` | `config.yaml` | `README.md`,
`user-guide.md`,
`troubleshooting.md` | _(shared runner invoked via Makefile)_ | Uses shared profile with YAML config; local wrappers removed. |
| flext-observability | `flext-observability/docs/maintenance` | `config.yaml` | `README.md`,
`dead_code_analysis.md`,
`dead_code_cleanup_summary.md` | _(shared runner invoked via Makefile)_ | Converted inline audit settings to YAML; scripts removed. |
| client-b-meltano-native | `client-b-meltano-native/docs/maintenance` | `config.yaml` | `README.md` | _(shared runner invoked via Makefile)_ | Added first-class config + Makefile target powered by shared runner. |
| flext-quality | `flext-quality/docs/maintenance` | `config/audit_rules.yaml`,
`config/style_guide.yaml`, `config/validation_config.yaml`, `config/schedule_config.yaml`,
`config/notification_config.yaml`, `config/lychee.toml` | `README.md`, `maintenance-procedures.md`,
`REFACTORING_PLAN.md` | Shared core (`scripts/*.py`, `dashboard.py`,
`scheduled_maintenance.py`) | Source of shared tooling; serves as target schema for alignment. |

All repositories now execute through the consolidated **advanced** profile; the legacy `grpc` slug is retained only as an alias for backward compatibility.

## Normalization Checklist

1. ✅ Convert JSON-based configs (`flext-grpc`) to shared YAML schema.
2. ✅ Extract inline/implicit configs (`flext-observability`) into explicit YAML files.
3. Align capability coverage with shared CLI options (identify profile gaps before Phase 2 upgrades).
4. Document required Markdown deliverables and ensure consistent naming/location (`docs/maintenance/reports/*.md`).
5. Replace bespoke automation entry points with shared Makefile targets invoking `flext-quality` profiles (completed for initial wave; extend to remaining repos during rollout).
