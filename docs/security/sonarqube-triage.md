# Triagem SonarCloud — flext-sh/flext-quality

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.16`

## Resumo

**47 issues** — BLOCKER 0, CRITICAL 18, MAJOR 8, MINOR 21
Tipos: VULNERABILITY 10, BUG 0, CODE_SMELL 37 · **Debt total: 459min**

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
| `text:S8565` | 1 |
| `python:S1854` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/core/config_manager.py:168` · **Effort**: 8min

> Define a constant instead of duplicating this literal "audit_rules.yaml" 4 times.

```python
      164  
      165      def get_audit_rules(self) -> FlextQualityConfigManager.AuditRules:
      166          """Get audit rules configuration."""
      167          if self._audit_rules is None:
>>>   168              data = self._load_config_file("audit_rules.yaml")
      169              self._audit_rules = FlextQualityConfigManager.AuditRules.model_validate(
      170                  data
      171              )
      172          return self._audit_rules
```

**Decisão**: pendente

### 2 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/core/config_manager.py:177` · **Effort**: 8min

> Define a constant instead of duplicating this literal "style_guide.yaml" 4 times.

```python
      173  
      174      def get_style_guide(self) -> FlextQualityConfigManager.StyleGuide:
      175          """Get style guide configuration."""
      176          if self._style_guide is None:
>>>   177              data = self._load_config_file("style_guide.yaml")
      178              self._style_guide = FlextQualityConfigManager.StyleGuide.model_validate(
      179                  data
      180              )
      181          return self._style_guide
```

**Decisão**: pendente

### 3 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/core/config_manager.py:186` · **Effort**: 8min

> Define a constant instead of duplicating this literal "validation_config.yaml" 4 times.

```python
      182  
      183      def get_validation_config(self) -> FlextQualityConfigManager.ValidationSettings:
      184          """Get validation configuration."""
      185          if self._validation_config is None:
>>>   186              data = self._load_config_file("validation_config.yaml")
      187              self._validation_config = (
      188                  FlextQualityConfigManager.ValidationSettings.model_validate(data)
      189              )
      190          return self._validation_config
```

**Decisão**: pendente

### 4 · 🟠 CRITICAL · VULNERABILITY · `python:S4502`
**Local**: `src/flext_quality/docs/dashboard.py:27` · **Effort**: 5min

> Make sure disabling CSRF protection is safe here.

```python
       23  
       24      def __init__(self, reports_dir: str = "docs/maintenance/reports/") -> None:
       25          """Initialize documentation dashboard with reports directory."""
       26          self.reports_dir = Path(reports_dir)
>>>    27          self.app = Flask(__name__)
       28          self._logger_instance: p.Logger = u.fetch_logger(__name__)
       29          self.setup_routes()
       30  
       31      @property
```

**Decisão**: pendente

### 5 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/dashboard.py:53` · **Effort**: 6min

> Define a constant instead of duplicating this literal "application/json" 3 times.

```python
       49              return Response(
       50                  t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.dump_json(
       51                      self.get_current_metrics()
       52                  ).decode(),
>>>    53                  mimetype="application/json",
       54              )
       55  
       56          _ = api_metrics
       57  
```

**Decisão**: pendente

### 6 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/notifications.py:93` · **Effort**: 47min

> Refactor this function to reduce its Cognitive Complexity from 57 to the 15 allowed.

```python
       89          self.results: m.Quality.NotifierResults = m.Quality.NotifierResults(
       90              timestamp=u.now().isoformat()
       91          )
       92  
>>>    93      def _load_user_config(self, loaded: t.JsonMapping) -> _NotifierConfig:
       94          cfg = self.get_default_config()
       95  
       96          channels = loaded.get("channels")
       97          if isinstance(channels, dict):
```

**Decisão**: pendente

### 7 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/notifications.py:442` · **Effort**: 9min

> Refactor this function to reduce its Cognitive Complexity from 19 to the 15 allowed.

```python
      438              webhook_config.url, json=payload, headers=headers, timeout=timeout
      439          )
      440          response.raise_for_status()
      441  
>>>   442      def _format_critical_issues_message(self, audit_data: t.JsonMapping) -> str:
      443          """Format message for critical issues notification."""
      444          metrics_val = audit_data.get("metrics")
      445          metrics: t.JsonMapping = (
      446              t.Quality.RELAXED_CONTAINER_MAPPING_ADAPTER.validate_python(metrics_val)
```

**Decisão**: pendente

### 8 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/notifications.py:582` · **Effort**: 19min

> Refactor this function to reduce its Cognitive Complexity from 29 to the 15 allowed.

```python
      578              None, description="Monthly report JSON file", validate_default=True
      579          )
      580  
      581          @override
>>>   582          def execute(self) -> p.Result[bool]:
      583              """Dispatch to the appropriate notification action."""
      584              notifier = FlextQualityDocumentationNotifier(self.settings_path)
      585              if self.test:
      586                  notifier.send_notification(
```

**Decisão**: pendente

### 9 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/audit.py:267` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
      263          ).search(content):
      264              indicators.append("potentially inconsistent status")
      265          return indicators
      266  
>>>   267      def check_content_completeness(self, doc_files: t.SequenceOf[Path]) -> None:
      268          """Check documentation completeness and identify missing sections."""
      269          min_word_count = self.audit_rules.quality_thresholds.min_word_count
      270          required_sections = self.validation_config.content_analysis.required_sections
      271          check_todos = self.validation_config.content_analysis.check_todos
```

**Decisão**: pendente

### 10 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/scripts/optimize.py:94` · **Effort**: 8min

> Define a constant instead of duplicating this literal r"^#{1,6}\\s" 4 times.

```python
       90          lines = content.split("\n")
       91          fixed_lines: MutableSequence[str] = []
       92          for i, line in enumerate(lines):
       93              if (
>>>    94                  u.Quality.compile_pattern(r"^#{1,6}\\s").match(line)
       95                  and i > 0
       96                  and lines[i - 1].strip()
       97              ):
       98                  fixed_lines.append("")
```

**Decisão**: pendente

### 11 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/scripts/optimize.py:252` · **Effort**: 6min

> Define a constant instead of duplicating this literal "[learn more](\\1)" 3 times.

```python
      248  
      249      def _improve_link_text(self, content: str) -> str:
      250          """Improve generic link text for better accessibility."""
      251          improvements = {
>>>   252              "\\[here\\]\\(([^)]+)\\)": "[learn more](\\1)",
      253              "\\[click here\\]\\(([^)]+)\\)": "[learn more](\\1)",
      254              "\\[link\\]\\(([^)]+)\\)": "[learn more](\\1)",
      255              "\\[read more\\]\\(([^)]+)\\)": "[continue reading](\\1)",
      256          }
```

**Decisão**: pendente

### 12 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/optimize.py:318` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
      314              ):
      315                  enhanced_lines.extend(("", "---", ""))
      316          return "\n".join(enhanced_lines)
      317  
>>>   318      def update_metadata(
      319          self, doc_files: t.SequenceOf[Path]
      320      ) -> m.Quality.OptimizerResults:
      321          """Update frontmatter metadata and timestamps."""
      322          for file_path in doc_files:
```

**Decisão**: pendente

### 13 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/report.py:173` · **Effort**: 24min

> Refactor this function to reduce its Cognitive Complexity from 34 to the 15 allowed.

```python
      169              return self._generate_markdown_report(report_data)
      170          msg = f"Unsupported format: {report_format}"
      171          raise ValueError(msg)
      172  
>>>   173      def _calculate_summary_metrics(
      174          self,
      175      ) -> FlextQualityDocumentationReporter.SummaryMetrics:
      176          """Calculate summary metrics from all available data."""
      177          overall_score = 0
```

**Decisão**: pendente

### 14 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/report.py:236` · **Effort**: 43min

> Refactor this function to reduce its Cognitive Complexity from 53 to the 15 allowed.

```python
      232      def _analyze_trends(self) -> FlextQualityDocumentationReporter.TrendData | None:
      233          """Analyze quality trends over time."""
      234          return None
      235  
>>>   236      def _generate_recommendations(
      237          self,
      238      ) -> MutableSequence[FlextQualityDocumentationReporter.Recommendation]:
      239          """Generate actionable recommendations based on current data."""
      240          recommendations: MutableSequence[
```

**Decisão**: pendente

### 15 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/report.py:557` · **Effort**: 22min

> Refactor this function to reduce its Cognitive Complexity from 32 to the 15 allowed.

```python
      553              str, t.Quality.DocumentationReportValue | datetime
      554          ] = {**report_data_raw, "date": report_date}
      555          return report_data_dict
      556  
>>>   557      def _analyze_trend_data(
      558          self,
      559          reports: t.SequenceOf[
      560              Mapping[str, t.Quality.DocumentationReportValue | datetime]
      561          ],
```

**Decisão**: pendente

### 16 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_quality/docs/scripts/report.py:741` · **Effort**: 6min

> Define a constant instead of duplicating this literal "report write failed" 3 times.

```python
      737                      self.filename or f"monthly_trends_{u.now().strftime('%Y%m%d')}"
      738                  )
      739                  save_result = reporter.save_report(trend_report, filename, "md")
      740                  if save_result.failure:
>>>   741                      return r[bool].fail(save_result.error or "report write failed")
      742              elif self.weekly_trends:
      743                  trend_report = reporter.generate_trend_report(days=7)
      744                  filename = (
      745                      self.filename or f"weekly_trends_{u.now().strftime('%Y%m%d')}"
```

**Decisão**: pendente

### 17 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/scripts/validate.py:275` · **Effort**: 6min

> Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.

```python
      271                  })
      272              )
      273              return max_retry_result
      274  
>>>   275          def validate_internal_links(
      276              self,
      277              links: t.SequenceOf[m.Quality.LinkRecord],
      278              doc_files: t.SequenceOf[Path],
      279          ) -> m.Quality.LinkValidatorResults:
```

**Decisão**: pendente

### 18 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_quality/docs/tools/link_checker.py:255` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
      251                  self.results.performance.slowest_response, response_time
      252              )
      253              return result
      254  
>>>   255      def check_link_sync(
      256          self, url: str, context: t.JsonMapping | None = None
      257      ) -> FlextQualityLinkChecker.LinkResult:
      258          """Check a single link synchronously (fallback method)."""
      259          start_time = time.time()
```

**Decisão**: pendente

### 19 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: pendente

### 20 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: pendente

### 21 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: pendente

### 22 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.


**Decisão**: pendente

### 23 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_quality/docs/core/config_manager.py:61` · **Effort**: 5min

> Either remove or fill this block of code.

```python
       57                      check_value = bool(self.style_checks.get(check_name, False))
       58                  case "accessibility":
       59                      check_value = bool(self.accessibility_checks.get(check_name, False))
       60                  case _:
>>>    61                      pass
       62              return check_value
       63  
       64      class StyleGuide(FlextQualityModels.Quality.StyleGuideConfig):
       65          """Configuration for style and formatting guidelines."""
```

**Decisão**: pendente

### 24 · 🟡 MAJOR · CODE_SMELL · `python:S1854`
**Local**: `src/flext_quality/docs/scripts/report.py:182` · **Effort**: 1min

> Remove this assignment to local variable 'quality_trend'; the value is never used.

```python
      178          total_issues = 0
      179          files_analyzed = 0
      180          links_checked = 0
      181          optimizations_applied = 0
>>>   182          quality_trend = "unknown"
      183  
      184          if self.audit_data and isinstance(self.audit_data, dict):
      185              metrics = self.audit_data.get("metrics")
      186              if isinstance(metrics, dict):
```

**Decisão**: pendente

### 25 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_quality/docs/scripts/validate.py:295` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      291                      link_file_dir = Path(link.file).parent
      292                      relative_target = (
      293                          link_file_dir / target[2:]
      294                          if target.startswith("./")
>>>   295                          else link_file_dir.parent / target[3:]
      296                          if target.startswith("../")
      297                          else Path(target)
      298                      )
      299                      search_root = Path(link.file).parent.parent.parent
```

**Decisão**: pendente

### 26 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_quality/docs/tools/style_validator.py:716` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      712  
      713          results = FlextQualityStyleValidator.validate_file_style(file_path, config_path)
      714  
      715          for _violation in results.violations[:3]:
>>>   716              pass
      717          return 0
      718  
      719  
      720  if __name__ == "__main__":
```

**Decisão**: pendente

### 27 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: pendente

### 28 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/core/config_manager.py:209` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      205                  self._as_config_data(raw) if raw else self._get_default_config(filename)
      206              )
      207          except FileNotFoundError:
      208              return self._get_default_config(filename)
>>>   209          except (OSError, PermissionError, UnicodeDecodeError) as exc:
      210              _ = exc
      211              return self._get_default_config(filename)
      212  
      213      def _get_default_config(
```

**Decisão**: pendente

### 29 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/notifications.py:324` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      320          # Email notification
      321          if self.config.channels.email.enabled:
      322              try:
      323                  self._send_email_notification(title, message, priority)
>>>   324              except (smtplib.SMTPException, ConnectionError, OSError) as e:
      325                  self.results.errors.append(f"Email notification failed: {e}")
      326                  success = False
      327  
      328          # Slack notification
```

**Decisão**: pendente

### 30 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/notifications.py:332` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      328          # Slack notification
      329          if self.config.channels.slack.enabled:
      330              try:
      331                  self._send_slack_notification(title, message, priority)
>>>   332              except (requests.RequestException, ConnectionError, OSError) as e:
      333                  self.results.errors.append(f"Slack notification failed: {e}")
      334                  success = False
      335  
      336          # Webhook notification
```

**Decisão**: pendente

### 31 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/notifications.py:332` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      328          # Slack notification
      329          if self.config.channels.slack.enabled:
      330              try:
      331                  self._send_slack_notification(title, message, priority)
>>>   332              except (requests.RequestException, ConnectionError, OSError) as e:
      333                  self.results.errors.append(f"Slack notification failed: {e}")
      334                  success = False
      335  
      336          # Webhook notification
```

**Decisão**: pendente

### 32 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/notifications.py:340` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      336          # Webhook notification
      337          if self.config.channels.webhook.enabled:
      338              try:
      339                  self._send_webhook_notification(title, message, priority)
>>>   340              except (requests.RequestException, ConnectionError, OSError) as e:
      341                  self.results.errors.append(f"Webhook notification failed: {e}")
      342                  success = False
      343  
      344          if success:
```

**Decisão**: pendente

### 33 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/notifications.py:340` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      336          # Webhook notification
      337          if self.config.channels.webhook.enabled:
      338              try:
      339                  self._send_webhook_notification(title, message, priority)
>>>   340              except (requests.RequestException, ConnectionError, OSError) as e:
      341                  self.results.errors.append(f"Webhook notification failed: {e}")
      342                  success = False
      343  
      344          if success:
```

**Decisão**: pendente

### 34 · ⚪ MINOR · CODE_SMELL · `python:S7500`
**Local**: `src/flext_quality/docs/notifications.py:362` · **Effort**: 5min

> Replace this comprehension with passing the iterable to the collection constructor call

```python
      358          email_config = self.config.email
      359  
      360          msg = MIMEMultipart()
      361          msg["From"] = email_config.from_address
>>>   362          msg["To"] = ", ".join(x for x in (email_config.to_addresses or []))
      363          msg["Subject"] = f"[{priority.upper()}] {title}"
      364  
      365          body = f"""
      366  FLEXT Quality Documentation Alert
```

**Decisão**: pendente

### 35 · ⚪ MINOR · VULNERABILITY · `python:S5332`
**Local**: `src/flext_quality/docs/scripts/audit.py:488` · **Effort**: 30min

> Using HTTP protocol is insecure. Use HTTPS instead.

```python
      484              internal_links = u.Quality.compile_pattern(
      485                  r"\\[([^\\]]+)\\]\\(([^)]+)\\)"
      486              ).findall(content)
      487              for text, link in internal_links:
>>>   488                  if not link.startswith(("http://", "https://", "#", "mailto:")):
      489                      all_links.append({
      490                          "url": link,
      491                          "text": text,
      492                          "file": str(file_path.relative_to(self.project_root)),
```

**Decisão**: pendente

### 36 · ⚪ MINOR · VULNERABILITY · `python:S5332`
**Local**: `src/flext_quality/docs/scripts/audit.py:571` · **Effort**: 30min

> Using HTTP protocol is insecure. Use HTTPS instead.

```python
      567  
      568      def _validate_images(self, images: t.SequenceOf[t.StrMapping]) -> None:
      569          """Validate image references."""
      570          for image in images:
>>>   571              if image["src"].startswith(("http://", "https://")):
      572                  continue
      573              image_path = Path(image["src"])
      574              if not image_path.is_absolute():
      575                  file_dir = Path(image["file"]).parent
```

**Decisão**: pendente

### 37 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/scripts/audit.py:852` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      848                  metrics = results.metrics
      849                  if self._should_fail(metrics):
      850                      return r[bool].fail("Audit failed quality threshold")
      851              except (
>>>   852                  FileNotFoundError,
      853                  PermissionError,
      854                  OSError,
      855                  KeyError,
      856                  ValueError,
```

**Decisão**: pendente

### 38 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/scripts/audit.py:853` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      849                  if self._should_fail(metrics):
      850                      return r[bool].fail("Audit failed quality threshold")
      851              except (
      852                  FileNotFoundError,
>>>   853                  PermissionError,
      854                  OSError,
      855                  KeyError,
      856                  ValueError,
      857              ) as exc:
```

**Decisão**: pendente

### 39 · ⚪ MINOR · VULNERABILITY · `python:S5332`
**Local**: `src/flext_quality/docs/scripts/validate.py:128` · **Effort**: 30min

> Using HTTP protocol is insecure. Use HTTPS instead.

```python
      124              # NOTE (multi-agent, mro-f8vk / kimi): match-with-guards was
      125              # non-exhaustive by construction (reportMatchNotExhaustive); the
      126              # if-chain keeps identical first-match semantics and an explicit
      127              # default without a dummy `case _: pass`.
>>>   128              if url.startswith(("http://", "https://")):
      129                  return "external"
      130              if url.startswith("mailto:"):
      131                  return "email"
      132              if url.startswith("#"):
```

**Decisão**: pendente

### 40 · ⚪ MINOR · VULNERABILITY · `python:S5332`
**Local**: `src/flext_quality/docs/scripts/validate.py:334` · **Effort**: 30min

> Using HTTP protocol is insecure. Use HTTPS instead.

```python
      330              """Validate image references."""
      331              images = [link for link in links if link.type == "image"]
      332              for image in images:
      333                  src = image.url
>>>   334                  if src.startswith(("http://", "https://")):
      335                      self.results.valid_links += 1
      336                      continue
      337                  image_path = Path(src)
      338                  if not image_path.is_absolute():
```

**Decisão**: pendente

### 41 · ⚪ MINOR · VULNERABILITY · `python:S5332`
**Local**: `src/flext_quality/docs/tools/link_checker.py:176` · **Effort**: 30min

> Using HTTP protocol is insecure. Use HTTPS instead.

```python
      172          return all_links
      173  
      174      def _classify_link(self, url: str) -> str:
      175          """Classify link type based on URL."""
>>>   176          if url.startswith(("http://", "https://")):
      177              return "external"
      178          if url.startswith("#"):
      179              return "anchor"
      180          if url.startswith(("mailto:", "tel:")):
```

**Decisão**: pendente

### 42 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/tools/link_checker.py:409` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      405              try:
      406                  async with ClientSession() as session:
      407                      self.session = session
      408                      results = await self.check_links_batch_async(links)
>>>   409              except (OSError, ClientError, TimeoutError, RuntimeError):
      410                  results = self.check_links_batch_sync(links)
      411          else:
      412              results = self.check_links_batch_sync(links)
      413  
```

**Decisão**: pendente

### 43 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/tools/link_checker.py:441` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      437              rp.set_url(f"https://{domain}/robots.txt")
      438              rp.read()
      439  
      440              return rp.can_fetch(self.settings.user_agent, "/")
>>>   441          except (OSError, ConnectionError, TimeoutError, UnicodeDecodeError):
      442              # If robots.txt can't be read, assume crawling is allowed
      443              return True
      444  
      445      def validate_github_links(
```

**Decisão**: pendente

### 44 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/tools/link_checker.py:441` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      437              rp.set_url(f"https://{domain}/robots.txt")
      438              rp.read()
      439  
      440              return rp.can_fetch(self.settings.user_agent, "/")
>>>   441          except (OSError, ConnectionError, TimeoutError, UnicodeDecodeError):
      442              # If robots.txt can't be read, assume crawling is allowed
      443              return True
      444  
      445      def validate_github_links(
```

**Decisão**: pendente

### 45 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_quality/docs/tools/style_validator.py:146` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
      142              if loaded_obj:
      143                  self.settings = self._normalize_config(loaded_obj)
      144              else:
      145                  self._set_default_config()
>>>   146          except (FileNotFoundError, KeyError, OSError):
      147              self._set_default_config()
      148  
      149      def _normalize_config(
      150          self, raw: t.JsonMapping
```

**Decisão**: pendente

### 46 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_quality/models.py:35` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       31              return []
       32  
       33          @staticmethod
       34          def _empty_dict_str_str() -> t.StrMapping:
>>>    35              return dict[str, str]()
       36  
       37          @staticmethod
       38          def _empty_list_dict_str_str() -> MutableSequence[t.MutableStrMapping]:
       39              return []
```

**Decisão**: pendente

### 47 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_quality/rules/validators.py:17` · **Effort**: 2min

> Rename this field "Base" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       13  
       14  class FlextQualityValidators:
       15      """Namespace for flext-quality validators (one class per module pattern)."""
       16  
>>>    17      Base = p.Quality.ValidatorBase
       18  
       19      class Pattern(p.Quality.ValidatorBase):
       20          """Validates content against regex patterns."""
       21  
```

**Decisão**: pendente
