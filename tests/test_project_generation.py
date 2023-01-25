import os
import subprocess
import tempfile
import typing as t
from pathlib import Path

import pytest
import urllib3


def python(project: Path) -> str:
    if os.name == "nt":
        return f"{project}/.venv/Scripts/python"
    else:
        return f"{project}/.venv/bin/python"


def inv(project: Path, task: str, *opts: str) -> t.List[str]:
    if os.name == "nt":
        return [python(project), "-m", "invoke", task, *opts]
    else:
        return [python(project), "-m", "invoke", task, *opts]


@pytest.fixture(scope="module")
def project() -> Path:
    with tempfile.TemporaryDirectory() as directory:
        subprocess.check_call(
            ["cookiecutter", ".", "--no-input", "--output-dir", directory]
        )
        output = Path(directory) / "demo-project"
        subprocess.check_call(["python3", "scripts/install.py", "--all"], cwd=output)
        yield output


def test_project_layout(project: Path):

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


def test_pytest_can_be_invoked(project: Path):
    # Check command that would be executed by "test" task
    assert (
        subprocess.check_output(inv(project, "test", "--dry-run"), cwd=project)
        .strip()
        .decode()
        == f"{python(project)} -m pytest"
    )
    # Run test task
    subprocess.check_call(inv(project, "test"), cwd=project)
    # Check that coverage does not exist
    assert not project.joinpath("coverage.xml").exists()
    assert not project.joinpath("coverage-report").exists()
    # Test results should exist though
    assert project.joinpath("junit.xml").exists()
    # Run test task with coverage
    subprocess.check_call(inv(project, "test", "--coverage"), cwd=project)
    # Check that test coverage files exist
    assert project.joinpath("coverage.xml").is_file()
    assert project.joinpath("junit.xml").is_file()
    assert project.joinpath("coverage-report").is_dir()


def test_mypy_can_be_invoked(project: Path):
    # Check command that would be executed by "check" task
    assert (
        subprocess.check_output(inv(project, "check", "--dry-run"), cwd=project)
        .strip()
        .decode()
        == f"{python(project)} -m mypy src/"
    )
    assert (
        subprocess.check_output(
            inv(project, "check", "--include-tests", "--dry-run"), cwd=project
        )
        .strip()
        .decode()
        == f"{python(project)} -m mypy src/ tests/"
    )
    # mypy indicate success with number of files analyzed when done without error
    assert (
        subprocess.check_output(inv(project, "check"), cwd=project).strip().decode()
        == "Success: no issues found in 2 source files"
    )
    assert (
        subprocess.check_output(inv(project, "check", "--include-tests"), cwd=project)
        .strip()
        .decode()
        == "Success: no issues found in 5 source files"
    )


def test_flake8_can_be_invoked(project: Path):
    # Check command that would be executed by "lint" task
    assert (
        subprocess.check_output(inv(project, "lint", "--dry-run"), cwd=project)
        .strip()
        .decode()
        == f"{python(project)} -m flake8 ."
    )
    # flake8 does not print any output when there is no error
    assert (
        subprocess.check_output(inv(project, "lint"), cwd=project).strip().decode()
        == ""
    )


def test_isort_and_black_can_be_invoked(project: Path):
    # Check command that would be executed by "format" task
    assert subprocess.check_output(
        inv(project, "format", "--dry-run"), cwd=project
    ).strip().decode() == (
        f"{python(project)} -m isort .\n" f"{python(project)} -m black ."
    )
    # Use subprocess.run to access both stdout and stderr at the same time
    # because isort prints output to stdout while black prints output to stderr
    process = subprocess.run(
        inv(project, "format"),
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout.strip().decode() == "Skipped 3 files"
    assert process.stderr.strip().decode() == (
        "All done! ✨ 🍰 ✨\n" "11 files left unchanged."
    )


def test_project_can_be_built(project: Path):
    # Check command that would be executed by "build" task
    assert subprocess.check_output(
        inv(project, "build", "--dry-run"), cwd=project
    ).strip().decode() == (f"{python(project)} -m build --no-isolation --outdir dist .")
    assert subprocess.check_output(
        inv(project, "build", "--docs", "--dry-run"), cwd=project
    ).strip().decode() == (
        f"{python(project)} -m build --no-isolation --outdir dist .\n"
        f"{python(project)} -m mkdocs build -d dist/documentation"
    )
    # Build wheel and sdist
    subprocess.check_call(inv(project, "build"), cwd=project)
    # Expect dist directory and files
    assert project.joinpath("dist").is_dir()
    assert project.joinpath("dist/demo-project-0.1.0.tar.gz").is_file()
    assert project.joinpath("dist/demo_project-0.1.0-py3-none-any.whl").is_file()
    # Doc should not be built yet
    assert not project.joinpath("dist/documentation").exists()


def test_wheelhouse_can_be_created(project: Path):
    # Check command that would be executed by "wheelhouse" task
    assert subprocess.check_output(
        inv(project, "wheelhouse", "--dry-run"), cwd=project
    ).strip().decode() == (f"{python(project)} -m pip wheel . -w dist/wheelhouse")
    assert subprocess.check_output(
        inv(project, "wheelhouse", "--compress", "--dry-run"), cwd=project
    ).strip().decode() == (
        f"{python(project)} -m pip wheel . -w dist/wheelhouse\n"
        "tar -czf dist/wheelhouse.tar.gz -C dist wheelhouse"
    )
    # Generate wheelhouse
    subprocess.check_call(inv(project, "wheelhouse"), cwd=project)
    # Check that directory exists
    assert project.joinpath("dist/wheelhouse").is_dir()
    # Generate wheelhouse with compressed archive
    subprocess.check_call(inv(project, "wheelhouse", "--compress"), cwd=project)
    # Check that archive exists
    assert project.joinpath("dist/wheelhouse.tar.gz").is_file()


def test_docs_can_be_built(project: Path):
    # Build with documentation
    subprocess.check_call(inv(project, "build", "--docs"), cwd=project)
    # Expect documentation directory to exist
    assert project.joinpath("dist/documentation").is_dir()
    # Expect index to exist
    assert project.joinpath("dist/documentation/index.html").is_file()
    # Expect license to exist
    assert project.joinpath("dist/documentation/LICENSE/index.html").is_file()
    # Expect changelog to exist
    assert project.joinpath("dist/documentation/CHANGELOG/index.html").is_file()


def test_docs_can_be_served_in_development_mode(project: Path):
    process = subprocess.Popen(
        inv(project, "docs", "--no-watch"), stderr=subprocess.PIPE, cwd=project
    )
    try:
        total_output = ""
        while True:
            output = process.stderr.readline().decode()
            total_output += output
            if "Serving on http://localhost:8000/" in output:
                break
            if output == "" and process.poll() is not None:
                assert False, f"Documentation did not start successfully:\n {total_output}"
        http = urllib3.PoolManager()
        response = http.request(
            "GET",
            f"http://localhost:8000/",
        )
        assert response.status == 200
    finally:
        # Terminate process
        process.kill()
        process.communicate()

def test_docker_task_command(project: Path):
    # Check command that would be executed by "docker" task
    assert (
        subprocess.check_output(inv(project, "docker", "--dry-run"), cwd=project)
        .strip()
        .decode()
        == "docker build -t demo-project:latest ."
    )
    # Check command that would be executed by "docker" task with options
    assert subprocess.check_output(
        inv(
            project,
            "docker",
            "--base-image",
            "python:latest",
            "-n",
            "test-image",
            "-r",
            "testregistry.io",
            "-t",
            "test",
            "--push",
            "--dry-run",
        ),
        cwd=project,
    ).strip().decode() == (
        "docker build -t testregistry.io/test-image:test --build-arg BASE_IMAGE=python:latest .\n"
        "docker push testregistry.io/test-image:test"
    )


def test_docker_cp_task_command(project: Path):
    # Check command that would be executed by "docker" task
    assert (
        subprocess.check_output(inv(project, "docker-cp", "--dry-run"), cwd=project)
        .strip()
        .decode()
        == "docker buildx build -t demo-project:latest -f Dockerfile.cross-platform --platform='linux/amd64,linux/arm64' ."
    )
    # Check command that would be executed by "docker" task with options
    assert subprocess.check_output(
        inv(
            project,
            "docker-cp",
            "--base-image",
            "python:latest",
            "-n",
            "test-image",
            "-r",
            "testregistry.io",
            "-t",
            "test",
            "--platforms",
            "linux/arm/v7,linux/arm64,linux/amd64",
            "--push",
            "--dry-run",
        ),
        cwd=project,
    ).strip().decode() == "docker buildx build -t testregistry.io/test-image:test -f Dockerfile.cross-platform --push --platform='linux/arm/v7,linux/arm64,linux/amd64' --build-arg BASE_IMAGE=python:latest ."
