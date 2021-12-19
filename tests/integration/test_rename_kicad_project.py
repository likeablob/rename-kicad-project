import subprocess
import sys
from pathlib import Path

import pytest
from utils.common_case import (
    CaseCloneFakeProjectExecutorProtocol,
    CaseRenameFakeProjectExecutorProtocol,
    case_clone_fake_project,
    case_rename_fake_project,
)
from utils.fake_project import FakeProject

IS_WIN32 = sys.platform.startswith("win32")
EXECUTABLE = ["python", "-m", "rename_kicad_project"]

if IS_WIN32:
    EXECUTABLE = ["poetry", "run", "python", "-m", "rename_kicad_project"]


@pytest.mark.skipif(IS_WIN32, reason="win32")
def test_cmd__runs_with_console_scripts():
    # Execution
    v = subprocess.run(
        ["rename-kicad-project", "--help"],
        capture_output=True,
        text=True,
    )
    print(v)

    # Assertion
    assert v.returncode == 0


def test_cmd_rename__renames_files(fake_project: FakeProject):
    # Preparation
    class executor(CaseRenameFakeProjectExecutorProtocol):
        @staticmethod
        def run(project_dir: Path, project_name: str):
            # Execution
            v = subprocess.run(
                [
                    *EXECUTABLE,
                    "rename",
                    str(project_dir.absolute()),
                    project_name,
                ],
                capture_output=True,
                text=True,
            )
            print(v)

            # Assertion
            assert v.returncode == 0

    case_rename_fake_project(fake_project, executor)


def test_cmd_clone__copies_files_with_project_name(
    tmp_path: Path, fake_project: FakeProject
):
    # Preparation
    class executor(CaseCloneFakeProjectExecutorProtocol):
        @staticmethod
        def run(src_dir: Path, dest_dir: Path, project_name: str):
            # Execution
            v = subprocess.run(
                [
                    *EXECUTABLE,
                    "clone",
                    str(src_dir),
                    str(dest_dir),
                    "-p",
                    project_name,
                ],
                capture_output=True,
                text=True,
            )
            print(v)

            # Assertion
            assert v.returncode == 0

    case_clone_fake_project(tmp_path, fake_project, executor)


def test_cmd_clone__copies_files_without_project_name(
    tmp_path: Path, fake_project: FakeProject
):
    # Preparation
    class executor(CaseCloneFakeProjectExecutorProtocol):
        @staticmethod
        def run(src_dir: Path, dest_dir: Path, project_name: str):
            # Execution
            v = subprocess.run(
                [
                    *EXECUTABLE,
                    "clone",
                    str(src_dir),
                    str(dest_dir),
                ],
                capture_output=True,
                text=True,
            )
            print(v)

            # Assertion
            assert v.returncode == 0

    case_clone_fake_project(tmp_path, fake_project, executor, project_name="cloned")
