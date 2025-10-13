# Configuration

Learn how to configure **Prompt Versioner** for your specific needs and environment.

## 🔧 Database Configuration

By default, Prompt Versioner uses SQLite with a local database file:

```python
from prompt_versioner import PromptVersioner

# Default configuration (creates database in project folder)
pv = PromptVersioner(project_name="my-project")

# Custom database path
pv = PromptVersioner(
    project_name="my-project",
    db_path="/path/to/your/database.db"
)

# Disable Git integration
pv = PromptVersioner(
    project_name="my-project",
    enable_git=False
)
```

## 🔗 Git Integration

Configure Git integration for version control:

```python
# Initialize with Git tracking enabled
pv = PromptVersioner(
    project_name="my-project",
    enable_git=True,
    git_repo="/path/to/git/repo"
)

# Install Git hooks for automatic tracking
pv.install_git_hooks()

# Later, uninstall if needed
pv.uninstall_git_hooks()
```

## 📊 Performance Monitoring

Set up custom monitoring for your prompts:

```python
def monitor_performance(pv, prompt_name):
    """Simple performance monitoring"""
    latest = pv.get_latest(prompt_name)
    version_data = pv.get_version(prompt_name, latest["version"])
    metrics = pv.storage.get_metrics(version_id=version_data["id"])

    if metrics:
        recent_metrics = metrics[-10:]  # Last 10 calls
        avg_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)
        avg_latency = sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics)

        # Check thresholds
        if avg_quality < 0.7:
            print(f"⚠️ Low quality: {avg_quality:.2f}")
        if avg_latency > 5000:
            print(f"⚠️ High latency: {avg_latency:.0f}ms")
        else:
            print(f"✅ Performance OK: Quality {avg_quality:.2f}, Latency {avg_latency:.0f}ms")

# Monitor your prompts
monitor_performance(pv, "my_prompt")
```

## 📝 Best Practices

1. **Environment Separation**: Use different projects for dev/staging/production
2. **Secure Paths**: Use secure database locations for sensitive data
3. **Git Integration**: Enable Git for version control and team collaboration
4. **Regular Monitoring**: Set up performance monitoring with thresholds
5. **Documentation**: Use annotations to document changes and decisions

## 🔍 Quick Validation

Test your configuration:

```python
from prompt_versioner import PromptVersioner, VersionBump

def validate_setup(project_name, db_path):
    """Quick setup validation"""
    try:
        pv = PromptVersioner(project_name=project_name, db_path=db_path)

        # Test basic operations
        pv.save_version(
            name="test_prompt",
            system_prompt="Test system prompt",
            user_prompt="Test user prompt",
            bump_type=VersionBump.MAJOR
        )

        # Clean up
        pv.delete_prompt("test_prompt")

        print("✅ Configuration valid!")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

# Validate
validate_setup("my-project", "./test.db")
```

Ready to get started? Check out the [Quick Start Guide](quick-start.md) or learn about [Basic Usage](../examples/basic-usage.md).
