import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
"""
setup:
1. generate a project using cookiecutter
2. crete a virtual env and install the project dependecies
------------
tests:
3. run tests
4. run linting

cleanup/teardown:
5. remove venv
6. remove generated proj
"""


def test__liniting_passes(project_dir: "Path"):
    subprocess.run(["make", "lint-ci"], text=True, cwd=str(project_dir), capture_output=True)
    subprocess.run(["make", "lint-ci"], text=True, check=True, cwd=str(project_dir))


def test__tests_pass(project_dir: "Path"):
    subprocess.run(args=["make", "install"], check=True, cwd=project_dir)
    subprocess.run(args=["make", "test"], check=True, cwd=project_dir)
    subprocess.run(args=["make", "test-wheel-locally"], check=True, cwd=project_dir)
