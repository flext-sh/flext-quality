# Private project handlers for flext-quality.
# Strict extension: only `_custom_<verb>_<what>` handlers and `(pre|post)-<verb>[-<what>]`
# hooks. Public targets, toolchain vars, .DEFAULT_GOAL, includes, and help are
# invalid (base.mk owns those). Each handler maps to `make <verb> WHAT=<what>`.
# NOTE: all standard-verb reimplementations (check/lint/format/type/test/build/
# clean/diagnose) and workspace toolchain vars were removed; base.mk owns them.
# --- Genuine project-specific quality-analysis actions (run verb) ---
.PHONY: _custom_run_analyze _custom_run_quality-check _custom_run_metrics _custom_run_report
.PHONY: _custom_run_workspace-analyze _custom_run_detect-issues _custom_run_calculate-scores
.PHONY: _custom_run_quality-grade _custom_run_coverage-score
_custom_run_analyze: ## make run WHAT=analyze — comprehensive quality analysis
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli analyze
_custom_run_quality-check: ## make run WHAT=quality-check — check quality thresholds
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli check-thresholds
_custom_run_metrics: ## make run WHAT=metrics — collect quality metrics
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli collect-metrics
_custom_run_report: ## make run WHAT=report — generate quality reports
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli generate-report
_custom_run_workspace-analyze: ## make run WHAT=workspace-analyze — analyze FLEXT workspace
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli analyze-workspace
_custom_run_detect-issues: ## make run WHAT=detect-issues — detect quality issues
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli detect-issues
_custom_run_calculate-scores: ## make run WHAT=calculate-scores — calculate quality scores
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli calculate-scores
_custom_run_quality-grade: ## make run WHAT=quality-grade — overall quality grade
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli quality-grade
_custom_run_coverage-score: ## make run WHAT=coverage-score — coverage score
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python -m flext_quality.cli coverage-score
# --- Django web operations (run verb) ---
.PHONY: _custom_run_web-start _custom_run_web-migrate _custom_run_web-shell _custom_run_web-collectstatic _custom_run_web-createsuperuser
_custom_run_web-start: ## make run WHAT=web-start — start Django web interface
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py runserver 8000
_custom_run_web-migrate: ## make run WHAT=web-migrate — run Django migrations
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py migrate
_custom_run_web-shell: ## make run WHAT=web-shell — open Django shell
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py shell
_custom_run_web-collectstatic: ## make run WHAT=web-collectstatic — collect static files
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py collectstatic --noinput
_custom_run_web-createsuperuser: ## make run WHAT=web-createsuperuser — create Django superuser
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run python manage.py createsuperuser
# --- Quality-domain test markers (test verb) ---
.PHONY: _custom_test_quality _custom_test_django _custom_test_analysis
_custom_test_quality: ## make test WHAT=quality — quality analysis tests
	$(Q)$(POETRY) run pytest $(TESTS_DIR) -m quality -v
_custom_test_django: ## make test WHAT=django — Django-specific tests
	$(Q)$(POETRY) run pytest $(TESTS_DIR) -m django -v
_custom_test_analysis: ## make test WHAT=analysis — analysis engine tests
	$(Q)$(POETRY) run pytest $(TESTS_DIR) -k analysis -v
