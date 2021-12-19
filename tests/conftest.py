import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent))

from utils.fake_project import create_fake_project  # noqa: E402


@pytest.fixture()
def fake_project(tmp_path: Path):
    return create_fake_project(tmp_path)
