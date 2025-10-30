# Multi-Model Performance Comparison

One of the most powerful features of Prompt Versioner is the ability to test the same prompt across multiple LLM models and automatically compare their performance.

## Overview

When working with LLMs, you often need to answer questions like:
- Which model provides the best quality for my use case?
- Which model is the most cost-effective?
- Which model has the lowest latency?
- How does performance vary across different models?

Prompt Versioner makes this easy by automatically tracking and aggregating metrics per model, allowing you to make data-driven decisions about which model to use in production.

## How It Works

### 1. Save Your Prompt Version

First, create a prompt version as you normally would:

```python
from prompt_versioner import PromptVersioner

pv = PromptVersioner(project_name="model-comparison")

version = pv.save_version(
    name="text-classifier",
    system_prompt="You are an expert text classifier.",
    user_prompt="Classify the following text: {text}"
)
```

### 2. Log Metrics for Multiple Models

When logging metrics, simply specify the `model_name` parameter:

```python
# Test with GPT-4
response = call_gpt4(prompt)
pv.log_metrics(
    prompt_name="text-classifier",
    version=version,
    model_name="gpt-4o",
    prompt_tokens=response.prompt_tokens,
    completion_tokens=response.completion_tokens,
    latency_ms=response.latency,
    quality_score=0.95,
    success=True,
    cost=0.002
)

# Test with Claude
response = call_claude(prompt)
pv.log_metrics(
    prompt_name="text-classifier",
    version=version,
    model_name="claude-3-5-sonnet",
    prompt_tokens=response.prompt_tokens,
    completion_tokens=response.completion_tokens,
    latency_ms=response.latency,
    quality_score=0.93,
    success=True,
    cost=0.0015
)

# Test with Gemini
response = call_gemini(prompt)
pv.log_metrics(
    prompt_name="text-classifier",
    version=version,
    model_name="gemini-pro",
    prompt_tokens=response.prompt_tokens,
    completion_tokens=response.completion_tokens,
    latency_ms=response.latency,
    quality_score=0.91,
    success=True,
    cost=0.001
)
```

### 3. View Comparison in Dashboard

Open the web dashboard and click on any version. You'll see:

1. **Performance Metrics (All Models)**: Aggregated metrics across all models, with weighted averages based on call count
2. **Model Performance Comparison**: Individual cards for each model showing:
   - Total cost
   - Latency range (min-max)
   - Average tokens
   - Average quality

The best-performing model in each category automatically gets a badge:
- ⚡ **Fastest**: Lowest average latency
- 💰 **Cheapest**: Lowest average cost per call
- ⭐ **Best Quality**: Highest average quality score
- ✅ **Most Reliable**: Highest success rate

## Complete Example

See `examples/multi_models.py` for a complete working example that:
- Tests 4 different models (GPT-4, GPT-4 Mini, Claude, Gemini)
- Simulates 250 calls per model with realistic metrics
- Demonstrates variance in performance across models

```bash
python examples/multi_models.py
```

Then launch the dashboard:

```bash
python examples/run_dashboard.py
```

Navigate to the "text-classifier" prompt and click on any version to see the model comparison.

## Metrics Aggregation

### Per-Model Metrics

For each model, the system tracks:
- **Call Count**: Total number of calls
- **Total Cost**: Sum of all costs
- **Average Tokens**: Mean of total tokens (prompt + completion)
- **Latency Range**: Min and max latency observed
- **Average Latency**: Mean latency
- **Average Quality**: Mean quality score
- **Success Rate**: Percentage of successful calls

### Aggregated Metrics (All Models)

The "Performance Metrics" section shows aggregated data across all models using **weighted averages** based on call count:

```python
# Example calculation for average tokens
total_calls = sum(model.call_count for all models)
avg_tokens = sum(model.avg_tokens * model.call_count for all models) / total_calls
```

This ensures that models with more calls have appropriate influence on the aggregated metrics.

## Best Practices

### 1. Consistent Test Data

Use the same test dataset for all models to ensure fair comparison:

```python
test_cases = [
    {"text": "This product is amazing!", "expected": "positive"},
    {"text": "Terrible experience.", "expected": "negative"},
    # ... more test cases
]

for model in ["gpt-4o", "claude-3-5-sonnet", "gemini-pro"]:
    for test_case in test_cases:
        response = call_model(model, test_case["text"])
        quality = calculate_quality(response, test_case["expected"])

        pv.log_metrics(
            prompt_name="classifier",
            version=version,
            model_name=model,
            # ... other metrics
            quality_score=quality
        )
```

### 2. Sufficient Sample Size

Collect enough data points for statistical significance:

```python
CALLS_PER_MODEL = 100  # Minimum recommended

for model in models:
    for i in range(CALLS_PER_MODEL):
        # Make call and log metrics
        pass
```

### 3. Realistic Simulation

When testing, simulate realistic conditions:
- Production-like prompts
- Representative input data
- Real latency (don't use cached responses)
- Actual costs based on provider pricing

### 4. Quality Scoring

Implement consistent quality scoring:

```python
def calculate_quality(response, expected_output):
    """
    Returns a quality score between 0 and 1
    """
    # Example: Simple comparison
    if response.lower() == expected_output.lower():
        return 1.0

    # Example: Similarity scoring
    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, response, expected_output).ratio()
    return similarity
```

## API Integration Examples

### OpenAI

```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

pv.log_metrics(
    prompt_name=name,
    version=version,
    model_name="gpt-4o",
    prompt_tokens=response.usage.prompt_tokens,
    completion_tokens=response.usage.completion_tokens,
    latency_ms=response_time,
    quality_score=evaluate(response.choices[0].message.content),
    success=True,
    cost=calculate_openai_cost(response.usage)
)
```

### Anthropic Claude

```python
import anthropic

response = anthropic.Anthropic().messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
    ]
)

pv.log_metrics(
    prompt_name=name,
    version=version,
    model_name="claude-3-5-sonnet",
    prompt_tokens=response.usage.input_tokens,
    completion_tokens=response.usage.output_tokens,
    latency_ms=response_time,
    quality_score=evaluate(response.content[0].text),
    success=True,
    cost=calculate_anthropic_cost(response.usage)
)
```

### Google Gemini

```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")

pv.log_metrics(
    prompt_name=name,
    version=version,
    model_name="gemini-pro",
    prompt_tokens=response.usage_metadata.prompt_token_count,
    completion_tokens=response.usage_metadata.candidates_token_count,
    latency_ms=response_time,
    quality_score=evaluate(response.text),
    success=True,
    cost=calculate_gemini_cost(response.usage_metadata)
)
```

## Understanding the Results

### Model Cards

Each model card shows:

```
🤖 gpt-4o                    250 calls
⚡ Fastest  💰 Cheapest

💸 Total Cost       €0.0245
📊 Latency Range    450ms - 1850ms
🔢 Avg Tokens       156
⭐ Avg Quality      95.2%
```

### Highlighted Models

Models with the best performance in any category are highlighted with a golden left border and display their achievement badges prominently.

### Making Decisions

Use the comparison to make informed decisions:

1. **Quality-First**: Choose the model with the highest quality score if accuracy is paramount
2. **Cost-Optimized**: Select the cheapest model if budget is a constraint
3. **Latency-Sensitive**: Pick the fastest model for real-time applications
4. **Balanced**: Consider the model that performs well across multiple metrics

## Troubleshooting

### No Model Comparison Shown

If you don't see the model comparison section:
- Ensure you've logged metrics with `model_name` parameter
- Verify that multiple models have been tested for the same version
- Check that the database has been properly updated

### Metrics Not Aggregating

If metrics aren't aggregating correctly:
- Ensure the `version` parameter is exactly the same for all models
- Check that `prompt_name` is consistent
- Verify there are no typos in `model_name`

### Best Model Badges Not Appearing

Badges only appear when:
- Multiple models have been tested (minimum 2)
- There's clear performance difference between models
- Sufficient data has been collected (recommended: 10+ calls per model)

## Next Steps

- Explore [A/B Testing](ab-testing.md) to compare prompt versions
- Learn about [Performance Monitoring](performance-monitoring.md) for production tracking
- Check [Metrics Tracking](metrics-tracking.md) for detailed metric information
