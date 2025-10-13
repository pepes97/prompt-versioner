# Quick Start

Get up and running with **Prompt Versioner** in just a few minutes!

## 🚀 Your First Prompt

Let's start by creating and versioning your first prompt:

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize the versioner
pv = PromptVersioner(project_name="my-first-project", enable_git=False)

# Create your first prompt version
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful assistant.",
    user_prompt="Please answer the following question: {question}",
    bump_type=VersionBump.MAJOR
)

print("✅ Created first prompt version 1.0.0!")
```

## 📝 Creating Versions

Improve the prompt and create a new version:

```python
# Create an improved version
pv.save_version(
    name="assistant",
    system_prompt="You are an expert AI tutor with deep knowledge.",
    user_prompt="Please provide a comprehensive answer to: {question}",
    bump_type=VersionBump.MINOR  # Creates 1.1.0
)

print("✅ Created version 1.1.0!")
```

## 📊 Tracking Metrics

Track the performance of your prompts:

```python
# Log performance metrics after using a prompt
pv.log_metrics(
    name="assistant",
    version="1.1.0",
    model_name="gpt-4o-mini",
    input_tokens=25,
    output_tokens=150,
    latency_ms=2300,
    quality_score=0.85,
    success=True
)

print("📊 Metrics tracked successfully!")
```

## 🔍 Using Your Prompts

Get prompts and their versions:

```python
# Get the latest version
latest = pv.get_latest("assistant")
print(f"Latest version: {latest['version']}")
print(f"System prompt: {latest['system_prompt']}")

# Get a specific version
v1_prompt = pv.get_version("assistant", "1.0.0")
print(f"V1.0.0 system prompt: {v1_prompt['system_prompt']}")

# List all versions
versions = pv.list_versions("assistant")
for v in versions:
    print(f"  v{v['version']} - {v['timestamp']}")
```

## 🧪 Basic A/B Testing

Compare two prompt versions:

```python
from prompt_versioner import ABTest

# Create an A/B test
ab_test = ABTest(
    versioner=pv,
    prompt_name="assistant",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score"
)

# Simulate test results
for i in range(15):
    ab_test.log_result("a", 0.7 + (i * 0.01))  # Version A
    ab_test.log_result("b", 0.8 + (i * 0.01))  # Version B

# Get results
if ab_test.is_ready(min_samples=10):
    result = ab_test.get_result()
    print(f"🏆 Winner: Version {result.winner}")
    print(f"📈 Improvement: {result.improvement:.1f}%")
```

## 🎯 What's Next?

Now that you've got the basics down, explore more:

- **[Configuration](configuration.md)**: Customize your setup
- **[Basic Usage](../examples/basic-usage.md)**: Learn with practical examples
- **[Core Concepts](../user-guide/core-concepts.md)**: Understand the architecture
- **[Version Management](../user-guide/version-management.md)**: Advanced versioning strategies
