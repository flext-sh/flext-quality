# FLEXT Quality Documentation Tools

The `flext_quality.docs` package audits, validates, optimizes, reports on, and
notifies about Markdown documentation. It requires Python `>=3.13,<3.14`.

## Setup And Validation

Run all commands from the `flext-quality` project root.

```bash
make setup
make gen WHAT=check
make check
make test FILE=tests/unit/test_docs_auditor.py
make build WHAT=artifacts
```

Packaged defaults live in `src/flext_quality/docs/config/`:

- `audit_rules.yaml` owns audit thresholds and checks.
- `style_guide.yaml` owns Markdown, formatting, accessibility, and heading rules.
- `validation_config.yaml` owns link and content validation settings.
- `notification_config.yaml` owns notification routes.
- `schedule_config.yaml` owns scheduled maintenance settings.

## Public Modules

The supported module entrypoints are:

- `flext_quality.docs.scripts.audit`
- `flext_quality.docs.scripts.optimize`
- `flext_quality.docs.scripts.validate`
- `flext_quality.docs.scripts.report`
- `flext_quality.docs.notifications`
- `flext_quality.docs.tools.style_validator`

Inspect command options through the module entrypoint:

```bash
python -m flext_quality.docs.scripts.audit --help
python -m flext_quality.docs.scripts.optimize --help
python -m flext_quality.docs.scripts.validate --help
python -m flext_quality.docs.scripts.report --help
python -m flext_quality.docs.notifications --help
```

Validate one Markdown file with the packaged style guide:

```bash
python -m flext_quality.docs.tools.style_validator README.md
```

Library consumers can construct the public tools directly:

```python
from flext_quality.docs import FlextQualityLinkChecker, FlextQualityStyleValidator

link_checker = FlextQualityLinkChecker()
style_validator = FlextQualityStyleValidator()
```

See `maintenance-procedures.md` for the current operator procedure and
`docs-maintenance-roadmap.md` for tracked documentation-tool work.
