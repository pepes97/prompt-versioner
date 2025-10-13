# Configuration

Learn how to configure **Prompt Versioner** for your specific needs and environment.

## 🔧 Basic Configuration

### Database Configuration

By default, Prompt Versioner uses SQLite with a local database file. You can configure this in several ways:

```python
from prompt_versioner import PromptVersioner

# Default configuration (creates database in project folder)
pv = PromptVersioner(project_name="my-project")

# Custom database path
pv = PromptVersioner(
    project_name="my-project",
    db_path="/path/to/your/database.db"
)

# Memory database (for testing - data is lost when process ends)
pv = PromptVersioner(
    project_name="test-project",
    db_path=":memory:"
)

# Disable Git integration
pv = PromptVersioner(
    project_name="my-project",
    enable_git=False
)
```

### Environment Variables

Set common configuration options using environment variables:

```bash
# Project configuration
export PROMPT_VERSIONER_PROJECT="my-project"
export PROMPT_VERSIONER_DB_PATH="/opt/prompts/production.db"

# Git integration
export PROMPT_VERSIONER_GIT_REPO="/path/to/git/repo"
export PROMPT_VERSIONER_ENABLE_GIT="true"

# Web dashboard (if available)
export PROMPT_VERSIONER_HOST="0.0.0.0"
export PROMPT_VERSIONER_PORT="5000"

# OpenAI integration (for examples)
export OPENAI_API_KEY="your-api-key-here"
```

### Configuration File

Create a configuration file for complex setups:

```yaml
# prompt_versioner_config.yaml
project:
  name: "production-prompts"
  db_path: "/opt/prompts/production.db"

git:
  enabled: true
  repository_path: "/path/to/git/repo"
  auto_commit: true

dashboard:
  host: "0.0.0.0"
  port: 5000
  enabled: true

metrics:
  default_quality_threshold: 0.7
  cost_alert_threshold: 0.1
  latency_alert_threshold: 5000  # milliseconds
```

Load the configuration:

```python
from prompt_versioner import PromptVersioner
import yaml

# Load configuration from file
with open("prompt_versioner_config.yaml", "r") as f:
    config = yaml.safe_load(f)

pv = PromptVersioner(
    project_name=config["project"]["name"],
    db_path=config["project"]["db_path"],
    enable_git=config["git"]["enabled"]
)
```

## 🔗 Git Integration

Configure Git integration for version control:

### Basic Git Setup

```python
from prompt_versioner import PromptVersioner

# Initialize with Git tracking enabled
pv = PromptVersioner(
    project_name="my-project",
    enable_git=True,
    git_repo="/path/to/git/repo"
)

# Install Git hooks for automatic tracking
pv.install_git_hooks()

print("🔗 Git integration enabled!")
```

### Advanced Git Configuration

```python
# Disable Git if needed
pv = PromptVersioner(
    project_name="my-project",
    enable_git=False  # No Git tracking
)

# Manual Git operations
if pv.git_enabled:
    # Install hooks
    pv.install_git_hooks()

    # Later, uninstall if needed
    pv.uninstall_git_hooks()
```

## 📊 Metrics Configuration

Configure metrics tracking and thresholds:

```python
from prompt_versioner import PromptVersioner

# Initialize with project
pv = PromptVersioner(project_name="production-ai")

# Set up custom thresholds for monitoring
def monitor_performance(name, version, metrics):
    """Custom performance monitoring"""

    # Quality threshold
    if metrics.get("quality_score", 0) < 0.7:
        print(f"⚠️ Low quality detected for {name} v{version}")

    # Latency threshold
    if metrics.get("latency_ms", 0) > 5000:
        print(f"⚠️ High latency detected for {name} v{version}")

    # Cost threshold
    if metrics.get("cost_eur", 0) > 0.1:
        print(f"⚠️ High cost detected for {name} v{version}")

# Use monitoring with your metrics
pv.log_metrics(
    name="my_prompt",
    version="1.0.0",
    model_name="gpt-4o-mini",
    input_tokens=100,
    output_tokens=200,
    latency_ms=1500,
    quality_score=0.85,
    success=True
)

# Custom analysis
def analyze_prompt_metrics(pv, prompt_name):
    """Analyze all metrics for a prompt"""
    versions = pv.list_versions(prompt_name)

    for version_info in versions:
        version_data = pv.get_version(prompt_name, version_info["version"])
        metrics = pv.storage.get_metrics(version_id=version_data["id"])

        if metrics:
            avg_quality = sum(m.get("quality_score", 0) for m in metrics) / len(metrics)
            avg_latency = sum(m.get("latency_ms", 0) for m in metrics) / len(metrics)
            total_cost = sum(m.get("cost_eur", 0) for m in metrics)

            print(f"📊 {prompt_name} v{version_info['version']}:")
            print(f"  Quality: {avg_quality:.2f}")
            print(f"  Latency: {avg_latency:.0f}ms")
            print(f"  Total cost: €{total_cost:.4f}")

# Run analysis
analyze_prompt_metrics(pv, "my_prompt")
```

## 🧪 A/B Testing Configuration

Configure A/B testing parameters:

```python
from prompt_versioner import ABTest

# Create A/B test with custom settings
ab_test = ABTest(
    versioner=pv,
    prompt_name="my_prompt",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score"
)

# Minimum samples for statistical significance
MIN_SAMPLES = 30

# Check if test is ready
if ab_test.is_ready(min_samples=MIN_SAMPLES):
    result = ab_test.get_result()
    print(f"Test complete: {result.winner} wins")
else:
    print(f"Need more samples (current: {ab_test.get_sample_counts()})")
```

## 🔒 Security Configuration

Configure security settings for production environments:

```python
from prompt_versioner import PromptVersioner
import os

# Secure database path
secure_db_path = os.path.join(os.path.expanduser("~"), ".prompt_versioner", "secure.db")

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(secure_db_path), exist_ok=True)

# Initialize with secure settings
pv = PromptVersioner(
    project_name="production-secure",
    db_path=secure_db_path,
    enable_git=False  # Disable Git for sensitive data
)

# Add annotations to track security decisions
pv.add_annotation(
    name="secure_prompt",
    version="1.0.0",
    text="Security review completed. No sensitive data in prompts.",
    author="security-team"
)
```

## 🏗️ Production Configuration Example

Here's a complete production configuration:

```python
from prompt_versioner import PromptVersioner
import os

# Production-ready configuration
production_config = {
    "project_name": "production-ai-system",
    "db_path": "/opt/prompts/production.db",
    "enable_git": True,
    "git_repo": "/opt/git/prompts"
}

# Initialize for production
pv = PromptVersioner(**production_config)

# Set up Git hooks for production tracking
pv.install_git_hooks()

# Add production monitoring
def production_monitor(pv):
    """Monitor production prompts"""
    prompts = pv.list_prompts()

    for prompt_name in prompts:
        latest = pv.get_latest(prompt_name)
        version_data = pv.get_version(prompt_name, latest["version"])
        metrics = pv.storage.get_metrics(version_id=version_data["id"])

        if metrics:
            recent_metrics = metrics[-10:]  # Last 10 calls
            avg_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)

            if avg_quality < 0.7:
                print(f"🚨 Production Alert: {prompt_name} quality below threshold!")

# Run monitoring
production_monitor(pv)
```

## 🐳 Docker Configuration

Configure Prompt Versioner for Docker deployment:

### Simple Docker Setup

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install prompt-versioner
RUN pip install prompt-versioner

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV PROMPT_VERSIONER_PROJECT=docker-project
ENV PROMPT_VERSIONER_DB_PATH=/app/data/prompts.db

# Copy your application
COPY . .

EXPOSE 5000

# Start your application
CMD ["python", "app.py"]
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
    environment:
      - PROMPT_VERSIONER_PROJECT=production
      - PROMPT_VERSIONER_DB_PATH=/app/data/prompts.db
    restart: unless-stopped
```

## 📝 Configuration Best Practices

1. **Environment Separation**: Use different projects for development, staging, and production
2. **Database Security**: Use secure paths and permissions for database files
3. **Git Integration**: Enable Git tracking for version control and team collaboration
4. **Monitoring**: Set up performance monitoring with metrics and thresholds
5. **Backup Strategy**: Export prompts regularly for backup and recovery
6. **Documentation**: Use annotations to document important changes and decisions

## 🔍 Configuration Validation

Validate your configuration before deployment:

```python
from prompt_versioner import PromptVersioner

def validate_setup(project_name, db_path):
    """Validate PromptVersioner setup"""
    try:
        pv = PromptVersioner(
            project_name=project_name,
            db_path=db_path
        )

        # Test basic operations
        pv.save_version(
            name="test_prompt",
            system_prompt="Test system prompt",
            user_prompt="Test user prompt",
            bump_type=VersionBump.MAJOR
        )

        # Clean up test
        pv.delete_prompt("test_prompt")

        print("✅ Configuration is valid!")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

# Validate your setup
if validate_setup("my-project", "./test.db"):
    print("Ready to proceed!")
```

Ready to configure your setup? Next, learn about the [core concepts](../user-guide/core-concepts.md) that drive Prompt Versioner.
