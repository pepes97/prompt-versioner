# Calculator

The `prompt_versioner.metrics.calculator` module provides utilities for calculating various metrics and derived scores for LLM calls.

## MetricsCalculator

Class for calculating additional metrics and enriching LLM call data.

### Constructor

```python
def __init__(self, pricing_manager: Optional[PricingManager] = None)
```

**Parameters:**
- `pricing_manager` (Optional[PricingManager]): Custom pricing manager (default: default PricingManager)

### Methods

#### calculate_cost()

```python
def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float
```

Calculates the cost in EUR for a model call.

**Parameters:**
- `model_name` (str): Model name
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens

**Returns:**
- `float`: Cost in EUR

**Example:**
```python
from prompt_versioner.metrics.calculator import MetricsCalculator

calculator = MetricsCalculator()

# Calculate cost for GPT-4
cost = calculator.calculate_cost("gpt-4", input_tokens=100, output_tokens=50)
print(f"Cost: €{cost:.4f}")

# Calculate cost for different models
models_test = [
    ("gpt-3.5-turbo", 200, 100),
    ("gpt-4", 200, 100),
    ("claude-3-haiku", 200, 100)
]

for model, input_tokens, output_tokens in models_test:
    cost = calculator.calculate_cost(model, input_tokens, output_tokens)
    print(f"{model}: €{cost:.4f} per {input_tokens + output_tokens} tokens")
```

#### enrich_metrics()

```python
def enrich_metrics(self, metrics: ModelMetrics) -> ModelMetrics
```

Enriches metrics with automatically calculated values.

**Features:**
- Calculates `total_tokens` if missing
- Calculates `cost_eur` if missing
- Adds derived metrics to metadata:
  - `cost_per_token`: Cost per token
  - `tokens_per_second`: Throughput in tokens/second
  - `cost_per_second`: Cost per second

**Parameters:**
- `metrics` (ModelMetrics): ModelMetrics object to enrich

**Returns:**
- `ModelMetrics`: Enriched object (modifies the original object)

**Example:**
```python
from prompt_versioner.metrics.models import ModelMetrics
from prompt_versioner.metrics.calculator import MetricsCalculator

# Create base metrics
metrics = ModelMetrics(
    model_name="gpt-4",
    input_tokens=150,
    output_tokens=75,
    latency_ms=1200,
    quality_score=0.92
    # cost_eur not specified - will be calculated
    # total_tokens not specified - will be calculated
)

calculator = MetricsCalculator()
enriched = calculator.enrich_metrics(metrics)

print(f"Total tokens: {enriched.total_tokens}")  # 225
print(f"Cost: €{enriched.cost_eur:.4f}")  # Automatically calculated
print(f"Cost per token: €{enriched.metadata['cost_per_token']:.6f}")
print(f"Tokens/sec: {enriched.metadata['tokens_per_second']:.1f}")
print(f"Cost/sec: €{enriched.metadata['cost_per_second']:.4f}")
```

#### calculate_efficiency_score()

```python
def calculate_efficiency_score(self, metrics: ModelMetrics) -> float
```

Calculates an efficiency score (quality per cost).

**Formula:**
```
efficiency = (quality_score / cost_eur) * normalization
```

**Parameters:**
- `metrics` (ModelMetrics): Object with quality_score and cost_eur

**Returns:**
- `float`: Efficiency score (0-100)

**Example:**
```python
# Compare efficiency of different versions
versions = [
    ModelMetrics(quality_score=0.85, cost_eur=0.002),  # Baseline
    ModelMetrics(quality_score=0.90, cost_eur=0.003),  # Higher quality, more expensive
    ModelMetrics(quality_score=0.82, cost_eur=0.001),  # Lower quality, cheaper
]

for i, metrics in enumerate(versions):
    efficiency = calculator.calculate_efficiency_score(metrics)
    print(f"Version {i+1}: Efficiency = {efficiency:.1f}")
    print(f"  Quality: {metrics.quality_score:.2%}")
    print(f"  Cost: €{metrics.cost_eur:.4f}")
```

#### calculate_value_score()

```python
def calculate_value_score(
        self,
        metrics: ModelMetrics,
        quality_weight: float = 0.5,
        cost_weight: float = 0.3,
        latency_weight: float = 0.2,
    ) -> float
```


Calculates an overall value score combining quality, cost, and latency.

**Formula:**
```
value_score = (quality * quality_weight +
               cost_score * cost_weight +
               latency_score * latency_weight) / total_weight
```

**Parameters:**
- `metrics` (ModelMetrics): Object with metrics to evaluate
- `quality_weight` (float): Weight for quality (default: 0.5)
- `cost_weight` (float): Weight for cost (default: 0.3)
- `latency_weight` (float): Weight for latency (default: 0.2)

**Returns:**
- `float`: Value score (0-100)

**Example:**
```python
# Multi-dimensional analysis
metrics = ModelMetrics(
    quality_score=0.88,
    cost_eur=0.0025,
    latency_ms=850
)

# Different weighting profiles
profiles = {
    "balanced": {"quality_weight": 0.5, "cost_weight": 0.3, "latency_weight": 0.2},
    "quality_focused": {"quality_weight": 0.7, "cost_weight": 0.2, "latency_weight": 0.1},
    "cost_focused": {"quality_weight": 0.3, "cost_weight": 0.5, "latency_weight": 0.2},
    "speed_focused": {"quality_weight": 0.3, "cost_weight": 0.2, "latency_weight": 0.5}
}

for profile_name, weights in profiles.items():
    score = calculator.calculate_value_score(metrics, **weights)
    print(f"{profile_name.title()}: {score:.1f}/100")
```

## See Also
- [`Aggregator`](aggregator.md) - Functionality to aggregate metrics across multiple test runs
- [`Analyzer`](analyzer.md) - Functionality for analyzing and comparing metrics between versions
- [`Models`](models.md) - Data models for metrics and comparison structures
- [`Pricing`](pricing.md) - Manages model pricing and calculates LLM call costs
- [`Tracker`](tracker.md) - Functionality for tracking and statistical analysis of metrics
