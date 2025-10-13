# Version Management

Manage prompt versions effectively with **Prompt Versioner**'s semantic versioning system.

## 🔄 Quick Start

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
pv = PromptVersioner(project_name="my-project", enable_git=False)

# Save your first version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer.",
    user_prompt="Review this code:\n{code}",
    bump_type=VersionBump.MAJOR,  # Creates 1.0.0
)

# Create an improved version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer with deep knowledge of software engineering.",
    user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
    bump_type=VersionBump.MINOR,  # Creates 1.1.0
)

# Get latest version
latest = pv.get_latest("code_reviewer")
print(f"Latest: {latest['version']}")

# List all versions
versions = pv.list_versions("code_reviewer")
for v in versions:
    print(f"Version {v['version']}: {v['timestamp']}")
```

## 📝 Semantic Versioning

Prompt Versioner uses semantic versioning (SemVer):

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Small fixes, typos
  │     └────────── New features, improvements
  └──────────────── Breaking changes
```

### Version Types

**PATCH (1.0.1)** - Small corrections:
```python
# Fix typo in prompt
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful assistant.",  # Fixed "helpfull" -> "helpful"
    user_prompt="How can I help you?",
    bump_type=VersionBump.PATCH,
)
```

**MINOR (1.1.0)** - New features:
```python
# Add more detailed instructions
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful assistant. Always be polite and detailed.",
    user_prompt="How can I help you today? Please be specific.",
    bump_type=VersionBump.MINOR,
)
```

**MAJOR (2.0.0)** - Breaking changes:
```python
# Complete redesign
pv.save_version(
    name="assistant",
    system_prompt="You are an AI assistant specialized in technical support.",
    user_prompt="What technical issue can I help you resolve?",
    bump_type=VersionBump.MAJOR,
)
```

## 🔍 Working with Versions

### Getting Versions

```python
# Get specific version
version = pv.get_version("code_reviewer", "1.0.0")
print(f"System: {version['system_prompt']}")
print(f"User: {version['user_prompt']}")

# Get latest version
latest = pv.get_latest("code_reviewer")
print(f"Latest: {latest['version']}")

# List all versions for a prompt
versions = pv.list_versions("code_reviewer")
for v in versions:
    print(f"v{v['version']}: {v['timestamp']}")

# List all prompts
prompts = pv.list_prompts()
print(f"All prompts: {prompts}")
```

### Comparing Versions

```python
# Compare two versions
diff = pv.diff("code_reviewer", "1.0.0", "1.1.0", format_output=True)
print(f"Changes: {diff.summary}")

# Compare multiple versions
comparison = pv.compare_versions("code_reviewer", ["1.0.0", "1.1.0", "1.2.0"])
print(f"Comparison data: {comparison}")
```

### Rolling Back

```python
# Rollback to previous version (creates new version)
new_version_id = pv.rollback("code_reviewer", to_version="1.0.0")
print(f"Rolled back to create new version: {new_version_id}")

# Check what version we're now at
latest = pv.get_latest("code_reviewer")
print(f"Current version: {latest['version']}")
```

## 📊 Tracking Metrics

Track performance for each version:

```python
# Log metrics after using a prompt
pv.log_metrics(
    name="code_reviewer",
    version="1.1.0",
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=250,
    latency_ms=420,
    quality_score=0.92,
    success=True,
)

# Get metrics for a version
version = pv.get_version("code_reviewer", "1.1.0")
metrics = pv.storage.get_metrics(version_id=version["id"])
print(f"Metrics: {len(metrics)} recorded")
```

## 📁 Export

### Export Prompts

```python
from pathlib import Path

# Export single prompt
pv.export_prompt(
    name="code_reviewer",
    output_file=Path("code_reviewer.json"),
    format="json",
    include_metrics=True,
)

# Export all prompts
pv.export_all(
    output_dir=Path("exports"),
    format="json"
)
```

## 🏷️ Annotations

Add notes to specific versions:

```python
# Add annotation
pv.add_annotation(
    name="code_reviewer",
    version="1.1.0",
    text="Improved handling of complex code patterns",
    author="team-lead"
)

# Get annotations
annotations = pv.get_annotations("code_reviewer", "1.1.0")
for note in annotations:
    print(f"{note['author']}: {note['text']}")
```

## 🗑️ Cleanup

```python
# Delete specific version
success = pv.delete_version("code_reviewer", "1.0.0")
print(f"Deleted: {success}")

# Delete entire prompt (all versions)
success = pv.delete_prompt("old_prompt")
print(f"Deleted prompt: {success}")
```

## 📚 Next Steps

- [Metrics Tracking](metrics-tracking.md) - Track prompt performance
- [A/B Testing](ab-testing.md) - Compare versions scientifically
- [Basic Usage](../examples/basic-usage.md) - More examples
