{%- if cookiecutter.command_line_interface == "Argparse" -%}
import pytest

from {{ cookiecutter.project_slug }}.cli.app import main


def test_cli_version_flag():
    # I don't know of to test that version is displayed
    # while ensuring code coverage.
    # It is possible to call a subprocess but then coverage does not take test into account
    with pytest.raises(SystemExit, match="0"):
        main(["--version"])
{%- endif %}
{%- if cookiecutter.command_line_interface == "Click" -%}
from click.testing import CliRunner

from {{ cookiecutter.project_slug }} import __version__
from {{ cookiecutter.project_slug }}.cli.app import cli

runner = CliRunner()


def test_cli_version_flag():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__
{%- endif %}
{%- if cookiecutter.command_line_interface == "Typer" -%}
from typer.testing import CliRunner

from {{ cookiecutter.project_slug }} import __version__
from {{ cookiecutter.project_slug }}.cli.app import cli

runner = CliRunner()


def test_cli_version_flag():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__
{%- endif %}
