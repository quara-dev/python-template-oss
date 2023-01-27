#!/usr/bin/env bash

set -euo pipefail

rm -Rf examples
mkdir examples/

echo -e "testing without CLI"
cookiecutter --no-input . project_name="demo-project-nocli" project_slug="demo_project" -o examples > /dev/null
black --check examples/demo-project-nocli
isort examples/demo-project-nocli
flake8 examples/demo-project-nocli

echo -e "testing with Argparse"
cookiecutter --no-input . command_line_interface=Argparse project_name="demo-project-argparse" project_slug="demo_project" -o examples > /dev/null
black --check examples/demo-project-argparse
isort --check examples/demo-project-argparse
flake8 examples/demo-project-argparse


echo -e "testing with Click"
cookiecutter --no-input . command_line_interface=Click project_name="demo-project-click" project_slug="demo_project" -o examples > /dev/null
black --check examples/demo-project-click
isort --check examples/demo-project-click
flake8 examples/demo-project-click

echo -e "testing with Typer"
cookiecutter --no-input . command_line_interface=Typer project_name="demo-project-typer" project_slug="demo_project" -o examples > /dev/null
black --check examples/demo-project-typer
isort --check examples/demo-project-typer
flake8 examples/demo-project-typer


python3 "examples/demo-project-nocli/scripts/install.py" -e dev  > /dev/null
python3 "examples/demo-project-argparse/scripts/install.py" -e dev > /dev/null
python3 "examples/demo-project-click/scripts/install.py" -e dev > /dev/null
python3 "examples/demo-project-typer/scripts/install.py" -e dev > /dev/null

cd examples/demo-project-nocli && inv lint && inv format --check && inv test && inv check && cd -
cd examples/demo-project-argparse && inv lint && inv format --check && inv test && inv check && cd -
cd examples/demo-project-click && inv lint && inv format --check && inv test && inv check && cd -
cd examples/demo-project-typer && inv lint && inv format --check && inv test && inv check && cd -
