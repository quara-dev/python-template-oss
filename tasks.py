from invoke import Context, task



@task
def test(c: Context):
    c.run("PIP_CONFIG_FILE=/dev/null pytest -x -vvvv -s tests/")


@task
def default(c: Context):
    c.run("PIP_CONFIG_FILE=/dev/null cookiecutter . --output-dir sandbox/ --no-input")
