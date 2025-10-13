# Versioner

The `PromptVersioner` class is the main entry point for the Prompt Versioner library. It provides a high-level interface for managing prompts, versions, metrics, and testing.

## Overview

The `PromptVersioner` class orchestrates all the components of the system, providing a unified API for:

- Creating and managing prompts
- Version control and history tracking
- Metrics collection and analysis
- A/B testing coordination
- Performance monitoring

## Class Reference

The main `PromptVersioner` class can be found in `prompt_versioner.core.versioner.PromptVersioner`.

### Key Methods

- `save_prompt()` - Create a new prompt
- `create_version()` - Create a new version of an existing prompt
- `get_prompt()` - Retrieve a prompt by ID
- `render_prompt()` - Render a prompt with variables
- `track_metrics()` - Track performance metrics
- `search_prompts()` - Search prompts by criteria

## Usage Examples

### Basic Initialization

```python
from prompt_versioner import PromptVersioner

# Default configuration
versioner = PromptVersioner()

# Custom database path
versioner = PromptVersioner(db_path="/path/to/prompts.db")

# With Git integration
versioner = PromptVersioner(
    db_path="prompts.db",
    git_repo="/path/to/git/repo"
)
```

### Creating and Managing Prompts

```python
# Create a new prompt
prompt_id = versioner.save_prompt(
    content="You are a {role}. Please help with: {task}",
    variables={"role": "assistant", "task": "coding"},
    tags=["development", "assistant"],
    description="General development assistant"
)

# Get a prompt
prompt = versioner.get_prompt(prompt_id)
print(f"Current version: {prompt['current_version']}")

# List all prompts
prompts = versioner.list_prompts()
for prompt in prompts:
    print(f"{prompt['id']}: {prompt['description']}")
```

### Version Management

```python
# Create a new version
new_version = versioner.create_version(
    prompt_id=prompt_id,
    content="You are an expert {role}. Please assist with: {task}",
    bump_type="minor",
    description="Enhanced expertise"
)

# Get version history
history = versioner.get_version_history(prompt_id)
for version in history:
    print(f"v{version['version']}: {version['description']}")

# Get specific version
version_data = versioner.get_prompt_version(prompt_id, "1.1.0")
```

### Metrics Tracking

```python
# Track metrics for a prompt usage
versioner.track_metrics(
    prompt_id=prompt_id,
    version="1.1.0",
    llm_response="Here's how to solve your coding problem...",
    input_tokens=50,
    output_tokens=200,
    latency=1.5,
    cost=0.003,
    quality_score=0.85,
    metadata={"model": "gpt-4", "temperature": 0.7}
)

# Get metrics for analysis
metrics = versioner.get_metrics(prompt_id, version="1.1.0")
print(f"Average quality: {metrics['avg_quality']:.2f}")
print(f"Average latency: {metrics['avg_latency']:.2f}s")
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

### Advanced Configuration

```python
from prompt_versioner.config import Config

config = Config(
    database_path="/opt/prompts/prod.db",
    enable_metrics=True,
    enable_git_tracking=True,
    git_repository="/opt/git/prompts",
    alert_thresholds={
        "quality_score": 0.7,
        "latency": 5.0,
        "cost": 0.1
    }
)

versioner = PromptVersioner(config=config)
```

## Integration Patterns

### With OpenAI

```python
import openai
from prompt_versioner import PromptVersioner

versioner = PromptVersioner()
client = openai.OpenAI()

def call_llm_with_tracking(prompt_id, version, variables):
    # Get and render prompt
    rendered = versioner.render_prompt(prompt_id, version, variables)

    # Make LLM call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": rendered}],
        max_tokens=150
    )

    # Track metrics
    versioner.track_metrics(
        prompt_id=prompt_id,
        version=version,
        llm_response=response.choices[0].message.content,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        cost=calculate_cost(response.usage),
        metadata={"model": "gpt-4"}
    )

    return response.choices[0].message.content

# Usage
result = call_llm_with_tracking(
    prompt_id="my-prompt-id",
    version="1.1.0",
    variables={"role": "teacher", "task": "explain quantum physics"}
)
```

### With A/B Testing

```python
from prompt_versioner.testing import ABTest

# Create A/B test
ab_test = ABTest(
    name="Assistant Personality Test",
    versioner=versioner
)

ab_test.add_variant("formal", prompt_id, "1.0.0", 50)
ab_test.add_variant("casual", prompt_id, "1.1.0", 50)

test_id = ab_test.start()

# Use in production
def get_prompt_for_user(user_id):
    variant = ab_test.get_variant(user_id)
    return versioner.render_prompt(
        prompt_id=variant["prompt_id"],
        version=variant["version"],
        variables=get_user_context(user_id)
    )
```

## Error Handling

```python
from prompt_versioner.exceptions import (
    PromptNotFoundError,
    VersionNotFoundError,
    InvalidBumpTypeError
)

try:
    # This might fail if prompt doesn't exist
    prompt = versioner.get_prompt("non-existent-id")
except PromptNotFoundError as e:
    print(f"Prompt not found: {e}")

try:
    # This might fail if version doesn't exist
    version = versioner.get_prompt_version(prompt_id, "999.0.0")
except VersionNotFoundError as e:
    print(f"Version not found: {e}")

try:
    # This might fail with invalid bump type
    versioner.create_version(
        prompt_id=prompt_id,
        content="new content",
        bump_type="invalid"
    )
except InvalidBumpTypeError as e:
    print(f"Invalid bump type: {e}")
```

## Performance Considerations

### Batch Operations

```python
# Batch create prompts
prompt_data = [
    {
        "content": "Prompt 1: {variable}",
        "variables": {"variable": "value1"},
        "tags": ["batch1"]
    },
    {
        "content": "Prompt 2: {variable}",
        "variables": {"variable": "value2"},
        "tags": ["batch2"]
    }
]

prompt_ids = versioner.batch_create_prompts(prompt_data)

# Batch track metrics
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
