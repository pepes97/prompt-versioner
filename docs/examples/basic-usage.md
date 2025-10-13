# Basic Usage

This guide covers the fundamental usage patterns of **Prompt Versioner** with practical, real-world examples.

## 🚀 Getting Started

### Simple Prompt Creation

```python
from prompt_versioner import PromptVersioner

# Initialize versioner
versioner = PromptVersioner(db_path="my_prompts.db")

# Create your first prompt
prompt_id = versioner.save_prompt(
    content="You are a helpful assistant. Please answer this question: {question}",
    variables={"question": "What is artificial intelligence?"},
    tags=["assistant", "general", "educational"],
    description="General purpose Q&A assistant"
)

print(f"Created prompt: {prompt_id}")
```

### Basic Version Management

```python
# Improve the prompt - create a minor version
v1_1 = versioner.create_version(
    prompt_id=prompt_id,
    content="You are a knowledgeable AI assistant. Please provide a detailed answer to: {question}",
    bump_type="minor",
    description="Enhanced with 'knowledgeable' and 'detailed' instructions"
)

print(f"Created version: {v1_1}")  # Output: 1.1.0

# Create a major revision with different structure
v2_0 = versioner.create_version(
    prompt_id=prompt_id,
    content="""Role: You are an expert AI assistant with deep knowledge across multiple domains.

Task: Answer the following question with accuracy and clarity.

Question: {question}

Requirements:
- Provide factual, well-reasoned answers
- Include relevant examples when helpful
- Acknowledge uncertainty when appropriate

Response:""",
    bump_type="major",
    description="Restructured with clear role, task, and requirements sections"
)

print(f"Created major version: {v2_0}")  # Output: 2.0.0
```

## 📊 Tracking Performance

### Basic Metrics Tracking

```python
import time
import openai

# Simulate LLM usage with metrics tracking
def use_prompt_with_tracking(prompt_id, version, user_question):
    # Render the prompt
    rendered = versioner.render_prompt(
        prompt_id=prompt_id,
        version=version,
        variables={"question": user_question}
    )

    # Simulate LLM call (replace with your actual LLM)
    start_time = time.time()

    # Example with OpenAI
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": rendered}],
        max_tokens=200
    )

    end_time = time.time()
    latency = end_time - start_time

    # Track metrics
    versioner.track_metrics(
        prompt_id=prompt_id,
        version=version,
        llm_response=response.choices[0].message.content,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        latency=latency,
        cost=calculate_openai_cost(response.usage),  # Your cost calculation
        quality_score=0.85,  # Manual or automated assessment
        metadata={
            "model": "gpt-3.5-turbo",
            "user_question": user_question,
            "temperature": 0.7
        }
    )

    return response.choices[0].message.content

def calculate_openai_cost(usage):
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
