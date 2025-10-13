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

### Quality Gates

```python
def check_quality_gate(pv, prompt_name, version, min_quality=0.8, min_samples=10):
    """Check if version meets quality gate requirements"""

    version_data = pv.get_version(prompt_name, version)
    metrics = pv.storage.get_metrics(version_id=version_data["id"], limit=100)

    if len(metrics) < min_samples:
        return {
            "passed": False,
            "reason": f"Insufficient samples: {len(metrics)} < {min_samples}"
        }

    avg_quality = sum(m.get("quality_score", 0) for m in metrics) / len(metrics)

    if avg_quality < min_quality:
        return {
            "passed": False,
            "reason": f"Quality below threshold: {avg_quality:.2f} < {min_quality}"
        }

    return {
        "passed": True,
        "quality": avg_quality,
        "samples": len(metrics)
    }

# Check quality gate before deployment
gate_result = check_quality_gate(pv, "customer_service", "2.1.0")

if gate_result["passed"]:
    print("✅ Quality gate passed - ready for deployment")
else:
    print(f"❌ Quality gate failed: {gate_result['reason']}")
```

## 📊 Team Metrics

### Team Performance Dashboard

```python
def generate_team_report(pv, prompts, days=7):
    """Generate team performance report"""

    from datetime import datetime, timedelta

    print("📊 TEAM PERFORMANCE REPORT")
    print("=" * 40)

    total_calls = 0
    total_cost = 0.0

    for prompt_name in prompts:
        latest = pv.get_latest(prompt_name)
        if not latest:
            continue

        metrics = pv.storage.get_metrics(version_id=latest["id"], limit=1000)

        # Filter recent metrics
        cutoff = datetime.now() - timedelta(days=days)
        recent_metrics = [
            m for m in metrics
            if datetime.fromisoformat(m.get('timestamp', '1970-01-01')) > cutoff
        ]

        if recent_metrics:
            calls = len(recent_metrics)
            avg_quality = sum(m.get("quality_score", 0) for m in recent_metrics) / calls
            cost = sum(m.get("cost_eur", 0) for m in recent_metrics)

            print(f"\n{prompt_name} v{latest['version']}:")
            print(f"  Calls: {calls}")
            print(f"  Quality: {avg_quality:.2f}")
            print(f"  Cost: €{cost:.3f}")

            total_calls += calls
            total_cost += cost

    print(f"\n📈 TOTALS (Last {days} days):")
    print(f"  Total Calls: {total_calls}")
    print(f"  Total Cost: €{total_cost:.3f}")
    print(f"  Avg Cost/Call: €{total_cost/total_calls:.4f}" if total_calls > 0 else "  No calls")

# Generate report for team prompts
team_prompts = ["customer_service", "code_reviewer", "email_classifier"]
generate_team_report(pv, team_prompts, days=7)
```

### Activity Tracking

```python
def track_team_activity(pv, prompts):
    """Track team activity across prompts"""

    activity = {}

    for prompt_name in prompts:
        versions = pv.list_versions(prompt_name)
        annotations = []

        for version in versions:
            version_annotations = pv.get_annotations(prompt_name, version['version'])
            annotations.extend(version_annotations)

        # Group by author
        for annotation in annotations:
            author = annotation['author']
            if author not in activity:
                activity[author] = []

            activity[author].append({
                "prompt": prompt_name,
                "action": annotation['text'][:50] + "...",
                "timestamp": annotation['timestamp']
            })

    # Report activity
    print("👥 TEAM ACTIVITY SUMMARY")
    print("=" * 30)

    for author, actions in activity.items():
        print(f"\n{author}: {len(actions)} actions")
        for action in actions[-3:]:  # Show last 3 actions
            print(f"  • {action['prompt']}: {action['action']}")

# Track team activity
track_team_activity(pv, team_prompts)
```

## 🔒 Access Control

### Role-Based Permissions

```python
# Define team roles and permissions
TEAM_ROLES = {
    "admin": {
        "can_create": True,
        "can_edit": True,
        "can_delete": True,
        "can_export": True,
        "can_view_metrics": True
    },
    "developer": {
        "can_create": True,
        "can_edit": True,
        "can_delete": False,
        "can_export": True,
        "can_view_metrics": True
    },
    "reviewer": {
        "can_create": False,
        "can_edit": False,
        "can_delete": False,
        "can_export": False,
        "can_view_metrics": True
    }
}

def check_permission(user_role, action):
    """Check if user role has permission for action"""
    permissions = TEAM_ROLES.get(user_role, {})
    return permissions.get(f"can_{action}", False)

# Usage
if check_permission("developer", "edit"):
    print("✅ Permission granted")
else:
    print("❌ Permission denied")
```

## 🎯 Best Practices

### 1. Clear Communication
- Use descriptive commit messages
- Add meaningful annotations for all changes
- Document the reasoning behind prompt modifications
- Tag team members in relevant annotations

### 2. Version Control
- Enable Git integration for all team projects
- Use feature branches for experimental changes
- Review all changes before merging to main
- Tag stable versions for production use

### 3. Quality Assurance
- Implement quality gates for all releases
- Require peer review for critical prompts
- Test changes thoroughly before deployment
- Monitor performance after deployment

### 4. Documentation
- Maintain clear documentation for all prompts
- Document team processes and workflows
- Keep track of decisions and rationales
- Update documentation when processes change

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
