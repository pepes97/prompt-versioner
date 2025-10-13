# Welcome to Prompt Versioner

<div align="center">
    <img src="images/logo.svg" alt="Prompt Versioner Logo" width="200" height="200">
    <h2>Comprehensive Python library for managing and versioning LLM prompts</h2>
</div>

**Prompt Versioner** is an enterprise-grade prompt management system that provides version control, performance tracking, A/B testing, and collaboration tools for AI applications.

## 🎯 Why Prompt Versioner?

In the rapidly evolving world of AI and Large Language Models, managing prompt versions, tracking performance, and ensuring consistent quality is crucial for production applications. **Prompt Versioner** provides enterprise-grade prompt management with:

- **🔄 Version Control**: Complete versioning for prompts with full history
- **📊 Performance Tracking**: Comprehensive metrics and regression detection
- **🧪 A/B Testing**: Built-in statistical framework for prompt optimization
- **⚡ Real-time Monitoring**: Automated alerts and performance dashboards
- **👥 Team Collaboration**: Annotations, reviews, and shared insights
- **🎨 Modern UI**: Beautiful web dashboard with dark/light themes

## ✨ Key Features

### 🔧 Core Functionality
- **Versioning**: Automatic version management with MAJOR/MINOR/PATCH bumps
- **Metrics Tracking**: Comprehensive LLM call metrics (tokens, latency, quality, cost)
- **Export/Import**: Backup and share prompts with full history
- **Git Integration**: Optional Git integration for version control

### 🧪 Advanced Testing & Monitoring
- **A/B Testing**: Built-in statistical framework for comparing prompt versions
- **Performance Monitoring**: Automated regression detection and alerting
- **Real-time Analytics**: Live metrics and performance dashboards
- **Custom Alerts**: Configure thresholds for cost, latency, and quality metrics

### 👥 Collaboration & Management
- **Team Annotations**: Collaborative notes and feedback system
- **Version Comparison**: Detailed diff views with change tracking
- **Search & Filtering**: Find prompts by metadata, performance, and tags

## 🚀 Quick Start

### Installation

```bash
pip install prompt-versioner
```

### Basic Usage

```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize the versioner
versioner = PromptVersioner(project_name="my-app")

# Save a prompt version
version_id = versioner.save_version(
    name="assistant",
    system_prompt="You are a helpful AI assistant.",
    user_prompt="Answer this question: {question}",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={"type": "general_assistant"}
)

# Create a new version
versioner.save_version(
    name="assistant",
    system_prompt="You are an expert AI assistant with deep knowledge.",
    user_prompt="Please provide a detailed answer to: {question}",
    bump_type=VersionBump.MINOR,  # Creates version 1.1.0
    metadata={"improvement": "enhanced expertise"}
)

# Track metrics
versioner.log_metrics(
    name="assistant",
    version="1.1.0",
    model_name="gpt-4o",
    input_tokens=15,
    output_tokens=25,
    latency_ms=1200,
    cost_eur=0.001,
    quality_score=0.95
)
```

### Web Dashboard

Launch the interactive web dashboard:

```bash
python examples/run_dashboard.py
```

<div style="display: flex; justify-content: space-between; margin: 20px 0;">
    <img src="images/dashboard-overview.png" alt="Dashboard Overview" style="width: 48%;">
    <img src="images/dark-mode.png" alt="Dark Mode" style="width: 48%;">
</div>

## 📖 Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation, setup, and configuration
- **[User Guide](user-guide/core-concepts.md)**: Comprehensive guides for all features
- **[Examples](examples/basic-usage.md)**: Practical examples and use cases
- **[API Reference](api-reference/core/versioner.md)**: Complete API documentation
- **[Development](development/contributing.md)**: Contributing and development guides

## 🔗 Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quick-start.md)
- [A/B Testing Guide](user-guide/ab-testing.md)
- [Web Dashboard](user-guide/web-dashboard.md)
- [API Reference](api-reference/core/versioner.md)

## 🤝 Community & Support

- **GitHub Repository**: [pepes97/prompt-versioner](https://github.com/pepes97/prompt-versioner)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/pepes97/prompt-versioner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pepes97/prompt-versioner/discussions)

---

<div align="center">
    <p>Built with ❤️ for the AI community</p>
</div>
