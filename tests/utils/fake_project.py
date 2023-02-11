from pathlib import Path
from typing import List, Tuple

FakeProject = Tuple[Path, List[Path]]

FAKE_PROJECT_NAME = "temp-project-1"


def create_fake_project(tmp_path: Path, use_kicad_pro: bool = False) -> FakeProject:
    project_name = FAKE_PROJECT_NAME

    project_dir = tmp_path / (project_name + "-dir")
    project_dir.mkdir()

    exts = (
        ".pro" if not use_kicad_pro else ".kicad_pro",
        ".kicad_pcb",
        ".rules",
        ".sch",
    )
    file_names = [project_name + x for x in exts] + ["fp-lib-table"]
    file_paths = []
    for fn in file_names:
        file_path = project_dir / fn
        file_path.touch()
        file_paths.append(file_path)

    return project_dir, file_paths
