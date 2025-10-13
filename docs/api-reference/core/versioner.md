# Versioner

The `PromptVersioner` class is the main entry point for the Prompt Versioner library. It provides a high-level interface for managing prompts, versions, metrics, and testing.

## Overview

The `PromptVersioner` class orchestrates all the components of the system, providing a unified API for:

- Creating and managing prompt versions
- Version control and history tracking
- Metrics collection and analysis
- Git integration and tracking
- Import/export functionality

## Class Reference

The main `PromptVersioner` class can be found in `prompt_versioner.core.versioner.PromptVersioner`.

### Key Methods

- `save_version()` - Save a new prompt version
- `get_version()` - Retrieve a specific version
- `get_latest()` - Get the latest version of a prompt
- `list_versions()` - List all versions of a prompt
- `list_prompts()` - List all prompt names
- `log_metrics()` - Track performance metrics
- `diff()` - Compare versions
- `rollback()` - Rollback to a previous version

## Usage Examples

### Basic Initialization

```python
from prompt_versioner import PromptVersioner

# Default configuration (creates prompts.db in current directory)
versioner = PromptVersioner(project_name="my-project")

# Custom database path and disable Git
versioner = PromptVersioner(
    project_name="my-project",
    db_path="/path/to/prompts.db",
    enable_git=False
)

# With Git integration enabled
versioner = PromptVersioner(
    project_name="my-project",
    enable_git=True,
    auto_track=True
)
```

### Creating and Managing Prompt Versions

```python
from prompt_versioner import PromptVersioner, VersionBump

versioner = PromptVersioner(project_name="my-app")

# Save a new prompt version
version_id = versioner.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer.",
    user_prompt="Review this code:\n{code}",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={"type": "code_review", "model_target": "gpt-4"}
)

# Get the latest version
latest = versioner.get_latest("code_reviewer")
print(f"Latest version: {latest['version']}")

# List all prompts
prompts = versioner.list_prompts()
for prompt_name in prompts:
    print(f"Prompt: {prompt_name}")

# List versions for a specific prompt
versions = versioner.list_versions("code_reviewer")
for version in versions:
    print(f"v{version['version']}: {version['timestamp']}")
```

### Version Management

```python
# Create incremental versions
versioner.save_version(
    name="code_reviewer",
    system_prompt="You are an EXPERT code reviewer with deep knowledge.",
    user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
    bump_type=VersionBump.MINOR,  # Creates version 1.1.0
    metadata={"improvement": "enhanced expertise"}
)

# Get a specific version
version_data = versioner.get_version("code_reviewer", "1.0.0")
print(f"System prompt: {version_data['system_prompt']}")
print(f"User prompt: {version_data['user_prompt']}")

# Compare versions
diff = versioner.diff("code_reviewer", "1.0.0", "1.1.0")
print(f"Changes: {diff.summary}")

# Rollback to a previous version
rollback_id = versioner.rollback("code_reviewer", "1.0.0")
print(f"Rolled back, new version ID: {rollback_id}")
```

### Metrics Tracking

```python
# Log metrics for a prompt usage
versioner.log_metrics(
    name="code_reviewer",
    version="1.1.0",
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=250,
    latency_ms=420.5,
    quality_score=0.95,
    cost_eur=0.003,
    temperature=0.7,
    success=True,
    metadata={"user_feedback": "excellent"}
)

# Get metrics for analysis
version = versioner.get_version("code_reviewer", "1.1.0")
metrics = versioner.storage.get_metrics(version_id=version["id"], limit=100)

# Calculate averages
if metrics:
    avg_quality = sum(m["quality_score"] for m in metrics if m["quality_score"]) / len(metrics)
    avg_latency = sum(m["latency_ms"] for m in metrics if m["latency_ms"]) / len(metrics)
    print(f"Average quality: {avg_quality:.2f}")
    print(f"Average latency: {avg_latency:.2f}ms")
```

### Rendering Prompts

```python
# Render a prompt with variables
rendered = versioner.render_prompt(
    prompt_id=prompt_id,
    version="1.1.0",
    variables={
        "role": "Python developer",
        "task": "debugging a memory leak"
    }
)
print(rendered)
# Output: "You are an expert Python developer. Please assist with: debugging a memory leak"

# Render with different variables
rendered = versioner.render_prompt(
    prompt_id=prompt_id,
    variables={"role": "data scientist", "task": "analyzing customer churn"}
)
```

## Configuration Options

### Database Configuration

```python
# SQLite database (default)
versioner = PromptVersioner(db_path="/opt/prompts/production.db")

# In-memory database (for testing)
versioner = PromptVersioner(db_path=":memory:")

# Custom connection string
versioner = PromptVersioner(
    connection_string="postgresql://user:pass@localhost/prompts"
)
```

### Git Integration

```python
# Enable Git tracking
versioner = PromptVersioner(
    db_path="prompts.db",
    git_repo="/path/to/git/repo",
    git_auto_commit=True
)

# Custom Git configuration
git_config = {
    "repository_path": "/path/to/git/repo",
    "auto_commit": True,
    "branch": "prompts",
    "commit_message_template": "feat: {action} prompt {prompt_id} v{version}"
}
versioner = PromptVersioner(git_config=git_config)
```

### Import/Export Operations

```python
from pathlib import Path

# Export a prompt and all its versions
versioner.export_prompt(
    name="code_reviewer",
    output_file=Path("backups/code_reviewer.json"),
    format="json",
    include_metrics=True
)

# Export all prompts
versioner.export_all(
    output_dir=Path("backups/"),
    format="yaml"
)

# Import prompt from file
result = versioner.import_prompt(
    input_file=Path("backups/code_reviewer.json"),
    overwrite=False,
    bump_type=VersionBump.PATCH
)
print(f"Imported {result['imported']} versions, skipped {result['skipped']}")
```

### Annotations and Metadata

```python
# Add annotation to a version
versioner.add_annotation(
    name="code_reviewer",
    version="1.1.0",
    text="This version performs significantly better on Python code",
    author="team@company.com"
)

# Get annotations
annotations = versioner.get_annotations("code_reviewer", "1.1.0")
for annotation in annotations:
    print(f"{annotation['author']}: {annotation['text']}")

# Delete version if needed
success = versioner.delete_version("code_reviewer", "1.0.0")
if success:
    print("Version deleted successfully")

# Delete entire prompt and all versions
success = versioner.delete_prompt("old_prompt")
if success:
    print("Prompt and all versions deleted")
```

## Integration Patterns

### With OpenAI

```python
import openai
from prompt_versioner import PromptVersioner, VersionBump

versioner = PromptVersioner(project_name="openai-integration")
client = openai.OpenAI()

def call_llm_with_tracking(name, version, variables, model="gpt-4o"):
    # Get the prompt version
    prompt_data = versioner.get_version(name, version)
    if not prompt_data:
        raise ValueError(f"Prompt {name} version {version} not found")

    # Render the prompt (simple string formatting for now)
    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data["user_prompt"].format(**variables)

    # Make LLM call
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    latency_ms = (time.time() - start_time) * 1000

    # Track metrics
    versioner.log_metrics(
        name=name,
        version=version,
        model_name=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        latency_ms=latency_ms,
        success=True,
        metadata={"variables": variables}
    )

    return response.choices[0].message.content

# Usage
result = call_llm_with_tracking(
    name="code_reviewer",
    version="1.1.0",
    variables={"code": "def hello(): print('world')"},
    model="gpt-4o"
)
```

### With A/B Testing

```python
from prompt_versioner.testing import ABTest

# Create A/B test comparing two versions
ab_test = ABTest(
    versioner=versioner,
    prompt_name="code_reviewer",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score"
)

# Log test results
for i in range(50):
    # Simulate A/B test with random quality scores
    quality_a = random.uniform(0.7, 0.85)
    quality_b = random.uniform(0.75, 0.90)

    ab_test.log_result("a", quality_a)
    ab_test.log_result("b", quality_b)

# Get results
if ab_test.is_ready(min_samples=20):
    result = ab_test.get_result()
    print(f"Winner: {result.winner}")
    print(f"Improvement: {result.improvement:.2f}%")
    ab_test.print_result()
```

## Testing Integration

```python
# Test a specific version
with versioner.test_version("code_reviewer", "1.1.0") as test_context:
    # Any metrics logged here will be tagged as test metrics
    versioner.log_metrics(
        name="code_reviewer",
        version="1.1.0",
        model_name="gpt-4o",
        quality_score=0.92,
        metadata={"test_case": "unit_test_1"}
    )
```

## Git Integration

```python
# Enable Git hooks for automatic versioning
versioner.install_git_hooks()

# Track decorator automatically creates versions on Git commits
@versioner.track("code_reviewer", auto_commit=True)
def review_code(code):
    # This function will be automatically tracked
    return f"Review of: {code}"

# Uninstall hooks when done
versioner.uninstall_git_hooks()
```

## Error Handling

```python
try:
    # This might fail if prompt doesn't exist
    version = versioner.get_version("non-existent", "1.0.0")
    if not version:
        print("Prompt or version not found")
except Exception as e:
    print(f"Error retrieving version: {e}")

try:
    # This might fail with invalid version string
    versioner.save_version(
        name="test",
        system_prompt="Test",
        user_prompt="Test",
        version="invalid-version-string"
    )
except ValueError as e:
    print(f"Invalid version format: {e}")
```
metrics_data = [
    {
        "prompt_id": prompt_ids[0],
        "version": "1.0.0",
        "input_tokens": 20,
        "output_tokens": 50,
        "latency": 1.2,
        "quality_score": 0.8
    },
    # ... more metrics
]

versioner.batch_track_metrics(metrics_data)
```

### Connection Management

```python
# Use context manager for automatic cleanup
with PromptVersioner(db_path="prompts.db") as versioner:
    prompt_id = versioner.save_prompt(...)
    # Database connection automatically closed
```

## See Also

- [Version Manager](version-manager.md) - Detailed version management
- [Metrics Tracker](../metrics/tracker.md) - Metrics collection and analysis
- [A/B Testing](../testing/ab-test.md) - Experimental testing framework
- [Configuration](../../getting-started/configuration.md) - Setup and configuration guide
