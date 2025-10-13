# Analyzer

The `prompt_versioner.metrics.analyzer` module provides functionality for analyzing and comparing metrics between versions.

## MetricsAnalyzer

Static class for analyzing and comparing metrics between different versions.

### Methods

#### compare_metrics()

```python
@staticmethod
    def compare_metrics(
        baseline_metrics: Dict[str, List[float]],
        new_metrics: Dict[str, List[float]],
    ) -> List[MetricComparison]
```

Compares metrics between two versions.

**Parameters:**
- `baseline_metrics` (Dict[str, List[float]]): Baseline version metrics
- `new_metrics` (Dict[str, List[float]]): New version metrics

**Returns:**
- `List[MetricComparison]`: List of MetricComparison objects

**Example:**
```python
from prompt_versioner.metrics.analyzer import MetricsAnalyzer

baseline = {
    "latency_ms": [100, 110, 95, 105],
    "cost_eur": [0.001, 0.0012, 0.0011, 0.0013]
}

new = {
    "latency_ms": [85, 90, 80, 88],
    "cost_eur": [0.0008, 0.0009, 0.0007, 0.0010]
}

comparisons = MetricsAnalyzer.compare_metrics(baseline, new)
for comp in comparisons:
    status = "improved" if comp.improved else "regressed"
    print(f"{comp.metric_name}: {comp.mean_pct_change:.1f}% ({status})")
```

#### format_comparison()

```python
@staticmethod
    def format_comparison(comparisons: List[MetricComparison]) -> str
```


Formats metric comparisons as readable text.

**Parameters:**
- `comparisons` (List[MetricComparison]): List of MetricComparison objects

**Returns:**
- `str`: Formatted string

**Example:**
```python
formatted = MetricsAnalyzer.format_comparison(comparisons)
print(formatted)
# Output:
# ================================================================================
# METRICS COMPARISON
# ================================================================================
#
# LATENCY_MS:
#   Baseline: 102.5000 (±6.4550)
#   New:      85.7500 (±4.3507)
#   Change:   ↑ 16.7500 (-16.34%) ✓ IMPROVED
```

#### detect_regressions()

```python
@staticmethod
    def detect_regressions(
        comparisons: List[MetricComparison],
        threshold: float = 0.05,
    ) -> List[MetricComparison]
```

Detects regressions in metrics.

**Parameters:**
- `comparisons` (List[MetricComparison]): List of MetricComparison objects
- `threshold` (float): Relative threshold for regression (default: 0.05 = 5%)

**Returns:**
- `List[MetricComparison]`: List of regressed metrics

**Example:**
```python
regressions = MetricsAnalyzer.detect_regressions(comparisons, threshold=0.10)
if regressions:
    print("Regressions detected:")
    for reg in regressions:
        print(f"- {reg.metric_name}: {reg.mean_pct_change:.1f}%")
```

#### get_best_version()

```python
@staticmethod
    def get_best_version(
        versions_metrics: Dict[str, Dict[str, List[float]]],
        metric_name: str,
        higher_is_better: bool = True,
    ) -> tuple[str, float]
```

Finds the best version for a specific metric.

**Parameters:**
- `versions_metrics` (Dict[str, Dict[str, List[float]]]): Dict version -> metrics
- `metric_name` (str): Name of the metric to compare
- `higher_is_better` (bool): Whether higher values are better (default: True)

**Returns:**
- `tuple[str, float]`: Tuple (best_version_name, best_value)

**Example:**
```python
versions = {
    "v1.0.0": {"accuracy": [0.85, 0.87, 0.86]},
    "v1.1.0": {"accuracy": [0.90, 0.92, 0.91]},
    "v1.2.0": {"accuracy": [0.88, 0.89, 0.87]}
}

best_version, best_score = MetricsAnalyzer.get_best_version(
    versions, "accuracy", higher_is_better=True
)
print(f"Best version: {best_version} (accuracy: {best_score:.3f})")
```

#### rank_versions()

```python
@staticmethod
    def rank_versions(
        versions_metrics: Dict[str, Dict[str, List[float]]],
        metric_name: str,
        higher_is_better: bool = True,
    ) -> List[tuple[str, float]]
```

Ranks all versions for a specific metric.

**Parameters:**
- `versions_metrics` (Dict[str, Dict[str, List[float]]]): Dict version -> metrics
- `metric_name` (str): Name of the metric for ranking
- `higher_is_better` (bool): Whether higher values are better (default: True)

**Returns:**
- `List[tuple[str, float]]`: List of tuples (version_name, mean_value) ordered by ranking

**Example:**
```python
rankings = MetricsAnalyzer.rank_versions(versions, "accuracy")
print("Ranking by accuracy:")
for i, (version, score) in enumerate(rankings, 1):
    print(f"{i}. {version}: {score:.3f}")
```

#### calculate_improvement_score()

```python
@staticmethod
    def calculate_improvement_score(
        comparisons: List[MetricComparison], weights: Dict[str, float] | None = None
    ) -> float
```

Calculates an overall improvement score from comparisons.

**Parameters:**
- `comparisons` (List[MetricComparison]): List of MetricComparison objects
- `weights` (Dict[str, float] | None): Optional weights for each metric (default: equal weights)

**Returns:**
- `float`: Overall improvement score (from -100 to +100)

**Example:**
```python
# Custom weights to give more importance to latency
weights = {
    "latency_ms": 2.0,
    "cost_eur": 1.0,
    "accuracy": 1.5
}

improvement_score = MetricsAnalyzer.calculate_improvement_score(comparisons, weights)
print(f"Improvement score: {improvement_score:.1f}")

if improvement_score > 0:
    print("✓ Overall improvement")
elif improvement_score < -5:
    print("✗ Significant regression")
else:
    print("≈ Stable performance")
```

## Improvement Logic

The analyzer automatically determines if a metric is improved based on its type:

- **HIGHER_IS_BETTER**: accuracy, throughput, success_rate, etc.
- **LOWER_IS_BETTER**: latency_ms, cost_eur, error_rate, etc.

The mapping is defined in `MetricType` and `METRIC_DIRECTIONS` in the metrics models.

## Ranking Algorithms

### Improvement Score
The improvement score is calculated as a weighted average of percent changes:

```
score = Σ(weight_i * pct_change_i) / Σ(weight_i)
```

Where:
- `pct_change_i` is the percent change for metric i
- `weight_i` is the weight assigned to metric i
- The result is limited between -100 and +100
## See Also
- [`Calculator`](calculator.md) - Utility for single-call metric calculations
- [`Aggregator`](aggregator.md) - Functionality to aggregate metrics across multiple test runs
- [`Models`](models.md) - Data models for metrics and comparison structures
- [`Pricing`](pricing.md) - Manages model pricing and calculates LLM call costs
- [`Tracker`](tracker.md) - Functionality for tracking and statistical analysis of metrics
