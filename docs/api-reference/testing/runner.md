# Runner

The `prompt_versioner.testing.runner` module provides a framework for running automated tests on prompts.

## PromptTestRunner

Class for running prompt tests with support for parallel execution and metric collection.

### Constructor

```python
def __init__(self, max_workers: int = 4)
```

**Parameters:**
- `max_workers` (int): Maximum number of parallel workers (default: 4)

### Methods

# run_test()

```python
def run_test(
        self,
        test_case: TestCase,
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
    ) -> TestResult
```

Runs a single test case.

**Parameters:**
- `test_case` (TestCase): Test case to run
- `prompt_fn` (Callable): Function that takes input and returns LLM output
- `metric_fn` (Optional[Callable]): Optional function to compute metrics from output

**Returns:**
- `TestResult`: Object with test results

**Example:**
```python
from prompt_versioner.testing.runner import PromptTestRunner
from prompt_versioner.testing.models import TestCase

# Define prompt function
def my_prompt_function(inputs: Dict[str, Any]) -> str:
    prompt = f"Classify sentiment: {inputs['text']}"
    # Simulate LLM call
    return "positive"

# Define metrics function
def calculate_metrics(output: str) -> Dict[str, float]:
    return {
        "confidence": 0.95,
        "accuracy": 1.0 if output in ["positive", "negative", "neutral"] else 0.0
    }

# Create test case
test_case = TestCase(
    name="sentiment_test_1",
    inputs={"text": "I love this product!"},
    expected_output="positive"
)

# Run test
runner = PromptTestRunner()
result = runner.run_test(test_case, my_prompt_function, calculate_metrics)

print(f"Success: {result.success}")
print(f"Output: {result.output}")
print(f"Duration: {result.duration_ms:.2f}ms")
print(f"Metrics: {result.metrics}")
```

#### run_tests()

```python
def run_tests(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
        parallel: bool = True,
    ) -> List[TestResult]
```

Runs multiple test cases sequentially or in parallel.

**Parameters:**
- `test_cases` (List[TestCase]): List of test cases
- `prompt_fn` (Callable): Prompt function
- `metric_fn` (Optional[Callable]): Optional metrics function
- `parallel` (bool): Whether to run tests in parallel (default: True)

**Returns:**
- `List[TestResult]`: List of test results

**Example:**
```python
# Create multiple test cases
test_cases = [
    TestCase(
        name="positive_sentiment",
        inputs={"text": "I love this!"},
        expected_output="positive"
    ),
    TestCase(
        name="negative_sentiment",
        inputs={"text": "This is terrible"},
        expected_output="negative"
    ),
    TestCase(
        name="neutral_sentiment",
        inputs={"text": "It's okay"},
        expected_output="neutral"
    )
]

# Run all tests
results = runner.run_tests(test_cases, my_prompt_function, calculate_metrics)

# Analyze results
for result in results:
    status = "✓" if result.success else "✗"
    print(f"{status} {result.test_case.name}: {result.output}")
```

#### get_summary()

```python
def get_summary(self, results: List[TestResult]) -> Dict[str, Any]
```

Generates a summary of test results.

**Parameters:**
- `results` (List[TestResult]): List of test results

**Returns:**
- `Dict[str, Any]`: Dictionary with statistics:
  - `total`: Total number of tests
  - `passed`: Number of passed tests
  - `failed`: Number of failed tests
  - `pass_rate`: Success rate
  - `metrics`: Aggregated metric statistics

**Example:**
```python
summary = runner.get_summary(results)
print(f"Pass rate: {summary['pass_rate']:.2%}")
print(f"Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}")
print(f"Metrics: {summary['metrics']}")
```

#### `format_summary(summary: Dict[str, Any]) -> str`

Formats the summary as readable text.

**Parameters:**
- `summary` (Dict[str, Any]): Summary from `get_summary()`

**Returns:**
- `str`: Formatted summary

**Example:**
```python
formatted = runner.format_summary(summary)
print(formatted)
# Output:
# ================================================================================
# TEST SUMMARY
# ================================================================================
# Total: 3 | Passed: 2 | Failed: 1 | Pass Rate: 66.67%
#
# METRICS SUMMARY:
# - duration_ms: mean=45.23, std=12.45, range=[32.10, 58.90]
# - accuracy: mean=0.83, std=0.41, range=[0.00, 1.00]
```

## Complete Workflow

Example of a complete usage of the test runner:

```python
from prompt_versioner.testing.runner import PromptTestRunner
from prompt_versioner.testing.models import TestCase
from typing import Dict, Any
import random

# 1. Define prompt function
def sentiment_classifier(inputs: Dict[str, Any]) -> str:
    """Simulate a sentiment classifier."""
    text = inputs.get("text", "")

    # Simulate classification logic
    if "love" in text.lower() or "great" in text.lower():
        return "positive"
    elif "hate" in text.lower() or "terrible" in text.lower():
        return "negative"
    else:
        return "neutral"

# 2. Define metrics function
def sentiment_metrics(output: str) -> Dict[str, float]:
    """Compute metrics for sentiment output."""
    valid_sentiments = ["positive", "negative", "neutral"]

    return {
        "validity": 1.0 if output in valid_sentiments else 0.0,
        "confidence": random.uniform(0.7, 0.99),  # Simulate confidence
        "response_length": len(output)
    }

# 3. Define custom validation function
def validate_sentiment(output: str) -> bool:
    """Validate that the output is a valid sentiment."""
    return output in ["positive", "negative", "neutral"]

# 4. Create test dataset
test_cases = [
    TestCase(
        name="clearly_positive",
        inputs={"text": "I love this product, it's great!"},
        expected_output="positive",
        validation_fn=validate_sentiment
    ),
    TestCase(
        name="clearly_negative",
        inputs={"text": "I hate this, it's terrible!"},
        expected_output="negative",
        validation_fn=validate_sentiment
    ),
    TestCase(
        name="neutral_text",
        inputs={"text": "This is a product."},
        expected_output="neutral",
        validation_fn=validate_sentiment
    ),
    TestCase(
        name="edge_case_empty",
        inputs={"text": ""},
        expected_output="neutral",
        validation_fn=validate_sentiment
    ),
    TestCase(
        name="mixed_sentiment",
        inputs={"text": "I love the design but hate the price"},
        # No expected_output, use only validation_fn
        validation_fn=validate_sentiment
    )
]

# 5. Initialize runner and run tests
print("🧪 Starting test suite...")
runner = PromptTestRunner(max_workers=2)

# Sequential tests for debugging
print("\n📝 Sequential execution for debugging:")
sequential_results = runner.run_tests(
    test_cases[:2],
    sentiment_classifier,
    sentiment_metrics,
    parallel=False
)

for result in sequential_results:
    status = "✓" if result.success else "✗"
    print(f"{status} {result.test_case.name}: {result.output} ({result.duration_ms:.1f}ms)")

# Parallel tests for speed
print("\n⚡ Full parallel execution:")
all_results = runner.run_tests(
    test_cases,
    sentiment_classifier,
    sentiment_metrics,
    parallel=True
)

# 6. Analyze results
summary = runner.get_summary(all_results)
print(f"\n📊 Results:")
print(f"Pass rate: {summary['pass_rate']:.1%}")
print(f"Tests passed: {summary['passed']}/{summary['total']}")

# 7. Show detailed summary
print("\n" + runner.format_summary(summary))

# 8. Error analysis
failed_tests = [r for r in all_results if not r.success]
if failed_tests:
    print("\n❌ Failed tests:")
    for result in failed_tests:
        print(f"- {result.test_case.name}: {result.error or 'Validation failed'}")
        print(f"  Input: {result.test_case.inputs}")
        print(f"  Output: {result.output}")
        print(f"  Expected: {result.test_case.expected_output}")

# 9. Performance analysis
durations = [r.duration_ms for r in all_results if r.duration_ms]
if durations:
    avg_duration = sum(durations) / len(durations)
    max_duration = max(durations)
    print(f"\n⏱️  Performance:")
    print(f"Average duration: {avg_duration:.1f}ms")
    print(f"Max duration: {max_duration:.1f}ms")
```

## Advanced Features

### Regression Testing

```python
def regression_test_suite():
    """Suite for regression tests."""

    # Historical test cases that must always pass
    regression_cases = [
        TestCase(name="regression_1", inputs={"text": "baseline test"}),
        TestCase(name="regression_2", inputs={"text": "edge case"}),
        # ... other critical tests
    ]

    results = runner.run_tests(regression_cases, sentiment_classifier)

    # Ensure all pass
    all_passed = all(r.success for r in results)
    if not all_passed:
        raise AssertionError("Regression test failed!")

    return results
```

### Performance Testing

```python
def performance_benchmark():
    """Performance benchmark."""

    # Create many test cases for stress testing
    stress_cases = [
        TestCase(
            name=f"perf_test_{i}",
            inputs={"text": f"Performance test number {i}"}
        )
        for i in range(100)
    ]

    # Measure performance
    start_time = time.time()
    results = runner.run_tests(stress_cases, sentiment_classifier, parallel=True)
    total_time = time.time() - start_time

    # Analyze performance metrics
    durations = [r.duration_ms for r in results]
    throughput = len(results) / total_time

    print(f"Throughput: {throughput:.1f} tests/sec")
    print(f"Average latency: {sum(durations)/len(durations):.1f}ms")

    return results
```

### CI/CD Integration

```python
def ci_test_suite() -> bool:
    """Test suite for CI/CD pipeline."""
    try:
        # Run all tests
        results = runner.run_tests(all_test_cases, prompt_function)
        summary = runner.get_summary(results)

        # Success criteria for CI
        success_criteria = {
            "min_pass_rate": 0.95,  # 95% of tests must pass
            "max_avg_duration": 1000,  # Max 1 second on average
        }

        pass_rate = summary["pass_rate"]
        avg_duration = summary["metrics"]["duration_ms"]["mean"]

        # Check criteria
        if pass_rate < success_criteria["min_pass_rate"]:
            print(f"❌ Pass rate too low: {pass_rate:.1%}")
            return False

        if avg_duration > success_criteria["max_avg_duration"]:
            print(f"❌ Average duration too high: {avg_duration:.1f}ms")
            return False

        print(f"✅ CI test passed: {pass_rate:.1%} pass rate, {avg_duration:.1f}ms avg")
        return True

    except Exception as e:
        print(f"❌ CI test failed: {e}")
        return False

# Usage in CI
if __name__ == "__main__":
    import sys
    success = ci_test_suite()
    sys.exit(0 if success else 1)
```

## Error Handling

The runner automatically handles:

- **Timeouts**: Timeout for hanging tests
- **Exceptions**: Catches exceptions and logs them as errors
- **Validation**: Supports custom validation via `validation_fn`
- **Metrics**: Collects metrics even in case of partial errors

### Error Handling Example

```python
def robust_prompt_function(inputs: Dict[str, Any]) -> str:
    """Prompt function with error handling."""
    try:
        text = inputs.get("text", "")
        if not text.strip():
            raise ValueError("Empty input text")

        # Simulate possible failure
        if "error" in text.lower():
            raise RuntimeError("Simulated LLM error")

        return sentiment_classifier(inputs)

    except Exception as e:
        # Log the error but continue with a default value
        print(f"Error in prompt function: {e}")
        return "neutral"  # Default safe value

# The runner will still catch any unhandled exceptions
```

## See Also

- [`A/B Test`](ab-test.md) - AB Testing for testing
