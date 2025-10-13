from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
pv = PromptVersioner(project_name="my-ai-project", enable_git=False)


# Create versions with semantic versioning
pv.save_version(
    name="summarizer",
    system_prompt="You are a skilled summarization assistant.",
    user_prompt="Summarize the following text:\n{text}",
    bump_type=VersionBump.MAJOR,  # MAJOR, MINOR, or PATCH
    metadata={"type": "summarization", "improvement": "better context"},
)

# List all versions
versions = pv.list_versions("summarizer")
for v in versions:
    print(f"Version {v['version']}: {v['timestamp']}")

# Get specific version
version_1_0 = pv.get_version("summarizer", "1.0.0")

print(
    f"✅ Retrieved version: {version_1_0['version']} with prompt, User Prompt:\n{version_1_0['user_prompt']}"
)


# Log comprehensive metrics
pv.log_metrics(
    name="summarizer",
    version="1.0.0",
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=75,
    latency_ms=420.5,
    quality_score=0.95,
    temperature=0.7,
    max_tokens=500,
    success=True,
    metadata={"user_feedback": "excellent", "domain": "tech_news"},
)

# Query metrics
v = pv.get_version("summarizer", "1.0.0")
metrics = pv.storage.get_metrics(version_id=v["id"], limit=100)
avg_quality = sum(m["quality_score"] for m in metrics) / len(metrics)
print(f"📊 Average quality score: {avg_quality:.2f}")
