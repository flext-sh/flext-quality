# Documentation Maintenance Procedures

<!-- TOC START -->

- [Configuration](#configuration)
- [Commands](#commands)
- [Scheduled Maintenance](#scheduled-maintenance)
- [Reports And Notifications](#reports-and-notifications)
- [Validation](#validation)

<!-- TOC END -->

The `flext_quality.docs` package provides documentation audit, validation,
optimization, reporting, notification, and scheduled-maintenance surfaces.
Run commands from the `flext-quality` project root.

## Configuration

Packaged defaults live in `src/flext_quality/docs/config/`.

| File | Owner |
| --- | --- |
| `audit_rules.yaml` | Audit thresholds and checks |
| `style_guide.yaml` | Markdown, formatting, accessibility, and heading rules |
| `validation_config.yaml` | Link and content validation settings |
| `notification_config.yaml` | Notification routes |
| `schedule_config.yaml` | Scheduled maintenance tasks and paths |

Public constructors load these files by default. Commands that expose a config
option accept an explicit path for a project-specific configuration.

## Commands

Inspect supported options through the module entrypoints:

```bash
python -m flext_quality.docs.scripts.audit --help
python -m flext_quality.docs.scripts.optimize --help
python -m flext_quality.docs.scripts.validate --help
python -m flext_quality.docs.scripts.report --help
python -m flext_quality.docs.notifications --help
python -m flext_quality.docs.scheduled_maintenance --help
```

The style validator accepts a Markdown file and an optional style-guide path:

```bash
python -m flext_quality.docs.tools.style_validator README.md
```

## Scheduled Maintenance

`flext_quality.docs.scheduled_maintenance` loads
`src/flext_quality/docs/config/schedule_config.yaml` by default. Use
`--settings` to select another schedule configuration.

```bash
python -m flext_quality.docs.scheduled_maintenance run --list-schedules
python -m flext_quality.docs.scheduled_maintenance run --manual daily
python -m flext_quality.docs.scheduled_maintenance run --daemon
```

The schedule configuration owns report, backup, and log paths. Review those
paths before daemon execution.

## Reports And Notifications

Audit, validation, optimization, and reporting commands accept output paths.
Notification dispatch uses `notification_config.yaml`. An explicit
`enabled: false` configuration prevents dispatch.

## Validation

Use the canonical Make surface for repository checks:

```bash
make test FILE=tests/unit/test_docs_auditor.py
make test FILE=tests/unit/test_docs_link_checker.py
make test FILE=tests/unit/test_docs_style_validator.py
make check FILES="src/flext_quality/docs/scripts/audit.py src/flext_quality/docs/scripts/validate.py"
make gen WHAT=check
```
