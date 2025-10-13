# Collaboration

Work effectively with your team using **Prompt Versioner**'s collaboration features.

## 👥 Quick Start

```python
from prompt_versioner import PromptVersioner

# Initialize for team use
pv = PromptVersioner(
    project_name="team-project",
    enable_git=True,  # Enable Git for team collaboration
)

# Add annotation for team communication
pv.add_annotation(
    name="customer_service",
    version="2.1.0",
    text="Updated for better sentiment handling. Ready for production.",
    author="alice@company.com"
)

# Export for sharing
from pathlib import Path
pv.export_prompt(
    name="customer_service",
    output_file=Path("customer_service_v2.1.0.json"),
    include_metrics=True
)
```

## 🤝 Team Workflows

### Version Control Integration

```python
# Work with Git branches
pv = PromptVersioner(project_name="team-ai", enable_git=True)

# Install Git hooks for automatic tracking
pv.install_git_hooks()

# Create version with Git context
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer for Python.",
    user_prompt="Review this Python code:\n{code}\n\nFocus on: {focus_areas}",
    bump_type=VersionBump.MINOR,
    metadata={
        "author": "dev-team@company.com",
        "branch": "feature/python-focus",
        "reviewer": "senior-dev@company.com",
        "approved": True
    }
)
```

### Team Annotations

```python
# Document changes for team
def add_team_annotation(pv, prompt_name, version, change_summary, author):
    """Standard team annotation format"""

    pv.add_annotation(
        name=prompt_name,
        version=version,
        text=f"[CHANGE] {change_summary}",
        author=author
    )

# Usage examples
add_team_annotation(
    pv, "email_classifier", "1.2.0",
    "Improved spam detection accuracy by 15%",
    "ml-team@company.com"
)

add_team_annotation(
    pv, "customer_service", "2.1.0",
    "Added support for multiple languages",
    "product@company.com"
)

# Review team annotations
annotations = pv.get_annotations("customer_service", "2.1.0")
for note in annotations:
    print(f"[{note['author']}] {note['text']}")
    print(f"Added: {note['timestamp']}\n")
```

## 📤 Sharing and Distribution

### Export for Team Sharing

```python
# Export prompts for team distribution
def export_for_team(pv, prompt_name, output_dir):
    """Export prompt with full context for team sharing"""

    from pathlib import Path
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"{prompt_name}_{timestamp}.json"

    pv.export_prompt(
        name=prompt_name,
        output_file=output_file,
        format="json",
        include_metrics=True
    )

    print(f"📤 Exported {prompt_name} to {output_file}")
    print(f"Share this file with your team!")

    return output_file

# Export latest version
export_for_team(pv, "customer_service", "team_exports")
```

## 🎯 Review Processes

### Code Review for Prompts

```python
def create_review_request(pv, prompt_name, old_version, new_version, reviewers):
    """Create a prompt review request"""

    # Generate diff for review
    diff = pv.diff(prompt_name, old_version, new_version, format_output=False)

    # Create review annotation
    review_text = f"""
REVIEW REQUEST
--------------
Changes: {old_version} → {new_version}
Reviewers: {', '.join(reviewers)}
Summary: {diff.summary}

Please review and approve/reject this change.
    """.strip()

    pv.add_annotation(
        name=prompt_name,
        version=new_version,
        text=review_text,
        author="review-system"
    )

    print(f"📋 Review request created for {prompt_name} v{new_version}")
    print(f"Reviewers: {', '.join(reviewers)}")

def approve_change(pv, prompt_name, version, reviewer, approved=True):
    """Approve or reject a prompt change"""

    status = "APPROVED" if approved else "REJECTED"

    pv.add_annotation(
        name=prompt_name,
        version=version,
        text=f"[{status}] Reviewed by {reviewer}",
        author=reviewer
    )

    print(f"✅ Change {status.lower()} by {reviewer}")

# Example workflow
create_review_request(
    pv, "code_reviewer", "1.0.0", "1.1.0",
    ["senior-dev@company.com", "team-lead@company.com"]
)

approve_change(pv, "code_reviewer", "1.1.0", "senior-dev@company.com", approved=True)
```

## 🚀 Team Setup Checklist

1. ✅ **Initialize Git**: Enable Git integration for version control
2. ✅ **Set Team Standards**: Define annotation formats and review processes
3. ✅ **Install Hooks**: Set up Git hooks for automatic tracking
4. ✅ **Define Roles**: Establish team roles and permissions
5. ✅ **Create Workflows**: Document review and approval processes
6. ✅ **Setup Monitoring**: Track team performance and activity
7. ✅ **Train Team**: Ensure all members understand the tools and processes

## 📚 Next Steps

- [Version Management](version-management.md) - Learn advanced version control
- [Web Dashboard](web-dashboard.md) - Use the visual interface for team collaboration
- [Performance Monitoring](performance-monitoring.md) - Monitor team prompt performance
