from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test__can_generate_project(project_dir: "Path"):
    assert project_dir.exists()
