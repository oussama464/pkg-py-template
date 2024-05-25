import json
import pathlib
import shutil
import subprocess
from copy import deepcopy
from typing import Generator
from uuid import uuid4

import pytest

THIS_DIR = pathlib.Path(__file__).parent
PROJECT_DIR = (THIS_DIR / "../" / "../").resolve()


def generate_test_session_id() -> str:
    return str(uuid4())[:6]


def initialize_git_repo(repo_dir: pathlib.Path) -> None:
    subprocess.run(["git", "init"], check=True, cwd=repo_dir)
    subprocess.run(["git", "add", "--all"], check=True, cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", "'initial commit'"], check=True, cwd=repo_dir)


@pytest.fixture(scope="session")
def cookiecutter_config():
    return {"default_context": {"repo_name": f"test-repo-{generate_test_session_id()}"}}


@pytest.fixture(scope="session")
def tmp_test_config_fpath(cookiecutter_config):
    template_values = deepcopy(cookiecutter_config)
    cookiecutter_config_fpath = PROJECT_DIR / f"cookiecutter-test-config-{generate_test_session_id()}.json"
    with cookiecutter_config_fpath.open("w") as f:
        json.dump(template_values, f)
    yield cookiecutter_config_fpath
    cookiecutter_config_fpath.unlink()


@pytest.fixture(scope="session")
def project_dir(cookiecutter_config, tmp_test_config_fpath) -> Generator[pathlib.Path, None, None]:
    generated_dir: pathlib.Path = PROJECT_DIR / "sample" / cookiecutter_config["default_context"]["repo_name"]
    cmd = [
        "cookiecutter",
        str(PROJECT_DIR),
        "--output-dir",
        str(PROJECT_DIR / "sample"),
        "--config-file",
        str(tmp_test_config_fpath),
        "--no-input",
    ]
    print(" ".join(cmd))
    try:
        subprocess.run(
            cmd,
            check=True,
        )
        initialize_git_repo(generated_dir)
        yield generated_dir
    finally:
        subprocess.run(["make", "clean"], check=True, cwd=generated_dir)
    shutil.rmtree(generated_dir)
