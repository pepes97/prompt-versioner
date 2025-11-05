# CLI Commands

Command-line interface commands for Prompt Versioner operations.

## Overview

The CLI commands module provides a comprehensive command-line interface for managing prompts, versions, and project configuration. All commands are accessible through the `prompt-versioner` CLI tool.

## Available Commands

### Installation and Usage

```bash
# Install prompt-versioner
pip install git+https://github.com/pepes97/prompt-versioner.git

# Access help
prompt-versioner --help

# Command-specific help
prompt-versioner <command> --help
```

## Command Categories

### Project Management
- [`init`](#init) - Initialize a new prompt versioning project

### Prompt Operations
- [`create`](#create) - Create a new prompt version
- [`list`](#list) - List prompts and versions
- [`show`](#show) - Display prompt details

### Model Pricing & Cost Estimation
- [`models`](pricing.md#models) - List available models with pricing
- [`estimate-cost`](pricing.md#estimate-cost) - Estimate cost for specific usage
- [`compare-costs`](pricing.md#compare-costs) - Compare costs across models

### Version Management
- [`diff`](#diff) - Compare prompt versions
- [`rollback`](#rollback) - Rollback to previous version

### Analysis and Monitoring
- [`metrics`](#metrics) - View performance metrics
- [`dashboard`](#dashboard) - Launch web dashboard
- [`export`](#export) - Export prompts and data

## Command Reference

### init

Initialize a new prompt versioning project in the current directory.

```bash
prompt-versioner init [OPTIONS] PROJECT_NAME
```

**Arguments:**
- `PROJECT_NAME` (required): Name of the project to initialize

**Options:**
- `--db-path PATH`: Custom database path (default: `./prompts.db`)
- `--git / --no-git`: Enable/disable Git integration (default: enabled)
- `--template TEXT`: Project template to use
- `--force`: Overwrite existing configuration

**Examples:**
```bash
# Basic initialization
prompt-versioner init my-ai-project

# Custom database path
prompt-versioner init my-project --db-path /opt/prompts/db.sqlite

# Without Git integration
prompt-versioner init my-project --no-git

# Force overwrite existing project
prompt-versioner init my-project --force
```

**Output:**
```
✅ Initialized prompt versioner project: my-ai-project
📁 Database: ./prompts.db
🔗 Git integration: enabled
📝 Config: .prompt-versioner.yaml

Next steps:
  prompt-versioner create --help
  prompt-versioner dashboard
```

### create

Create a new prompt version.

```bash
prompt-versioner create [OPTIONS] NAME
```

**Arguments:**
- `NAME` (required): Name of the prompt to create/update

**Options:**
- `--system-prompt TEXT`: System prompt content
- `--user-prompt TEXT`: User prompt template
- `--file PATH`: Read prompts from file
- `--bump {major,minor,patch}`: Version bump type (default: patch)
- `--metadata KEY=VALUE`: Add metadata (can be used multiple times)
- `--interactive / --no-interactive`: Interactive prompt editor

**Examples:**
```bash
# Create with inline prompts
prompt-versioner create code-reviewer \
  --system-prompt "You are an expert code reviewer." \
  --user-prompt "Review this code: {code}" \
  --bump major

# Create from file
prompt-versioner create assistant --file prompts/assistant.yaml --bump minor

# Interactive creation
prompt-versioner create classifier --interactive

# With metadata
prompt-versioner create chatbot \
  --system-prompt "You are a helpful chatbot." \
  --user-prompt "User: {message}" \
  --metadata author=john.doe \
  --metadata purpose="customer support"
```

**File Format (YAML):**
```yaml
# prompts/assistant.yaml
system_prompt: "You are a helpful AI assistant."
user_prompt: "Help the user with: {request}"
metadata:
  author: "team@company.com"
  purpose: "General assistance"
```

### list

List prompts and their versions.

```bash
prompt-versioner list [OPTIONS] [NAME]
```

**Arguments:**
- `NAME` (optional): Specific prompt name to list versions for

**Options:**
- `--format {table,json,yaml}`: Output format (default: table)
- `--sort {name,version,created}`: Sort order (default: name)
- `--limit INTEGER`: Limit number of results
- `--filter TEXT`: Filter by name pattern

**Examples:**
```bash
# List all prompts
prompt-versioner list

# List versions of specific prompt
prompt-versioner list code-reviewer

# JSON output
prompt-versioner list --format json

# Filter by pattern
prompt-versioner list --filter "chat*"

# Limited results
prompt-versioner list --limit 10 --sort created
```

**Output:**
```
┌──────────────┬─────────┬─────────────────────┬────────────────┐
│ Name         │ Version │ Created             │ Author         │
├──────────────┼─────────┼─────────────────────┼────────────────┤
│ code-reviewer│ 1.2.0   │ 2025-01-15 10:30:00 │ john.doe       │
│ chatbot      │ 2.1.0   │ 2025-01-15 09:15:00 │ team@company   │
│ classifier   │ 1.0.1   │ 2025-01-14 16:45:00 │ ai-team        │
└──────────────┴─────────┴─────────────────────┴────────────────┘
```

### show

Display detailed information about a prompt or version.

```bash
prompt-versioner show [OPTIONS] NAME [VERSION]
```

**Arguments:**
- `NAME` (required): Prompt name
- `VERSION` (optional): Specific version (default: latest)

**Options:**
- `--format {text,json,yaml}`: Output format (default: text)
- `--include-metrics`: Include performance metrics
- `--include-annotations`: Include team annotations

**Examples:**
```bash
# Show latest version
prompt-versioner show code-reviewer

# Show specific version
prompt-versioner show code-reviewer 1.0.0

# Include metrics and annotations
prompt-versioner show chatbot --include-metrics --include-annotations

# JSON output
prompt-versioner show classifier --format json
```

**Output:**
```
📝 Prompt: code-reviewer
🏷️  Version: 1.2.0
📅 Created: 2025-01-15 10:30:00
👤 Author: john.doe@company.com

📋 System Prompt:
You are an expert code reviewer with deep knowledge of best practices.

📝 User Prompt:
Review the following code and provide feedback:
{code}

Focus on: {focus_areas}

📊 Metadata:
  purpose: code review automation
  model_target: gpt-4o
  languages: ["python", "javascript", "go"]
```

### diff

Compare two versions of a prompt.

```bash
prompt-versioner diff [OPTIONS] NAME VERSION_A VERSION_B
```

**Arguments:**
- `NAME` (required): Prompt name
- `VERSION_A` (required): First version to compare
- `VERSION_B` (required): Second version to compare

**Options:**
- `--format {text,unified,side-by-side}`: Diff display format
- `--context INTEGER`: Number of context lines (default: 3)
- `--ignore-whitespace`: Ignore whitespace changes
- `--output PATH`: Save diff to file

**Examples:**
```bash
# Basic diff
prompt-versioner diff code-reviewer 1.0.0 1.1.0

# Side-by-side comparison
prompt-versioner diff chatbot 1.0.0 2.0.0 --format side-by-side

# Save diff to file
prompt-versioner diff classifier 1.0.0 1.0.1 --output changes.diff

# Ignore whitespace
prompt-versioner diff assistant 1.1.0 1.2.0 --ignore-whitespace
```

**Output:**
```
📊 Diff: code-reviewer (1.0.0 → 1.1.0)

📋 System Prompt:
- You are an expert code reviewer.
+ You are an expert code reviewer with deep knowledge of best practices.

📝 User Prompt:
  Review the following code and provide feedback:
  {code}
+
+ Focus on: {focus_areas}

📈 Summary:
  • Added: 2 lines
  • Removed: 0 lines
  • Modified: 1 line
```

### metrics

View and analyze performance metrics for prompts.

```bash
prompt-versioner metrics [OPTIONS] [NAME] [VERSION]
```

**Arguments:**
- `NAME` (optional): Prompt name to analyze
- `VERSION` (optional): Specific version (default: latest)

**Options:**
- `--format {table,chart,json}`: Output format
- `--period {day,week,month}`: Time period for analysis
- `--limit INTEGER`: Limit number of metrics records
- `--export PATH`: Export metrics to file

**Examples:**
```bash
# Overview of all prompts
prompt-versioner metrics

# Specific prompt metrics
prompt-versioner metrics code-reviewer

# Specific version metrics
prompt-versioner metrics chatbot 1.2.0

# Weekly analysis with chart
prompt-versioner metrics classifier --period week --format chart

# Export to CSV
prompt-versioner metrics --export metrics.csv
```

**Output:**
```
📊 Metrics Summary: code-reviewer v1.2.0

🎯 Performance (Last 30 days):
  Average Quality Score: 0.87 ± 0.05
  Average Latency: 1,247ms ± 324ms
  Success Rate: 98.5%
  Total Requests: 1,247

💰 Cost Analysis:
  Total Cost: €12.45
  Cost per Request: €0.01
  Token Usage: 245,670 tokens

📈 Trends:
  Quality: ↗️  +3.2% vs previous week
  Latency: ↘️  -8.1% vs previous week
  Cost: ↗️  +1.5% vs previous week
```

### dashboard

Launch the interactive web dashboard.

```bash
prompt-versioner dashboard [OPTIONS]
```

**Options:**
- `--host TEXT`: Host to bind to (default: localhost)
- `--port INTEGER`: Port to bind to (default: 8080)
- `--debug`: Enable debug mode
- `--open / --no-open`: Open browser automatically (default: open)

**Examples:**
```bash
# Launch dashboard
prompt-versioner dashboard

# Custom host and port
prompt-versioner dashboard --host 0.0.0.0 --port 3000

# Debug mode without auto-opening browser
prompt-versioner dashboard --debug --no-open
```

**Output:**
```
🚀 Starting Prompt Versioner Dashboard...

📍 Local:   http://localhost:8080
🌐 Network: http://192.168.1.100:8080

✨ Features available:
  • Prompt management and editing
  • Version comparison and diffs
  • Metrics visualization and analysis
  • A/B testing management
  • Team annotations and collaboration

Press Ctrl+C to stop the server
```

### export

Export prompts and associated data.

```bash
prompt-versioner export [OPTIONS] [NAME]
```

**Arguments:**
- `NAME` (optional): Specific prompt to export (default: all)

**Options:**
- `--output PATH`: Output file or directory
- `--format {json,yaml,csv}`: Export format (default: json)
- `--include-metrics`: Include performance metrics
- `--include-annotations`: Include team annotations
- `--version VERSION`: Specific version to export

**Examples:**
```bash
# Export all prompts
prompt-versioner export --output backup.json

# Export specific prompt
prompt-versioner export code-reviewer --output code-reviewer.yaml --format yaml

# Export with metrics and annotations
prompt-versioner export chatbot \
  --include-metrics \
  --include-annotations \
  --output chatbot-full.json

# Export specific version
prompt-versioner export classifier --version 1.0.0 --output classifier-v1.json
```

### rollback

Rollback a prompt to a previous version.

```bash
prompt-versioner rollback [OPTIONS] NAME TO_VERSION
```

**Arguments:**
- `NAME` (required): Prompt name
- `TO_VERSION` (required): Version to rollback to

**Options:**
- `--bump {major,minor,patch}`: Version bump for rollback (default: patch)
- `--reason TEXT`: Reason for rollback
- `--confirm / --no-confirm`: Skip confirmation prompt

**Examples:**
```bash
# Rollback with confirmation
prompt-versioner rollback code-reviewer 1.0.0

# Rollback with reason
prompt-versioner rollback chatbot 1.5.0 --reason "Critical bug in 2.0.0"

# Force rollback without confirmation
prompt-versioner rollback classifier 1.0.1 --no-confirm --bump major
```

**Output:**
```
⚠️  Rollback Operation

📝 Prompt: code-reviewer
🔄 From: 1.2.0 → 1.0.0
🏷️  New Version: 1.2.1 (rollback)

❓ This will create a new version based on 1.0.0. Continue? [y/N]: y

✅ Rollback completed successfully!
📦 New version: 1.2.1
📝 Reason: User requested rollback to stable version
```

## See Also

- [`PromptVersioner`](../core/versioner.md) - Python API that powers these commands
- [`CLI Utils`](utils.md) - Utility functions used by CLI commands
- [Configuration Guide](../../getting-started/configuration.md) - Detailed configuration options
