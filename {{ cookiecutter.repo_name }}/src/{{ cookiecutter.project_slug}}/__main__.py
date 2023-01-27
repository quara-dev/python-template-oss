{%- if cookiecutter.command_line_interface == "Argparse" -%}
import sys

from demo_project_argparse.cli.app import main

if __name__ == "__main__":
    sys.exit(main())
{%- endif %}
{%- if cookiecutter.command_line_interface == "Click" -%}
import sys

from demo_project_argparse.cli.app import cli

if __name__ == "__main__":
    sys.exit(cli())
{%- endif %}
{%- if cookiecutter.command_line_interface == "Typer" -%}
from demo_project_argparse.cli.app import cli

if __name__ == "__main__":
    cli()
{%- endif %}
