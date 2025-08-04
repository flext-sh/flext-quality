# FLEXT Quality API Documentation

This document provides comprehensive API documentation for FLEXT Quality, including REST endpoints, authentication, request/response formats, and integration examples.

## API Overview

FLEXT Quality provides multiple API interfaces:

- **REST API** - Primary HTTP API for external integrations
- **GraphQL API** - Flexible query interface for complex data retrieval
- **Python SDK** - Native Python client library
- **Webhook API** - Event-driven notifications

### Base URLs

```bash
# Local Development
http://localhost:8000/api/v1

# Staging
https://staging-quality.flext.sh/api/v1

# Production
https://quality.flext.sh/api/v1
```

### API Versioning

- **Current Version**: `v1`
- **Version Header**: `X-API-Version: v1`
- **URL Versioning**: `/api/v1/`

## Authentication

### API Key Authentication

```bash
# Header-based authentication
curl -H "Authorization: Bearer your-api-key" \
     https://quality.flext.sh/api/v1/projects
```

### OAuth 2.0 Authentication

```bash
# Get access token
curl -X POST https://quality.flext.sh/oauth/token \
     -H "Content-Type: application/json" \
     -d '{
       "grant_type": "client_credentials",
       "client_id": "your-client-id",
       "client_secret": "your-client-secret"
     }'

# Use access token
curl -H "Authorization: Bearer access-token" \
     https://quality.flext.sh/api/v1/projects
```

### FLEXT Ecosystem Authentication

```bash
# Service-to-service authentication
curl -H "X-FLEXT-Service: flext-web" \
     -H "X-FLEXT-Token: service-token" \
     https://quality.flext.sh/api/v1/metrics/ecosystem
```

## REST API Endpoints

### Projects API

#### List Projects

```http
GET /api/v1/projects
```

**Parameters:**

- `limit` (int, optional): Number of results (default: 20, max: 100)
- `offset` (int, optional): Pagination offset (default: 0)
- `search` (string, optional): Search projects by name
- `language` (string, optional): Filter by programming language
- `status` (string, optional): Filter by analysis status

**Response:**

```json
{
  "status": "success",
  "data": {
    "projects": [
      {
        "id": "proj_123456789",
        "name": "flext-core",
        "project_path": "/path/to/flext-core",
        "repository_url": "https://github.com/flext-sh/flext-core",
        "language": "python",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-20T14:45:00Z",
        "last_analysis_at": "2024-01-20T14:30:00Z",
        "quality_score": 92.5,
        "quality_grade": "A",
        "status": "active"
      }
    ],
    "pagination": {
      "total": 45,
      "limit": 20,
      "offset": 0,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

#### Get Project Details

```http
GET /api/v1/projects/{project_id}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "proj_123456789",
    "name": "flext-core",
    "project_path": "/path/to/flext-core",
    "repository_url": "https://github.com/flext-sh/flext-core",
    "language": "python",
    "quality_config": {
      "min_coverage": 90.0,
      "max_complexity": 10,
      "enabled_analyzers": ["ruff", "mypy", "bandit"]
    },
    "latest_analysis": {
      "id": "analysis_987654321",
      "status": "completed",
      "started_at": "2024-01-20T14:30:00Z",
      "completed_at": "2024-01-20T14:35:00Z",
      "quality_score": 92.5,
      "quality_grade": "A",
      "metrics": {
        "total_files": 156,
        "total_lines": 12450,
        "coverage_percentage": 94.2,
        "complexity_score": 8.1,
        "security_score": 98.5
      },
      "issue_counts": {
        "critical": 0,
        "high": 2,
        "medium": 8,
        "low": 15
      }
    }
  }
}
```

#### Create Project

```http
POST /api/v1/projects
```

**Request Body:**

```json
{
  "name": "new-project",
  "project_path": "/path/to/project",
  "repository_url": "https://github.com/company/project",
  "language": "python",
  "auto_analyze": true,
  "quality_config": {
    "min_coverage": 85.0,
    "max_complexity": 12,
    "enabled_analyzers": ["ruff", "mypy", "bandit"]
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "proj_123456790",
    "name": "new-project",
    "status": "created",
    "created_at": "2024-01-20T15:00:00Z"
  }
}
```

#### Update Project

```http
PUT /api/v1/projects/{project_id}
```

**Request Body:**

```json
{
  "quality_config": {
    "min_coverage": 95.0,
    "max_complexity": 8,
    "enabled_analyzers": ["ruff", "mypy", "bandit", "semgrep"]
  },
  "auto_analyze": false
}
```

#### Delete Project

```http
DELETE /api/v1/projects/{project_id}
```

**Response:**

```json
{
  "status": "success",
  "message": "Project deleted successfully"
}
```

### Analysis API

#### Start Analysis

```http
POST /api/v1/projects/{project_id}/analyze
```

**Request Body:**

```json
{
  "commit_hash": "abc123def456",
  "branch": "main",
  "pull_request_id": "123",
  "analysis_config": {
    "full_analysis": true,
    "include_security": true,
    "include_performance": true
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "analysis_id": "analysis_987654322",
    "status": "queued",
    "estimated_duration": "5-10 minutes",
    "progress_url": "/api/v1/analyses/analysis_987654322/progress"
  }
}
```

#### Get Analysis Status

```http
GET /api/v1/analyses/{analysis_id}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "analysis_987654322",
    "project_id": "proj_123456789",
    "status": "in_progress",
    "progress": 65,
    "started_at": "2024-01-20T15:30:00Z",
    "estimated_completion": "2024-01-20T15:37:00Z",
    "current_stage": "security_analysis",
    "stages": {
      "code_analysis": "completed",
      "type_checking": "completed",
      "security_analysis": "in_progress",
      "coverage_analysis": "pending",
      "report_generation": "pending"
    }
  }
}
```

#### Get Analysis Results

```http
GET /api/v1/analyses/{analysis_id}/results
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "analysis_987654322",
    "project_id": "proj_123456789",
    "status": "completed",
    "started_at": "2024-01-20T15:30:00Z",
    "completed_at": "2024-01-20T15:37:00Z",
    "duration_seconds": 420,
    "quality_score": 91.8,
    "quality_grade": "A-",
    "metrics": {
      "total_files": 156,
      "total_lines": 12450,
      "code_lines": 9850,
      "comment_lines": 1200,
      "blank_lines": 1400,
      "coverage_percentage": 93.1,
      "complexity_score": 8.3,
      "security_score": 97.2,
      "maintainability_score": 89.5,
      "duplication_percentage": 2.1
    },
    "scores": {
      "coverage_score": 93.1,
      "complexity_score": 82.5,
      "security_score": 97.2,
      "maintainability_score": 89.5,
      "duplication_score": 95.8,
      "overall_score": 91.8
    },
    "issue_counts": {
      "critical": 0,
      "high": 3,
      "medium": 12,
      "low": 28,
      "total": 43
    },
    "analysis_details": {
      "analyzers_used": ["ruff", "mypy", "bandit", "coverage"],
      "files_analyzed": 156,
      "files_skipped": 4,
      "analysis_time_by_stage": {
        "code_analysis": 180,
        "type_checking": 120,
        "security_analysis": 90,
        "coverage_analysis": 30
      }
    }
  }
}
```

### Quality Issues API

#### List Quality Issues

```http
GET /api/v1/analyses/{analysis_id}/issues
```

**Parameters:**

- `severity` (string, optional): Filter by severity (critical, high, medium, low)
- `issue_type` (string, optional): Filter by issue type (security, complexity, style, etc.)
- `file_path` (string, optional): Filter by file path
- `status` (string, optional): Filter by status (active, suppressed, fixed)
- `limit` (int, optional): Number of results (default: 20, max: 100)
- `offset` (int, optional): Pagination offset

**Response:**

```json
{
  "status": "success",
  "data": {
    "issues": [
      {
        "id": "issue_555666777",
        "analysis_id": "analysis_987654322",
        "severity": "high",
        "issue_type": "security",
        "rule_id": "B101",
        "rule_name": "assert_used",
        "message": "Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.",
        "file_path": "src/flext_quality/analyzer.py",
        "line_number": 245,
        "column_number": 8,
        "end_line_number": 245,
        "end_column_number": 35,
        "code_snippet": "assert project_path.exists(), \"Project path must exist\"",
        "suggestion": "Replace assert with proper error handling using FlextResult pattern",
        "created_at": "2024-01-20T15:32:00Z",
        "status": "active"
      }
    ],
    "pagination": {
      "total": 43,
      "limit": 20,
      "offset": 0
    },
    "summary": {
      "by_severity": {
        "critical": 0,
        "high": 3,
        "medium": 12,
        "low": 28
      },
      "by_type": {
        "security": 8,
        "complexity": 12,
        "style": 15,
        "typing": 5,
        "documentation": 3
      }
    }
  }
}
```

#### Get Issue Details

```http
GET /api/v1/issues/{issue_id}
```

#### Suppress Issue

```http
PUT /api/v1/issues/{issue_id}/suppress
```

**Request Body:**

```json
{
  "reason": "False positive - this assert is used for development debugging only",
  "suppressed_until": "2024-06-01T00:00:00Z"
}
```

#### Mark Issue as Fixed

```http
PUT /api/v1/issues/{issue_id}/fixed
```

### Reports API

#### Generate Report

```http
POST /api/v1/analyses/{analysis_id}/reports
```

**Request Body:**

```json
{
  "format": "html",
  "template": "executive",
  "include_sections": ["summary", "metrics", "issues", "recommendations"],
  "custom_branding": {
    "company_name": "FLEXT Platform",
    "logo_url": "https://company.com/logo.png"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "report_id": "report_111222333",
    "status": "generating",
    "estimated_completion": "2024-01-20T15:40:00Z",
    "download_url": "/api/v1/reports/report_111222333/download"
  }
}
```

#### Download Report

```http
GET /api/v1/reports/{report_id}/download
```

**Response:** Binary file download (PDF, HTML, etc.)

### Metrics API

#### Get Project Metrics

```http
GET /api/v1/projects/{project_id}/metrics
```

**Parameters:**

- `period` (string, optional): Time period (day, week, month, quarter, year)
- `start_date` (string, optional): Start date (ISO 8601)
- `end_date` (string, optional): End date (ISO 8601)
- `metrics` (array, optional): Specific metrics to retrieve

**Response:**

```json
{
  "status": "success",
  "data": {
    "project_id": "proj_123456789",
    "period": "month",
    "metrics": {
      "quality_score_trend": [
        { "date": "2024-01-01", "value": 89.2 },
        { "date": "2024-01-02", "value": 89.8 },
        { "date": "2024-01-03", "value": 91.2 }
      ],
      "coverage_trend": [
        { "date": "2024-01-01", "value": 92.1 },
        { "date": "2024-01-02", "value": 93.0 },
        { "date": "2024-01-03", "value": 93.1 }
      ],
      "issue_trend": [
        {
          "date": "2024-01-01",
          "critical": 1,
          "high": 5,
          "medium": 15,
          "low": 32
        },
        {
          "date": "2024-01-02",
          "critical": 0,
          "high": 4,
          "medium": 13,
          "low": 29
        },
        {
          "date": "2024-01-03",
          "critical": 0,
          "high": 3,
          "medium": 12,
          "low": 28
        }
      ]
    },
    "summary": {
      "current_score": 91.8,
      "score_change": 2.6,
      "trend": "improving",
      "days_analyzed": 30
    }
  }
}
```

#### Get Ecosystem Metrics

```http
GET /api/v1/metrics/ecosystem
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "ecosystem_overview": {
      "total_projects": 32,
      "active_projects": 28,
      "average_quality_score": 87.3,
      "projects_meeting_standards": 25,
      "compliance_percentage": 89.3
    },
    "quality_distribution": {
      "A+": 8,
      "A": 12,
      "A-": 5,
      "B+": 3,
      "B": 2,
      "B-": 1,
      "C+": 1,
      "C": 0,
      "C-": 0,
      "D+": 0,
      "D": 0,
      "F": 0
    },
    "project_categories": {
      "core_libraries": {
        "count": 2,
        "average_score": 95.2,
        "projects": ["flext-core", "flext-observability"]
      },
      "application_services": {
        "count": 5,
        "average_score": 89.1,
        "projects": [
          "flext-api",
          "flext-web",
          "flext-auth",
          "flext-quality",
          "flext-cli"
        ]
      },
      "infrastructure": {
        "count": 6,
        "average_score": 86.8
      },
      "singer_ecosystem": {
        "count": 15,
        "average_score": 84.2
      }
    }
  }
}
```

### Quality Rules API

#### List Quality Rules

```http
GET /api/v1/rules
```

#### Create Custom Rule

```http
POST /api/v1/rules
```

**Request Body:**

```json
{
  "name": "FLEXT Entity Pattern",
  "description": "Ensure all domain entities extend FlextEntity",
  "category": "architecture",
  "severity": "high",
  "analyzer": "semgrep",
  "rule_definition": {
    "pattern": "class $CLASS(...):\n  ...",
    "condition": "not ($CLASS extends FlextEntity)",
    "message": "Domain entities must extend FlextEntity"
  },
  "enabled": true
}
```

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request validation failed",
    "details": {
      "field": "project_path",
      "reason": "Project path is required"
    },
    "timestamp": "2024-01-20T15:45:00Z",
    "request_id": "req_123456789"
  }
}
```

### HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request parameters
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **409 Conflict** - Resource conflict
- **422 Unprocessable Entity** - Validation error
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error
- **503 Service Unavailable** - Service temporarily unavailable

### Common Error Codes

- `VALIDATION_ERROR` - Request validation failed
- `AUTHENTICATION_ERROR` - Authentication failed
- `AUTHORIZATION_ERROR` - Insufficient permissions
- `RESOURCE_NOT_FOUND` - Requested resource not found
- `RESOURCE_CONFLICT` - Resource already exists
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `ANALYSIS_FAILED` - Quality analysis failed
- `REPORT_GENERATION_FAILED` - Report generation failed

## Rate Limiting

### Rate Limits

- **Authenticated users**: 1000 requests per hour
- **Service-to-service**: 10000 requests per hour
- **Analysis operations**: 10 concurrent analyses per project
- **Report generation**: 5 reports per minute

### Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1642694400
X-RateLimit-Retry-After: 3600
```

## Webhooks

### Webhook Events

- `analysis.started` - Analysis started
- `analysis.completed` - Analysis completed
- `analysis.failed` - Analysis failed
- `issue.created` - New quality issue detected
- `issue.resolved` - Quality issue resolved
- `report.generated` - Quality report generated

### Webhook Payload Example

```json
{
  "event": "analysis.completed",
  "timestamp": "2024-01-20T15:37:00Z",
  "data": {
    "analysis_id": "analysis_987654322",
    "project_id": "proj_123456789",
    "project_name": "flext-core",
    "quality_score": 91.8,
    "quality_grade": "A-",
    "previous_score": 89.2,
    "score_change": 2.6,
    "analysis_url": "https://quality.flext.sh/analyses/analysis_987654322"
  }
}
```

## SDK Integration

### Python SDK

```python
from flext_quality import FlextQualityClient

# Initialize client
client = FlextQualityClient(
    base_url="https://quality.flext.sh",
    api_key="your-api-key"
)

# Create project
project = await client.projects.create(
    name="my-project",
    project_path="/path/to/project",
    repository_url="https://github.com/company/project"
)

# Start analysis
analysis = await client.analyses.start(
    project_id=project.id,
    branch="main"
)

# Wait for completion
analysis = await client.analyses.wait_for_completion(
    analysis_id=analysis.id,
    timeout=600  # 10 minutes
)

# Get results
results = await client.analyses.get_results(analysis.id)
print(f"Quality Score: {results.quality_score}")

# Generate report
report = await client.reports.generate(
    analysis_id=analysis.id,
    format="html",
    template="executive"
)

# Download report
report_data = await client.reports.download(report.id)
```

## Next Steps

- **[Python SDK Documentation](python-sdk.md)** - Detailed Python client library guide
- **[GraphQL API](graphql.md)** - GraphQL schema and queries
- **[Webhook Integration](webhooks.md)** - Event-driven integrations
- **[Integration Examples](../integration/README.md)** - Real-world integration examples
