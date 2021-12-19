#! /usr/bin/env python3
from pathlib import Path
from typing import Optional

import typer

from rename_kicad_project.manipulator import Manipulator

app = typer.Typer()
common_args = {"dry_run": False}
arg_src_dir = typer.Argument(..., help="Source KiCad project dir.")

manipulator = Manipulator()


@app.command()
def rename(
    src_dir: Path = arg_src_dir,
    new_project_name: str = typer.Argument(..., help="New project name."),
):
    """ "Rename KiCad project in place."""
    # Common args
    dry_run = common_args["dry_run"]

    manipulator.check_src_dir(src_dir)
    prev_project_name, target_files = manipulator.list_target_files(src_dir)

    manipulator.rename_project(
        target_files, prev_project_name, new_project_name, dry_run
    )


@app.command()
def clone(
    src_dir: Path = arg_src_dir,
    dest_dir: Path = typer.Argument(..., help="New project dir."),
    new_project_name: Optional[str] = typer.Option(
        None,
        "--project-name",
        "-p",
        help="New project name. By default it's inferred from 'DEST'.",
    ),
):
    """Clone KiCad project with a new project name."""
    # Common args
    dry_run = common_args["dry_run"]

    manipulator.check_src_dir(src_dir)
    prev_project_name, target_files = manipulator.list_target_files(src_dir)

    manipulator.check_dest_dir(dest_dir, dry_run)

    # Infer new_project_name from dest_dir if it's not specified
    if new_project_name is None:
        new_project_name = dest_dir.name

    manipulator.clone_project(
        target_files, prev_project_name, new_project_name, dest_dir, dry_run
    )


@app.callback()
def main(
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="Just shows possible manupilations and exits."
    )
):
    """
    Example of use:

        \b
        $ rename-kicad-project rename ../foo new_project_name
        >>> ../foo/old_project_name{.pro, .sch, ...}
            will be renamed with new_project_name.pro, ...

        \b
        $ rename-kicad-project -n rename ../project_dir new_project_name
        >>> Run the first example with --dry-run to see possible changes.

        \b
        $ rename-kicad-project clone ./foo /tmp/bar
        >>> ./foo/project_name{.pro, .sch, ...}
            will be copied into /tmp/bar/project_name.pro, ...
        >>> /tmp/bar will be automatically created if it doesn't exist yet.

        \b
        $ rename-kicad-project clone ./foo /tmp/bar -p new_project_name
        >>> ./foo/old_project_name{.pro, .sch, ...}
            will be copied into /tmp/bar/new_project_name,pro, ...
    """
    common_args["dry_run"] = dry_run
