"""Test script with full metrics tracking and new features."""

import sys
from pathlib import Path
import time
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_versioner.core import PromptVersioner, VersionBump
from prompt_versioner.testing import ABTest
from prompt_versioner.monitoring import PerformanceMonitor


def simulate_llm_call(prompt_data, model="claude-sonnet-4"):
    """Simulate an LLM call with metrics."""
    time.sleep(random.uniform(0.05, 0.15))

    input_tokens = len(prompt_data["system"].split()) * 1.3 + len(prompt_data["user"].split()) * 1.3
    output_tokens = random.randint(50, 200)
    latency_ms = random.uniform(200, 800)
    quality_score = random.uniform(0.75, 0.95)
    accuracy = random.uniform(0.80, 0.98)

    return {
        "model_name": model,
        "input_tokens": int(input_tokens),
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
        "quality_score": quality_score,
        "accuracy": accuracy,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 1000,
        "success": True,
    }


def main():
    print("=" * 80)
    print("Testing Prompt Versioner - All Features")
    print("=" * 80)

    pv = PromptVersioner(project_name="full-test", enable_git=False)

    # 1. Semantic Versioning
    print("\n1. Testing Semantic Versioning...")
    pv.save_version(
        name="code_reviewer",
        system_prompt="You are an expert code reviewer.",
        user_prompt="Review this code:\n{code}",
        bump_type=VersionBump.MAJOR,  # First version: 1.0.0
        metadata={"type": "code_review"},
    )

    v1 = pv.get_latest("code_reviewer")
    print(f"   Created version: {v1['version']}")

    # Log metrics for v1
    for i in range(10):

        input_tokens = len(v1["system_prompt"].split()) * 1.3 + len(v1["user_prompt"].split()) * 1.3
        output_tokens = random.randint(50, 200)
        latency_ms = random.uniform(200, 800)
        quality_score = random.uniform(0.75, 0.95)
        accuracy = random.uniform(0.80, 0.98)
        pv.log_metrics(
            name="code_reviewer",
            version=v1["version"],
            model_name="gpt-4o",
            input_tokens=int(input_tokens),
            output_tokens=output_tokens,
            max_tokens=500,
            latency_ms=latency_ms,
            quality_score=quality_score,
            accuracy=accuracy,
        )

    print(f"   Logged 10 calls for {v1['version']}")

    # 2. Annotations
    print("\n2. Testing Annotations...")
    pv.add_annotation(
        name="code_reviewer",
        version=v1["version"],
        text="Initial version. Works well for Python but needs improvement for JavaScript.",
        author="sveva.pepe",
    )
    pv.add_annotation(
        name="code_reviewer",
        version=v1["version"],
        text="Cost is acceptable, quality is good.",
        author="team.lead",
    )
    annotations = pv.get_annotations("code_reviewer", v1["version"])
    print(f"   Added {len(annotations)} annotations")
    for ann in annotations:
        print(f"     - {ann['author']}: {ann['text'][:50]}...")

    # 3. Create improved version (MINOR bump)
    print("\n3. Creating improved version (MINOR)...")
    pv.save_version(
        name="code_reviewer",
        system_prompt="You are an EXPERT code reviewer with deep knowledge of software engineering.",
        user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
        bump_type=VersionBump.MINOR,  # 1.1.0
        metadata={"type": "code_review", "improvement": "more detailed"},
    )

    v2 = pv.get_latest("code_reviewer")

    pv.log_metrics(
        name="code_reviewer",
        version=v2["version"],
        model_name="claude-sonnet-4",
        input_tokens=15,
        output_tokens=35,
        max_tokens=500,
        latency_ms=latency_ms,
        quality_score=quality_score,
        accuracy=accuracy,
    )

    print(f"   Created version: {v2['version']}")

    # 4. A/B Testing
    print("\n4. Running A/B Test...")
    ab_test = ABTest(
        versioner=pv,
        prompt_name="code_reviewer",
        version_a=v1["version"],
        version_b=v2["version"],
        metric_name="quality_score",
    )

    # Simulate A/B test calls
    for i in range(15):
        # Test version A
        metrics_a = simulate_llm_call({"system": v1["system_prompt"], "user": v1["user_prompt"]})
        pv.log_metrics(name="code_reviewer", version=v1["version"], **metrics_a)
        ab_test.log_result("a", metrics_a["quality_score"])

        # Test version B (slightly better)
        metrics_b = simulate_llm_call({"system": v2["system_prompt"], "user": v2["user_prompt"]})
        metrics_b["quality_score"] = min(0.98, metrics_b["quality_score"] + 0.05)
        pv.log_metrics(name="code_reviewer", version=v2["version"], **metrics_b)
        ab_test.log_result("b", metrics_b["quality_score"])

    ab_test.print_result()

    # 5. Performance Monitoring
    print("\n5. Testing Performance Monitoring...")
    monitor = PerformanceMonitor(pv)

    # Add alert handler
    def alert_handler(alert):
        print(f"   ALERT: {alert.alert_type.value.upper()}")
        print(f"     {alert.message}")
        print(f"     Baseline: {alert.baseline_value:.4f}, Current: {alert.current_value:.4f}")

    monitor.add_alert_handler(alert_handler)

    # Check for regressions
    alerts = monitor.check_regression(
        name="code_reviewer",
        current_version=v2["version"],
        baseline_version=v1["version"],
        thresholds={"cost": 0.15, "latency": 0.20, "quality": -0.05},
    )

    if alerts:
        print(f"   Found {len(alerts)} alert(s)")
    else:
        print("   No performance regressions detected")

    # 6. Export/Import
    print("\n6. Testing Export/Import...")
    export_file = Path("test_export.json")
    pv.export_prompt("code_reviewer", export_file, include_metrics=True)
    print(f"   Exported to {export_file}")

    # Create a new prompt to test import
    pv.save_version(
        name="test_import", system_prompt="test", user_prompt="test", bump_type=VersionBump.MAJOR
    )

    # # Import back
    # result = pv.import_prompt(export_file, overwrite=True)
    # print(f"   Import result: {result['imported']} imported, {result['skipped']} skipped")

    # Cleanup
    export_file.unlink()

    # 7. Create additional prompts for dashboard testing
    print("\n7. Creating additional prompts...")

    # Summarizer
    pv.save_version(
        name="summarizer",
        system_prompt="You are a skilled summarization assistant.",
        user_prompt="Summarize: {text}",
        bump_type=VersionBump.MAJOR,
        metadata={"type": "summarization"},
    )

    latest_sum = pv.get_latest("summarizer")
    for i in range(8):
        pv.log_metrics(
            name="summarizer",
            version=latest_sum["version"],
            model_name="gpt-4o",
            input_tokens=random.randint(500, 1000),
            output_tokens=random.randint(100, 200),
            latency_ms=random.uniform(300, 600),
            quality_score=random.uniform(0.85, 0.95),
            temperature=0.5,
            top_p=1.0,
            max_tokens=500,
            success=True,
        )

    pv.add_annotation(
        name="summarizer",
        version=latest_sum["version"],
        text="Perfect for blog posts and articles",
        author="content.team",
    )

    # Entity extractor
    pv.save_version(
        name="entity_extractor",
        system_prompt="You are an entity extraction specialist.",
        user_prompt="Extract entities from: {text}",
        bump_type=VersionBump.MAJOR,
        metadata={"type": "extraction"},
    )

    latest_entity = pv.get_latest("entity_extractor")
    for i in range(12):
        pv.log_metrics(
            name="entity_extractor",
            version=latest_entity["version"],
            model_name="claude-sonnet-4",
            input_tokens=random.randint(200, 500),
            output_tokens=random.randint(50, 150),
            latency_ms=random.uniform(250, 500),
            quality_score=random.uniform(0.88, 0.96),
            accuracy=random.uniform(0.85, 0.95),
            temperature=0.3,
            top_p=0.9,
            max_tokens=800,
            success=random.choice([True, True, True, False]),  # 75% success rate
        )

    print("   Created 3 prompts with metrics")

    # 8. Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    all_prompts = pv.list_prompts()
    print(f"\nTotal Prompts: {len(all_prompts)}")

    for prompt_name in all_prompts:
        versions = pv.list_versions(prompt_name)
        print(f"\n  {prompt_name}:")
        print(f"    Versions: {len(versions)}")

        for v in versions[:2]:  # Show first 2 versions
            summary = pv.storage.get_metrics_summary(v["id"])
            annotations = pv.get_annotations(prompt_name, v["version"])

            if summary and summary.get("call_count", 0) > 0:
                print(
                    f"    - {v['version']}: {summary['call_count']} calls, "
                    f"${summary['total_cost']:.4f} cost, "
                    f"{summary['avg_quality']:.1%} quality, "
                    f"{len(annotations)} annotations"
                )

    print("\n" + "=" * 80)
    print("All Features Tested Successfully!")
    print("=" * 80)
    print(f"\nDatabase: {pv.storage.db_path}")
    print("\nNext steps:")
    print("  1. Run dashboard: poetry run python run_dashboard.py")
    print("  2. Open: http://localhost:5000")
    print("  3. Test search/filter in the dashboard")
    print("  4. Toggle light/dark mode")
    print("  5. View annotations and metrics")


if __name__ == "__main__":
    main()
