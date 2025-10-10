"""Run the web dashboard."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_versioner.core import PromptVersioner
from prompt_versioner.app import create_app


def main():
    print("=" * 80)
    print("Starting Prompt Versioner Dashboard")
    print("=" * 80)

    # Initialize versioner
    pv = PromptVersioner(project_name="dashboard-app", enable_git=False)

    # Create some sample data if database is empty
    prompts = pv.list_prompts()
    if not prompts:
        print("\n📝 Creating sample data...")

        # Sample prompt 1
        pv.save_version(
            name="code_reviewer",
            system_prompt="You are an expert code reviewer. Analyze code for quality, bugs, and improvements.",
            user_prompt="Review this code:\n{code}",
            metadata={"type": "code", "model": "gpt-4"},
        )

        # Sample prompt 2
        pv.save_version(
            name="summarizer",
            system_prompt="You are a skilled summarization assistant. Create concise, accurate summaries.",
            user_prompt="Summarize the following:\n{text}",
            metadata={"type": "summarization"},
        )

        # Add some versions
        pv.save_version(
            name="code_reviewer",
            system_prompt="You are an EXPERT code reviewer. Analyze code for quality, security, bugs, and performance improvements.",
            user_prompt="Review this code:\n{code}\n\nProvide detailed feedback.",
            metadata={"type": "code", "model": "claude-sonnet-4", "version": "improved"},
        )

        print("✅ Sample data created!")

    # Create and run app
    app = create_app(pv)

    port = 5000
    print(f"\nDashboard running at: http://localhost:{port}")
    print(f"Database: {pv.storage.db_path}")
    print(f"Tracked prompts: {len(pv.list_prompts())}")
    print("\nPress Ctrl+C to stop\n")
    print("=" * 80)

    app.run(host="localhost", port=port, debug=True)


if __name__ == "__main__":
    main()
