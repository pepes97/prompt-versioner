# Version Manager

The `VersionManager` class provides utilities for semantic version management and calculations following SemVer 2.0.0 standards.

## Overview

The Version Manager is a utility class responsible for:
- Parsing and validating semantic version strings
- Calculating next versions with different bump types
- Comparing versions for ordering
- Supporting pre-release labels (SNAPSHOT, M, RC)

## Class Reference

### VersionManager

```python
from prompt_versioner.core.version_manager import VersionManager
```

A static utility class for semantic versioning operations. All methods are static and don't require instantiation.

## Methods

### parse_bump_type()

```python
@staticmethod
def parse_bump_type(bump_type: VersionBump | str | None) -> Optional[VersionBump]
```

Parse bump type from string or enum value.

**Parameters:**
- `bump_type` (VersionBump | str | None): VersionBump enum or string ("major", "minor", "patch")

**Returns:**
- `Optional[VersionBump]`: Parsed VersionBump enum or None if invalid

**Example:**
```python
from prompt_versioner.core.version_manager import VersionManager
from prompt_versioner.core.enums import VersionBump

# Parse from string
bump = VersionManager.parse_bump_type("patch")  # → VersionBump.PATCH
bump = VersionManager.parse_bump_type("MAJOR")  # → VersionBump.MAJOR

# Pass through enum
bump = VersionManager.parse_bump_type(VersionBump.MINOR)  # → VersionBump.MINOR
```

### parse_pre_label()

```python
@staticmethod
def parse_pre_label(pre_label: PreReleaseLabel | str | None) -> Optional[PreReleaseLabel]
```

Parse pre-release label from string or enum value.

**Parameters:**
- `pre_label` (PreReleaseLabel | str | None): PreReleaseLabel enum or string

**Returns:**
- `Optional[PreReleaseLabel]`: Parsed PreReleaseLabel enum or None if invalid

**Example:**
```python
# Parse from string
label = VersionManager.parse_pre_label("snapshot")  # → PreReleaseLabel.SNAPSHOT
label = VersionManager.parse_pre_label("RC")        # → PreReleaseLabel.RC
label = VersionManager.parse_pre_label("m")         # → PreReleaseLabel.MILESTONE
label = VersionManager.parse_pre_label("stable")    # → PreReleaseLabel.STABLE
```

### parse_version()

```python
@staticmethod
def parse_version(version_string: str) -> Optional[Dict]
```

Parse a semantic version string into its components.

**Parameters:**
- `version_string` (str): Version string (e.g., "1.2.3-RC.1")

**Returns:**
- `Optional[Dict]`: Dictionary with parsed components or None if invalid

**Components:**
- `major` (int): Major version number
- `minor` (int): Minor version number
- `patch` (int): Patch version number
- `pre_label` (str): Pre-release label (if any)
- `pre_number` (int): Pre-release number (if any)

**Example:**
```python
# Parse different version formats
parsed = VersionManager.parse_version("1.2.3")
# → {"major": 1, "minor": 2, "patch": 3, "pre_label": None, "pre_number": None}

parsed = VersionManager.parse_version("2.0.0-RC.1")
# → {"major": 2, "minor": 0, "patch": 0, "pre_label": "RC", "pre_number": 1}

parsed = VersionManager.parse_version("1.5.0-SNAPSHOT")
# → {"major": 1, "minor": 5, "patch": 0, "pre_label": "SNAPSHOT", "pre_number": None}
```

### format_version()

```python
@staticmethod
def format_version(
    major: int,
    minor: int,
    patch: int,
    pre_label: Optional[PreReleaseLabel] = None,
    pre_number: Optional[int] = None,
) -> str
```

Format version components into a semantic version string.

**Parameters:**
- `major` (int): Major version number
- `minor` (int): Minor version number
- `patch` (int): Patch version number
- `pre_label` (Optional[PreReleaseLabel]): Pre-release label
- `pre_number` (Optional[int]): Pre-release number

**Returns:**
- `str`: Formatted version string

**Example:**
```python
from prompt_versioner.core.enums import PreReleaseLabel

# Basic version
version = VersionManager.format_version(1, 2, 3)  # → "1.2.3"

# With pre-release label
version = VersionManager.format_version(1, 0, 0, PreReleaseLabel.RC, 1)  # → "1.0.0-RC.1"

# Snapshot version
version = VersionManager.format_version(2, 1, 0, PreReleaseLabel.SNAPSHOT)  # → "2.1.0-SNAPSHOT"
```

### calculate_next_version()

```python
@staticmethod
def calculate_next_version(
    current_version: Optional[str],
    bump_type: VersionBump,
    pre_label: Optional[PreReleaseLabel] = None,
    pre_number: Optional[int] = None,
) -> str
```

Calculate the next semantic version following SemVer 2.0.0 rules.

**Parameters:**
- `current_version` (Optional[str]): Current version string or None for first version
- `bump_type` (VersionBump): Type of version bump (MAJOR, MINOR, PATCH)
- `pre_label` (Optional[PreReleaseLabel]): Pre-release label for new version
- `pre_number` (Optional[int]): Pre-release number

**Returns:**
- `str`: Next version string

**Example:**
```python
from prompt_versioner.core.enums import VersionBump, PreReleaseLabel

# First version
next_ver = VersionManager.calculate_next_version(None, VersionBump.PATCH)
# → "1.0.0"

# Increment patch
next_ver = VersionManager.calculate_next_version("1.0.0", VersionBump.PATCH)
# → "1.0.1"

# Minor with pre-release
next_ver = VersionManager.calculate_next_version(
    "1.0.0",
    VersionBump.MINOR,
    PreReleaseLabel.SNAPSHOT
)
# → "1.1.0-SNAPSHOT"

# Release candidate
next_ver = VersionManager.calculate_next_version(
    "1.0.0",
    VersionBump.MINOR,
    PreReleaseLabel.RC,
    1
)
# → "1.1.0-RC.1"

# Promote RC to stable
next_ver = VersionManager.calculate_next_version(
    "1.0.0-RC.2",
    VersionBump.PATCH,
    PreReleaseLabel.STABLE
)
# → "1.0.0"
```

### is_valid_semver()

```python
@staticmethod
def is_valid_semver(version_string: str) -> bool
```

Check if a version string is valid SemVer format.

**Parameters:**
- `version_string` (str): Version string to validate

**Returns:**
- `bool`: True if valid semantic version

**Example:**
```python
# Valid versions
VersionManager.is_valid_semver("1.0.0")        # → True
VersionManager.is_valid_semver("2.1.3-RC.1")   # → True
VersionManager.is_valid_semver("0.0.1-SNAPSHOT") # → True

# Invalid versions
VersionManager.is_valid_semver("1.0")          # → False
VersionManager.is_valid_semver("v1.0.0")       # → False
VersionManager.is_valid_semver("1.0.0.1")      # → False
```

### compare_versions()

```python
@staticmethod
def compare_versions(version1: str, version2: str) -> int
```

Compare two semantic versions according to SemVer precedence rules.

**Parameters:**
- `version1` (str): First version to compare
- `version2` (str): Second version to compare

**Returns:**
- `int`: -1 if version1 < version2, 0 if equal, 1 if version1 > version2

**Precedence Rules:**
1. Major.minor.patch numbers are compared numerically
2. Stable versions have higher precedence than pre-release
3. Pre-release precedence: SNAPSHOT < M < RC
4. Pre-release numbers are compared numerically

**Example:**
```python
# Basic comparison
VersionManager.compare_versions("1.0.0", "1.0.1")    # → -1
VersionManager.compare_versions("2.0.0", "1.9.9")    # → 1
VersionManager.compare_versions("1.0.0", "1.0.0")    # → 0

# Pre-release comparison
VersionManager.compare_versions("1.0.0-RC.1", "1.0.0")      # → -1 (stable > pre-release)
VersionManager.compare_versions("1.0.0-M.1", "1.0.0-RC.1")  # → -1 (M < RC)
VersionManager.compare_versions("1.0.0-RC.1", "1.0.0-RC.2") # → -1 (RC.1 < RC.2)
```

## Version Bump Types

The Version Manager works with the `VersionBump` enum for semantic versioning:

### VersionBump Enum

```python
from prompt_versioner.core.enums import VersionBump

class VersionBump(Enum):
    MAJOR = "major"  # Breaking changes (non-backward compatible)
    MINOR = "minor"  # New features (backward compatible)
    PATCH = "patch"  # Bug fixes (backward compatible)
```

### Usage Examples

```python
# Major version bump - breaking changes
next_version = VersionManager.calculate_next_version("1.5.2", VersionBump.MAJOR)
# → "2.0.0"

# Minor version bump - new features
next_version = VersionManager.calculate_next_version("1.5.2", VersionBump.MINOR)
# → "1.6.0"

# Patch version bump - bug fixes
next_version = VersionManager.calculate_next_version("1.5.2", VersionBump.PATCH)
# → "1.5.3"
```

## Pre-Release Labels

The Version Manager supports pre-release versioning with labels:

### PreReleaseLabel Enum

```python
from prompt_versioner.core.enums import PreReleaseLabel

class PreReleaseLabel(Enum):
    SNAPSHOT = "SNAPSHOT"  # Development version
    MILESTONE = "M"        # Milestone version
    RC = "RC"             # Release Candidate
    STABLE = None         # Stable release (no label)
```

### Pre-Release Workflows

```python
# Development snapshot
dev_version = VersionManager.calculate_next_version(
    "1.0.0",
    VersionBump.MINOR,
    PreReleaseLabel.SNAPSHOT
)
# → "1.1.0-SNAPSHOT"

# Milestone releases
milestone = VersionManager.calculate_next_version(
    "1.1.0-SNAPSHOT",
    VersionBump.PATCH,
    PreReleaseLabel.MILESTONE,
    1
)
# → "1.1.0-M.1"

# Release candidate
rc = VersionManager.calculate_next_version(
    "1.1.0-M.1",
    VersionBump.PATCH,
    PreReleaseLabel.RC,
    1
)
# → "1.1.0-RC.1"

# Final stable release
stable = VersionManager.calculate_next_version(
    "1.1.0-RC.1",
    VersionBump.PATCH,
    PreReleaseLabel.STABLE
)
# → "1.1.0"
```

## Integration with PromptVersioner

The Version Manager is used internally by the main `PromptVersioner` class:

```python
from prompt_versioner import PromptVersioner, VersionBump

pv = PromptVersioner("my-project")

# When you call save_version, VersionManager calculates the next version
version = pv.save_version(
    name="my_prompt",
    system_prompt="You are a helpful assistant.",
    user_prompt="Help with: {request}",
    bump_type=VersionBump.MAJOR  # VersionManager calculates "1.0.0"
)
```

## Error Handling

The Version Manager handles invalid inputs gracefully:

```python
# Invalid version strings return None
parsed = VersionManager.parse_version("invalid")  # → None

# Invalid bump types return None
bump = VersionManager.parse_bump_type("invalid")  # → None

# Version comparison falls back to string comparison for invalid versions
result = VersionManager.compare_versions("invalid1", "invalid2")  # → string comparison
```

## See Also

- [`PromptVersioner`](versioner.md) - Main versioner class that uses VersionManager
- [`VersionBump`](enums.md#versionbump) - Version increment types
- [`PreReleaseLabel`](enums.md#prereleaselabel) - Pre-release label types
