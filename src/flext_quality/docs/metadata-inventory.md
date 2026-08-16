# Documentation Maintenance Metadata Inventory

<!-- TOC START -->

- [Normalization Checklist](#normalization-checklist)

<!-- TOC END -->

| Surface | Current Path | Purpose |
| --- | --- | --- |
| Packaged configuration | `src/flext_quality/docs/config/` | Audit, style, validation, notification, and schedule settings |
| Public commands | `src/flext_quality/docs/scripts/` | Audit, optimize, report, and validate entrypoints |
| Public tools | `src/flext_quality/docs/tools/` | Link and style validation |
| Scheduled maintenance | `src/flext_quality/docs/scheduled_maintenance.py` | Scheduled and manual maintenance dispatch |
| Operator documentation | `src/flext_quality/docs/README.md`, `src/flext_quality/docs/maintenance-procedures.md` | Supported setup and operation |

## Normalization Checklist

1. Keep packaged configuration paths aligned with public default constructors.
1. Keep command and tool names aligned with importable modules.
1. Remove inventory entries when their source path is removed.
