"""Commands for managing versions (rollback, delete)."""

import click
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import print_success, print_error, print_warning, console


@cli.command()
@click.argument("name")
@click.argument("to_version")
@click.pass_context
def rollback(ctx: click.Context, name: str, to_version: str) -> None:
    """Rollback to a previous version."""
    versioner = ctx.obj["versioner"]

    if not click.confirm(f"Rollback '{name}' to version '{to_version}'?"):
        return

    try:
        new_version_id = versioner.rollback(name, to_version)
        print_success(f"Rolled back to {to_version}")
        console.print(f"Created new version with ID: {new_version_id}")
    except ValueError as e:
        print_error(str(e))


@cli.command()
@click.argument("name")
@click.option("--delete-all", is_flag=True, help="Delete all versions")
@click.argument("version", required=False)
@click.pass_context
def delete(ctx: click.Context, name: str, version: str, delete_all: bool) -> None:
    """Delete a specific version or all versions of a prompt."""
    versioner = ctx.obj["versioner"]

    if delete_all:
        if not click.confirm(f"Delete ALL versions of '{name}'?", abort=True):
            return

        versions = versioner.list_versions(name)
        for v in versions:
            versioner.storage.delete_version(name, v["version"])

        print_success(f"Deleted {len(versions)} versions of '{name}'")

    elif version:
        if not click.confirm(f"Delete version '{version}' of '{name}'?", abort=True):
            return

        if versioner.storage.delete_version(name, version):
            print_success(f"Deleted version '{version}'")
        else:
            print_error(f"Version '{version}' not found")

    else:
        print_warning("Specify a version or use --delete-all")
