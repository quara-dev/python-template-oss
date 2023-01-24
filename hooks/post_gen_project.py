"""See: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html#using-pre-post-generate-hooks-0-7-0"""
import subprocess
import shutil


if not {{cookiecutter.azdevops}}:
    shutil.rmtree(".azuredevops")


if not {{cookiecutter.github}}:
    shutil.rmtree(".github")


if {{cookiecutter.init_git_repo}}:
    subprocess.check_call(["git", "init", "-b", "main"])
    subprocess.check_call(["git", "add", "."])
    subprocess.check_call([
        "git",
        "commit",
        "-m",
        "chore(project): initialize project layout and configured development tools",
    ])
