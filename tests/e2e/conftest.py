import subprocess
import tempfile
import typing as t
from pathlib import Path

import pytest

from .utils import ProjectValidator


@pytest.fixture(scope="module")
def project_name() -> str:
    """Project name used during tests"""
    return "test-project"


@pytest.fixture(scope="module")
def project_version() -> str:
    """Project version used during tests"""
    return "1.2.0"


@pytest.fixture(scope="module")
def project_slug(project_name: str) -> str:
    """Project slug used during tests"""
    return project_name.replace("-", "_")


@pytest.fixture(
    scope="module", params=["No command-line interface", "Argparse", "Click", "Typer"]
)
def cli_option(request):
    """Parametrized fixture providing allowed cli options"""
    return request.param


@pytest.fixture(scope="module")
def project(
    project_name: str, project_version: str, cli_option: str
) -> t.Iterator[Path]:
    """Create a project and install it in order to run unit tests."""
    with tempfile.TemporaryDirectory() as directory:
        subprocess.check_call(
            [
                "cookiecutter",
                ".",
                "--no-input",
                "--output-dir",
                directory,
                f"command_line_interface={cli_option}",
                f"project_name={project_name}",
                f"version={project_version}",
            ]
        )
        output = Path(directory) / project_name
        yield output


@pytest.fixture(scope="module")
def validator(project: Path) -> ProjectValidator:
    return ProjectValidator(project)
