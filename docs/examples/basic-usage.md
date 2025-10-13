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

### Understanding Your Performance

```python
def analyze_prompt_performance(pv, prompt_name, version):
    """Simple performance analysis"""

    # Get the version and its metrics
    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"])

    if not metrics:
        print("No metrics found for this version")
        return

    # Calculate averages
    total_calls = len(metrics)
    avg_quality = sum(m.get("quality_score", 0) for m in metrics) / total_calls
    avg_latency = sum(m.get("latency_ms", 0) for m in metrics) / total_calls
    success_rate = sum(1 for m in metrics if m.get("success", True)) / total_calls
    total_cost = sum(m.get("cost_eur", 0) for m in metrics)

    print(f"📈 Performance for {prompt_name} v{version}:")
    print(f"  Total calls: {total_calls}")
    print(f"  Average quality: {avg_quality:.2f}")
    print(f"  Average latency: {avg_latency:.1f}ms")
    print(f"  Success rate: {success_rate:.1%}")
    print(f"  Total cost: €{total_cost:.4f}")

# Analyze your prompt
analyze_prompt_performance(pv, "email_writer", "1.1.0")
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

### Import Prompts

```python
# Import prompts from a file
result = pv.import_prompt(
    input_file=Path("email_writer_backup.json"),
    overwrite=False  # Don't overwrite existing versions
)

print(f"📥 Import results:")
print(f"  Prompt: {result['prompt_name']}")
print(f"  Imported: {result['imported']} versions")
print(f"  Skipped: {result['skipped']} versions")
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

## 🎯 Real-World Example

### Complete Workflow

```python
from prompt_versioner import PromptVersioner, VersionBump
import random
import time

# 1. Initialize for your project
pv = PromptVersioner(project_name="customer-support-ai", enable_git=False)

# 2. Create your first prompt
pv.save_version(
    name="support_assistant",
    system_prompt="You are a helpful customer support assistant.",
    user_prompt="Help the customer with: {issue}",
    bump_type=VersionBump.MAJOR,
    metadata={"created_for": "customer support team", "initial_version": True}
)

# 3. Test it and log performance
for i in range(10):
    # Simulate using the prompt
    quality = random.uniform(0.75, 0.9)
    latency = random.uniform(300, 600)

    pv.log_metrics(
        name="support_assistant",
        version="1.0.0",
        model_name="gpt-4o-mini",
        input_tokens=random.randint(80, 150),
        output_tokens=random.randint(100, 200),
        latency_ms=latency,
        quality_score=quality,
        success=True,
        metadata={"test_round": i+1}
    )

# 4. Analyze performance
def get_performance_summary(pv, prompt_name, version):
    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"])

    avg_quality = sum(m.get("quality_score", 0) for m in metrics) / len(metrics)
    avg_latency = sum(m.get("latency_ms", 0) for m in metrics) / len(metrics)

    return {"quality": avg_quality, "latency": avg_latency, "samples": len(metrics)}

perf = get_performance_summary(pv, "support_assistant", "1.0.0")
print(f"📊 Initial performance: Quality={perf['quality']:.2f}, Latency={perf['latency']:.0f}ms")

# 5. Improve the prompt based on results
pv.save_version(
    name="support_assistant",
    system_prompt="You are a helpful and empathetic customer support assistant. Always acknowledge the customer's concern first.",
    user_prompt="The customer has this issue: {issue}\n\nPlease help them solve it step by step.",
    bump_type=VersionBump.MINOR,
    metadata={"improvement": "added empathy and structure", "based_on_testing": True}
)

# 6. Document the improvement
pv.add_annotation(
    name="support_assistant",
    version="1.1.0",
    text="Added empathy and step-by-step structure based on initial testing. Expect improved customer satisfaction.",
    author="me"
)

# 7. Test the improved version
for i in range(10):
    quality = random.uniform(0.85, 0.95)  # Better performance
    latency = random.uniform(280, 550)

    pv.log_metrics(
        name="support_assistant",
        version="1.1.0",
        model_name="gpt-4o-mini",
        input_tokens=random.randint(90, 160),
        output_tokens=random.randint(120, 220),
        latency_ms=latency,
        quality_score=quality,
        success=True,
        metadata={"test_round": i+1, "improved_version": True}
    )

# 8. Compare versions
new_perf = get_performance_summary(pv, "support_assistant", "1.1.0")
print(f"📈 Improved performance: Quality={new_perf['quality']:.2f}, Latency={new_perf['latency']:.0f}ms")

improvement = ((new_perf['quality'] - perf['quality']) / perf['quality']) * 100
print(f"🎉 Quality improvement: {improvement:.1f}%")

# 9. Export for backup
pv.export_prompt(
    name="support_assistant",
    output_file=Path("support_assistant_backup.json"),
    include_metrics=True
)

print("✅ Complete workflow finished!")
```

## 🎓 What You've Learned

After completing these examples, you now know how to:

- ✅ Create and manage prompt versions
- ✅ Track performance with metrics
- ✅ Compare versions to see improvements
- ✅ Run simple A/B tests
- ✅ Export and import prompts
- ✅ Add documentation with annotations
- ✅ Analyze your prompt performance

## 📚 Next Steps

Ready to learn more advanced features?

- [Version Management](../user-guide/version-management.md) - Advanced version control techniques
- [Metrics Tracking](../user-guide/metrics-tracking.md) - Comprehensive performance monitoring
- [A/B Testing](../user-guide/ab-testing.md) - Scientific prompt optimization
- [Performance Monitoring](../user-guide/performance-monitoring.md) - Monitor your prompts in production

## 💡 Tips for Success

1. **Start Small**: Begin with simple prompts and basic metrics
2. **Be Consistent**: Use consistent naming and versioning practices
3. **Document Everything**: Add annotations to explain your changes
4. **Test Regularly**: Use metrics and A/B testing to validate improvements
5. **Export Regularly**: Keep backups of your important prompts

Happy prompt versioning! 🚀
    # Example cost calculation for GPT-3.5-turbo
    input_cost = usage.prompt_tokens * 0.0015 / 1000
    output_cost = usage.completion_tokens * 0.002 / 1000
    return input_cost + output_cost

# Use the prompt
answer = use_prompt_with_tracking(
    prompt_id=prompt_id,
    version="1.1.0",
    user_question="What are the main types of machine learning?"
)

print(f"Answer: {answer}")
```

### Analyzing Performance

```python
# Get performance metrics
metrics = versioner.get_metrics(prompt_id, version="1.1.0")

print(f"Total uses: {metrics['total_uses']}")
print(f"Average quality: {metrics['avg_quality']:.2f}")
print(f"Average latency: {metrics['avg_latency']:.2f}s")
print(f"Total cost: ${metrics['total_cost']:.4f}")
print(f"Average cost per use: ${metrics['avg_cost']:.4f}")

# Compare versions
v1_0_metrics = versioner.get_metrics(prompt_id, version="1.0.0")
v1_1_metrics = versioner.get_metrics(prompt_id, version="1.1.0")

quality_improvement = v1_1_metrics['avg_quality'] - v1_0_metrics['avg_quality']
print(f"Quality improvement from v1.0.0 to v1.1.0: {quality_improvement:.3f}")
```

## 🏷️ Organization and Discovery

### Using Tags Effectively

```python
# Create prompts with hierarchical tags
customer_service_prompt = versioner.save_prompt(
    content="You are a {tone} customer service representative. Help resolve: {issue}",
    variables={"tone": "friendly and professional", "issue": "billing inquiry"},
    tags=[
        "domain:customer-service",
        "type:support",
        "tone:professional",
        "language:english",
        "team:support"
    ],
    description="Customer service issue resolution"
)

marketing_prompt = versioner.save_prompt(
    content="Create a {type} marketing copy for {product}. Target audience: {audience}",
    variables={
        "type": "compelling",
        "product": "SaaS platform",
        "audience": "small business owners"
    },
    tags=[
        "domain:marketing",
        "type:copywriting",
        "tone:persuasive",
        "language:english",
        "team:marketing"
    ],
    description="Marketing copy generation"
)

# Search by tags
customer_service_prompts = versioner.search_prompts(
    tags=["domain:customer-service"],
    tag_operator="AND"
)

professional_prompts = versioner.search_prompts(
    tags=["tone:professional", "language:english"],
    tag_operator="AND"
)

print(f"Found {len(customer_service_prompts)} customer service prompts")
print(f"Found {len(professional_prompts)} professional English prompts")
```

### Advanced Search

```python
# Search with multiple criteria
high_quality_prompts = versioner.search_prompts(
    content_contains="helpful",
    tags=["type:assistant"],
    quality_score_min=0.8,
    created_after="2025-01-01",
    sort_by="quality_score",
    sort_order="desc",
    limit=10
)

for prompt in high_quality_prompts:
    print(f"{prompt['description']}: Quality {prompt['avg_quality']:.2f}")
```

## 🔄 Template and Variable Patterns

### Dynamic Role-Based Prompts

```python
# Create a flexible role-based template
role_template_id = versioner.save_prompt(
    content="""You are a {role} with {experience_level} experience in {domain}.

Your personality traits:
- {trait_1}
- {trait_2}
- {trait_3}

Task: {task}

Context: {context}

Please provide a response that reflects your role and expertise.""",
    variables={
        "role": "software engineer",
        "experience_level": "senior",
        "domain": "web development",
        "trait_1": "detail-oriented",
        "trait_2": "collaborative",
        "trait_3": "solution-focused",
        "task": "code review",
        "context": "React component with performance issues"
    },
    tags=["template", "role-based", "flexible"],
    description="Flexible role-based prompt template"
)

# Use for different scenarios
scenarios = [
    {
        "role": "data scientist",
        "experience_level": "expert",
        "domain": "machine learning",
        "trait_1": "analytical",
        "trait_2": "methodical",
        "trait_3": "research-oriented",
        "task": "analyze dataset patterns",
        "context": "Customer churn data with 50+ features"
    },
    {
        "role": "product manager",
        "experience_level": "senior",
        "domain": "SaaS products",
        "trait_1": "strategic",
        "trait_2": "user-focused",
        "trait_3": "data-driven",
        "task": "prioritize feature requests",
        "context": "Q1 roadmap with 20+ potential features"
    }
]

for scenario in scenarios:
    rendered = versioner.render_prompt(
        prompt_id=role_template_id,
        variables=scenario
    )
    print(f"\n=== {scenario['role'].title()} Prompt ===")
    print(rendered[:200] + "...")
```

### Conditional Logic in Prompts

```python
# Create prompts with conditional elements
conditional_prompt_id = versioner.save_prompt(
    content="""You are a {assistant_type} assistant.

{expertise_section}

User Request: {user_request}

{additional_instructions}

Please provide a helpful response.""",
    variables={
        "assistant_type": "general",
        "expertise_section": "",
        "user_request": "Help me debug my code",
        "additional_instructions": ""
    },
    tags=["conditional", "flexible"],
    description="Prompt with conditional sections"
)

def render_conditional_prompt(prompt_id, request_type, user_request):
    """Render prompt with conditional logic based on request type"""

    base_vars = {
        "user_request": user_request,
        "additional_instructions": ""
    }

    if request_type == "technical":
        base_vars.update({
            "assistant_type": "technical",
            "expertise_section": "Expertise: Software development, debugging, and system architecture.",
            "additional_instructions": "Provide code examples and technical explanations."
        })
    elif request_type == "creative":
        base_vars.update({
            "assistant_type": "creative",
            "expertise_section": "Expertise: Creative writing, brainstorming, and content creation.",
            "additional_instructions": "Be imaginative and provide multiple creative options."
        })
    else:
        base_vars.update({
            "assistant_type": "general",
            "expertise_section": "I'm here to help with a wide range of topics."
        })

    return versioner.render_prompt(prompt_id, variables=base_vars)

# Usage examples
technical_prompt = render_conditional_prompt(
    conditional_prompt_id,
    "technical",
    "My Python script is throwing a KeyError"
)

creative_prompt = render_conditional_prompt(
    conditional_prompt_id,
    "creative",
    "I need ideas for a blog post about AI"
)
```

## 📈 Performance Monitoring

### Setting Up Monitoring

```python
# Enable performance monitoring
versioner.enable_monitoring(
    prompt_id=prompt_id,
    thresholds={
        "quality_score_min": 0.7,
        "latency_max": 3.0,
        "cost_max": 0.05,
        "error_rate_max": 0.05
    },
    window_size=100  # Monitor last 100 uses
)

# Simulate usage with varying performance
import random

def simulate_usage_with_variance():
    for i in range(50):
        # Simulate some performance variance
        base_quality = 0.85
        quality_variance = random.uniform(-0.1, 0.1)
        quality = max(0, min(1, base_quality + quality_variance))

        base_latency = 1.5
        latency_variance = random.uniform(-0.5, 1.0)
        latency = max(0.1, base_latency + latency_variance)

        versioner.track_metrics(
            prompt_id=prompt_id,
            version="1.1.0",
            llm_response=f"Sample response {i}",
            input_tokens=random.randint(20, 80),
            output_tokens=random.randint(50, 200),
            latency=latency,
            cost=random.uniform(0.001, 0.010),
            quality_score=quality
        )

simulate_usage_with_variance()

# Check for alerts
alerts = versioner.get_active_alerts(prompt_id)
if alerts:
    print("⚠️ Performance alerts:")
    for alert in alerts:
        print(f"  - {alert['type']}: {alert['message']}")
else:
    print("✅ No performance issues detected")
```

### Performance Analysis

```python
# Get detailed performance analysis
analysis = versioner.analyze_performance(prompt_id, version="1.1.0")

print("=== Performance Analysis ===")
print(f"Total uses: {analysis['total_uses']}")
print(f"Quality trend: {analysis['quality_trend']}")  # 'improving', 'stable', 'declining'
print(f"Latency trend: {analysis['latency_trend']}")
print(f"Cost efficiency: {analysis['cost_efficiency']:.2f}")
print(f"Reliability: {analysis['reliability']:.1%}")

# Performance over time
import matplotlib.pyplot as plt

metrics_history = versioner.get_metrics_history(prompt_id, version="1.1.0")

# Plot quality over time
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot([m['timestamp'] for m in metrics_history],
         [m['quality_score'] for m in metrics_history])
plt.title('Quality Score Over Time')
plt.ylabel('Quality Score')
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
plt.plot([m['timestamp'] for m in metrics_history],
         [m['latency'] for m in metrics_history])
plt.title('Latency Over Time')
plt.ylabel('Latency (s)')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
plt.plot([m['timestamp'] for m in metrics_history],
         [m['cost'] for m in metrics_history])
plt.title('Cost Over Time')
plt.ylabel('Cost ($)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
```

## 🔍 Debugging and Troubleshooting

### Common Issues and Solutions

```python
# Issue 1: Prompt not rendering correctly
try:
    rendered = versioner.render_prompt(
        prompt_id=prompt_id,
        variables={"missing_variable": "value"}  # Wrong variable name
    )
except KeyError as e:
    print(f"Missing variable: {e}")

    # Get required variables
    prompt_data = versioner.get_prompt(prompt_id)
    required_vars = prompt_data['variables'].keys()
    print(f"Required variables: {list(required_vars)}")

# Issue 2: Version not found
try:
    version_data = versioner.get_prompt_version(prompt_id, "999.0.0")
except VersionNotFoundError:
    print("Version not found")

    # Get available versions
    history = versioner.get_version_history(prompt_id)
    available_versions = [v['version'] for v in history]
    print(f"Available versions: {available_versions}")

# Issue 3: Performance debugging
def debug_performance_issue(prompt_id, version):
    """Debug performance issues with a prompt"""

    # Get recent metrics
    recent_metrics = versioner.get_metrics(
        prompt_id=prompt_id,
        version=version,
        limit=50,
        order_by="timestamp DESC"
    )

    # Analyze patterns
    quality_scores = [m['quality_score'] for m in recent_metrics if m['quality_score']]
    latencies = [m['latency'] for m in recent_metrics if m['latency']]

    if quality_scores:
        avg_quality = sum(quality_scores) / len(quality_scores)
        quality_variance = max(quality_scores) - min(quality_scores)

        print(f"Quality Analysis:")
        print(f"  Average: {avg_quality:.3f}")
        print(f"  Range: {min(quality_scores):.3f} - {max(quality_scores):.3f}")
        print(f"  Variance: {quality_variance:.3f}")

        if quality_variance > 0.3:
            print("  ⚠️ High quality variance detected")

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)

        print(f"Latency Analysis:")
        print(f"  Average: {avg_latency:.2f}s")
        print(f"  Maximum: {max_latency:.2f}s")

        if max_latency > 5.0:
            print("  ⚠️ High latency detected")

debug_performance_issue(prompt_id, "1.1.0")
```

## 🎯 Best Practices

### 1. Prompt Design Patterns

```python
# Good: Clear structure with descriptive variables
good_prompt = versioner.save_prompt(
    content="""Role: You are a {expert_role} with {years_experience} years of experience.

Task: {primary_task}

Context: {situational_context}

Constraints:
- {constraint_1}
- {constraint_2}

Output Format: {desired_format}

Begin your response:""",
    variables={
        "expert_role": "financial advisor",
        "years_experience": "10",
        "primary_task": "analyze investment portfolio",
        "situational_context": "Market volatility concerns",
        "constraint_1": "Risk tolerance is moderate",
        "constraint_2": "Investment horizon is 5-10 years",
        "desired_format": "Structured recommendations with rationale"
    },
    tags=["financial", "advisory", "structured"],
    description="Structured financial advisory prompt"
)

# Avoid: Unclear, monolithic prompts
avoid_prompt = versioner.save_prompt(
    content="Help me with {stuff} and make sure it's {quality}",
    variables={"stuff": "things", "quality": "good"},
    description="Vague prompt - avoid this pattern"
)
```

### 2. Version Management Strategy

```python
# Strategy: Semantic versioning with clear change descriptions
class PromptEvolution:
    def __init__(self, versioner, base_prompt_id):
        self.versioner = versioner
        self.prompt_id = base_prompt_id

    def fix_typo(self, corrected_content):
        """PATCH version for typos/grammar fixes"""
        return self.versioner.create_version(
            prompt_id=self.prompt_id,
            content=corrected_content,
            bump_type="patch",
            description="Fixed typo/grammar"
        )

    def enhance_clarity(self, improved_content):
        """MINOR version for clarity improvements"""
        return self.versioner.create_version(
            prompt_id=self.prompt_id,
            content=improved_content,
            bump_type="minor",
            description="Enhanced clarity and specificity"
        )

    def restructure_completely(self, new_content):
        """MAJOR version for structural changes"""
        return self.versioner.create_version(
            prompt_id=self.prompt_id,
            content=new_content,
            bump_type="major",
            description="Complete restructure with new format"
        )

# Usage
evolution = PromptEvolution(versioner, prompt_id)
v1_0_1 = evolution.fix_typo("Fixed content...")
v1_1_0 = evolution.enhance_clarity("Clearer content...")
v2_0_0 = evolution.restructure_completely("Completely new structure...")
```

### 3. Metrics Collection Best Practices

```python
def comprehensive_metrics_tracking(versioner, prompt_id, version, llm_call_func, variables):
    """Best practice metrics tracking wrapper"""

    import time
    from datetime import datetime

    # Pre-call setup
    start_time = time.time()
    timestamp = datetime.utcnow()

    try:
        # Make the LLM call
        response_data = llm_call_func(variables)

        # Calculate timing
        end_time = time.time()
        latency = end_time - start_time

        # Extract metrics
        metrics_data = {
            "prompt_id": prompt_id,
            "version": version,
            "llm_response": response_data.get("text", ""),
            "input_tokens": response_data.get("input_tokens", 0),
            "output_tokens": response_data.get("output_tokens", 0),
            "latency": latency,
            "cost": response_data.get("cost", 0),
            "quality_score": assess_quality(response_data.get("text", "")),
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "model": response_data.get("model", "unknown"),
                "temperature": response_data.get("temperature"),
                "variables_used": variables,
                "success": True
            }
        }

        # Track metrics
        versioner.track_metrics(**metrics_data)

        return response_data

    except Exception as e:
        # Track failed attempts too
        versioner.track_metrics(
            prompt_id=prompt_id,
            version=version,
            latency=time.time() - start_time,
            metadata={
                "timestamp": timestamp.isoformat(),
                "error": str(e),
                "success": False,
                "variables_used": variables
            }
        )
        raise

def assess_quality(text):
    """Simple quality assessment - replace with your logic"""
    # This is a placeholder - implement your quality scoring logic
    if len(text) < 10:
        return 0.3  # Too short
    elif len(text) > 2000:
        return 0.7  # Might be too verbose
    else:
        return 0.85  # Reasonable length
```

Ready to explore more advanced features? Check out [Advanced Workflows](advanced-workflows.md) or dive into [A/B Testing](../user-guide/ab-testing.md).
