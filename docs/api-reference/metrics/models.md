# Models

The `prompt_versioner.metrics.models` module defines data models for metrics and comparison structures.

## ModelMetrics

Dataclass representing metrics for a single LLM call.

### Attributes

#### Model Information
- `model_name` (Optional[str]): Name of the model used

#### Token Usage
- `input_tokens` (Optional[int]): Number of input tokens
- `output_tokens` (Optional[int]): Number of output tokens
- `total_tokens` (Optional[int]): Total number of tokens

#### Costs
- `cost_eur` (Optional[float]): Cost in EUR

#### Performance
- `latency_ms` (Optional[float]): Latency in milliseconds

#### Quality Metrics
- `quality_score` (Optional[float]): Quality score
- `accuracy` (Optional[float]): Accuracy

#### Model Parameters
- `temperature` (Optional[float]): Temperature used
- `max_tokens` (Optional[int]): Maximum number of tokens
- `top_p` (Optional[float]): Top_p value

#### Status
- `success` (bool): Whether the call was successful (default: True)
- `error_message` (Optional[str]): Error message if present

#### Additional Data
- `metadata` (Optional[Dict[str, Any]]): Additional metadata

### Methods

#### to_dict()
```python
def to_dict(self) -> Dict[str, Any]
```
Converts the object to a dictionary.

**Returns:**
- `Dict[str, Any]`: Dictionary representation

#### from_dict()

```python
@classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelMetrics"
```

Creates an instance from a dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Data in dictionary format

**Returns:**
- `ModelMetrics`: New instance

**Example:**
```python
from prompt_versioner.metrics.models import ModelMetrics

# Manual creation
metrics = ModelMetrics(
    model_name="gpt-4",
    input_tokens=100,
    output_tokens=50,
    total_tokens=150,
    cost_eur=0.003,
    latency_ms=1200,
    quality_score=0.95,
    temperature=0.7,
    success=True
)

# Convert to dictionary
data = metrics.to_dict()
print(f"Cost: €{data['cost_eur']}")

# Create from dictionary
metrics_copy = ModelMetrics.from_dict(data)
```

## MetricStats

Dataclass representing a statistical summary of a metric.

### Attributes
- `name` (str): Name of the metric
- `count` (int): Number of values
- `mean` (float): Mean
- `median` (float): Median
- `std_dev` (float): Standard deviation
- `min_val` (float): Minimum value
- `max_val` (float): Maximum value

### Methods

#### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

Converts to dictionary.

#### format() -> str

```python
def format(self) -> str
```

Formats as a readable string.

**Example:**
```python
from prompt_versioner.metrics.models import MetricStats

stats = MetricStats(
    name="latency_ms",
    count=100,
    mean=150.5,
    median=145.0,
    std_dev=25.3,
    min_val=95.0,
    max_val=250.0
)

print(stats.format())
# Output: latency_ms: mean=150.5000, median=145.0000, std=25.3000, range=[95.0000, 250.0000], n=100
```

## MetricComparison

Dataclass representing a comparison between two sets of metrics.

### Attributes
- `metric_name` (str): Name of the metric
- `baseline_mean` (float): Baseline mean
- `new_mean` (float): New version mean
- `mean_diff` (float): Difference between means
- `mean_pct_change` (float): Percent change
- `improved` (bool): Whether the metric improved
- `baseline_stats` (Dict[str, float]): Baseline statistics
- `new_stats` (Dict[str, float]): New version statistics

### Methods

#### format()

```python
def format(self) -> str
```

Formats the comparison as a readable string.

**Example:**
```python
from prompt_versioner.metrics.models import MetricComparison

comparison = MetricComparison(
    metric_name="latency_ms",
    baseline_mean=150.0,
    new_mean=120.0,
    mean_diff=-30.0,
    mean_pct_change=-20.0,
    improved=True,
    baseline_stats={"std_dev": 15.0},
    new_stats={"std_dev": 12.0}
)

print(comparison.format())
# Output: latency_ms: 150.0000 → 120.0000 (↑ 20.00%)
```

## MetricType

Enum defining common metric types for LLM prompts.

### Values

#### Token Metrics
- `INPUT_TOKENS = "input_tokens"`
- `OUTPUT_TOKENS = "output_tokens"`
- `TOTAL_TOKENS = "total_tokens"`

#### Cost Metrics
- `COST = "cost_eur"`
- `COST_PER_TOKEN = "cost_per_token"`

#### Performance Metrics
- `LATENCY = "latency_ms"`
- `THROUGHPUT = "throughput"`

#### Quality Metrics
- `QUALITY = "quality_score"`
- `ACCURACY = "accuracy"`
- `RELEVANCE = "relevance"`
- `COHERENCE = "coherence"`
- `FACTUALITY = "factuality"`
- `FLUENCY = "fluency"`

#### Success Metrics
- `SUCCESS_RATE = "success_rate"`
- `ERROR_RATE = "error_rate"`

**Example:**
```python
from prompt_versioner.metrics.models import MetricType

# Using constants
print(MetricType.LATENCY)  # "latency_ms"
print(MetricType.ACCURACY)  # "accuracy"

# Check if a string is a valid type
metric_name = "cost_eur"
if metric_name in [mt.value for mt in MetricType]:
    print(f"{metric_name} is a valid metric type")
```

## MetricDirection

Enum defining the optimization direction for metrics.

### Values
- `HIGHER_IS_BETTER = "higher"`: Higher values are better
- `LOWER_IS_BETTER = "lower"`: Lower values are better
- `NEUTRAL = "neutral"`: Neutral direction

## METRIC_DIRECTIONS

Dictionary mapping metric types to their optimization direction.

```python
METRIC_DIRECTIONS = {
    MetricType.COST: MetricDirection.LOWER_IS_BETTER,
    MetricType.COST_PER_TOKEN: MetricDirection.LOWER_IS_BETTER,
    MetricType.LATENCY: MetricDirection.LOWER_IS_BETTER,
    MetricType.ERROR_RATE: MetricDirection.LOWER_IS_BETTER,
    MetricType.QUALITY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.ACCURACY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.RELEVANCE: MetricDirection.HIGHER_IS_BETTER,
    MetricType.COHERENCE: MetricDirection.HIGHER_IS_BETTER,
    MetricType.FACTUALITY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.FLUENCY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.THROUGHPUT: MetricDirection.HIGHER_IS_BETTER,
    MetricType.SUCCESS_RATE: MetricDirection.HIGHER_IS_BETTER,
}
```

**Example:**
```python
from prompt_versioner.metrics.models import MetricType, METRIC_DIRECTIONS, MetricDirection

# Check optimization direction
direction = METRIC_DIRECTIONS.get(MetricType.LATENCY, MetricDirection.NEUTRAL)
print(f"For latency, {direction.value} is better")  # "lower is better"

if direction == MetricDirection.LOWER_IS_BETTER:
    print("We aim to reduce latency")
```

## MetricThreshold

Dataclass for configuring warning thresholds for a metric.

### Attributes
- `metric_type` (MetricType): Type of metric
- `warning_threshold` (float): Warning threshold
- `critical_threshold` (float): Critical threshold
- `direction` (MetricDirection): Optimization direction (default: HIGHER_IS_BETTER)

### Methods

#### check()

```python
def check(self, value: float) -> str:
```

Checks if a value meets the thresholds.

**Parameters:**
- `value` (float): Value to check

**Returns:**
- `str`: 'ok', 'warning', or 'critical'

**Example:**
```python
from prompt_versioner.metrics.models import MetricThreshold, MetricType, MetricDirection

# Thresholds for latency (lower is better)
latency_threshold = MetricThreshold(
    metric_type=MetricType.LATENCY,
    warning_threshold=200.0,  # warning if > 200ms
    critical_threshold=500.0,  # critical if > 500ms
    direction=MetricDirection.LOWER_IS_BETTER
)

# Test values
values = [150.0, 250.0, 600.0]
for val in values:
    status = latency_threshold.check(val)
    print(f"Latency {val}ms: {status}")

# Thresholds for accuracy (higher is better)
accuracy_threshold = MetricThreshold(
    metric_type=MetricType.ACCURACY,
    warning_threshold=0.8,   # warning if < 0.8
    critical_threshold=0.6,  # critical if < 0.6
    direction=MetricDirection.HIGHER_IS_BETTER
)

accuracy_values = [0.95, 0.75, 0.5]
for val in accuracy_values:
    status = accuracy_threshold.check(val)
    print(f"Accuracy {val}: {status}")
```

## See Also
- [`Aggregator`](aggregator.md) - Functionality to aggregate metrics across multiple test runs
- [`Analyzer`](analyzer.md) - Functionality for analyzing and comparing metrics between versions
- [`Calculator`](calculator.md) - Utility for single-call metric calculations
- [`Pricing`](pricing.md) - Manages model pricing and calculates LLM call costs
- [`Tracker`](tracker.md) - Functionality for tracking and statistical analysis of metrics
