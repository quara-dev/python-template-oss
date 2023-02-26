{%- if cookiecutter.command_line_interface == "Argparse" -%}
import sys

from {{ cookiecutter.project_slug }}.cli.app import main

if __name__ == "__main__":
    sys.exit(main())
{%- endif %}
{%- if cookiecutter.command_line_interface == "Click" -%}
import sys

from {{ cookiecutter.project_slug }}.cli.app import cli

if __name__ == "__main__":
    sys.exit(cli())
{%- endif %}
{%- if cookiecutter.command_line_interface == "Typer" -%}
from {{ cookiecutter.project_slug }}.cli.app import cli

if __name__ == "__main__":
    cli()
{%- endif %}
