# Aggregator

The `prompt_versioner.metrics.aggregator` module provides functionality to aggregate metrics across multiple test runs.

## MetricAggregator

Class for collecting and aggregating metrics from multiple LLM calls, providing summary statistics.

### Constructor

```python
def __init__(self) -> None
```

Initializes an empty aggregator.

### Add Methods

#### add()

```python
def add(self, metric: ModelMetrics) -> None
```

Adds a single metric to the aggregator.

**Parameters:**
- `metric` (ModelMetrics): ModelMetrics object to add

**Example:**
```python
from prompt_versioner.metrics.aggregator import MetricAggregator
from prompt_versioner.metrics.models import ModelMetrics

aggregator = MetricAggregator()

# Add metrics one at a time
metric1 = ModelMetrics(
    model_name="gpt-4",
    input_tokens=100,
    output_tokens=50,
    cost_eur=0.003,
    latency_ms=1200,
    quality_score=0.92
)

aggregator.add(metric1)
```

#### add_dict()

```python
def add_dict(self, **kwargs: Any) -> None
```

Adds metrics from keyword arguments.

**Parameters:**
- `**kwargs`: Metric fields as keyword arguments

**Example:**
```python
# Add metrics directly from a dictionary
aggregator.add_dict(
    model_name="gpt-3.5-turbo",
    input_tokens=150,
    output_tokens=75,
    cost_eur=0.001,
    latency_ms=800,
    quality_score=0.85,
    success=True
)
```

#### add_batch()

```python
def add_batch(self, metrics: List[ModelMetrics]) -> None
```

Adds multiple metrics at once.

**Parameters:**
- `metrics` (List[ModelMetrics]): List of ModelMetrics objects

**Example:**
```python
# Batch of metrics from a test
test_metrics = [
    ModelMetrics(model_name="gpt-4", quality_score=0.90, cost_eur=0.003),
    ModelMetrics(model_name="gpt-4", quality_score=0.88, cost_eur=0.0035),
    ModelMetrics(model_name="gpt-4", quality_score=0.92, cost_eur=0.0028)
]

aggregator.add_batch(test_metrics)
```

### Analysis Methods

#### get_summary()

```python
def get_summary(self) -> Dict[str, Any]
```

Gets a statistical summary of all aggregated metrics.

**Returns:**
- `Dict[str, Any]`: Dictionary with aggregate statistics

**Included statistics:**
- **Counts**: `call_count`, `success_count`, `failure_count`, `success_rate`
- **Tokens**: `total_tokens`, `avg_input_tokens`, `avg_output_tokens`, `avg_total_tokens`
- **Costs**: `total_cost`, `avg_cost`, `min_cost`, `max_cost`
- **Latency**: `avg_latency`, `min_latency`, `max_latency`, `median_latency`
- **Quality**: `avg_quality`, `min_quality`, `max_quality`
- **Accuracy**: `avg_accuracy`
- **Models**: `models_used`, `primary_model`

**Example:**
```python
# After adding many metrics
summary = aggregator.get_summary()

print(f"Total calls: {summary['call_count']}")
print(f"Success rate: {summary['success_rate']:.2%}")
print(f"Average cost: €{summary['avg_cost']:.4f}")
print(f"Average latency: {summary['avg_latency']:.1f}ms")
print(f"Average quality: {summary['avg_quality']:.2%}")
print(f"Models used: {summary['models_used']}")
print(f"Primary model: {summary['primary_model']}")
```

#### get_summary_by_model()

```python
def get_summary_by_model(self) -> Dict[str, Dict[str, Any]]
```

Gets statistics grouped by model.

**Returns:**
- `Dict[str, Dict[str, Any]]`: Dictionary model -> statistics

**Example:**
```python
# Analysis by model
by_model = aggregator.get_summary_by_model()

for model_name, stats in by_model.items():
    print(f"\n{model_name}:")
    print(f"  Calls: {stats['call_count']}")
    print(f"  Average quality: {stats['avg_quality']:.2%}")
    print(f"  Average cost: €{stats['avg_cost']:.4f}")
    print(f"  Average latency: {stats['avg_latency']:.1f}ms")
    print(f"  Success rate: {stats['success_rate']:.2%}")
```

### Filter Methods

#### get_failures()

```python
def get_failures(self) -> List[ModelMetrics]
```

Gets all metrics that failed.

**Returns:**
- `List[ModelMetrics]`: List of metrics with success=False

**Example:**
```python
failures = aggregator.get_failures()
if failures:
    print(f"❌ {len(failures)} failed calls:")
    for failure in failures:
        print(f"  - {failure.model_name}: {failure.error_message}")
```

#### filter_by_model()

```python
def filter_by_model(self, model_name: str) -> List[ModelMetrics]
```

Filters metrics by model name.

**Parameters:**
- `model_name` (str): Name of the model to filter

**Returns:**
- `List[ModelMetrics]`: List of metrics for the specified model

**Example:**
```python
gpt4_metrics = aggregator.filter_by_model("gpt-4")
print(f"GPT-4 metrics: {len(gpt4_metrics)}")

# Specific analysis for GPT-4
costs = [m.cost_eur for m in gpt4_metrics if m.cost_eur]
avg_cost = sum(costs) / len(costs) if costs else 0
print(f"Average GPT-4 cost: €{avg_cost:.4f}")
```

### Utility Methods

#### clear()

Clears all aggregated metrics.

#### to_list()

Exports metrics as a list of dictionaries.

#### __len__() -> int

Returns the number of aggregated metrics.

#### __iter__()

Allows iteration over metrics.

**Example:**
```python
print(f"Number of metrics: {len(aggregator)}")

# Iterate over all metrics
for metric in aggregator:
    if metric.cost_eur and metric.cost_eur > 0.01:
        print(f"Expensive call: €{metric.cost_eur}")

# Export as list
exported = aggregator.to_list()
```

## Statistical Methods

### Implemented Statistical Calculations

**Average (`_avg`):**
```python
valid_values = [v for v in values if v is not None]
return sum(valid_values) / len(valid_values) if valid_values else 0.0
```

**Median (`_median`):**
```python
valid_values = sorted([v for v in values if v is not None])
n = len(valid_values)
if n % 2 == 0:
    return (valid_values[n // 2 - 1] + valid_values[n // 2]) / 2
else:
    return valid_values[n // 2]
```

**Most common value (`_most_common`):**
```python
from collections import Counter
counter = Counter(values)
most_common = counter.most_common(1)
return most_common[0][0] if most_common else None
```

## See Also
- [`Calculator`](calculator.md) - Utility for single-call metric calculations
- [`Analyzer`](analyzer.md) - Functionality for analyzing and comparing metrics between versions
- [`Models`](models.md) - Data models for metrics and comparison structures
- [`Pricing`](pricing.md) - Manages model pricing and calculates LLM call costs
- [`Tracker`](tracker.md) - Functionality for tracking and statistical analysis of metrics
