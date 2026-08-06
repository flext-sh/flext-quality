# Triagem SonarCloud — flext-sh/flext-quality

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.16`

## Resumo

**47 issues** — BLOCKER 0, CRITICAL 18, MAJOR 8, MINOR 21
Tipos: VULNERABILITY 10, BUG 0, CODE_SMELL 37

| regra | issues |
|---|---|
| `python:S5713` | 12 |
| `python:S3776` | 10 |
| `python:S1192` | 7 |
| `python:S5332` | 5 |
| `githubactions:S8233` | 2 |
| `python:S108` | 2 |
| `python:S4502` | 1 |
| `githubactions:S8264` | 1 |

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/core/config_manager.py` | 168 | |
| 2 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/core/config_manager.py` | 177 | |
| 3 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/core/config_manager.py` | 186 | |
| 4 | CRITICAL | VULNERABILITY | `python:S4502` | `src/flext_quality/docs/dashboard.py` | 27 | |
| 5 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/dashboard.py` | 53 | |
| 6 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/notifications.py` | 93 | |
| 7 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/notifications.py` | 442 | |
| 8 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/notifications.py` | 582 | |
| 9 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/audit.py` | 267 | |
| 10 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/scripts/optimize.py` | 94 | |
| 11 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/scripts/optimize.py` | 252 | |
| 12 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/optimize.py` | 318 | |
| 13 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/report.py` | 173 | |
| 14 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/report.py` | 236 | |
| 15 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/report.py` | 557 | |
| 16 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_quality/docs/scripts/report.py` | 741 | |
| 17 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/scripts/validate.py` | 275 | |
| 18 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_quality/docs/tools/link_checker.py` | 255 | |
| 19 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 20 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 21 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 22 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 23 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_quality/docs/core/config_manager.py` | 61 | |
| 24 | MAJOR | CODE_SMELL | `python:S1854` | `src/flext_quality/docs/scripts/report.py` | 182 | |
| 25 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_quality/docs/scripts/validate.py` | 295 | |
| 26 | MAJOR | CODE_SMELL | `python:S108` | `src/flext_quality/docs/tools/style_validator.py` | 716 | |
| 27 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 28 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/core/config_manager.py` | 209 | |
| 29 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/notifications.py` | 324 | |
| 30 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/notifications.py` | 332 | |
| 31 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/notifications.py` | 332 | |
| 32 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/notifications.py` | 340 | |
| 33 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/notifications.py` | 340 | |
| 34 | MINOR | CODE_SMELL | `python:S7500` | `src/flext_quality/docs/notifications.py` | 362 | |
| 35 | MINOR | VULNERABILITY | `python:S5332` | `src/flext_quality/docs/scripts/audit.py` | 488 | |
| 36 | MINOR | VULNERABILITY | `python:S5332` | `src/flext_quality/docs/scripts/audit.py` | 571 | |
| 37 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/scripts/audit.py` | 852 | |
| 38 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/scripts/audit.py` | 853 | |
| 39 | MINOR | VULNERABILITY | `python:S5332` | `src/flext_quality/docs/scripts/validate.py` | 128 | |
| 40 | MINOR | VULNERABILITY | `python:S5332` | `src/flext_quality/docs/scripts/validate.py` | 334 | |
| 41 | MINOR | VULNERABILITY | `python:S5332` | `src/flext_quality/docs/tools/link_checker.py` | 176 | |
| 42 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/tools/link_checker.py` | 409 | |
| 43 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/tools/link_checker.py` | 441 | |
| 44 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/tools/link_checker.py` | 441 | |
| 45 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_quality/docs/tools/style_validator.py` | 146 | |
| 46 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_quality/models.py` | 35 | |
| 47 | MINOR | CODE_SMELL | `python:S116` | `src/flext_quality/rules/validators.py` | 17 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-quality.json`

