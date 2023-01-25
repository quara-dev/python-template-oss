"""See: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html#using-pre-post-generate-hooks-0-7-0"""
import shutil
import os
import subprocess
import sys


HELP = """
####### Next steps ##########


1. Visit project on GitHub:

    {{ cookiecutter.repo_url }}


2. Configure GitHub Pages to be deployed using Github Action:

    https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site


3. Create a deploy key named COMMIT_KEY and an associated action secret named COMMIT_KEY:

    # $ alias clip="clip.exe"  # WSL users only

    $ ssh-keygen -t ed25519 -f id_ed25519 -N "" -q -C ""
    $ cat id_ed25519.pub | clip  # This is the value of the deployed key
    $ cat id_ed25519 | clip # This is the value of the action secret


4. Import project in sonarcloud:

    https://sonarcloud.io/projects/create


5. Obtain project token from SonarCloud and create an action secret named SONAR_TOKEN:

    https://docs.sonarcloud.io/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud/


6. Add git origin remote:
{% if cookiecutter.github %}
    $ git remote add origin git@github.com:{{ cookiecutter.repo_org }}/{{ cookiecutter.repo_name }}.git
{%- elif cookiecutter.azdevops %}
    $ git remote add origin git@ssh.dev.azure.com:v3/{{ cookiecutter.repo_org }}/{{ cookiecutter.repo_name }}.git
{%- endif %}


7. Push next branch:

    $ git push -u origin next


8. Push main branch:

    $ git checkout main
    $ git push -u origin main


9. Start developping on a new branch:

    $ git checkout -b feat/my_feature_branch
"""

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
    process = subprocess.run(["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if process.returncode != 0:
        print(process.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    subprocess.check_call(["git", "branch", "-m", "main"], stdout=subprocess.DEVNULL)
    subprocess.check_call(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.check_call(
        [
            "git",
            "commit",
            "-m",
            "chore(project): initialize project layout and configured development tools",
        ],
        stdout=subprocess.DEVNULL
    )
    subprocess.check_call(["git", "checkout", "-b", "next"], stdout=subprocess.DEVNULL)
    subprocess.check_call(["git", "--no-pager", "log", "--stat"])
    print(HELP)


