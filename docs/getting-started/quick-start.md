# Quick Start

Get up and running with **Prompt Versioner** in just a few minutes! This guide will walk you through the essential features and basic usage patterns.

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
    bump_type=VersionBump.MAJOR,
    metadata={"created_for": "education", "type": "assistant"}
)

print("✅ Created first prompt version 1.0.0!")
```

## 📝 Creating Versions

Now let's improve the prompt and create a new version:

```python
# Create an improved version
pv.save_version(
    name="assistant",
    system_prompt="You are an expert AI tutor with deep knowledge.",
    user_prompt="Please provide a comprehensive answer to: {question}",
    bump_type=VersionBump.MINOR,  # Creates 1.1.0
    metadata={"improvement": "enhanced with expert persona"}
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
    latency_ms=2300,  # milliseconds
    quality_score=0.85,  # 0-1 scale
    success=True,
    metadata={"model": "gpt-4o-mini", "temperature": 0.7}
)

print("📊 Metrics tracked successfully!")
```

## 🔍 Retrieving and Using Prompts

Get prompts and their versions for use:

```python
# Get the latest version of a prompt
latest = pv.get_latest("assistant")
print(f"Latest version: {latest['version']}")
print(f"System prompt: {latest['system_prompt']}")
print(f"User prompt: {latest['user_prompt']}")

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
    version_a="1.0.0",  # Basic version
    version_b="1.1.0",  # Expert version
    metric_name="quality_score"
)

# Simulate test results
for i in range(20):
    # Version A results (basic)
    score_a = 0.7 + (i * 0.01)  # Gradual improvement
    ab_test.log_result("a", score_a)

    # Version B results (expert)
    score_b = 0.8 + (i * 0.01)  # Better performance
    ab_test.log_result("b", score_b)

# Get results when ready
if ab_test.is_ready(min_samples=15):
    result = ab_test.get_result()
    print(f"🏆 Winner: Version {result.winner}")
    print(f"📈 Improvement: {result.improvement:.1f}%")
    ab_test.print_result()
```

## 📱 Web Dashboard

Launch the interactive web dashboard to visualize your prompts:

```bash
# Start the dashboard (if available)
pv dashboard

# Or start programmatically
pv.start_dashboard(host="0.0.0.0", port=5000)
```

Then open your browser to `http://localhost:5000` to see:

- 📊 **Dashboard Overview**: Metrics and performance summaries
- 📝 **Prompt Management**: Browse, edit, and version prompts
- 🧪 **A/B Testing**: Create and monitor experiments
- 📈 **Analytics**: Detailed performance analysis
- ⚠️ **Alerts**: Monitor for performance regressions

## 🔧 CLI Usage

Use the command-line interface for quick operations:

```bash
# Initialize a new project
pv init my-project

# List all prompts
pv list

# Show prompt details
pv show <prompt-name>

# Compare versions
pv diff <prompt-name> 1.0.0 1.1.0

# Export prompts
pv export <prompt-name> --output backup.json

# Show metrics
pv metrics <prompt-name> --version 1.1.0
```

## 📈 Advanced Example: Complete Workflow

Here's a complete example showing a typical workflow:

```python
from prompt_versioner import PromptVersioner, VersionBump
import time

# Initialize
pv = PromptVersioner(project_name="customer-support", enable_git=False)

# Create base prompt
pv.save_version(
    name="support_agent",
    system_prompt="You are a helpful customer service agent.",
    user_prompt="Customer issue: {issue}\n\nPlease provide assistance:",
    bump_type=VersionBump.MAJOR,
    metadata={"type": "customer-service", "initial": True}
)

# Test and iterate
improvements = [
    "You are a helpful and empathetic customer service agent.",
    "You are a helpful, empathetic, and knowledgeable customer service agent.",
    "You are a professional customer service specialist who provides helpful, empathetic, and accurate assistance."
]

for i, system_prompt in enumerate(improvements, 1):
    # Create improved version
    pv.save_version(
        name="support_agent",
        system_prompt=system_prompt,
        user_prompt="Customer issue: {issue}\n\nPlease provide step-by-step assistance:",
        bump_type=VersionBump.MINOR,
        metadata={"iteration": i, "improvement": "enhanced persona"}
    )

    # Simulate testing and log metrics
    for test_round in range(5):
        pv.log_metrics(
            name="support_agent",
            version=f"1.{i}.0",
            model_name="gpt-4o-mini",
            input_tokens=50 + (i * 5),
            output_tokens=120 + (i * 10),
            latency_ms=1200 + (test_round * 100),
            cost_eur=0.002 + (i * 0.001),
            quality_score=0.7 + (i * 0.05) + (test_round * 0.01),
            success=True,
            metadata={"iteration": i, "test_round": test_round}
        )

    print(f"✅ Completed iteration {i} with version 1.{i}.0")

# Compare performance
latest = pv.get_latest("support_agent")
print(f"🎉 Final version: {latest['version']}")

print("📊 Workflow completed! Check metrics with pv.get_version() for analysis.")
```

## 🎯 What's Next?

Now that you've got the basics down, explore more advanced features:

- **[Core Concepts](../user-guide/core-concepts.md)**: Understand the architecture and design principles
- **[Version Management](../user-guide/version-management.md)**: Advanced versioning strategies
- **[A/B Testing](../user-guide/ab-testing.md)**: Comprehensive testing framework
- **[Performance Monitoring](../user-guide/performance-monitoring.md)**: Set up alerts and monitoring
- **[Web Dashboard](../user-guide/web-dashboard.md)**: Deep dive into the web interface

## 💡 Tips for Success

1. **Start Simple**: Begin with basic version management before adding complex workflows
2. **Track Everything**: The more metrics you track, the better insights you'll gain
3. **Use Tags**: Organize prompts with meaningful tags for easy discovery
4. **Regular Exports**: Backup your prompts regularly using the export feature
5. **Monitor Continuously**: Set up alerts for performance regressions
6. **Collaborate**: Use annotations and the web dashboard for team collaboration

Ready to build better prompts? Let's dive deeper into the [core concepts](../user-guide/core-concepts.md)!
