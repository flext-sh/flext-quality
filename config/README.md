# Configuration Module - Centralized Settings Management

The configuration module provides centralized configuration management for FLEXT Quality, handling environment-specific settings, external service configuration, and quality analysis parameters with proper validation and type safety.

## Overview

The configuration module implements a layered configuration system that provides:
- **Environment-Specific Configuration**: Development, testing, staging, and production settings
- **External Service Configuration**: Database, Redis, monitoring, and external tool settings
- **Quality Analysis Configuration**: Thresholds, tool settings, and analysis parameters
- **Security Configuration**: Authentication, authorization, and security policy settings
- **Validation and Type Safety**: Pydantic-based configuration validation with clear error messages

## Architecture

### Configuration Hierarchy
```
config/
├── __init__.py              # Configuration module initialization and exports
├── base.py                  # Base configuration classes and validation
├── development.py           # Development environment configuration
├── testing.py              # Test environment configuration
├── production.py           # Production environment configuration
├── quality.py              # Quality analysis specific configuration
└── README.md               # This documentation
```

### Configuration Layers
The configuration system uses a hierarchical approach:

1. **Base Configuration**: Common settings shared across all environments
2. **Environment Configuration**: Environment-specific overrides
3. **Local Configuration**: Local development and testing overrides
4. **Runtime Configuration**: Dynamic configuration from environment variables
5. **Analysis Configuration**: Per-analysis configuration and parameters

## Base Configuration (`base.py`)

### Core Configuration Classes
Foundation configuration classes using Pydantic for validation:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from pathlib import Path
import os

class DatabaseConfig(BaseModel):
    """Database connection configuration."""
    
    url: str = Field(
        ...,
        description="Database connection URL",
        example="postgresql://user:pass@localhost:5432/flext_quality"
    )
    
    pool_size: int = Field(
        default=10,
        description="Connection pool size",
        ge=1,
        le=100
    )
    
    max_overflow: int = Field(
        default=20,
        description="Maximum connection overflow",
        ge=0,
        le=100
    )
    
    echo_sql: bool = Field(
        default=False,
        description="Enable SQL query logging"
    )
    
    @validator('url')
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if not v.startswith(('postgresql://', 'sqlite:///', 'mysql://')):
            raise ValueError("Database URL must use supported scheme")
        return v

class RedisConfig(BaseModel):
    """Redis connection configuration."""
    
    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    
    connection_pool_size: int = Field(
        default=10,
        description="Redis connection pool size",
        ge=1,
        le=100
    )
    
    timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
        ge=1,
        le=300
    )

class ExternalToolConfig(BaseModel):
    """Configuration for external analysis tools."""
    
    ruff: Dict[str, any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "timeout": 300,
            "config_file": "pyproject.toml",
            "rules": ["ALL"]
        },
        description="Ruff linter configuration"
    )
    
    mypy: Dict[str, any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "strict": True,
            "timeout": 600,
            "ignore_missing_imports": False
        },
        description="MyPy type checker configuration"
    )
    
    bandit: Dict[str, any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "confidence": "medium",
            "severity": "low",
            "timeout": 300
        },
        description="Bandit security scanner configuration"
    )
    
    coverage: Dict[str, any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "minimum_coverage": 90.0,
            "timeout": 300
        },
        description="Coverage analysis configuration"
    )

class QualityThresholds(BaseModel):
    """Quality analysis thresholds and limits."""
    
    min_overall_score: float = Field(
        default=80.0,
        description="Minimum acceptable overall quality score",
        ge=0.0,
        le=100.0
    )
    
    max_complexity: int = Field(
        default=10,
        description="Maximum acceptable cyclomatic complexity",
        ge=1,
        le=100
    )
    
    min_coverage: float = Field(
        default=90.0,
        description="Minimum required test coverage percentage",
        ge=0.0,
        le=100.0
    )
    
    max_duplication: float = Field(
        default=5.0,
        description="Maximum acceptable code duplication percentage",
        ge=0.0,
        le=100.0
    )
    
    max_security_issues: int = Field(
        default=0,
        description="Maximum acceptable security issues",
        ge=0
    )

class ObservabilityConfig(BaseModel):
    """Observability and monitoring configuration."""
    
    metrics_endpoint: Optional[str] = Field(
        default=None,
        description="Metrics collection endpoint URL"
    )
    
    tracing_endpoint: Optional[str] = Field(
        default=None,
        description="Distributed tracing endpoint URL"
    )
    
    service_name: str = Field(
        default="flext-quality",
        description="Service name for observability"
    )
    
    enable_metrics: bool = Field(
        default=True,
        description="Enable metrics collection"
    )
    
    enable_tracing: bool = Field(
        default=True,
        description="Enable distributed tracing"
    )

class Config(BaseModel):
    """Base configuration with common settings."""
    
    # Application settings
    app_name: str = Field(
        default="FLEXT Quality",
        description="Application name"
    )
    
    version: str = Field(
        default="0.9.0",
        description="Application version"
    )
    
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    # Database configuration
    database: DatabaseConfig = Field(
        default_factory=DatabaseConfig,
        description="Database configuration"
    )
    
    # Redis configuration
    redis: RedisConfig = Field(
        default_factory=RedisConfig,
        description="Redis configuration"
    )
    
    # External tools configuration
    external_tools: ExternalToolConfig = Field(
        default_factory=ExternalToolConfig,
        description="External analysis tools configuration"
    )
    
    # Quality thresholds
    quality_thresholds: QualityThresholds = Field(
        default_factory=QualityThresholds,
        description="Quality analysis thresholds"
    )
    
    # Observability configuration
    observability: ObservabilityConfig = Field(
        default_factory=ObservabilityConfig,
        description="Observability and monitoring configuration"
    )
    
    # Security settings
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for cryptographic operations"
    )
    
    allowed_hosts: List[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        description="Allowed host names for API access"
    )
    
    # File system settings
    allowed_project_paths: List[str] = Field(
        default_factory=lambda: ["/workspace", "/projects"],
        description="Allowed project paths for analysis"
    )
    
    max_analysis_timeout: int = Field(
        default=3600,
        description="Maximum analysis timeout in seconds",
        ge=60,
        le=7200
    )
    
    @validator('secret_key')
    def validate_secret_key(cls, v, values):
        """Validate secret key strength in production."""
        if not values.get('debug', True) and v == "dev-secret-key-change-in-production":
            raise ValueError("Must set secure secret key in production")
        return v
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "FLEXT_QUALITY_"
        case_sensitive = False
        validate_assignment = True
```

## Environment-Specific Configuration

### Development Configuration (`development.py`)
Development environment settings with debugging enabled:

```python
from .base import Config, DatabaseConfig, RedisConfig

class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    debug: bool = True
    
    # Development database (SQLite for simplicity)
    database: DatabaseConfig = DatabaseConfig(
        url="sqlite:///./flext_quality_dev.db",
        echo_sql=True
    )
    
    # Local Redis
    redis: RedisConfig = RedisConfig(
        url="redis://localhost:6379/0"
    )
    
    # Relaxed quality thresholds for development
    quality_thresholds: QualityThresholds = QualityThresholds(
        min_overall_score=70.0,
        max_complexity=15,
        min_coverage=80.0
    )
    
    # Enable all debugging features
    log_level: str = "DEBUG"
    enable_hot_reload: bool = True
    
    # Development-specific allowed paths
    allowed_project_paths: List[str] = [
        "/workspace",
        "/tmp/analysis",
        str(Path.home() / "projects")
    ]
```

### Testing Configuration (`testing.py`)
Test environment settings optimized for testing:

```python
class TestingConfig(Config):
    """Testing environment configuration."""
    
    debug: bool = True
    testing: bool = True
    
    # In-memory database for tests
    database: DatabaseConfig = DatabaseConfig(
        url="sqlite:///:memory:",
        echo_sql=False
    )
    
    # Test Redis (or mock)
    redis: RedisConfig = RedisConfig(
        url="redis://localhost:6379/15"  # Test database
    )
    
    # Strict quality thresholds for testing
    quality_thresholds: QualityThresholds = QualityThresholds(
        min_overall_score=90.0,
        max_complexity=8,
        min_coverage=95.0
    )
    
    # Fast timeouts for tests
    max_analysis_timeout: int = 60
    
    # Test-specific settings
    log_level: str = "WARNING"
    disable_external_calls: bool = True
```

### Production Configuration (`production.py`)
Production environment settings with security and performance optimizations:

```python
import os
from typing import List

class ProductionConfig(Config):
    """Production environment configuration."""
    
    debug: bool = False
    
    # Production database from environment
    database: DatabaseConfig = DatabaseConfig(
        url=os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/flext_quality"),
        pool_size=20,
        max_overflow=40,
        echo_sql=False
    )
    
    # Production Redis
    redis: RedisConfig = RedisConfig(
        url=os.getenv("REDIS_URL", "redis://redis:6379/0"),
        connection_pool_size=20
    )
    
    # Strict production quality thresholds
    quality_thresholds: QualityThresholds = QualityThresholds(
        min_overall_score=85.0,
        max_complexity=10,
        min_coverage=90.0,
        max_security_issues=0
    )
    
    # Security settings
    secret_key: str = os.getenv("SECRET_KEY")  # Must be set in environment
    allowed_hosts: List[str] = os.getenv("ALLOWED_HOSTS", "").split(",")
    
    # Production logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Performance settings
    max_concurrent_analyses: int = 10
    analysis_result_cache_ttl: int = 3600  # 1 hour
    
    # Production paths (restricted)
    allowed_project_paths: List[str] = [
        "/workspace/projects",
        "/data/repositories"
    ]
    
    @validator('secret_key')
    def validate_production_secret_key(cls, v):
        """Ensure secret key is set in production."""
        if not v:
            raise ValueError("SECRET_KEY environment variable must be set")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
```

## Quality Analysis Configuration (`quality.py`)

### Analysis-Specific Configuration
Configuration for different types of quality analysis:

```python
from enum import Enum
from typing import Dict, List, Optional

class AnalysisType(str, Enum):
    """Types of quality analysis."""
    COMPREHENSIVE = "comprehensive"
    SECURITY_FOCUSED = "security_focused"
    COMPLEXITY_FOCUSED = "complexity_focused"
    MAINTENANCE_FOCUSED = "maintenance_focused"
    CUSTOM = "custom"

class ProjectType(str, Enum):
    """Types of projects for different quality standards."""
    CORE_LIBRARY = "core_library"
    APPLICATION_SERVICE = "application_service"
    DATA_TAP = "data_tap"
    DATA_TARGET = "data_target"
    DBT_PROJECT = "dbt_project"
    INFRASTRUCTURE = "infrastructure"

class AnalysisConfiguration(BaseModel):
    """Configuration for a specific analysis run."""
    
    analysis_type: AnalysisType = Field(
        default=AnalysisType.COMPREHENSIVE,
        description="Type of analysis to perform"
    )
    
    project_type: Optional[ProjectType] = Field(
        default=None,
        description="Type of project being analyzed"
    )
    
    # Analysis components to include
    include_security: bool = Field(
        default=True,
        description="Include security vulnerability analysis"
    )
    
    include_complexity: bool = Field(
        default=True,
        description="Include code complexity analysis"
    )
    
    include_dead_code: bool = Field(
        default=True,
        description="Include dead code detection"
    )
    
    include_duplicates: bool = Field(
        default=True,
        description="Include code duplication analysis"
    )
    
    include_style: bool = Field(
        default=True,
        description="Include code style validation"
    )
    
    include_performance: bool = Field(
        default=False,
        description="Include performance analysis"
    )
    
    # Tool-specific configuration
    tool_configurations: Dict[str, Dict] = Field(
        default_factory=dict,
        description="Tool-specific configuration overrides"
    )
    
    # Custom quality thresholds for this analysis
    quality_thresholds: Optional[QualityThresholds] = Field(
        default=None,
        description="Custom quality thresholds"
    )
    
    # File and directory filters
    include_patterns: List[str] = Field(
        default_factory=lambda: ["**/*.py"],
        description="File patterns to include in analysis"
    )
    
    exclude_patterns: List[str] = Field(
        default_factory=lambda: [
            "**/__pycache__/**",
            "**/.*",
            "**/venv/**",
            "**/node_modules/**"
        ],
        description="File patterns to exclude from analysis"
    )
    
    # Analysis limits and timeouts
    max_file_size: int = Field(
        default=1024 * 1024,  # 1MB
        description="Maximum file size to analyze in bytes"
    )
    
    analysis_timeout: int = Field(
        default=3600,  # 1 hour
        description="Maximum analysis timeout in seconds"
    )
    
    def get_project_type_thresholds(self) -> QualityThresholds:
        """Get quality thresholds based on project type."""
        if self.quality_thresholds:
            return self.quality_thresholds
            
        # Project-type-specific thresholds
        project_thresholds = {
            ProjectType.CORE_LIBRARY: QualityThresholds(
                min_overall_score=90.0,
                max_complexity=8,
                min_coverage=95.0,
                max_security_issues=0
            ),
            ProjectType.APPLICATION_SERVICE: QualityThresholds(
                min_overall_score=85.0,
                max_complexity=10,
                min_coverage=90.0,
                max_security_issues=0
            ),
            ProjectType.DATA_TAP: QualityThresholds(
                min_overall_score=80.0,
                max_complexity=12,
                min_coverage=85.0,
                max_security_issues=1
            ),
            ProjectType.DATA_TARGET: QualityThresholds(
                min_overall_score=80.0,
                max_complexity=12,
                min_coverage=85.0,
                max_security_issues=1
            ),
            ProjectType.DBT_PROJECT: QualityThresholds(
                min_overall_score=75.0,
                max_complexity=15,
                min_coverage=80.0,
                max_security_issues=2
            )
        }
        
        return project_thresholds.get(
            self.project_type, 
            QualityThresholds()  # Default thresholds
        )

class QualityConfigurationManager:
    """Manager for quality analysis configurations."""
    
    def __init__(self, base_config: Config):
        self.base_config = base_config
        self._analysis_templates = self._load_analysis_templates()
    
    def create_analysis_config(
        self,
        analysis_type: AnalysisType,
        project_type: Optional[ProjectType] = None,
        overrides: Optional[Dict] = None
    ) -> AnalysisConfiguration:
        """Create analysis configuration with appropriate defaults."""
        
        # Start with template configuration
        template = self._analysis_templates.get(analysis_type, {})
        
        # Apply project type specific settings  
        if project_type:
            template.update(self._get_project_type_settings(project_type))
        
        # Apply any custom overrides
        if overrides:
            template.update(overrides)
        
        return AnalysisConfiguration(**template)
    
    def _load_analysis_templates(self) -> Dict[AnalysisType, Dict]:
        """Load predefined analysis templates."""
        return {
            AnalysisType.COMPREHENSIVE: {
                "include_security": True,
                "include_complexity": True,
                "include_dead_code": True,
                "include_duplicates": True,
                "include_style": True,
                "include_performance": False
            },
            AnalysisType.SECURITY_FOCUSED: {
                "include_security": True,
                "include_complexity": False,
                "include_dead_code": False,
                "include_duplicates": False,
                "include_style": False,
                "include_performance": False
            },
            AnalysisType.COMPLEXITY_FOCUSED: {
                "include_security": False,
                "include_complexity": True,
                "include_dead_code": True,
                "include_duplicates": True,
                "include_style": False,
                "include_performance": True
            }
        }
```

## Configuration Loading and Management

### Configuration Factory
Centralized configuration loading with environment detection:

```python
import os
from typing import Type

def get_config_class() -> Type[Config]:
    """Get appropriate configuration class based on environment."""
    env = os.getenv("FLEXT_ENV", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    
    return config_map.get(env, DevelopmentConfig)

def load_config() -> Config:
    """Load configuration from environment and files."""
    config_class = get_config_class()
    
    # Load from environment variables
    config = config_class()
    
    # Load from configuration files if they exist
    config_file = os.getenv("FLEXT_QUALITY_CONFIG_FILE")
    if config_file and os.path.exists(config_file):
        config = load_config_from_file(config, config_file)
    
    return config

def load_config_from_file(base_config: Config, config_file: str) -> Config:
    """Load configuration overrides from YAML or JSON file."""
    import yaml
    import json
from pathlib import Path
    
    config_path = Path(config_file)
    
    if config_path.suffix.lower() == '.yaml' or config_path.suffix.lower() == '.yml':
        with open(config_path) as f:
            file_config = yaml.safe_load(f)
    elif config_path.suffix.lower() == '.json':
        with open(config_path) as f:
            file_config = json.load(f)
    else:
        raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")
    
    # Merge file configuration with base configuration
    return base_config.copy(update=file_config)

# Global configuration instance
config = load_config()
```

### Configuration Validation
Comprehensive validation with helpful error messages:

```python
def validate_configuration(config: Config) -> List[str]:
    """Validate configuration and return list of validation errors."""
    errors = []
    
    # Validate database connectivity
    try:
        # Test database connection
        pass
    except Exception as e:
        errors.append(f"Database connection failed: {e}")
    
    # Validate Redis connectivity  
    try:
        # Test Redis connection
        pass
    except Exception as e:
        errors.append(f"Redis connection failed: {e}")
    
    # Validate external tools
    for tool_name, tool_config in config.external_tools.dict().items():
        if tool_config.get("enabled", False):
            if not check_tool_availability(tool_name):
                errors.append(f"External tool not available: {tool_name}")
    
    # Validate file system permissions
    for path in config.allowed_project_paths:
        if not os.path.exists(path):
            errors.append(f"Allowed project path does not exist: {path}")
        elif not os.access(path, os.R_OK):
            errors.append(f"No read access to project path: {path}")
    
    return errors

def check_tool_availability(tool_name: str) -> bool:
    """Check if external tool is available and executable."""
    import shutil
    return shutil.which(tool_name) is not None
```

## Configuration Examples

### Environment Configuration File
```yaml
# config/production.yml
database:
  url: postgresql://user:pass@db-host:5432/flext_quality
  pool_size: 20
  max_overflow: 40

redis:
  url: redis://redis-host:6379/0
  connection_pool_size: 20

external_tools:
  ruff:
    enabled: true
    timeout: 300
    rules: ["E", "W", "F", "B", "S"]
  
  mypy:
    enabled: true
    strict: true
    timeout: 600

quality_thresholds:
  min_overall_score: 85.0
  max_complexity: 10
  min_coverage: 90.0

observability:
  metrics_endpoint: http://prometheus:9090
  tracing_endpoint: http://jaeger:14268
  service_name: flext-quality-prod

allowed_project_paths:
  - /workspace/projects
  - /data/repositories

max_analysis_timeout: 3600
```

### Docker Environment Variables
```bash
# .env file for Docker deployment
FLEXT_ENV=production
FLEXT_QUALITY_SECRET_KEY=super-secure-secret-key-here
FLEXT_QUALITY_ALLOWED_HOSTS=api.company.com,quality.company.com

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/flext_quality
REDIS_URL=redis://redis:6379/0

FLEXT_QUALITY_MIN_OVERALL_SCORE=85.0
FLEXT_QUALITY_MAX_COMPLEXITY=10
FLEXT_QUALITY_MIN_COVERAGE=90.0

PROMETHEUS_ENDPOINT=http://prometheus:9090
JAEGER_ENDPOINT=http://jaeger:14268
```

## Testing Support

### Configuration Testing Utilities
```python
@pytest.fixture
def test_config():
    """Provide test configuration for unit tests."""
    return TestingConfig()

@pytest.fixture  
def temp_config_file(tmp_path):
    """Create temporary configuration file for testing."""
    config_data = {
        "debug": True,
        "database": {"url": "sqlite:///test.db"},
        "quality_thresholds": {"min_overall_score": 95.0}
    }
    
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    
    return str(config_file)

def test_configuration_loading(temp_config_file):
    """Test configuration loading from file."""
    os.environ["FLEXT_QUALITY_CONFIG_FILE"] = temp_config_file
    
    config = load_config()
    
    assert config.debug is True
    assert config.quality_thresholds.min_overall_score == 95.0
```

## Related Documentation

- **[Base Configuration](base.py)** - Core configuration classes and validation
- **[Quality Configuration](quality.py)** - Analysis-specific configuration
- **[Application Services](../application/README.md)** - Service configuration integration
- **[Infrastructure Layer](../infrastructure/README.md)** - External service configuration
