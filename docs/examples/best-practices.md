# Best Practices

Comprehensive best practices guide for using **Prompt Versioner** effectively in production.

## 🎯 General Principles

### 1. Start Simple, Evolve Gradually

```python
from prompt_versioner import PromptVersioner, VersionBump

# ✅ Good: Start with basic setup
pv = PromptVersioner(project_name="my-app", enable_git=False)

# Save your first version
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful assistant.",
    user_prompt="Help with: {query}",
    bump_type=VersionBump.MAJOR
)

# ❌ Avoid: Complex setup from the beginning
# Don't start with advanced features like pre-release versions,
# complex metadata, or extensive integrations
```

### 2. Consistent Naming Conventions

```python
# ✅ Good: Descriptive, consistent names
good_names = [
    "email_classifier",      # Clear purpose
    "code_reviewer",         # Descriptive function
    "customer_service_bot",  # Specific domain
    "content_summarizer"     # Clear action
]

# ❌ Avoid: Vague or inconsistent names
bad_names = [
    "prompt1",              # Not descriptive
    "the_ai_thing",         # Too vague
    "EmailClassifierV2",    # Inconsistent casing
    "temp_prompt"           # Temporary names in production
]

# Use consistent naming pattern
def create_prompt_name(domain, function, variant=None):
    """Create consistent prompt names"""
    name = f"{domain}_{function}"
    if variant:
        name += f"_{variant}"
    return name.lower()

# Examples
print(create_prompt_name("customer", "service"))        # "customer_service"
print(create_prompt_name("code", "review", "python"))   # "code_review_python"
```

## 📝 Version Management Best Practices

### Semantic Versioning Strategy

```python
# ✅ Good: Clear versioning strategy
class VersioningStrategy:

    @staticmethod
    def patch_for_fixes():
        """Use PATCH for typos, small corrections"""
        return VersionBump.PATCH
        # Examples: Fix typos, grammar corrections, small clarifications

    @staticmethod
    def minor_for_enhancements():
        """Use MINOR for new features, improvements"""
        return VersionBump.MINOR
        # Examples: Add new instructions, improve clarity, extend functionality

    @staticmethod
    def major_for_breaking_changes():
        """Use MAJOR for fundamental changes"""
        return VersionBump.MAJOR
        # Examples: Complete rewrites, change in purpose, different output format

# Document your changes
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert Python code reviewer...",  # Enhanced
    user_prompt="Review this Python code...",
    bump_type=VersioningStrategy.minor_for_enhancements(),
    metadata={
        "change_summary": "Added Python-specific expertise",
        "author": "dev-team",
        "reasoning": "Improved accuracy for Python code reviews"
    }
)

# Add meaningful annotations
pv.add_annotation(
    name="code_reviewer",
    version="1.1.0",
    text="Tested on 100+ Python files, shows 15% improvement in review quality",
    author="qa-team"
)
```

### Metadata Best Practices

```python
# ✅ Good: Comprehensive, structured metadata
def create_standard_metadata(author, purpose, testing_info=None):
    """Create standardized metadata"""

    metadata = {
        # Who and when
        "author": author,
        "created_by_team": author.split("@")[1] if "@" in author else "unknown",
        "creation_date": datetime.now().isoformat(),

        # What and why
        "purpose": purpose,
        "change_type": "enhancement",  # enhancement, fix, feature, breaking

        # Quality assurance
        "tested": testing_info is not None,
        "approval_required": True,
        "production_ready": False,

        # Context
        "target_model": "gpt-4o",
        "expected_use_cases": [],
        "known_limitations": []
    }

    if testing_info:
        metadata.update(testing_info)

    return metadata

# Usage
metadata = create_standard_metadata(
    author="alice@company.com",
    purpose="Improve code review accuracy for Python projects",
    testing_info={
        "test_cases": 50,
        "quality_threshold": 0.85,
        "performance_benchmark": "latency < 500ms"
    }
)

pv.save_version(
    name="code_reviewer",
    system_prompt="...",
    user_prompt="...",
    bump_type=VersionBump.MINOR,
    metadata=metadata
)
```

## 📊 Metrics and Monitoring

### Multi-Model Performance Tracking

When testing across multiple models, always include the `model_name` parameter:

```python
# ✅ Good: Track model-specific performance
models_to_test = ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet", "gemini-pro"]

for model in models_to_test:
    response = call_llm(model, prompt)

    pv.log_metrics(
        prompt_name="classifier",
        version="1.0.0",
        model_name=model,  # ✅ Always specify the model
        prompt_tokens=response.prompt_tokens,
        completion_tokens=response.completion_tokens,
        latency_ms=response.latency,
        quality_score=evaluate_response(response),
        cost=calculate_cost(model, response)
    )

# ❌ Avoid: Missing model_name or inconsistent naming
pv.log_metrics(
    prompt_name="classifier",
    version="1.0.0",
    # model_name missing - can't compare models!
    ...
)

# ❌ Avoid: Inconsistent model naming
pv.log_metrics(model_name="GPT-4")  # Inconsistent casing
pv.log_metrics(model_name="gpt4")   # Missing delimiter
pv.log_metrics(model_name="openai-gpt-4-turbo")  # Too verbose
```

**Best practices for model naming:**
- Use consistent, lowercase names: `gpt-4o`, `claude-3-5-sonnet`, `gemini-pro`
- Match official provider naming where possible
- Keep names concise but descriptive
- Use hyphens for multi-word names

### Comprehensive Metrics Tracking

```python
class MetricsTracker:
    """Standardized metrics tracking"""

    def __init__(self, pv):
        self.pv = pv

    def log_production_metrics(self, prompt_name, version, llm_response,
                             model_name=None, user_context=None, quality_score=None):
        """Log comprehensive production metrics"""

        # Calculate quality if not provided
        if quality_score is None:
            quality_score = self.evaluate_quality(llm_response)

        # Standard metrics
        self.pv.log_metrics(
            name=prompt_name,
            version=version,

            # LLM performance
            model_name=llm_response.model,
            input_tokens=llm_response.usage.prompt_tokens,
            output_tokens=llm_response.usage.completion_tokens,
            latency_ms=llm_response.latency_ms,

            # Cost tracking
            cost_eur=self.calculate_cost(llm_response),

            # Quality assessment
            quality_score=quality_score,
            success=llm_response.success,
            error_message=llm_response.error if not llm_response.success else None,

            # Model parameters
            temperature=llm_response.temperature,
            max_tokens=llm_response.max_tokens,

            # Context
            metadata={
                "user_id": user_context.get("user_id") if user_context else None,
                "session_id": user_context.get("session_id") if user_context else None,
                "environment": "production",
                "user_feedback": None,  # To be updated later
                "business_context": user_context.get("context") if user_context else None
            }
        )

    def evaluate_quality(self, response):
        """Evaluate response quality (implement your logic)"""
        # Implement your quality evaluation logic
        # This could involve sentiment analysis, coherence checks, etc.
        return 0.85  # Placeholder

    def calculate_cost(self, response):
        """Calculate cost in EUR"""
        # Implement your cost calculation
        return 0.003  # Placeholder

# Usage
tracker = MetricsTracker(pv)

# In production code
# tracker.log_production_metrics(
#     "customer_service", "2.1.0",
#     llm_response, user_context, quality_score
# )
```

### Performance Monitoring

```python
def setup_performance_monitoring(pv, critical_prompts):
    """Set up automated performance monitoring"""

    thresholds = {
        "min_quality": 0.8,
        "max_latency": 1000,
        "min_success_rate": 0.95,
        "max_cost_per_call": 0.01
    }

    def check_prompt_health(prompt_name, version):
        """Check if prompt meets performance thresholds"""

        version_data = pv.get_version(prompt_name, version)
        recent_metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=100)

        if len(recent_metrics) < 10:
            return {"status": "insufficient_data"}

        # Calculate current performance
        avg_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / len(recent_metrics)
        avg_latency = sum(m.get("latency_ms", 0) for m in recent_metrics) / len(recent_metrics)
        success_rate = sum(1 for m in recent_metrics if m.get("success", True)) / len(recent_metrics)
        avg_cost = sum(m.get("cost_eur", 0) for m in recent_metrics) / len(recent_metrics)

        # Check thresholds
        issues = []
        if avg_quality < thresholds["min_quality"]:
            issues.append(f"Quality below threshold: {avg_quality:.2f}")
        if avg_latency > thresholds["max_latency"]:
            issues.append(f"Latency above threshold: {avg_latency:.0f}ms")
        if success_rate < thresholds["min_success_rate"]:
            issues.append(f"Success rate below threshold: {success_rate:.1%}")
        if avg_cost > thresholds["max_cost_per_call"]:
            issues.append(f"Cost above threshold: €{avg_cost:.4f}")

        return {
            "status": "healthy" if not issues else "unhealthy",
            "issues": issues,
            "metrics": {
                "quality": avg_quality,
                "latency": avg_latency,
                "success_rate": success_rate,
                "cost": avg_cost
            }
        }

    # Monitor all critical prompts
    print("🔍 Health Check Results:")
    for prompt_name, version in critical_prompts:
        health = check_prompt_health(prompt_name, version)
        status_emoji = "✅" if health["status"] == "healthy" else "❌"

        print(f"{status_emoji} {prompt_name} v{version}: {health['status']}")
        for issue in health.get("issues", []):
            print(f"    ⚠️ {issue}")

# Monitor critical prompts
critical_prompts = [
    ("customer_service", "2.1.0"),
    ("code_reviewer", "1.1.0"),
    ("content_generator", "1.3.0")
]

setup_performance_monitoring(pv, critical_prompts)
```

## 🧪 Testing Best Practices

### Systematic Testing Approach

```python
class PromptTestSuite:
    """Comprehensive testing for prompt versions"""

    def __init__(self, pv):
        self.pv = pv
        self.test_cases = []

    def add_test_case(self, name, input_data, expected_criteria):
        """Add a test case to the suite"""
        self.test_cases.append({
            "name": name,
            "input": input_data,
            "criteria": expected_criteria
        })

    def run_tests(self, prompt_name, version):
        """Run all test cases for a prompt version"""

        results = []

        print(f"🧪 Running {len(self.test_cases)} tests for {prompt_name} v{version}")

        for test_case in self.test_cases:
            with self.pv.test_version(prompt_name, version) as test:
                # Simulate LLM call (replace with actual call)
                result = self.simulate_llm_call(test_case["input"])

                # Evaluate against criteria
                evaluation = self.evaluate_result(result, test_case["criteria"])

                # Log test metrics
                test.log(
                    tokens=result["tokens"],
                    cost=result["cost"],
                    latency_ms=result["latency"],
                    quality_score=evaluation["quality"],
                    metadata={
                        "test_case": test_case["name"],
                        "passed": evaluation["passed"],
                        "criteria_met": evaluation["criteria_met"]
                    }
                )

                results.append({
                    "test_case": test_case["name"],
                    "passed": evaluation["passed"],
                    "quality": evaluation["quality"],
                    "details": evaluation
                })

        return self.generate_test_report(results)

    def simulate_llm_call(self, input_data):
        """Simulate LLM call (replace with actual implementation)"""
        import random
        return {
            "tokens": random.randint(100, 300),
            "cost": random.uniform(0.001, 0.005),
            "latency": random.uniform(200, 800),
            "content": f"Response to: {input_data[:50]}"
        }

    def evaluate_result(self, result, criteria):
        """Evaluate result against test criteria"""

        quality = random.uniform(0.7, 0.95)  # Replace with actual evaluation

        criteria_met = {
            "quality": quality >= criteria.get("min_quality", 0.8),
            "latency": result["latency"] <= criteria.get("max_latency", 1000),
            "cost": result["cost"] <= criteria.get("max_cost", 0.01)
        }

        passed = all(criteria_met.values())

        return {
            "passed": passed,
            "quality": quality,
            "criteria_met": criteria_met
        }

    def generate_test_report(self, results):
        """Generate comprehensive test report"""

        total_tests = len(results)
        passed_tests = sum(1 for r in results if r["passed"])
        avg_quality = sum(r["quality"] for r in results) / total_tests

        print(f"\n📊 Test Results Summary:")
        print(f"Tests passed: {passed_tests}/{total_tests} ({passed_tests/total_tests:.1%})")
        print(f"Average quality: {avg_quality:.2f}")

        if passed_tests == total_tests:
            print("✅ All tests passed! Ready for deployment.")
        else:
            print("❌ Some tests failed. Review before deployment.")
            for result in results:
                if not result["passed"]:
                    print(f"  Failed: {result['test_case']}")

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": passed_tests / total_tests,
            "avg_quality": avg_quality,
            "results": results
        }

# Usage
test_suite = PromptTestSuite(pv)

# Add test cases
test_suite.add_test_case(
    "simple_query",
    "What is Python?",
    {"min_quality": 0.8, "max_latency": 500, "max_cost": 0.005}
)

test_suite.add_test_case(
    "complex_query",
    "Explain advanced Python metaclasses with examples",
    {"min_quality": 0.85, "max_latency": 1000, "max_cost": 0.01}
)

test_suite.add_test_case(
    "edge_case",
    "Handle this ambiguous request...",
    {"min_quality": 0.7, "max_latency": 800, "max_cost": 0.008}
)

# Run tests
report = test_suite.run_tests("code_assistant", "1.2.0")
```
## 🎯 Team Collaboration

### Code Review Process for Prompts

```python
def create_prompt_review_request(pv, prompt_name, old_version, new_version, reviewers):
    """Create a structured prompt review request"""

    # Generate diff
    diff = pv.diff(prompt_name, old_version, new_version, format_output=False)

    # Create review request annotation
    review_request = f"""
PROMPT REVIEW REQUEST
===================
Prompt: {prompt_name}
Change: {old_version} → {new_version}
Reviewers: {', '.join(reviewers)}

CHANGES SUMMARY:
{diff.summary}

REVIEW CHECKLIST:
□ Prompt clarity and specificity
□ Expected behavior alignment
□ Performance implications
□ Security considerations
□ Testing requirements

Please review and add APPROVED/REJECTED annotation.
    """.strip()

    pv.add_annotation(
        name=prompt_name,
        version=new_version,
        text=review_request,
        author="review-system"
    )

    print(f"📝 Review request created for {prompt_name} v{new_version}")
    print(f"Reviewers: {', '.join(reviewers)}")

def approve_prompt_change(pv, prompt_name, version, reviewer, approved=True, comments=""):
    """Approve or reject a prompt change"""

    status = "APPROVED" if approved else "REJECTED"

    approval_text = f"[{status}] {comments}" if comments else f"[{status}]"

    pv.add_annotation(
        name=prompt_name,
        version=version,
        text=approval_text,
        author=reviewer
    )

    print(f"{'✅' if approved else '❌'} {status} by {reviewer}")

# Example workflow
create_prompt_review_request(
    pv, "customer_service", "2.0.0", "2.1.0",
    ["senior-dev@company.com", "product-owner@company.com"]
)

approve_prompt_change(
    pv, "customer_service", "2.1.0",
    "senior-dev@company.com", True,
    "Looks good, improved clarity and specificity"
)
```

## 📚 Next Steps

- [Advanced Workflows](../examples/advanced-workflows.md) - Complex deployment patterns
- [Integrations](../examples/integrations.md) - Tool and framework integrations
- [Performance Monitoring](../user-guide/performance-monitoring.md) - Monitor your systems
