from pathlib import Path

from typing_extensions import Protocol
from utils.fake_project import FakeProject


class CaseRenameFakeProjectExecutorProtocol(Protocol):
    @staticmethod
    def run(project_dir: Path, project_name: str):
        pass  # pragma: no cover


class CaseCloneFakeProjectExecutorProtocol(Protocol):
    @staticmethod
    def run(src_dir: Path, dest_dir: Path, project_name: str):
        pass  # pragma: no cover


def case_rename_fake_project(
    fake_project: FakeProject, executor: CaseRenameFakeProjectExecutorProtocol
):
    # Preparation
    project_dir, _ = fake_project
    new_project_name = "new_project_name"

    # Execution
    executor.run(project_dir, new_project_name)

    # Assertion
    assert sorted([x.name for x in project_dir.glob("*")]) == sorted(
        [
            f"{new_project_name}.sch",
            f"{new_project_name}.pro",
            f"{new_project_name}.rules",
            "fp-lib-table",
            f"{new_project_name}.kicad_pcb",
        ]
    )


def case_clone_fake_project(
    tmp_path: Path,
    fake_project: FakeProject,
    executor: CaseCloneFakeProjectExecutorProtocol,
    dest_dir_name: str = "cloned",
    project_name: str = "new_project_name",
):
    # Preparation
    src_dir, _ = fake_project
    dest_dir = tmp_path / dest_dir_name
    new_project_name = project_name

    # Execution
    executor.run(src_dir, dest_dir, project_name)

    # Assertion
    assert sorted(
        [x.relative_to(dest_dir.parent).as_posix() for x in dest_dir.glob("*")]
    ) == sorted(
        [
            f"{dest_dir_name}/{new_project_name}.sch",
            f"{dest_dir_name}/{new_project_name}.pro",
            f"{dest_dir_name}/{new_project_name}.rules",
            f"{dest_dir_name}/fp-lib-table",
            f"{dest_dir_name}/{new_project_name}.kicad_pcb",
        ]
    )
