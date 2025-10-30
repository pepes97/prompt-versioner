import time
from prompt_versioner.core import PromptVersioner, VersionBump

print("🚀 Starting News Summarizer Example")
print("=" * 45)

# Initialize with your project
print("\n📝 Initializing PromptVersioner...")
pv = PromptVersioner("content-ai", enable_git=True)
print("✅ PromptVersioner initialized for project: content-ai")

# Create a summarization prompt
print("\n📋 Creating baseline news summarizer prompt...")
version_id = pv.save_version(
    name="news_summarizer",
    system_prompt="""You are a professional news summarizer. Create concise,
    accurate summaries that capture the key points and maintain journalistic objectivity.""",
    user_prompt="""Summarize this news article in 2-3 sentences:

Article: {article_text}

Summary:""",
    bump_type=VersionBump.MAJOR,
    metadata={"domain": "journalism", "target_length": "2-3 sentences", "style": "objective"},
)

baseline_version = pv.get_latest("news_summarizer")
print(f"✅ Created baseline version: {baseline_version['version']} (ID: {version_id})")
print(f"   System prompt length: {len(baseline_version['system_prompt'])} chars")
print(f"   User prompt length: {len(baseline_version['user_prompt'])} chars")


# Use in production with metrics tracking
def summarize_article(article_text: str) -> str:
    print(f"\n📰 Processing article ({len(article_text)} chars)...")
    prompt_data = pv.get_latest("news_summarizer")
    print(f"   Using prompt version: {prompt_data['version']}")

    # Format the prompt
    formatted_prompt = prompt_data["user_prompt"].format(article_text=article_text)
    print(f"   Formatted prompt length: {len(formatted_prompt)} chars")

    # Call your LLM (simulated - comment out for real API call)
    print("   ⏳ Calling LLM...")
    start_time = time.time()

    # Simulate API response
    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]
            self.usage = MockUsage()

    class MockChoice:
        def __init__(self):
            self.message = MockMessage()

    class MockMessage:
        def __init__(self):
            self.content = "This is a simulated summary of the article about breaking news. The key points are highlighted in this concise overview."

    class MockUsage:
        def __init__(self):
            self.prompt_tokens = len(formatted_prompt) // 4  # Rough estimation
            self.completion_tokens = 45

    response = MockResponse()

    # Uncomment for real OpenAI API call:
    # response = openai.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": prompt_data["system_prompt"]},
    #         {"role": "user", "content": formatted_prompt}
    #     ],
    #     temperature=0.7,
    #     max_tokens=200
    # )

    latency = (time.time() - start_time) * 1000
    print(f"   ✅ LLM response received in {latency:.1f}ms")
    print(
        f"   📊 Tokens - Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens}"
    )

    # Log metrics automatically
    print("   💾 Logging metrics...")
    pv.log_metrics(
        name="news_summarizer",
        version=prompt_data["version"],
        model_name="gpt-4o",
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        latency_ms=latency,
        success=True,
    )
    print("   ✅ Metrics logged successfully")

    summary = response.choices[0].message.content
    print(f"   📝 Generated summary: {summary[:100]}...")
    return summary


# Run A/B test on improvements
print("\n🔬 Creating enhanced version for A/B testing...")
enhanced_version_id = pv.save_version(
    name="news_summarizer",
    system_prompt="""You are a professional news summarizer with expertise in
    extracting key insights. Create engaging, concise summaries that highlight
    the most important developments.""",
    user_prompt="""Create a compelling summary of this news article:

Article: {article_text}

Key Points:
-""",
    bump_type=VersionBump.MINOR,  # Now version 1.1.0
    metadata={
        "domain": "journalism",
        "improvement": "more engaging format",
        "style": "key_points_format",
    },
)

enhanced_version = pv.get_latest("news_summarizer")
print(f"✅ Created enhanced version: {enhanced_version['version']} (ID: {enhanced_version_id})")
print(f"   System prompt length: {len(enhanced_version['system_prompt'])} chars")
print(f"   User prompt length: {len(enhanced_version['user_prompt'])} chars")

# Test with sample article
print("\n🧪 Testing with sample news articles...")
print("-" * 50)

sample_articles = [
    "Breaking: Scientists at MIT have developed a new quantum computing chip that could revolutionize data processing speeds by 1000x. The breakthrough uses novel superconducting materials to maintain quantum coherence at higher temperatures than previously possible.",
    "Election Update: Voter turnout reached historic highs in today's municipal elections, with preliminary results showing a tight race between incumbent Mayor Johnson and challenger Rodriguez. Key issues include housing affordability and public transportation funding.",
    "Tech News: Major social media platform announces significant changes to its privacy policy, affecting over 2 billion users worldwide. The updates include new data retention policies and enhanced user control over personal information sharing.",
]

for i, article in enumerate(sample_articles, 1):
    print(f"\n📖 Article {i}:")
    print(f"   Content: {article[:100]}...")

    summary = summarize_article(article)
    print(f"   Summary: {summary}")

print("\n📈 Checking stored metrics...")
all_prompts = pv.list_prompts()
print(f"Available prompts: {all_prompts}")

if "news_summarizer" in all_prompts:
    versions = pv.list_versions("news_summarizer")
    print(f"Versions for news_summarizer: {[v['version'] for v in versions]}")

    # Show version details
    for version in versions:
        metrics_count = len(pv.get_version("news_summarizer", version["version"]))
        print(f"   Version {version['version']}: {metrics_count} metrics logged")

print("\n🎉 Example completed successfully!")
print("=" * 45)
