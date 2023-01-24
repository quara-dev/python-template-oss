from pathlib import Path
import subprocess
import tempfile
import pytest


def INV(project: Path) -> str:
    return project.joinpath(".venv/bin/inv").as_posix()


@pytest.fixture(scope="module")
def project() -> Path:
    with tempfile.TemporaryDirectory() as directory:
        subprocess.check_call([
            "cookiecutter",
            ".",
            "--no-input",
            "--output-dir",
            directory
        ])
        output = Path(directory) / "demo-project"
        subprocess.check_call(["python3", "scripts/install.py", "-e", "dev,doc"], cwd=output)
        yield output


def test_expect_files(project: Path) -> None:

    project_slug = "demo_project"

    assert project.joinpath(".coveragerc").is_file()
    assert project.joinpath(".gitignore").is_file()
    assert project.joinpath("Dockerfile").is_file()
    assert project.joinpath("Dockerfile.cross-platform").is_file()
    assert project.joinpath("mkdocs.yml").is_file()
    assert project.joinpath("pyproject.toml").is_file()
    assert project.joinpath("README.md").is_file()
    assert project.joinpath("release.config.js").is_file()
    assert project.joinpath("setup.cfg").is_file()
    assert project.joinpath("sonar-project.properties").is_file()
    assert project.joinpath("tasks.py").is_file()

    assert not project.joinpath(".azuredevops").exists()

    assert project.joinpath(".github").is_dir()
    assert project.joinpath(".vscode").is_dir()
    assert project.joinpath("docs").is_dir()
    assert project.joinpath("scripts").is_dir()
    assert project.joinpath(f"src/{project_slug}").is_dir()
    assert project.joinpath("tests").is_dir()

    assert project.joinpath(f"src/{project_slug}/__init__.py").is_file()
    assert project.joinpath(f"src/{project_slug}/__about__.py").is_file()

    assert project.joinpath("tests/conftest.py").is_file()
    assert project.joinpath("tests/test_version.py").is_file()


def test_pytest_can_be_invoked(project: Path) -> None:
    subprocess.check_call([INV(project), "test"], cwd=project)
    assert not project.joinpath("coverage.xml").exists()
    subprocess.check_call([INV(project), "test", "--coverage"], cwd=project)
    assert project.joinpath("coverage.xml").is_file()


def test_mypy_can_be_invoked(project: Path) -> None:
    subprocess.check_call([INV(project), "check"], cwd=project)
    subprocess.check_call([INV(project), "check", "--include-tests"], cwd=project)


def test_flake8_can_be_invoked(project: Path) -> None:
    subprocess.check_call([INV(project), "lint"], cwd=project)


def test_isort_and_black_can_be_invoked(project: Path) -> None:
    subprocess.check_call([INV(project), "format"], cwd=project)
