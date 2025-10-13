# Metrics Tracking

Track and analyze prompt performance with **Prompt Versioner**'s metrics system.

## 📊 Quick Start

```python
from prompt_versioner import PromptVersioner

# Initialize versioner
pv = PromptVersioner(project_name="my-project", enable_git=False)

# Log metrics after using a prompt
pv.log_metrics(
    name="code_reviewer",
    version="1.0.0",
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=250,
    latency_ms=420.5,
    quality_score=0.92,
    cost_eur=0.003,
    temperature=0.7,
    max_tokens=1000,
    success=True,
    metadata={"user_feedback": "excellent", "domain": "backend"}
)

print("📊 Metrics logged successfully!")
```

## 🎯 Core Metrics

### Basic Performance Metrics

```python
# Essential metrics for every prompt call
pv.log_metrics(
    name="summarizer",
    version="1.1.0",

    # Model info
    model_name="gpt-4o-mini",

    # Token usage
    input_tokens=200,
    output_tokens=100,

    # Performance
    latency_ms=350.0,
    success=True,

    # Optional quality assessment
    quality_score=0.88,  # Your evaluation (0.0-1.0)
)
```

### Advanced Metrics

```python
# Comprehensive metrics tracking
pv.log_metrics(
    name="customer_service",
    version="2.1.0",
    model_name="gpt-4o",

    # Usage
    input_tokens=180,
    output_tokens=220,

    # Performance
    latency_ms=580.2,
    cost_eur=0.0045,

    # Quality metrics
    quality_score=0.94,
    accuracy=0.91,

    # Model parameters used
    temperature=0.3,
    top_p=0.9,
    max_tokens=500,

    # Result
    success=True,
    error_message=None,

    # Context
    metadata={
        "user_id": "user123",
        "session_id": "sess456",
        "issue_type": "billing",
        "satisfaction_score": 4.5,
        "resolved": True
    }
)
```

## 📈 Analyzing Performance

### Get Metrics for Analysis

```python
# Get version details
version = pv.get_version("customer_service", "2.1.0")
version_id = version["id"]

# Retrieve all metrics for this version
metrics = pv.storage.get_metrics(version_id=version_id, limit=100)

print(f"Found {len(metrics)} metric records")

# Calculate averages
if metrics:
    avg_quality = sum(m["quality_score"] for m in metrics if m["quality_score"]) / len(metrics)
    avg_latency = sum(m["latency_ms"] for m in metrics if m["latency_ms"]) / len(metrics)
    success_rate = sum(1 for m in metrics if m["success"]) / len(metrics)

    print(f"📊 Performance Summary:")
    print(f"  Average Quality: {avg_quality:.2f}")
    print(f"  Average Latency: {avg_latency:.1f}ms")
    print(f"  Success Rate: {success_rate:.1%}")
```

### Compare Version Performance

```python
# Compare multiple versions
def compare_version_metrics(pv, prompt_name, versions):
    """Compare performance across versions"""

    results = {}

    for version_str in versions:
        version = pv.get_version(prompt_name, version_str)
        if not version:
            continue

        metrics = pv.storage.get_metrics(version_id=version["id"], limit=1000)

        if metrics:
            results[version_str] = {
                "samples": len(metrics),
                "avg_quality": sum(m.get("quality_score", 0) for m in metrics) / len(metrics),
                "avg_latency": sum(m.get("latency_ms", 0) for m in metrics) / len(metrics),
                "success_rate": sum(1 for m in metrics if m.get("success", False)) / len(metrics),
                "avg_cost": sum(m.get("cost_eur", 0) for m in metrics) / len(metrics)
            }

    return results

# Usage
comparison = compare_version_metrics(pv, "customer_service", ["2.0.0", "2.1.0", "2.2.0"])

for version, stats in comparison.items():
    print(f"\nVersion {version}:")
    print(f"  Samples: {stats['samples']}")
    print(f"  Quality: {stats['avg_quality']:.2f}")
    print(f"  Latency: {stats['avg_latency']:.1f}ms")
    print(f"  Success: {stats['success_rate']:.1%}")
    print(f"  Cost: €{stats['avg_cost']:.4f}")
```

## 🧪 Testing with Metrics

### Test Context for Controlled Testing

```python
# Use test context for structured testing
with pv.test_version("summarizer", "1.2.0") as test:
    # Your LLM call would go here
    # result = call_llm(prompt, text)

    # Log test metrics
    test.log(
        tokens=180,
        cost=0.002,
        latency_ms=290,
        quality_score=0.89,
        metadata={"test_case": "technical_doc", "length": "medium"}
    )

print("✅ Test metrics logged")
```

### Batch Metrics Collection

```python
# Collect metrics for multiple test cases
test_cases = [
    {"text": "Simple text", "expected_quality": 0.8},
    {"text": "Complex technical document", "expected_quality": 0.85},
    {"text": "Creative content", "expected_quality": 0.9}
]

for i, case in enumerate(test_cases):
    with pv.test_version("summarizer", "1.2.0") as test:
        # Simulate processing
        simulated_quality = case["expected_quality"] + random.uniform(-0.05, 0.05)
        simulated_latency = 300 + random.uniform(-50, 100)

        test.log(
            tokens=150 + i * 20,
            cost=0.002 + i * 0.0005,
            latency_ms=simulated_latency,
            quality_score=simulated_quality,
            metadata={"test_case": f"case_{i+1}", "type": case["text"][:10]}
        )

print(f"✅ Logged metrics for {len(test_cases)} test cases")
```

## 📊 Production Monitoring

### Automatic Metrics Collection

```python
def track_production_call(pv, prompt_name, version, llm_response, start_time, end_time):
    """Standard production metrics tracking"""

    latency_ms = (end_time - start_time) * 1000

    # Extract from your LLM response object
    pv.log_metrics(
        name=prompt_name,
        version=version,
        model_name=llm_response.model,
        input_tokens=llm_response.usage.prompt_tokens,
        output_tokens=llm_response.usage.completion_tokens,
        latency_ms=latency_ms,
        cost_eur=calculate_cost(llm_response.usage),  # Your cost calculation
        quality_score=evaluate_quality(llm_response.content),  # Your quality eval
        success=llm_response.success,
        error_message=llm_response.error if not llm_response.success else None,
        metadata={
            "user_id": llm_response.user_id,
            "request_id": llm_response.request_id,
            "environment": "production"
        }
    )

# Usage in production
import time

start = time.time()
# response = your_llm_call(prompt, inputs)
end = time.time()

# track_production_call(pv, "customer_service", "2.1.0", response, start, end)
```

### Performance Alerts

```python
def check_performance_degradation(pv, prompt_name, version, threshold_quality=0.8, threshold_latency=1000):
    """Check if recent performance is degrading"""

    version_data = pv.get_version(prompt_name, version)
    if not version_data:
        return {"status": "version_not_found"}

    # Get recent metrics (last 100 calls)
    recent_metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=100)

    if len(recent_metrics) < 10:
        return {"status": "insufficient_data"}

    # Calculate recent averages
    avg_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)
    avg_latency = sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics)
    error_rate = sum(1 for m in recent_metrics if not m.get("success", True)) / len(recent_metrics)

    alerts = []

    if avg_quality < threshold_quality:
        alerts.append(f"Quality below threshold: {avg_quality:.2f} < {threshold_quality}")

    if avg_latency > threshold_latency:
        alerts.append(f"Latency above threshold: {avg_latency:.1f}ms > {threshold_latency}ms")

    if error_rate > 0.05:  # 5% error rate
        alerts.append(f"High error rate: {error_rate:.1%}")

    return {
        "status": "ok" if not alerts else "degraded",
        "alerts": alerts,
        "metrics": {
            "quality": avg_quality,
            "latency": avg_latency,
            "error_rate": error_rate,
            "sample_size": len(recent_metrics)
        }
    }

# Check performance
status = check_performance_degradation(pv, "customer_service", "2.1.0")
print(f"Status: {status['status']}")
if status.get("alerts"):
    for alert in status["alerts"]:
        print(f"⚠️ {alert}")
```

## 🎯 Best Practices

### 1. Consistent Tracking
- Log metrics for every production call
- Use standardized quality evaluation
- Include relevant context in metadata

### 2. Quality Assessment
- Develop consistent quality scoring (0.0-1.0)
- Consider multiple quality dimensions
- Use both automated and human evaluation

### 3. Cost Monitoring
- Track costs per call in your currency
- Monitor cost trends over time
- Set up cost alerts for budget control

### 4. Performance Monitoring
- Set latency thresholds for your use case
- Monitor success rates and error patterns
- Track performance degradation over time

## 🔧 Useful Patterns

### Metrics Decorator

```python
def track_metrics(prompt_name, version):
    """Decorator to automatically track metrics"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                end_time = time.time()

                # Track successful call
                pv.log_metrics(
                    name=prompt_name,
                    version=version,
                    latency_ms=(end_time - start_time) * 1000,
                    success=True,
                    # Add more metrics based on result
                )

                return result

            except Exception as e:
                end_time = time.time()

                # Track failed call
                pv.log_metrics(
                    name=prompt_name,
                    version=version,
                    latency_ms=(end_time - start_time) * 1000,
                    success=False,
                    error_message=str(e)
                )

                raise

        return wrapper
    return decorator

# Usage
@track_metrics("summarizer", "1.1.0")
def summarize_text(text):
    # Your summarization logic
    return "summary result"
```

### Performance Dashboard Data

```python
def get_dashboard_data(pv, prompt_name, days=7):
    """Get data for performance dashboard"""

    versions = pv.list_versions(prompt_name)
    dashboard_data = {}

    for version_info in versions:
        version_str = version_info['version']
        metrics = pv.storage.get_metrics(version_id=version_info['id'], limit=1000)

        # Filter recent metrics
        cutoff = datetime.now() - timedelta(days=days)
        recent_metrics = [
            m for m in metrics
            if datetime.fromisoformat(m.get('timestamp', '1970-01-01')) > cutoff
        ]

        if recent_metrics:
            dashboard_data[version_str] = {
                "calls_count": len(recent_metrics),
                "avg_quality": sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics),
                "avg_latency": sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics),
                "success_rate": sum(1 for m in recent_metrics if m.get("success", False)) / len(recent_metrics),
                "total_cost": sum(m.get("cost_eur", 0) for m in recent_metrics)
            }

    return dashboard_data

# Get last 7 days of data
dashboard = get_dashboard_data(pv, "customer_service", days=7)
for version, data in dashboard.items():
    print(f"\n{version}: {data['calls_count']} calls")
    print(f"  Quality: {data['avg_quality']:.2f}")
    print(f"  Latency: {data['avg_latency']:.0f}ms")
    print(f"  Success: {data['success_rate']:.1%}")
    print(f"  Cost: €{data['total_cost']:.3f}")
```

## 📚 Next Steps

- [A/B Testing](ab-testing.md) - Compare versions systematically
- [Version Management](version-management.md) - Manage your prompt versions
- [Basic Usage](../examples/basic-usage.md) - More examples and patterns
