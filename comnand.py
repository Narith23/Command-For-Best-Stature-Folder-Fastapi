import os
import tkinter as tk

from tkinter import filedialog
from dependencies.item_file import (
    generate_base_response_file,
    generate_config_file,
    generate_database_file,
    generate_env_file,
    generate_gitignore_file,
    generate_logging_file,
    generate_main_file,
    generate_readme_file,
    generate_requirements_file,
)
from utils.jwt_secret_key import generate_secret_key
from utils.loading_spinner import loading_spinner


def create_folders(base_dir: str, folders: list[str]) -> None:
    """
    Create folders inside base_dir.
    Adds __init__.py to each folder except those related to tests,
    so they are treated as Python packages.
    """
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)

        if "tests" not in folder.split(os.sep):
            init_file = os.path.join(path, "__init__.py")
            try:
                with open(init_file, "w", encoding="utf-8") as f:
                    pass
            except OSError as e:
                print(f"⚠️ Warning: Failed to create {init_file}: {e}")


def create_files(base_dir: str, files: dict[str, str]) -> None:
    """
    Create files with given content inside base_dir.
    Creates parent folders if needed.
    """
    for relative_path, content in files.items():
        full_path = os.path.join(base_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            print(f"⚠️ Warning: Failed to create file {full_path}: {e}")


def ask_yes_no(question: str, default: bool = False) -> bool:
    """
    Helper to ask yes/no question with default option.
    """
    choice = input(f"\n{question} (y/n): ").strip().lower()
    if choice in ("y", "yes"):
        return True
    if choice in ("n", "no"):
        return False
    return default


def select_base_folder() -> str | None:
    """
    Opens a folder selection dialog and returns the selected folder path.
    Returns None if no folder selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select Base Folder")
    root.destroy()
    return folder_selected if folder_selected else None


def select_db_type() -> str | None:
    """Let the user select a database type from a menu."""
    db_options = ["mysql", "postgresql", "oracle"]
    print("\n🗄️  Select a database type:")
    for idx, db in enumerate(db_options, start=1):
        print(f"{idx}. {db.capitalize()}")

    choice = input("Enter number (1-3): ").strip()
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(db_options):
            return db_options[idx - 1]

    print("❌ Invalid choice. Exiting.")
    return None


def main() -> None:
    print("📂 Please select the base folder for the FastAPI project.")
    base_folder = select_base_folder()
    if not base_folder:
        print("❌ No folder selected. Exiting.")
        return

    # Ask feature options
    request_jwt = ask_yes_no("🔑 Do you want to use JWT authentication?", default=True)
    request_db = ask_yes_no("🗄️  Do you want to use a database?", default=True)

    # Database selection
    db_type = None
    if request_db:
        db_type = select_db_type()
        if not db_type:
            return
        print(f"✅ Selected database: {db_type}")

    print(f"\n📦 Creating Laravel-style FastAPI project inside: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)
    loading_spinner("Initializing project", duration=1.2)

    # Laravel-style FastAPI folder structure
    folders = [
        "app",
        "app/api/controllers",  # like Laravel Http/Controllers
        "app/api/middleware",  # request middleware
        "app/api/requests",  # Pydantic requests
        "app/api/routes",  # routes definitions
        "app/models",  # SQLAlchemy models
        "app/schemas",  # Pydantic schemas
        "app/services",  # business logic
        "app/repositories",  # DB queries
        "app/exceptions",  # custom exceptions
        "app/providers",  # DI, event providers
        "app/core",  # config, database, logging
        "app/utils",  # utils & helpers
        "database/migrations",  # alembic migrations
        "database/seeders",  # seeders
        "database/factories",  # faker factories
        "resources/views",  # Jinja2 templates
        "resources/lang",  # translations
        "public",  # static files
        "storage",  # cache, logs, uploads
        "tests",  # pytest tests
    ]

    print("\n📁 Creating folders...")
    create_folders(base_folder, folders)
    loading_spinner("Creating folders", duration=1.2)

    # Starter files
    files = {
        "README.md": generate_readme_file(),
        "requirements.txt": generate_requirements_file(
            request_db=request_db, request_jwt=request_jwt, db_type=db_type
        ),
        "main.py": generate_main_file(),
        "app/core/config.py": generate_config_file(
            request_jwt=request_jwt, request_db=request_db
        ),
        "app/core/logging.py": generate_logging_file(),
        "app/utils/base_response.py": generate_base_response_file(),
        ".env": generate_env_file(
            request_jwt=request_jwt,
            request_db=request_db,
            jwt_secret_key=generate_secret_key(),
            db_type=db_type,
        ),
        ".env.example": generate_env_file(
            request_jwt=request_jwt, request_db=request_db, db_type=db_type
        ),
        ".gitignore": generate_gitignore_file(),
        "routes/api.py": "# API routes entry (like Laravel routes/api.php)\n",
        "routes/web.py": "# Web routes entry (like Laravel routes/web.php)\n",
    }

    if request_db:
        files["app/core/database.py"] = generate_database_file(db_type=db_type)

    print("\n📝 Creating files...")
    create_files(base_folder, files)
    loading_spinner("Creating files", duration=1.2)

    print("\n✅ FastAPI project (Laravel-style) created successfully!")
    print(f"👉 Next step: cd {base_folder} && uvicorn main:app --reload")


if __name__ == "__main__":
    main()
