"""Console script for {{cookiecutter.project_slug}}."""

import typer

from {{ cookiecutter.project_slug }} import __version__

cli = typer.Typer(name="{{ cookiecutter.project_name }}")
"""{{ cookiecutter.project_name }} CLI entrypoint."""


def version_callback(value: bool) -> None:
    """Callback to show version and exit when '--version' option is provided."""
    if value:
        print(__version__)
        raise typer.Exit()


@cli.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
) -> None:
    """CLI callback to add global options."""
    pass
