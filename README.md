<div align="center">


<img src="docs/images/logo.svg" alt="Prompt Versioner Logo" width="250" height="250">

**A comprehensive Python library for managing and versioning LLM prompts, with built-in A/B testing, metric tracking, and performance monitoring capabilities.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Web Dashboard](#-web-dashboard) • [Examples](#-examples--use-cases) • [Documentation](https://pepes97.github.io/prompt-versioner/)

</div>

---

## 🎯 Why Prompt Versioner?

In the rapidly evolving world of AI and Large Language Models, managing prompt versions, tracking performance, and ensuring consistent quality is crucial for production applications. **Prompt Versioner** provides enterprise-grade prompt management with:

- **🔄 Version Control**: Versioning for prompts with complete history
- **📊 Performance Tracking**: Comprehensive metrics and regression detection
- **🧪 A/B Testing**: Built-in statistical framework for prompt optimization
- **⚡ Real-time Monitoring**: Automated alerts and performance dashboards
- **👥 Team Collaboration**: Annotations, reviews, and shared insights
- **🎨 Modern UI**: Beautiful web dashboard with dark/light themes

---

## ✨ Features


<table>
<tr>
<td width="50%" valign="top">

### 🔧 Core Functionality
- **Versioning**: Automatic version management with MAJOR/MINOR/PATCH bumps
- **Metrics Tracking**: Comprehensive LLM call metrics (tokens, latency, quality, cost)
- **Export**: Backup and share prompts with full history
- **Git Integration**: Optional Git integration for version control

</td>
<td width="50%" valign="top">

### 🧪 Advanced Testing & Monitoring
- **A/B Testing**: Built-in statistical framework for comparing prompt versions
- **Performance Monitoring**: Automated regression detection and alerting
- **Real-time Analytics**: Live metrics and performance dashboards
- **Custom Alerts**: Configure thresholds for cost, latency, and quality metrics

</tr>
<tr>
</td>
<td width="50%" valign="top">

### 👥 Collaboration & Management
- **Team Annotations**: Collaborative notes and feedback system
- **Version Comparison**: Detailed diff views with change tracking
- **Search & Filtering**: Find prompts by metadata, performance, and tags

</td>
<td width="50%" valign="top">

### 🎨 Modern Web Interface
- **Interactive Dashboard**: Beautiful, responsive web UI
- **Dark/Light Themes**: Customizable interface with modern design
- **Tab Navigation**: Organized sections for Prompts, A/B Testing, Comparisons, and Alerts
- **Real-time Updates**: Live data refresh and instant feedback
</tr>
</table>

![Dashboard Overview](docs/images/dashboard-overview.png)

---


## 📦 Installation

### Prerequisites
- **Python 3.11** or higher
- **Poetry** (recommended) or pip
- **Git** (optional, for version control integration)

<table>
<tr>
<td width="50%" valign="top">

### Using Poetry (Recommended)

```bash
# Install from GitHub repository
poetry add git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally for development
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
poetry install
```
</td>
<td width="50%" valign="top">


### Using pip

```bash
# Install from GitHub repository
pip install git+https://github.com/pepes97/prompt-versioner.git

# Or clone and install locally
git clone https://github.com/pepes97/prompt-versioner.git
cd prompt-versioner
pip install -e .
```
</td>
</tr>
</table>

---

## 🚀 Quick Start


```python
from prompt_versioner import PromptVersioner, VersionBump

# Initialize the versioner
pv = PromptVersioner(project_name="my-first-project", enable_git=False)

# Create your first prompt version
pv.save_version(
    name="assistant",
    system_prompt="You are a helpful assistant.",
    user_prompt="Please answer the following question: {question}",
    bump_type=VersionBump.MAJOR
)

print("✅ Created first prompt version 1.0.0!")
```
---

## 🎨 Web Dashboard

The modern web interface provides a comprehensive view of your prompt versions, metrics, and testing results.
### Core Features

#### 📋 **Prompts Management**
- **Version History**: Complete timeline with visual diffs
- **Semantic Search**: Find prompts by content, metadata, or version
- **Bulk Operations**: Export, compare, and manage multiple versions
- **Real-time Preview**: Live rendering of prompt templates

![Prompts Management](docs/images/prompts-management.png)

#### 📊 **Metrics & Analytics**
- **Performance Tracking**: Token usage, latency, cost analysis
- **Quality Monitoring**: Success rates, quality scores over time

![Metrics Dashboard](docs/images/metrics-analytics.png)

#### 🧪 **A/B Testing**
- **Split Testing**: Compare prompt versions with statistical significance
- **Real-time Results**: Monitor test progress and early indicators

![AB Testing Interface](docs/images/ab-testing.png)

#### 🔍 **Version Comparison**
- **Visual Diff Engine**: Side-by-side prompt comparison with syntax highlighting
- **Metadata Changes**: Track parameter modifications and settings
- **Performance Delta**: Compare metrics between versions
- **Smart Annotations**: Highlight significant changes and impacts

![Version Comparison](docs/images/version-comparison.png)

#### ⚠️ **Smart Alerts**
- **Performance Degradation**: Automatic detection of quality drops
- **Cost Anomalies**: Unusual spending patterns and token usage
- **Error Rate Monitoring**: Success rate thresholds and notifications
- **Custom Metrics**: Define your own alert conditions

![Alerts System](docs/images/alerts-system.png)

---

## 💻 CLI Interface

### Core Commands

```bash
# Initialize a new project
pv init

# List all prompts
pv list

# Show all versions of a specific prompt
pv versions <prompt>

# Show details of a specific version
pv show <nome prompt> <version>

# Compare two versions (shows diff)
pv diff <nome prompt> <version 1> <version 2>

# Compare versions with metrics
pv compare <nome prompt> <version 1> <version 2>

# Delete a specific version
pv delete <nome prompt> <version>

# Rollback to a previous version
pv rollback <nome prompt> <version>

# Launch web dashboard
pv dashboard --port 5000
```

---

## 📖 Examples & Use Cases

> 💡 **All examples are fully functional and can be run directly!**

> 📂 **Examples Directory**: [`examples/`](examples/) contains complete working examples for every feature.

| Example | Description | Key Features |
|---------|-------------|--------------|
| [`basic_usage.py`](examples/basic_usage.py) | Getting started with prompt versioning | Version creation, retrieval, basic metrics |
| [`version_management.py`](examples/version_management.py) | Advanced version control operations | Semantic versioning, metadata, version comparison |
| [`metrics_tracking.py`](examples/metrics_tracking.py) | Comprehensive metrics logging | Token tracking, quality scores, cost analysis |
| [`ab_testing.py`](examples/ab_testing.py) | A/B testing framework | Statistical testing, winner determination |
| [`performance_monitoring.py`](examples/performance_monitoring.py) | Automated performance monitoring | Regression detection, alert generation |
| [`summarization_example.py`](examples/summarization_example.py) | Real-world summarization pipeline | Production-ready LLM integration |
| [`code_review.py`](examples/code_review.py) | Multi-stage code review system | Security and performance analysis |
| [`test_all_features.py`](examples/test_all_features.py) | Complete feature demonstration | End-to-end workflow testing |
| [`run_dashboard.py`](examples/run_dashboard.py) | Web dashboard launcher | Dashboard configuration and startup |
| [`clear_db.py`](examples/clear_db.py) | Database management utilities | Clean up and reset operations |

---

## 🌟 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details (TODO).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Documentation**: [Doc](https://pepes97.github.io/prompt-versioner/)
- **Issues**: [GitHub Issues](https://github.com/pepes97/prompt-versioner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pepes97/prompt-versioner/discussions)

---

<p align="center">
  <strong>Build by Sveva Pepe, an NLP Engineer</strong><br>
  <sub>Star ⭐ this project if it helps you build better AI applications!</sub>
</p>
