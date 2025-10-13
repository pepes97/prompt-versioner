# Basic Usage

Get started with **Prompt Versioner** - learn the fundamentals through practical examples.

## 🚀 Quick Start

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
pv = PromptVersioner(project_name="my-first-project", enable_git=False)

# Save your first prompt version
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful AI assistant.",
    user_prompt="Please help me with: {query}",
    bump_type=VersionBump.MAJOR,  # Creates v1.0.0
)

print("🎉 Your first prompt version is saved!")
```

## 📝 Creating Versions

### Your First Versions

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize
pv = PromptVersioner(project_name="learning-prompts", enable_git=False)

# Create initial version
pv.save_version(
    name="email_writer",
    system_prompt="You are a professional email writing assistant.",
    user_prompt="Write a professional email about: {topic}",
    bump_type=VersionBump.MAJOR,  # Creates 1.0.0
    metadata={"type": "email", "author": "me"}
)

# Improve the prompt
pv.save_version(
    name="email_writer",
    system_prompt="You are a professional email writing assistant. Always be polite and concise.",
    user_prompt="Write a professional, polite email about: {topic}\n\nKeep it concise and friendly.",
    bump_type=VersionBump.MINOR,  # Creates 1.1.0
    metadata={"improvement": "added politeness and conciseness"}
)

# Fix a typo
pv.save_version(
    name="email_writer",
    system_prompt="You are a professional email writing assistant. Always be polite and concise.",
    user_prompt="Write a professional, polite email about: {topic}\n\nKeep it concise and friendly.",  # Fixed typo
    bump_type=VersionBump.PATCH,  # Creates 1.1.1
    metadata={"fix": "typo correction"}
)

print("✅ Created 3 versions: 1.0.0, 1.1.0, 1.1.1")
```

### Version Types Explained

```python
# MAJOR version (1.0.0 → 2.0.0) - Breaking changes
pv.save_version(
    name="translator",
    system_prompt="You are a language translator.",
    user_prompt="Translate to {language}: {text}",
    bump_type=VersionBump.MAJOR
)

# MINOR version (2.0.0 → 2.1.0) - New features
pv.save_version(
    name="translator",
    system_prompt="You are a language translator. Provide context when helpful.",
    user_prompt="Translate to {language}: {text}\n\nProvide brief context if the translation might be ambiguous.",
    bump_type=VersionBump.MINOR
)

# PATCH version (2.1.0 → 2.1.1) - Small fixes
pv.save_version(
    name="translator",
    system_prompt="You are a language translator. Provide context when helpful.",
    user_prompt="Translate to {language}: {text}\n\nProvide brief context if the translation might be ambiguous.",
    bump_type=VersionBump.PATCH
```

## 🔍 Working with Versions

### Getting Your Versions

```python
# Get the latest version
latest = pv.get_latest("email_writer")
print(f"Latest version: {latest['version']}")
print(f"System prompt: {latest['system_prompt']}")
print(f"User prompt: {latest['user_prompt']}")

# Get a specific version
version_1_0 = pv.get_version("email_writer", "1.0.0")
print(f"Version 1.0.0 system prompt: {version_1_0['system_prompt']}")

# List all versions (newest first)
versions = pv.list_versions("email_writer")
print(f"All versions:")
for v in versions:
    print(f"  v{v['version']} - {v['timestamp']}")

# List all your prompts
all_prompts = pv.list_prompts()
print(f"All prompts: {all_prompts}")
```

### Comparing Versions

```python
# See what changed between versions
diff = pv.diff("email_writer", "1.0.0", "1.1.0", format_output=True)
# This will print a formatted diff showing the changes

# Get diff details
print(f"Changes summary: {diff.summary}")
print(f"Number of changes: {len(diff.changes)}")
```

## 📊 Tracking Performance

### Basic Metrics Tracking

```python
# Log performance metrics after using a prompt
pv.log_metrics(
    name="email_writer",
    version="1.1.0",
    model_name="gpt-4o-mini",
    input_tokens=50,
    output_tokens=120,
    latency_ms=340,
    quality_score=0.9,  # Your assessment (0.0 to 1.0)
    success=True
)

print("📊 Metrics logged!")

# Check how many metrics you have
version_data = pv.get_version("email_writer", "1.1.0")
metrics = pv.storage.get_metrics(version_id=version_data["id"])
print(f"Total metrics recorded: {len(metrics)}")
```

## 🧪 Simple A/B Testing

### Compare Two Versions

```python
from prompt_versioner import ABTest
import random

# Create an A/B test
ab_test = ABTest(
    versioner=pv,
    prompt_name="email_writer",
    version_a="1.0.0",  # Original version
    version_b="1.1.0",  # Improved version
    metric_name="quality_score"
)

# Simulate some test results
print("🧪 Running A/B test simulation...")

# Version A results (original)
for i in range(15):
    score = random.uniform(0.7, 0.85)  # Slightly lower performance
    ab_test.log_result("a", score)

# Version B results (improved)
for i in range(15):
    score = random.uniform(0.8, 0.95)  # Better performance
    ab_test.log_result("b", score)

# Get results
if ab_test.is_ready(min_samples=10):
    result = ab_test.get_result()
    print(f"🏆 Winner: Version {result.winner}")
    print(f"📈 Improvement: {result.improvement:.1f}%")
    print(f"🎯 Confidence: {result.confidence:.1%}")

    # Print detailed report
    ab_test.print_result()
else:
    print("Need more test data")
```

## 📁 Saving and Sharing

### Export Your Prompts

```python
from pathlib import Path

# Export a single prompt with all versions
pv.export_prompt(
    name="email_writer",
    output_file=Path("email_writer_backup.json"),
    format="json",
    include_metrics=True
)

print("💾 Exported email_writer to backup file")

# Export all prompts
pv.export_all(
    output_dir=Path("all_prompts_backup"),
    format="json"
)

print("💾 Exported all prompts to backup folder")
```

## 🏷️ Adding Notes

### Document Your Changes

```python
# Add notes to document your changes
pv.add_annotation(
    name="email_writer",
    version="1.1.0",
    text="Added politeness instructions. Tested with 20 examples, quality improved by 12%.",
    author="me"
)

# Add another note
pv.add_annotation(
    name="email_writer",
    version="1.1.0",
    text="Works especially well for business communications and customer service emails.",
    author="me"
)

# Read your notes
annotations = pv.get_annotations("email_writer", "1.1.0")
print(f"📝 Notes for email_writer v1.1.0:")
for note in annotations:
    print(f"  {note['author']}: {note['text']}")
```

## 🧹 Clean Up

### Delete Versions You Don't Need

```python
# Delete a specific version (be careful!)
success = pv.delete_version("email_writer", "1.0.0")
if success:
    print("🗑️ Deleted version 1.0.0")

# Delete an entire prompt (use with caution!)
# success = pv.delete_prompt("old_prompt_name")
```
## 📚 Next Steps

Ready to learn more advanced features?

- [Version Management](../user-guide/version-management.md) - Advanced version control techniques
- [Metrics Tracking](../user-guide/metrics-tracking.md) - Comprehensive performance monitoring
- [A/B Testing](../user-guide/ab-testing.md) - Scientific prompt optimization
- [Performance Monitoring](../user-guide/performance-monitoring.md) - Monitor your prompts in production
- [Advanced Workflows](advanced-workflows.md)
