import pathlib
import tempfile

from .utils import NEXT_PORT, ProjectValidator


def test_project_layout(project_slug: str, validator: ProjectValidator):
    # Expect hidden files to be present
    validator.expect_file_exists(".coveragerc")
    validator.expect_file_exists(".gitignore")
    # Expect README file
    validator.expect_file_exists("README.md")
    # Expect python project definition
    validator.expect_file_exists("pyproject.toml")
    # Expect python project configuration
    validator.expect_file_exists("setup.cfg")
    # Expect invoke tasks file
    validator.expect_file_exists("tasks.py")
    # Expect semantic release configuration
    validator.expect_file_exists("release.config.js")
    # Expect sonar project properties
    validator.expect_file_exists("sonar-project.properties")
    # Expect Dockerfile
    validator.expect_file_exists("Dockerfile")
    # Expect mkdocs config
    validator.expect_file_exists("mkdocs.yml")
    # Expect CI pipelines
    validator.expect_file_exists(".github", "workflows", "ci.yml")
    validator.expect_file_exists(".github", "workflows", "cd.yml")
    validator.expect_file_exists(".github", "workflows", "semantic_release.yml")
    # Expect vscode config
    validator.expect_directory_exists(".vscode")
    validator.expect_file_exists(".vscode/settings.json")
    # Expect directories (files will be tested later)
    validator.expect_directory_exists("docs")
    validator.expect_directory_exists("scripts")
    # Expect test directory
    validator.expect_directory_exists("tests", "unit")
    validator.expect_directory_exists("tests", "e2e")
    validator.expect_file_exists("tests", "e2e", "conftest.py")
    validator.expect_file_exists("tests", "unit", "conftest.py")
    validator.expect_file_exists("tests", "unit", "test_version.py")
    # Expect source code directory
    validator.expect_directory_exists("src", project_slug)
    validator.expect_file_exists("src", project_slug, "__init__.py")
    validator.expect_file_exists("src", project_slug, "__about__.py")


def test_pytest_can_be_invoked(validator: ProjectValidator, project_slug: str):
    # Check command that would be executed by "test" task
    validator.expect_dry_run_output("test", match="{python} -m pytest tests/unit/")
    validator.expect_dry_run_output("test", "--e2e", match="{python} -m pytest tests/")
    validator.expect_dry_run_output(
        "test",
        "--cov",
        match=f"{{python}} -m pytest --cov src/{project_slug} tests/unit/",
    )
    validator.expect_dry_run_output(
        "test",
        "--e2e",
        "--cov",
        match=f"{{python}} -m pytest --cov src/{project_slug} tests/",
    )
    # Run test task
    validator.expect_task_successful("test")
    # Check that coverage does not exist
    validator.expect_file_does_not_exist("coverage.xml")
    validator.expect_directory_does_not_exist("coverage-report")
    # Test results should exist though
    validator.expect_file_exists("junit.xml")
    # Run test task with coverage
    validator.expect_task_successful("test", "--cov")
    # Check that test coverage files exist
    validator.expect_file_exists("coverage.xml")
    validator.expect_directory_exists("coverage-report")
    validator.expect_file_exists("junit.xml")


def test_mypy_can_be_invoked(validator: ProjectValidator, cli_option: str):
    # Check command that would be executed by "check" task
    validator.expect_dry_run_output("check", match="{python} -m mypy src/")
    validator.expect_dry_run_output(
        "check", "--include-tests", match="{python} -m mypy src/ tests/"
    )
    # mypy indicate success with number of files analyzed when done without error
    if cli_option == "No command-line interface":
        validator.expect_task_output(
            "check", match="Success: no issues found in 2 source files"
        )
        validator.expect_task_output(
            "check",
            "--include-tests",
            match="Success: no issues found in 7 source files",
        )
    else:
        validator.expect_task_output(
            "check", match="Success: no issues found in 5 source files"
        )
        validator.expect_task_output(
            "check",
            "--include-tests",
            match="Success: no issues found in 11 source files",
        )


def test_flake8_can_be_invoked(validator: ProjectValidator):
    # Check command that would be executed by "lint" task
    validator.expect_dry_run_output("lint", match="{python} -m flake8 .")
    # flake8 does not print any output when there is no error
    validator.expect_task_output("lint", match="")


def test_isort_and_black_can_be_invoked(validator: ProjectValidator, cli_option: str):
    # Check command that would be executed by "format" task
    validator.expect_dry_run_output(
        "format", match="{python} -m isort .\n{python} -m black ."
    )
    if cli_option == "No command-line interface":
        # Use subprocess.run to access both stdout and stderr at the same time
        # because isort prints output to stdout while black prints output to stderr
        validator.expect_task_outputs(
            "format",
            match_stderr="All done! ✨ 🍰 ✨\n13 files left unchanged.",
            match_stdout="Skipped 3 files",
        )
    else:
        validator.expect_task_outputs(
            "format",
            match_stderr="All done! ✨ 🍰 ✨\n17 files left unchanged.",
            match_stdout="Skipped 3 files",
        )


def test_project_can_be_built(
    validator: ProjectValidator,
    project_name: str,
    project_slug: str,
    project_version: str,
):
    # Check command that would be executed by "build" task
    validator.expect_dry_run_output(
        "build", match="{python} -m build --no-isolation --outdir dist ."
    )
    # Check command that would be executed by "build" task with "--docs" options
    validator.expect_dry_run_output(
        "build",
        "--docs",
        match=(
            "{python} -m build --no-isolation --outdir dist .\n"
            "{python} -m mkdocs build -d dist/documentation"
        ),
    )
    # Dist should not exist yet
    validator.expect_directory_does_not_exist("dist")
    # Build wheel and sdist
    validator.expect_task_successful("build")
    # Expect dist directory and files
    validator.expect_directory_exists("dist")
    validator.expect_file_exists("dist", f"{project_name}-{project_version}.tar.gz")
    validator.expect_file_exists(
        "dist", f"{project_slug}-{project_version}-py3-none-any.whl"
    )
    # Doc should not be built yet
    validator.expect_directory_does_not_exist("dist", "documentation")


def test_requirements_can_be_generated(validator: ProjectValidator):
    # Check command that would be executed by "build" task
    validator.expect_dry_run_output(
        "requirements",
        match="{python} -m piptools compile --no-header --output-file=requirements.txt --resolver=backtracking pyproject.toml",
    )
    validator.expect_dry_run_output(
        "requirements",
        "--with-hashes",
        match="{python} -m piptools compile --no-header --output-file=requirements.txt --resolver=backtracking --generate-hashes pyproject.toml",
    )
    # Requirements should not exist yet
    # Generate requirements
    validator.expect_task_successful("requirements")


def test_wheelhouse_can_be_created(validator: ProjectValidator):
    # Check command that would be executed by "wheelhouse" task
    validator.expect_dry_run_output(
        "wheelhouse", match="{python} -m pip wheel . -w dist/wheelhouse"
    )
    validator.expect_dry_run_output(
        "wheelhouse",
        "--compress",
        match=(
            "{python} -m pip wheel . -w dist/wheelhouse\n"
            "tar -czf dist/wheelhouse.tar.gz -C dist wheelhouse"
        ),
    )
    # Generate wheelhouse
    validator.expect_task_successful("wheelhouse")
    # Check that directory exists
    validator.expect_directory_exists("dist", "wheelhouse")
    # Generate wheelhouse with compressed archive
    validator.expect_task_successful("wheelhouse", "--compress")
    # Check that archive exists
    validator.expect_file_exists("dist", "wheelhouse.tar.gz")


def test_docs_can_be_built(validator: ProjectValidator):
    # Build with documentation
    validator.expect_task_successful("build", "--docs")
    # Expect documentation directory to exist
    validator.expect_directory_exists("dist", "documentation")
    # Expect index to exist
    validator.expect_file_exists("dist/documentation/index.html")
    # Expect license to exist
    validator.expect_file_exists("dist/documentation/LICENSE/index.html")
    # Expect changelog to exist
    validator.expect_file_exists("dist/documentation/CHANGELOG/index.html")


def test_docs_can_be_served_in_development_mode(validator: ProjectValidator):
    global NEXT_PORT
    process = validator.expect_task_started(
        "docs", "--no-watch", "--port", str(NEXT_PORT)
    )
    try:
        validator.expect_file_server(
            process, address=f"http://localhost:{NEXT_PORT}", method="GET", status=200
        )
    finally:
        # Terminate process
        process.terminate()
        process.wait()
        NEXT_PORT += 1


def test_docker_task_command(project_name: str, validator: ProjectValidator):
    # Check command that would be executed by "docker" task
    default_pip_config = pathlib.Path("~/.config/pip/pip.conf").expanduser()
    validator.expect_dry_run_output(
        "docker",
        match=f"docker buildx build --secret id=pip-config,src={default_pip_config} -t {project_name}:latest -f Dockerfile --provenance=false --platform='linux/amd64' .",
    )
    # Check command that would be executed by "docker" task with options
    tmp_pip_config_root = pathlib.Path(tempfile.mkdtemp())
    tmp_pip_config = tmp_pip_config_root.joinpath("pip.conf").as_posix()
    validator.expect_dry_run_output(
        "docker",
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
        "--pip-config",
        tmp_pip_config,
        match=f"docker buildx build --secret id=pip-config,src={tmp_pip_config} -t testregistry.io/test-image:test -f Dockerfile --provenance=false --push --platform='linux/arm/v7,linux/arm64,linux/amd64' --build-arg BASE_IMAGE=python:latest .",
    )
    # Pip config must have been created
    validator.expect_file_exists(tmp_pip_config)
