# Advanced Workflows

Explore advanced patterns and workflows with **Prompt Versioner** for complex use cases.

## 🚀 Automated Version Management

### Continuous Integration Pipeline

```python
from prompt_versioner import PromptVersioner, VersionBump
import os

def ci_pipeline_versioning():
    """Automated versioning in CI/CD pipeline"""

    pv = PromptVersioner(project_name="production-ai", enable_git=True)

    # Get current branch and commit info
    branch = os.getenv("CI_BRANCH", "main")
    commit_hash = os.getenv("CI_COMMIT_SHA", "unknown")

    # Automatic version bump based on branch
    if branch == "main":
        bump_type = VersionBump.PATCH
    elif branch.startswith("feature/"):
        bump_type = VersionBump.MINOR
    elif branch.startswith("breaking/"):
        bump_type = VersionBump.MAJOR
    else:
        bump_type = VersionBump.PATCH

    # Create version with CI context
    version_id = pv.save_version(
        name="production_assistant",
        system_prompt=load_prompt_from_file("prompts/system.txt"),
        user_prompt=load_prompt_from_file("prompts/user.txt"),
        bump_type=bump_type,
        metadata={
            "ci_build": True,
            "branch": branch,
            "commit": commit_hash,
            "pipeline_id": os.getenv("CI_PIPELINE_ID"),
            "automated": True
        }
    )

    print(f"✅ CI: Created version {version_id} for branch {branch}")
    return version_id

def load_prompt_from_file(filepath):
    """Load prompt content from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

# Run in CI
if os.getenv("CI"):
    ci_pipeline_versioning()
```

### Auto-versioning with Decorators

```python
from functools import wraps
import hashlib

def auto_version(prompt_name, check_changes=True):
    """Decorator for automatic versioning when prompt logic changes"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function to get prompts
            result = func(*args, **kwargs)

            # Extract prompts
            if isinstance(result, dict):
                system_prompt = result.get("system", "")
                user_prompt = result.get("user", "")
            else:
                return result

            # Check if prompts changed (optional optimization)
            if check_changes:
                content_hash = hashlib.md5(
                    (system_prompt + user_prompt).encode()
                ).hexdigest()

                latest = pv.get_latest(prompt_name)
                if latest and latest.get("content_hash") == content_hash:
                    return result  # No changes, skip versioning

            # Auto-version the prompts
            pv.save_version(
                name=prompt_name,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                bump_type=VersionBump.PATCH,
                metadata={
                    "auto_generated": True,
                    "function": func.__name__,
                    "content_hash": content_hash
                }
            )

            return result

        return wrapper
    return decorator

# Usage
@auto_version("dynamic_assistant")
def create_context_aware_prompt(user_type, domain):
    """Create prompts based on context"""

    system_prompt = f"You are an AI assistant specialized in {domain} for {user_type} users."
    user_prompt = f"Help with {domain}-related questions. User type: {user_type}. Question: {{question}}"

    return {
        "system": system_prompt,
        "user": user_prompt
    }

# This will auto-version when called with different parameters
create_context_aware_prompt("developer", "software engineering")
create_context_aware_prompt("designer", "user experience")
```

## 🧪 Advanced Testing Patterns

### Multi-Environment Testing

```python
class MultiEnvironmentTester:
    """Test prompts across multiple environments"""

    def __init__(self, environments):
        self.environments = environments
        self.results = {}

    def test_across_environments(self, prompt_name, version, test_cases):
        """Test same prompt version across different environments"""

        for env_name, env_config in self.environments.items():
            print(f"🧪 Testing in {env_name} environment...")

            # Initialize versioner for this environment
            pv = PromptVersioner(
                project_name=f"{prompt_name}_{env_name}",
                db_path=env_config["db_path"]
            )

            env_results = []

            for test_case in test_cases:
                with pv.test_version(prompt_name, version) as test:
                    # Simulate LLM call with environment-specific settings
                    result = self.simulate_llm_call(
                        test_case,
                        env_config
                    )

                    test.log(
                        tokens=result["tokens"],
                        cost=result["cost"],
                        latency_ms=result["latency"],
                        quality_score=result["quality"],
                        metadata={
                            "environment": env_name,
                            "test_case": test_case["name"]
                        }
                    )

                    env_results.append(result)

            self.results[env_name] = env_results

        return self.generate_comparison_report()

    def simulate_llm_call(self, test_case, env_config):
        """Simulate LLM call with environment-specific behavior"""
        import random

        # Simulate different performance based on environment
        base_latency = env_config.get("base_latency", 300)
        base_quality = env_config.get("base_quality", 0.85)

        return {
            "tokens": random.randint(100, 300),
            "cost": random.uniform(0.001, 0.005),
            "latency": base_latency + random.uniform(-50, 100),
            "quality": base_quality + random.uniform(-0.1, 0.1),
            "success": random.random() > 0.05  # 95% success rate
        }

    def generate_comparison_report(self):
        """Generate comparison report across environments"""

        report = {"summary": {}, "details": self.results}

        for env_name, results in self.results.items():
            avg_quality = sum(r["quality"] for r in results) / len(results)
            avg_latency = sum(r["latency"] for r in results) / len(results)
            avg_cost = sum(r["cost"] for r in results) / len(results)

            report["summary"][env_name] = {
                "avg_quality": avg_quality,
                "avg_latency": avg_latency,
                "avg_cost": avg_cost,
                "total_tests": len(results)
            }

        return report

# Usage
environments = {
    "development": {
        "db_path": "dev_prompts.db",
        "base_latency": 200,
        "base_quality": 0.8
    },
    "staging": {
        "db_path": "staging_prompts.db",
        "base_latency": 350,
        "base_quality": 0.85
    },
    "production": {
        "db_path": "prod_prompts.db",
        "base_latency": 500,
        "base_quality": 0.9
    }
}

test_cases = [
    {"name": "simple_query", "input": "What is Python?"},
    {"name": "complex_query", "input": "Explain advanced Python decorators"},
    {"name": "edge_case", "input": "Handle this unusual scenario..."}
]

tester = MultiEnvironmentTester(environments)
report = tester.test_across_environments("code_assistant", "1.2.0", test_cases)

print("📊 Cross-Environment Test Results:")
for env, summary in report["summary"].items():
    print(f"{env}: Quality={summary['avg_quality']:.2f}, Latency={summary['avg_latency']:.0f}ms")
```

### A/B Testing with Statistical Significance

```python
import scipy.stats as stats
from prompt_versioner import ABTest

class StatisticalABTest(ABTest):
    """A/B test with proper statistical analysis"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = 0.05  # Significance level
        self.power = 0.8   # Statistical power

    def calculate_sample_size(self, baseline_rate, minimum_detectable_effect):
        """Calculate required sample size for statistical significance"""

        # Effect size (Cohen's d)
        effect_size = minimum_detectable_effect / baseline_rate

        # Sample size calculation (simplified)
        z_alpha = stats.norm.ppf(1 - self.alpha/2)
        z_beta = stats.norm.ppf(self.power)

        sample_size = ((z_alpha + z_beta) ** 2) * 2 / (effect_size ** 2)

        return int(sample_size)

    def analyze_results_statistical(self):
        """Perform statistical analysis of A/B test results"""

        if not self.is_ready(min_samples=30):
            return {"status": "insufficient_data"}

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(self.results_b, self.results_a)

        # Calculate effect size (Cohen's d)
        pooled_std = ((len(self.results_a) - 1) * stats.tstd(self.results_a) ** 2 +
                     (len(self.results_b) - 1) * stats.tstd(self.results_b) ** 2) / \
                     (len(self.results_a) + len(self.results_b) - 2)
        pooled_std = pooled_std ** 0.5

        cohens_d = (stats.tmean(self.results_b) - stats.tmean(self.results_a)) / pooled_std

        # Confidence interval
        confidence_interval = stats.t.interval(
            1 - self.alpha,
            len(self.results_a) + len(self.results_b) - 2,
            loc=stats.tmean(self.results_b) - stats.tmean(self.results_a),
            scale=pooled_std * (1/len(self.results_a) + 1/len(self.results_b)) ** 0.5
        )

        return {
            "status": "complete",
            "p_value": p_value,
            "is_significant": p_value < self.alpha,
            "effect_size": cohens_d,
            "confidence_interval": confidence_interval,
            "sample_size_a": len(self.results_a),
            "sample_size_b": len(self.results_b),
            "mean_a": stats.tmean(self.results_a),
            "mean_b": stats.tmean(self.results_b)
        }

    def print_statistical_report(self):
        """Print detailed statistical report"""

        analysis = self.analyze_results_statistical()

        if analysis["status"] == "insufficient_data":
            print("⚠️ Insufficient data for statistical analysis")
            return

        print("📊 STATISTICAL A/B TEST ANALYSIS")
        print("=" * 40)
        print(f"Version A ({self.version_a}): {analysis['sample_size_a']} samples, mean = {analysis['mean_a']:.3f}")
        print(f"Version B ({self.version_b}): {analysis['sample_size_b']} samples, mean = {analysis['mean_b']:.3f}")
        print()
        print(f"P-value: {analysis['p_value']:.4f}")
        print(f"Effect size (Cohen's d): {analysis['effect_size']:.3f}")
        print(f"95% CI: [{analysis['confidence_interval'][0]:.3f}, {analysis['confidence_interval'][1]:.3f}]")
        print()

        if analysis["is_significant"]:
            winner = "B" if analysis['mean_b'] > analysis['mean_a'] else "A"
            improvement = abs(analysis['mean_b'] - analysis['mean_a']) / analysis['mean_a'] * 100
            print(f"🎉 SIGNIFICANT RESULT: Version {winner} wins!")
            print(f"Improvement: {improvement:.1f}%")
        else:
            print("❌ No significant difference detected")

# Usage
statistical_test = StatisticalABTest(
    versioner=pv,
    prompt_name="customer_service",
    version_a="2.0.0",
    version_b="2.1.0"
)

# Calculate required sample size
required_samples = statistical_test.calculate_sample_size(
    baseline_rate=0.85,
    minimum_detectable_effect=0.05
)
print(f"Required samples per variant: {required_samples}")

# ... collect data ...

# Analyze with proper statistics
statistical_test.print_statistical_report()
```

## 📚 Next Steps

- [Integrations](integrations.md) - Learn about system integrations
- [Best Practices](best-practices.md) - Comprehensive best practices guide
- [Performance Monitoring](../user-guide/performance-monitoring.md) - Advanced monitoring techniques
