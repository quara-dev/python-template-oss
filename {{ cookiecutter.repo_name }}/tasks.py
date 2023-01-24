import typing as t
from pathlib import Path
from shutil import rmtree

from invoke import Context, task


@task
def clean(c: Context, docs: bool = False, bytecode: bool = False, extra: str = ""):
    """Clean build artifacts and optionally documentation artifacts as well as generated bytecode."""
    patterns = ["dist/*.whl", "dist/*.tar.gz"]
    if docs:
        patterns.append("dist/documentation")
    if bytecode:
        patterns.append("**/*.pyc")
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def build(c: Context, docs: bool = False):
    """Build sdist and wheel, and optionally build documentation."""
    c.run(".venv/bin/python -m build --no-isolation --outdir dist .")
    if docs:
        rmtree("dist/documentation", ignore_errors=True)
        c.run(".venv/bin/python -m mkdocs build -d dist/documentation")


@task
def wheelhouse(c: Context, clean: bool = False, compress: bool = False):
    """Build wheelhouse for the project"""
    Path("dist").mkdir(exist_ok=True)
    if clean:
        rmtree("dist/wheelhouse", ignore_errors=True)
    c.run(".venv/bin/pip wheel . -w dist/wheelhouse")
    rmtree("build", ignore_errors=True)
    if compress:
        c.run("tar -czf dist/wheelhouse.tar.gz -C dist wheelhouse")


@task
def docs(c: Context, watch: bool = True, port: int = 8000):
    """Serve the documentation in development mode."""
    cmd = f".venv/bin/python -m mkdocs serve -a localhost:{port}"
    if watch:
        cmd += " --livereload --watch docs/ --watch src"
    c.run(cmd)


@task
def test(c: Context, coverage: bool = False):
    """Run tests using pytest and optionally enable coverage."""
    cmd = ".venv/bin/python -m pytest"
    if coverage:
        cmd += " --cov src"
    c.run(cmd)


@task
def coverage(c: Context, run: bool = False, port: int = 8000):
    """Serve code coverage results and optionally run tests before serving results"""
    if run:
        test(c, True)
    c.run(f".venv/bin/python -m http.server {port} --dir coverage-report")


@task
def check(c: Context, include_tests: bool = True):
    """Run mypy typechecking."""
    cmd = ".venv/bin/python -m mypy src"
    if include_tests:
        cmd += " tests/"
    c.run(cmd)


@task
def format(c: Context):
    """Format source code using black and isort."""
    c.run(".venv/bin/isort .")
    c.run(".venv/bin/black .")


@task
def lint(c: Context):
    """Lint source code using flake8."""
    c.run(".venv/bin/flake8 .")


@task
def docker(
    c: Context,
    name: str = "{{ cookiecutter.project_name }}",
    tag: str = "latest",
    registry: t.Optional[str] = None,
    base_image: t.Optional[str] = None,
    push: bool = False,
    build: bool = False,
):
    """Build docker image for the project"""
    if build:
        wheelhouse(c, clean=True, compress=False)
    image = f"{name}:{tag}"
    if registry:
        while registry.endswith("/"):
            registry = registry[:-1]
        image = f"{registry}/{image}"
    build_args: t.Dict[str, str] = {}
    if base_image:
        build_args["BASE_IMAGE"] = base_image
    cmd = f"docker build -t {image}"
    for key, value in build_args.items():
        cmd += f" --build-arg {key}={value}"
    cmd += " ."
    c.run(cmd)
    if push:
        c.run(f"docker push {image}")


@task
def docker_cp(
    c: Context,
    platforms: str = "linux/amd64,linux/arm64",
    name: str = "{{ cookiecutter.project_name }}",
    tag: str = "latest",
    registry: t.Optional[str] = None,
    base_image: t.Optional[str] = None,
    build_image: t.Optional[str] = None,
    push: bool = False,
    load: bool = False,
    output: t.Optional[str] = None,
):
    """Build cross-platform docker image for the project"""
    image = f"{name}:{tag}"
    if registry:
        while registry.endswith("/"):
            registry = registry[:-1]
        image = f"{registry}/{image}"
    build_args: t.Dict[str, str] = {}
    if base_image:
        build_args["BASE_IMAGE"] = base_image
    if build_image:
        build_args["BUILD_IMAGE"] = build_image
    cmd = f"docker buildx build -t {image} -f Dockerfile.cross-platform"
    if push:
        cmd += " --push"
    elif load:
        cmd += " --load"
    elif output:
        cmd += f" --output=type=local,dest={output}"
    cmd += f" --platform='{platforms}'"
    for key, value in build_args.items():
        cmd += f" --build-arg {key}={value}"
    cmd += " ."
    print(cmd)
    c.run(cmd)