# Performance Monitoring

Monitor prompt performance and system health with **Prompt Versioner**'s monitoring capabilities.

## 🔍 Quick Overview

```python
from prompt_versioner import PromptVersioner

pv = PromptVersioner(project_name="my-project", enable_git=False)

# Check recent performance
def check_prompt_health(prompt_name, version):
    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=50)

    if metrics:
        avg_quality = sum(m.get("quality_score", 0) for m in metrics) / len(metrics)
        avg_latency = sum(m.get("latency_ms", 0) for m in metrics) / len(metrics)
        success_rate = sum(1 for m in metrics if m.get("success", True)) / len(metrics)

        print(f"📊 {prompt_name} v{version} Health:")
        print(f"  Quality: {avg_quality:.2f}")
        print(f"  Latency: {avg_latency:.1f}ms")
        print(f"  Success: {success_rate:.1%}")
        print(f"  Samples: {len(metrics)}")

check_prompt_health("code_reviewer", "1.1.0")
```

## 📈 Performance Metrics

### Key Performance Indicators

Monitor these essential metrics:

- **Quality Score**: Your custom evaluation (0.0-1.0)
- **Latency**: Response time in milliseconds
- **Success Rate**: Percentage of successful calls
- **Cost**: Per-call cost tracking
- **Token Usage**: Input/output token consumption

## 🎯 Best Practices

### 1. Set Appropriate Thresholds
- Define quality thresholds based on your use case
- Set latency limits based on user experience requirements
- Monitor success rates to catch errors early

### 2. Regular Health Checks
- Check performance at least daily for production prompts
- Set up automated alerts for critical issues
- Review trends weekly to identify patterns

### 3. Baseline Comparisons
- Compare current performance to historical baselines
- Look for gradual degradation over time
- Track performance after prompt updates

### 4. Cost Monitoring
- Monitor cost per call and daily/monthly totals
- Set budget alerts to prevent unexpected costs
- Track cost efficiency alongside quality metrics

## 📚 Next Steps

- [Metrics Tracking](metrics-tracking.md) - Learn about detailed metrics collection
- [A/B Testing](ab-testing.md) - Compare performance between versions
- [Version Management](version-management.md) - Manage your prompt versions
