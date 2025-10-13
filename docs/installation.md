# Installation

## Prerequisites

Before installing Prompt Versioner, ensure you have:

- **Python 3.11** or higher
- **Poetry** (recommended) or pip
- **Git** (optional, for version control integration)

## Using Poetry (Recommended)

Poetry provides better dependency management and virtual environment handling:

```bash
# Install from GitHub repository
poetry add git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally for development
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
poetry install
```

## Using pip

If you prefer pip, you can install directly:

```bash
# Install from GitHub repository
pip install git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
pip install -e .
```

## Verify Installation

Test that everything is working correctly:

```bash
# Check if CLI is available
pv --help

# Launch dashboard to verify web interface
pv dashboard --port 5000
```

If the commands work without errors, you're ready to go!

## Optional Dependencies

For enhanced functionality, you may want to install additional packages:

### Git Integration
```bash
# Already included in main installation
pip install gitpython
```

### Development Tools
```bash
# For contributing to the project
pip install pytest black ruff mypy pre-commit
```

### Web Dashboard Dependencies
```bash
# Already included in main installation
pip install flask rich click
```

## Next Steps

Now that you have Prompt Versioner installed, check out the [Quick Start Guide](quickstart.md) to begin managing your prompts!
