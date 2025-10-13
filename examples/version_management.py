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
    f"Retrieved version: {version_1_0['version']} with prompt, User Prompt:\n{version_1_0['user_prompt']}"
)
