# Quick Start

This guide will help you get started with Prompt Versioner in just a few minutes.

## Basic Setup

### 1. Initialize Your Project

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner for your project
pv = PromptVersioner(project_name="my-ai-project", enable_git=False)
```

### 2. Create Your First Prompt

```python
# Save your first prompt version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer with deep knowledge of software engineering.",
    user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={
        "type": "code_review",
        "author": "team",
        "model_target": "gpt-4o",
        "use_case": "pull_request_review"
    }
)
```

### 3. Retrieve and Use Prompts

```python
# Get the latest version
latest = pv.get_latest("code_reviewer")
print(f"✅ Latest version: {latest['version']}")

# Use the prompt in your application
system_prompt = latest["system_prompt"]
user_prompt = latest["user_prompt"].format(code="def hello(): print('world')")
```

### 4. Track Metrics

```python
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

print("📊 Metrics logged successfully!")
```

## Launch the Web Dashboard

The easiest way to manage your prompts is through the web interface:

```bash
# Quick start - auto-detects database in current directory
pv dashboard

# Custom configuration
pv dashboard --port 8080 --host 0.0.0.0 --project my-project

# With custom database path
pv dashboard --db-path /path/to/prompts.sqlite --port 5000
```

## Complete Example

Here's a complete working example:

```python title="complete_example.py"
from prompt_versioner import PromptVersioner, VersionBump
import time

# Initialize versioner
pv = PromptVersioner(project_name="tutorial", enable_git=False)

# Create a summarization prompt
pv.save_version(
    name="summarizer",
    system_prompt="You are a skilled text summarizer.",
    user_prompt="Summarize this text in 2-3 sentences:\n{text}",
    bump_type=VersionBump.MAJOR,
    metadata={"domain": "general", "max_length": "3_sentences"}
)

# Simulate using the prompt
latest = pv.get_latest("summarizer")
print(f"Using prompt version: {latest['version']}")

# Simulate LLM call metrics
pv.log_metrics(
    name="summarizer",
    version=latest["version"],
    model_name="gpt-4o",
    input_tokens=120,
    output_tokens=45,
    latency_ms=340.2,
    quality_score=0.89,
    success=True
)

# Create an improved version
pv.save_version(
    name="summarizer",
    system_prompt="You are an expert text summarizer with focus on key insights.",
    user_prompt="Create a concise summary highlighting the main points:\n{text}",
    bump_type=VersionBump.MINOR,  # Now version 1.1.0
    metadata={"domain": "general", "improvement": "better_instructions"}
)

# List all versions
versions = pv.list_versions("summarizer")
for v in versions:
    print(f"Version {v['version']}: {v['timestamp']}")
```

## CLI Quick Reference

Essential CLI commands to get you started:

```bash
# Initialize a new project
pv init

# List all prompts
pv list

# Show versions of a prompt
pv versions summarizer

# Show details of a specific version
pv show summarizer 1.0.0

# Compare two versions
pv diff summarizer 1.0.0 1.1.0

# Launch web dashboard
pv dashboard --port 5000
```

## What's Next?

Now that you have the basics working, explore these advanced features:

- **[Version Management](guide/version-management.md)**: Learn advanced versioning strategies
- **[A/B Testing](guide/ab-testing.md)**: Compare prompt performance scientifically
- **[Performance Monitoring](guide/performance-monitoring.md)**: Set up automated alerts
- **[Web Dashboard](dashboard/overview.md)**: Explore the full web interface

## Need Help?

- Check the [API Reference](api/core.md) for detailed documentation
- Browse [Examples](examples/basic.md) for more use cases
- [Open an issue](https://github.com/pepes97/prompt-versioner/issues) if you find bugs
