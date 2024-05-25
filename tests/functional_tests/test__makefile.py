import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test__liniting_passes(project_dir: "Path"):
    subprocess.run(["make", "lint-ci"], text=True, cwd=project_dir, capture_output=True)
    subprocess.run(["make", "lint-ci"], text=True, check=True, cwd=project_dir)


def test__tests_pass(project_dir: "Path"):
    subprocess.run(args=["make", "install"], check=True, cwd=project_dir)
    subprocess.run(args=["make", "test"], check=True, cwd=project_dir)
    subprocess.run(args=["make", "test-wheel-locally"], check=True, cwd=project_dir)
