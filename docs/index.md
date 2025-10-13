# Prompt Versioner

![Prompt Versioner Logo](images/logo.svg){ align=right width="200" }

**A comprehensive Python library for managing and versioning LLM prompts, with built-in A/B testing, metric tracking, and performance monitoring capabilities.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://pepes97.github.io/prompt-versioner/)

---

## Why Prompt Versioner?

In the rapidly evolving world of AI and Large Language Models, managing prompt versions, tracking performance, and ensuring consistent quality is crucial for production applications. **Prompt Versioner** provides enterprise-grade prompt management with:

!!! tip "Key Benefits"
    - **🔄 Version Control**: Complete versioning for prompts with full history
    - **📊 Performance Tracking**: Comprehensive metrics and regression detection
    - **🧪 A/B Testing**: Built-in statistical framework for prompt optimization
    - **⚡ Real-time Monitoring**: Automated alerts and performance dashboards
    - **👥 Team Collaboration**: Annotations, reviews, and shared insights
    - **🎨 Modern UI**: Beautiful web dashboard with dark/light themes

## Quick Start

Get started with Prompt Versioner in just a few lines of code:

```python title="Basic Usage"
from prompt_versioner import PromptVersioner, VersionBump

# Initialize versioner
pv = PromptVersioner(project_name="my-ai-project", enable_git=False)

# Save your first prompt version
pv.save_version(
    name="code_reviewer",
    system_prompt="You are an expert code reviewer...",
    user_prompt="Review this code: {code}",
    bump_type=VersionBump.MAJOR,  # Creates version 1.0.0
    metadata={"type": "code_review", "author": "team"}
)

# Get the latest version
latest = pv.get_latest("code_reviewer")
print(f"✅ Latest version: {latest['version']}")
```

## What's Next?

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Get Prompt Versioner installed quickly with Poetry or pip

    [:octicons-arrow-right-24: Install now](installation.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Learn the basics with our step-by-step guide

    [:octicons-arrow-right-24: Get started](quickstart.md)

-   :material-monitor-dashboard:{ .lg .middle } **Web Dashboard**

    ---

    Explore the beautiful web interface for managing prompts

    [:octicons-arrow-right-24: View dashboard](dashboard/overview.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Detailed documentation for all classes and methods

    [:octicons-arrow-right-24: API docs](api/core.md)

</div>

## Features Overview

### Core Functionality

**Versioning**
:   Automatic version management with MAJOR/MINOR/PATCH bumps using semantic versioning

**Metrics Tracking**
:   Comprehensive LLM call metrics including tokens, latency, quality scores, and costs

**Export & Backup**
:   Complete backup and sharing capabilities with full prompt history

**Git Integration**
:   Optional Git integration for seamless version control workflows

### Advanced Testing & Monitoring

**A/B Testing**
:   Built-in statistical framework for comparing prompt versions with confidence intervals

**Performance Monitoring**
:   Automated regression detection and alerting for production environments

**Real-time Analytics**
:   Live metrics dashboards with customizable views and filters

**Custom Alerts**
:   Configurable thresholds for cost, latency, quality, and custom metrics

### Collaboration & Management

**Team Annotations**
:   Collaborative notes and feedback system for prompt development

**Version Comparison**
:   Detailed diff views with syntax highlighting and change tracking

**Search & Filtering**
:   Powerful search capabilities by metadata, performance metrics, and tags

**Modern Web Interface**
:   Beautiful, responsive UI with dark/light themes and real-time updates

---

## Community & Support

Join our growing community of developers building better AI applications:

- **GitHub**: [pepes97/prompt-versioner](https://github.com/pepes97/prompt-versioner)
- **Issues**: [Report bugs or request features](https://github.com/pepes97/prompt-versioner/issues)
- **Discussions**: [Join the community](https://github.com/pepes97/prompt-versioner/discussions)

---

*Built with ❤️ by Sveva Pepe, an NLP Engineer*
