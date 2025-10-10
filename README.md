# Prompt Versioner

A comprehensive Python library for managing, versioning, and monitoring AI prompt performance with built-in A/B testing, metrics tracking, and performance monitoring capabilities.

## Features

- **Semantic Versioning**: Automatic version management with MAJOR/MINOR/PATCH bumps
- **Metrics Tracking**: Comprehensive LLM call metrics (tokens, latency, quality, cost)
- **A/B Testing**: Built-in framework for comparing prompt versions
- **Performance Monitoring**: Automated regression detection and alerting
- **Annotations**: Team collaboration through version annotations
- **Export/Import**: Backup and share prompts with full history
- **Web Dashboard**: Interactive UI for visualization and management
- **Git Integration**: Optional Git integration for version control

## Installation

### Using Poetry (Recommended)

```bash
# Install from GitHub repository
poetry add git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
poetry install
```

### Using pip

```bash
# Install from GitHub repository
pip install git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
pip install -e .
```

## Quick Start

```python
from prompt_versioner.core import PromptVersioner, VersionBump
from prompt_versioner.testing import ABTest
from prompt_versioner.app import PerformanceMonitor

# Initialize versioner
pv = PromptVersioner(project_name="my-ai-project", enable_git=False)

# Save your first prompt version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer.",
    user_prompt="Review this code:\n{code}",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={"type": "code_review", "author": "team"}
)

# Get the latest version
latest = pv.get_latest("code_reviewer")
print(f"Latest version: {latest['version']}")

# Log metrics from your LLM calls
pv.log_metrics(
    name="code_reviewer",
    version=latest["version"],
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=250,
    latency_ms=450.5,
    quality_score=0.92,
    temperature=0.7,
    max_tokens=1000,
    success=True
)
```

## Core Functionality

### 1. Version Management

```python
# Create versions with semantic versioning
pv.save_version(
    name="summarizer",
    system_prompt="You are a skilled summarization assistant.",
    user_prompt="Summarize the following text:\n{text}",
    bump_type=VersionBump.MAJOR,  # MAJOR, MINOR, or PATCH
    metadata={"type": "summarization", "improvement": "better context"}
)

# List all versions
versions = pv.list_versions("summarizer")
for v in versions:
    print(f"Version {v['version']}: {v['created_at']}")

# Get specific version
version_1_0 = pv.get_version("summarizer", "1.0.0")
```

### 2. Metrics Tracking

```python
# Log comprehensive metrics
pv.log_metrics(
    name="summarizer",
    version="1.0.0",
    model_name="claude-sonnet-4",
    input_tokens=500,
    output_tokens=150,
    latency_ms=320.8,
    quality_score=0.95,
    accuracy=0.88,
    temperature=0.5,
    top_p=0.9,
    max_tokens=200,
    success=True
)

# Get metrics summary
summary = pv.get_metrics_summary("summarizer", "1.0.0")
print(f"Average quality: {summary['avg_quality']:.1%}")
print(f"Total cost: ${summary['total_cost']:.4f}")
print(f"Call count: {summary['call_count']}")
```

### 3. A/B Testing

```python
# Set up A/B test
ab_test = ABTest(
    versioner=pv,
    prompt_name="summarizer",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score"
)

# Log results from your LLM calls
def test_prompt_version(version, text):
    # Your LLM call logic here
    result = call_llm(version, text)

    # Log the result
    if version == "1.0.0":
        ab_test.log_result("a", result["quality_score"])
    else:
        ab_test.log_result("b", result["quality_score"])

    return result

# Run tests and get statistical results
ab_test.print_result()
# Output: Statistical significance, confidence intervals, recommendations
```

### 4. Performance Monitoring

```python
monitor = PerformanceMonitor(pv)

# Set up alert handler
def handle_alert(alert):
    print(f"ALERT: {alert.alert_type.value}")
    print(f"Message: {alert.message}")
    # Send to Slack, email, etc.

monitor.add_alert_handler(handle_alert)

# Check for performance regressions
alerts = monitor.check_regression(
    name="summarizer",
    current_version="1.1.0",
    baseline_version="1.0.0",
    thresholds={
        "cost": 0.15,      # 15% cost increase threshold
        "latency": 0.20,   # 20% latency increase threshold
        "quality": -0.05   # 5% quality decrease threshold
    }
)
```

### 5. Annotations and Collaboration

```python
# Add team annotations
pv.add_annotation(
    name="summarizer",
    version="1.0.0",
    text="Works great for technical documents, needs improvement for creative content",
    author="alice@company.com"
)

pv.add_annotation(
    name="summarizer",
    version="1.0.0",
    text="Cost is within budget, quality acceptable",
    author="bob@company.com"
)

# Retrieve annotations
annotations = pv.get_annotations("summarizer", "1.0.0")
for ann in annotations:
    print(f"{ann['author']}: {ann['text']}")
```

### 6. Export and Import

```python
# Export prompts with full history
pv.export_prompt(
    name="summarizer",
    filepath="summarizer_backup.json",
    include_metrics=True,
    include_annotations=True
)

# Import prompts
result = pv.import_prompt("summarizer_backup.json", overwrite=False)
print(f"Imported: {result['imported']}, Skipped: {result['skipped']}")
```

## Web Dashboard

Launch the interactive web dashboard to visualize and manage your prompts:

```bash
# Using the main CLI (auto-detects database in current directory)
pv dashboard --port 5000 --host localhost

# Or run from Python
poetry run python examples/run_dashboard.py

# With custom database path
pv dashboard --db-path /path/to/your/database.sqlite --port 5000

# With custom project name
pv --project my-project dashboard --port 5000
```

The dashboard provides:
- **Prompt Overview**: Visual metrics and version history
- **A/B Test Results**: Statistical analysis and visualizations
- **Performance Monitoring**: Regression detection and alerts
- **Team Annotations**: Collaborative notes and feedback
- **Search and Filtering**: Find prompts by metadata, performance, etc.
- **Dark/Light Mode**: Customizable interface

## Advanced Usage

### Custom Storage Backend

```python
from prompt_versioner.storage import SQLiteStorage

# Custom database location
storage = SQLiteStorage(db_path="custom/path/prompts.db")
pv = PromptVersioner(storage=storage, project_name="my-project")
```

### Git Integration

```python
# Enable Git integration for automatic commits
pv = PromptVersioner(
    project_name="my-project",
    enable_git=True,
    git_repo_path="/path/to/repo"
)

# Each version save will create a Git commit
pv.save_version(
    name="prompt",
    system_prompt="...",
    user_prompt="...",
    bump_type=VersionBump.MINOR,
    commit_message="Improve prompt clarity"
)
```

### Batch Operations

```python
# List all prompts in project
all_prompts = pv.list_prompts()

# Bulk export
for prompt_name in all_prompts:
    pv.export_prompt(prompt_name, f"backups/{prompt_name}.json")

# Search prompts by metadata
code_prompts = [p for p in all_prompts if "code" in p.get("metadata", {}).get("type", "")]
```

## Examples

The [`examples`](examples) directory contains comprehensive examples:

- [`test_all_features.py`](examples/test_all_features.py) - Complete feature demonstration
- [`run_dashboard.py`](examples/run_dashboard.py) - Web dashboard launcher
- [`test_with_metrics.py`](examples/test_with_metrics.py) - Metrics tracking examples

Run the full feature test:

```bash
cd examples
poetry run python test_all_features.py
```

## Configuration

```python
# Advanced configuration
pv = PromptVersioner(
    project_name="my-ai-project",
    enable_git=True,
    git_repo_path="./",
    auto_commit=True,
    storage=custom_storage,
    default_metadata={"team": "ai-team", "environment": "production"}
)
```

## Best Practices

1. **Use Semantic Versioning**: MAJOR for breaking changes, MINOR for improvements, PATCH for fixes
2. **Track All Metrics**: Include quality scores, latency, and cost data
3. **Add Annotations**: Document changes and team feedback
4. **Run A/B Tests**: Validate improvements before production deployment
5. **Monitor Performance**: Set up alerts for regressions
6. **Regular Exports**: Backup your prompt history
7. **Team Collaboration**: Use annotations for code reviews and feedback

## Requirements

- Python 3.11.x
- SQLite (included)
- Optional: Git (for version control integration)

## Contributing

See CONTRIBUTING.md for development setup and guidelines.

## License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.
