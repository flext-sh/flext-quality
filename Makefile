# flext-quality - Code Quality Tools
PROJECT_NAME := flext-quality
COV_DIR := flext_quality
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell analyze

analyze: ## Analyze code quality
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run flext-quality analyze .

.DEFAULT_GOAL := help
