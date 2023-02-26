import os
import subprocess
import typing as t
from pathlib import Path

import urllib3

NEXT_PORT = 8000


def python(project: Path) -> str:
    """Get path to virtual environment python."""
    if os.name == "nt":
        return f"{project}/.venv/Scripts/python"
    else:
        return f"{project}/.venv/bin/python"


def inv(project: Path, task: str, *opts: str) -> t.List[str]:
    """Invoke a python task;"""
    return [python(project), "-m", "invoke", task, *opts]


class ProjectValidator:
    def __init__(self, project: Path) -> None:
        self.project = project

    def expect_file_exists(self, *file: str) -> None:
        assert self.project.joinpath(*file).is_file()

    def expect_file_does_not_exist(self, *file: str) -> None:
        assert not self.project.joinpath(*file).exists()

    def expect_directory_exists(self, *directory: str) -> None:
        assert self.project.joinpath(*directory).is_dir()

    def expect_directory_does_not_exist(self, *directory: str) -> None:
        assert not self.project.joinpath(*directory).exists()

    def expect_task_output(self, task: str, *opts: str, match: str) -> None:
        match = match.format(python=python(self.project))
        output = (
            subprocess.check_output(inv(self.project, task, *opts), cwd=self.project)
            .strip()
            .decode()
        )
        assert output == match, f"Expected: '{match}'. Got: '{output}'"

    def expect_task_outputs(
        self, task: str, *opts: str, match_stdout: str, match_stderr: str
    ) -> None:
        match_stdout = match_stdout.format(python=python(self.project))
        match_stderr = match_stderr.format(python=python(self.project))
        process = subprocess.run(
            inv(self.project, task, *opts),
            cwd=self.project,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert process.returncode == 0
        stdout = process.stdout.strip().decode()
        assert stdout == match_stdout, f"Expected: '{match_stdout}'. Got: '{stdout}'"
        stderr = process.stderr.strip().decode()
        assert stderr == match_stderr, f"Expected: '{match_stderr}'. Got: '{stderr}'"

    def expect_task_successful(self, task: str, *opts: str) -> None:
        subprocess.check_call(inv(self.project, task, *opts), cwd=self.project)

    def expect_task_started(self, task: str, *opts: str) -> subprocess.Popen:
        process = subprocess.Popen(
            inv(self.project, task, *opts), stderr=subprocess.PIPE, cwd=self.project
        )
        assert process.poll() is None
        return process

    def expect_dry_run_output(self, task: str, *opts: str, match: str) -> None:
        match = match.format(python=python(self.project))
        self.expect_task_output(task, *opts, "--dry-run", match=match)

    def expect_file_server(
        self,
        process: subprocess.Popen,
        address: str = "http://localhost:8000/",
        method: str = "GET",
        status: int = 200,
    ) -> None:
        """Expect that a file server is running within given process."""
        total_output = ""
        while True:
            output = process.stderr.readline().decode()
            total_output += output
            if f"Serving on {address}" in output:
                break
            if output == "" and process.poll() is not None:
                assert False, f"Fileserver did not start successfully:\n {total_output}"
        http = urllib3.PoolManager()
        response = http.request(
            method,
            address,
        )
        assert response.status == status, f"Expected: {status}. Got: {response.status}"
