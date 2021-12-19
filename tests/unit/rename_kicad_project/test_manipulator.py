from pathlib import Path
from unittest.mock import MagicMock, call

import pytest
from pytest_mock import MockerFixture
from utils.fake_project import FAKE_PROJECT_NAME, FakeProject

from rename_kicad_project.cli import Manipulator
from rename_kicad_project.manipulator import ManipulatorFatalError


@pytest.fixture()
def instance():
    return Manipulator()


def test_panic__stops_process(instance: Manipulator):
    # Preparation
    mocked_stop_by = MagicMock()
    # Execution
    with pytest.raises(ManipulatorFatalError):
        instance.panic("test message", stop_by=mocked_stop_by)

    # Assertion
    mocked_stop_by.assert_called_once_with(1)


def test_rename_file__renames_file_if_not_dry_run(
    instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    project_dir, project_files = fake_project
    file_path = next(iter(project_files))
    assert not file_path.with_name("new_name").exists()

    # Execution
    new_path = instance.rename_file(file_path, "new_name")

    # Assertion
    assert not file_path.exists()
    assert new_path.exists()
    assert project_dir == new_path.parent
    assert new_path.name == "new_name"


def test_rename_file__does_not_rename_file_if_dry_run(
    instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    project_dir, project_files = fake_project
    file_path = next(iter(project_files))
    assert not file_path.with_name("new_name").exists()

    # Execution
    new_path = instance.rename_file(file_path, "new_name", dry_run=True)

    # Assertion
    assert file_path.exists()
    assert not new_path.exists()
    assert project_dir == new_path.parent


def test_copy_file__copies_file_if_not_dry_run(
    instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    _, project_files = fake_project
    src_path = next(iter(project_files))
    dest_path = src_path.with_name("new_name")
    assert not dest_path.exists()

    # Executionee
    instance.copy_file(src_path, dest_path)

    # Assertion
    assert src_path.exists()
    assert dest_path.exists()


def test_copy_file__does_not_copy_file_if_dry_run(
    instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    _, project_files = fake_project
    src_path = next(iter(project_files))
    dest_path = src_path.with_name("new_name")
    assert not dest_path.exists()

    # Execution
    instance.copy_file(src_path, dest_path, dry_run=True)

    # Assertion
    assert src_path.exists()
    assert not dest_path.exists()


def test_list_target_files__only_returns_project_files(
    instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    project_dir, project_files = fake_project
    unrelated_file = project_dir / "unrelated_file.txt"
    unrelated_file.touch()

    # Execution
    project_name, target_files = instance.list_target_files(project_dir)

    # Assertion
    assert project_name == FAKE_PROJECT_NAME
    assert sorted(target_files) == sorted(project_files)


def test_list_target_files__panics_when_there_is_no_pro_file(
    mocker: MockerFixture, instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    project_dir, _ = fake_project
    for f in project_dir.glob("*.pro"):
        f.unlink()

    mocked_panic = mocker.patch.object(instance, "panic")

    # Execution
    instance.list_target_files(project_dir)

    # Assertion
    mocked_panic.assert_called_once()


def test_rename_project__skips_specific_files(
    mocker: MockerFixture, instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    mocked_rename_file = mocker.patch.object(instance, "rename_file")

    project_dir, project_files = fake_project
    unrelated_file = project_dir / (FAKE_PROJECT_NAME + "-unrelated.file")
    unrelated_file.touch()

    new_project_name = "renamed_project"

    # Execution
    instance.rename_project(
        project_files + [unrelated_file],
        FAKE_PROJECT_NAME,
        new_project_name,
        dry_run=False,
    )

    # Assertion
    related_files = [
        "temp-project-1.pro",
        "temp-project-1.kicad_pcb",
        "temp-project-1.rules",
        "temp-project-1.sch",
    ]
    mocked_rename_file.assert_has_calls(
        [
            call(project_dir / x, x.replace(FAKE_PROJECT_NAME, new_project_name), False)
            for x in related_files
        ]
    )


def test_clone_project__renames_only_specific_files(
    mocker: MockerFixture, instance: Manipulator, fake_project: FakeProject
):
    # Preparation
    mocked_copy_file = mocker.patch.object(instance, "copy_file")

    project_dir, project_files = fake_project
    unrelated_file = project_dir / (FAKE_PROJECT_NAME + "-unrelated.file")
    unrelated_file.touch()

    new_project_name = "new_project"
    new_project_path = project_dir.parent / "renamed_project"

    # Execution
    instance.clone_project(
        project_files + [unrelated_file],
        FAKE_PROJECT_NAME,
        new_project_name,
        new_project_path,
        dry_run=False,
    )

    # Assertion
    file_names_src = [
        "temp-project-1.pro",
        "temp-project-1.kicad_pcb",
        "temp-project-1.rules",
        "temp-project-1.sch",
        "fp-lib-table",
        unrelated_file.name,
    ]
    file_names_dest = [
        new_project_name + ".pro",
        new_project_name + ".kicad_pcb",
        new_project_name + ".rules",
        new_project_name + ".sch",
        "fp-lib-table",
        unrelated_file.name,
    ]
    mocked_copy_file.assert_has_calls(
        [
            call(project_dir / f_src, new_project_path / f_dest, False)
            for f_src, f_dest in zip(file_names_src, file_names_dest)
        ]
    )


def test_check_src_dir__panics_when_src_dir_does_not_exist(
    mocker: MockerFixture, tmp_path: Path, instance: Manipulator
):
    # Preparation
    src_dir = tmp_path / "does-not-exist"
    mocked_panic = mocker.patch.object(instance, "panic")

    # Execution
    instance.check_src_dir(src_dir)

    # Assertion
    mocked_panic.assert_called_once()


def test_check_src_dir__panics_when_src_dir_is_file(
    mocker: MockerFixture, tmp_path: Path, instance: Manipulator
):
    # Preparation
    src_dir = tmp_path / "some.file"
    src_dir.touch()
    mocked_panic = mocker.patch.object(instance, "panic")

    # Execution
    instance.check_src_dir(src_dir)

    # Assertion
    mocked_panic.assert_called_once()


@pytest.mark.parametrize("dry_run", [(False), (True)])
def test_check_dest_dir__create_directory_depending_on_dry_run(
    tmp_path: Path, instance: Manipulator, dry_run: bool
):
    # Preparation
    dest_dir = tmp_path / "some_dir"

    # Execution
    instance.check_dest_dir(dest_dir, dry_run=dry_run)

    # Assertion
    is_dir_created = not dry_run
    assert dest_dir.exists() is is_dir_created
    if is_dir_created:
        assert dest_dir.is_dir()


def test_check_dest_dir__panics_when_src_dir_is_file(
    mocker: MockerFixture, tmp_path: Path, instance: Manipulator
):
    # Preparation
    dest_dir = tmp_path / "some.file"
    dest_dir.touch()
    mocked_panic = mocker.patch.object(instance, "panic")

    # Execution
    instance.check_dest_dir(dest_dir, dry_run=False)

    # Assertion
    mocked_panic.assert_called_once()


def test_check_dest_dir__panics_when_dest_dir_is_not_empty(
    mocker: MockerFixture, tmp_path: Path, instance: Manipulator
):
    # Preparation
    dest_dir = tmp_path
    some_file = dest_dir / ".some.file"
    some_file.touch()
    mocked_panic = mocker.patch.object(instance, "panic")

    # Execution
    instance.check_dest_dir(dest_dir, dry_run=False)

    # Assertion
    mocked_panic.assert_called_once()
    assert some_file.exists()
