# rename-kicad-project
[![PyPI version](https://badge.fury.io/py/rename-kicad-project.svg)](https://badge.fury.io/py/rename-kicad-project)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/rename-kicad-project.svg)](https://pypi.python.org/pypi/rename-kicad-project/)
[![CI](https://github.com/likeablob/rename-kicad-project/actions/workflows/ci.yml/badge.svg)](https://github.com/likeablob/rename-kicad-project/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/likeablob/rename-kicad-project/branch/main/graph/badge.svg)](https://codecov.io/gh/likeablob/rename-kicad-project)

**rename-kicad-project** is a nifty tool for renaming or cloning your KiCad (v4, v5) project.

## Install
```sh
python3 -m pip install --user rename-kicad-project
```
Or with [pipx](https://github.com/pypa/pipx),
```sh
pipx install rename-kicad-project
```

## Usage
```sh
# Show helps
rename-kicad-project --help

# Show helps of `rename` sub-command (see below)
rename-kicad-project rename --help
```
Or you can invoke this tool by 
```sh
python3 -m rename_kicad_project --help
```

## `rename`
In the following example, `../foo/old_project_name{.pro, .sch, ...}` will be renamed as `../foo/new_project_name.pro`, ..., respectively.
```sh
rename-kicad-project rename ../foo new_project_name

# ls ../foo
# new_project_name.pro new_project_name.sch, ...
```
You may want to run the command above with `--dry-run` (`-n`) beforehand;
```sh
rename-kicad-project -n rename ../foo new_project_name
# Renaming: /path/to/old_project_name.kicad_pcb as new_project_name.kicad_pcb
# ...
```

## `clone`
In the following example, `./foo/old_project_name{.pro, .sch, ...}` will be cloned into `/tmp/bar/new_project_name.pro`, ..., respectively.
```sh
rename-kicad-project clone ./foo /tmp/bar -p new_project_name

# ls /tmp/bar
# new_project_name.pro new_project_name.sch, ...
```
You can omit `-p` to let the tool infer the new project name like `/tmp/bar/bar.pro`.
```sh
rename-kicad-project clone ./foo /tmp/bar

# ls /tmp/bar
# bar.pro bar.sch, ...
```
Note that `/tmp/bar` will be automatically created if it doesn't exist.  
And as you expected, `--dry-run` also works with `clone`.

## How it works
For the folks who wouldn't want to rely on someone's script, here is a basic explanation of how this tool works;
1. In the given source directory, glob `*.pro` files and based on the first found one, determine the current project name. (`${PROJECT_NAME}.pro`)
2. Determine target files with globbing `${PROJECT_NAME}.*` and including some special files like `fp-lib-table`.
3. Rename the target files in place (`rename`) or copy the files into the specified destination (`clone`). That' it!

## License
MIT

## Alternatives
- https://github.com/bobc/KiRename
  - As of 2021-12, it only runs on Python 2.
