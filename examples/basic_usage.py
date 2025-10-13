from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
pv = PromptVersioner(project_name="my-ai-project", enable_git=False)

# Save your first prompt version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer with deep knowledge of software engineering.",
    user_prompt="Review this code thoroughly:\n{code}\n\nProvide detailed feedback.",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={
        "type": "code_review",
        "author": "team",
        "model_target": "gpt-4o",
        "use_case": "pull_request_review",
    },
)

# Get the latest version
latest = pv.get_latest("code_reviewer")
print(f"✅ Latest version: {latest['version']}")

# Log metrics from your LLM calls
pv.log_metrics(
    name="code_reviewer",
    version=latest["version"],
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=250,
    latency_ms=450.5,
    quality_score=0.92,
    temperature=0.7,
    max_tokens=1000,
    success=True,
)

print("📊 Metrics logged successfully!")
