# AB Test

The `prompt_versioner.testing.ab_test` module provides a framework for A/B testing between prompt versions.

## ABTest

Class to implement A/B tests and compare performance between two prompt versions.

### Constructor

```python
def __init__(
        self,
        versioner: Any,
        prompt_name: str,
        version_a: str,
        version_b: str,
        metric_name: str = "quality_score",
    ):
```

**Parameters:**
- `versioner` (Any): Instance of PromptVersioner
- `prompt_name` (str): Name of the prompt to test
- `version_a` (str): First version (baseline)
- `version_b` (str): Second version (challenger)
- `metric_name` (str): Metric to compare (default: "quality_score")

### Methods

#### log_result()

```python
def log_result(self, version: str, metric_value: float) -> None
```

Logs a test result for a specific version.

**Parameters:**
- `version` (str): Which version ('a' or 'b')
- `metric_value` (float): Value of the metric

**Raises:**
- `ValueError`: If the version is not 'a' or 'b'

**Example:**
```python
from prompt_versioner.testing.ab_test import ABTest

# Initialize A/B test
ab_test = ABTest(
    versioner=versioner,
    prompt_name="email_classifier",
    version_a="v1.0.0",
    version_b="v1.1.0",
    metric_name="accuracy"
)

# Log results for version A
ab_test.log_result("a", 0.85)
ab_test.log_result("a", 0.87)
ab_test.log_result("a", 0.84)

# Log results for version B
ab_test.log_result("b", 0.90)
ab_test.log_result("b", 0.92)
ab_test.log_result("b", 0.89)
```

#### log_batch_results()

```python
def log_batch_results(self, version: str, metric_values: List[float]) -> None
```

Logs multiple results at once for a version.

**Parameters:**
- `version` (str): Which version ('a' or 'b')
- `metric_values` (List[float]): List of metric values

**Example:**
```python
# Log batch results
results_a = [0.85, 0.87, 0.84, 0.86, 0.88]
results_b = [0.90, 0.92, 0.89, 0.91, 0.93]

ab_test.log_batch_results("a", results_a)
ab_test.log_batch_results("b", results_b)
```

#### get_result()

```python
def get_result(self) -> ABTestResult
```

Gets the A/B test result with statistical analysis.

**Returns:**
- `ABTestResult`: Object with winner and statistics

**Raises:**
- `ValueError`: If there is not enough data for both versions

**Example:**
```python
result = ab_test.get_result()
print(f"Winner: {result.winner}")
print(f"Improvement: {result.improvement:.2f}%")
print(f"Confidence: {result.confidence:.2f}")
```

#### print_result()

```python
def print_result(self) -> None
```

Prints the A/B test result in a readable format.

**Example:**
```python
ab_test.print_result()
# Output:
# ================================================================================
# A/B TEST RESULT: email_classifier
# ================================================================================
# Version A (v1.0.0): accuracy = 0.8560 (±0.0151)
# Version B (v1.1.0): accuracy = 0.9100 (±0.0141)
#
# 🎉 WINNER: v1.1.0 with 6.31% improvement
# Confidence: 85%
```

#### clear_results()

```python
def clear_results(self) -> None
```

Clears all logged results.

**Example:**
```python
ab_test.clear_results()
# Removes all data to restart the test
```

#### get_sample_counts()

```python
def get_sample_counts(self) -> tuple[int, int]
```

Gets the number of samples for each version.

**Returns:**
- `tuple[int, int]`: Tuple (count_a, count_b)

**Example:**
```python
count_a, count_b = ab_test.get_sample_counts()
print(f"Version A: {count_a} samples")
print(f"Version B: {count_b} samples")
```

#### is_ready()

```python
def is_ready(self, min_samples: int = 30) -> bool
```

Checks if enough samples have been collected for reliable results.

**Parameters:**
- `min_samples` (int): Minimum number of samples per version (default: 30)

**Returns:**
- `bool`: True if both versions have enough samples

**Example:**
```python
if ab_test.is_ready(min_samples=50):
    result = ab_test.get_result()
    ab_test.print_result()
else:
    count_a, count_b = ab_test.get_sample_counts()
    print(f"Need more data: A={count_a}, B={count_b}")
```

## Complete Workflow

Example of a complete usage of the A/B testing framework:

```python
from prompt_versioner.testing.ab_test import ABTest
from prompt_versioner import PromptVersioner
import random

# 1. Initialize versioner and test
versioner = PromptVersioner("my_prompts.db")
ab_test = ABTest(
    versioner=versioner,
    prompt_name="sentiment_analysis",
    version_a="v1.0.0",
    version_b="v1.1.0",
    metric_name="accuracy"
)

# 2. Simulate data collection in production
def simulate_production_testing():
    # Simulate results for version A (baseline)
    for _ in range(100):
        # Simulate baseline accuracy ~0.85
        accuracy_a = random.normalvariate(0.85, 0.05)
        accuracy_a = max(0, min(1, accuracy_a))  # Clamp 0-1
        ab_test.log_result("a", accuracy_a)

    # Simulate results for version B (improved)
    for _ in range(100):
        # Simulate improved accuracy ~0.89
        accuracy_b = random.normalvariate(0.89, 0.04)
        accuracy_b = max(0, min(1, accuracy_b))  # Clamp 0-1
        ab_test.log_result("b", accuracy_b)

# 3. Monitor test progress
def monitor_test():
    count_a, count_b = ab_test.get_sample_counts()
    print(f"Progress: A={count_a}, B={count_b}")

    if ab_test.is_ready(min_samples=30):
        print("✓ Enough samples for preliminary analysis")

        result = ab_test.get_result()
        if result.confidence > 0.8:
            print("✓ High confidence in results")
            return True
        else:
            print("⚠️  Low confidence, keep collecting data")

    return False

# 4. Run test
print("🧪 Starting A/B test...")
simulate_production_testing()

# 5. Analyze results
if monitor_test():
    print("\n📊 Final results:")
    ab_test.print_result()

    result = ab_test.get_result()

    # Decision based on results
    if result.improvement > 5.0 and result.confidence > 0.8:
        print(f"\n🚀 Promote {result.winner} to production!")
    elif result.improvement < 1.0:
        print("\n📊 No significant difference, keep current version")
    else:
        print("\n⏳ Collect more data before deciding")
```

## Statistical Analysis

### Winner Calculation

The winner is determined by comparing means:
- **Winner**: Version with the highest mean
- **Improvement**: `|mean_b - mean_a| / mean_a * 100`

### Confidence Calculation

Confidence is calculated considering:
1. **Sample size**: `min(samples) / 30.0`
2. **Variance**: Penalty for high variance in data
3. **Simplified formula**: In production use proper t-tests

```python
confidence = min(min_samples / 30.0, 1.0)
if high_variance:
    confidence *= variance_penalty
```

### Recommendations

- **Minimum samples**: At least 30 per version for reliable results
- **Significance**: Improvement > 5% with confidence > 80%
- **Test duration**: Continue until results stabilize
- **Balancing**: Keep a 50/50 ratio between versions during the test

## Integration with Metrics

The A/B test can use any tracked metric:

```python
# Test for different metrics
test_accuracy = ABTest(versioner, "classifier", "v1", "v2", "accuracy")
test_latency = ABTest(versioner, "classifier", "v1", "v2", "latency_ms")
test_cost = ABTest(versioner, "classifier", "v1", "v2", "cost_eur")

# Multi-metric analysis
results = {
    "accuracy": test_accuracy.get_result(),
    "latency": test_latency.get_result(),
    "cost": test_cost.get_result()
}

for metric, result in results.items():
    print(f"{metric}: {result.winner} wins by {result.improvement:.1f}%")
```

## See Also

- [`Runner`](runner.md) - Framework for testing
