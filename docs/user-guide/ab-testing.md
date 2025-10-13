# A/B Testing

Compare prompt versions scientifically to optimize performance with **Prompt Versioner**'s A/B testing framework.

## 🧪 Quick Start

```python
from prompt_versioner import PromptVersioner, ABTest
import random

# Initialize versioner
pv = PromptVersioner(project_name="my-project", enable_git=False)

# Create an A/B test
ab_test = ABTest(
    versioner=pv,
    prompt_name="code_reviewer",
    version_a="1.0.0",    # Baseline version
    version_b="1.1.0",    # Test version
    metric_name="quality_score",
)

# Log test results
for i in range(20):
    # Version A results (baseline)
    metric_value = random.uniform(0.75, 0.85)
    ab_test.log_result("a", metric_value)

    # Version B results (test)
    metric_value = random.uniform(0.80, 0.90)
    ab_test.log_result("b", metric_value)

# Check if ready and get results
if ab_test.is_ready(min_samples=15):
    result = ab_test.get_result()
    print(f"🏆 Winner: {result.winner}")
    print(f"📈 Improvement: {result.improvement:.2f}%")
    print(f"🎯 Confidence: {result.confidence:.1%}")

    # Print detailed results
    ab_test.print_result()
```

## 🔧 Setting Up Tests

### 1. Create Test Versions

First, create the prompt versions you want to test:

```python
from prompt_versioner import PromptVersioner, VersionBump

pv = PromptVersioner(project_name="my-project", enable_git=False)

# Create baseline version
pv.save_version(
    name="summarizer",
    system_prompt="You are a summarization assistant.",
    user_prompt="Summarize: {text}",
    bump_type=VersionBump.MAJOR,  # Creates 1.0.0
)

# Create test version with improvements
pv.save_version(
    name="summarizer",
    system_prompt="You are an expert summarization assistant that creates concise, accurate summaries.",
    user_prompt="Please provide a clear, concise summary of the following text:\n{text}",
    bump_type=VersionBump.MINOR,  # Creates 1.1.0
    metadata={"improvement": "enhanced clarity and instructions"}
)
```

### 2. Initialize A/B Test

```python
from prompt_versioner import ABTest

# Set up the test
ab_test = ABTest(
    versioner=pv,
    prompt_name="summarizer",
    version_a="1.0.0",  # Control/baseline
    version_b="1.1.0",  # Treatment/test
    metric_name="quality_score"
)
```

## 📊 Collecting Results

### Manual Result Logging

```python
# Log individual results
ab_test.log_result("a", 0.85)  # Version A result
ab_test.log_result("b", 0.92)  # Version B result

# Log batch results
batch_results_a = [0.78, 0.82, 0.85, 0.80, 0.88]
batch_results_b = [0.85, 0.90, 0.92, 0.87, 0.94]

ab_test.log_batch_results("a", batch_results_a)
ab_test.log_batch_results("b", batch_results_b)
```

### Integration with Production

```python
def run_prompt_with_testing(text, user_id):
    """Example production integration"""

    # Determine which version to use (simple hash-based assignment)
    version = "a" if hash(user_id) % 2 == 0 else "b"
    prompt_version = "1.0.0" if version == "a" else "1.1.0"

    # Get the prompt
    prompt_data = pv.get_version("summarizer", prompt_version)

    # Run your LLM call here
    result = call_llm(prompt_data, {"text": text})

    # Evaluate quality (your custom scoring logic)
    quality_score = evaluate_response_quality(result)

    # Log the result to A/B test
    ab_test.log_result(version, quality_score)

    return result
```

## 📈 Analyzing Results

### Check Test Status

```python
# Check sample counts
count_a, count_b = ab_test.get_sample_counts()
print(f"Samples: A={count_a}, B={count_b}")

# Check if ready for analysis
if ab_test.is_ready(min_samples=30):
    print("✅ Ready for analysis")
else:
    print("⚠️ Need more samples")
```

### Get Test Results

```python
# Get detailed results
result = ab_test.get_result()

print(f"Version A (Control): {result.version_a}")
print(f"  Mean: {result.a_mean:.3f}")
print(f"  Samples: {len(result.a_values)}")

print(f"Version B (Treatment): {result.version_b}")
print(f"  Mean: {result.b_mean:.3f}")
print(f"  Samples: {len(result.b_values)}")

print(f"\n🏆 Winner: {result.winner}")
print(f"📈 Improvement: {result.improvement:.1f}%")
print(f"🎯 Confidence: {result.confidence:.1%}")

# Print formatted report
ab_test.print_result()
```

### Clear and Reset

```python
# Clear results to start fresh
ab_test.clear_results()

# Verify cleared
count_a, count_b = ab_test.get_sample_counts()
print(f"After clear: A={count_a}, B={count_b}")  # Should be 0, 0
```

## 🎯 Best Practices

### 1. Test Design
- **Single Variable**: Test only one change at a time
- **Clear Hypothesis**: Define what you expect to improve
- **Sufficient Sample Size**: Collect enough data for reliable results

### 2. Sample Collection
- **Random Assignment**: Ensure fair distribution between versions
- **Representative Data**: Use real user scenarios
- **Consistent Metrics**: Use the same evaluation criteria

### 3. Statistical Considerations
- **Minimum Samples**: Collect at least 30 samples per version
- **Statistical Significance**: Higher confidence scores indicate more reliable results
- **Practical Significance**: Consider if improvements are meaningful in practice

### 4. Production Integration
- **Gradual Rollout**: Start with small traffic percentages
- **Monitoring**: Track test health and performance
- **Rollback Plan**: Be ready to revert if issues arise

## 🔍 Example Workflow

Complete example workflow:

```python
from prompt_versioner import PromptVersioner, VersionBump, ABTest

# 1. Initialize
pv = PromptVersioner(project_name="content-ai", enable_git=False)

# 2. Create versions
pv.save_version(
    name="blog_writer",
    system_prompt="Write blog posts.",
    user_prompt="Write about: {topic}",
    bump_type=VersionBump.MAJOR,
)

pv.save_version(
    name="blog_writer",
    system_prompt="You are a professional blog writer. Create engaging, well-structured content.",
    user_prompt="Create a comprehensive blog post about: {topic}\n\nInclude an introduction, main points, and conclusion.",
    bump_type=VersionBump.MINOR,
)

# 3. Set up test
test = ABTest(
    versioner=pv,
    prompt_name="blog_writer",
    version_a="1.0.0",
    version_b="1.1.0",
    metric_name="engagement_score"
)

# 4. Simulate data collection
import random
for i in range(50):
    # Baseline performance
    score_a = random.uniform(0.6, 0.8)
    test.log_result("a", score_a)

    # Improved performance
    score_b = random.uniform(0.7, 0.9)
    test.log_result("b", score_b)

# 5. Analyze results
if test.is_ready():
    result = test.get_result()

    if result.confidence > 0.8:
        print(f"🎉 Strong result: {result.winner} wins!")
        print(f"📊 Improvement: {result.improvement:.1f}%")

        # If B wins, consider promoting it
        if result.winner == "1.1.0":
            print("Consider promoting version 1.1.0 to production")
    else:
        print("📊 Results not yet conclusive, continue testing")

# 6. Check test status
test.print_result()
```

## 📚 Next Steps

- [Metrics Tracking](metrics-tracking.md) - Learn about tracking performance metrics
- [Version Management](version-management.md) - Manage your prompt versions effectively
- [Basic Usage](../examples/basic-usage.md) - More examples and patterns

## 🧪 Introduction to A/B Testing for Prompts

A/B testing allows you to scientifically compare different prompt versions to determine which performs better. This data-driven approach helps you make objective decisions about prompt improvements.

### Why A/B Test Prompts?

- **Objective Optimization**: Remove guesswork and bias from prompt improvement
- **Statistical Confidence**: Make decisions based on statistically significant results
- **Risk Mitigation**: Test changes safely before full deployment
- **Performance Insights**: Understand what makes prompts effective
- **Continuous Improvement**: Establish a culture of data-driven optimization

## 🔬 Core A/B Testing Concepts

### Statistical Foundation

The A/B testing framework in Prompt Versioner provides simple yet powerful tools to compare prompt versions:

```python
from prompt_versioner.testing import ABTest
from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
versioner = PromptVersioner(project_name="ab-test-project")

# Create baseline prompt version
versioner.save_version(
    name="customer_service",
    system_prompt="You are a customer service representative.",
    user_prompt="Help the customer with: {customer_issue}",
    bump_type=VersionBump.MAJOR,
    metadata={"type": "baseline", "tone": "professional"}
)

# Create alternative version to test
versioner.save_version(
    name="customer_service",
    system_prompt="You are a friendly and empathetic customer service representative.",
    user_prompt="I understand your concern. Let me help you with: {customer_issue}",
    bump_type=VersionBump.MINOR,
    metadata={"type": "test", "tone": "empathetic", "experiment": "tone_test"}
)
```

### Test Design Principles

#### 1. **Single Variable Testing**
Test only one variable at a time to isolate the effect:

```python
# Good: Testing only tone difference
baseline_system = "You are a customer service representative."
test_system = "You are a friendly and empathetic customer service representative."

# User prompt stays the same to isolate the system prompt change
user_prompt = "Help the customer with: {customer_issue}"

# Avoid: Testing multiple variables simultaneously
# bad_test = "You are a friendly, empathetic, and highly knowledgeable customer service expert."
```

#### 2. **Proper Test Setup**
Ensure controlled testing environment:

```python
# Create A/B test instance
ab_test = ABTest(
    versioner=versioner,
    prompt_name="customer_service",
    version_a="1.0.0",  # Baseline version
    version_b="1.1.0",  # Test version
    metric_name="quality_score"
)

print(f"A/B test created for prompt: {ab_test.prompt_name}")
print(f"Comparing versions: {ab_test.version_a} vs {ab_test.version_b}")
print(f"Primary metric: {ab_test.metric_name}")
```

## 🎯 Setting Up A/B Tests

### Simple A/B Test

```python
from prompt_versioner import PromptVersioner, VersionBump
from prompt_versioner.testing import ABTest
import random

# Initialize
versioner = PromptVersioner(project_name="customer-service-ab-test")

# Create baseline version
versioner.save_version(
    name="support_assistant",
    system_prompt="You are a professional customer support assistant.",
    user_prompt="Please assist with this customer issue: {issue}",
    bump_type=VersionBump.MAJOR,
    metadata={"test_group": "control", "description": "Professional tone"}
)

# Create test version
versioner.save_version(
    name="support_assistant",
    system_prompt="You are a warm and understanding customer support assistant who genuinely cares about helping customers.",
    user_prompt="I'm here to help you with: {issue}. Let's work together to resolve this.",
    bump_type=VersionBump.MINOR,
    metadata={"test_group": "treatment", "description": "Empathetic tone"}
)

# Create improved version
improved_version = versioner.create_version(
    prompt_id=prompt_id,
    content="You are a friendly and empathetic customer service representative. I'm here to help you with: {customer_issue}",
    bump_type="minor",
    description="Added empathy and friendliness"
)

# Set up A/B test to compare the versions
ab_test = ABTest(
    versioner=versioner,
    prompt_name="support_assistant",
    version_a="1.0.0",  # Control (professional)
    version_b="1.1.0",  # Treatment (empathetic)
    metric_name="quality_score"
)

print(f"A/B test created for: {ab_test.prompt_name}")
print(f"Testing {ab_test.version_a} vs {ab_test.version_b}")

# Simulate A/B test with sample data
print("\n🧪 Running A/B Test simulation...")

# Log results for version A (control)
for i in range(25):
    quality_score = random.uniform(0.70, 0.85)  # Professional tone baseline
    ab_test.log_result("a", quality_score)

# Log results for version B (treatment)
for i in range(25):
    quality_score = random.uniform(0.75, 0.90)  # Empathetic tone improvement
    ab_test.log_result("b", quality_score)

# Check test status
sample_a, sample_b = ab_test.get_sample_counts()
print(f"📊 Samples collected: Version A = {sample_a}, Version B = {sample_b}")

# Analyze results
if ab_test.is_ready(min_samples=20):
    print("✅ Test has enough samples for analysis")

    result = ab_test.get_result()
    print(f"\n=== A/B Test Results ===")
    print(f"🏆 Winner: Version {result.winner}")
    print(f"📈 Improvement: {result.improvement:.2f}%")
    print(f"🎯 Confidence: {result.confidence:.1%}")

    # Print detailed results
    ab_test.print_result()
else:
    print("⚠️  Need more samples for reliable results")
```

### Production Integration Pattern

```python
def production_ab_test_workflow():
    """Example of how to integrate A/B testing in production"""

    # Create versions for testing
    versioner = PromptVersioner(project_name="production-app")

    # Control version (current production)
    versioner.save_version(
        name="email_responder",
        system_prompt="You are a professional email assistant.",
        user_prompt="Please draft a response to: {email_content}",
        bump_type=VersionBump.MAJOR,
        metadata={"deployment": "production", "test_group": "control"}
    )

    # Test version (new approach)
    versioner.save_version(
        name="email_responder",
        system_prompt="You are a helpful and personable email assistant.",
        user_prompt="Please draft a thoughtful response to: {email_content}",
        bump_type=VersionBump.MINOR,
        metadata={"deployment": "testing", "test_group": "treatment"}
    )

    # Set up A/B test
    ab_test = ABTest(
        versioner=versioner,
        prompt_name="email_responder",
        version_a="1.0.0",
        version_b="1.1.0",
        metric_name="quality_score"
    )

    return ab_test

def handle_email_request(user_id, email_content, ab_test):
    """Handle email request with A/B testing"""

    # Determine which version to use (simple hash-based assignment)
    use_version_b = hash(user_id) % 2 == 1
    version = "1.1.0" if use_version_b else "1.0.0"
    variant = "b" if use_version_b else "a"

    # Get prompt version
    prompt_data = ab_test.versioner.get_version("email_responder", version)

    # Render prompt (simple formatting)
    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data["user_prompt"].format(email_content=email_content)

    # Simulate LLM call and quality assessment
    response = f"[Generated response using {version}]"
    quality_score = random.uniform(0.7, 0.9)

    # Log the result for A/B test analysis
    ab_test.log_result(variant, quality_score)

    # Also log to versioner metrics
    ab_test.versioner.log_metrics(
        name="email_responder",
        version=version,
        model_name="gpt-4o",
        quality_score=quality_score,
        success=True,
        metadata={
            "user_id": user_id,
            "ab_test_variant": variant,
            "email_type": "customer_response"
        }
    )

    return response

# Usage example
ab_test = production_ab_test_workflow()

# Simulate production requests
for i in range(50):
    user_id = f"user_{i}"
    email_content = f"Sample email content {i}"
    response = handle_email_request(user_id, email_content, ab_test)

# Check results
if ab_test.is_ready(min_samples=20):
    result = ab_test.get_result()
    print(f"A/B Test Results: {result.winner} wins with {result.improvement:.1f}% improvement")
```

### Real-world LLM Integration

```python
import openai

def llm_ab_test_example():
    """Example with real LLM calls"""

    versioner = PromptVersioner(project_name="llm-ab-test")
    client = openai.OpenAI()

    # Create prompt versions
    versioner.save_version(
        name="code_reviewer",
        system_prompt="You are a code reviewer.",
        user_prompt="Review this code: {code}",
        bump_type=VersionBump.MAJOR
    )

    versioner.save_version(
        name="code_reviewer",
        system_prompt="You are an expert code reviewer with years of experience.",
        user_prompt="Please provide a detailed review of this code: {code}",
        bump_type=VersionBump.MINOR
    )

    # Set up A/B test
    ab_test = ABTest(
        versioner=versioner,
        prompt_name="code_reviewer",
        version_a="1.0.0",
        version_b="1.1.0",
        metric_name="quality_score"
    )

    # Test with real code samples
    test_code_samples = [
        "def hello(): print('world')",
        "class User: pass",
        "for i in range(10): print(i)"
    ]

    for code_sample in test_code_samples:
        for version, variant in [("1.0.0", "a"), ("1.1.0", "b")]:
            try:
                # Get prompt
                prompt_data = versioner.get_version("code_reviewer", version)

                # Make LLM call
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Use cheaper model for testing
                    messages=[
                        {"role": "system", "content": prompt_data["system_prompt"]},
                        {"role": "user", "content": prompt_data["user_prompt"].format(code=code_sample)}
                    ],
                    max_tokens=100
                )

                # Simple quality assessment
                response_text = response.choices[0].message.content
                quality_score = len(response_text) / 200.0  # Simple length-based quality
                quality_score = min(quality_score, 1.0)

                # Log result
                ab_test.log_result(variant, quality_score)

                # Log to versioner
                versioner.log_metrics(
                    name="code_reviewer",
                    version=version,
                    model_name="gpt-4o-mini",
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    quality_score=quality_score,
                    success=True
                )

            except Exception as e:
                print(f"Error with version {version}: {e}")
                ab_test.log_result(variant, 0.0)  # Log failure

    # Analyze results
    if ab_test.is_ready(min_samples=3):
        result = ab_test.get_result()
        ab_test.print_result()
        return result

    return None

# Run the example (commented out to avoid API calls)
# result = llm_ab_test_example()

        # Get variant assignment
        variant = self.test.get_variant(user_id)

        # Track assignment
        self.test.track_assignment(
            user_id=user_id,
            variant=variant["name"],
            context=context
        )

        return variant

    def track_outcome(self, user_id, outcome_metrics):
        """Track outcome metrics for the user"""
        variant = self.test.get_user_variant(user_id)

        if variant:
            self.test.track_outcome(
                user_id=user_id,
                variant=variant,
                metrics=outcome_metrics
            )

    def is_user_eligible(self, user_id, context):
        """Determine if user is eligible for testing"""
        # Implement eligibility logic
        # e.g., exclude internal users, new users, etc.

        eligibility_criteria = {
            "min_account_age_days": 30,
            "exclude_internal_users": True,
            "include_premium_users": True,
            "geographic_restrictions": ["US", "CA", "UK"]
        }

        # Check criteria against user context
        return self.check_eligibility(user_id, context, eligibility_criteria)

# Usage in production
tester = ProductionABTester(versioner, test_id)

def handle_customer_request(user_id, customer_issue):
    """Production handler with A/B testing"""

    # Get appropriate prompt variant
    variant = tester.get_prompt_for_user(
        user_id=user_id,
        context={"issue_type": classify_issue(customer_issue)}
    )

    # Render prompt
    rendered_prompt = versioner.render_prompt(
        prompt_id=variant["prompt_id"],
        version=variant["version"],
        variables={"customer_issue": customer_issue}
    )

    # Make LLM call
    response = call_llm(rendered_prompt)

    # Track outcome metrics
    tester.track_outcome(
        user_id=user_id,
        outcome_metrics={
            "quality_score": assess_quality(response),
            "latency": response.latency,
            "cost": response.cost,
            "user_satisfaction": get_user_feedback(user_id, response)
        }
    )

    return response.text
```

## 📊 Statistical Analysis

### Real-time Results Monitoring

```python
# Monitor test results in real-time
def monitor_test_progress(test_id, check_interval=3600):
    """Monitor A/B test progress and provide updates"""

    test = ABTest.load(test_id)

    while test.is_running():
        # Get current results
        results = test.get_intermediate_results()

        print(f"\n=== Test Progress Update ===")
        print(f"Test: {test.name}")
        print(f"Running time: {results['runtime_hours']:.1f} hours")
        print(f"Total samples: {results['total_samples']}")

        # Show results for each variant
        for variant_name, variant_results in results['variants'].items():
            print(f"\n{variant_name.title()} Variant:")
            print(f"  Samples: {variant_results['sample_size']}")
            print(f"  Conversion Rate: {variant_results['conversion_rate']:.3f}")
            print(f"  Quality Score: {variant_results['avg_quality']:.3f}")
            print(f"  Latency: {variant_results['avg_latency']:.2f}s")
            print(f"  Cost: ${variant_results['avg_cost']:.4f}")

        # Statistical significance check
        if results['has_enough_samples']:
            significance = test.calculate_significance()

            print(f"\n=== Statistical Analysis ===")
            print(f"Statistical Power: {significance['power']:.2f}")
            print(f"P-value: {significance['p_value']:.4f}")
            print(f"Confidence Interval: [{significance['ci_lower']:.3f}, {significance['ci_upper']:.3f}]")

            if significance['is_significant']:
                winner = significance['winning_variant']
                improvement = significance['improvement_percentage']
                print(f"🎉 Significant result! {winner} wins with {improvement:.1f}% improvement")

                # Check if we should stop the test early
                if test.should_stop_early():
                    print("Stopping test early due to significant results")
                    test.stop()
                    break
            else:
                print("No significant difference detected yet")

                # Estimate time to significance
                eta = test.estimate_time_to_significance()
                if eta:
                    print(f"Estimated time to significance: {eta:.1f} hours")
        else:
            needed_samples = test.calculate_required_samples()
            print(f"Need {needed_samples - results['total_samples']} more samples")

        # Wait before next check
        time.sleep(check_interval)

# Start monitoring
monitor_test_progress(test_id, check_interval=1800)  # Check every 30 minutes
```

### Statistical Significance Testing

```python
# Advanced statistical analysis
import scipy.stats as stats
from statsmodels.stats.power import ttest_power
from statsmodels.stats.proportion import proportions_ztest

class StatisticalAnalyzer:
    def __init__(self, confidence_level=0.95, power=0.8):
        self.confidence_level = confidence_level
        self.power = power
        self.alpha = 1 - confidence_level

    def calculate_sample_size(self, baseline_rate, minimum_detectable_effect):
        """Calculate required sample size for test"""

        # Convert to effect size
        effect_size = minimum_detectable_effect / np.sqrt(baseline_rate * (1 - baseline_rate))

        # Calculate required sample size
        sample_size = ttest_power(
            effect_size=effect_size,
            power=self.power,
            alpha=self.alpha,
            alternative='two-sided'
        )

        return int(np.ceil(sample_size))

    def analyze_results(self, control_data, treatment_data, metric="conversion_rate"):
        """Perform comprehensive statistical analysis"""

        results = {
            "metric": metric,
            "control": self._analyze_variant(control_data),
            "treatment": self._analyze_variant(treatment_data)
        }

        # Perform significance test based on metric type
        if metric in ["conversion_rate", "success_rate"]:
            significance = self._test_proportions(control_data, treatment_data)
        else:
            significance = self._test_means(control_data, treatment_data, metric)

        results["significance"] = significance

        # Calculate practical significance
        practical_significance = self._assess_practical_significance(
            control_mean=results["control"]["mean"],
            treatment_mean=results["treatment"]["mean"],
            metric=metric
        )

        results["practical_significance"] = practical_significance

        # Generate recommendation
        recommendation = self._generate_recommendation(significance, practical_significance)
        results["recommendation"] = recommendation

        return results

    def _analyze_variant(self, data):
        """Analyze individual variant data"""
        return {
            "sample_size": len(data),
            "mean": np.mean(data),
            "std": np.std(data),
            "median": np.median(data),
            "confidence_interval": self._calculate_confidence_interval(data)
        }

    def _test_proportions(self, control_data, treatment_data):
        """Test difference in proportions (e.g., conversion rates)"""

        control_successes = np.sum(control_data)
        control_total = len(control_data)
        treatment_successes = np.sum(treatment_data)
        treatment_total = len(treatment_data)

        # Perform z-test for proportions
        z_stat, p_value = proportions_ztest(
            [control_successes, treatment_successes],
            [control_total, treatment_total]
        )

        # Calculate effect size (difference in proportions)
        control_rate = control_successes / control_total
        treatment_rate = treatment_successes / treatment_total
        effect_size = treatment_rate - control_rate

        return {
            "test_type": "proportions_z_test",
            "z_statistic": z_stat,
            "p_value": p_value,
            "is_significant": p_value < self.alpha,
            "effect_size": effect_size,
            "control_rate": control_rate,
            "treatment_rate": treatment_rate,
            "relative_improvement": (effect_size / control_rate) * 100 if control_rate > 0 else 0
        }

    def _test_means(self, control_data, treatment_data, metric):
        """Test difference in means (e.g., quality scores, latency)"""

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(treatment_data, control_data)

        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(control_data) - 1) * np.var(control_data) +
                             (len(treatment_data) - 1) * np.var(treatment_data)) /
                            (len(control_data) + len(treatment_data) - 2))
        cohens_d = (np.mean(treatment_data) - np.mean(control_data)) / pooled_std

        return {
            "test_type": "independent_t_test",
            "t_statistic": t_stat,
            "p_value": p_value,
            "is_significant": p_value < self.alpha,
            "cohens_d": cohens_d,
            "control_mean": np.mean(control_data),
            "treatment_mean": np.mean(treatment_data),
            "absolute_difference": np.mean(treatment_data) - np.mean(control_data),
            "relative_improvement": ((np.mean(treatment_data) - np.mean(control_data)) /
                                   np.mean(control_data)) * 100 if np.mean(control_data) > 0 else 0
        }

# Usage
analyzer = StatisticalAnalyzer(confidence_level=0.95, power=0.8)

# Get test data
test_results = test.get_detailed_results()
control_quality = test_results['control']['quality_scores']
treatment_quality = test_results['treatment']['quality_scores']

# Analyze results
analysis = analyzer.analyze_results(
    control_data=control_quality,
    treatment_data=treatment_quality,
    metric="quality_score"
)

print(f"Statistical Analysis Results:")
print(f"P-value: {analysis['significance']['p_value']:.4f}")
print(f"Is Significant: {analysis['significance']['is_significant']}")
print(f"Effect Size (Cohen's d): {analysis['significance']['cohens_d']:.3f}")
print(f"Relative Improvement: {analysis['significance']['relative_improvement']:.1f}%")
print(f"Recommendation: {analysis['recommendation']}")
```

## 🎯 Advanced Testing Strategies

### Sequential Testing

```python
# Sequential A/B testing for faster results
class SequentialABTest(ABTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sequential_bounds = self.calculate_sequential_bounds()

    def calculate_sequential_bounds(self):
        """Calculate bounds for sequential testing"""
        # Implement sequential probability ratio test (SPRT) bounds
        alpha = 1 - self.confidence_level
        beta = 1 - self.statistical_power

        upper_bound = np.log((1 - beta) / alpha)
        lower_bound = np.log(beta / (1 - alpha))

        return {"upper": upper_bound, "lower": lower_bound}

    def should_stop_test(self):
        """Check if test should stop based on sequential analysis"""
        results = self.get_current_results()

        # Calculate log-likelihood ratio
        llr = self.calculate_log_likelihood_ratio(results)

        if llr >= self.sequential_bounds["upper"]:
            return True, "treatment_wins"
        elif llr <= self.sequential_bounds["lower"]:
            return True, "control_wins"
        else:
            return False, "continue"

# Bayesian A/B Testing
class BayesianABTest(ABTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prior_alpha = kwargs.get('prior_alpha', 1)
        self.prior_beta = kwargs.get('prior_beta', 1)

    def calculate_probability_of_superiority(self):
        """Calculate probability that treatment is better than control"""

        results = self.get_current_results()

        # Update posterior distributions
        control_alpha = self.prior_alpha + results['control']['successes']
        control_beta = self.prior_beta + results['control']['failures']

        treatment_alpha = self.prior_alpha + results['treatment']['successes']
        treatment_beta = self.prior_beta + results['treatment']['failures']

        # Monte Carlo simulation to calculate P(treatment > control)
        n_simulations = 10000
        control_samples = np.random.beta(control_alpha, control_beta, n_simulations)
        treatment_samples = np.random.beta(treatment_alpha, treatment_beta, n_simulations)

        probability_treatment_wins = np.mean(treatment_samples > control_samples)

        return {
            "probability_treatment_wins": probability_treatment_wins,
            "probability_control_wins": 1 - probability_treatment_wins,
            "expected_loss": self.calculate_expected_loss(
                control_samples, treatment_samples
            )
        }

    def should_stop_test(self, threshold=0.95):
        """Stop test when probability exceeds threshold"""
        prob_results = self.calculate_probability_of_superiority()

        if (prob_results["probability_treatment_wins"] > threshold or
            prob_results["probability_control_wins"] > threshold):
            return True

        return False
```

### Multi-Armed Bandit Testing

```python
# Multi-armed bandit for dynamic allocation
class MultiArmedBanditTest:
    def __init__(self, variants, exploration_rate=0.1):
        self.variants = variants
        self.exploration_rate = exploration_rate
        self.arm_stats = {
            variant: {"pulls": 0, "rewards": 0, "avg_reward": 0}
            for variant in variants
        }

    def select_variant(self):
        """Select variant using epsilon-greedy strategy"""

        if np.random.random() < self.exploration_rate:
            # Explore: random selection
            return np.random.choice(self.variants)
        else:
            # Exploit: select best performing variant
            best_variant = max(
                self.variants,
                key=lambda v: self.arm_stats[v]["avg_reward"]
            )
            return best_variant

    def update_reward(self, variant, reward):
        """Update variant performance with new reward"""
        stats = self.arm_stats[variant]
        stats["pulls"] += 1
        stats["rewards"] += reward
        stats["avg_reward"] = stats["rewards"] / stats["pulls"]

    def get_performance_summary(self):
        """Get current performance summary"""
        return {
            variant: {
                "pulls": stats["pulls"],
                "avg_reward": stats["avg_reward"],
                "confidence": self.calculate_confidence(stats)
            }
            for variant, stats in self.arm_stats.items()
        }

# Thompson Sampling for more sophisticated bandit
class ThompsonSamplingBandit:
    def __init__(self, variants):
        self.variants = variants
        # Beta distribution parameters for each variant
        self.alpha = {variant: 1 for variant in variants}
        self.beta = {variant: 1 for variant in variants}

    def select_variant(self):
        """Select variant using Thompson sampling"""
        samples = {
            variant: np.random.beta(self.alpha[variant], self.beta[variant])
            for variant in self.variants
        }

        return max(samples, key=samples.get)

    def update(self, variant, success):
        """Update parameters based on outcome"""
        if success:
            self.alpha[variant] += 1
        else:
            self.beta[variant] += 1
```

## 📋 Test Management and Operations

### Test Lifecycle Management

```python
# Complete test lifecycle management
class TestManager:
    def __init__(self, versioner):
        self.versioner = versioner
        self.active_tests = {}
        self.test_history = []

    def create_test_plan(self, test_spec):
        """Create comprehensive test plan"""

        plan = {
            "test_id": generate_test_id(),
            "name": test_spec["name"],
            "objective": test_spec["objective"],
            "hypothesis": test_spec["hypothesis"],

            # Test parameters
            "variants": test_spec["variants"],
            "traffic_allocation": test_spec["traffic_allocation"],
            "duration_estimate": self.estimate_duration(test_spec),
            "sample_size_required": self.calculate_sample_size(test_spec),

            # Success criteria
            "primary_metric": test_spec["primary_metric"],
            "secondary_metrics": test_spec.get("secondary_metrics", []),
            "minimum_detectable_effect": test_spec["minimum_detectable_effect"],

            # Risk assessment
            "risk_level": self.assess_risk(test_spec),
            "rollback_plan": test_spec.get("rollback_plan"),

            # Approvals
            "requires_approval": test_spec.get("requires_approval", True),
            "approved_by": None,
            "approval_date": None,

            # Status
            "status": "planning",
            "created_at": datetime.now(),
            "created_by": test_spec["created_by"]
        }

        return plan

    def submit_for_approval(self, test_plan, approvers):
        """Submit test plan for approval"""

        approval_request = {
            "test_plan": test_plan,
            "approvers": approvers,
            "submitted_at": datetime.now(),
            "status": "pending_approval"
        }

        # Send approval notifications
        self.send_approval_notifications(approval_request)

        return approval_request

    def approve_test(self, test_id, approver, comments=None):
        """Approve test for execution"""

        test_plan = self.get_test_plan(test_id)
        test_plan["approved_by"] = approver
        test_plan["approval_date"] = datetime.now()
        test_plan["approval_comments"] = comments
        test_plan["status"] = "approved"

        # Update test plan
        self.update_test_plan(test_plan)

        return test_plan

    def start_test_execution(self, test_id):
        """Start test execution with safety checks"""

        test_plan = self.get_test_plan(test_id)

        # Pre-flight checks
        safety_checks = self.run_safety_checks(test_plan)

        if not safety_checks["all_passed"]:
            raise TestExecutionError(
                f"Safety checks failed: {safety_checks['failures']}"
            )

        # Initialize test
        test = ABTest.from_plan(test_plan)
        test_id = test.start()

        # Track active test
        self.active_tests[test_id] = {
            "test": test,
            "start_time": datetime.now(),
            "monitoring_enabled": True
        }

        # Start monitoring
        self.start_test_monitoring(test_id)

        return test_id

    def run_safety_checks(self, test_plan):
        """Run comprehensive safety checks before starting test"""

        checks = []

        # Check 1: Traffic allocation
        total_traffic = sum(test_plan["traffic_allocation"].values())
        checks.append({
            "name": "traffic_allocation",
            "passed": total_traffic == 100,
            "message": f"Traffic allocation sums to {total_traffic}%"
        })

        # Check 2: Variant validation
        for variant in test_plan["variants"]:
            prompt_exists = self.versioner.prompt_exists(
                variant["prompt_id"],
                variant["version"]
            )
            checks.append({
                "name": f"variant_{variant['name']}_exists",
                "passed": prompt_exists,
                "message": f"Variant {variant['name']} prompt exists"
            })

        # Check 3: Metric availability
        metrics_available = self.check_metrics_availability(
            test_plan["primary_metric"],
            test_plan["secondary_metrics"]
        )
        checks.append({
            "name": "metrics_available",
            "passed": metrics_available,
            "message": "All required metrics are available"
        })

        # Check 4: No conflicting tests
        conflicts = self.check_test_conflicts(test_plan)
        checks.append({
            "name": "no_conflicts",
            "passed": len(conflicts) == 0,
            "message": f"Found {len(conflicts)} conflicting tests"
        })

        all_passed = all(check["passed"] for check in checks)
        failures = [check["message"] for check in checks if not check["passed"]]

        return {
            "all_passed": all_passed,
            "checks": checks,
            "failures": failures
        }

# Usage
test_manager = TestManager(versioner)

# Create test specification
test_spec = {
    "name": "Customer Service Empathy Test",
    "objective": "Improve customer satisfaction through empathetic language",
    "hypothesis": "Adding empathetic language will increase quality scores by 5%",
    "variants": [
        {
            "name": "control",
            "prompt_id": "cs-prompt-001",
            "version": "2.0.0",
            "description": "Current standard prompt"
        },
        {
            "name": "empathetic",
            "prompt_id": "cs-prompt-001",
            "version": "2.1.0",
            "description": "Enhanced with empathetic language"
        }
    ],
    "traffic_allocation": {"control": 50, "empathetic": 50},
    "primary_metric": "quality_score",
    "secondary_metrics": ["latency", "user_satisfaction"],
    "minimum_detectable_effect": 0.05,
    "created_by": "product_manager@company.com"
}

# Create test plan
test_plan = test_manager.create_test_plan(test_spec)

# Submit for approval
approval_request = test_manager.submit_for_approval(
    test_plan,
    approvers=["team_lead@company.com", "data_scientist@company.com"]
)

# Approve test (after review)
approved_plan = test_manager.approve_test(
    test_plan["test_id"],
    approver="team_lead@company.com",
    comments="Looks good, approved to run for 2 weeks"
)

# Start test execution
test_id = test_manager.start_test_execution(test_plan["test_id"])
print(f"Test {test_id} started successfully!")
```

## 🏆 Best Practices and Guidelines

### Test Design Best Practices

1. **Clear Hypothesis**: Always start with a specific, testable hypothesis
2. **Single Variable**: Test only one change at a time
3. **Sufficient Sample Size**: Calculate and ensure adequate sample size
4. **Representative Sample**: Ensure test traffic represents your user base
5. **Proper Randomization**: Use proper randomization to avoid bias

### Statistical Best Practices

1. **Pre-define Metrics**: Decide on success metrics before starting
2. **Multiple Testing Correction**: Account for multiple comparisons
3. **Power Analysis**: Ensure sufficient statistical power
4. **Effect Size**: Focus on practical significance, not just statistical
5. **Proper Duration**: Run tests long enough to account for variations

### Operational Best Practices

1. **Monitoring**: Continuously monitor test health and performance
2. **Documentation**: Document all decisions and learnings
3. **Rollback Plan**: Always have a rollback strategy
4. **Stakeholder Communication**: Keep stakeholders informed of progress
5. **Post-Test Analysis**: Conduct thorough post-test analysis

A/B testing is a powerful tool for optimizing prompts systematically. By following statistical best practices and maintaining rigorous testing standards, you can make data-driven decisions that lead to meaningful improvements in prompt performance.

## 📚 Related Topics

- [Metrics & Tracking](metrics-tracking.md) - Understanding what to measure
- [Performance Monitoring](performance-monitoring.md) - Monitoring test health
- [Version Management](version-management.md) - Managing test variants
- [Web Dashboard](web-dashboard.md) - Visual test management interface
