# Tracker

The `prompt_versioner.metrics.tracker` module provides functionality for tracking and statistical analysis of metrics.

## MetricsTracker

Static class for tracking and analyzing prompt version metrics.

### Methods

#### compute_stats()

```python
@staticmethod
    def compute_stats(values: List[float]) -> Dict[str, float]
```

Computes a statistical summary of metric values.

**Parameters:**
- `values` (List[float]): List of metric values

**Returns:**
- `Dict[str, float]`: Dictionary with statistical measures:
  - `count`: Number of values
  - `mean`: Arithmetic mean
  - `median`: Median
  - `std_dev`: Standard deviation
  - `min`: Minimum value
  - `max`: Maximum value
  - `sum`: Total sum

**Example:**
```python
from prompt_versioner.metrics.tracker import MetricsTracker

values = [1.5, 2.3, 1.8, 3.1, 2.0, 1.9, 2.5]
stats = MetricsTracker.compute_stats(values)
print(f"Mean: {stats['mean']:.2f}")
print(f"Standard deviation: {stats['std_dev']:.2f}")
```

#### compute_percentiles()

```python
@staticmethod
    def compute_percentiles(
        values: List[float], percentiles: List[int] = [25, 50, 75, 90, 95, 99]
    ) -> Dict[int, float]
```

Computes percentiles of metric values.

**Parameters:**
- `values` (List[float]): List of metric values
- `percentiles` (List[int]): List of percentiles to compute (default: [25, 50, 75, 90, 95, 99])

**Returns:**
- `Dict[int, float]`: Dictionary percentile -> value

**Example:**
```python
values = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
percentiles = MetricsTracker.compute_percentiles(values, [25, 50, 75, 95])
print(f"25th percentile: {percentiles[25]}")
print(f"95th percentile: {percentiles[95]}")
```

#### analyze_metrics()

```python
@staticmethod
    def analyze_metrics(metrics: Dict[str, List[float]]) -> List[MetricStats]
```

Analyzes metrics and returns statistical summaries.

**Parameters:**
- `metrics` (Dict[str, List[float]]): Dictionary metric name -> list of values

**Returns:**
- `List[MetricStats]`: List of MetricStats objects

**Example:**
```python
metrics = {
    "latency_ms": [100, 120, 95, 110, 105],
    "cost_eur": [0.001, 0.0015, 0.0012, 0.0018, 0.0014]
}
stats_list = MetricsTracker.analyze_metrics(metrics)
for stats in stats_list:
    print(f"{stats.name}: mean={stats.mean:.4f}, std={stats.std_dev:.4f}")
```

#### detect_outliers()

```python
@staticmethod
    def detect_outliers(
        values: List[float], method: str = "iqr", threshold: float = 1.5
    ) -> List[int]
```

Detects outliers in metric values.

**Parameters:**
- `values` (List[float]): List of metric values
- `method` (str): Method to use ('iqr' or 'zscore', default: 'iqr')
- `threshold` (float): Threshold for outlier detection (default: 1.5)

**Returns:**
- `List[int]`: List of indices of outlier values

**Detection methods:**
- **IQR (Interquartile Range):** Uses Q1 - threshold*IQR and Q3 + threshold*IQR as limits
- **Z-Score:** Uses standard deviation and considers values with |z-score| > threshold as outliers

**Example:**
```python
values = [1.0, 1.1, 1.2, 1.1, 1.0, 5.0, 1.1, 1.0, 1.2]  # 5.0 is an outlier
outliers = MetricsTracker.detect_outliers(values, method="iqr")
print(f"Outlier indices: {outliers}")  # [5]

# Using z-score
outliers_z = MetricsTracker.detect_outliers(values, method="zscore", threshold=2.0)
```

#### calculate_trend()

```python
@staticmethod
    def calculate_trend(values: List[float]) -> Dict[str, Any]
```

Calculates the trend in metric values over time.

**Parameters:**
- `values` (List[float]): List of metric values in chronological order

**Returns:**
- `Dict[str, Any]`: Dictionary with trend information:
  - `trend`: Trend type ('increasing', 'decreasing', 'stable', 'insufficient_data')
  - `direction`: Direction ('up', 'down', None)
  - `slope`: Linear regression slope
  - `start_value`: First value
  - `end_value`: Last value
  - `change`: Absolute change
  - `pct_change`: Percent change

**Example:**
```python
# Increasing values over time
values = [1.0, 1.2, 1.5, 1.8, 2.0]
trend = MetricsTracker.calculate_trend(values)
print(f"Trend: {trend['trend']}")  # 'increasing'
print(f"Change: {trend['change']}")  # 1.0
print(f"Percent change: {trend['pct_change']:.1f}%")  # 100.0%
```

## Algorithms Used

### Linear Regression for Trend

Trend calculation uses simple linear regression:
- **Slope**: Indicates direction and intensity of the trend
- **R²**: Implicitly evaluated through the slope
- **Stability threshold**: |slope| < 0.01 indicates a stable trend

### Outlier Detection

**IQR Method:**
```
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
```

**Z-Score Method:**
```
Z = |value - mean| / std_dev
Outlier if Z > threshold
```

## See Also
- [`Aggregator`](aggregator.md) - Functionality to aggregate metrics across multiple test runs
- [`Analyzer`](analyzer.md) - Functionality for analyzing and comparing metrics between versions
- [`Models`](models.md) - Data models for metrics and comparison structures
- [`Calculator`](calculator.md) - Utility for single-call metric calculations
- [`Pricing`](pricing.md) - Manages model pricing and calculates LLM call costs
