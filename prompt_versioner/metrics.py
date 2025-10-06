"""Metrics tracking and analysis for prompt versions."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics


@dataclass
class ModelMetrics:
    """Metrics for a single LLM call."""
    model_name: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_eur: Optional[float] = None
    latency_ms: Optional[float] = None
    quality_score: Optional[float] = None
    accuracy: Optional[float] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class MetricStats:
    """Statistical summary of a metric."""
    name: str
    count: int
    mean: float
    median: float
    std_dev: float
    min_val: float
    max_val: float


# Model pricing per 1M tokens (input/output) in EUR
MODEL_PRICING = {
  "claude-opus-4-1": {"input": 13.80, "output": 69.00},
  "claude-opus-4": {"input": 13.80, "output": 69.00},
  "claude-sonnet-4": {"input": 5.06, "output": 23.00},
  "mistral-large-24-11": {"input": 1.84, "output": 5.52},
  "mistral-medium-3": {"input": 0.37, "output": 1.84},
  "mistral-small-3-1": {"input": 0.09, "output": 0.28},
  "mistral-nemo": {"input": 0.14, "output": 0.14},
  "gpt-5": {"input": 1.15, "output": 9.20},
  "gpt-5-mini": {"input": 0.23, "output": 1.84},
  "gpt-5-nano": {"input": 0.05, "output": 0.37},
  "gpt-4-1": {"input": 0.92, "output": 3.68},
  "gpt-4-1-mini": {"input": 0.18, "output": 0.73},
  "gpt-4o": {"input": 1.15, "output": 4.60},
}



class MetricsCalculator:
    """Calculate costs and metrics for LLM calls."""
    
    @staticmethod
    def calculate_cost(
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost in USD for a model call.
        
        Args:
            model_name: Name of the model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
        """
        if model_name not in MODEL_PRICING:
            return 0.0
        
        pricing = MODEL_PRICING[model_name]
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
    
    @staticmethod
    def add_pricing_to_model(model_name: str, input_price: float, output_price: float) -> None:
        """Add custom pricing for a model.
        
        Args:
            model_name: Name of the model
            input_price: Price per 1M input tokens
            output_price: Price per 1M output tokens
        """
        MODEL_PRICING[model_name] = {"input": input_price, "output": output_price}


class MetricsTracker:
    """Tracks and analyzes metrics for prompt versions."""

    @staticmethod
    def compute_stats(values: List[float]) -> Dict[str, float]:
        """Compute statistical summary of metric values.
        
        Args:
            values: List of metric values
            
        Returns:
            Dict with statistical measures
        """
        if not values:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "std_dev": 0.0,
                "min": 0.0,
                "max": 0.0,
            }
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
        }

    @staticmethod
    def analyze_metrics(metrics: Dict[str, List[float]]) -> List[MetricStats]:
        """Analyze metrics and return statistical summaries.
        
        Args:
            metrics: Dict of metric name -> list of values
            
        Returns:
            List of MetricStats objects
        """
        results = []
        
        for name, values in metrics.items():
            stats = MetricsTracker.compute_stats(values)
            results.append(
                MetricStats(
                    name=name,
                    count=stats["count"],
                    mean=stats["mean"],
                    median=stats["median"],
                    std_dev=stats["std_dev"],
                    min_val=stats["min"],
                    max_val=stats["max"],
                )
            )
        
        return results

    @staticmethod
    def compare_metrics(
        baseline_metrics: Dict[str, List[float]],
        new_metrics: Dict[str, List[float]],
    ) -> Dict[str, Dict[str, Any]]:
        """Compare metrics between two versions.
        
        Args:
            baseline_metrics: Metrics from baseline version
            new_metrics: Metrics from new version
            
        Returns:
            Dict with comparison results for each metric
        """
        comparison = {}
        
        # Find common metrics
        common_metrics = set(baseline_metrics.keys()) & set(new_metrics.keys())
        
        for metric_name in common_metrics:
            baseline_vals = baseline_metrics[metric_name]
            new_vals = new_metrics[metric_name]
            
            baseline_stats = MetricsTracker.compute_stats(baseline_vals)
            new_stats = MetricsTracker.compute_stats(new_vals)
            
            # Compute differences
            mean_diff = new_stats["mean"] - baseline_stats["mean"]
            mean_pct_change = (
                (mean_diff / baseline_stats["mean"] * 100)
                if baseline_stats["mean"] != 0
                else 0.0
            )
            
            comparison[metric_name] = {
                "baseline": baseline_stats,
                "new": new_stats,
                "mean_diff": mean_diff,
                "mean_pct_change": mean_pct_change,
                "improved": mean_diff > 0,  # Assuming higher is better
            }
        
        return comparison

    @staticmethod
    def format_metric_comparison(comparison: Dict[str, Dict[str, Any]]) -> str:
        """Format metric comparison as human-readable text.
        
        Args:
            comparison: Comparison dict from compare_metrics
            
        Returns:
            Formatted string
        """
        lines = ["=" * 80, "METRICS COMPARISON", "=" * 80]
        
        for metric_name, data in comparison.items():
            lines.append(f"\n{metric_name.upper()}:")
            lines.append(f"  Baseline: {data['baseline']['mean']:.4f} (±{data['baseline']['std_dev']:.4f})")
            lines.append(f"  New:      {data['new']['mean']:.4f} (±{data['new']['std_dev']:.4f})")
            
            diff = data['mean_diff']
            pct = data['mean_pct_change']
            symbol = "↑" if diff > 0 else "↓"
            
            lines.append(f"  Change:   {symbol} {abs(diff):.4f} ({pct:+.2f}%)")
        
        return "\n".join(lines)

    @staticmethod
    def detect_regression(
        baseline_metrics: Dict[str, List[float]],
        new_metrics: Dict[str, List[float]],
        threshold: float = 0.05,
    ) -> List[str]:
        """Detect if new version has regressed on any metrics.
        
        Args:
            baseline_metrics: Metrics from baseline version
            new_metrics: Metrics from new version
            threshold: Relative threshold for regression (default 5%)
            
        Returns:
            List of metric names that have regressed
        """
        regressions = []
        comparison = MetricsTracker.compare_metrics(baseline_metrics, new_metrics)
        
        for metric_name, data in comparison.items():
            # Check if metric decreased by more than threshold
            pct_change = data['mean_pct_change']
            if pct_change < -threshold * 100:
                regressions.append(metric_name)
        
        return regressions


class MetricType:
    """Common metric types for LLM prompts."""
    
    TOKENS = "tokens"
    COST = "cost"
    LATENCY = "latency_ms"
    QUALITY = "quality_score"
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FACTUALITY = "factuality"


class MetricAggregator:
    """Aggregates metrics across multiple test runs."""

    def __init__(self):
        """Initialize aggregator."""
        self.metrics: List[ModelMetrics] = []

    def add(self, metric: ModelMetrics) -> None:
        """Add a metric.
        
        Args:
            metric: ModelMetrics object
        """
        self.metrics.append(metric)

    def add_dict(self, **kwargs: Any) -> None:
        """Add metrics from keyword arguments.
        
        Args:
            **kwargs: Metric fields
        """
        self.metrics.append(ModelMetrics(**kwargs))

    def get_summary(self) -> Dict[str, Any]:
        """Get statistical summary of all metrics.
        
        Returns:
            Dict with aggregated statistics
        """
        if not self.metrics:
            return {}
        
        return {
            "call_count": len(self.metrics),
            "total_tokens": sum(m.total_tokens or 0 for m in self.metrics),
            "avg_input_tokens": self._avg([m.input_tokens for m in self.metrics if m.input_tokens]),
            "avg_output_tokens": self._avg([m.output_tokens for m in self.metrics if m.output_tokens]),
            "total_cost": sum(m.cost_eur or 0 for m in self.metrics),
            "avg_cost": self._avg([m.cost_eur for m in self.metrics if m.cost_eur]),
            "avg_latency": self._avg([m.latency_ms for m in self.metrics if m.latency_ms]),
            "min_latency": min([m.latency_ms for m in self.metrics if m.latency_ms], default=0),
            "max_latency": max([m.latency_ms for m in self.metrics if m.latency_ms], default=0),
            "avg_quality": self._avg([m.quality_score for m in self.metrics if m.quality_score]),
            "avg_accuracy": self._avg([m.accuracy for m in self.metrics if m.accuracy]),
            "success_rate": sum(1 for m in self.metrics if m.success) / len(self.metrics),
            "models_used": list(set(m.model_name for m in self.metrics if m.model_name)),
        }
    
    @staticmethod
    def _avg(values: List[float]) -> float:
        """Calculate average of values."""
        return sum(values) / len(values) if values else 0.0

    def clear(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()

    def to_list(self) -> List[Dict[str, Any]]:
        """Export metrics as list of dicts.
        
        Returns:
            List of metric dicts
        """
        return [
            {
                "model_name": m.model_name,
                "input_tokens": m.input_tokens,
                "output_tokens": m.output_tokens,
                "total_tokens": m.total_tokens,
                "cost_eur": m.cost_eur,
                "latency_ms": m.latency_ms,
                "quality_score": m.quality_score,
                "accuracy": m.accuracy,
                "temperature": m.temperature,
                "max_tokens": m.max_tokens,
                "success": m.success,
                "error_message": m.error_message,
                "metadata": m.metadata,
            }
            for m in self.metrics
        ]