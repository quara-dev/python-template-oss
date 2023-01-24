#!/usr/bin/env python3

"""Install the project in editable mode."""

import argparse
import os
import pathlib
import subprocess
import sys
import venv

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve(True)
VENV_DIR = ROOT_DIR / ".venv"
REQUIREMENTS = ROOT_DIR / "requirements.txt"
REQUIREMENTS_DOCS = ROOT_DIR / "requirements-docs.txt"


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
        symlinks=False,
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
                "wheel",
            ]
        )
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)


def install_requirements(install_docs_requirements: bool = False) -> None:
    """Installing requirements"""
    try:
        subprocess.run([VENV_PYTHON, "-m", "pip", "install", "-r", REQUIREMENTS.as_posix()])
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)
    if install_docs_requirements:
        try:
            subprocess.run([VENV_PYTHON, "-m", "pip", "install", "-r", REQUIREMENTS_DOCS.as_posix()])
        except Exception:
            # No need to print traceback, error will be printed from subprocess stderr
            sys.exit(1)

cli_parser = argparse.ArgumentParser(
    description=(
        "Create or update virtual environment in project root directory then "
        "install requirement."
    )
)
cli_parser.add_argument("--docs", action="store_true", default=False)


if __name__ == "__main__":
    args = cli_parser.parse_args()
    docs = args.docs
    # First make sure virtualenv exists
    install_virtualenv()
    # Install project in development mode
    install_requirements(docs)
