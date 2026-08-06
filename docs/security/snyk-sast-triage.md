# Triagem Snyk Code (SAST) — flext-sh/flext-quality

Gerado do scan Snyk (dump 2026-08-06). Bead: `mro-6oyz`

## Resumo

**1 achados** — critical 0, high 0, medium 1, low 0

| categoria | achados |
|---|---|
| Jinja auto-escape is set to false. | 1 |

## Como usar este documento

Cada achado traz o **código real** extraído da worktree (linha `>>>` = sink reportado), a regra completa e o CWE.
Preencha **Decisão**: `corrigir` / `falso-positivo` (registrar em `.snyk`) / `risco-aceito` (com prazo).

## Achados

### 1 · 🟡 MEDIUM · Jinja auto-escape is set to false.
**Local**: `src/flext_quality/docs/scripts/report.py:385` · **CWE**: -

```python
      381  
      382      def _get_html_template(self) -> Template:
      383          """Get HTML report template."""
      384          template_content = '\n<!DOCTYPE html>\n<html>\n<head>\n    <title>{{ title }}</title>\n    <style>\n        body { font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }\n        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }\n        .header { text-align: center; border-bottom: 2px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }\n        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }\n        .metric-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007acc; }\n        .metric-value { font-size: 2.5em; font-weight: bold; color: #007acc; margin: 10px 0; }\n        .metric-label { color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }\n        .section { margin: 40px 0; }\n        .section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }\n        .recommendations { display: grid; gap: 15px; }\n        .recommendation { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; }\n        .priority-critical { border-left: 4px solid #dc3545; background: #f8d7da; }\n        .priority-high { border-left: 4px solid #fd7e14; background: #fff3cd; }\n        .priority-medium { border-left: 4px solid #ffc107; background: #fff3cd; }\n        .priority-low { border-left: 4px solid #28a745; background: #d4edda; }\n        .issue-list { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto; }\n        .issue-item { background: white; margin: 5px 0; padding: 8px; border-radius: 3px; border-left: 3px solid #dc3545; }\n        .timestamp { color: #666; font-size: 0.9em; text-align: center; margin-top: 30px; }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="header">\n            <h1>{{ title }}</h1>\n            <p>Generated: {{ timestamp }}</p>\n        </div>\n\n        <div class="summary-grid">\n            <div class="metric-card">\n                <div class="metric-label">Overall Quality Score</div>\n                <div class="metric-value">{{ summary.overall_score }}%</div>\n                <div>Trend: {{ summary.quality_trend|title }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Files Analyzed</div>\n                <div class="metric-value">{{ summary.files_analyzed }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Total Issues</div>\n                <div class="metric-value">{{ summary.total_issues }}</div>\n            </div>\n            <div class="metric-card">\n                <div class="metric-label">Links Checked</div>\n                <div class="metric-value">{{ summary.links_checked }}</div>\n            </div>\n        </div>\n\n        {% if audit_summary %}\n        <div class="section">\n            <h2>Content Audit Results</h2>\n            <p>Quality Score: {{ audit_summary.quality_score }}%</p>\n            <p>Issues Found: {{ audit_summary.total_issues }}</p>\n            <p>Critical: {{ audit_summary.critical_issues }}, High: {{ audit_summary.high_issues }}</p>\n        </div>\n        {% endif %}\n\n        {% if validation_summary %}\n        <div class="section">\n            <h2>Link Validation Results</h2>\n            <p>Links Checked: {{ validation_summary.links_checked }}</p>\n            <p>Valid: {{ validation_summary.valid_links }}, Broken: {{ validation_summary.broken_links }}</p>\n        </div>\n        {% endif %}\n\n        {% if optimization_summary %}\n        <div class="section">\n            <h2>Optimization Results</h2>\n            <p>Files Processed: {{ optimization_summary.files_processed }}</p>\n            <p>Changes Made: {{ optimization_summary.changes_made }}</p>\n            <p>Backups Created: {{ optimization_summary.backups_created }}</p>\n        </div>\n        {% endif %}\n\n        <div class="section">\n            <h2>Recommendations</h2>\n            <div class="recommendations">\n                {% for rec in recommendations %}\n                <div class="recommendation priority-{{ rec.priority }}">\n                    <h3>{{ rec.title }}</h3>\n                    <p>{{ rec.description }}</p>\n                    <ul>\n                        {% for action in rec.actions %}\n                        <li>{{ action }}</li>\n                        {% endfor %}\n                    </ul>\n                </div>\n                {% endfor %}\n            </div>\n        </div>\n\n        <div class="timestamp">\n            Report generated by FLEXT Quality Documentation Maintenance System\n        </div>\n    </div>\n</body>\n</html>\n        '
>>>   385          return Template(template_content)
      386  
      387      def _generate_markdown_report(
      388          self, data: FlextQualityDocumentationReporter.ReportData
      389      ) -> str:
```

**Decisão**: 

