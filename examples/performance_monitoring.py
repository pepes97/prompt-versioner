from prompt_versioner import PerformanceMonitor, PromptVersioner, VersionBump
import random

pv = PromptVersioner(project_name="my-ai-project", enable_git=False)

print("🚀 Creating test data for performance monitoring...")

# 1. Create a prompt with baseline version
print("\n📝 Creating baseline version...")
pv.save_version(
    name="test_classifier",
    system_prompt="You are an expert text classifier.",
    user_prompt="Classify this text: {text}",
    bump_type=VersionBump.MAJOR,
    metadata={"version_type": "baseline", "author": "team"},
)

baseline_version = pv.get_latest("test_classifier")
print(f"✅ Created baseline version: {baseline_version['version']}")

# 2. Log baseline metrics (good performance)
print("📊 Logging baseline metrics...")
for i in range(20):
    pv.log_metrics(
        name="test_classifier",
        version=baseline_version["version"],
        model_name="gpt-4o",
        input_tokens=random.randint(100, 200),  # nosec B311
        output_tokens=random.randint(20, 50),  # nosec B311
        latency_ms=random.uniform(300, 500),  # nosec B311
        quality_score=random.uniform(0.85, 0.95),  # nosec B311
        success=True,
        temperature=0.7,
        max_tokens=100,
    )

print(f"✅ Logged {20} baseline metrics")

# 3. Create new version with worse performance
print("\n📝 Creating new version with performance issues...")
pv.save_version(
    name="test_classifier",
    system_prompt="You are an expert text classifier with detailed analysis capabilities.",
    user_prompt="Classify this text with detailed reasoning: {text}\n\nProvide classification and explanation:",
    bump_type=VersionBump.MINOR,
    metadata={"version_type": "detailed", "author": "team", "change": "added detailed reasoning"},
)

current_version = pv.get_latest("test_classifier")
print(f"✅ Created current version: {current_version['version']}")

# 4. Log worse metrics for new version
print("📊 Logging current metrics (with regressions)...")
for i in range(20):
    pv.log_metrics(
        name="test_classifier",
        version=current_version["version"],
        model_name="gpt-4o",
        input_tokens=random.randint(150, 300),  # nosec B311
        output_tokens=random.randint(80, 150),  # nosec B311
        latency_ms=random.uniform(600, 900),  # nosec B311
        quality_score=random.uniform(0.70, 0.85),  # nosec B311
        success=random.choice([True] * 18 + [False] * 2),  # nosec B311
        temperature=0.7,
        max_tokens=200,
    )

print(f"✅ Logged {20} current metrics with regressions")

print("\n" + "=" * 60)
print("🔍 PERFORMANCE MONITORING TEST")
print("=" * 60)

# Set up automated monitoring
monitor = PerformanceMonitor(versioner=pv)

# Check if we have enough prompts and versions to test
prompts = pv.list_prompts()
print(f"📊 Found {len(prompts)} prompts: {prompts}")

if prompts:
    prompt_name = "test_classifier"
    versions = pv.list_versions(prompt_name)
    print(f"📋 Found {len(versions)} versions for '{prompt_name}'")

    if len(versions) >= 2:
        # Check for regressions between versions
        current_v = versions[0]["version"]  # Latest
        baseline_v = versions[1]["version"]  # Previous

        print(f"🔍 Checking regressions: {baseline_v} → {current_v}")

        # Define custom thresholds (optional)
        thresholds = {
            "cost": 0.20,  # 20% cost increase threshold
            "latency": 0.30,  # 30% latency increase threshold
            "quality": -0.10,  # 10% quality decrease threshold
            "error_rate": 0.05,  # 5% error rate increase threshold
        }

        # Check for performance regressions
        alerts = monitor.check_regression(
            name=prompt_name,
            current_version=current_v,
            baseline_version=baseline_v,
            thresholds=thresholds,
        )

        if alerts:
            print(f"\n⚠️  Found {len(alerts)} performance alerts:")
            for i, alert in enumerate(alerts, 1):
                print(f"   {i}. {alert.alert_type.value}: {alert.message}")
                print(
                    f"      Baseline: {alert.baseline_value:.4f} → Current: {alert.current_value:.4f}"
                )
                print(
                    f"      Change: {alert.change_percent:+.1f}% (threshold: {alert.threshold:.0f}%)"
                )
                print()
        else:
            print("✅ No performance regressions detected!")

        # Add alert handler for future monitoring
        def alert_handler(alert):
            print(f"🚨 REAL-TIME ALERT: {alert.alert_type.value} for {alert.prompt_name}")
            print(f"    {alert.message}")
            print(f"    Change: {alert.change_percent:+.1f}%")

        monitor.add_alert_handler(alert_handler)
        print("📡 Alert handler registered for future monitoring")

        # Show metrics summary
        print("\n📈 Metrics Summary:")
        baseline_metrics = pv.storage.get_metrics_summary(versions[1]["id"])
        current_metrics = pv.storage.get_metrics_summary(versions[0]["id"])

        if baseline_metrics and current_metrics:
            print(
                f"   Cost:    {baseline_metrics.get('avg_cost', 0):.4f} → {current_metrics.get('avg_cost', 0):.4f}"
            )
            print(
                f"   Latency: {baseline_metrics.get('avg_latency', 0):.1f}ms → {current_metrics.get('avg_latency', 0):.1f}ms"
            )
            print(
                f"   Quality: {baseline_metrics.get('avg_quality', 0):.3f} → {current_metrics.get('avg_quality', 0):.3f}"
            )
            print(
                f"   Success: {baseline_metrics.get('success_rate', 0):.1%} → {current_metrics.get('success_rate', 0):.1%}"
            )

    else:
        print("⚠️  Need at least 2 versions to check for regressions")
else:
    print("⚠️  No prompts found. Create some prompts first with basic_usage.py")

print("\n✅ Performance monitoring test complete!")
