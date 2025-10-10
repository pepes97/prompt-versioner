"""Test script with full metrics tracking."""

import sys
from pathlib import Path
import time
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_versioner.core import PromptVersioner


def simulate_llm_call(prompt_data, model="claude-sonnet-4"):
    """Simulate an LLM call with metrics."""
    # Simulate processing time
    time.sleep(random.uniform(0.1, 0.3))  # nosec B311

    # Simulate token usage
    input_tokens = len(prompt_data["system"].split()) * 1.3 + len(prompt_data["user"].split()) * 1.3
    output_tokens = random.randint(50, 200)  # nosec B311

    # Simulate latency
    latency_ms = random.uniform(200, 800)  # nosec B311

    # Simulate quality metrics
    quality_score = random.uniform(0.75, 0.95)  # nosec B311
    accuracy = random.uniform(0.80, 0.98)  # nosec B311

    return {
        "model_name": model,
        "input_tokens": int(input_tokens),
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
        "quality_score": quality_score,
        "accuracy": accuracy,
        "temperature": 0.7,
        "max_tokens": 1000,
        "success": True,
    }


def main():
    print("=" * 80)
    print("Testing Prompt Versioner with Full Metrics")
    print("=" * 80)

    # Initialize
    pv = PromptVersioner(project_name="metrics-test", enable_git=False)

    # Create a prompt
    print("\n1. Creating code review prompt...")

    latest = pv.get_latest("code_reviewer")
    version_str = latest["version"]
    print(f"Created version: {version_str}")

    # Simulate multiple LLM calls with metrics
    print("\n2. Simulating 10 LLM calls with metrics...")

    for i in range(10):
        # Simulate call
        prompt_data = {
            "system": latest["system_prompt"],
            "user": latest["user_prompt"].replace("{code}", "def hello(): pass"),
        }

        metrics = simulate_llm_call(prompt_data, model="gpt-4")

        # Log metrics
        pv.log_metrics(name="code_reviewer", version=version_str, **metrics)

        print(
            f"   Call {i+1}: {metrics['input_tokens']} in + {metrics['output_tokens']} out = "
            f"{metrics['input_tokens'] + metrics['output_tokens']} tokens, "
            f"{metrics['latency_ms']:.0f}ms, quality={metrics['quality_score']:.2f}"
        )

    print("Logged 10 calls")

    # Create an improved version
    print("\n3. Creating improved version...")
    pv.save_version(
        name="code_reviewer",
        system_prompt="You are an EXPERT code reviewer with deep knowledge of software engineering. "
        "Analyze code for quality, bugs, security, and performance improvements.",
        user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
        metadata={"type": "code_review", "language": "python", "improvement": "more detailed"},
    )

    latest_v2 = pv.get_latest("code_reviewer")
    version_v2 = latest_v2["version"]
    print(f"Created version: {version_v2}")

    # Simulate calls for v2 (slightly better metrics)
    print("\n4. Simulating 8 LLM calls for v2...")

    for i in range(8):
        prompt_data = {
            "system": latest_v2["system_prompt"],
            "user": latest_v2["user_prompt"].replace("{code}", "def process(data): return data"),
        }

        metrics = simulate_llm_call(prompt_data, model="claude-sonnet-4")
        # Make v2 slightly better
        metrics["quality_score"] = min(0.98, metrics["quality_score"] + 0.05)
        metrics["accuracy"] = min(0.99, metrics["accuracy"] + 0.03)

        pv.log_metrics(name="code_reviewer", version=version_v2, **metrics)

        print(
            f"   Call {i+1}: quality={metrics['quality_score']:.2f}, "
            f"accuracy={metrics['accuracy']:.2f}"
        )

    print("Logged 8 calls for v2")

    # Show summary
    print("\n5. Metrics Summary:")
    print("-" * 80)

    versions = pv.list_versions("code_reviewer")
    for v in versions:
        summary = pv.storage.get_metrics_summary(v["id"])
        if summary and summary.get("call_count", 0) > 0:
            print(f"\n  Version: {v['version']}")
            print(f"    Calls: {summary['call_count']}")
            print(f"    Avg Tokens: {summary['avg_total_tokens']:.0f}")
            print(f"    Total Cost: €{summary['total_cost']:.4f}")
            print(f"    Avg Latency: {summary['avg_latency']:.0f}ms")
            print(f"    Avg Quality: {summary['avg_quality']:.2%}")
            print(f"    Avg Accuracy: {summary['avg_accuracy']:.2%}")
            print(f"    Success Rate: {summary['success_rate']:.2%}")

    # Create another prompt type
    print("\n6. Creating summarization prompt...")
    pv.save_version(
        name="summarizer",
        system_prompt="You are a skilled summarization assistant.",
        user_prompt="Summarize: {text}",
        metadata={"type": "summarization"},
    )

    latest_sum = pv.get_latest("summarizer")

    # Add some metrics
    for i in range(5):
        pv.log_metrics(
            name="summarizer",
            version=latest_sum["version"],
            model_name="gpt-4-turbo",
            input_tokens=random.randint(500, 1000),  # nosec B311
            output_tokens=random.randint(100, 200),  # nosec B311
            latency_ms=random.uniform(300, 600),  # nosec B311
            quality_score=random.uniform(0.85, 0.95),  # nosec B311
            temperature=0.5,
            max_tokens=500,
            success=True,
        )

    print("Created summarizer with 5 calls")

    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)
    print(f"\nDatabase: {pv.storage.db_path}")
    print(f"Tracked prompts: {pv.list_prompts()}")
    print("\nNow run: poetry run python run_dashboard.py")
    print("   Then open: http://localhost:5000")


if __name__ == "__main__":
    main()
