"""Example usage of prompt-versioner library."""

import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_versioner.core import PromptVersioner
from prompt_versioner.testing import PromptTestRunner, TestDataset
from prompt_versioner.metrics import MetricsTracker

# Initialize versioner
pv = PromptVersioner(project_name="example-app", enable_git=True)


# Example 1: Decorator-based tracking
@pv.track(name="code_reviewer", auto_commit=True)
def get_code_review_prompts(code: str, language: str = "python"):
    """Generate prompts for code review."""
    system = f"""You are an expert {language} code reviewer.
Analyze code for:
- Code quality and best practices
- Potential bugs and edge cases
- Performance improvements
- Security vulnerabilities

Provide constructive feedback with specific suggestions."""

    user = f"""Review the following {language} code:

```{language}
{code}
```

Provide a detailed code review."""

    return {"system": system, "user": user}


# Example 2: Manual versioning with metadata
def save_summarization_prompt():
    """Save a summarization prompt manually."""
    pv.save_version(
        name="document_summarizer",
        system_prompt="""You are an AI assistant specialized in summarization.
Create concise, accurate summaries that capture key points while maintaining context.
Use bullet points for clarity when appropriate.""",
        user_prompt="Summarize the following document:\n\n{document}",
        metadata={
            "tags": ["summarization", "production"],
            "model": "claude-sonnet-4",
            "author": "team@example.com",
        },
    )


# Example 3: Testing prompts with datasets
def test_code_review_prompt():
    """Test the code review prompt with various examples."""

    # Create test dataset
    dataset = TestDataset("code_review_tests")

    # Add test cases
    dataset.add_test(
        name="simple_function",
        inputs={
            "code": "def add(a, b):\n    return a + b",
            "language": "python",
        },
        validation_fn=lambda output: len(output) > 50 and "function" in output.lower(),
    )

    dataset.add_test(
        name="with_bug",
        inputs={
            "code": "def divide(a, b):\n    return a / b  # Missing zero check!",
            "language": "python",
        },
        validation_fn=lambda output: "zero" in output.lower() or "division" in output.lower(),
    )

    dataset.add_test(
        name="complex_function",
        inputs={
            "code": """def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result""",
            "language": "python",
        },
        validation_fn=lambda output: len(output) > 100,
    )

    # Create test runner
    runner = PromptTestRunner(max_workers=4)

    # Mock LLM function (replace with your actual LLM call)
    def mock_llm_call(inputs):
        prompts = get_code_review_prompts(inputs["code"], inputs["language"])
        # In real usage: return call_to_llm(prompts["system"], prompts["user"])
        return f"Code review completed for {inputs['language']} code."

    # Run tests
    results = runner.run_tests(
        test_cases=dataset.get_tests(),
        prompt_fn=mock_llm_call,
        metric_fn=lambda output: {
            "tokens": len(output.split()),
            "cost": 0.002,
            "quality": 0.9,
        },
        parallel=True,
    )

    # Get summary
    summary = runner.get_summary(results)
    print(runner.format_summary(summary))

    return results


# Example 4: Version comparison
def compare_prompt_versions():
    """Compare different versions of a prompt."""

    # Save multiple versions
    for i, temp in enumerate([0.7, 0.8, 0.9]):
        pv.save_version(
            name="creative_writer",
            system_prompt=f"You are a creative writer. Temperature: {temp}",
            user_prompt="Write a story about: {{topic}}",
            version=f"v1.{i}.0",
            metadata={"temperature": temp},
        )

    # Compare versions
    diff = pv.diff("creative_writer", "v1.0.0", "v1.2.0", format_output=True)

    # Get all versions
    versions = pv.list_versions("creative_writer")
    print(f"\nFound {len(versions)} versions of 'creative_writer'")

    # Compare metrics across versions
    comparison = pv.compare_versions("creative_writer", ["v1.0.0", "v1.1.0", "v1.2.0"])
    print("\nVersion comparison:", comparison)


# Example 5: Rollback to previous version
def rollback_example():
    """Demonstrate rollback functionality."""

    # Get current version
    latest = pv.get_latest("code_reviewer")
    print(f"Current version: {latest['version']}")

    # Rollback to previous version
    versions = pv.list_versions("code_reviewer")
    if len(versions) > 1:
        previous = versions[1]
        new_id = pv.rollback("code_reviewer", previous["version"])
        print(f"Rolled back to {previous['version']}, created new version with ID: {new_id}")


# Example 6: Testing with context manager
def test_with_context_manager():
    """Use context manager for cleaner testing."""

    with pv.test_version("code_reviewer", "v1.0.0") as test:
        # Simulate LLM call
        prompts = get_code_review_prompts("def hello(): pass")
        result = "Mock LLM response"  # Replace with actual call

        # Log metrics
        test.log(
            tokens=150,
            cost=0.002,
            quality_score=0.95,
            latency_ms=450,
        )


# Example 7: Metric analysis
def analyze_metrics():
    """Analyze metrics across versions."""

    # Get metrics for two versions
    v1 = pv.get_version("code_reviewer", "v1.0.0")
    v2 = pv.get_version("code_reviewer", "v1.1.0")

    if v1 and v2:
        metrics_v1 = pv.storage.get_metrics(v1["id"])
        metrics_v2 = pv.storage.get_metrics(v2["id"])

        # Compare metrics
        comparison = MetricsTracker.compare_metrics(metrics_v1, metrics_v2)
        formatted = MetricsTracker.format_metric_comparison(comparison)
        print(formatted)

        # Detect regressions
        regressions = MetricsTracker.detect_regression(metrics_v1, metrics_v2, threshold=0.05)
        if regressions:
            print(f"\n⚠️  Regressions detected in: {', '.join(regressions)}")


if __name__ == "__main__":
    print("=" * 80)
    print("Prompt Versioner - Example Usage")
    print("=" * 80)

    # Run examples
    print("\n1. Saving prompts...")
    save_summarization_prompt()
    code_prompts = get_code_review_prompts("def test(): pass")
    print(f"Generated code review prompts: {list(code_prompts.keys())}")

    print("\n2. Testing prompts...")
    test_code_review_prompt()

    print("\n3. Comparing versions...")
    compare_prompt_versions()

    print("\n4. Listing all tracked prompts...")
    all_prompts = pv.list_prompts()
    print(f"Tracked prompts: {all_prompts}")

    print("\n✅ Examples completed!")