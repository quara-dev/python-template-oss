"""See: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html#using-pre-post-generate-hooks-0-7-0"""
import shutil
import os
import subprocess

if {{cookiecutter.use_poetry}}:
    shutil.move("pyproject.poetry.toml", "pyproject.toml")
    os.remove("pyproject.setuptools.toml")
    shutil.move("scripts/install.poetry.py", "scripts/install.py")
    os.remove("scripts/install.setuptools.py")
else:
    shutil.move("pyproject.setuptools.toml", "pyproject.toml")
    os.remove("pyproject.poetry.toml")
    shutil.move("scripts/install.setuptools.py", "scripts/install.py")
    os.remove("scripts/install.poetry.py")

if not {{cookiecutter.azdevops}}:
    shutil.rmtree(".azuredevops")

if not {{cookiecutter.github}}:
    shutil.rmtree(".github")

if {{cookiecutter.init_git_repo}}:
    subprocess.check_call(["git", "init", "-b", "main"])
    subprocess.check_call(["git", "add", "."])
    subprocess.check_call(
        [
            "git",
            "commit",
            "-m",
            "chore(project): initialize project layout and configured development tools",
        ]
    )
