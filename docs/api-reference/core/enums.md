# Enums

Core enumeration classes used throughout the Prompt Versioner library for versioning and configuration.

## Overview

The enums module defines standard constants and types used for version management, pre-release labeling, and system configuration. All enums follow Python's standard `enum.Enum` pattern.

## VersionBump

Defines the type of version increment for semantic versioning operations.

```python
from prompt_versioner.core.enums import VersionBump
```

### Enum Definition

```python
class VersionBump(Enum):
    """Type of version bump following SemVer 2.0.0."""

    MAJOR = "major"  # Breaking changes (non retrocompatibile)
    MINOR = "minor"  # New features (retrocompatibile)
    PATCH = "patch"  # Bug fixes (retrocompatibile)
```

### Values

| Value | String | Description | Version Impact |
|-------|--------|-------------|----------------|
| `MAJOR` | "major" | Breaking changes, non-backward compatible | 1.0.0 → 2.0.0 |
| `MINOR` | "minor" | New features, backward compatible | 1.0.0 → 1.1.0 |
| `PATCH` | "patch" | Bug fixes, backward compatible | 1.0.0 → 1.0.1 |

### Usage Examples

```python
from prompt_versioner import PromptVersioner, VersionBump

pv = PromptVersioner("my-project")

# Major version - breaking change
pv.save_version(
    name="classifier",
    system_prompt="You are a classification expert.",
    user_prompt="Classify: {text}",
    bump_type=VersionBump.MAJOR  # Creates 1.0.0
)

# Minor version - improvement
pv.save_version(
    name="classifier",
    system_prompt="You are an expert text classifier with deep understanding.",
    user_prompt="Classify the following text: {text}",
    bump_type=VersionBump.MINOR  # Creates 1.1.0
)

# Patch version - small fix
pv.save_version(
    name="classifier",
    system_prompt="You are an expert text classifier with deep understanding.",
    user_prompt="Classify the following text carefully: {text}",
    bump_type=VersionBump.PATCH  # Creates 1.1.1
)
```

### When to Use Each Type

#### MAJOR (Breaking Changes)
Use when changes fundamentally alter the prompt's behavior or interface:

```python
# Before: Simple classification
system_prompt = "You are a classifier."
user_prompt = "Classify: {text}"

# After: Structured output format (breaking change)
system_prompt = "You are a classifier. Return JSON format."
user_prompt = "Classify: {text}. Format: {\"category\": \"...\", \"confidence\": 0.9}"

# This is a MAJOR change
bump_type = VersionBump.MAJOR
```

#### MINOR (New Features)
Use when adding new capabilities while maintaining backward compatibility:

```python
# Before: Basic classification
system_prompt = "You are a classifier."
user_prompt = "Classify: {text}"

# After: Added context awareness (compatible)
system_prompt = "You are a classifier with context awareness."
user_prompt = "Context: {context}\nClassify: {text}"

# This is a MINOR change
bump_type = VersionBump.MINOR
```

#### PATCH (Bug Fixes)
Use for small corrections, typos, or minor improvements:

```python
# Before: Typo in prompt
system_prompt = "You are a classifer."  # Typo!
user_prompt = "Classify: {text}"

# After: Fixed typo
system_prompt = "You are a classifier."  # Fixed
user_prompt = "Classify: {text}"

# This is a PATCH change
bump_type = VersionBump.PATCH
```

### String Conversion

The VersionBump enum can be parsed from strings:

```python
from prompt_versioner.core.version_manager import VersionManager

# Parse from string (case-insensitive)
bump = VersionManager.parse_bump_type("major")    # → VersionBump.MAJOR
bump = VersionManager.parse_bump_type("MINOR")    # → VersionBump.MINOR
bump = VersionManager.parse_bump_type("patch")    # → VersionBump.PATCH

# Invalid strings return None
bump = VersionManager.parse_bump_type("invalid")  # → None
```

## PreReleaseLabel

Defines pre-release labels for development and staging versions.

```python
from prompt_versioner.core.enums import PreReleaseLabel
```

### Enum Definition

```python
class PreReleaseLabel(Enum):
    """Pre-release labels for versioning."""

    SNAPSHOT = "SNAPSHOT"  # Development version
    MILESTONE = "M"        # Milestone version
    RC = "RC"             # Release Candidate
    STABLE = None         # Stable release (no label)
```

### Values

| Value | String | Description | Example Version |
|-------|--------|-------------|-----------------|
| `SNAPSHOT` | "SNAPSHOT" | Development/nightly builds | 1.0.0-SNAPSHOT |
| `MILESTONE` | "M" | Feature milestone releases | 1.0.0-M.1 |
| `RC` | "RC" | Release candidates | 1.0.0-RC.1 |
| `STABLE` | None | Stable production releases | 1.0.0 |

### Usage Examples

```python
from prompt_versioner.core.version_manager import VersionManager
from prompt_versioner.core.enums import VersionBump, PreReleaseLabel

# Development snapshot
version = VersionManager.calculate_next_version(
    current_version="1.0.0",
    bump_type=VersionBump.MINOR,
    pre_label=PreReleaseLabel.SNAPSHOT
)
# → "1.1.0-SNAPSHOT"

# Milestone release
version = VersionManager.calculate_next_version(
    current_version="1.1.0-SNAPSHOT",
    bump_type=VersionBump.PATCH,
    pre_label=PreReleaseLabel.MILESTONE,
    pre_number=1
)
# → "1.1.0-M.1"

# Release candidate
version = VersionManager.calculate_next_version(
    current_version="1.1.0-M.1",
    bump_type=VersionBump.PATCH,
    pre_label=PreReleaseLabel.RC,
    pre_number=1
)
# → "1.1.0-RC.1"

# Final stable release
version = VersionManager.calculate_next_version(
    current_version="1.1.0-RC.1",
    bump_type=VersionBump.PATCH,
    pre_label=PreReleaseLabel.STABLE
)
# → "1.1.0"
```

### Pre-Release Workflow

A typical development workflow using pre-release labels:

```python
# 1. Start development with snapshot
dev_version = VersionManager.calculate_next_version(
    "1.0.0", VersionBump.MINOR, PreReleaseLabel.SNAPSHOT
)
# → "1.1.0-SNAPSHOT"

# 2. Feature complete - create milestone
milestone = VersionManager.calculate_next_version(
    "1.1.0-SNAPSHOT", VersionBump.PATCH, PreReleaseLabel.MILESTONE, 1
)
# → "1.1.0-M.1"

# 3. Testing phase - release candidate
rc1 = VersionManager.calculate_next_version(
    "1.1.0-M.1", VersionBump.PATCH, PreReleaseLabel.RC, 1
)
# → "1.1.0-RC.1"

# 4. Bug fixes - new release candidate
rc2 = VersionManager.calculate_next_version(
    "1.1.0-RC.1", VersionBump.PATCH, PreReleaseLabel.RC, 2
)
# → "1.1.0-RC.2"

# 5. Production ready - stable release
stable = VersionManager.calculate_next_version(
    "1.1.0-RC.2", VersionBump.PATCH, PreReleaseLabel.STABLE
)
# → "1.1.0"
```

### String Conversion

PreReleaseLabel can be parsed from strings:

```python
from prompt_versioner.core.version_manager import VersionManager

# Parse from string (case-insensitive)
label = VersionManager.parse_pre_label("snapshot")    # → PreReleaseLabel.SNAPSHOT
label = VersionManager.parse_pre_label("RC")          # → PreReleaseLabel.RC
label = VersionManager.parse_pre_label("m")           # → PreReleaseLabel.MILESTONE
label = VersionManager.parse_pre_label("stable")      # → PreReleaseLabel.STABLE

# Alternative string formats
label = VersionManager.parse_pre_label("milestone")           # → PreReleaseLabel.MILESTONE
label = VersionManager.parse_pre_label("release_candidate")   # → PreReleaseLabel.RC
label = VersionManager.parse_pre_label("")                    # → PreReleaseLabel.STABLE
```

### Version Precedence

Pre-release versions have lower precedence than stable versions:

```python
from prompt_versioner.core.version_manager import VersionManager

# Stable > pre-release
result = VersionManager.compare_versions("1.0.0", "1.0.0-RC.1")  # → 1

# Among pre-releases: SNAPSHOT < M < RC
result = VersionManager.compare_versions("1.0.0-SNAPSHOT", "1.0.0-M.1")  # → -1
result = VersionManager.compare_versions("1.0.0-M.1", "1.0.0-RC.1")      # → -1

# Same label, compare numbers
result = VersionManager.compare_versions("1.0.0-RC.1", "1.0.0-RC.2")     # → -1
```

## Validation and Error Handling

Both enums have validation through the VersionManager:

```python
from prompt_versioner.core.version_manager import VersionManager

# Valid enum values
assert VersionManager.parse_bump_type("major") == VersionBump.MAJOR
assert VersionManager.parse_pre_label("RC") == PreReleaseLabel.RC

# Invalid values return None
assert VersionManager.parse_bump_type("invalid") is None
assert VersionManager.parse_pre_label("invalid") is None

# Use in your code with validation
def safe_version_bump(bump_string: str) -> VersionBump:
    bump = VersionManager.parse_bump_type(bump_string)
    if bump is None:
        raise ValueError(f"Invalid bump type: {bump_string}")
    return bump
```

## See Also

- [`VersionManager`](version-manager.md) - Uses these enums for version calculations
- [`PromptVersioner`](versioner.md) - Main class that accepts these enum values
- [Semantic Versioning](https://semver.org/) - Official SemVer specification
