import sys
from pathlib import Path
from shutil import copyfile
from typing import Callable, List

from rename_kicad_project.logger import LogLevel, logger

KICAD_SPECIAL_FILES = ["fp-lib-table"]


class ManipulatorBaseException(Exception):
    pass


class ManipulatorFatalError(ManipulatorBaseException):
    pass


class Manipulator:
    def panic(self, msg: str, stop_by: Callable = sys.exit):
        logger.print(msg, style=LogLevel.DANGER)
        logger.print("Exitting...", style=LogLevel.DANGER)
        stop_by(1)
        raise ManipulatorFatalError(msg)

    def rename_file(self, file: Path, name: str, dry_run=False):
        logger.print(f"Renaming: {file.absolute()} as {name}")

        new_path = file.with_name(name)
        if not dry_run:
            file.rename(new_path)

        return new_path

    def copy_file(self, src: Path, dest: Path, dry_run=False):
        logger.print(f"Copying: {src.absolute()} -> {dest.absolute()}")

        if not dry_run:
            copyfile(src, dest)

    def list_target_files(self, src_dir: Path):
        project_file = next(src_dir.glob("*.pro"), None) or next(
            src_dir.glob("*.kicad_pro"), None
        )
        if project_file is None:
            return self.panic("Error: .pro  or .kicad_pro file is not found.")

        project_name = project_file.stem

        return project_name, list(src_dir.glob(f"{project_name}.*")) + [
            src_dir / x for x in KICAD_SPECIAL_FILES if (src_dir / x).exists()
        ]

    def _with_stem(self, path: Path, stem: str):
        name = f"{stem}{''.join(path.suffixes)}"
        return path.with_name(name)

    def rename_project(
        self,
        files: List[Path],
        prev_project_name: str,
        new_project_name: str,
        dry_run: bool,
    ):
        for f in files:
            if f.stem == prev_project_name:
                new_name = self._with_stem(f, new_project_name).name
                self.rename_file(f, new_name, dry_run)

    def clone_project(
        self,
        files: List[Path],
        prev_project_name: str,
        new_project_name: str,
        dest_dir: Path,
        dry_run: bool,
    ):

        for f in files:
            # Rename if the file contains project_name else just copy
            if f.stem == prev_project_name:
                new_name = self._with_stem(f, new_project_name).name
            else:
                new_name = f.name

            f_dest = dest_dir / new_name

            self.copy_file(f, f_dest, dry_run)

    def check_src_dir(self, src_dir: Path):
        if not src_dir.exists() or not src_dir.is_dir():
            return self.panic("Error: Source dir does not exists.")

    def check_dest_dir(self, dest_dir: Path, dry_run: bool):
        if dest_dir.exists() and not dest_dir.is_dir():
            return self.panic(f"Error: Destination is not directory: {dest_dir}")

        elif dest_dir.exists() and next(dest_dir.glob("*"), False):
            return self.panic(f"Error: Destination is not empty: {dest_dir}")

        elif not dest_dir.exists():
            logger.print(f"Creating dir for the new project: {dest_dir}")
            if not dry_run:
                dest_dir.mkdir()
