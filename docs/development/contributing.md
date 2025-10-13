# Contributing

We welcome contributions to **Prompt Versioner**! This guide will help you get started with contributing to the project.

## 🚀 Quick Start for Contributors

### Prerequisites

- **Python 3.11+**
- **Poetry** (for dependency management)
- **Git**
- **Node.js** (for web dashboard development)

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner

# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=prompt_versioner --cov-report=html

# Run specific test file
poetry run pytest tests/test_versioner.py

# Run tests with verbose output
poetry run pytest -v
```

### Code Quality

We maintain high code quality standards using several tools:

```bash
# Format code with Black
poetry run black prompt_versioner/ tests/

# Lint with Ruff
poetry run ruff check prompt_versioner/ tests/

# Type checking with MyPy
poetry run mypy prompt_versioner/

# Run all quality checks
poetry run pre-commit run --all-files
```

## 📝 Development Guidelines

### Code Style

We follow these coding standards:

- **PEP 8** compliance with 100-character line length
- **Type hints** for all public functions and methods
- **Docstrings** in Google style for all public APIs
- **Black** for code formatting
- **Ruff** for linting

### Example Code Style

```python
from typing import Optional, Dict, Any, List
from datetime import datetime

class PromptVersioner:
    """Main class for prompt version management.

    This class provides comprehensive prompt management capabilities including
    versioning, metrics tracking, and A/B testing coordination.

    Args:
        db_path: Path to SQLite database file
        git_repo: Optional path to Git repository for version control
        config: Optional configuration object

    Example:
        >>> versioner = PromptVersioner(db_path="prompts.db")
        >>> prompt_id = versioner.save_prompt(
        ...     content="Hello {name}",
        ...     variables={"name": "World"}
        ... )
    """

    def __init__(
        self,
        db_path: str = "prompts.db",
        git_repo: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        self.db_path = db_path
        self.git_repo = git_repo
        self.config = config or {}

    def save_prompt(
        self,
        content: str,
        variables: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None
    ) -> str:
        """Save a new prompt to the database.

        Args:
            content: The prompt template content with variable placeholders
            variables: Dictionary of default variable values
            tags: List of tags for organization and discovery
            description: Human-readable description of the prompt

        Returns:
            Unique identifier for the created prompt

        Raises:
            ValueError: If content is empty or invalid
            DatabaseError: If database operation fails
        """
        if not content.strip():
            raise ValueError("Prompt content cannot be empty")

        # Implementation here...
        return "prompt-id-uuid"
```

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear commit history:

```bash
# Features
feat: add A/B testing framework
feat(web): implement dark mode toggle
feat(cli): add export command with JSON format

# Bug fixes
fix: resolve database connection leak
fix(metrics): correct quality score calculation
fix(web): fix responsive layout on mobile

# Documentation
docs: add contributing guidelines
docs: update API reference for versioner class
docs(examples): add advanced A/B testing example

# Tests
test: add unit tests for version manager
test: improve coverage for metrics calculator
test(integration): add end-to-end dashboard tests

# Refactoring
refactor: simplify prompt rendering logic
refactor(storage): optimize database queries
refactor: extract common utilities to shared module

# Performance
perf: optimize database indexing
perf(web): implement lazy loading for large datasets

# CI/CD
ci: add automated documentation deployment
ci: update Python version in workflows
```

## 🧪 Testing Guidelines

### Test Structure

We organize tests by component:

```
tests/
├── unit/                 # Unit tests for individual components
│   ├── test_versioner.py
│   ├── test_version_manager.py
│   ├── test_metrics.py
│   └── test_ab_testing.py
├── integration/          # Integration tests
│   ├── test_database.py
│   ├── test_git_integration.py
│   └── test_web_dashboard.py
├── e2e/                  # End-to-end tests
│   ├── test_full_workflow.py
│   └── test_cli_commands.py
├── fixtures/             # Test data and fixtures
│   ├── sample_prompts.json
│   └── test_database.sql
└── conftest.py           # Pytest configuration
```

### Writing Tests

#### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
from prompt_versioner.core.versioner import PromptVersioner

class TestPromptVersioner:
    """Test cases for PromptVersioner class."""

    @pytest.fixture
    def versioner(self, tmp_path):
        """Create a versioner instance with temporary database."""
        db_path = tmp_path / "test.db"
        return PromptVersioner(db_path=str(db_path))

    def test_save_prompt_success(self, versioner):
        """Test successful prompt creation."""
        prompt_id = versioner.save_prompt(
            content="Hello {name}",
            variables={"name": "World"},
            tags=["greeting"],
            description="Simple greeting prompt"
        )

        assert prompt_id is not None
        assert len(prompt_id) == 36  # UUID length

        # Verify prompt was saved
        prompt = versioner.get_prompt(prompt_id)
        assert prompt["content"] == "Hello {name}"
        assert prompt["variables"]["name"] == "World"
        assert "greeting" in prompt["tags"]

    def test_save_prompt_empty_content_raises_error(self, versioner):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Prompt content cannot be empty"):
            versioner.save_prompt(content="")

    @patch('prompt_versioner.storage.database.DatabaseManager')
    def test_save_prompt_database_error(self, mock_db, versioner):
        """Test handling of database errors."""
        mock_db.return_value.save_prompt.side_effect = Exception("DB Error")

        with pytest.raises(Exception, match="DB Error"):
            versioner.save_prompt(content="Test content")
```

#### Integration Tests

```python
import pytest
import tempfile
import shutil
from pathlib import Path
from prompt_versioner import PromptVersioner

class TestGitIntegration:
    """Test Git integration functionality."""

    @pytest.fixture
    def git_repo(self, tmp_path):
        """Create a temporary Git repository."""
        repo_path = tmp_path / "git_repo"
        repo_path.mkdir()

        # Initialize git repo
        import subprocess
        subprocess.run(["git", "init"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path)

        return repo_path

    def test_git_auto_commit(self, tmp_path, git_repo):
        """Test automatic Git commits on prompt changes."""
        db_path = tmp_path / "prompts.db"
        versioner = PromptVersioner(
            db_path=str(db_path),
            git_repo=str(git_repo),
            git_auto_commit=True
        )

        # Create a prompt
        prompt_id = versioner.save_prompt(
            content="Test prompt",
            description="Test auto-commit"
        )

        # Check that commit was created
        import subprocess
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=git_repo,
            capture_output=True,
            text=True
        )

        assert "feat: created prompt" in result.stdout
```

#### End-to-End Tests

```python
import pytest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestWebDashboard:
    """End-to-end tests for web dashboard."""

    @pytest.fixture(scope="session")
    def dashboard_server(self):
        """Start dashboard server for testing."""
        # Start server in background
        process = subprocess.Popen(
            ["python", "-m", "prompt_versioner.web.app"],
            env={"PROMPT_VERSIONER_PORT": "5001"}
        )
        time.sleep(2)  # Wait for server to start

        yield "http://localhost:5001"

        # Cleanup
        process.terminate()
        process.wait()

    @pytest.fixture
    def browser(self):
        """Create browser instance."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    def test_dashboard_loads(self, browser, dashboard_server):
        """Test that dashboard loads successfully."""
        browser.get(dashboard_server)

        # Check page title
        assert "Prompt Versioner" in browser.title

        # Check main elements exist
        assert browser.find_element(By.CLASS_NAME, "dashboard-overview")
        assert browser.find_element(By.CLASS_NAME, "navigation-menu")
```

### Test Coverage

We aim for high test coverage:

```bash
# Generate coverage report
poetry run pytest --cov=prompt_versioner --cov-report=html --cov-report=term

# View coverage in browser
open htmlcov/index.html

# Coverage requirements:
# - Overall coverage: >90%
# - Critical paths: 100%
# - New code: 100%
```

## 📁 Project Structure

### Core Architecture

```
prompt_versioner/
├── __init__.py           # Package initialization
├── core/                 # Core business logic
│   ├── __init__.py
│   ├── versioner.py      # Main versioner class
│   ├── version_manager.py # Version management
│   ├── enums.py          # Enumerations and constants
│   └── test_context.py   # Testing context utilities
├── storage/              # Data persistence layer
│   ├── __init__.py
│   ├── database.py       # Database management
│   ├── schema.py         # Database schema
│   ├── queries.py        # SQL queries
│   ├── versions.py       # Version storage
│   ├── metrics.py        # Metrics storage
│   └── annotations.py    # Annotations storage
├── metrics/              # Performance metrics
│   ├── __init__.py
│   ├── tracker.py        # Metrics tracking
│   ├── analyzer.py       # Analysis engine
│   ├── calculator.py     # Calculations
│   ├── aggregator.py     # Data aggregation
│   ├── models.py         # Data models
│   └── pricing.py        # Cost calculations
├── testing/              # A/B testing framework
│   ├── __init__.py
│   ├── ab_test.py        # A/B test management
│   ├── runner.py         # Test execution
│   ├── dataset.py        # Test datasets
│   ├── models.py         # Test models
│   └── formatters.py     # Result formatting
├── tracker/              # Change tracking
│   ├── __init__.py
│   ├── git.py            # Git integration
│   ├── hasher.py         # Content hashing
│   └── auto.py           # Automatic tracking
├── cli/                  # Command-line interface
│   ├── __init__.py
│   ├── main_cli.py       # Main CLI entry point
│   ├── commands/         # CLI commands
│   └── utils/            # CLI utilities
├── web/                  # Web dashboard
│   ├── __init__.py
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   ├── app/              # Flask application
│   └── utils/            # Web utilities
└── app/                  # Application configuration
    ├── __init__.py
    ├── config.py         # Configuration management
    ├── flask_builder.py  # Flask app builder
    ├── controllers/      # Web controllers
    ├── models/           # Web models
    └── services/         # Business services
```

### Adding New Features

When adding new features:

1. **Create feature branch**: `git checkout -b feature/new-feature-name`
2. **Add tests first**: Write tests that describe the expected behavior
3. **Implement feature**: Write the minimal code to make tests pass
4. **Update documentation**: Add or update relevant documentation
5. **Submit PR**: Create pull request with clear description

#### Feature Development Template

```python
# 1. Add tests (tests/unit/test_new_feature.py)
class TestNewFeature:
    def test_new_functionality(self):
        # Test implementation
        pass

# 2. Implement feature (prompt_versioner/core/new_feature.py)
class NewFeature:
    """New feature implementation."""

    def __init__(self):
        pass

    def new_method(self):
        """New method implementation."""
        pass

# 3. Update main versioner class
class PromptVersioner:
    def __init__(self):
        self.new_feature = NewFeature()

    def use_new_feature(self):
        """Expose new feature functionality."""
        return self.new_feature.new_method()

# 4. Add CLI command (prompt_versioner/cli/commands/new_command.py)
@click.command()
def new_command():
    """CLI command for new feature."""
    pass

# 5. Update documentation (docs/user-guide/new-feature.md)
```

## 🔍 Debugging and Development Tools

### Development Server

```bash
# Start development web server with auto-reload
poetry run python -m prompt_versioner.web.app --debug

# Start with specific configuration
poetry run python -m prompt_versioner.web.app --config dev_config.yaml
```

### Database Tools

```bash
# Inspect database schema
poetry run python -c "
from prompt_versioner.storage.database import DatabaseManager
db = DatabaseManager('prompts.db')
db.print_schema()
"

# Export database for debugging
poetry run python -c "
from prompt_versioner import PromptVersioner
v = PromptVersioner('prompts.db')
v.export_database('debug_export.json')
"
```

### Profiling

```python
# Performance profiling
import cProfile
import pstats
from prompt_versioner import PromptVersioner

def profile_operation():
    versioner = PromptVersioner()
    # Your operation here
    pass

if __name__ == "__main__":
    cProfile.run('profile_operation()', 'profile_stats')
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('cumulative').print_stats(10)
```

## 📚 Documentation

### Documentation Structure

- **Getting Started**: Installation, quick start, configuration
- **User Guide**: Comprehensive feature documentation
- **Examples**: Practical examples and use cases
- **API Reference**: Complete API documentation
- **Development**: Contributing and development guides

### Writing Documentation

- Use **clear, concise language**
- Include **code examples** for all features
- Add **screenshots** for UI features
- Keep **API documentation** up to date
- Use **consistent formatting**

### Building Documentation Locally

```bash
# Install documentation dependencies
pip install mkdocs-material mkdocs-autorefs mkdocstrings[python]

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 🚀 Release Process

### Version Management

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite**: `poetry run pytest`
4. **Build documentation**: `mkdocs build`
5. **Create release tag**: `git tag v1.2.3`
6. **Build package**: `poetry build`
7. **Publish to PyPI**: `poetry publish`
8. **Create GitHub release** with release notes

### Automated Releases

We use GitHub Actions for automated releases:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Poetry
        run: pip install poetry
      - name: Build and publish
        run: |
          poetry build
          poetry publish --username __token__ --password ${{ secrets.PYPI_TOKEN }}
```

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our [Code of Conduct](https://github.com/pepes97/prompt-versioner/blob/main/CODE_OF_CONDUCT.md).

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussion
- **Pull Requests**: Code contributions and reviews

### Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Major contributions highlighted
- **Documentation**: Author attribution where appropriate

Thank you for contributing to Prompt Versioner! 🎉
