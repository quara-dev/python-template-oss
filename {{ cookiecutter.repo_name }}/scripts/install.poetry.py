#!/usr/bin/env python3

"""Install the project in editable mode."""

import argparse
import os
import pathlib
import subprocess
import sys
import typing as t
import venv

VENV_DIR = pathlib.Path(__file__).parent.parent.resolve(True) / ".venv"


if os.name == "nt":
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"


def install_virtualenv() -> None:
    """Create a virtualenv and install dependencies"""
    venv.create(
        VENV_DIR,
        system_site_packages=False,
        clear=False,
        with_pip=True,
        prompt=None,
    )
    try:
        subprocess.run(
            [
                VENV_PYTHON,
                "-m",
                "pip",
                "install",
                "-U",
                "pip",
                "setuptools",
            ]
        )
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)


def install_project(groups: t.Optional[str] = None) -> None:
    """Installing project in editable mode using pip"""
    cmd = ["poetry", "install"]
    if groups:
        cmd += ["--with", groups]
    try:
        subprocess.run(cmd)
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)


cli_parser = argparse.ArgumentParser(
    description=(
        "Create or update virtual environment in project root directory then "
        "install project."
    )
)
cli_parser.add_argument(
    "-g",
    "--groups",
    type=str,
    required=False,
    default=None,
    help="Install additional dependency groups",
)
cli_parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    required=False,
    default=False,
    help="Install all dependency groups",
)

if __name__ == "__main__":
    args = cli_parser.parse_args()
    # Parse arguments
    groups = args.groups
    all_groups = args.all
    # First make sure virtualenv exists
    install_virtualenv()
    # Install project in development mode
    if groups:
        install_project(groups)
    elif all_groups:
        # Install all extras
        install_project("dev,doc")
    else:
        # Only install build dependencies by default
        install_project()
