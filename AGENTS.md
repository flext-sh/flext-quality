# AGENTS.md — flext-quality

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_quality` · deps: `flext-api`, `flext-cli`, `flext-core`, `flext-infra`, `flext-web`

## Overview

Unified orchestration platform for Claude Code / agent tooling and quality workflows. One of the few packages that legitimately depends on `flext-infra`.

## Structure

```text
src/flext_quality/
├── api.py cli.py __main__.py   # FlextQuality facade + command surface (Check / Validate)
├── mcp/                        # MCP tools (search_code, execute_hook)
├── hooks/                      # hook manager (register / configure / execute)
├── integrations/               # external tool integrations
├── rules/                      # quality rules
├── docs/                       # tools, scripts, core docs
├── services/
└── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextQuality` | class | `api.py` | facade: `execute_hook`, `load_rules` |
| `FlextQualityMcpTools` | class | `mcp/tools.py` | `search_code`, `execute_hook` |
| `FlextQualityHookManager` | class | `hooks/manager.py` | hook registration/config/execution |

## Conventions (specific to this package)

- MCP tools and hook execution are first-class orchestration paths.
- CLI `Check` / `Validate` assemble Ruff, basedpyright, Bandit, pytest, and coverage commands.

## Commands

```bash
make check PROJECT=flext-quality
make test  PROJECT=flext-quality       # tests/{unit,helpers}
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
