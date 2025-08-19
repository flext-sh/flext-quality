# FLEXT Quality Integration Guide

This guide covers how to integrate FLEXT Quality with other systems, services, and development workflows. Learn how to embed quality analysis into your existing development processes and connect with the broader FLEXT ecosystem.

## Overview

FLEXT Quality provides multiple integration points:

- **FLEXT Ecosystem Integration** - Native integration with other FLEXT services
- **CI/CD Pipeline Integration** - Quality gates in continuous integration
- **IDE Integration** - Real-time quality feedback in development environments
- **Monitoring Integration** - Quality metrics in observability platforms
- **External Service Integration** - GitHub, GitLab, Slack, and more

## FLEXT Ecosystem Integration

### flext-core Integration

FLEXT Quality is built on flext-core foundation patterns:

```python
from flext_core import FlextEntity, FlextResult, FlextContainer
from flext_quality.domain.entities import QualityProject

# All domain entities extend FlextEntity
class QualityProject(FlextEntity):
    """Quality project following flext-core patterns."""

    def validate_standards(self) -> FlextResult[bool]:
        """Validate project standards using FlextResult pattern."""
        if not self.project_path:
            return FlextResult[None].fail("Project path is required")
        return FlextResult[None].ok(True)

# Services return FlextResult for consistent error handling
async def analyze_project(project_id: str) -> FlextResult[QualityAnalysis]:
    """Analyze project with standard error handling."""
    try:
        result = await quality_service.analyze_project(project_id)
        return result
    except Exception as e:
        return FlextResult[None].fail(f"Analysis failed: {e}")
```

### flext-observability Integration

Quality metrics automatically flow to the FLEXT observability platform:

```python
from flext_observability import flext_create_metric, flext_create_trace

# Quality metrics sent to central monitoring
@flext_create_trace("quality_analysis")
async def analyze_project_with_monitoring(project: QualityProject):
    """Analyze project with distributed tracing."""

    # Analysis execution automatically traced
    analysis = await run_quality_analysis(project)

    # Send quality metrics to observability platform
    flext_create_metric(
        name="quality_score",
        value=analysis.overall_score,
        tags={
            "project": project.name,
            "ecosystem": "flext",
            "project_type": project.project_type
        }
    )

    flext_create_metric(
        name="quality_issues",
        value=analysis.total_issues,
        tags={
            "project": project.name,
            "severity": "all"
        }
    )

    return analysis
```

### flext-web Integration

Quality dashboards integrate with the main FLEXT web interface:

```javascript
// FLEXT web dashboard integration
const qualityWidget = {
  name: "ecosystem-quality",
  component: "QualityDashboardWidget",
  config: {
    endpoint: "http://flext-quality:8000/api/v1/metrics/ecosystem",
    refreshInterval: 300000, // 5 minutes
    metrics: ["overall_score", "projects_meeting_standards", "issue_trends"],
  },
};

// Register widget with flext-web
await flextWeb.widgets.register(qualityWidget);
```

### flext-cli Integration

Quality commands available through the main FLEXT CLI:

```bash
# Quality analysis via flext-cli
flext quality analyze --project flext-core
flext quality report --project flext-api --format executive
flext quality dashboard --ecosystem --open

# Workspace-wide quality operations
flext quality workspace-analyze
flext quality workspace-report
flext quality set-standards --coverage 90 --complexity 10
```

Configuration in flext-cli:

```yaml
# ~/.flext/config.yml
quality:
  service_url: "http://flext-quality:8000"
  default_standards:
    min_coverage: 90.0
    max_complexity: 10
    security_enabled: true
  auto_analyze: true
  report_format: "executive"
```

### flext-api Integration

Quality endpoints exposed through the main FLEXT API:

```python
# flext-api router integration
from flext_api.routers import APIRouter
from flext_quality.presentation.api import quality_router

# Include quality routes in main API
api_router = APIRouter()
api_router.include_router(
    quality_router,
    prefix="/quality",
    tags=["quality"]
)

# Quality endpoints available at:
# GET /api/v1/quality/projects
# POST /api/v1/quality/projects/{id}/analyze
# GET /api/v1/quality/ecosystem/metrics
```

## CI/CD Pipeline Integration

### GitHub Actions Integration

`.github/workflows/quality.yml`:

```yaml
name: FLEXT Quality Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup FLEXT Quality
        uses: flext-sh/quality-action@v1
        with:
          flext-quality-url: ${{ secrets.FLEXT_QUALITY_URL }}
          api-key: ${{ secrets.FLEXT_QUALITY_API_KEY }}

      - name: Run Quality Analysis
        id: quality
        run: |
          # Start analysis
          ANALYSIS_ID=$(flext-quality analyze \
            --project-path . \
            --branch ${{ github.ref_name }} \
            --commit ${{ github.sha }} \
            --pr ${{ github.event.pull_request.number }} \
            --output json | jq -r '.analysis_id')

          # Wait for completion
          flext-quality wait $ANALYSIS_ID --timeout 600

          # Get results
          RESULTS=$(flext-quality results $ANALYSIS_ID --format json)
          SCORE=$(echo $RESULTS | jq -r '.quality_score')
          GRADE=$(echo $RESULTS | jq -r '.quality_grade')

          echo "score=$SCORE" >> $GITHUB_OUTPUT
          echo "grade=$GRADE" >> $GITHUB_OUTPUT

      - name: Quality Gate
        run: |
          if (( $(echo "${{ steps.quality.outputs.score }} < 80" | bc -l) )); then
            echo "Quality gate failed: Score ${{ steps.quality.outputs.score }} < 80"
            exit 1
          fi
          echo "Quality gate passed: Score ${{ steps.quality.outputs.score }}"

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📊 FLEXT Quality Report
              
              **Quality Score:** ${{ steps.quality.outputs.score }}/100
              **Grade:** ${{ steps.quality.outputs.grade }}
              
              [View Full Report](${process.env.FLEXT_QUALITY_URL}/analyses/${analysisId})
              `
            });
```

### GitLab CI Integration

`.gitlab-ci.yml`:

```yaml
stages:
  - quality
  - deploy

variables:
  FLEXT_QUALITY_URL: "https://quality.flext.sh"

quality_analysis:
  stage: quality
  image: flext/quality-cli:latest
  services:
    - postgres:15
    - redis:7

  variables:
    POSTGRES_HOST: postgres
    REDIS_URL: redis://redis:6379/0

  script:
    - flext-quality configure --url $FLEXT_QUALITY_URL --token $FLEXT_QUALITY_TOKEN
    - |
      ANALYSIS_ID=$(flext-quality analyze \
        --project-path . \
        --branch $CI_COMMIT_REF_NAME \
        --commit $CI_COMMIT_SHA \
        --mr $CI_MERGE_REQUEST_IID \
        --output json | jq -r '.analysis_id')

    - flext-quality wait $ANALYSIS_ID --timeout 600
    - flext-quality results $ANALYSIS_ID --format junit > quality-report.xml
    - |
      SCORE=$(flext-quality results $ANALYSIS_ID --format json | jq -r '.quality_score')
      if (( $(echo "$SCORE < 80" | bc -l) )); then
        echo "Quality gate failed: Score $SCORE < 80"
        exit 1
      fi

  artifacts:
    reports:
      junit: quality-report.xml
    paths:
      - quality-report.xml

  only:
    - merge_requests
    - main
    - develop
```

### Jenkins Pipeline Integration

```groovy
pipeline {
    agent any

    environment {
        FLEXT_QUALITY_URL = 'https://quality.flext.sh'
        FLEXT_QUALITY_TOKEN = credentials('flext-quality-token')
    }

    stages {
        stage('Quality Analysis') {
            steps {
                script {
                    // Start analysis
                    def analysisResult = sh(
                        script: """
                            flext-quality analyze \
                                --project-path . \
                                --branch ${env.BRANCH_NAME} \
                                --commit ${env.GIT_COMMIT} \
                                --output json
                        """,
                        returnStdout: true
                    ).trim()

                    def analysis = readJSON text: analysisResult
                    def analysisId = analysis.analysis_id

                    // Wait for completion
                    sh "flext-quality wait ${analysisId} --timeout 600"

                    // Get results
                    def resultsJson = sh(
                        script: "flext-quality results ${analysisId} --format json",
                        returnStdout: true
                    ).trim()

                    def results = readJSON text: resultsJson

                    // Quality gate
                    if (results.quality_score < 80) {
                        error("Quality gate failed: Score ${results.quality_score} < 80")
                    }

                    // Store results
                    env.QUALITY_SCORE = results.quality_score
                    env.QUALITY_GRADE = results.quality_grade
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
                expression { env.QUALITY_SCORE.toFloat() >= 80 }
            }
            steps {
                echo "Deploying with quality score: ${env.QUALITY_SCORE}"
                // Deployment steps
            }
        }
    }

    post {
        always {
            // Archive quality reports
            archiveArtifacts artifacts: 'quality-report.*', allowEmptyArchive: true
        }

        failure {
            // Notify on quality gate failure
            emailext (
                subject: "Quality Gate Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Quality score: ${env.QUALITY_SCORE}\nGrade: ${env.QUALITY_GRADE}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

## IDE Integration

### VS Code Extension

Install the FLEXT Quality VS Code extension:

```json
// .vscode/settings.json
{
  "flext-quality.enabled": true,
  "flext-quality.server.url": "http://localhost:8000",
  "flext-quality.analysis.autorun": true,
  "flext-quality.analysis.onSave": true,
  "flext-quality.standards.minCoverage": 90,
  "flext-quality.standards.maxComplexity": 10,
  "flext-quality.notifications.enabled": true
}
```

Extension features:

- Real-time quality analysis
- Inline issue highlighting
- Quality metrics in status bar
- Quality reports in sidebar
- Integration with VS Code problems panel

### PyCharm Plugin

Install the FLEXT Quality PyCharm plugin:

```xml
<!-- .idea/flext-quality.xml -->
<component name="FlextQualitySettings">
  <option name="serverUrl" value="http://localhost:8000" />
  <option name="autoAnalysis" value="true" />
  <option name="showInlineIssues" value="true" />
  <option name="qualityThreshold" value="80.0" />
</component>
```

### Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: flext-quality
        name: FLEXT Quality Analysis
        entry: flext-quality
        args: ["analyze-staged", "--threshold", "80", "--fail-on-regression"]
        language: system
        types: [python]
        pass_filenames: false
```

## Monitoring Integration

### Prometheus Integration

FLEXT Quality exposes Prometheus metrics:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: "flext-quality"
    static_configs:
      - targets: ["flext-quality:8000"]
    metrics_path: "/metrics"
    scrape_interval: 30s
```

Available metrics:

```
# Quality scores
flext_quality_score{project="flext-core", type="overall"} 92.5
flext_quality_score{project="flext-core", type="coverage"} 94.2
flext_quality_score{project="flext-core", type="security"} 98.5

# Analysis metrics
flext_quality_analyses_total{status="completed"} 1250
flext_quality_analyses_total{status="failed"} 15
flext_quality_analysis_duration_seconds{project="flext-core"} 180.5

# Issue metrics
flext_quality_issues_total{severity="critical", project="flext-core"} 0
flext_quality_issues_total{severity="high", project="flext-core"} 3
flext_quality_issues_total{severity="medium", project="flext-core"} 12
```

### Grafana Dashboard

Import the FLEXT Quality Grafana dashboard:

```json
{
  "dashboard": {
    "title": "FLEXT Quality Metrics",
    "panels": [
      {
        "title": "Ecosystem Quality Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(flext_quality_score{type=\"overall\"})",
            "legendFormat": "Average Quality Score"
          }
        ]
      },
      {
        "title": "Quality Score Trends",
        "type": "graph",
        "targets": [
          {
            "expr": "flext_quality_score{type=\"overall\"}",
            "legendFormat": "{{project}}"
          }
        ]
      },
      {
        "title": "Issue Distribution",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum by (severity) (flext_quality_issues_total)",
            "legendFormat": "{{severity}}"
          }
        ]
      }
    ]
  }
}
```

### DataDog Integration

```python
# DataDog metrics integration
from datadog import initialize, statsd
from flext_quality.domain.events import QualityAnalysisCompleted

initialize(
    api_key=os.getenv('DATADOG_API_KEY'),
    app_key=os.getenv('DATADOG_APP_KEY')
)

@event_handler(QualityAnalysisCompleted)
async def send_quality_metrics_to_datadog(event: QualityAnalysisCompleted):
    """Send quality metrics to DataDog."""

    # Quality score gauge
    statsd.gauge(
        'flext.quality.score',
        event.analysis.overall_score,
        tags=[
            f'project:{event.analysis.project_id}',
            f'grade:{event.analysis.quality_grade}',
            'ecosystem:flext'
        ]
    )

    # Issue counts
    for severity, count in event.analysis.issue_counts.items():
        statsd.gauge(
            'flext.quality.issues',
            count,
            tags=[
                f'project:{event.analysis.project_id}',
                f'severity:{severity}',
                'ecosystem:flext'
            ]
        )
```

## External Service Integration

### GitHub Integration

Integrate quality analysis with GitHub workflows:

```python
# GitHub webhook handler
@app.post("/webhooks/github")
async def github_webhook(request: Request):
    """Handle GitHub webhook events."""

    payload = await request.json()
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'pull_request':
        if payload['action'] in ['opened', 'synchronize']:
            # Start quality analysis for PR
            await start_pr_analysis(
                repo=payload['repository']['full_name'],
                pr_number=payload['pull_request']['number'],
                commit_sha=payload['pull_request']['head']['sha']
            )

    elif event_type == 'push':
        if payload['ref'] == 'refs/heads/main':
            # Start quality analysis for main branch
            await start_branch_analysis(
                repo=payload['repository']['full_name'],
                branch='main',
                commit_sha=payload['after']
            )

    return {"status": "ok"}

async def start_pr_analysis(repo: str, pr_number: int, commit_sha: str):
    """Start quality analysis for pull request."""

    # Create temporary project for PR analysis
    project = await quality_service.create_pr_project(
        repository=repo,
        pr_number=pr_number,
        commit_sha=commit_sha
    )

    # Start analysis
    analysis = await quality_service.analyze_project(project.id)

    # Post results to GitHub
    await post_github_pr_comment(
        repo=repo,
        pr_number=pr_number,
        analysis_id=analysis.id
    )
```

### Slack Integration

Send quality notifications to Slack:

```python
from slack_sdk import WebClient
from flext_quality.domain.events import QualityGateFailure

slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

@event_handler(QualityGateFailure)
async def notify_quality_gate_failure(event: QualityGateFailure):
    """Send Slack notification for quality gate failures."""

    message = {
        "channel": "#quality-alerts",
        "text": f"🚨 Quality Gate Failed: {event.project_name}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Quality Gate Failed*\n"
                           f"Project: {event.project_name}\n"
                           f"Score: {event.quality_score}/100\n"
                           f"Threshold: {event.threshold}/100"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View Report"},
                        "url": f"{BASE_URL}/analyses/{event.analysis_id}"
                    }
                ]
            }
        ]
    }

    await slack_client.chat_postMessage(**message)
```

### Jira Integration

Create Jira issues for quality violations:

```python
from jira import JIRA
from flext_quality.domain.events import CriticalIssueDetected

jira_client = JIRA(
    server=os.getenv('JIRA_SERVER'),
    basic_auth=(
        os.getenv('JIRA_USERNAME'),
        os.getenv('JIRA_API_TOKEN')
    )
)

@event_handler(CriticalIssueDetected)
async def create_jira_issue_for_critical_quality_issue(event: CriticalIssueDetected):
    """Create Jira issue for critical quality violations."""

    issue_dict = {
        'project': {'key': 'QUALITY'},
        'summary': f'Critical Quality Issue: {event.issue.rule_name}',
        'description': f"""
Critical quality issue detected in {event.project_name}:

*File:* {event.issue.file_path}:{event.issue.line_number}
*Rule:* {event.issue.rule_id} - {event.issue.rule_name}
*Message:* {event.issue.message}

*Code Snippet:*
{{code}}
{event.issue.code_snippet}
{{code}}

*Recommendation:* {event.issue.suggestion}

*Analysis Report:* {BASE_URL}/analyses/{event.analysis_id}
        """,
        'issuetype': {'name': 'Bug'},
        'priority': {'name': 'High'},
        'labels': ['quality', 'critical', event.project_name.lower()],
        'components': [{'name': 'Code Quality'}]
    }

    new_issue = jira_client.create_issue(fields=issue_dict)

    # Link to quality analysis
    jira_client.create_issue_link(
        type="relates to",
        inwardIssue=new_issue.key,
        outwardIssue=f"QUALITY-{event.analysis_id}"
    )
```

## Configuration Management

### Environment-Specific Configuration

```yaml
# config/development.yml
quality:
  thresholds:
    min_coverage: 85.0  # Lower for development
    max_complexity: 15   # Higher for development
  integrations:
    github:
      enabled: true
      post_comments: true
    slack:
      enabled: true
      channel: "#dev-quality"

# config/production.yml
quality:
  thresholds:
    min_coverage: 95.0  # Strict for production
    max_complexity: 8    # Lower for production
  integrations:
    github:
      enabled: true
      post_comments: true
      create_issues: true
    slack:
      enabled: true
      channel: "#quality-alerts"
    jira:
      enabled: true
      create_issues: true
```

### Integration Testing

Test your integrations with comprehensive test suites:

```python
import pytest
from unittest.mock import Mock, patch
from flext_quality.integrations.github import GitHubIntegration

class TestGitHubIntegration:

    @pytest.fixture
    def github_integration(self):
        return GitHubIntegration(
            token="test-token",
            base_url="https://api.github.com"
        )

    @patch('requests.post')
    async def test_post_pr_comment(self, mock_post, github_integration):
        """Test posting PR comment to GitHub."""

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 123}

        result = await github_integration.post_pr_comment(
            repo="flext-sh/flext-core",
            pr_number=42,
            comment="Quality analysis completed"
        )

        assert result.success
        mock_post.assert_called_once()
```

## Next Steps

- **[CI/CD Integration Details](cicd.md)** - Detailed CI/CD pipeline setup
- **[IDE Integration Guide](ide.md)** - Development environment integration
- **[Monitoring Setup](monitoring.md)** - Comprehensive monitoring configuration
- **[API Documentation](../api/README.md)** - API integration reference
