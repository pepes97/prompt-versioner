# Quick Start

Get up and running with **Prompt Versioner** in just a few minutes! This guide will walk you through the essential features and basic usage patterns.

## 🚀 Your First Prompt

Let's start by creating and versioning your first prompt:

```python
from prompt_versioner import PromptVersioner

# Initialize the versioner
versioner = PromptVersioner(db_path="my_prompts.db")

# Create your first prompt
prompt_id = versioner.save_prompt(
    content="You are a helpful assistant. Please answer the following question: {question}",
    variables={"question": "What is machine learning?"},
    tags=["assistant", "education", "ml"],
    description="Basic educational assistant prompt"
)

print(f"Created prompt with ID: {prompt_id}")
# Output: Created prompt with ID: 550e8400-e29b-41d4-a716-446655440000
```

## 📝 Creating Versions

Now let's improve the prompt and create a new version:

```python
# Create an improved version
new_version = versioner.create_version(
    prompt_id=prompt_id,
    content="You are an expert AI tutor. Please provide a comprehensive answer to: {question}",
    bump_type="minor",  # MAJOR, MINOR, or PATCH
    description="Enhanced prompt with expert persona"
)

print(f"Created version: {new_version}")
# Output: Created version: 1.1.0
```

## 📊 Tracking Metrics

Track the performance of your prompts:

```python
# Simulate an LLM call and track metrics
versioner.track_metrics(
    prompt_id=prompt_id,
    version="1.1.0",
    llm_response="Machine learning is a subset of artificial intelligence...",
    input_tokens=25,
    output_tokens=150,
    latency=2.3,  # seconds
    cost=0.004,   # USD
    quality_score=0.85,  # 0-1 scale
    metadata={"model": "gpt-4", "temperature": 0.7}
)

print("Metrics tracked successfully!")
```

## 🔍 Retrieving and Using Prompts

Get prompts and their versions for use:

```python
# Get the latest version of a prompt
prompt_data = versioner.get_prompt(prompt_id)
print(f"Latest version: {prompt_data['current_version']}")
print(f"Content: {prompt_data['content']}")

# Get a specific version
v1_prompt = versioner.get_prompt_version(prompt_id, "1.0.0")
print(f"V1.0.0 content: {v1_prompt['content']}")

# Render prompt with variables
rendered = versioner.render_prompt(
    prompt_id=prompt_id,
    version="1.1.0",
    variables={"question": "What is deep learning?"}
)
print(f"Rendered: {rendered}")
```

## 🧪 Basic A/B Testing

Compare two prompt versions:

```python
from prompt_versioner.testing import ABTest

# Create an A/B test
ab_test = ABTest(
    name="Education Assistant Improvement",
    description="Testing expert vs. basic assistant persona",
    versioner=versioner
)

# Add test variants
ab_test.add_variant(
    name="basic",
    prompt_id=prompt_id,
    version="1.0.0",
    traffic_percentage=50
)

ab_test.add_variant(
    name="expert",
    prompt_id=prompt_id,
    version="1.1.0",
    traffic_percentage=50
)

# Start the test
test_id = ab_test.start()
print(f"A/B test started with ID: {test_id}")

# Get a variant for testing
variant = ab_test.get_variant()
print(f"Selected variant: {variant['name']} (v{variant['version']})")
```

## 📱 Web Dashboard

Launch the interactive web dashboard to visualize your prompts:

```bash
# Start the dashboard
prompt-dashboard

# Or specify custom host/port
prompt-dashboard --host 0.0.0.0 --port 8080
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
# Initialize a new prompt database
pv init --db-path ./prompts.db

# List all prompts
pv prompts list

# Show prompt details
pv prompts show <prompt-id>

# Create a new version
pv prompts version <prompt-id> --bump minor --description "Improved version"

# Export prompts
pv export --output prompts_backup.json

# Show metrics for a prompt
pv metrics show <prompt-id> --version 1.1.0
```

## 📈 Advanced Example: Complete Workflow

Here's a complete example showing a typical workflow:

```python
from prompt_versioner import PromptVersioner
from prompt_versioner.testing import ABTest
import openai

# Initialize
versioner = PromptVersioner(db_path="production_prompts.db")
client = openai.OpenAI()

# Create base prompt
prompt_id = versioner.save_prompt(
    content="System: {system_role}\n\nUser: {user_input}\n\nAssistant:",
    variables={
        "system_role": "You are a helpful customer service agent.",
        "user_input": "I need help with my order."
    },
    tags=["customer-service", "support"],
    description="Customer service base prompt"
)

# Test and iterate
for i, improvement in enumerate([
    "You are a helpful and empathetic customer service agent.",
    "You are a helpful, empathetic, and knowledgeable customer service agent.",
    "You are a professional customer service specialist who provides helpful, empathetic, and accurate assistance."
], 1):

    # Create improved version
    version = versioner.create_version(
        prompt_id=prompt_id,
        content=f"System: {improvement}\n\nUser: {{user_input}}\n\nAssistant:",
        bump_type="minor",
        description=f"Iteration {i}: Enhanced agent persona"
    )

    # Simulate testing with real LLM
    test_input = "I need help with my order."
    rendered_prompt = versioner.render_prompt(
        prompt_id=prompt_id,
        version=version,
        variables={"user_input": test_input}
    )

    # Make LLM call (example)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": rendered_prompt}],
        max_tokens=150
    )

    # Track metrics
    versioner.track_metrics(
        prompt_id=prompt_id,
        version=version,
        llm_response=response.choices[0].message.content,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        latency=1.2,  # You would measure this
        cost=0.002,   # Calculate based on pricing
        quality_score=0.8 + (i * 0.05),  # Simulated improvement
        metadata={
            "model": "gpt-3.5-turbo",
            "test_iteration": i
        }
    )

print("Workflow completed! Check the dashboard for results.")
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
