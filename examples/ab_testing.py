from prompt_versioner import ABTest, PromptVersioner
import random

pv = PromptVersioner(project_name="my-ai-project", enable_git=False)

# Create an A/B test
ab_test = ABTest(
    versioner=pv,
    prompt_name="code_reviewer",  # Usa un prompt che esiste
    version_a="1.0.0",
    version_b="1.0.0",  # Per ora usa la stessa versione come esempio
    metric_name="quality_score",
)

# Simula alcuni risultati per il test
print("🧪 Running A/B Test simulation...")

# Log results for version A
for i in range(20):
    metric_value = random.uniform(0.75, 0.85)  # nosec B311 # Simulation only, not cryptographic
    ab_test.log_result("a", metric_value)

# Log results for version B
for i in range(20):
    metric_value = random.uniform(0.80, 0.90)  # nosec B311 # Simulation only, not cryptographic
    ab_test.log_result("b", metric_value)

# Check if test has enough data
sample_a, sample_b = ab_test.get_sample_counts()
print(f"📊 Samples collected: Version A = {sample_a}, Version B = {sample_b}")

# Check if ready for analysis
if ab_test.is_ready(min_samples=15):
    print("✅ Test has enough samples for analysis")

    # Get results
    result = ab_test.get_result()
    print(f"🏆 Winner: {result.winner}")
    print(f"📈 Improvement: {result.improvement:.2f}%")
    print(f"🎯 Confidence: {result.confidence:.1%}")

    # Print detailed results
    ab_test.print_result()
else:
    print("⚠️  Need more samples for reliable results")
