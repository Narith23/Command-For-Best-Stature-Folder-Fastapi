"""Project creation orchestration."""

from pathlib import Path

from bot.builders.api_builder import create_api_files
from bot.builders.common_builder import (
    create_app_main,
    create_common_files,
    create_readme,
    create_vendor_files,
)
from bot.builders.web_builder import create_web_files
from bot.utils.file_writer import make_normal_dirs, make_package_dirs


COMMON_PACKAGE_DIRS = [
    "app",
    "app/Http",
    "app/Http/Controllers",
    "app/Providers",
    "bootstrap",
    "config",
    "routes",
    "vendor",
    "vendor/helpers",
]

API_PACKAGE_DIRS = [
    "app/Http/Controllers/Api",
    "app/Http/Requests",
    "app/Http/Resources",
    "app/Models",
    "app/Services",
]

WEB_PACKAGE_DIRS = [
    "app/Http/Controllers/Web",
]

COMMON_NORMAL_DIRS = [
    "database/migrations",
    "database/seeders",
    "storage/framework",
    "storage/logs",
]

API_NORMAL_DIRS = [
    "tests",
]

WEB_NORMAL_DIRS = [
    "public/css",
    "public/js",
    "public/images",
    "resources/views/layouts",
]


def create_project(project_path: Path, project_title: str, project_type: str) -> None:
    """Create a new FastAPI project."""

    if project_type not in {"api", "web", "hybrid"}:
        raise ValueError("project_type must be 'api', 'web', or 'hybrid'")

    if project_path.exists():
        answer = input(
            f"Project folder already exists: {project_path}\n"
            "Continue and overwrite generated files? [y/N]: "
        ).strip().lower()

        if answer not in {"y", "yes"}:
            raise SystemExit("Project generation cancelled.")

    package_dirs = list(COMMON_PACKAGE_DIRS)
    normal_dirs = list(COMMON_NORMAL_DIRS)

    if project_type in {"api", "hybrid"}:
        package_dirs.extend(API_PACKAGE_DIRS)
        normal_dirs.extend(API_NORMAL_DIRS)

    if project_type in {"web", "hybrid"}:
        package_dirs.extend(WEB_PACKAGE_DIRS)
        normal_dirs.extend(WEB_NORMAL_DIRS)

    project_path.mkdir(parents=True, exist_ok=True)
    make_package_dirs(project_path, package_dirs)
    make_normal_dirs(project_path, normal_dirs)

    create_common_files(project_path, project_title, project_type)
    create_vendor_files(project_path)
    create_app_main(project_path, project_title, project_type)

    if project_type in {"api", "hybrid"}:
        create_api_files(project_path)

    if project_type in {"web", "hybrid"}:
        create_web_files(project_path)

    create_readme(project_path, project_title, project_type)
