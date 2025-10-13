# Installation

This guide will help you install and set up **Prompt Versioner** in your environment.

## Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux

## Installation Methods

### 📦 Poetry (Recommended)

Install from the GitHub repository:

```bash
# Install from GitHub repository
poetry add git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally for development
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
poetry install
```

### 🚀 Development Installation

For development:

```bash
# Clone the repository
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner

# Install with Poetry
poetry install

# Or install with pip in development mode
pip install -e .
```

## Verification

Verify your installation:

```python
# Test the Python import
from prompt_versioner import PromptVersioner, VersionBump
pv = PromptVersioner(project_name="test", enable_git=False)
print("✅ Prompt Versioner is working!")
```

## Database Setup

Prompt Versioner uses SQLite by default - no additional setup required. The database file will be created automatically.

### Custom Database Location

```python
from prompt_versioner import PromptVersioner

# Custom database path
pv = PromptVersioner(
    project_name="my-project",
    db_path="/path/to/your/database.db"
)
```

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/pepes97/prompt-versioner/issues)
2. Include your Python version, OS, and error messages

## Next Steps

Now that you have Prompt Versioner installed:

- [Quick Start Guide](quick-start.md) - Get up and running in minutes
- [Configuration](configuration.md) - Customize your setup
- [Basic Usage](../examples/basic-usage.md) - Learn with practical examples
