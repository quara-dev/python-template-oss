"""Console script for {{cookiecutter.project_slug}}."""

import click

from {{ cookiecutter.project_slug }} import __version__


@click.group()
@click.help_option("-h", "--help")
@click.version_option(__version__, message="%(version)s")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """{{ cookiecutter.project_name }} CLI entrypoint."""
    pass


if __name__ == "__main__":
    cli()
