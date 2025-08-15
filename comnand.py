import os
import tkinter as tk
from tkinter import filedialog
from dependencies.item_file import (
    generate_base_response_file,
    generate_config_file,
    generate_database_file,
    generate_env_file,
    generate_gitignore_file,
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


def main() -> None:
    print("Please select the base folder for the FastAPI project.")
    base_folder = select_base_folder()
    if not base_folder:
        print("❌ No folder selected. Exiting.")
        return

    # Ask for JWT authentication usage
    request_jwt = (
        input("\n🔑 Do you want to use JWT authentication? (y/n): ").strip().lower()
    )
    if request_jwt == "y":
        request_jwt = True
    else:
        request_jwt = False

    # Ask for database usage
    request_db = input("\n📦 Do you want to use a database? (y/n): ").strip().lower()
    if request_db == "y":
        request_db = True
    else:
        request_db = False
    
    if request_db:
        # Ask for database type
        connection_type = (
            input("\n🔑 What type of database do you want to use? (mysql/postgres): ")
            .strip()
            .lower()
        )

    print(f"\n📦 Creating FastAPI project inside: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)
    loading_spinner("Initializing project", duration=1.5)

    folders = [
        "app",
        "app/api/form",
        "app/api/router",
        "app/api/schema",
        "app/core",
        "app/db",
        "app/dependencies",
        "app/services",
        "app/utils",
        "tests",
    ]

    print("\n📁 Creating folders...")
    create_folders(base_folder, folders)
    loading_spinner("Creating folders", duration=1.5)

    # Define starter files
    files = {
        "README.md": generate_readme_file(),
        "requirements.txt": generate_requirements_file(),
        "main.py": generate_main_file(),
        "app/core/config.py": generate_config_file(
            request_jwt=request_jwt, request_db=request_db
        ),
        "app/utils/base_response.py": generate_base_response_file(),
        ".env": generate_env_file(
            request_jwt=request_jwt,
            request_db=request_db,
            jwt_secret_key=generate_secret_key(),
        ),
        ".env.example": generate_env_file(
            request_jwt=request_jwt, request_db=request_db
        ),
        ".gitignore": generate_gitignore_file(),
    }
    
    if request_db:
        files["app/core/database.py"] = generate_database_file(connection_type)

    print("\n📝 Creating files...")
    create_files(base_folder, files)
    loading_spinner("Creating files", duration=1.5)

    print("\n✅ FastAPI project structure created successfully!")


if __name__ == "__main__":
    main()
