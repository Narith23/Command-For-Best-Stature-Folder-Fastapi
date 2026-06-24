"""Command line interface for the project generator."""

from bot.builders.project_builder import create_project
from bot.utils.name_utils import to_project_slug, to_title
from bot.utils.path_utils import ask_parent_folder


PROJECT_TYPES = {
    "1": ("api", "API only"),
    "2": ("web", "Web only"),
    "3": ("hybrid", "API + Web"),
}


def print_header() -> None:
    """Print the generator header."""

    print("=" * 70)
    print("FastAPI Project Generator")
    print("=" * 70)


def ask_project_name() -> str:
    """Ask the user for a project name."""

    while True:
        project_name = input("Enter project name: ").strip()

        if project_name:
            return project_name

        print("Project name cannot be empty.")


def ask_project_type() -> str:
    """Ask the user which project type to generate."""

    print("Select project type:")
    print("1. API only")
    print("2. Web only")
    print("3. API + Web")

    while True:
        choice = input("Choose an option [1-3]: ").strip()

        if choice in PROJECT_TYPES:
            return PROJECT_TYPES[choice][0]

        print("Please choose 1, 2, or 3.")


def print_success(project_path, project_title: str, project_type: str) -> None:
    """Print the success message after project generation."""

    project_type_label = {
        "api": "API only",
        "web": "Web only",
        "hybrid": "API + Web",
    }[project_type]

    print()
    print("Project generated successfully.")
    print(f"Name: {project_title}")
    print(f"Type: {project_type_label}")
    print(f"Path: {project_path}")
    print()
    print("Next steps:")
    print(f"  cd {project_path}")
    print("  py -3.13 -m venv .venv")
    print("  .\\.venv\\Scripts\\activate")
    print("  pip install -r requirements.txt")
    print("  python main.py")


def run() -> None:
    """Run the generator bot."""

    print_header()

    project_name = ask_project_name()
    parent_folder = ask_parent_folder()
    project_type = ask_project_type()

    project_slug = to_project_slug(project_name)
    project_title = to_title(project_name)
    project_path = parent_folder / project_slug

    create_project(project_path, project_title, project_type)
    print_success(project_path, project_title, project_type)
