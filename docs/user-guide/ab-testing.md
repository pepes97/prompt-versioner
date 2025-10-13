# A/B Testing

A concise guide to running A/B tests with Prompt Versioner. Keep this page focused on the common, practical workflows: Quick Start, setting up versions, collecting results, basic analysis and a short example.

## 🧪 Quick Start

```python
from prompt_versioner import PromptVersioner, ABTest
import random

pv = PromptVersioner(project_name="my-project", enable_git=False)

# Prepare versions (assumes 1.0.0 and 1.1.0 exist)
ab_test = ABTest(
    versioner=pv,
    prompt_name="code_reviewer",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score",
)

# Simulate logging
for _ in range(30):
    ab_test.log_result("a", random.uniform(0.70, 0.85))
    ab_test.log_result("b", random.uniform(0.75, 0.90))

if ab_test.is_ready(min_samples=20):
    result = ab_test.get_result()
    print(f"Winner: {result.winner} — improvement: {result.improvement:.2%}, confidence: {result.confidence:.1%}")
```

## 🔧 Setting Up Tests

1. Create the versions you want to compare. Use `pv.save_version(...)` with `VersionBump.MAJOR/MINOR/PATCH` depending on the change.

2. Initialize the `ABTest` with the prompt name and the two versions to compare. Choose a primary metric (e.g., `quality_score`) to evaluate.

```python
from prompt_versioner import PromptVersioner, VersionBump

pv = PromptVersioner(project_name="my-project")

# Baseline
pv.save_version(
    name="summarizer",
    system_prompt="You are a summarization assistant.",
    user_prompt="Summarize: {text}",
    bump_type=VersionBump.MAJOR,
)

# Improved
pv.save_version(
    name="summarizer",
    system_prompt="You are an expert summarizer that produces concise, accurate summaries.",
    user_prompt="Please summarize: {text}",
    bump_type=VersionBump.MINOR,
)

ab_test = ABTest(
    versioner=pv,
    prompt_name="summarizer",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="quality_score",
)
```

## 📊 Collecting Results

- Use `ab_test.log_result(variant, value)` to add single observations (variant is "a" or "b").
- For batch uploads, use `ab_test.log_batch_results(variant, list_of_values)` where available.
- Integrate logging into your production path: after an LLM call, evaluate the response and log the metric.

```python
# Example after calling the LLM and computing a quality_score
ab_test.log_result("a", quality_score)
pv.log_metrics(name="summarizer", version="1.1.0", model_name="gpt-4o", quality_score=quality_score, success=True)
```

## 📈 Analyzing Results

- Check sample counts with `ab_test.get_sample_counts()`.
- When `ab_test.is_ready(min_samples)` is True, call `ab_test.get_result()` to get summary stats (means, samples, winner, confidence).
- Use `ab_test.print_result()` for a human-readable report.

```python
count_a, count_b = ab_test.get_sample_counts()
print(f"Samples: A={count_a}, B={count_b}")

if ab_test.is_ready(min_samples=30):
    result = ab_test.get_result()
    print(result)
    ab_test.print_result()
```

## ⚖️ Best Practices (Short)

- Test one change at a time. Keep tests focused.
- Define the primary metric and a minimum sample size before starting.
- Randomize assignment to avoid bias.
- Monitor test health (latency, errors) alongside quality metrics.

## 🧩 Short Example

A short, complete example showing the minimal end-to-end flow.

```python
from prompt_versioner import PromptVersioner, VersionBump, ABTest
import random

pv = PromptVersioner(project_name="quick-ab")

pv.save_version(name="g", system_prompt="You are helpful.", user_prompt="Q:{q}", bump_type=VersionBump.MAJOR)
pv.save_version(name="g", system_prompt="You are concise and helpful.", user_prompt="Q:{q}", bump_type=VersionBump.MINOR)

ab = ABTest(versioner=pv, prompt_name="g", version_a="1.0.0", version_b="1.1.0", metric_name="quality_score")
for i in range(40):
    ab.log_result("a", random.uniform(0.6, 0.8))
    ab.log_result("b", random.uniform(0.65, 0.9))

if ab.is_ready(min_samples=20):
    r = ab.get_result()
    ab.print_result()
```

## 📚 Next steps

- [Metrics & Tracking](metrics-tracking.md)
- [Version Management](version-management.md)
