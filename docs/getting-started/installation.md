# Installation

This guide will help you install and set up **Prompt Versioner** in your environment.

## Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 512MB available RAM
- **Storage**: 100MB for installation plus database storage

## Installation Methods

### 📦 PyPI (Recommended)

Install the latest stable version from PyPI:

```bash
pip install prompt-versioner
```

### 🚀 Development Installation

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner

# Install with Poetry (recommended)
poetry install

# Or install with pip in development mode
pip install -e .
```

### 🐳 Docker Installation

Run Prompt Versioner in a Docker container:

```bash
# Pull the image
docker pull ghcr.io/pepes97/prompt-versioner:latest

# Run with volume mounting for data persistence
docker run -d \
  --name prompt-versioner \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  ghcr.io/pepes97/prompt-versioner:latest
```

## Verification

Verify your installation by checking the version:

```bash
# Check CLI (if available)
pv --version

# Or check in Python
python -c "import prompt_versioner; print('✅ Installed successfully!')"
```

Or test the Python import:

```python
from prompt_versioner import PromptVersioner, VersionBump
pv = PromptVersioner(project_name="test", enable_git=False)
print("✅ Prompt Versioner is working!")
```

## Optional Dependencies

### Web Dashboard Dependencies

The web dashboard requires additional dependencies that are included by default:

- **Flask**: Web framework for the dashboard
- **Rich**: Enhanced terminal output

### Git Integration

For Git integration features:

```bash
pip install gitpython
```

### OpenAI Integration

For OpenAI API integration examples:

```bash
pip install openai
```

## Database Setup

Prompt Versioner uses SQLite by default, which requires no additional setup. The database file will be created automatically when you first use the library.

### Custom Database Location

You can specify a custom database location:

```python
from prompt_versioner import PromptVersioner

# Custom database path
pv = PromptVersioner(
    project_name="my-project",
    db_path="/path/to/your/database.db"
)
```

### Database Migration

If you're upgrading from an older version, the database schema will be automatically migrated when you first use the library.

## Environment Variables

You can configure Prompt Versioner using environment variables:

```bash
# Project configuration
export PROMPT_VERSIONER_PROJECT="my-project"
export PROMPT_VERSIONER_DB_PATH="/path/to/database.db"

# Git integration
export PROMPT_VERSIONER_ENABLE_GIT="true"
export PROMPT_VERSIONER_GIT_REPO="/path/to/git/repo"

# OpenAI API key for examples
export OPENAI_API_KEY="your-openai-api-key"
```

## Troubleshooting

### Common Issues

#### 1. Permission Errors

If you encounter permission errors during installation:

```bash
# Install with user flag
pip install --user prompt-versioner

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install prompt-versioner
```

#### 2. Python Version Compatibility

Ensure you're using Python 3.11 or higher:

```bash
python --version
```

If you have multiple Python versions, use the specific version:

```bash
python3.11 -m pip install prompt-versioner
```

#### 3. Database Permission Issues

Ensure the directory where the database will be created has write permissions:

```bash
# Check permissions
ls -la /path/to/database/directory

# Fix permissions if needed
chmod 755 /path/to/database/directory
```

#### 4. Port Already in Use

If port 5000 is already in use for the web dashboard:

```python
# Use a different port programmatically
pv = PromptVersioner(project_name="my-project")
# pv.start_dashboard(port=8080)  # If dashboard available
```

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/pepes97/prompt-versioner/issues)
2. Search existing issues or create a new one
3. Include your Python version, OS, and error messages
4. Consider joining our [GitHub Discussions](https://github.com/pepes97/prompt-versioner/discussions)

## Next Steps

Now that you have Prompt Versioner installed, check out:

- [Quick Start Guide](quick-start.md) - Get up and running in minutes
- [Configuration](configuration.md) - Customize your setup
- [Basic Usage](../examples/basic-usage.md) - Learn with practical examples
- [Version Management](../user-guide/version-management.md) - Understand version control
