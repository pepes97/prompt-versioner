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

### Real-time Monitoring

```python
def monitor_performance(pv, prompt_name, version, alert_thresholds=None):
    """Monitor prompt performance with alerts"""

    if alert_thresholds is None:
        alert_thresholds = {
            "min_quality": 0.8,
            "max_latency": 1000,
            "min_success_rate": 0.95
        }

    version_data = pv.get_version(prompt_name, version)
    recent_metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=100)

    if len(recent_metrics) < 10:
        print("⚠️ Insufficient data for monitoring")
        return

    # Calculate current performance
    current_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)
    current_latency = sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics)
    current_success = sum(1 for m in recent_metrics if m.get("success", True)) / len(recent_metrics)

    # Check alerts
    alerts = []
    if current_quality < alert_thresholds["min_quality"]:
        alerts.append(f"Quality below threshold: {current_quality:.2f}")

    if current_latency > alert_thresholds["max_latency"]:
        alerts.append(f"Latency above threshold: {current_latency:.1f}ms")

    if current_success < alert_thresholds["min_success_rate"]:
        alerts.append(f"Success rate below threshold: {current_success:.1%}")

    # Report status
    status = "🟢 Healthy" if not alerts else "🔴 Alert"
    print(f"{status} - {prompt_name} v{version}")

    for alert in alerts:
        print(f"  ⚠️ {alert}")

    return {
        "status": "healthy" if not alerts else "alert",
        "metrics": {
            "quality": current_quality,
            "latency": current_latency,
            "success_rate": current_success
        },
        "alerts": alerts
    }

# Monitor with custom thresholds
monitor_performance(pv, "customer_service", "2.1.0", {
    "min_quality": 0.85,
    "max_latency": 800,
    "min_success_rate": 0.98
})
```

## 🚨 Alerting System

### Performance Degradation Detection

```python
def detect_degradation(pv, prompt_name, version, lookback_days=7):
    """Detect performance degradation over time"""

    from datetime import datetime, timedelta

    version_data = pv.get_version(prompt_name, version)
    all_metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=1000)

    # Split into recent and baseline periods
    cutoff = datetime.now() - timedelta(days=lookback_days)
    baseline_cutoff = cutoff - timedelta(days=lookback_days)

    recent_metrics = [
        m for m in all_metrics
        if datetime.fromisoformat(m.get('timestamp', '1970-01-01')) > cutoff
    ]

    baseline_metrics = [
        m for m in all_metrics
        if baseline_cutoff < datetime.fromisoformat(m.get('timestamp', '1970-01-01')) <= cutoff
    ]

    if len(recent_metrics) < 5 or len(baseline_metrics) < 5:
        return {"status": "insufficient_data"}

    # Compare performance
    recent_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)
    baseline_quality = sum(m.get("quality_score", 0) for m in baseline_metrics) / len(baseline_metrics)

    recent_latency = sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics)
    baseline_latency = sum(m.get("latency_ms", 0) for m in baseline_metrics) / len(baseline_metrics)

    quality_change = (recent_quality - baseline_quality) / baseline_quality * 100
    latency_change = (recent_latency - baseline_latency) / baseline_latency * 100

    # Detect significant changes
    degradation_alerts = []

    if quality_change < -5:  # 5% quality drop
        degradation_alerts.append(f"Quality degraded by {abs(quality_change):.1f}%")

    if latency_change > 20:  # 20% latency increase
        degradation_alerts.append(f"Latency increased by {latency_change:.1f}%")

    return {
        "status": "degraded" if degradation_alerts else "stable",
        "alerts": degradation_alerts,
        "changes": {
            "quality_change_pct": quality_change,
            "latency_change_pct": latency_change
        },
        "comparison": {
            "recent": {"quality": recent_quality, "latency": recent_latency},
            "baseline": {"quality": baseline_quality, "latency": baseline_latency}
        }
    }

# Check for degradation
degradation = detect_degradation(pv, "customer_service", "2.1.0")
print(f"Status: {degradation['status']}")
for alert in degradation.get('alerts', []):
    print(f"⚠️ {alert}")
```

## 📊 Monitoring Dashboard

### Simple Performance Dashboard

```python
def create_monitoring_dashboard(pv, prompts_to_monitor):
    """Create a simple text-based monitoring dashboard"""

    print("=" * 60)
    print("🔍 PROMPT VERSIONER MONITORING DASHBOARD")
    print("=" * 60)

    for prompt_name, version in prompts_to_monitor:
        version_data = pv.get_version(prompt_name, version)
        if not version_data:
            print(f"❌ {prompt_name} v{version} - Version not found")
            continue

        metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=50)

        if not metrics:
            print(f"⚠️ {prompt_name} v{version} - No metrics available")
            continue

        # Calculate stats
        avg_quality = sum(m.get("quality_score", 0) for m in metrics) / len(metrics)
        avg_latency = sum(m.get("latency_ms", 0) for m in metrics) / len(metrics)
        success_rate = sum(1 for m in metrics if m.get("success", True)) / len(metrics)
        total_cost = sum(m.get("cost_eur", 0) for m in metrics)

        # Status indicator
        status = "🟢"
        if avg_quality < 0.8 or avg_latency > 1000 or success_rate < 0.95:
            status = "🔴"
        elif avg_quality < 0.9 or avg_latency > 500 or success_rate < 0.98:
            status = "🟡"

        print(f"{status} {prompt_name} v{version}")
        print(f"   Quality: {avg_quality:.2f} | Latency: {avg_latency:.0f}ms | Success: {success_rate:.1%}")
        print(f"   Calls: {len(metrics)} | Cost: €{total_cost:.3f}")
        print()

# Monitor multiple prompts
prompts_to_monitor = [
    ("customer_service", "2.1.0"),
    ("code_reviewer", "1.1.0"),
    ("summarizer", "1.2.0")
]

create_monitoring_dashboard(pv, prompts_to_monitor)
```

## 🔄 Automated Monitoring

### Scheduled Health Checks

```python
import time
import threading

def start_monitoring_loop(pv, prompts, check_interval=300):  # 5 minutes
    """Start automated monitoring in background"""

    def monitoring_loop():
        while True:
            print(f"\n🔍 Automated health check - {datetime.now().strftime('%H:%M:%S')}")

            for prompt_name, version in prompts:
                try:
                    status = monitor_performance(pv, prompt_name, version)

                    if status["status"] == "alert":
                        print(f"🚨 ALERT: {prompt_name} v{version} needs attention!")
                        # Here you could send notifications, emails, etc.

                except Exception as e:
                    print(f"❌ Error monitoring {prompt_name}: {e}")

            time.sleep(check_interval)

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    print(f"🚀 Started automated monitoring (checking every {check_interval}s)")

    return monitor_thread

# Start monitoring (uncomment to use)
# monitored_prompts = [("customer_service", "2.1.0"), ("code_reviewer", "1.1.0")]
# start_monitoring_loop(pv, monitored_prompts, check_interval=60)
```

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

## 🛠️ Integration Tips

### Log Analysis
```python
# Analyze error patterns
def analyze_errors(pv, prompt_name, version):
    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=500)

    errors = [m for m in metrics if not m.get("success", True)]

    if errors:
        print(f"Found {len(errors)} errors out of {len(metrics)} calls ({len(errors)/len(metrics):.1%})")

        # Group by error message
        error_groups = {}
        for error in errors:
            msg = error.get("error_message", "Unknown error")
            error_groups[msg] = error_groups.get(msg, 0) + 1

        print("Error breakdown:")
        for msg, count in sorted(error_groups.items(), key=lambda x: x[1], reverse=True):
            print(f"  {count}x: {msg}")
    else:
        print("No errors found ✅")

analyze_errors(pv, "customer_service", "2.1.0")
```

### Performance Trends
```python
# Track performance over time
def track_performance_trend(pv, prompt_name, version, days=30):
    from datetime import datetime, timedelta

    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=10000)

    # Group by day
    daily_performance = {}

    for metric in metrics:
        timestamp = datetime.fromisoformat(metric.get('timestamp', '1970-01-01'))
        day = timestamp.date()

        if day not in daily_performance:
            daily_performance[day] = []

        daily_performance[day].append(metric)

    # Show trends for recent days
    recent_days = sorted(daily_performance.keys())[-days:]

    print(f"📈 Performance trend for {prompt_name} v{version} (last {len(recent_days)} days):")

    for day in recent_days:
        day_metrics = daily_performance[day]
        avg_quality = sum(m.get("quality_score", 0) for m in day_metrics) / len(day_metrics)
        call_count = len(day_metrics)

        print(f"  {day}: {avg_quality:.2f} quality, {call_count} calls")

track_performance_trend(pv, "customer_service", "2.1.0", days=7)
```

## 📚 Next Steps

- [Metrics Tracking](metrics-tracking.md) - Learn about detailed metrics collection
- [A/B Testing](ab-testing.md) - Compare performance between versions
- [Version Management](version-management.md) - Manage your prompt versions
