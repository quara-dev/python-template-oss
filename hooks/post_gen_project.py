"""See: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html#using-pre-post-generate-hooks-0-7-0"""
import os
import shutil
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
    $ git remote add origin git@github.com:{{ cookiecutter.repo_org }}/{{ cookiecutter.repo_name }}.git


7. Push next branch:

    $ git push -u origin next


8. Push main branch:

    $ git checkout main
    $ git push -u origin main


9. Start developping on a new branch:

    $ git checkout -b feat/my_feature_branch
"""

CLI = "{{ cookiecutter.command_line_interface }}".lower()

if CLI == "no command-line interface":
    shutil.rmtree("src/{{ cookiecutter.project_slug }}/cli")
    os.remove("src/{{ cookiecutter.project_slug }}/__main__.py")
    os.remove("tests/e2e/test_cli.py")
elif CLI == "argparse":
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.click.py")
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.typer.py")
    shutil.move(
        "src/{{ cookiecutter.project_slug }}/cli/app.argparse.py",
        "src/{{ cookiecutter.project_slug }}/cli/app.py",
    )
elif CLI == "click":
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.argparse.py")
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.typer.py")
    shutil.move(
        "src/{{ cookiecutter.project_slug }}/cli/app.click.py",
        "src/{{ cookiecutter.project_slug }}/cli/app.py",
    )
elif CLI == "typer":
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.argparse.py")
    os.remove("src/{{ cookiecutter.project_slug }}/cli/app.click.py")
    shutil.move(
        "src/{{ cookiecutter.project_slug }}/cli/app.typer.py",
        "src/{{ cookiecutter.project_slug }}/cli/app.py",
    )

subprocess.check_call([sys.executable, "./scripts/install.py", "--all"])
project_python = subprocess.check_output([sys.executable, "./scripts/install.py", "--show-python-path"]).strip().decode()
subprocess.check_call([project_python, "-m", "invoke", "requirements"])

if {{cookiecutter.init_git_repo}}:
    process = subprocess.run(
        ["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        print(process.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    subprocess.check_call(["git", "checkout", "-b", "main"], stdout=subprocess.DEVNULL)
    subprocess.check_call(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.check_call(
        [
            "git",
            "commit",
            "-m",
            "chore(project): initialize project layout and configured development tools",
        ],
        stdout=subprocess.DEVNULL,
    )
    subprocess.check_call(["git", "checkout", "-b", "next"], stdout=subprocess.DEVNULL)
    subprocess.check_call(["git", "--no-pager", "log", "--stat"])
    print(HELP)
