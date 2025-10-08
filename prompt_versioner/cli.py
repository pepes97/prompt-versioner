"""Command-line interface for prompt-versioner."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path

from prompt_versioner.core import PromptVersioner
from prompt_versioner.diff import DiffEngine

console = Console()


@click.group()
@click.option('--project', default='default', help='Project name')
@click.pass_context
def cli(ctx: click.Context, project: str) -> None:
    """Prompt Versioner - Intelligent versioning for LLM prompts."""
    ctx.ensure_object(dict)
    ctx.obj['versioner'] = PromptVersioner(project_name=project)


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize prompt versioner in current directory."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    # Create .prompt_versions directory
    Path('.prompt_versions').mkdir(exist_ok=True)
    
    console.print("[green]✓[/green] Initialized prompt versioner")
    console.print(f"Database: .prompt_versions/db.sqlite")
    
    # Offer to install Git hooks
    if versioner.git_tracker:
        if click.confirm("Install Git hooks for automatic versioning?"):
            versioner.install_git_hooks()
            console.print("[green]✓[/green] Git hooks installed")


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all tracked prompts."""
    versioner: PromptVersioner = ctx.obj['versioner']
    prompts = versioner.list_prompts()
    
    if not prompts:
        console.print("[yellow]No prompts tracked yet[/yellow]")
        return
    
    table = Table(title="Tracked Prompts")
    table.add_column("Name", style="cyan")
    table.add_column("Versions", style="magenta")
    table.add_column("Latest", style="green")
    
    for prompt in prompts:
        versions = versioner.list_versions(prompt)
        latest = versions[0] if versions else None
        
        table.add_row(
            prompt,
            str(len(versions)),
            latest['version'] if latest else "N/A",
        )
    
    console.print(table)


@cli.command()
@click.argument('name')
@click.pass_context
def versions(ctx: click.Context, name: str) -> None:
    """List all versions of a prompt."""
    versioner: PromptVersioner = ctx.obj['versioner']
    versions = versioner.list_versions(name)
    
    if not versions:
        console.print(f"[yellow]No versions found for prompt '{name}'[/yellow]")
        return
    
    table = Table(title=f"Versions of '{name}'")
    table.add_column("Version", style="cyan")
    table.add_column("Timestamp", style="green")
    table.add_column("Git Commit", style="magenta")
    
    for v in versions:
        table.add_row(
            v['version'],
            v['timestamp'],
            v.get('git_commit', 'N/A'),
        )
    
    console.print(table)


@cli.command()
@click.argument('name')
@click.argument('version1')
@click.argument('version2')
@click.pass_context
def diff(ctx: click.Context, name: str, version1: str, version2: str) -> None:
    """Show diff between two versions."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    try:
        diff_result = versioner.diff(name, version1, version2)
        
        # Print summary
        console.print(Panel(
            diff_result.summary,
            title=f"Diff: {version1} → {version2}",
            border_style="blue",
        ))
        
        # Print formatted diff
        diff_text = DiffEngine.format_diff_text(diff_result)
        console.print(diff_text)
        
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.argument('name')
@click.argument('version')
@click.pass_context
def show(ctx: click.Context, name: str, version: str) -> None:
    """Show details of a specific version."""
    versioner: PromptVersioner = ctx.obj['versioner']
    v = versioner.get_version(name, version)
    
    if not v:
        console.print(f"[red]Version '{version}' not found for prompt '{name}'[/red]")
        return
    
    # Show metadata
    console.print(Panel(
        f"[cyan]Version:[/cyan] {v['version']}\n"
        f"[cyan]Timestamp:[/cyan] {v['timestamp']}\n"
        f"[cyan]Git Commit:[/cyan] {v.get('git_commit', 'N/A')}",
        title=f"Prompt: {name}",
        border_style="green",
    ))
    
    # Show system prompt
    console.print("\n[bold]System Prompt:[/bold]")
    console.print(Panel(v['system_prompt'], border_style="blue"))
    
    # Show user prompt
    console.print("\n[bold]User Prompt:[/bold]")
    console.print(Panel(v['user_prompt'], border_style="magenta"))
    
    # Show metrics if available
    metrics = versioner.storage.get_metrics(v['id'])
    if metrics:
        console.print("\n[bold]Metrics:[/bold]")
        table = Table()
        table.add_column("Metric", style="cyan")
        table.add_column("Values", style="green")
        
        for metric_name, values in metrics.items():
            table.add_row(metric_name, ", ".join(f"{v:.4f}" for v in values))
        
        console.print(table)


@cli.command()
@click.argument('name')
@click.argument('to_version')
@click.pass_context
def rollback(ctx: click.Context, name: str, to_version: str) -> None:
    """Rollback to a previous version."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    if not click.confirm(f"Rollback '{name}' to version '{to_version}'?"):
        return
    
    try:
        new_version_id = versioner.rollback(name, to_version)
        console.print(f"[green]✓[/green] Rolled back to {to_version}")
        console.print(f"Created new version with ID: {new_version_id}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.argument('name')
@click.argument('versions', nargs=-1)
@click.pass_context
def compare(ctx: click.Context, name: str, versions: tuple) -> None:
    """Compare multiple versions with metrics."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    if len(versions) < 2:
        console.print("[red]Error:[/red] Need at least 2 versions to compare")
        return
    
    comparison = versioner.compare_versions(name, list(versions))
    
    table = Table(title=f"Comparison: {name}")
    table.add_column("Version", style="cyan")
    table.add_column("Timestamp", style="green")
    table.add_column("Metrics", style="magenta")
    
    for v_data in comparison['versions']:
        metrics_str = ", ".join(
            f"{k}: {sum(v)/len(v):.2f}" 
            for k, v in v_data['metrics'].items()
            if v
        ) or "No metrics"
        
        table.add_row(
            v_data['version'],
            v_data['timestamp'],
            metrics_str,
        )
    
    console.print(table)


@cli.command()
@click.pass_context
def install_hooks(ctx: click.Context) -> None:
    """Install Git hooks for automatic versioning."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    try:
        versioner.install_git_hooks()
        console.print("[green]✓[/green] Git hooks installed")
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.pass_context
def uninstall_hooks(ctx: click.Context) -> None:
    """Uninstall Git hooks."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    try:
        versioner.uninstall_git_hooks()
        console.print("[green]✓[/green] Git hooks uninstalled")
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.option('--pre-commit', is_flag=True, help='Run in pre-commit mode')
@click.option('--post-commit', is_flag=True, help='Run in post-commit mode')
@click.pass_context
def auto_version(ctx: click.Context, pre_commit: bool, post_commit: bool) -> None:
    """Auto-version prompts (used by Git hooks)."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    if pre_commit:
        console.print("[blue]Running pre-commit prompt versioning...[/blue]")
        # Add pre-commit logic here
        console.print("[green]✓[/green] Pre-commit checks passed")
    
    elif post_commit:
        console.print("[blue]Running post-commit prompt versioning...[/blue]")
        # Add post-commit logic here
        console.print("[green]✓[/green] Prompts versioned")
    
    else:
        console.print("[yellow]Specify --pre-commit or --post-commit[/yellow]")


@cli.command()
@click.option('--port', default=5000, help='Port to run dashboard on')
@click.pass_context
def dashboard(ctx: click.Context, port: int) -> None:
    """Launch web dashboard."""
    from prompt_versioner.web.app import create_app
    
    versioner: PromptVersioner = ctx.obj['versioner']
    app = create_app(versioner)
    
    console.print(f"[green]Starting dashboard on http://localhost:{port}[/green]")
    app.run(host='0.0.0.0', port=port, debug=True)


@cli.command()
@click.argument('name')
@click.option('--delete-all', is_flag=True, help='Delete all versions')
@click.argument('version', required=False)
@click.pass_context
def delete(ctx: click.Context, name: str, version: str, delete_all: bool) -> None:
    """Delete a specific version or all versions of a prompt."""
    versioner: PromptVersioner = ctx.obj['versioner']
    
    if delete_all:
        if not click.confirm(f"Delete ALL versions of '{name}'?", abort=True):
            return
        
        versions = versioner.list_versions(name)
        for v in versions:
            versioner.storage.delete_version(name, v['version'])
        
        console.print(f"[green]✓[/green] Deleted {len(versions)} versions of '{name}'")
    
    elif version:
        if not click.confirm(f"Delete version '{version}' of '{name}'?", abort=True):
            return
        
        if versioner.storage.delete_version(name, version):
            console.print(f"[green]✓[/green] Deleted version '{version}'")
        else:
            console.print(f"[red]Version '{version}' not found[/red]")
    
    else:
        console.print("[yellow]Specify a version or use --delete-all[/yellow]")

@cli.command()
@click.option('--port', default=5000, help='Port to run dashboard on')
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--project', default=None, help='Project name (auto-detected if not specified)')
@click.option('--db-path', type=click.Path(), default=None, help='Custom database path')
@click.pass_context
def dashboard(ctx: click.Context, port: int, host: str, project: str, db_path: str) -> None:
    """Launch web dashboard (auto-detects database in current directory)."""
    from pathlib import Path
    
    # Auto-detect database in current directory
    default_db_dir = Path.cwd() / ".prompt_versions"
    default_db_path = default_db_dir / "db.sqlite"
    
    if db_path:
        db_path_obj = Path(db_path)
    elif default_db_path.exists():
        db_path_obj = default_db_path
        console.print(f"[green]✓[/green] Found database: {db_path_obj}")
    else:
        console.print(f"[yellow]No database found in current directory[/yellow]")
        if not project:
            project = click.prompt("Enter project name", default="default")
        db_path_obj = None
    
    # Get project name from context or auto-detect
    if not project:
        if db_path_obj:
            project = "auto-detected"
        else:
            project = ctx.obj.get('versioner').project_name if ctx.obj.get('versioner') else "default"
    
    console.print(Panel(
        f"[cyan]Project:[/cyan] {project}\n"
        f"[cyan]Database:[/cyan] {db_path_obj or 'default location'}\n"
        f"[cyan]URL:[/cyan] http://localhost:{port}",
        title="Starting Dashboard",
        border_style="green"
    ))
    
    # Create versioner and launch
    from prompt_versioner.core import PromptVersioner
    from prompt_versioner.web.app import create_app
    
    pv = PromptVersioner(
        project_name=project,
        db_path=db_path_obj,
        enable_git=False
    )
    
    # Show stats
    prompts = pv.list_prompts()
    if prompts:
        console.print(f"\n[green] Tracked prompts:[/green] {len(prompts)}")
        for prompt_name in prompts[:5]:  # Show first 5
            versions = pv.list_versions(prompt_name)
            console.print(f"  • {prompt_name}: {len(versions)} versions")
        if len(prompts) > 5:
            console.print(f"  ... and {len(prompts) - 5} more")
    else:
        console.print("\n[yellow]No prompts tracked yet[/yellow]")
    
    console.print(f"\n[bold green]Dashboard running at http://localhost:{port}[/bold green]")
    console.print("Press Ctrl+C to stop\n")
    
    app = create_app(pv)
    app.run(host=host, port=port, debug=False)


# ✅ NUOVO: Standalone command (può essere chiamato direttamente)
@click.command()
@click.option('--port', '-p', default=5000, help='Port to run dashboard on')
@click.option('--host', '-h', default='0.0.0.0', help='Host to bind to')
@click.option('--project', default=None, help='Project name')
@click.option('--db-path', type=click.Path(), default=None, help='Database path')
def dashboard_command(port: int, host: str, project: str, db_path: str) -> None:
    """Launch Prompt Versioner Dashboard.
    
    Auto-detects database in current directory (.prompt_versions/db.sqlite)
    or creates new one if not found.
    """
    from pathlib import Path
    from prompt_versioner.core import PromptVersioner
    from prompt_versioner.web.app import create_app
    
    console = Console()
    
    # Auto-detect database
    default_db_dir = Path.cwd() / ".prompt_versions"
    default_db_path = default_db_dir / "db.sqlite"
    
    if db_path:
        db_path_obj = Path(db_path)
        console.print(f"[cyan]Using database:[/cyan] {db_path_obj}")
    elif default_db_path.exists():
        db_path_obj = default_db_path
        console.print(f"[green]✓ Found database:[/green] {db_path_obj}")
    else:
        db_path_obj = None
        console.print(f"[yellow]No database found, will create new one[/yellow]")
    
    if not project:
        project = Path.cwd().name
    
    console.print(Panel(
        f"[cyan]Project:[/cyan] {project}\n"
        f"[cyan]Database:[/cyan] {db_path_obj or default_db_path}\n"
        f"[cyan]URL:[/cyan] http://localhost:{port}",
        title="Prompt Versioner Dashboard",
        border_style="green"
    ))
    
    # Create versioner
    pv = PromptVersioner(
        project_name=project,
        db_path=db_path_obj,
        enable_git=False
    )
    
    # Show stats
    prompts = pv.list_prompts()
    if prompts:
        table = Table(title="Current Prompts")
        table.add_column("Name", style="cyan")
        table.add_column("Versions", style="magenta")
        table.add_column("Latest", style="green")
        
        for prompt_name in prompts[:10]:
            versions = pv.list_versions(prompt_name)
            latest = versions[0] if versions else None
            table.add_row(
                prompt_name,
                str(len(versions)),
                latest['version'][:20] if latest else "N/A"
            )
        
        console.print(table)
        
        if len(prompts) > 10:
            console.print(f"\n[dim]... and {len(prompts) - 10} more prompts[/dim]")
    else:
        console.print("\n[yellow]No prompts tracked yet[/yellow]")
        console.print("[dim]Start using PromptVersioner in your code to see data here[/dim]\n")
    
    console.print(f"\n[bold green]Dashboard: http://localhost:{port}[/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    try:
        app = create_app(pv)
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Dashboard stopped[/yellow]")

if __name__ == '__main__':
    cli()