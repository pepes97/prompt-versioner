# Configuration

Learn how to configure **Prompt Versioner** for your specific needs and environment.

## 🔧 Basic Configuration

### Database Configuration

By default, Prompt Versioner uses SQLite with a local database file. You can configure this in several ways:

```python
from prompt_versioner import PromptVersioner

# Default configuration (creates 'prompts.db' in current directory)
versioner = PromptVersioner()

# Custom database path
versioner = PromptVersioner(db_path="/path/to/your/database.db")

# Memory database (for testing - data is lost when process ends)
versioner = PromptVersioner(db_path=":memory:")
```

### Environment Variables

Set common configuration options using environment variables:

```bash
# Database configuration
export PROMPT_VERSIONER_DB_PATH="/opt/prompts/production.db"

# Web dashboard configuration
export PROMPT_VERSIONER_HOST="0.0.0.0"
export PROMPT_VERSIONER_PORT="8080"
export PROMPT_VERSIONER_DEBUG="false"

# Git integration
export PROMPT_VERSIONER_GIT_REPO="/path/to/git/repo"
export PROMPT_VERSIONER_GIT_AUTO_COMMIT="true"

# OpenAI integration (for examples)
export OPENAI_API_KEY="your-api-key-here"
```

### Configuration File

Create a configuration file for complex setups:

```yaml
# prompt_versioner_config.yaml
database:
  path: "/opt/prompts/production.db"
  backup_interval: 3600  # seconds

web_dashboard:
  host: "0.0.0.0"
  port: 8080
  debug: false
  secret_key: "your-secret-key-here"

git_integration:
  repository_path: "/path/to/git/repo"
  auto_commit: true
  commit_message_template: "feat: {action} prompt {prompt_id} v{version}"

metrics:
  default_quality_threshold: 0.7
  cost_alert_threshold: 0.1
  latency_alert_threshold: 5.0

alerts:
  enabled: true
  email_notifications: true
  smtp_server: "smtp.example.com"
  smtp_port: 587
  email_from: "alerts@yourcompany.com"
  email_to: ["team@yourcompany.com"]
```

Load the configuration:

```python
from prompt_versioner import PromptVersioner
from prompt_versioner.config import load_config

# Load configuration from file
config = load_config("prompt_versioner_config.yaml")
versioner = PromptVersioner(config=config)
```

## 🔗 Git Integration

Configure Git integration for version control:

### Basic Git Setup

```python
from prompt_versioner import PromptVersioner
from prompt_versioner.tracker.git import GitTracker

# Initialize with Git tracking
versioner = PromptVersioner(
    db_path="prompts.db",
    git_repo="/path/to/git/repo"
)

# Enable auto-commit for prompt changes
versioner.enable_git_tracking(
    auto_commit=True,
    commit_message_template="feat: updated prompt {prompt_id} to v{version}"
)
```

### Advanced Git Configuration

```python
# Custom Git configuration
git_config = {
    "repository_path": "/path/to/git/repo",
    "auto_commit": True,
    "auto_push": False,  # Don't auto-push commits
    "branch": "prompts",  # Use specific branch
    "commit_message_template": "prompt: {action} {prompt_id} v{version}\n\n{description}",
    "author_name": "Prompt Versioner",
    "author_email": "prompts@yourcompany.com"
}

versioner = PromptVersioner(git_config=git_config)
```

## 📊 Metrics Configuration

Configure metrics tracking and thresholds:

```python
from prompt_versioner.metrics import MetricsConfig

metrics_config = MetricsConfig(
    # Quality thresholds
    quality_score_min=0.7,
    quality_score_warning=0.8,

    # Performance thresholds
    latency_max=5.0,
    latency_warning=3.0,

    # Cost thresholds
    cost_per_1k_tokens_max=0.1,
    cost_per_1k_tokens_warning=0.05,

    # Token usage
    input_tokens_warning=4000,
    output_tokens_warning=2000,

    # Automatic quality assessment
    enable_auto_quality_scoring=True,
    quality_model="sentiment-analysis",

    # Retention policy
    metrics_retention_days=365,
    detailed_logs_retention_days=30
)

versioner = PromptVersioner(metrics_config=metrics_config)
```

## ⚠️ Alerts Configuration

Set up automated alerts for performance monitoring:

```python
from prompt_versioner.alerts import AlertConfig, AlertChannel

# Configure alert channels
email_channel = AlertChannel(
    type="email",
    config={
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "alerts@yourcompany.com",
        "password": "app-password",
        "to_addresses": ["team@yourcompany.com"]
    }
)

slack_channel = AlertChannel(
    type="slack",
    config={
        "webhook_url": "https://hooks.slack.com/services/...",
        "channel": "#ai-alerts",
        "username": "Prompt Versioner"
    }
)

# Configure alert rules
alert_config = AlertConfig(
    channels=[email_channel, slack_channel],
    rules=[
        {
            "name": "High Latency",
            "condition": "latency > 5.0",
            "severity": "warning",
            "message": "Prompt {prompt_id} v{version} has high latency: {latency}s"
        },
        {
            "name": "Low Quality Score",
            "condition": "quality_score < 0.7",
            "severity": "error",
            "message": "Prompt {prompt_id} v{version} quality dropped to {quality_score}"
        },
        {
            "name": "High Cost",
            "condition": "cost > 0.1",
            "severity": "warning",
            "message": "Prompt {prompt_id} v{version} cost is high: ${cost}"
        }
    ]
)

versioner = PromptVersioner(alert_config=alert_config)
```

## 🌐 Web Dashboard Configuration

Configure the web dashboard for your environment:

```python
from prompt_versioner.web import DashboardConfig

dashboard_config = DashboardConfig(
    host="0.0.0.0",
    port=8080,
    debug=False,
    secret_key="your-secret-key-for-sessions",

    # Authentication (optional)
    enable_auth=True,
    auth_config={
        "type": "basic",  # or "oauth", "ldap"
        "users": {
            "admin": "hashed_password",
            "viewer": "hashed_password"
        }
    },

    # Customization
    app_title="My Company Prompts",
    logo_url="/static/custom_logo.png",
    theme="auto",  # "light", "dark", or "auto"

    # Features
    enable_editing=True,
    enable_deletion=False,
    enable_export=True,
    show_sensitive_data=False,

    # Performance
    cache_enabled=True,
    cache_timeout=300,  # 5 minutes
    pagination_size=50
)

# Start dashboard with custom config
versioner.start_dashboard(config=dashboard_config)
```

## 🧪 A/B Testing Configuration

Configure A/B testing parameters:

```python
from prompt_versioner.testing import ABTestConfig

ab_test_config = ABTestConfig(
    # Statistical parameters
    confidence_level=0.95,
    statistical_power=0.8,
    minimum_detectable_effect=0.05,

    # Sample size
    min_samples_per_variant=100,
    max_samples_per_variant=10000,

    # Duration limits
    min_test_duration_hours=24,
    max_test_duration_days=30,

    # Auto-stopping rules
    enable_early_stopping=True,
    early_stopping_threshold=0.99,

    # Traffic allocation
    default_traffic_split="equal",  # or "ramped"
    max_variants=5,

    # Metrics to track
    primary_metrics=["quality_score", "latency"],
    secondary_metrics=["cost", "token_usage"]
)

versioner = PromptVersioner(ab_test_config=ab_test_config)
```

## 🔒 Security Configuration

Configure security settings for production environments:

```python
from prompt_versioner.security import SecurityConfig

security_config = SecurityConfig(
    # Database encryption
    encrypt_database=True,
    encryption_key="your-encryption-key",

    # Data masking
    mask_sensitive_variables=True,
    sensitive_patterns=[
        r"api[_-]?key",
        r"password",
        r"token",
        r"secret"
    ],

    # Audit logging
    enable_audit_log=True,
    audit_log_path="/var/log/prompt_versioner_audit.log",

    # Access control
    role_based_access=True,
    default_permissions={
        "viewer": ["read"],
        "editor": ["read", "write"],
        "admin": ["read", "write", "delete", "admin"]
    }
)

versioner = PromptVersioner(security_config=security_config)
```

## 🏗️ Production Configuration Example

Here's a complete production configuration:

```python
from prompt_versioner import PromptVersioner
from prompt_versioner.config import ProductionConfig

# Production-ready configuration
config = ProductionConfig(
    # Database
    database_path="/opt/prompts/production.db",
    enable_database_backups=True,
    backup_interval_hours=6,
    backup_retention_days=30,

    # Performance
    connection_pool_size=20,
    query_timeout=30,
    cache_size_mb=512,

    # Monitoring
    enable_health_checks=True,
    health_check_endpoint="/health",
    enable_metrics_export=True,
    prometheus_port=9090,

    # Logging
    log_level="INFO",
    log_file="/var/log/prompt_versioner.log",
    log_rotation_size="100MB",
    log_retention_days=30,

    # Security
    enable_https=True,
    ssl_cert_path="/etc/ssl/certs/prompt_versioner.crt",
    ssl_key_path="/etc/ssl/private/prompt_versioner.key",

    # Git integration
    git_repository="/opt/git/prompts",
    git_auto_commit=True,
    git_auto_push=True,
    git_branch="production"
)

versioner = PromptVersioner(config=config)
```

## 🐳 Docker Configuration

Configure Prompt Versioner for Docker deployment:

### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 promptuser
RUN chown -R promptuser:promptuser /app
USER promptuser

# Configure defaults
ENV PROMPT_VERSIONER_DB_PATH=/app/data/prompts.db
ENV PROMPT_VERSIONER_HOST=0.0.0.0
ENV PROMPT_VERSIONER_PORT=5000

# Create data directory
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["prompt-dashboard"]
```

### Docker Compose Example

```yaml
version: '3.8'

services:
  prompt-versioner:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - PROMPT_VERSIONER_DB_PATH=/app/data/prompts.db
      - PROMPT_VERSIONER_CONFIG_FILE=/app/config/production.yaml
    restart: unless-stopped

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  grafana-data:
```

## 📝 Configuration Best Practices

1. **Environment Separation**: Use different configurations for development, staging, and production
2. **Secret Management**: Never store secrets in configuration files; use environment variables or secret management systems
3. **Backup Strategy**: Configure regular database backups and test restore procedures
4. **Monitoring**: Set up comprehensive monitoring and alerting for production systems
5. **Security**: Enable encryption, audit logging, and proper access controls in production
6. **Performance**: Tune connection pools, cache sizes, and query timeouts based on your usage patterns
7. **Documentation**: Document your configuration choices and keep them version controlled

## 🔍 Configuration Validation

Validate your configuration before deployment:

```python
from prompt_versioner.config import validate_config

# Validate configuration
config = load_config("production.yaml")
validation_result = validate_config(config)

if validation_result.is_valid:
    print("Configuration is valid!")
    versioner = PromptVersioner(config=config)
else:
    print("Configuration errors:")
    for error in validation_result.errors:
        print(f"  - {error}")
```

Ready to configure your setup? Next, learn about the [core concepts](../user-guide/core-concepts.md) that drive Prompt Versioner.
