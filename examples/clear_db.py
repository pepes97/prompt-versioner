"""Script to clear prompts from the database."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_versioner.core import PromptVersioner


def main():
    print("=" * 80)
    print("🗑️  Prompt Database Cleaner")
    print("=" * 80)

    pv = PromptVersioner(project_name="dashboard-app", enable_git=False)

    # Get all prompts
    prompts = pv.list_prompts()

    if not prompts:
        print("\n✨ Database is already empty!")
        return

    print(f"\n📊 Found {len(prompts)} prompt(s):")
    for prompt in prompts:
        versions = pv.list_versions(prompt)
        print(f"   - {prompt} ({len(versions)} versions)")

    # Ask for confirmation
    print("\n⚠️  This will delete ALL prompts and their versions!")
    response = input("Are you sure? Type 'yes' to confirm: ")

    if response.lower() != "yes":
        print("\n❌ Operation cancelled")
        return

    # Delete all prompts
    print("\n🗑️  Deleting prompts...")
    deleted_count = 0

    for prompt in prompts:
        versions = pv.list_versions(prompt)
        for version in versions:
            pv.storage.delete_version(prompt, version["version"])
            deleted_count += 1

    print(f"\n✅ Deleted {deleted_count} version(s) across {len(prompts)} prompt(s)")
    print("✨ Database is now empty!")
    print("=" * 80)


if __name__ == "__main__":
    main()
