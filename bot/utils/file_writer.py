"""File and directory writing helpers."""

from pathlib import Path


def write_file(path: Path, content: str, overwrite: bool = False) -> None:
    """Write text content to a file."""

    if path.exists() and not overwrite:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_package_dirs(project_path: Path, dirs: list[str]) -> None:
    """Create Python package directories with __init__.py files."""

    for directory in dirs:
        package_path = project_path / directory
        package_path.mkdir(parents=True, exist_ok=True)
        init_file = package_path / "__init__.py"
        init_file.touch(exist_ok=True)


def make_normal_dirs(project_path: Path, dirs: list[str]) -> None:
    """Create normal directories with .gitkeep files."""

    for directory in dirs:
        normal_path = project_path / directory
        normal_path.mkdir(parents=True, exist_ok=True)
        gitkeep_file = normal_path / ".gitkeep"
        gitkeep_file.touch(exist_ok=True)
