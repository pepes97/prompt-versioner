# CLI Utilities

Utility functions and formatters for the command-line interface.

## Overview

The CLI utilities module provides formatting, display, and helper functions used across all CLI commands. It leverages the Rich library for enhanced terminal output with colors, tables, and interactive elements.

## Formatters Module

### Overview

The formatters module (`prompt_versioner.cli.utils.formatters`) provides Rich-based formatting functions for displaying prompt data in the terminal.

```python
from prompt_versioner.cli.utils.formatters import (
    format_prompts_table,
    format_versions_table,
    format_version_detail,
    format_metrics_table,
    format_diff_output
)
```

## Functions

### format_prompts_table()

```python
def format_prompts_table(prompts: List[str], versioner: Any) -> Table
```

Format a list of prompts as a Rich table with version counts and latest version info.

**Parameters:**
- `prompts` (List[str]): List of prompt names
- `versioner` (PromptVersioner): PromptVersioner instance for data access

**Returns:**
- `Table`: Rich Table object ready for display

**Example:**
```python
from prompt_versioner import PromptVersioner
from prompt_versioner.cli.utils.formatters import format_prompts_table
from rich.console import Console

pv = PromptVersioner("my-project")
prompts = pv.list_prompts()
table = format_prompts_table(prompts, pv)

console = Console()
console.print(table)
```

**Output:**
```
┌───────────────┬───────────┬────────┐
│ Name          │ Versions  │ Latest │
├───────────────┼───────────┼────────┤
│ code-reviewer │ 5         │ 1.2.0  │
│ chatbot       │ 12        │ 2.1.0  │
│ classifier    │ 3         │ 1.0.1  │
└───────────────┴───────────┴────────┘
```

### format_versions_table()

```python
def format_versions_table(name: str, versions: List[Dict[str, Any]]) -> Table
```

Format a list of versions for a specific prompt as a Rich table.

**Parameters:**
- `name` (str): Prompt name for table title
- `versions` (List[Dict[str, Any]]): List of version dictionaries

**Returns:**
- `Table`: Rich Table object with version details

**Example:**
```python
versions = pv.list_versions("code-reviewer")
table = format_versions_table("code-reviewer", versions)
console.print(table)
```

**Output:**
```
                   Versions of 'code-reviewer'
┌─────────┬─────────────────────┬─────────────┐
│ Version │ Timestamp           │ Git Commit  │
├─────────┼─────────────────────┼─────────────┤
│ 1.2.0   │ 2025-01-15 10:30:00 │ a1b2c3d4    │
│ 1.1.0   │ 2025-01-14 16:45:00 │ e5f6g7h8    │
│ 1.0.0   │ 2025-01-10 09:15:00 │ i9j0k1l2    │
└─────────┴─────────────────────┴─────────────┘
```

### format_version_detail()

```python
def format_version_detail(name: str, version: Dict[str, Any]) -> None
```

Display detailed information about a specific version with panels and formatting.

**Parameters:**
- `name` (str): Prompt name
- `version` (Dict[str, Any]): Version data dictionary

**Side Effects:**
- Prints formatted output directly to console

**Example:**
```python
version = pv.get_version("code-reviewer", "1.2.0")
format_version_detail("code-reviewer", version)
```

**Output:**
```
╭──────────────── Prompt: code-reviewer ────────────────╮
│ Version: 1.2.0                                         │
│ Timestamp: 2025-01-15 10:30:00                         │
│ Git Commit: a1b2c3d4                                   │
╰────────────────────────────────────────────────────────╯

System Prompt:
╭────────────────────────────────────────────────────────╮
│ You are an expert code reviewer with deep knowledge    │
│ of best practices and security considerations.         │
╰────────────────────────────────────────────────────────╯

User Prompt:
╭────────────────────────────────────────────────────────╮
│ Review the following code and provide feedback:        │
│ {code}                                                 │
│                                                        │
│ Focus areas: {focus_areas}                             │
╰────────────────────────────────────────────────────────╯
```

### format_metrics_table()

```python
def format_metrics_table(metrics: Dict[str, List[float]]) -> Table
```

Format performance metrics as a statistical summary table.

**Parameters:**
- `metrics` (Dict[str, List[float]]): Dictionary mapping metric names to value lists

**Returns:**
- `Table`: Rich Table with statistical summary

**Example:**
```python
# Sample metrics data
metrics = {
    "quality_score": [0.85, 0.87, 0.86, 0.88, 0.84],
    "latency_ms": [1200, 1150, 1300, 1180, 1220],
    "cost_eur": [0.003, 0.004, 0.003, 0.004, 0.003]
}

table = format_metrics_table(metrics)
console.print(table)
```

**Output:**
```
┌──────────────┬───────┬───────┬───────┬────────┬────────┐
│ Metric       │ Count │ Mean  │ Min   │ Max    │ Std    │
├──────────────┼───────┼───────┼───────┼────────┼────────┤
│ quality_score│ 5     │ 0.860 │ 0.840 │ 0.880  │ 0.015  │
│ latency_ms   │ 5     │ 1210  │ 1150  │ 1300   │ 58.3   │
│ cost_eur     │ 5     │ 0.003 │ 0.003 │ 0.004  │ 0.0005 │
└──────────────┴───────┴───────┴───────┴────────┴────────┘
```

### format_diff_output()

```python
def format_diff_output(
    name: str,
    version_a: str,
    version_b: str,
    diff_result: DiffResult
) -> None
```

Display a formatted diff comparison between two prompt versions.

**Parameters:**
- `name` (str): Prompt name
- `version_a` (str): First version being compared
- `version_b` (str): Second version being compared
- `diff_result` (DiffResult): Diff result object

**Side Effects:**
- Prints formatted diff output directly to console

**Example:**
```python
diff = pv.diff("code-reviewer", "1.0.0", "1.1.0", format_output=False)
format_diff_output("code-reviewer", "1.0.0", "1.1.0", diff)
```

**Output:**
```
╭─────────── Diff: code-reviewer (1.0.0 → 1.1.0) ───────────╮
│ Changes: 2 additions, 0 deletions, 1 modification         │
╰────────────────────────────────────────────────────────────╯

System Prompt:
╭────────────────────────────────────────────────────────────╮
│ - You are an expert code reviewer.                        │
│ + You are an expert code reviewer with deep knowledge     │
│ + of best practices and security considerations.          │
╰────────────────────────────────────────────────────────────╯

User Prompt:
╭────────────────────────────────────────────────────────────╮
│   Review the following code and provide feedback:         │
│   {code}                                                   │
│ +                                                          │
│ + Focus areas: {focus_areas}                               │
╰────────────────────────────────────────────────────────────╯
```

## Helper Functions

### prompt_input()

```python
def prompt_input(message: str, default: str = None) -> str
```

Enhanced input prompt with Rich formatting and default value support.

**Parameters:**
- `message` (str): Prompt message to display
- `default` (str, optional): Default value if user presses Enter

**Returns:**
- `str`: User input or default value

**Example:**
```python
from prompt_versioner.cli.utils.formatters import prompt_input

name = prompt_input("Enter prompt name", default="my-prompt")
# → "Enter prompt name [my-prompt]: "
```

### confirm()

```python
def confirm(message: str, default: bool = False) -> bool
```

Interactive yes/no confirmation prompt.

**Parameters:**
- `message` (str): Confirmation message
- `default` (bool): Default response (default: False)

**Returns:**
- `bool`: True for yes, False for no

**Example:**
```python
from prompt_versioner.cli.utils.formatters import confirm

if confirm("Delete this prompt?", default=False):
    # Proceed with deletion
    pass
```

### progress_bar()

```python
def progress_bar(iterable, description: str = "Processing...")
```

Create a Rich progress bar for long-running operations.

**Parameters:**
- `iterable`: Iterable to process
- `description` (str): Description text for progress bar

**Returns:**
- Progress bar context manager

**Example:**
```python
from prompt_versioner.cli.utils.formatters import progress_bar

prompts = ["prompt1", "prompt2", "prompt3"]
with progress_bar(prompts, "Exporting prompts...") as progress:
    for prompt in progress:
        # Process each prompt
        export_prompt(prompt)
```

## Console Configuration

### Rich Console Setup

The formatters module uses a pre-configured Rich console:

```python
from rich.console import Console
from rich.theme import Theme

# Custom theme for Prompt Versioner CLI
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "magenta",
    "version": "blue",
    "metric": "green"
})

console = Console(theme=custom_theme)
```

### Color Scheme

| Element | Color | Usage |
|---------|-------|-------|
| **Info** | Cyan | General information |
| **Warning** | Yellow | Warnings and cautions |
| **Error** | Bold Red | Error messages |
| **Success** | Bold Green | Success confirmations |
| **Prompt** | Magenta | User input prompts |
| **Version** | Blue | Version numbers |
| **Metric** | Green | Performance metrics |

## Output Formats

### JSON Formatting

```python
def format_json_output(data: Any) -> str:
    """Format data as pretty-printed JSON."""
    import json
    return json.dumps(data, indent=2, ensure_ascii=False)
```

### YAML Formatting

```python
def format_yaml_output(data: Any) -> str:
    """Format data as YAML."""
    import yaml
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)
```

### CSV Formatting

```python
def format_csv_output(data: List[Dict[str, Any]]) -> str:
    """Format tabular data as CSV."""
    import csv
    import io

    if not data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
```

## Interactive Elements

### Menu Selection

```python
def select_from_menu(options: List[str], title: str = "Select an option") -> int:
    """Display interactive menu and return selected index."""
    from rich.prompt import IntPrompt

    console.print(f"\n[bold]{title}:[/bold]")
    for i, option in enumerate(options, 1):
        console.print(f"  {i}. {option}")

    choice = IntPrompt.ask(
        "Enter your choice",
        choices=[str(i) for i in range(1, len(options) + 1)]
    )
    return choice - 1
```

### Multi-line Input

```python
def multiline_input(prompt: str) -> str:
    """Get multi-line input from user."""
    console.print(f"[prompt]{prompt}[/prompt]")
    console.print("[dim]Enter your text (Ctrl+D to finish):[/dim]")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines)
```

## Usage Examples

### Complete CLI Command Output

```python
from prompt_versioner import PromptVersioner
from prompt_versioner.cli.utils.formatters import *
from rich.console import Console

def list_command():
    """Example implementation of list command."""
    console = Console()
    pv = PromptVersioner("my-project")

    try:
        # Get prompts
        prompts = pv.list_prompts()

        if not prompts:
            display_warning("No prompts found in this project")
            return

        # Display table
        table = format_prompts_table(prompts, pv)
        console.print(table)

        display_success(f"Found {len(prompts)} prompts")

    except Exception as e:
        display_error("Failed to list prompts", str(e))
```

### Interactive Prompt Creation

```python
def create_command_interactive():
    """Example interactive prompt creation."""
    console = Console()

    # Get basic info
    name = prompt_input("Prompt name")
    system_prompt = multiline_input("System prompt")
    user_prompt = multiline_input("User prompt")

    # Select bump type
    bump_options = ["major", "minor", "patch"]
    bump_index = select_from_menu(bump_options, "Version bump type")
    bump_type = bump_options[bump_index]

    # Confirm creation
    if confirm(f"Create prompt '{name}' with {bump_type} version?"):
        try:
            pv = PromptVersioner("my-project")
            version = pv.save_version(
                name=name,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                bump_type=bump_type
            )
            display_success(f"Created prompt '{name}' version {version}")
        except Exception as e:
            display_error("Failed to create prompt", str(e))
```

## See Also

- [`CLI Commands`](commands.md) - CLI commands that use these utilities
- [Rich Library](https://rich.readthedocs.io/) - Terminal formatting library
- [`PromptVersioner`](../core/versioner.md) - Core functionality accessed by CLI
